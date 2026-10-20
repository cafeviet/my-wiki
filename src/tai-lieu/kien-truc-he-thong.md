---
layout: doc
title: Kiến trúc hệ thống
---

# Kiến trúc Local Wiki & RAG Chatbot

Tài liệu này mô tả kiến trúc **đang được triển khai trong repository**, theo các góc nhìn C4 Context, Container, luồng truy vấn RAG và pipeline lập chỉ mục. Hệ thống ưu tiên chạy cục bộ: tài liệu, embedding và vector database đều nằm trên máy; Ollama là tích hợp tùy chọn để sinh câu trả lời.

> [!IMPORTANT]
> Endpoint `/api/search` hiện được cài bằng `configureServer` của Vite. Vì vậy chức năng RAG search hoạt động với `npm run dev`, nhưng **không tự tồn tại trong static output** của `npm run build`. Muốn triển khai production cần bổ sung một API runtime tương đương.

## 1. Phạm vi và nguyên tắc

| Thuộc tính | Hiện trạng |
|---|---|
| Kiểu ứng dụng | VitePress + Vue 3, chạy local-first |
| Nguồn tri thức | Markdown trong `src/tai-lieu`, `src/nghien-cuu`, `src/dich-thuat` |
| Embedding | `Xenova/all-MiniLM-L6-v2`, pooling `mean`, normalize `true` |
| Vector store | LanceDB tại `data/wiki-vector-db`, bảng `wiki_chunks` |
| Retrieval | Vector search, lấy tối đa 4 đoạn gần nhất |
| Generation | Ollama tại `localhost:11434`, gọi trực tiếp từ trình duyệt |
| Chế độ suy giảm | Không có Ollama: hiển thị trực tiếp các đoạn tìm thấy và link nguồn |

## 2. C4 Level 1 — System Context

Người dùng tương tác với Local Wiki qua trình duyệt. Hệ thống cung cấp đọc tài liệu, tìm kiếm ngữ nghĩa và giao diện hỏi đáp. Nếu Ollama đang chạy và có model, UI dùng các đoạn truy xuất làm context để tạo câu trả lời; nếu không, UI vẫn hoạt động ở chế độ search-only.

<iframe class="architecture-diagram" src="/diagrams/context.html" title="Sơ đồ ngữ cảnh hệ thống Local Wiki" loading="lazy"></iframe>

**Ranh giới hệ thống:** Local Wiki quản lý UI, tài liệu, embedding và retrieval. Ollama chạy như một dịch vụ cục bộ độc lập và không phải điều kiện bắt buộc để đọc hoặc tìm kiếm tài liệu.

## 3. C4 Level 2 — Container & runtime boundaries

Kiến trúc có hai luồng thực thi khác nhau:

1. **Runtime query:** trình duyệt → VitePress UI → Vite dev middleware → LanceDB.
2. **Offline indexing:** CLI → Markdown → embedding model → LanceDB.

<iframe class="architecture-diagram architecture-diagram--tall" src="/diagrams/containers.html" title="Sơ đồ container và ranh giới runtime" loading="lazy"></iframe>

### Trách nhiệm của từng container

| Container | Công nghệ | Trách nhiệm |
|---|---|---|
| VitePress Web UI | VitePress, Vue 3 | Render tài liệu, chat UI, kiểm tra Ollama, gọi search và generation |
| Vite Middleware | Node.js, Vite plugin | Cung cấp `GET /api/search`, sinh query embedding và truy vấn LanceDB |
| Indexing CLI | Node.js | Quét Markdown, parse metadata, chunking, sinh embedding và ghi DB |
| LanceDB | File-based vector store | Lưu vector, đoạn văn bản, title và route nguồn |
| Ollama | HTTP service cục bộ | Liệt kê model và stream kết quả sinh ngôn ngữ |

## 4. Luồng truy vấn RAG

Khi người dùng gửi câu hỏi, retrieval luôn chạy trước. Generation chỉ được dùng khi Ollama có ít nhất một model khả dụng.

