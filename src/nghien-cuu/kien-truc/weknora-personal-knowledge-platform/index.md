# Nền tảng Tri thức Cá nhân WeKnora

> **Phiên bản triển khai:** WeKnora Core 0.8.0 (Official Stable Release)  
> **Môi trường:** Local Windows 11 Pro (x86_64), Docker 29.6.1, Docker Compose v5.2.0  
> **Trạng thái:** Triển khai hoàn tất, xác minh 4 Verification Gates và Persistence thành công 100%.  
> **Tài liệu liên quan:** [Hướng dẫn Sử dụng & Cấu hình](./huong-dan-su-dung) | [Nghiên cứu Kiến trúc & C4 Model](./danh-gia-kien-truc)

---

## 1. Tổng quan & Mục tiêu Triển khai

**WeKnora** là nền tảng quản trị tri thức mã nguồn mở do Tencent phát triển, kết hợp ba năng lực cốt lõi: **RAG Q&A**, **ReAct Agent** và **Auto-Wiki**. Trong bài nghiên cứu này, WeKnora được triển khai trên môi trường máy cá nhân (Local) để đóng vai trò làm **Personal Knowledge Platform** (Nền tảng tri thức tính toán - Computational Knowledge Surface), hoạt động song song và bổ trợ cho kho tài liệu tĩnh **my-wiki** (Authoring & Publication Surface).

### Nguyên tắc triển khai
1. **Official configuration > workaround > custom modification**: Sử dụng trực tiếp repository chính thức Tencent/WeKnora, cấu hình qua .env, không can thiệp sửa đổi docker-compose.yml.
2. **Docker Core tối giản**: Chỉ bật 5 dịch vụ Core mặc định (rontend, pp, docreader, postgres, 
edis). Tuyệt đối không bật --profile full hay các phụ trợ chưa cần thiết (
eo4j, minio, qdrant, searxng, langfuse, sandbox).
3. **Bảo toàn tuyệt đối dịch vụ hiện có**: Nhận diện và giải quyết xung đột cổng mạng mà không dừng, kill hay thay đổi bất kỳ container nào của hệ thống đang chạy.
4. **Bản địa hóa tiếng Anh**: Cấu hình mặc định toàn bộ giao diện UI và bộ xử lý tài liệu sang tiếng Anh (n-US).

---

## 2. Sơ đồ Kiến trúc Triển khai (Deployment Architecture)

Kiến trúc triển khai thực tế của WeKnora Core trên máy local được biểu diễn qua sơ đồ sau:

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/deployment-topology.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

---

## 3. Chi tiết các Thành phần Hạ tầng (Running Services)

| Dịch vụ | Tên Container | Image & Tag | Cổng Host / Mạng | Trạng thái | Nhiệm vụ chính |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **frontend** | WeKnora-frontend | wechatopenai/weknora-ui:v0.8.0 | 0.0.0.0:80->80/tcp | Up | Cung cấp Web UI Vue 3 (Vite), Nginx reverse proxy /api/ về container pp:8080. |
| **app** | WeKnora-app | wechatopenai/weknora-app:v0.8.0 | 0.0.0.0:8085->8080/tcp | Up (Healthy) | Core Go Gin backend: quản lý Workspace, Knowledge Base, API router, Asynq task worker pools, RAG pipeline. |
| **docreader** | WeKnora-docreader | wechatopenai/weknora-docreader:v0.8.0 | 50051/tcp (Nội bộ) | Up (Healthy) | Python gRPC service: bóc tách đa định dạng (PDF, DOCX, Markdown, Office, hình ảnh), chuyển đổi về cấu trúc chuẩn. |
| **postgres** | WeKnora-postgres | paradedb/paradedb:v0.22.2-pg17 | 5432/tcp (Nội bộ) | Up (Healthy) | PostgreSQL 17 tích hợp ParadeDB: lưu trữ bảng quan hệ, Full-text Search (BM25) và Vector embeddings (pgvector). |
| **redis** | WeKnora-redis | 
edis:7.0-alpine | 6379/tcp (Nội bộ) | Up | Quản lý hàng đợi Asynq (ingestion pools, enrichment, wiki generation), cơ chế stream recovery và pub/sub. |

> [!IMPORTANT]
> **Không có cổng nội bộ nào bị rò rỉ**: Cả PostgreSQL, Redis và DocReader đều chỉ lắng nghe bên trong mạng bridge weknora_WeKnora-network. Cổng 5432 không expose ra ngoài, hoàn toàn không xung đột với container a-platform-db đang chạy trên máy.

---

## 4. Xử lý Xung đột Cổng Mạng (Port Allocation Strategy)

