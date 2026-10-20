# Hướng dẫn Sử dụng & Cấu hình WeKnora

> **Phiên bản áp dụng:** WeKnora Core v0.8.0  
> **Địa chỉ Web UI:** [http://localhost:80](http://localhost:80)  
> **Địa chỉ Backend API:** [http://localhost:8085/api/v1](http://localhost:8085/api/v1)  
> **Tài liệu liên quan:** [Kiến trúc Triển khai Thực tế](./) | [Nghiên cứu Kiến trúc & C4 Model](./danh-gia-kien-truc)

---

## 1. Bắt đầu Nhanh (Quick Start)

WeKnora là trạm làm việc tri thức cá nhân (**Personal Knowledge Platform**). Sau khi hoàn tất triển khai Docker Core, toàn bộ giao diện đã sẵn sàng phục vụ việc tải tài liệu, phân đoạn, nhúng vector và hỏi đáp RAG.

### 1.1. Thông tin Đăng nhập Hệ thống

| Mục | Giá trị mặc định | Ghi chú |
| :--- | :--- | :--- |
| **URL Truy cập** | `http://localhost:80` | Mở trực tiếp trên trình duyệt Web |
| **Tài khoản Quản trị** | `smoketest@local.internal` | Đã cấp quyền **System Admin & Workspace Owner** |
| **Mật khẩu** | `SmokeTestPassword123!` | Khuyến nghị đổi mật khẩu sau lần đăng nhập đầu |
| **Đăng ký Tự do** | Nút **Register** tại màn hình Login | Dành cho việc tạo thêm tài khoản làm việc riêng biệt |

> [!TIP]
> **Đổi mật khẩu tài khoản Admin:**  
> Sau khi đăng nhập, nhấp vào ảnh đại diện (Avatar) ở góc trên bên phải $\rightarrow$ Chọn **Account Settings** (Cài đặt tài khoản) $\rightarrow$ Tab **Security** $\rightarrow$ Nhập mật khẩu hiện tại và đặt mật khẩu mới.

---

## 2. Vòng đời Tri thức trên WeKnora (Knowledge Lifecycle)

Quá trình biến các tài liệu rời rạc thành một mạng lưới tri thức có thể truy vấn và trích dẫn chính xác tuân theo quy trình 5 bước khép kín. Sơ đồ tương tác dưới đây mô tả toàn bộ vòng đời này:

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/user-journey-workflow.html" width="100%" height="720" style="border:none;border-radius:0.75rem;box-shadow:0 4px 12px rgba(0,0,0,0.08);"></iframe>

### Giải thích 5 Giai đoạn Vận hành:

1. **Ingestion (Tiếp nhận & Bóc tách):**  
   Người dùng tải lên tài liệu đa định dạng (PDF, DOCX, Markdown, Text). Container `docreader` (chạy service Python gRPC) tiến hành phân tích cú pháp, trích xuất cấu trúc văn bản, tiêu đề, bảng biểu và loại bỏ rác định dạng.
2. **Chunking & Index (Phân đoạn & Lập chỉ mục kép):**  
   Tài liệu được cắt nhỏ thành các đoạn logic (Chunks) có độ gối đầu (Overlap). Hệ thống đồng thời lập chỉ mục kép: chỉ mục từ khóa **BM25** (qua ParadeDB) và chỉ mục ngữ nghĩa **Vector** (qua mô hình Embedding lưu trong PostgreSQL pgvector).
3. **Auto-Wiki (Liên kết Thực thể & Đồ thị Tri thức):**  
   Backend quét các đoạn văn bản để trích xuất thực thể, khái niệm chính và tạo các liên kết chéo (Cross-links), hình thành các trang tri thức tổng hợp tự động.
4. **Hybrid Retrieval (Truy vấn Kết hợp):**  
   Khi người dùng đặt câu hỏi, hệ thống kích hoạt tìm kiếm kép: BM25 tìm chính xác thuật ngữ/mã hiệu + Vector tìm ý niệm ngữ nghĩa. Thuật toán **Reciprocal Rank Fusion (RRF)** kết hợp và xếp hạng lại Top-K đoạn phù hợp nhất.
5. **Grounded Synthesis (Tổng hợp & Trích dẫn Nguồn):**  
   Mô hình LLM sinh câu trả lời tự nhiên dựa trên ngữ cảnh đã lọc, đồng thời đánh số trích dẫn `[1]`, `[2]` tương ứng với vị trí chính xác trong tài liệu gốc tại **Reference Drawer**.

---

## 3. Cấu hình Model Providers qua 9Router & Ollama

WeKnora cần hai loại mô hình để vận hành trọn vẹn:
1. **Chat / Completion Model:** Phục vụ việc phân tích ý định, sinh câu trả lời đối thoại RAG, tóm tắt trang Auto-Wiki và đánh số trích dẫn.
2. **Embedding Model:** Phục vụ việc biến đổi văn bản (Chunks) thành các vector đa chiều lưu vào PostgreSQL pgvector.

Mô hình định tuyến tối ưu nhất trên máy local là **Kiến trúc Lai (Hybrid Architecture)**: Sử dụng **9Router AI Gateway** cho toàn bộ Chat & Lý luận, kết hợp với **Ollama Local** cho Embeddings nhằm tối ưu hóa chi phí và tốc độ:

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/model-routing-topology.html" width="100%" height="720" style="border:none;border-radius:0.75rem;box-shadow:0 4px 12px rgba(0,0,0,0.08);"></iframe>

---

### 3.1. Cấu hình AI Gateway qua 9Router (Khuyến nghị Cốt lõi)

**9Router** (`D:\4.Code\9router`) là cổng AI Gateway & Reverse Proxy đang chạy trên máy chủ Windows tại cổng **`20127`**. 9Router cung cấp một điểm cuối tương thích chuẩn OpenAI (`/v1`), tích hợp tính năng nén token (Token Saver), chống nghẽn và tự động định tuyến dự phòng (Multi-tier Failover) giữa các nhà cung cấp AI.

#### 1. Thông số Kết nối Mạng

| Tham số | Giá trị Cấu hình | Giải thích |
| :--- | :--- | :--- |
| **Provider Type** | `OpenAI` hoặc `OpenAI Compatible` | Chuẩn giao tiếp mà 9Router hỗ trợ |
| **Provider Name** | `9Router Gateway` | Tên hiển thị gợi nhớ trong WeKnora |
| **Base URL** | `http://host.docker.internal:20127/v1` | **Bắt buộc**: Trỏ từ Docker Container về cổng 20127 của máy Windows Host |
| **API Key** | `sk-4159bc8f7dbb711a-7chwxp-3d6bc0ef` | Khóa API xác thực truy cập từ xa (Remote Client) |

> [!IMPORTANT]
> **Tại sao cần API Key khi 9Router chạy trên cùng một máy?**  
> 9Router tích hợp cơ chế bảo vệ `dashboardGuard`: Các kết nối xuất phát từ địa chỉ loopback (`127.0.0.1` của Host) không cần key. Tuy nhiên, khi WeKnora chạy bên trong Docker Container, gói tin đi qua Docker Bridge Network (`172.x.x.x`), 9Router sẽ nhận diện đây là kết nối từ xa (**Remote Access**) và yêu cầu Bearer API Key hợp lệ.

Khóa API khả dụng sẵn có trên máy bạn có thể dùng ngay:
- `sk-4159bc8f7dbb711a-7chwxp-3d6bc0ef` *(Default Key)*
- `sk-4159bc8f7dbb711a-nn6eeo-a815f78b`
- `sk-4159bc8f7dbb711a-ev7345-71f18c06` *(codex-local)*

*(Bạn cũng có thể mở Dashboard 9Router tại `http://localhost:20128` để tạo thêm khóa mới tùy ý).*

---

#### 2. Danh mục Model Khả dụng (Available Models Catalog) trên 9Router

9Router quản lý danh mục mô hình phong phú được phân cấp theo tiền tố (Prefix). Khi khai báo Model trong WeKnora, bạn cần nhập **chính xác mã ID** dưới đây:

##### Nhóm 1: Google Gemini qua Antigravity (`ag/`) — *Khuyến nghị Tốc độ & Hỏi đáp*
- **`ag/gemini-3.7-flash-medium`** ⭐ **(Khuyên dùng số 1 cho RAG Chat):** Tốc độ phản hồi cực nhanh, xử lý ngữ cảnh mượt mà, hỗ trợ suy luận logic tự nhiên.
- `ag/gemini-3.7-flash-high`: Chế độ suy luận sâu (Deep thinking) cho các câu hỏi tổng hợp khó.
- `ag/gemini-3.8-flash-medium` / `ag/gemini-3.8-flash`: Thế hệ Flash mới nhất với độ dài context cực lớn.
- `ag/claude-sonnet-4-6`: Phiên bản Claude Sonnet định tuyến qua Antigravity, chất lượng hành văn kỹ thuật sắc sảo.

##### Nhóm 2: DeepSeek Native (`ds/`) — *Khuyến nghị Tư duy Logic*
- **`ds/deepseek-chat`** ⭐ **(Khuyên dùng cho Diễn giải Tri thức):** Bản DeepSeek V3 tiếng Việt và tiếng Anh cực chuẩn, tổng hợp nội dung mạch lạc.
- **`ds/deepseek-reasoner`** ⭐ **(Khuyên dùng cho Phân tích Đa chiều):** Bản DeepSeek R1 với chuỗi suy luận (Chain-of-thought) chi tiết trước khi trả lời.

##### Nhóm 3: Kimi / Multi-Provider Gateway (`kr/`) — *Khuyến nghị Dự phòng Bền bỉ*
- **`kr/auto`** ⭐ **(Khuyên dùng làm Fallback Model):** Tự động chọn mô hình tối ưu nhất và tự động chuyển sang mô hình dự phòng khi nhà cung cấp chính bị chạm hạn mức (HTTP 429).
- `kr/claude-sonnet-4.6` / `kr/claude-sonnet-5`: Dòng Claude Sonnet qua Kimi Router.
- `kr/deepseek-3.2` / `kr/deepseek-3.2-thinking`: DeepSeek reasoning.
- **`kr/qwen3-coder-next`** ⭐ **(Khuyên dùng cho Kho Tài liệu Code):** Dòng Qwen Coder tối ưu hóa đặc biệt cho mã nguồn, cú pháp Markdown, lệnh shell và cấu trúc JSON.

##### Nhóm 4: Codex / GPT Next (`cx/`)
- `cx/gpt-5.6-sol` / `cx/gpt-5.5` / `cx/gpt-5.4`: Các model GPT thế hệ mới.
- `cx/gpt-6-astra`: Mô hình thử nghiệm hiệu năng cao.

---

#### 3. Các bước Cài đặt Từng bước trong WeKnora UI

1. Đăng nhập WeKnora tại [http://localhost:80](http://localhost:80).
2. Nhấp vào biểu tượng **Settings** (Bánh răng) ở thanh bên trái $\rightarrow$ Chọn mục **Model Providers**.
3. Bấm nút **Add Provider**:
   - **Provider Type:** Chọn **OpenAI** (hoặc **OpenAI Compatible**).
   - **Name:** Điền `9Router Gateway`.
   - **Base URL:** Điền `http://host.docker.internal:20127/v1`
   - **API Key:** Dán chuỗi `sk-4159bc8f7dbb711a-7chwxp-3d6bc0ef`
4. Bấm **Save & Test Connection** để hệ thống xác nhận kết nối thành công.
5. **Đăng ký các Model sử dụng:**
   - Bấm **Add Model** dưới provider 9Router vừa tạo.
   - Lần lượt thêm các Model ID bạn muốn dùng:
     - Model ID: `ag/gemini-3.7-flash-medium` | Tên hiển thị: `Gemini 3.7 Flash` | Type: `Chat`
     - Model ID: `ds/deepseek-chat` | Tên hiển thị: `DeepSeek V3` | Type: `Chat`
     - Model ID: `ds/deepseek-reasoner` | Tên hiển thị: `DeepSeek R1` | Type: `Chat / Reasoner`
     - Model ID: `kr/auto` | Tên hiển thị: `Auto Fallback Router` | Type: `Chat`
     - Model ID: `kr/qwen3-coder-next` | Tên hiển thị: `Qwen Coder Next` | Type: `Chat / Code`

#### 4. Lệnh Kiểm tra Kết nối từ Terminal (Verification Command)
Để kiểm tra kết nối từ container Docker đến 9Router mà không cần mở UI:

```powershell
# Kiểm tra WeKnora backend container truy vấn danh sách model của 9Router
docker exec WeKnora-app curl -s -H "Authorization: Bearer sk-4159bc8f7dbb711a-7chwxp-3d6bc0ef" http://host.docker.internal:20127/v1/models
```
*(Nếu kết quả trả về danh sách JSON chứa các model `ag/...`, `ds/...`, `kr/...` là kết nối thông suốt 100%).*

---

### 3.2. Cấu hình Embedding Model qua Ollama Local

Do 9Router tập trung tối ưu hóa cho các mô hình Chat/Completion, để lập chỉ mục vector (Embedding) cho Knowledge Base với chi phí bằng 0 và tốc độ cao nhất, ta kết hợp với **Ollama** chạy ngay trên máy chủ Windows:

1. **Endpoint kết nối:** `http://host.docker.internal:11434`
2. **Khởi động Ollama lắng nghe tất cả interface:**
   ```powershell
   # Đảm bảo biến môi trường OLLAMA_HOST cho phép Docker kết nối
   $env:OLLAMA_HOST = "0.0.0.0:11434"
   # Kéo model embedding đa ngôn ngữ hàng đầu
   ollama pull bge-m3
   ```
3. **Thêm Provider trong WeKnora:**
   - **Provider Type:** `Ollama`
   - **Base URL:** `http://host.docker.internal:11434`
   - **Model ID:** `bge-m3` (Type: `Embedding`, Dimension: `1024`)

> [!IMPORTANT]
> **Quy tắc Bất biến về Embedding Model:**  
> Một Knowledge Base khi đã được tạo và gán một Embedding Model (ví dụ `bge-m3`) thì **toàn bộ tài liệu trong Knowledge Base đó phải sử dụng cùng số chiều vector (1024-dim)**. Không thể đổi Embedding Model giữa chừng cho một Knowledge Base đã có dữ liệu mà không re-index lại toàn bộ.

---

### 3.3. Cấu hình Trực tiếp với Cloud Providers (Tùy chọn Bổ sung)

Nếu muốn gọi trực tiếp đến API đám mây mà không qua 9Router:

| Nhà cung cấp | Base URL | API Key | Model Chat Khuyến nghị | Model Embedding Khuyến nghị |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI Native** | `https://api.openai.com/v1` | `sk-...` | `gpt-4o`, `gpt-4o-mini` | `text-embedding-3-small` (1536-dim) |
| **DeepSeek Native** | `https://api.deepseek.com/v1` | `sk-...` | `deepseek-chat`, `deepseek-reasoner` | *(Kết hợp BGE-M3 của Ollama)* |
| **Google Gemini Native** | `https://generativelanguage.googleapis.com/v1beta` | `AIza...` | `gemini-1.5-flash` | `text-embedding-004` (768-dim) |

---

## 4. Quản lý Kho Tri thức (Knowledge Base Management)

Kho tri thức (**Knowledge Base - KB**) là đơn vị tổ chức tài liệu cốt lõi trong WeKnora. Mỗi KB đại diện cho một chủ đề nghiên cứu, một dự án hoặc một kho lưu trữ chuyên biệt (ví dụ: *Hạ tầng Cloud*, *Kiến trúc AI Agent*, *Tài liệu Dự án Wiki*).

### 4.1. Tạo Knowledge Base Mới

1. Tại thanh điều hướng bên trái, chọn **Knowledge Bases** $\rightarrow$ Bấm nút **Create Knowledge Base**.
2. Điền các thông số cơ bản:
   - **Name:** Tên kho tri thức (ví dụ: `Personal Wiki Archives`, `AI Engineering Docs`).
   - **Description:** Tóm tắt phạm vi tri thức để AI có thể tự định tuyến câu hỏi khi ở chế độ Multi-KB.
   - **Avatar / Color:** Đặt màu sắc nhận diện.
3. **Cấu hình Engine:**
   - **Embedding Model:** Chọn mô hình embedding đã khai báo ở mục 3 (ví dụ `bge-m3` hoặc `text-embedding-3-small`).
   - **Language:** Chọn `en-US` hoặc `vi-VN` tùy tài liệu nguồn chủ đạo.

### 4.2. Chiến lược Phân đoạn (Chunking Strategy)

WeKnora cung cấp bộ điều khiển thông số phân đoạn linh hoạt để tối ưu hóa khả năng truy xuất:

| Tham số | Giá trị Khuyến nghị | Ý nghĩa Kỹ thuật |
| :--- | :--- | :--- |
| **Chunk Size** | `600 - 800 tokens` | Kích thước lý tưởng: đủ lớn để chứa trọn vẹn một luận điểm/đoạn văn, nhưng đủ nhỏ để không làm loãng vector embedding. |
| **Chunk Overlap** | `100 - 150 tokens` | Độ gối đầu giữa 2 đoạn liên tiếp: đảm bảo các câu văn ở ranh giới cắt không bị đứt đoạn ngữ nghĩa. |
| **Separators** | `\n\n`, `\n`, `. `, `? `, `! ` | Thứ tự ưu tiên ngắt đoạn: ưu tiên ngắt theo đoạn văn đôi, sau đó đến dòng đơn, rồi mới đến câu kết thúc bằng dấu chấm. |
| **Header Inheritance** | `Bật (True)` | Tự động kế thừa cấu trúc Heading (`# H1`, `## H2`) vào đầu mỗi chunk để giữ trọn vẹn ngữ cảnh phân cấp của văn bản. |

### 4.3. Tải lên và Bóc tách Tài liệu (Document Ingestion)

1. Mở Knowledge Base vừa tạo $\rightarrow$ Bấm **Upload Documents**.
2. Kéo thả các tập tin cần nạp. Định dạng hỗ trợ qua `docreader`:
   - **Văn bản & Báo cáo:** `.pdf`, `.docx`, `.doc`, `.txt`.
   - **Ghi chú & Kỹ thuật:** `.md` (Markdown từ `my-wiki`), `.rst`, `.html`.
   - **Bảng dữ liệu & Thuyết trình:** `.xlsx`, `.csv`, `.pptx`.
3. Nhấp **Process & Ingest**.
4. Theo dõi thanh tiến trình (Pipeline Monitor):
   $$\text{Uploaded} \longrightarrow \text{Parsing (DocReader)} \longrightarrow \text{Chunking} \longrightarrow \text{Embedding (pgvector)} \longrightarrow \text{Ready}$$

---

## 5. RAG Pipeline & Hỏi đáp Có Trích dẫn (Verifiable Citations)

Điểm vượt trội của WeKnora so với các ứng dụng Chat RAG đơn giản là khả năng **truy xuất lai (Hybrid Search)** kết hợp kiểm chứng trích dẫn nguồn theo thời gian thực.

Sơ đồ chi tiết chu trình xử lý truy vấn:

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/rag-pipeline.html" width="100%" height="720" style="border:none;border-radius:0.75rem;box-shadow:0 4px 12px rgba(0,0,0,0.08);"></iframe>

### 5.1. Cơ chế Truy xuất Lai (Hybrid Retrieval Architecture)

Khi nhận câu hỏi từ người dùng, WeKnora thực thi song song hai luồng tìm kiếm:
1. **Full-Text BM25 Search (ParadeDB pg_search):**  
   Bắt chính xác các từ khóa hiếm, tên hàm (`dockerComposeUp`), mã hiệu lỗi (`ERR_PORT_CONFLICT`), thuật ngữ viết tắt (`RRF`, `MCP`).
2. **Dense Vector Search (pgvector):**  
   Bắt các câu hỏi diễn giải bằng ngôn ngữ tự nhiên mang ý nghĩa tương đồng nhưng không trùng từ khóa chính xác.
3. **Reciprocal Rank Fusion (RRF):**  
   Kết hợp thứ hạng của cả hai luồng bằng công thức:
   $$RRF\_Score(d) = \sum_{m \in \{BM25, Vector\}} \frac{1}{k + Rank_m(d)}$$
   với $k = 60$. Nhờ đó, tài liệu đứng đầu ở cả hai tiêu chí sẽ nhận điểm ưu tiên cao nhất mà không bị méo điểm số vì sự chênh lệch thang đo.

### 5.2. Hướng dẫn Tương tác & Kiểm chứng Trích dẫn (Reference Drawer)

1. Truy cập mục **Chat & Assistant** trên menu.
2. Chọn Knowledge Base cần hỏi tại menu thả xuống ở đầu trang.
3. Nhập câu hỏi cần tra cứu.
4. **Kiểm tra câu trả lời có trích dẫn:**
   - Trong nội dung phản hồi, các khẳng định quan trọng sẽ có số trích dẫn nổi bật dạng `[1]`, `[2]`.
   - Nhấp chuột trực tiếp vào nhãn `[1]`: Bảng **Reference Drawer** bên phải sẽ trượt ra, tự động tô sáng đoạn văn gốc và hiển thị rõ tên tập tin nguồn, số trang, điểm số tương đồng (Score).

```
┌──────────────────────────────────────────────────┬─────────────────────────────────┐
│ AI Chat Interface                                │ Reference Drawer (Right Panel)  │
│                                                  │                                 │
│ User: Làm sao xử lý xung đột cổng WeKnora?        │ 📄 Source: deployment-guide.md  │
│                                                  │ 🏷️ Chunk #4 (Score: 0.94)        │
│ Assistant:                                       │                                 │
│ Để giải quyết xung đột cổng mạng với các dịch    │ "...Đối với cổng 8080 đang bị  │
│ vụ hiện có (như Harness), bạn chỉ cần đặt biến   │ chiếm dụng bởi Git server,     │
│ APP_PORT=8085 trong file .env [1]. Khi đó cổng  │ cấu hình APP_PORT=8085 trong   │
│ UI 80 vẫn kết nối thông suốt qua reverse proxy.  │ file .env để tránh xung đột..." │
│                                                  │                                 │
│                                           ↑ [1]  │ [Edit Chunk]   [Jump to File]   │
└──────────────────────────────────────────────────┴─────────────────────────────────┘
```

### 5.3. Tính năng Hiệu chỉnh Chunk Trực tiếp (Chunk Editing)

Nếu bạn phát hiện tài liệu gốc có thông tin cũ hoặc bộ tách từ chưa chuẩn:
- Tại Reference Drawer, bấm nút **Edit Chunk** (Biểu tượng cây bút).
- Sửa trực tiếp nội dung văn bản hoặc thêm nhãn (Tags).
- Bấm **Save & Re-embed**: WeKnora sẽ tự động sinh lại vector embedding cho riêng chunk này mà không cần re-index toàn bộ tài liệu.

---

## 6. Tính năng Auto-Wiki (Mạng lưới Tri thức Tự động)

Khác với kho tài liệu tĩnh thông thường, WeKnora tích hợp engine **Auto-Wiki**:

- **Nhận diện Khái niệm (Concept Synthesis):**  
  Khi quét qua các tài liệu trong Knowledge Base, hệ thống tự động phát hiện các khái niệm xuyên suốt (ví dụ: *Docker Compose*, *ParadeDB*, *Reverse Proxy*).
- **Trang Wiki Tổng hợp:**  
  Engine tự động tạo trang tóm tắt cho từng khái niệm, trích xuất tất cả các đoạn văn bản từ các tập tin khác nhau có nhắc đến khái niệm đó.
- **Tạo Liên kết Chéo (Bidirectional Links):**  
  Tạo mạng lưới siêu liên kết hai chiều giúp người dùng đọc hiểu tri thức theo dạng bách khoa toàn thư cá nhân.

---

## 7. Tích hợp Bên ngoài & MCP Server (Model Context Protocol)

WeKnora đóng vai trò là **Bộ não Tri thức (Knowledge Server)** cho các công cụ AI khác trên máy cá nhân thông qua API và giao thức **MCP (Model Context Protocol)**.

### 7.1. Lấy API Token từ WeKnora
1. Nhấp vào Avatar góc trên bên phải $\rightarrow$ **API Keys**.
2. Bấm **Generate New Token**.
3. Đặt tên token (ví dụ: `Hermes-Agent-Token` hoặc `Claude-Desktop-Token`) $\rightarrow$ Lưu lại chuỗi khóa bí mật.

### 7.2. Tích hợp với Claude Desktop
Thêm đoạn cấu hình sau vào file cấu hình Claude Desktop (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "weknora-knowledge": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-weknora",
        "--api-url",
        "http://localhost:8085",
        "--api-key",
        "YOUR_WEKNORA_API_TOKEN"
      ]
    }
  }
}
```

### 7.3. Tích hợp với Cursor / VS Code Agent
Trong cấu hình MCP của Cursor (`Settings` $\rightarrow$ `Features` $\rightarrow$ `MCP`):
- **Name:** `weknora`
- **Type:** `command`
- **Command:** `npx -y @modelcontextprotocol/server-weknora --api-url http://localhost:8085 --api-key YOUR_WEKNORA_API_TOKEN`

