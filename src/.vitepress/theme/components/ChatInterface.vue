<template>
  <div class="chat-wrapper">
    <!-- Header: Trạng thái kết nối và chọn Mô hình -->
    <div class="chat-header">
      <div class="header-left">
        <div class="status-badge" :class="{ online: ollamaOnline, offline: !ollamaOnline }">
          <span class="pulse-dot"></span>
          <span class="status-text">
            Ollama: {{ ollamaOnline ? 'Sẵn sàng' : 'Không kết nối' }}
          </span>
        </div>
      </div>
      
      <div class="header-right">
        <div v-if="ollamaOnline" class="model-select-wrapper">
          <svg class="icon-brain" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.07 19.55 10.47 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/>
          </svg>
          <select v-model="selectedModel" class="model-dropdown">
            <option v-for="model in availableModels" :key="model.name" :value="model.name">
              {{ model.name }}
            </option>
          </select>
        </div>
        <div v-else class="search-mode-badge">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14">
            <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
          Chỉ tìm kiếm tài liệu (Search-only)
        </div>
      </div>
    </div>

    <!-- Khung hiển thị cuộc hội thoại -->
    <div class="chat-messages" ref="messagesArea">
      <!-- Màn hình chào mừng trống -->
      <div v-if="messages.length === 0" class="welcome-container">
        <div class="welcome-avatar">
          <div class="avatar-glow"></div>
          <span class="avatar-emoji">🤖</span>
        </div>
        <h2 class="welcome-title">Xin chào! Tôi là Trợ Lý AI của bạn</h2>
        <p class="welcome-subtitle">
          Tôi có thể đọc hiểu và tìm kiếm ngữ nghĩa trên toàn bộ kho tài liệu dịch thuật, nghiên cứu và tài liệu cá nhân của bạn.
        </p>
        
        <div class="prompt-suggestions-box">
          <span class="suggestions-label">Gợi ý câu hỏi nhanh:</span>
          <div class="suggestions-grid">
            <button class="suggestion-card" @click="usePrompt('Làm sao để thêm tài liệu mới?')">
              <span class="card-icon">📂</span>
              <span class="card-text">Làm sao để thêm tài liệu mới?</span>
            </button>
            <button class="suggestion-card" @click="usePrompt('Tương lai của trí tuệ nhân tạo là gì?')">
              <span class="card-icon">🧠</span>
              <span class="card-text">Tương lai của trí tuệ nhân tạo là gì?</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Tin nhắn hội thoại -->
      <div v-for="(msg, idx) in messages" :key="idx" class="message-row" :class="msg.sender">
        <div class="message-avatar-circle" :class="msg.sender">
          {{ msg.sender === 'user' ? '👤' : '🤖' }}
        </div>
        
        <div class="message-bubble-wrapper">
          <div class="message-bubble">
            <div class="message-text" v-html="renderMarkdown(msg.text)"></div>
          </div>
          
          <!-- Hiển thị nguồn tham khảo -->
          <div v-if="msg.links && msg.links.length > 0" class="message-sources">
            <div class="sources-header">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" height="12">
                <path fill="currentColor" d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
              </svg>
              Nguồn tham khảo tài liệu:
            </div>
            <div class="sources-container">
              <a v-for="(link, lIdx) in msg.links" 
                 :key="lIdx" 
                 :href="link.path" 
                 class="source-item"
                 title="Mở tài liệu này">
                <span class="source-icon">📄</span>
                <span class="source-name">{{ link.title }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Typing indicator -->
      <div v-if="loading && currentStreamText === ''" class="message-row bot loading-state">
        <div class="message-avatar-circle bot">🤖</div>
        <div class="message-bubble-wrapper">
          <div class="message-bubble loading-bubble">
            <div class="loader-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Nhập nội dung chát (Dạng Capsule hiện đại) -->
    <div class="chat-input-container">
      <div class="input-capsule">
        <textarea 
          ref="inputTextArea"
          v-model="inputVal" 
          placeholder="Hỏi tôi bất kỳ điều gì về tài liệu của bạn... (Enter để gửi)" 
          @keydown.enter.prevent="sendMessage"
          @input="adjustTextareaHeight"
          :disabled="loading"
          rows="1"
          class="chat-textarea"
        ></textarea>
        
        <button 
          @click="sendMessage" 
          :disabled="loading || inputVal.trim() === ''" 
          class="chat-send-btn"
          aria-label="Gửi tin nhắn"
        >
          <svg class="send-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
            <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </div>
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
const inputTextArea = ref(null);

// Cấu hình Ollama
const ollamaOnline = ref(false);
const availableModels = ref([]);
const selectedModel = ref('');

// Kiểm tra Ollama
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:11434/api/tags');
    if (res.ok) {
      const data = await res.json();
      if (data.models && data.models.length > 0) {
        availableModels.value = data.models;
        const preferred = ['qwen2', 'llama3', 'mistral', 'gemma'];
        let matched = data.models.find(m => preferred.some(p => m.name.toLowerCase().includes(p)));
        selectedModel.value = matched ? matched.name : data.models[0].name;
        ollamaOnline.value = true;
      }
    }
  } catch (e) {
    console.warn("Không thể kết nối đến Ollama local. Chạy chế độ chỉ tìm kiếm.");
    ollamaOnline.value = false;
  }
});