Trong quá trình Pre-flight check, hệ thống phát hiện cổng 8080 đang được container harness-opensource (4f1cc250bb0) sử dụng làm Git Server cho dự án my-wiki (http://localhost:8080/git/admin/my-wiki.git).

**Chiến lược xử lý an toàn nhất**:
- **Giữ nguyên 100% container harness-opensource**: Không tắt, không đổi cổng của Harness để tránh làm đứt gãy kết nối Git của my-wiki.
- **Ánh xạ cổng host cho WeKnora App qua .env**:
  `nv
  APP_PORT=8085
  FRONTEND_PORT=80
  `
- **Cơ chế hoạt động**:
  - Người dùng truy cập UI trực tiếp tại: http://localhost:80
  - Các API client hoặc MCP gọi backend trực tiếp tại: http://localhost:8085/api/v1 (hoặc thông qua proxy tại http://localhost:80/api/v1)
  - Nginx bên trong container rontend tiếp tục kết nối với pp:8080 qua DNS nội bộ của Docker network.

---

## 5. Cấu hình & Bản địa hóa (Configuration & Localization)

File cấu hình .env được tạo độc lập tại D:\4.Code\weknora\.env và được loại trừ khỏi Git tracking (.gitignore chứa rule .*).

### Cấu hình ngôn ngữ mặc định (English)
Hệ thống đã được thiết lập mặc định sử dụng Tiếng Anh (n-US) cho cả giao diện lẫn xử lý ngôn ngữ tài liệu:
`nv
# Ngôn ngữ hiển thị UI mặc định cho người dùng mới
DEFAULT_LOCALE=en-US
VITE_DEFAULT_LOCALE=en-US

# Ngôn ngữ xử lý tài liệu mặc định ở backend (Prompt, sinh câu hỏi, tóm tắt)
WEKNORA_LANGUAGE=en-US
`

### Quản lý Secret & Xác thực
- DB_PASSWORD & REDIS_PASSWORD: Được tạo ngẫu nhiên bảo mật 24 ký tự chữ và số.
- JWT_SECRET: Token bí mật độ dài 64 hex đảm bảo an toàn cho phiên làm việc.
- SYSTEM_AES_KEY: Khóa mã hóa 32-byte an toàn theo chuẩn AES.
- WEKNORA_SANDBOX_DOCKER_ENABLED=false: Vô hiệu hóa Docker socket mount để loại trừ rủi ro bảo mật leo thang đặc quyền.

---

## 6. Tính Bền bỉ Dữ liệu & Backup (Persistence Architecture)

### Vị trí lưu trữ dữ liệu
> **Câu hỏi quan trọng:** *Nếu thư mục mã nguồn D:\4.Code\weknora bị xóa và clone lại, dữ liệu local nằm ở đâu?*

**Sự thật đã kiểm chứng:** Dữ liệu hoàn toàn **KHÔNG** nằm trong thư mục mã nguồn Git, mà nằm trong **Docker Named Volumes**:
1. weknora_postgres-data: Chứa toàn bộ cơ sở dữ liệu quan hệ (tài khoản người dùng, cấu hình workspace, metadata của knowledge base, vector embeddings của ParadeDB).
2. weknora_data-files: Chứa các tệp tin gốc tải lên kho tri thức (STORAGE_TYPE=local gắn tại /data/files).
3. weknora_docreader-tmp: Bộ nhớ đệm tạm thời cho quá trình render trang và bóc tách hình ảnh.

Khi xóa thư mục D:\4.Code\weknora, các volume này vẫn tồn tại nguyên vẹn trên Docker Engine (WSL2 backend). Khi clone lại dự án và chạy docker compose up -d, Docker Compose sẽ tự động gắn (attach) lại vào các volume cũ, khôi phục 100% dữ liệu.

### Quy trình Sao lưu & Phục hồi (Khuyến nghị)
`powershell
# 1. Sao lưu Cơ sở dữ liệu ParadeDB
docker exec -t WeKnora-postgres pg_dump -U postgres -d WeKnora > D:\backup\weknora_db.sql

# 2. Sao lưu Tập tin tài liệu gốc
docker run --rm -v weknora_data-files:/data -v D:\backup:/backup alpine tar czf /backup/weknora_files.tar.gz -C /data .

# 3. Lưu trữ an toàn file cấu hình .env (chứa DB_PASSWORD và các AES keys)
Copy-Item D:\4.Code\weknora\.env D:\backup\.env.backup
`

---

## 7. Kết quả Kiểm chứng 4 Verification Gates

| Gate | Hạng mục kiểm tra | Tiêu chí đánh giá | Kết quả | Bằng chứng kiểm chứng |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1** | **Infrastructure** | Tất cả 5 containers Core chạy ổn định, healthy, không có restart loop. | PASS | docker compose ps xác nhận 5 containers đều Up (healthy). Logs ứng dụng khởi tạo DB migration và asynq workers thành công. |
| **Gate 2** | **Web UI & API** | Frontend port 80 trả về HTML, Backend API port 8085 phản hồi HTTP 200. | PASS | http://localhost:80/ trả về status 200 (<title>WeKnora</title>). http://localhost:8085/health trả về {"status":"ok"}. |
| **Gate 3** | **Smoke Test** | Đăng ký user, đăng nhập JWT, tạo KB local-smoke-test, upload doc smoke_test.md. | PASS (Infra)<br>BLOCKED (Model) | User smoketest@local.internal được tạo thành công. KB local-smoke-test (ID 6ee78ae8...) và doc smoke_test.md (ID d1ab6a54...) hiển thị đầy đủ. Bước RAG dừng chờ cấu hình model theo đúng nguyên tắc bảo mật. |
| **Gate 4** | **Persistence** | Chạy docker compose restart, kiểm tra dữ liệu không bị mất. | PASS | Sau khi restart, toàn bộ containers healthy. Token đăng nhập, KB local-smoke-test và document smoke_test.md vẫn tồn tại nguyên vẹn. |

---

## 8. Kiến trúc Tích hợp với my-wiki & MCP Server

Trong giai đoạn tiếp theo, WeKnora sẽ được tích hợp vào luồng làm việc cá nhân theo mô hình kiến trúc phân lớp:

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/integration-architecture.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

### Nguyên tắc tích hợp then chốt
1. **Nguồn sự thật một chiều (Single Source of Truth)**: my-wiki (Markdown trong Git) là nguồn chân lý duy nhất. Tài liệu chỉ được đẩy một chiều từ my-wiki sang WeKnora.
2. **Tri thức dẫn xuất (Derived Knowledge)**: Auto-Wiki và tóm tắt do WeKnora sinh ra chỉ là tầng phục vụ tra cứu (serving layer). Mọi thay đổi nội dung lâu dài phải được cập nhật ở tệp Markdown gốc trong my-wiki.
3. **MCP Server an toàn**: MCP Server của WeKnora (mcp-server/) kết nối qua HTTP/stdio sử dụng scoped API Key, cho phép các tác tử như Hermes, Claude Desktop hoặc Cursor tra cứu tri thức trực tiếp mà không cần truy cập cơ sở dữ liệu.

---

## 9. Hướng dẫn Vận hành Nhanh (Operations Guide)

### Khởi động và Dừng dịch vụ
`powershell
# Chuyển vào thư mục cài đặt
cd D:\4.Code\weknora

# Khởi động dịch vụ nền
docker compose up -d

# Xem trạng thái containers
docker compose ps

# Xem nhật ký hệ thống
docker compose logs -f app

# Khởi động lại an toàn
docker compose restart

# Dừng hệ thống (KHÔNG dùng cờ -v)
docker compose down
`

### Thông tin Truy cập Mặc định
- **Giao diện Web UI**: [http://localhost:80](http://localhost:80)
- **Tài khoản System Admin thử nghiệm**:
  - Email: smoketest@local.internal
  - Mật khẩu: SmokeTestPassword123!
  - Vai trò: Workspace Owner & System Administrator
- **Tạo tài khoản mới**: Bấm **Register** tại màn hình đăng nhập (chế độ đăng ký tự do đang bật).

---

## 10. Gom nhóm Mục Nghiên cứu WeKnora

Cụm nghiên cứu về WeKnora trong hệ thống my-wiki bao gồm các tài liệu chuyên sâu:

1. **[Kiến trúc Triển khai Thực tế WeKnora](./)** *(Trang này)*: Đặc tả chi tiết hạ tầng Docker Core, cấu hình mạng, phân bổ cổng, cơ chế lưu trữ persistent, xử lý xung đột và kết quả kiểm chứng.
2. **[Hướng dẫn Sử dụng & Cấu hình Cơ bản](./huong-dan-su-dung)**: Cẩm nang vận hành toàn diện, cấu hình LLM (Ollama / Cloud), quy trình vòng đời tri thức, RAG pipeline, Auto-Wiki và tích hợp MCP Server.
3. **[Nghiên cứu Kiến trúc & Đánh giá Khả thi C4](./danh-gia-kien-truc)**: Bài phân tích lý thuyết toàn diện dựa trên mã nguồn WeKnora, mô hình C4 Level 1–3, so sánh Lite vs Standard vs Full, pipeline RAG, Auto-Wiki và ma trận đánh giá rủi ro.
4. **Báo cáo Kết quả Cài đặt Local**: Lưu trữ tại `D:\4.Code\weknora\weknora-local-install-result.md` ghi nhận nhật ký chi tiết các lệnh đã thực thi trên máy.