Bây giờ trong cửa sổ chat của Cursor hoặc Claude Desktop, bạn có thể gõ:
> *"@weknora tra cứu tài liệu kiến trúc của dự án my-wiki và liệt kê các container đang chạy."*  
AI sẽ tự động gọi WeKnora qua MCP, truy xuất các chunk liên quan và phản hồi chính xác.

### 7.4. Truy vấn Nhanh qua REST API bằng cURL / PowerShell
Bạn có thể tích hợp WeKnora vào các script tự động hóa:

```powershell
# Ví dụ truy vấn Knowledge Base qua PowerShell
$headers = @{
    "Authorization" = "Bearer YOUR_WEKNORA_API_TOKEN"
    "Content-Type"  = "application/json"
}

$body = @{
    knowledge_base_id = "YOUR_KB_ID"
    query             = "Chiến lược phân bổ cổng WeKnora là gì?"
    top_k             = 3
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8085/api/v1/retrieval/search" -Method Post -Headers $headers -Body $body
$response.data.chunks | ForEach-Object { $_.content }
```

---

## 8. Vận hành & Bảo trì Thường nhật (Ops & Maintenance)

Tất cả các lệnh vận hành dưới đây được thực hiện tại thư mục gốc: `D:\4.Code\weknora`.

### 8.1. Các Lệnh Vận hành Cơ bản

