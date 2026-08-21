---
layout: doc
title: Kiến trúc hệ thống
---

# Kiến Trúc Hệ Thống (C4 Model)

Tài liệu này mô tả chi tiết kiến trúc của dự án **Local Wiki & RAG Chatbot** tuân theo tiêu chuẩn **C4 Model** (Context, Container, Component, Code). Dự án được thiết kế dưới dạng ứng dụng quản lý tri thức cục bộ (local-first) hỗ trợ tìm kiếm ngữ nghĩa và trợ lý AI offline.

---

## C4 - Cấp độ 1: Sơ đồ ngữ cảnh hệ thống (System Context Diagram)

Sơ đồ ngữ cảnh mô tả mối quan hệ giữa người dùng, hệ thống Local Wiki và thực thể bên ngoài duy nhất (mô hình ngôn ngữ lớn chạy trên Ollama).

```mermaid
graph TD
    User["👤 Người dùng (User)<br>Đọc giả, nghiên cứu viên"]
    
    subgraph SystemBoundary ["Ranh giới hệ thống cục bộ"]
        WikiSystem["📚 Hệ thống Local Wiki & Chatbot<br>(Hệ thống đang xây dựng)"]
    end
    
    Ollama["🤖 Ollama LLM Service<br>(Hệ thống chạy trên máy của User)<br>Cung cấp mô hình ngôn ngữ Llama/Qwen"]
    
    User -->|"1. Đọc tài liệu, viết câu hỏi"| WikiSystem
    WikiSystem -->|"2. Truy xuất tài liệu & Gửi ngữ cảnh"| Ollama
    Ollama -->|"3. Stream câu trả lời thông minh"| WikiSystem
    WikiSystem -->|"4. Hiển thị câu trả lời và nguồn tài liệu"| User

    style WikiSystem fill:#4f46e5,stroke:#fff,stroke-width:2px,color:#fff
    style Ollama fill:#22c55e,stroke:#fff,stroke-width:2px,color:#fff
    style User fill:#0ea5e9,stroke:#fff,stroke-width:2px,color:#fff
```

---

## C4 - Cấp độ 2: Sơ đồ Container (Container Diagram)

Sơ đồ này phân rã hệ thống Local Wiki thành các Container công nghệ chạy độc lập hoặc kết hợp trong môi trường local.

```mermaid
graph TB
    User["👤 Người dùng (Trình duyệt Web)"]
    
    subgraph WikiApp ["Dự án Local Wiki (VitePress Node.js App)"]
        Frontend["🌐 VitePress Web UI<br>(Vue 3 / HTML / CSS / JS)<br>Hiển thị trang tài liệu và giao diện Chat Capsule"]
        
        ViteServer["⚙️ Vite Dev Server Middleware<br>(Node.js)<br>Lắng nghe và xử lý API tìm kiếm vector"]
        
        IndexScript["📜 Indexing Script<br>(Node.js CLI)<br>Tiền xử lý tài liệu .md và trích xuất vector"]
        
        LanceDB["🗄️ LanceDB Vector Store<br>(File phẳng cục bộ)<br>Lưu trữ vector và đoạn văn bản tài liệu"]
    end
    
    MdFiles["📄 Tài liệu cục bộ (.md)<br>(Thư mục src/)"]
    Ollama["🤖 Ollama Service<br>(Port 11434)<br>Chạy mô hình LLM nội bộ"]

    %% Luồng tương tác
    User -->|"Truy cập web & hỏi đáp"| Frontend
    Frontend -->|"Gọi API: /api/search?q=..."| ViteServer
    
    ViteServer -->|"Truy vấn vector"| LanceDB
    IndexScript -->|"1. Đọc tài liệu"| MdFiles
    IndexScript -->|"2. Tạo & Lưu vector"| LanceDB
    
    Frontend -->|"Gọi API RAG: /api/generate"| Ollama
    
    style Frontend fill:#6366f1,stroke:#fff,color:#fff
    style ViteServer fill:#4f46e5,stroke:#fff,color:#fff
    style IndexScript fill:#818cf8,stroke:#fff,color:#fff
    style LanceDB fill:#ec4899,stroke:#fff,color:#fff
    style MdFiles fill:#94a3b8,stroke:#fff,color:#fff
    style Ollama fill:#22c55e,stroke:#fff,color:#fff
```

---

## C4 - Cấp độ 3: Sơ đồ thành phần (Component Diagram)