const scrollToBottom = async () => {
  await nextTick();
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight;
  }
};

const usePrompt = (text) => {
  inputVal.value = text;
  sendMessage();
};

// Tự động co giãn chiều cao khung nhập liệu
const adjustTextareaHeight = () => {
  const ta = inputTextArea.value;
  if (!ta) return;
  ta.style.height = 'auto';
  ta.style.height = Math.min(ta.scrollHeight, 150) + 'px';
};

const renderMarkdown = (text) => {
  if (!text) return '';
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  
  // Format code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre class="chat-code-block"><code class="language-${lang}">${code.trim()}</code></pre>`;
  });
  
  // Format inline code
  html = html.replace(/`([^`]+)`/g, '<code class="chat-inline-code">$1</code>');
  
  // Bold
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Line breaks
  html = html.replace(/\n/g, '<br/>');
  
  return html;
};

const sendMessage = async () => {
  const query = inputVal.value.trim();
  if (!query || loading.value) return;

  messages.value.push({ sender: 'user', text: query });
  inputVal.value = '';
  loading.value = true;
  currentStreamText.value = '';
  
  // Reset textarea height
  if (inputTextArea.value) {
    inputTextArea.value.style.height = 'auto';
  }
  
  scrollToBottom();

  try {
    const searchRes = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    if (!searchRes.ok) throw new Error("Lỗi kết nối tới cơ sở dữ liệu Vector.");
    const searchData = await searchRes.json();
    
    const uniqueLinks = [];
    const seenLinks = new Set();
    searchData.forEach(item => {
      const baseTitle = item.title.replace(/\s*\(Đoạn\s+\d+\)/g, '');
      if (!seenLinks.has(item.link)) {
        seenLinks.add(item.link);
        uniqueLinks.push({ title: baseTitle, path: item.link });
      }
    });

    if (searchData.length === 0) {
      messages.value.push({
        sender: 'bot',
        text: "Không tìm thấy tài liệu nào trong thư mục của bạn có nghĩa tương đương câu hỏi này. Bạn hãy thử thêm tài liệu và chạy `npm run index` để cập nhật cơ sở dữ liệu.",
        links: []
      });
      loading.value = false;
      scrollToBottom();
      return;
    }

    if (!ollamaOnline.value) {
      let botResponse = "Tôi đã quét cơ sở dữ liệu tài liệu cục bộ của bạn và tìm thấy các bài viết có nội dung liên quan nhất sau đây:\n\n";
      searchData.forEach((item, index) => {
        botResponse += `**${index + 1}. ${item.title}**\n*...${item.text.trim()}...*\n\n`;
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

    const contextText = searchData.map(item => `[Tài liệu: ${item.title}]\n${item.text}`).join('\n\n');
    const prompt = `Sử dụng các thông tin tham khảo sau đây để trả lời câu hỏi của người dùng một cách chi tiết bằng Tiếng Việt. Nếu thông tin không liên quan trực tiếp, hãy cố gắng trả lời tốt nhất dựa trên ngữ cảnh và kiến thức của bạn, nhưng nêu rõ thông tin nào nằm ngoài tài liệu.
    