```powershell
# Di chuyển đến thư mục cài đặt
cd D:\4.Code\weknora

# Xem trạng thái các container
docker compose ps

# Xem nhật ký hoạt động thời gian thực của backend
docker compose logs -f app

# Xem nhật ký xử lý bóc tách tài liệu của docreader
docker compose logs -f docreader

# Khởi động lại toàn bộ hệ thống
docker compose restart

# Dừng hệ thống khi không làm việc (KHÔNG dùng cờ -v để bảo toàn dữ liệu)
docker compose down
```

### 8.2. Sao lưu Dữ liệu (Backup & Export)

Dữ liệu quan trọng nhất của WeKnora nằm ở cơ sở dữ liệu PostgreSQL (chứa thông tin bảng, tài liệu và vector embeddings).

```powershell
# Xuất toàn bộ cơ sở dữ liệu WeKnora ra file SQL
docker exec WeKnora-postgres pg_dumpall -U weknora > D:\4.Code\weknora\weknora_backup_$(Get-Date -Format "yyyyMMdd").sql

# Phục hồi dữ liệu từ file backup (khi cần)
# Get-Content D:\4.Code\weknora\weknora_backup.sql | docker exec -i WeKnora-postgres psql -U weknora -d weknora
```

### 8.3. Bảng Khắc phục Sự cố Nhanh (Troubleshooting)

