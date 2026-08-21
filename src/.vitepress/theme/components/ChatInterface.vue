<template>
  <div class="chat-container">
    <!-- Header: Trạng thái và Chọn Mô hình -->
    <div class="chat-header">
      <div class="status-indicator">
        <span class="dot" :class="{ online: ollamaOnline, offline: !ollamaOnline }"></span>
        <span class="status-text">
          Ollama: {{ ollamaOnline ? 'Sẵn sàng' : 'Không kết nối' }}
        </span>
      </div>
      
      <div v-if="ollamaOnline" class="model-selector">
        <label for="model-select">Mô hình LLM: </label>
        <select id="model-select" v-model="selectedModel">
          <option v-for="model in availableModels" :key="model.name" :value="model.name">
            {{ model.name }}
          </option>
        </select>
      </div>
      <div v-else class="offline-warning">
        <span>Chạy chế độ: Chỉ tìm kiếm tài liệu (Search-only)</span>
      </div>
    </div>

    <!-- Khung hiển thị tin nhắn -->
    <div class="messages-area" ref="messagesArea">
      <div v-if="messages.length === 0" class="welcome-screen">
        <div class="welcome-icon">🤖</div>
        <h3>Xin chào! Tôi có thể giúp gì cho bạn?</h3>
        <p>Hỏi tôi về bất kỳ tài liệu nào bạn đã lưu trữ trong thư mục nghiên cứu, dịch thuật hoặc tài liệu cá nhân.</p>
        <div class="suggested-prompts">
          <button @click="usePrompt('Làm sao để thêm tài liệu mới?')">Làm sao để thêm tài liệu mới?</button>
          <button @click="usePrompt('Tương lai của trí tuệ nhân tạo là gì?')">Tương lai của trí tuệ nhân tạo là gì?</button>
        </div>
      </div>

      <div v-for="(msg, idx) in messages" :key="idx" class="message-wrapper" :class="msg.sender">
        <div class="avatar">{{ msg.sender === 'user' ? '👤' : '🤖' }}</div>
        <div class="message-content-box">
          <div class="message-text" v-html="renderMarkdown(msg.text)"></div>
          
          <!-- Nguồn tham khảo nếu có -->
          <div v-if="msg.links && msg.links.length > 0" class="sources-box">
            <span class="sources-title">Nguồn tham khảo:</span>
            <div class="sources-list">
              <a v-for="(link, lIdx) in msg.links" 
                 :key="lIdx" 
                 :href="link.path" 
                 class="source-badge"
                 title="Xem tài liệu gốc">
                📂 {{ link.title }}
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Tin nhắn đang chờ -->
      <div v-if="loading && currentStreamText === ''" class="message-wrapper bot loading">
        <div class="avatar">🤖</div>
        <div class="message-content-box">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Nhập câu hỏi -->
    <div class="input-area">
      <textarea 
        v-model="inputVal" 
        placeholder="Nhập câu hỏi của bạn tại đây... (Nhấn Enter để gửi)" 
        @keydown.enter.prevent="sendMessage"
        :disabled="loading"
        rows="2"
      ></textarea>
      <button @click="sendMessage" :disabled="loading || inputVal.trim() === ''" class="send-btn">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
          <path fill="currentColor" d="M3.4 22a.8.8 0 0 1-.7-1.1L6.6 12 2.7 3.1a.8.8 0 0 1 .7-1.1c.3 0 .7.1.9.3l17 8.5a.8.8 0 0 1 0 1.4l-17 8.5c-.2.1-.5.3-.9.3z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

const messages = ref([]);
const inputVal = ref('');
const loading = ref(false);
const currentStreamText = ref('');
const messagesArea = ref(null);

// Cấu hình Ollama
const ollamaOnline = ref(false);
const availableModels = ref([]);
const selectedModel = ref('');

// 1. Kiểm tra trạng thái kết nối Ollama khi Component được load
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:11434/api/tags');
    if (res.ok) {
      const data = await res.json();
      if (data.models && data.models.length > 0) {
        availableModels.value = data.models;
        // Ưu tiên chọn các model thông dụng nếu có
        const preferred = ['qwen2', 'llama3', 'mistral', 'gemma'];
        let matched = data.models.find(m => preferred.some(p => m.name.toLowerCase().includes(p)));
        selectedModel.value = matched ? matched.name : data.models[0].name;
        ollamaOnline.value = true;
      }
    }
  } catch (e) {
    console.warn("Không kết nối được tới Ollama local. Chạy chế độ chỉ tìm kiếm.");
    ollamaOnline.value = false;
  }
});