Sơ đồ này mô tả chi tiết các thành phần bên trong **Vite Dev Server Middleware** (xử lý API Tìm kiếm) và **Indexing Script** (xử lý Lập chỉ mục).

### 3.1 Thành phần xử lý API tìm kiếm (Vite Server Middleware)
Khi người dùng thực hiện chat, thành phần này phân tích ý định câu hỏi và truy xuất dữ liệu từ Database.

```mermaid
graph LR
    Request["Request từ UI (/api/search)"] --> Router["Vite API Router Middleware"]
    
    subgraph MiddlewareComponents ["Thành phần Middleware"]
        Router --> EmbeddingLoader["Transformers.js Loader<br>(Nhúng trong Node)"]
        EmbeddingLoader --> Model["Model all-MiniLM-L6-v2<br>(Chuyển text thành vector)"]
        Model --> DBClient["LanceDB Client"]
    end
    
    DBClient -->|"Truy vấn gần đúng (ANN)"| VectorDB[("LanceDB Storage<br>(data/wiki-vector-db)")]
    DBClient -->|"Trả về 4 đoạn khớp nhất"| Router
    Router --> Response["Response (JSON Results)"]

    style MiddlewareComponents fill:#f8fafc,stroke:#4f46e5,stroke-dasharray: 5 5
    style VectorDB fill:#ec4899,stroke:#fff,color:#fff
```

### 3.2 Thành phần lập chỉ mục tài liệu (Indexing Script)
Thực hiện quét offline tài liệu nguồn để chuẩn bị dữ liệu vector cho cơ sở dữ liệu.

```mermaid
graph TD
    Trigger["Chạy lệnh: npm run index"] --> Scanner["Directory Scanner<br>(Quét đệ quy src/)"]
    
    subgraph IndexingPipeline ["Đường ống Lập chỉ mục"]
        Scanner --> Parser["Markdown Parser<br>(Tách Frontmatter & Body)"]
        Parser --> Chunker["Text Chunker<br>(Cắt nhỏ thành các đoạn 800 ký tự)"]
        Chunker --> Embedding["Transformers.js Generator<br>(Chuyển đổi văn bản sang Vector)"]
        Embedding --> DBWriter["LanceDB Writer"]
    end
    
    DBWriter -->|"Ghi đè/Cập nhật"| FileStore[("LanceDB Storage")]

    style IndexingPipeline fill:#f8fafc,stroke:#818cf8,stroke-dasharray: 5 5
    style FileStore fill:#ec4899,stroke:#fff,color:#fff
```

---

## C4 - Cấp độ 4: Code & Ánh xạ tập tin (Code Mapping)

Dưới đây là các lớp mã nguồn chính trong thư mục dự án chịu trách nhiệm thực thi các thành phần kiến trúc trên:

1.  **Giao diện Chatbot UI (`ChatInterface.vue`):**
    *   *Đường dẫn:* [`src/.vitepress/theme/components/ChatInterface.vue`](file:///d:/4.Code/my-wiki/src/.vitepress/theme/components/ChatInterface.vue)
    *   *Chức năng:* Giao diện người dùng Web, quản lý luồng hội thoại, gọi API `/api/search` nội bộ và gọi API `/api/generate` từ Ollama.
2.  **Lập chỉ mục và Sinh Vector (`index-docs.js`):**
    *   *Đường dẫn:* [`scripts/index-docs.js`](file:///d:/4.Code/my-wiki/scripts/index-docs.js)
    *   *Chức năng:* Pipeline chạy bằng dòng lệnh (CLI). Đọc file `.md`, thực hiện chia nhỏ văn bản (Chunking) và nạp dữ liệu vector vào LanceDB thông qua mô hình cục bộ của Transformers.js.
3.  **Tích hợp Server Middleware (`config.mts`):**
    *   *Đường dẫn:* [`src/.vitepress/config.mts`](file:///d:/4.Code/my-wiki/src/.vitepress/config.mts)
    *   *Chức năng:* Tích hợp custom Vite plugin để chặn các request đến `/api/search`, tải mô hình sinh vector và thực hiện truy vấn trực tiếp trên cơ sở dữ liệu LanceDB ngay trên máy chủ phát triển cục bộ.
4.  **Cơ sở dữ liệu Vector (`wiki_chunks`):**
    *   *Đường dẫn:* `d:\4.Code\my-wiki\data\wiki-vector-db`
    *   *Chức năng:* Lưu trữ các file định dạng Lance chứa dữ liệu văn bản và các chuỗi số vector đại diện cho ngữ nghĩa của tài liệu.