| Hiện tượng | Nguyên nhân có thể | Cách xử lý |
| :--- | :--- | :--- |
| **Không mở được Web UI (80)** | Cổng 80 bị chiếm bởi IIS hoặc tiến trình khác trên Windows | Đổi `FRONTEND_PORT=8081` trong `.env`, sau đó chạy `docker compose up -d frontend` |
| **DocReader báo lỗi khi upload PDF** | File PDF scan ảnh không có text layer | Bật OCR trong cấu hình KB hoặc kiểm tra log: `docker compose logs docreader` |
| **Không kết nối được Ollama** | Khai báo nhầm `localhost` thay vì Docker host network | Đổi URL của Provider thành `http://host.docker.internal:11434` |
| **Task bóc tách bị treo (Pending)** | Hàng đợi Asynq / Redis bị nghẽn | Kiểm tra Redis: `docker compose logs redis`, restart app: `docker compose restart app` |

---

## 9. Cẩm nang Vận hành Thực chiến & Giải đáp Thắc mắc (Operational Guide & FAQs)

Phần này tổng hợp các kinh nghiệm thực tế, quy tắc kiến trúc và cách xử lý các tình huống thường gặp trong quá trình vận hành WeKnora hàng ngày.

### 9.1. Phân loại & Vai trò 4 Nhóm Mô hình trong WeKnora (Model Taxonomy)