Thông tin tham khảo:
${contextText}

Câu hỏi: ${query}`;

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
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.trim()) {
          try {
            const parsed = JSON.parse(line);
            currentStreamText.value += parsed.response;
            messages.value[botMessageIdx].text = currentStreamText.value;
            scrollToBottom();
          } catch (e) {
            // ignore
          }
        }
      }
    }

  } catch (err) {
    console.error(err);
    messages.value.push({
      sender: 'bot',
      text: `Đã xảy ra lỗi hệ thống: ${err.message}. Vui lòng thử kiểm tra lại kết nối.`,
      links: []
    });
    scrollToBottom();
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 650px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-gutter);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.12),
              0 1px 3px rgba(0, 0, 0, 0.05);
  margin: 24px 0;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.chat-wrapper:hover {
  border-color: var(--vp-c-brand-2);
  box-shadow: 0 12px 35px -8px rgba(99, 102, 241, 0.08),
              0 1px 4px rgba(0, 0, 0, 0.04);
}

/* Header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: var(--vp-c-bg-alt);
  border-bottom: 1px solid var(--vp-c-gutter);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.online {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-badge.offline {
  background: rgba(244, 63, 94, 0.1);
  color: #f43f5e;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: currentColor;
}

.online .pulse-dot {
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.model-select-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--vp-c-bg);
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-gutter);
}

.icon-brain {
  color: var(--vp-c-brand-1);
}

.model-dropdown {
  border: none;
  background: transparent;
  color: var(--vp-c-text-1);
  font-size: 13px;
  font-weight: 500;
  outline: none;
  cursor: pointer;
}

.search-mode-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #eab308;
  background: rgba(234, 179, 8, 0.08);
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 500;
}

/* Messages Area */
.chat-messages {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: var(--vp-c-bg);
  scrollbar-width: thin;
}

/* Welcome Screen */
.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  max-width: 500px;
  text-align: center;
  padding: 40px 20px;
}

.welcome-avatar {
  position: relative;
  width: 70px;
  height: 70px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--vp-c-brand-1), #ec4899);
  filter: blur(14px);
  opacity: 0.35;
  animation: glow-pulse 3s infinite ease-in-out;
}

@keyframes glow-pulse {
  0%, 100% { transform: scale(0.9); opacity: 0.3; }
  50% { transform: scale(1.15); opacity: 0.55; }
}

.avatar-emoji {
  font-size: 38px;
  position: relative;
  z-index: 1;
}

.welcome-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, var(--vp-c-brand-1) 0%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 14.5px;
  color: var(--vp-c-text-2);
  line-height: 1.5;
  margin-bottom: 28px;
}

.prompt-suggestions-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestions-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--vp-c-text-3);
  letter-spacing: 0.5px;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

@media (max-width: 600px) {
  .suggestions-grid {
    grid-template-columns: 1fr;
  }
}

.suggestion-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-gutter);
  border-radius: 12px;
  text-align: left;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.suggestion-card:hover {
  background: var(--vp-c-bg);
  border-color: var(--vp-c-brand-1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
}

.card-icon {
  font-size: 18px;
}

.card-text {
  font-size: 13px;
  font-weight: 500;
  color: var(--vp-c-text-1);
}

/* Chat bubble styling */
.message-row {
  display: flex;
  gap: 14px;
  width: 100%;
  animation: fade-in 0.3s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-row.user {
  flex-direction: row-reverse;
}

.message-avatar-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-avatar-circle.user {
  background: linear-gradient(135deg, var(--vp-c-brand-2) 0%, var(--vp-c-brand-1) 100%);
  color: white;
}

.message-avatar-circle.bot {
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-gutter);
  color: var(--vp-c-text-1);
}

.message-bubble-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 78%;
}

.user .message-bubble-wrapper {
  align-items: flex-end;
}

.message-bubble {
  padding: 12px 18px;
  border-radius: 16px;
  font-size: 14.5px;
  line-height: 1.55;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.user .message-bubble {
  background: linear-gradient(135deg, var(--vp-c-brand-1) 0%, #4f46e5 100%);
  color: white;
  border-top-right-radius: 4px;
}

.bot .message-bubble {
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-gutter);
  color: var(--vp-c-text-1);
  border-top-left-radius: 4px;
}

/* Nguồn tham khảo */
.message-sources {
  margin-top: 4px;
  width: 100%;
}

.sources-header {
  font-size: 11px;
  font-weight: 600;
  color: var(--vp-c-text-3);
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sources-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.source-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-gutter);
  font-size: 12px;
  font-weight: 500;
  color: var(--vp-c-brand-1) !important;
  text-decoration: none !important;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.source-item:hover {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  transform: scale(1.02);
}

/* Loader dots */
.loader-dots {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
}

.loader-dots span {
  width: 6px;
  height: 6px;
  background-color: var(--vp-c-text-3);
  border-radius: 50%;
  display: inline-block;
  animation: dot-bounce 1.4s infinite ease-in-out both;
}

.loader-dots span:nth-child(1) { animation-delay: -0.32s; }
.loader-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}

/* Input Capsule styling */
.chat-input-container {
  padding: 16px 24px 20px 24px;
  background: var(--vp-c-bg);
  border-top: 1px solid var(--vp-c-gutter);
}

.input-capsule {
  display: flex;
  align-items: flex-end;
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-gutter);
  border-radius: 24px;
  padding: 8px 10px 8px 18px;
  gap: 10px;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.input-capsule:focus-within {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  box-shadow: 0 0 0 3px var(--vp-c-brand-soft);
}

.chat-textarea {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--vp-c-text-1);
  font-size: 14.5px;
  line-height: 1.5;
  outline: none;
  resize: none;
  font-family: inherit;
  padding: 6px 0;
  max-height: 150px;
  scrollbar-width: thin;
}

.chat-send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--vp-c-brand-1);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  margin-bottom: 2px;
}

.chat-send-btn:hover:not(:disabled) {
  background: var(--vp-c-brand-3);
  transform: scale(1.05);
}

.chat-send-btn:disabled {
  background: transparent;
  color: var(--vp-c-text-3);
  cursor: not-allowed;
}

.send-icon {
  margin-left: 2px;
}
</style>

<style>
/* CSS định dạng các phần tử con render từ markdown */
.chat-code-block {
  background-color: var(--vp-code-block-bg) !important;
  border: 1px solid var(--vp-c-gutter);
  border-radius: 8px;
  padding: 12px 16px;
  margin: 10px 0;
  overflow-x: auto;
  font-family: var(--vp-font-family-mono);
  font-size: 13px;
  line-height: 1.5;
}

.chat-inline-code {
  background-color: var(--vp-c-bg-mute);
  padding: 3px 6px;
  border-radius: 6px;
  font-family: var(--vp-font-family-mono);
  font-size: 13px;
  border: 1px solid var(--vp-c-gutter);
  color: var(--vp-c-brand-1);
}

.message-text strong {
  font-weight: 700;
}

.message-text br {
  margin-bottom: 6px;
}
</style>