// Cuộn xuống tin nhắn mới nhất
const scrollToBottom = async () => {
  await nextTick();
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight;
  }
};

// Đề xuất câu hỏi nhanh
const usePrompt = (text) => {
  inputVal.value = text;
  sendMessage();
};

// Hàm định dạng Markdown cơ bản để hiển thị nội dung tin nhắn
const renderMarkdown = (text) => {
  if (!text) return '';
  // Convert các dòng code block ```js ... ```
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre class="chat-code-block"><code class="language-${lang}">${code.trim()}</code></pre>`;
  });
  
  // Convert inline code `code`
  html = html.replace(/`([^`]+)`/g, '<code class="chat-inline-code">$1</code>');
  
  // Convert xuống dòng
  html = html.replace(/\n/g, '<br/>');
  
  return html;
};

// Gửi tin nhắn và thực hiện RAG
const sendMessage = async () => {
  const query = inputVal.value.trim();
  if (!query || loading.value) return;

  // 1. Thêm câu hỏi của User vào khung chat
  messages.value.push({ sender: 'user', text: query });
  inputVal.value = '';
  loading.value = true;
  currentStreamText.value = '';
  scrollToBottom();

  try {
    // 2. Gọi API tìm kiếm vector cục bộ
    const searchRes = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    if (!searchRes.ok) throw new Error("Lỗi kết nối tới cơ sở dữ liệu Vector.");
    const searchData = await searchRes.json();
    
    // Tách nguồn tham khảo để hiển thị liên kết
    const uniqueLinks = [];
    const seenLinks = new Set();
    searchData.forEach(item => {
      // Chuẩn hóa tên tiêu đề hiển thị (bỏ phần "Đoạn x")
      const baseTitle = item.title.replace(/\s*\(Đoạn\s+\d+\)/g, '');
      if (!seenLinks.has(item.link)) {
        seenLinks.add(item.link);
        uniqueLinks.push({ title: baseTitle, path: item.link });
      }
    });

    if (searchData.length === 0) {
      messages.value.push({
        sender: 'bot',
        text: "Không tìm thấy tài liệu nào trong cơ sở dữ liệu liên quan đến câu hỏi của bạn. Hãy thử chạy cập nhật chỉ mục bằng lệnh `npm run index`.",
        links: []
      });
      loading.value = false;
      scrollToBottom();
      return;
    }

    // 3. Nếu Ollama KHÔNG Online -> Chỉ hiển thị các bài viết liên quan tìm được
    if (!ollamaOnline.value) {
      let botResponse = "Tôi tìm thấy một số bài viết liên quan trong tài liệu của bạn:\n\n";
      searchData.forEach((item, index) => {
        botResponse += `**${index + 1}. ${item.title}**\n${item.text.slice(0, 200)}...\n\n`;
      });
      messages.value.push({
        sender: 'bot',
        text: botResponse,
        links: uniqueLinks
      });
      loading.value = false;
      scrollToBottom();
      return;
    }

    // 4. Nếu Ollama Online -> Thực hiện gọi RAG Streaming
    const contextText = searchData.map(item => `[Nguồn: ${item.title}]\n${item.text}`).join('\n\n');
    const prompt = `Sử dụng các thông tin tham khảo sau đây để trả lời câu hỏi của người dùng một cách chi tiết bằng Tiếng Việt. Nếu thông tin không liên quan trực tiếp, hãy cố gắng trả lời tốt nhất dựa trên ngữ cảnh và kiến thức của bạn, nhưng nêu rõ thông tin nào nằm ngoài tài liệu.
    
Thông tin tham khảo:
${contextText}

Câu hỏi: ${query}`;

    // Tạo tin nhắn trống của Bot để stream chữ vào
    const botMessageIdx = messages.value.push({
      sender: 'bot',
      text: '',
      links: uniqueLinks
    }) - 1;

    const ollamaRes = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: selectedModel.value,
        prompt: prompt,
        stream: true
      })
    });

    if (!ollamaRes.ok) throw new Error("Lỗi khi kết nối với mô hình Ollama.");

    const reader = ollamaRes.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value, { stream: true });
      // Xử lý JSON Lines từ Ollama
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.trim()) {
          try {
            const parsed = JSON.parse(line);
            currentStreamText.value += parsed.response;
            messages.value[botMessageIdx].text = currentStreamText.value;
            scrollToBottom();
          } catch (e) {
            // Bỏ qua lỗi dòng dở dang
          }
        }
      }
    }

  } catch (err) {
    console.error(err);
    messages.value.push({
      sender: 'bot',
      text: `Đã xảy ra lỗi: ${err.message}. Vui lòng thử lại.`,
      links: []
    });
    scrollToBottom();
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid rgba(128, 128, 128, 0.2);
  border-radius: 12px;
  background-color: var(--vp-c-bg-soft);
  margin: 20px 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: var(--vp-c-bg-mute);
  border-bottom: 1px solid rgba(128, 128, 128, 0.15);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot.online {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.dot.offline {
  background-color: #ef4444;
}

.status-text {
  font-size: 13px;
  font-weight: 500;
}

.model-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.model-selector select {
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid rgba(128, 128, 128, 0.3);
  background-color: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  outline: none;
}

.offline-warning {
  font-size: 12px;
  color: #f59e0b;
}

/* Messages Area */
.messages-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: var(--vp-c-bg);
}

.welcome-screen {
  text-align: center;
  margin: auto;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.welcome-icon {
  font-size: 48px;
}

.welcome-screen p {
  font-size: 14px;
  color: var(--vp-c-text-2);
}

.suggested-prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 12px;
}

.suggested-prompts button {
  padding: 8px 14px;
  font-size: 13px;
  background-color: var(--vp-c-bg-soft);
  border: 1px solid rgba(128, 128, 128, 0.2);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.suggested-prompts button:hover {
  background-color: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

/* Message Bubble */
.message-wrapper {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message-wrapper.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-wrapper.bot {
  align-self: flex-start;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--vp-c-bg-mute);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  border: 1px solid rgba(128, 128, 128, 0.2);
  flex-shrink: 0;
}

.message-content-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14.5px;
  line-height: 1.5;
  background-color: var(--vp-c-bg-soft);
  border: 1px solid rgba(128, 128, 128, 0.1);
  color: var(--vp-c-text-1);
  word-break: break-word;
}

.user .message-text {
  background-color: var(--vp-c-brand-soft);
  border-color: rgba(99, 102, 241, 0.2);
  border-top-right-radius: 2px;
}

.bot .message-text {
  border-top-left-radius: 2px;
}

/* Sources */
.sources-box {
  margin-top: 4px;
}

.sources-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 4px;
}

.sources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.source-badge {
  display: inline-block;
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 6px;
  background-color: var(--vp-c-bg-mute);
  border: 1px solid rgba(128, 128, 128, 0.2);
  color: var(--vp-c-brand-1) !important;
  text-decoration: none !important;
  transition: all 0.2s;
}

.source-badge:hover {
  background-color: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
}

/* Input Area */
.input-area {
  display: flex;
  padding: 12px;
  background-color: var(--vp-c-bg-mute);
  border-top: 1px solid rgba(128, 128, 128, 0.15);
  gap: 8px;
  align-items: center;
}

.input-area textarea {
  flex: 1;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid rgba(128, 128, 128, 0.3);
  background-color: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  outline: none;
  font-size: 14px;
  resize: none;
  font-family: inherit;
  transition: border-color 0.2s;
}

.input-area textarea:focus {
  border-color: var(--vp-c-brand-1);
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background-color: var(--vp-c-brand-1);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s;
}

.send-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.send-btn:disabled {
  background-color: var(--vp-c-bg-soft);
  color: var(--vp-c-text-3);
  cursor: not-allowed;
  border: 1px solid rgba(128, 128, 128, 0.2);
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 20px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: var(--vp-c-text-3);
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.3s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -1.1s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: -0.9s;
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>

<style>
/* Style cho code block nằm bên trong tin nhắn */
.chat-code-block {
  background-color: var(--vp-c-bg-mute) !important;
  border: 1px solid rgba(128, 128, 128, 0.2);
  border-radius: 6px;
  padding: 10px 14px;
  margin: 8px 0;
  overflow-x: auto;
  font-family: monospace;
  font-size: 13px;
}

.chat-inline-code {
  background-color: var(--vp-c-bg-mute);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
  border: 1px solid rgba(128, 128, 128, 0.15);
}
</style>