WeKnora phân định rạch ròi nhiệm vụ của 4 loại mô hình AI trong hệ thống:

| Nhóm Mô hình | Nhiệm vụ Cốt lõi | Cơ chế Hoạt động | Khuyến nghị Cấu hình |
| :--- | :--- | :--- | :--- |
| **Chat / Completion Model** | Phân tích câu hỏi, tổng hợp ngữ cảnh, đối thoại và trả lời người dùng. | Nhận Prompt văn bản $\rightarrow$ Sinh chuỗi phản hồi tự nhiên kèm trích dẫn. | **9Router:** `ag/gemini-3.7-flash-medium` (siêu nhanh, ngữ cảnh dài) hoặc `ds/deepseek-chat` (lập luận tiếng Việt tốt). |
| **Embedding Model** | Chuyển đổi văn bản thành các vector toán học đa chiều để đo độ tương đồng ngữ nghĩa. | Bi-Encoder: Biến đoạn văn hoặc câu hỏi thành 1 chuỗi số float (ví dụ 1024 chiều). **Không thể dùng model chat thuần túy làm embedding.** | **Ollama Local:** `bge-m3` (1024-dim, đa ngôn ngữ cực mạnh) hoặc `nomic-embed-text` (768-dim, siêu nhẹ ~274MB). |
| **Vision (VLM) Model** | "Nhìn" và hiểu hình ảnh, biểu đồ, tài liệu scan. | Đa phương thức (Multimodal): OCR nhận diện chữ/bảng biểu/công thức từ ảnh, sinh caption cho ảnh trong tài liệu RAG. | **9Router:** `ag/gemini-3.7-flash` hoặc **Ollama Local:** `qwen3.5:4b` / `minicpm-v`. *(Không bắt buộc nếu chỉ dùng file text/PDF có chữ).* |
| **ReRank Model** | Tái sắp xếp và chấm điểm độ liên quan chính xác của Top 20-50 đoạn văn bản sau vòng sơ loại. | Cross-Encoder: Đặt câu hỏi và đoạn văn cạnh nhau cùng lúc để so sánh sâu từng từ ngữ, loại bỏ tối đa ảo giác (hallucination). | **Remote API:** `bge-reranker-v2-m3` qua SiliconFlow/Jina. *(Không bắt buộc đối với kho tài liệu vừa và nhỏ).* |