<iframe class="architecture-diagram" src="/diagrams/rag-flow.html" title="Luồng truy vấn RAG tại runtime" loading="lazy"></iframe>

### Trình tự xử lý

1. `ChatInterface.vue` gọi `/api/search?q=<encoded query>`.
2. Middleware tải hoặc tái sử dụng embedding pipeline đã cache trong process.
3. Câu hỏi được chuyển thành vector với cùng model và cấu hình dùng khi indexing.
4. LanceDB trả tối đa 4 bản ghi gần nhất từ bảng `wiki_chunks`.
5. UI loại trùng link nguồn.
6. Nếu Ollama online, UI ghép các đoạn vào prompt và gọi `POST http://localhost:11434/api/generate` với `stream: true`.
7. Nếu Ollama offline, UI hiển thị trực tiếp kết quả retrieval.

> [!NOTE]
> Trình duyệt gọi Ollama trực tiếp, không đi qua endpoint `/api/generate` của Local Wiki. Ollama cần cho phép origin của trang web nếu chính sách CORS được bật.

## 5. Pipeline lập chỉ mục

Index là batch job chạy thủ công. Mỗi lần chạy sẽ tái tạo bảng `wiki_chunks` bằng chế độ `overwrite`.

<iframe class="architecture-diagram" src="/diagrams/index-flow.html" title="Pipeline lập chỉ mục tài liệu" loading="lazy"></iframe>

### Quy tắc dữ liệu

- Chỉ quét ba thư mục: `tai-lieu`, `nghien-cuu`, `dich-thuat`.
- Frontmatter được parse để lấy `title`; nếu thiếu, dùng heading H1 hoặc tên file.
- Route được tính tương đối từ `src`; hậu tố `.md` và `/index` được loại bỏ.
- Chunk mặc định tối đa 800 ký tự; đoạn quá dài dùng overlap 150 ký tự.
- Mỗi record gồm `vector`, `text`, `title` có hậu tố `(Đoạn N)` và `link`.
- Sau khi thêm hoặc sửa tài liệu, chạy lại:

```bash
npm run index
```

## 6. Ánh xạ code

| Thành phần | Mã nguồn | Điểm vào chính |
|---|---|---|
| Chat UI | `src/.vitepress/theme/components/ChatInterface.vue` | `sendMessage()` |
| Search middleware | `src/.vitepress/config.mts` | `localSearchApiPlugin()` |
| Indexing pipeline | `scripts/index-docs.js` | `main()` |
| Vector database | `data/wiki-vector-db` | bảng `wiki_chunks` |
| Trang chat | `src/chat.md` | `<ChatInterface />` |
| Theme registration | `src/.vitepress/theme/index.ts` | `enhanceApp()` |

## 7. Chạy hệ thống

```bash
# Khởi động docs + search runtime
npm run dev

# Tái tạo vector index sau khi đổi tài liệu
npm run index

# Kiểm tra static site có build được hay không
npm run build
```

Ollama là tùy chọn. Khi dùng generation, khởi động Ollama riêng và bảo đảm có ít nhất một model phù hợp (`qwen2`, `llama3`, `mistral`, `gemma`, hoặc model đầu tiên trong danh sách).

## 8. Giới hạn và hướng phát triển

1. **Production API:** chuyển search middleware sang server/API runtime độc lập nếu cần deploy static site.
2. **CORS Ollama:** proxy generation qua backend để kiểm soát origin, timeout và lỗi tốt hơn.
3. **Index consistency:** dùng chung module chunking/embedding cho indexing và query thay vì khai báo ở hai file.
4. **Incremental indexing:** hiện tại mọi lần chạy đều ghi đè toàn bộ bảng; có thể bổ sung hash theo tài liệu.
5. **Observability:** thêm health endpoint và log có cấu trúc thay vì log trực tiếp toàn bộ thư viện Lance.

<style>
.architecture-diagram {
  display: block;
  width: 100%;
  min-height: 620px;
  margin: 24px 0 32px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}

.architecture-diagram--tall {
  min-height: 700px;
}

@media (max-width: 700px) {
  .architecture-diagram {
    min-height: 520px;
  }
}
</style>