---

### 9.2. Xử lý Lỗi SSRF khi Thêm Model Local (`hostname suffix .internal is restricted`)

Khi thêm model Ollama từ giao diện Web (`Settings` $\rightarrow$ `Model Management`), người dùng có thể gặp thông báo lỗi:
> `Base URL 未通过安全校验：SSRF validation failed: hostname suffix .internal is restricted... 示例：SSRF_WHITELIST_EXTRA=local.internal...`

#### 1. Nguyên nhân Kỹ thuật:
- Cơ chế bảo mật SSRF (*Server-Side Request Forgery*) của WeKnora mặc định chặn các tên miền nội bộ như `.internal`, `.local` để phòng ngừa tấn công mạng nội bộ.
- Trong giao diện thêm model, nếu để nguồn mặc định là **Remote** và tự gõ URL chứa `local.internal` hoặc `host.docker.internal` khi chưa đưa vào whitelist, bộ lọc sẽ từ chối kết nối.
- Bên trong container Docker, địa chỉ `local.internal` không thể tự phân giải về máy Windows host; địa chỉ chính xác bắt buộc phải là `http://host.docker.internal:11434`.

#### 2. Giải pháp Chuẩn mực:
* **Cách 1 (Thao tác đúng trên UI):**
  - Trong hộp thoại **+ Add Model**, chuyển mục **Model Source (模型来源)** sang tab **Local (本地 / Ollama)** thay vì để *Remote*.
  - WeKnora sẽ tự động gọi API nội bộ tới Ollama và liệt kê danh sách các model đã tải trên máy bạn trong ô chọn dropdown. Bạn chỉ việc chọn tên model và bấm Save, hệ thống tự động điền cấu hình ngầm mà không kích hoạt lỗi SSRF.
* **Cách 2 (Mở rộng Whitelist SSRF qua API an toàn):**
  - WeKnora hỗ trợ cập nhật whitelist tức thì qua API mà không cần restart container:
    ```powershell
    $loginBody = @{ email = 'smoketest@local.internal'; password = 'SmokeTestPassword123!' } | ConvertTo-Json
    $res = Invoke-RestMethod -Uri 'http://localhost:8085/api/v1/auth/login' -Method Post -ContentType 'application/json' -Body $loginBody
    $headers = @{ Authorization = "Bearer $($res.token)"; "Content-Type" = "application/json" }
    $body = @{ value = @("host.docker.internal", "local.internal", "*.internal", "localhost", "127.0.0.1") } | ConvertTo-Json
    Invoke-RestMethod -Uri 'http://localhost:8085/api/v1/system/admin/settings/ssrf.whitelist' -Method Put -Headers $headers -Body $body
    ```
  > [!CAUTION]
  > **Tuyệt đối KHÔNG chạy `docker compose up -d app` đơn lẻ** để cập nhật biến môi trường SSRF: Docker sẽ cấp IP mới cho container `app`, trong khi Nginx reverse proxy ở `frontend` vẫn trỏ IP cũ, dẫn đến lỗi toàn hệ thống **502 Bad Gateway**. Mọi cập nhật cấu hình runtime nên ưu tiên qua API hệ thống.

---

### 9.3. Cấu hình Ngôn ngữ Tiếng Việt Chuẩn mực

Để toàn bộ hệ thống WeKnora và các Agent luôn phản hồi mạch lạc bằng Tiếng Việt:

1. **Ở cấp độ từng Agent (Hiệu quả nhất):**
   - Mở cửa sổ **Edit Agent** $\rightarrow$ Chọn tab **Prompts Configuration** (biểu tượng *File-Paste* bên trái).
   - Tại ô **System Prompt**, bổ sung chỉ thị ưu tiên:
     ```text
     - Luôn luôn trả lời người dùng bằng Tiếng Việt chuẩn mực, tự nhiên, chính xác và mạch lạc.
     - Ngay cả khi tài liệu tham khảo hoặc câu hỏi gốc bằng tiếng Anh hay tiếng Trung, câu trả lời cuối cùng vẫn phải được dịch và diễn đạt hoàn toàn bằng Tiếng Việt (trừ các thuật ngữ kỹ thuật chuyên ngành cần giữ nguyên).
     ```
   - Tại ô **Fallback Response** (khi không tìm thấy tài liệu), đổi thành tiếng Việt:
     `"Xin lỗi, thông tin bạn cần hiện chưa có trong cơ sở tri thức."`
2. **Ở cấp độ Toàn hệ thống (Docker Server):**
   - Trong file `D:\4.Code\weknora\.env`, thêm biến môi trường:
     ```bash
     WEKNORA_LANGUAGE=vi-VN
     ```
   - Hệ thống sẽ dùng thiết lập này làm ngôn ngữ đích cho các tác vụ ngầm (sinh tóm tắt tài liệu, phân loại nhãn tự động, trích xuất thực thể).

---

### 9.4. Cơ chế Cập nhật Tài liệu & Chống trùng lặp (Deduplication & Sync)

#### 1. WeKnora có tự động nhận biết thay đổi trong folder máy tính không?
👉 **KHÔNG.** Vì WeKnora chạy độc lập bên trong Docker container, hệ thống không gắn tiến trình theo dõi file (*file watcher*) liên tục trên ổ cứng máy bạn để tránh tốn CPU/RAM và rủi ro bảo mật. Khi bạn sửa file hoặc thêm file mới vào folder, bạn cần đưa file đó vào WeKnora.

#### 2. Cơ chế Chống trùng lặp thông minh (Deduplication via SHA-256 Hash):
WeKnora tích hợp bộ kiểm tra `CheckKnowledgeExists` dựa trên mã băm nội dung `file_hash` (SHA-256), `file_size` và định dạng `file_type`:
- **Khi kéo thả lại nguyên cả folder vào Knowledge Base:**
  - **File không thay đổi:** WeKnora tính mã hash thấy trùng với bản ghi cũ $\rightarrow$ **Tự động BỎ QUA (Skip)**, không tốn tài nguyên cắt chunk và không chạy lại embedding `bge-m3`.
  - **File mới thêm vào:** WeKnora nhận diện hash chưa tồn tại $\rightarrow$ Tự động bóc tách và tạo vector mới.
  - **File bị sửa nội dung:** Mã hash thay đổi $\rightarrow$ WeKnora coi đây là nội dung mới và nạp vào (tạo thêm 1 bản ghi mới).
- **Quy tắc thao tác chuẩn:**
  - Khi thêm file mới: Cứ kéo thả file mới (hoặc kéo cả folder) vào Knowledge Base.
  - Khi chỉnh sửa file cũ: Bấm **Delete** đúng file cũ trên UI WeKnora, sau đó tải file mới đã sửa lên lại.
  > [!WARNING]
  > **KHÔNG NÊN XÓA SẠCH CẢ KNOWLEDGE BASE RỒI UPLOAD LẠI:** Việc xóa sạch sẽ làm mất toàn bộ vector trong database, buộc hệ thống phải chạy lại toàn bộ quy trình embedding từ đầu cho 100% tài liệu, gây lãng phí thời gian và tài nguyên máy tính.

---

### 9.5. Giải mã 4 Built-in Agents: Khi nào nên dùng Agent nào?

WeKnora tích hợp sẵn 4 trợ lý ảo mẫu đại diện cho 4 phong cách làm việc khác nhau:

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────────────────┐
│     ⚡ Quick Answer     │   🧠 Smart Reasoning    │   📚 Wiki Questioner    │    📊 Data Analyst      │
├─────────────────────────┼─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ • RAG 1 bước (One-shot) │ • ReAct Agent đa bước   │ • Chuyên biệt cho Wiki  │ • Chuyên dữ liệu số     │
│ • Tốc độ: 1 - 2 giây    │ • Tự lập kế hoạch       │ • Tra cứu bách khoa thư │ • Tự viết và chạy SQL   │
│ • Tiết kiệm token nhất  │ • Gọi nhiều công cụ     │ • Phát hiện mâu thuẫn   │ • Nhiệt độ thấp (0.3)   │
│ • Tra cứu nhanh sự thật │ • So sánh, suy luận sâu │ • Đọc tài liệu nguồn    │ • Tính toán chính xác   │
└─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

1. **Quick Answer:** Phù hợp nhất cho nhu cầu hỏi đáp văn bản thông thường, tra cứu quy chế, thông số kỹ thuật rõ ràng. Phản hồi tức thì.
2. **Smart Reasoning:** Dành cho các bài toán phức tạp đòi hỏi xâu chuỗi thông tin từ nhiều nguồn, ví dụ: *"So sánh kiến trúc bảo mật giữa tài liệu A và tài liệu B, chỉ ra điểm khác biệt cốt lõi"*.
3. **Wiki Questioner:** Khai thác tối đa sức mạnh của mạng lưới tri thức liên kết (Wiki Pages & Cross-links), phù hợp cho kho tài liệu kiến trúc phần mềm, bách khoa thư dự án.
4. **Data Analyst:** Bắt buộc sử dụng khi tải lên file CSV hoặc Excel (`.xlsx`). Agent sẽ chuyển hóa câu hỏi tự nhiên thành câu lệnh SQL để truy vấn trực tiếp vào bảng số liệu, không đoán mò kết quả.

---

### 9.6. Chiến lược Quản lý Knowledge Base: Khi nào nên tạo KB mới?

Bạn nên phân chia hoặc tạo mới Knowledge Base dựa trên 4 tiêu chuẩn thực tế:

1. **Khác nhau về Miền Kiến thức / Chủ đề:** Tách biệt rõ giữa *Tài liệu Lập trình/Kỹ thuật* và *Tài liệu Nhân sự/Hành chính*. Việc chia tách giúp công cụ tìm kiếm vector không bị nhầm lẫn giữa các thuật ngữ giống nhau nhưng khác ngữ cảnh.
2. **Phục vụ các Agent Chuyên biệt:** Gán Agent Kỹ thuật chỉ đọc KB Kỹ thuật; Agent Hỗ trợ chỉ đọc KB Sản phẩm để câu trả lời luôn tập trung và chính xác.
3. **Bảo mật & Phân quyền (Shared Spaces):** Tạo KB riêng cho tài liệu dùng chung để chia sẻ cho nhóm, và KB riêng cho các nghiên cứu cá nhân bảo mật.
4. **Khác nhau về Bản chất Dữ liệu:** 
   - **Document KB:** Dành cho văn bản dài, tài liệu PDF, DOCX, sách báo.
   - **FAQ KB:** Dành cho danh sách các cặp câu Hỏi - Đáp ngắn (truy xuất nhanh và độ chuẩn xác 100%).

> [!TIP]
> **Khi nào KHÔNG CẦN tạo KB mới?**  
> Nếu các tài liệu cùng thuộc một dự án hoặc một chủ đề lớn, hãy tận dụng tính năng **Thư mục (Folders)** bên trong Knowledge Base để phân loại, thay vì tạo quá nhiều KB rời rạc gây khó quản lý.

---

## 10. Tổng kết

WeKnora mang lại cho người dùng cá nhân một môi trường quản trị tri thức mạnh mẽ, riêng tư và hoàn toàn làm chủ. Kết hợp với kho tài liệu tĩnh **my-wiki**, bạn có được một kiến trúc tri thức toàn diện:
- **my-wiki:** Soạn thảo, tổ chức cây thư mục, lưu trữ phiên bản Git và xuất bản tĩnh trực quan.
- **WeKnora:** Chỉ mục hóa sâu, tìm kiếm ngữ nghĩa lai, hỏi đáp đối thoại với độ chính xác cao và làm bộ não MCP cho các tác tử lập trình.
