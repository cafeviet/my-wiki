# Báo cáo Kiến trúc & Nợ Kỹ thuật CNTT

> **Tài liệu tham chiếu:** Báo cáo Đánh giá Mức độ Sẵn sàng Công nghệ và AI (CS5 Assessment — 09/2026) · **Đơn vị khảo sát:** MBBank (MB).  
> **Đối tượng độc giả:** Enterprise Architects, Solution Architects, Giám đốc Công nghệ (CTO), Trưởng ban Chuyển đổi Số, Đội ngũ Kỹ sư Dữ liệu & MLOps, Chuyên gia An toàn Thông tin (CISO).  
> **Mục tiêu báo cáo:** Bóc tách toàn diện các khiếm khuyết mang tính hệ thống, nợ kỹ thuật (Technical Debt) và rủi ro kiến trúc trong các giải pháp AI hiện hành; từ đó xác lập **Bản thiết kế Kiến trúc CNTT Mục tiêu (Target Architecture Blueprint)** chuẩn hóa cho toàn ngân hàng.
>
> 📖 **Xem bài nghiên cứu tổng thể:** [Đánh giá Sẵn sàng Công nghệ và AI tại Ngân hàng (Toàn văn)](./) — Tầm nhìn chiến lược, mô hình Hub-and-Spoke và phân tích 11 Use Cases.

---

## 1. Tóm tắt Đánh giá Kiến trúc (Architecture Executive Summary)

Qua kiểm toán 11 trường hợp sử dụng AI (AI Use Cases) và 19 cấu phần dữ liệu & công nghệ tại ngân hàng, thực trạng kiến trúc CNTT phục vụ AI hiện tại bộc lộ sự **mất cân đối nghiêm trọng giữa "Bề mặt Ứng dụng" và "Độ vững chắc của Nền tảng"**:

```
 [ BỀ MẶT ỨNG DỤNG ] 11 Use Cases (App, Biz, Cards, Credit Memo, Contact Center...)
        ▲
        │  (Kết nối điểm-nhiều-điểm tùy tiện, thiếu Gateway, thiếu MLOps)
        ▼
 [ NỀN TẢNG KỸ THUẬT ] 5/19 Thành phần xếp hạng THẤP (Low) — Nghẽn DataOps, MLOps, Data Domains
                       12/19 Thành phần xếp hạng VỪA (Medium) — Dữ liệu phân mảnh, thủ công
                       Duy nhất 1/19 Thành phần xếp hạng CAO (High) — Cổng phân phối API
```

### Các chỉ số nợ kỹ thuật đáng báo động:
1. **5 điểm nghẽn xếp hạng Thấp (Low Maturity):**
   * **DataOps & MLOps:** Quy trình chuẩn bị dữ liệu và dán nhãn thủ công; lệch pha (mismatch) giữa môi trường thử nghiệm và sản xuất.
   * **Data Domains:** Dữ liệu lưu trữ theo các kho kỹ thuật vật lý rời rạc, chưa tổ chức thành Domain và thiếu Data Domain Owners.
   * **Data Operating Model:** Vận hành phân tán, tồn tại nhiều dự án thử nghiệm (PoC) tự phát ngoài tầm kiểm soát của kiến trúc doanh nghiệp.
   * **Mô hình Ưu tiên Đề tài (Op Model for Priorities):** Xử lý theo vụ việc cá nhân, thiếu quy hoạch kiến trúc tổng thể.
   * **Nhân lực & Văn hóa Kỹ thuật (Talent & Resourcing):** Thiếu hụt nghiêm trọng Kỹ sư Dữ liệu (Data Engineers), Kỹ sư MLOps và Kiến trúc sư Giải pháp AI (AI Solution Architects).
2. **Nguy cơ sụp đổ kiến trúc khi mở rộng quy mô (Scale Breakdown):**
   * Dữ liệu đầu vào bẩn và thiếu chuẩn hóa buộc kiến trúc phải lùi về các tập quy tắc tĩnh (như trường hợp **AI Beerich** phải bỏ ML để dùng rule-based).
   * Không có cơ chế kiểm soát chất lượng mô hình tự động: Thiếu bộ dữ liệu chuẩn (Golden Dataset), thiếu kiểm thử hồi quy (Regression Test) và không có công cụ giám sát độ trôi (Drift Observability) trong sản xuất.
   * Hiện tượng "Shadow AI" và rủi ro an toàn thông tin khi tích hợp LLM từ bên thứ ba mà không có **Cổng điều phối tập trung (Enterprise LLM Gateway)** và **Tường lửa AI (AI Guardrails)**.

---

## 2. Phân tích Chi tiết 6 Nhóm Khiếm khuyết Kiến trúc Cốt lõi

### 2.1. Kiến trúc Tổ chức & Ranh giới Hệ thống (Conway's Law & Siloed Boundaries)

Khảo sát cơ cấu Khối CNTT (IT Division) cho thấy đơn vị AI hiện được bố trí như một phòng kỹ thuật chuyên sâu trực thuộc IT:

```
                            KHỐI CÔNG NGHỆ THÔNG TIN (IT DIVISION)
 ┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
 │    IT Governance     │  Business Analysis   │  Quality Assurance   │ Platform Technology  │
 ├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
 │  Digital Technology  │       AI UNIT        │Technology Operations │  IT Infrastructure   │
 │                      │  • Virtual Assistant │                      │                      │
 │                      │  • Computer Vision   │                      │ Information Security │
 │                      │  • Language & Speech │                      │                      │
 │                      │  • AI R&D and Apps   │                      │                      │
 └──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

#### Hệ quả kiến trúc theo Định luật Conway:
* **Hòn đảo Công nghệ Độc lập (Isolated Tech Island):** Kiến trúc của phần mềm phản chiếu cơ cấu tổ chức của doanh nghiệp. Vì nhóm AI nằm biệt lập và chia theo các "mảng thuật toán" (Vision, Speech, Bot, R&D), hệ thống AI sinh ra dưới dạng các **dịch vụ vi mô rời rạc (Point Solutions)** thay vì các dịch vụ nghiệp vụ tích hợp.
* **Đứt gãy Khâu Bàn giao & Hợp đồng Dữ liệu (Broken Handoffs):** Lập trình viên AI phải tự mình khảo sát các Khối nghiệp vụ để hỏi cấu trúc trường thông tin. Quy trình này dẫn đến việc không có **Đặc tả Giao diện Dữ liệu (Data Contract)** chính thức, làm các API tích hợp AI bị biến động liên tục khi nghiệp vụ thay đổi mẫu biểu.
* **Thiếu vắng Vai trò Kiến trúc Cầu nối:** Không có các Kiến trúc sư AI am hiểu sâu nghiệp vụ ngân hàng (AI–Business Translators) để chuẩn hóa yêu cầu phi chức năng (Non-functional Requirements - NFR) như độ trễ (Latency), chi phí token trên mỗi giao dịch, tính sẵn sàng (Availability) và độ chính xác tối thiểu trước khi code.

---

### 2.2. Kiến trúc Dữ liệu & Sự Thiếu vắng Mô hình Data Mesh (Data Architecture Pitfalls)

Đánh giá 19 cấu phần dữ liệu cho thấy hệ thống dữ liệu phục vụ AI đang chịu tải bởi các kiến trúc kiểu cũ:

```
 [ HIỆN TRẠNG: DATA STORAGE SILOS ]             [ MỤC TIÊU: DOMAIN DATA MESH ]
  Kho dữ liệu A ──┐                              ┌── Domain Bán lẻ (Data Product)
  Kho dữ liệu B ──┼─> [ Hồ dữ liệu tập trung ] ──┼── Domain Tín dụng (Data Product)
  Kho dữ liệu C ──┘     (Thiếu Data Owner)       └── Domain Vận hành (Data Product)
```

1. **Lưu trữ dạng Kho Kỹ thuật (Storage Silos) thay vì Domain Nghiệp vụ (Data Domains — Xếp hạng Low):**
   * Dữ liệu được gom tụ thụ động về Kho dữ liệu (Data Warehouse) và Hồ dữ liệu (Data Lake) nhưng không phân chia theo ranh giới nghiệp vụ (Bounded Contexts).
   * Không có cá nhân hoặc phòng ban nào chịu trách nhiệm làm **Chủ sở hữu Dữ liệu (Data Domain Owner)**. Khi mô hình AI dự báo sai lệch do dữ liệu đầu vào bị thiếu hoặc trễ, đội ngũ kỹ sư IT và chuyên viên nghiệp vụ đổ lỗi cho nhau do không có SLA dữ liệu rõ ràng.
2. **Khủng hoảng Chất lượng Dữ liệu Đầu vào (Data Dirt Trap — Case AI Beerich):**
   * Trong giải pháp **AI Beerich** (phân loại giao dịch tài chính lớn), hệ thống dự kiến sử dụng mô hình học máy để phân loại giao dịch tự động. Tuy nhiên, do dữ liệu giao dịch gốc bị nhiễu, thiếu chuẩn hóa ký tự và trường thông tin không đồng nhất, mô hình AI không thể hội tụ độ chính xác mong muốn.
   * **Hậu quả kiến trúc:** Kỹ sư buộc phải thiết kế lùi về **Tập luật tĩnh (Static Rule-based Engine)**, làm triệt tiêu hoàn toàn khả năng thích ứng linh hoạt và biến giải pháp AI thành một hệ thống if-else cồng kềnh, khó bảo trì.
3. **Master Data Management (MDM — Xếp hạng Medium) chắp vá:**
   * Mặc dù đã định danh mã khách hàng duy nhất (Common Customer ID) trên các hệ thống Core banking, nhưng dữ liệu từ các công ty con (MB Ageas Life, MBS, MBCambodia...) hoàn toàn bị cô lập.
   * Điều này ngăn cản kiến trúc xây dựng bức tranh **Hồ sơ Khách hàng 360 độ (Customer 360 Profile)** thời gian thực, dẫn đến các giải pháp như **AI Credit Scoring** bị giới hạn góc nhìn, đạt tỷ lệ chuyển đổi rất thấp (~0.2% đối với vay tín chấp cao cấp và ~5% đối với thẻ tín dụng).
4. **Quy trình Giám sát Dữ liệu Thụ động (Data Quality — Xếp hạng Medium):**
   * Việc kiểm tra chất lượng dữ liệu hiện tại chỉ làm thủ công theo các đợt định kỳ. Hệ thống không có cơ chế kiểm tra tự động dòng chảy dữ liệu (Data Lineage), không có công cụ tự động phát hiện dị thường (Data Profiling & Anomaly Detection) và thiếu kênh cảnh báo sự cố (Incident Escalation).

---

### 2.3. Khuyết tật Kiến trúc MLOps & Nền tảng Hạ tầng AI (MLOps & Platform Gaps)

Khảo sát chuyên sâu vòng đời của giải pháp **AI Credit Memo** (Hệ thống lập tờ trình thẩm định tín dụng tự động) làm lộ rõ các lỗ hổng chí mạng trong chuỗi cung ứng phần mềm AI:

```
             VÒNG ĐỜI AI CREDIT MEMO: CÁC ĐIỂM NGHẼN KIẾN TRÚC
 ┌──────────────────────┬──────────────────────┬──────────────────────┐
 │  THỬ NGHIỆM MÔ HÌNH  │  TÍCH HỢP & MVP      │  SCALE & VẬN HÀNH    │
 ├──────────────────────┼──────────────────────┼──────────────────────┤
 │• Thử nghiệm Gemini   │• Dev tự gõ cửa hỏi   │• Thiếu Regression Test│
 │• Thiếu Golden Dataset│• Thiếu HITL Router   │• Không giám sát Drift │
 │• Nguy cơ ảo giác cao │  tự động theo điểm số│• Không có retraining  │
 │  trên tài liệu dài   │  tin cậy (confidence)│  loop từ phản hồi RM  │
 └──────────────────────┴──────────────────────┴──────────────────────┘
```

1. **Chuẩn bị & Dán nhãn Dữ liệu Thủ công (DataOps & MLOps — Xếp hạng Low):**
   * Khâu làm sạch tài liệu, chuyển đổi định dạng và dán nhãn ngữ nghĩa (Annotation) cho các hồ sơ tín dụng vẫn thực hiện thủ công bằng tay. Điều này tạo ra nút cổ chai (Bottleneck) lớn nhất khiến thời gian phát triển mô hình bị kéo dài nhiều tháng.
2. **Lệch pha Môi trường Huấn luyện và Vận hành (Live vs Test Mismatch):**
   * Dữ liệu dùng để thử nghiệm mô hình là các tập tài liệu "sạch" được chọn lọc nhân tạo. Khi đưa ra môi trường sản xuất (Production), mô hình phải đối mặt với các bản scan mờ, văn bản viết tay, định dạng bảng biểu phức tạp và dữ liệu thiếu trường, dẫn đến tỷ lệ lỗi trích xuất tăng vọt.
3. **Sự Thiếu vắng Hoàn toàn của "Tập Dữ liệu Vàng" (Golden Dataset Benchmark):**
   * Ngân hàng không có một kho dữ liệu kiểm thử chuẩn mực được đóng băng (Frozen Golden Dataset) bao gồm đầy đủ các kịch bản hồ sơ từ dễ đến cực khó.
   * Khi nhóm phát triển cập nhật phiên bản mô hình (ví dụ: chuyển từ Gemini 1.5 Flash sang Gemini 1.5 Pro hoặc fine-tune mô hình mã nguồn mở), họ không thể chạy **Kiểm thử hồi quy tự động (Automated Regression Testing)** để chứng minh mô hình mới không làm hỏng các trường dữ liệu vốn đã chạy đúng trước đó.
4. **Mù Quan sát Độ trôi Mô hình (Model Drift Observability Blindness):**
   * Sau khi Golive, hệ thống không có công cụ giám sát thời gian thực để đo lường:
     * *Độ trôi dữ liệu (Data Drift):* Sự thay đổi trong hành vi người vay hoặc biểu mẫu pháp lý mới.
     * *Độ trôi khái niệm (Concept Drift):* Sự biến động của chính sách tín dụng hoặc khẩu vị rủi ro.
   * Hoàn toàn thiếu vắng **Vòng lặp đóng (Closed-Loop Feedback)**: Khi Relationship Manager (RM) sửa lại các số liệu do AI trích xuất sai trên Credit Memo, dữ liệu hiệu chỉnh này bị trôi đi mất thay vì được lưu trữ tự động vào tập dữ liệu tái huấn luyện (Retraining Dataset).

---

### 2.4. Sự Thiếu vắng Cấu phần Tái sử dụng: Enterprise LLM Gateway & Prompt Catalog

Hiện tại, các đội dự án AI tại ngân hàng đang tích hợp trực tiếp (Point-to-Point) vào các nhà cung cấp mô hình (Google, OpenAI...) hoặc tự dựng các model server riêng:

```
 [ HIỆN TRẠNG: KẾT NỐI TÙY TIỆN ]             [ MỤC TIÊU: ENTERPRISE LLM GATEWAY ]
  App MBBank ────> Google Gemini API             App MBBank ──┐
  Biz MBBank ────> OpenAI API                    Biz MBBank ──┼─> [ LLM GATEWAY ] ──> Multi-LLMs
  Credit Memo ───> Self-hosted Model             Credit Memo ─┘   • Rate Limit & Cost
                                                                  • Prompt Catalog
                                                                  • PII Redaction
```

#### Các rủi ro kiến trúc phát sinh do thiếu LLM Gateway:
1. **Mất kiểm soát Ngân sách Token & Chi phí API:** Mỗi use case tự tạo API key riêng, không có cơ chế giới hạn hạn ngạch (Quota Enforcement) theo phòng ban, không có báo cáo tập trung về lượng token tiêu thụ và chi phí tài chính thực tế.
2. **Không có Khả năng Chuyển mạch Dự phòng (Failover & Circuit Breaker):** Khi nhà cung cấp dịch vụ LLM gặp sự cố ngừng hoạt động (Outage) hoặc áp đặt giới hạn tốc độ (Rate Limit), các ứng dụng như AI Paste2Pay hoặc AI Customer sẽ lập tức bị treo cứng (Hung/Crash) thay vì tự động chuyển hướng truy vấn sang mô hình dự phòng (Fallback Model).
3. **Lãng phí Tài nguyên do Thiếu Bộ đệm (Semantic Caching):** Nhiều người dùng hỏi các câu hỏi có ngữ nghĩa tương đồng (như trong AI Enterprise hoặc AI SmartSearch), nhưng hệ thống không có lớp bộ đệm ngữ nghĩa (Semantic Cache) để trả lời ngay lập tức, mà vẫn gửi truy vấn đi xa, gây tốn kém chi phí và tăng độ trễ (Latency).
4. **Nguy cơ Rò rỉ Dữ liệu Nhạy cảm (PII Data Leakage):** Không có lớp lọc trung gian để tự động phát hiện và che giấu (Mask/Redact) số thẻ tín dụng, số CCCD/CMND, số tài khoản hoặc số dư của khách hàng trước khi gửi dữ liệu lên các mô hình LLM trên Cloud công cộng.
5. **Prompt Sprawl (Hỗn loạn Gợi ý):** Các đoạn mã prompt nằm rải rác trực tiếp trong mã nguồn (Hardcoded Prompts) của từng ứng dụng, không có hệ thống quản lý phiên bản (Prompt Registry), không thể đánh giá A/B test prompt và dễ bị tấn công bởi kỹ thuật **Prompt Injection**.

---

### 2.5. Thách thức Điều phối Đa phương thức & Luồng Human-in-the-Loop (HITL)

Khảo sát các use case Contact Center và Vận hành bộc lộ những hạn chế trong tầng điều phối (Orchestration Layer):

| Use Case | Biểu hiện kỹ thuật | Khiếm khuyết Kiến trúc Cốt lõi |
|---|---|---|
| **AI Paste2Pay** (Launched) | Độ phức tạp điều phối tăng vọt khi xử lý thông tin chuyển khoản dạng ảnh chụp màn hình hoặc text phi cấu trúc. | **Thiếu Pipeline Đa phương thức (Multimodal Ingestion Pipeline):** Xử lý hình ảnh và văn bản bị ghép nối thô sơ; không có engine tiền xử lý OCR phân tầng để tách biệt giữa khâu nhận dạng ký tự và khâu suy luận logic của LLM. |
| **AI Enterprise** (Launched) | Trải nghiệm truy vấn phức tạp bị giới hạn; mô hình quên ngữ cảnh sau 1–2 câu hỏi; 70% truy vấn dồn vào mảng Tín dụng. | **Thiếu Kiến trúc Bộ nhớ Ngữ cảnh Bền vững (Stateful Context Management):** Hệ thống RAG (Retrieval-Augmented Generation) xây dựng dạng Stateless đơn giản; không có bộ nhớ hội thoại đa tầng (Working Memory, Episodic Memory) để duy trì bối cảnh nghiệp vụ phức tạp. |
| **AI Customer** (Pilot) | Chất lượng trả lời dao động mạnh; điều hướng sai phòng ban hoặc sai nguồn tri thức. | **Kiến trúc Định tuyến Đơn tầng (Shallow Routing):** Bộ phân loại câu hỏi (Intent Classifier) không đủ năng lực xử lý các trường hợp mập mờ; thiếu cơ chế phân luồng theo độ phức tạp (Complexity-based Escalation) để tự động đẩy lên chuyên viên khi độ tự tin thấp. |
| **AI Credit Memo** (Launched) | Không thể đo lường thời gian tiết kiệm thực tế; chuyên viên tín dụng vẫn phải đọc lại toàn bộ hồ sơ. | **Thiếu Kiến trúc HITL Dựa trên Điểm Tin cậy (Confidence-based HITL):** Mô hình trích xuất ra văn bản nhưng không sinh ra điểm số tin cậy (Confidence Score) cho từng trường số liệu; hệ thống không thể tự động chỉ làm nổi bật (Highlight) các trường nghi ngờ để RM duyệt nhanh. |

---

### 2.6. Lỗ hổng Quản trị AI trong Phát triển Phần mềm (AI for IT & Supply Chain Risks)

Giải pháp **AI for IT** đã được triển khai rộng rãi cho đội ngũ lập trình viên và kiểm thử viên để tăng tốc độ viết code. Tuy nhiên, khảo sát ghi nhận: **"AI governance undefined — no established framework for controls and accountability"** (Quản trị AI hoàn toàn chưa được định nghĩa; không có khung kiểm soát và trách nhiệm giải trình).

#### 4 Rủi ro Kiến trúc & An ninh phần mềm nghiêm trọng:
1. **Rò rỉ Mã nguồn Bí mật (Source Code Exfiltration):** Lập trình viên có thể vô tình hoặc cố ý dán các đoạn mã chứa logic kinh doanh nhạy cảm, API keys, chuỗi kết nối database (Connection Strings) vào các công cụ AI công cộng.
2. **Nguy cơ Gói phần mềm Ảo giác (Hallucinated Package Attack):** Các mô hình sinh code thường gợi ý các thư viện bên thứ ba không tồn tại hoặc đã bị tin tặc chiếm quyền (Typosquatting). Nếu không có hệ thống kiểm soát dependency tự động, mã độc sẽ được nhúng thẳng vào hệ thống ngân hàng lõi.
3. **Rủi ro Bản quyền & Sở hữu Trí tuệ (IP Licensing Risks):** Code sinh ra từ mô hình AI có thể vi phạm các giấy phép mã nguồn mở nghiêm ngặt (như GPL/AGPL), gây rủi ro pháp lý cho ngân hàng khi thương mại hóa sản phẩm.
4. **Thiếu Trách nhiệm Giải trình (No Accountability Traceability):** Khi một đoạn mã do AI sinh ra gây lỗi dừng hệ thống (Outage) hoặc tạo ra lỗ hổng bảo mật zero-day, hệ thống Git hiện tại không ghi nhận rõ đoạn code nào do con người viết và đoạn code nào do AI sinh ra, làm vô hiệu hóa quy trình điều tra nguyên nhân gốc rễ (RCA).

---

## 3. Kiến trúc CNTT & AI Mục tiêu (Enterprise Target Architecture Blueprint)

Để khắc phục triệt để các khiếm khuyết kiến trúc nêu trên, ngân hàng cần thiết lập **Bản thiết kế Kiến trúc 4 Tầng Chuẩn hóa**:

<iframe src="/nghien-cuu/ngan-hang-so/mb-technology-and-ai-readiness/assets/04-it-target-architecture.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

---

### Phân tích Chức năng 4 Tầng Kiến trúc Mục tiêu

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │ LAYER 4: TẦNG KÊNH & TRẢI NGHIỆM NGHIỆP VỤ (CHANNELS & HITL DELIVERY)  │
 │ • RM Co-pilot     • Portal Thẩm định Tín dụng   • Contact Center Desk  │
 │ ──> TÍCH HỢP HITL CONFIDENCE ROUTER (ĐIỀU HƯỚNG THEO ĐỘ TIN CẬY) <──   │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ (Secure API & WebSocket)
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 3: TẦNG ĐIỀU PHỐI TÁC TỬ & NGỮ CẢNH (AGENTIC RUNTIME & CONTEXT)  │
 │ • Multi-Agent Orchestrator (LangGraph/Semantic Kernel)                 │
 │ • Stateful Session Memory (Working / Episodic Context)                 │
 │ • Domain Prompt Catalog & Tool-use Registry                            │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ (Internal Model Protocol)
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 2: TẦNG CỔNG AI & BẢO MẬT DÙNG CHUNG (ENTERPRISE LLM GATEWAY)   │
 │ • Rate Limiting & Token Quota     • Dynamic Model Router & Fallback    │
 │ • AI Guardrails & PII Masking     • Semantic Caching                   │
 │ ──> CONTINUOUS EVALUATION HARNESS & GOLDEN DATASET BENCHMARK <──       │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ (Vector & SQL Data Flow)
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 1: TẦNG DỮ LIỆU MESH & MLOPS NỀN TẢNG (DATA MESH & MLOPS PLATFORM│
 │ • Domain Data Products (Gán rõ Domain Owner & SLA Hợp đồng Dữ liệu)    │
 │ • Automated DataOps Pipeline (Làm sạch & Dán nhãn tự động)             │
 │ • Enterprise Feature Store & Vector Database (Thời gian thực)          │
 │ • Model Observability & Automated Drift Retraining Loop                │
 └────────────────────────────────────────────────────────────────────────┘
```

#### Tầng 1: Dữ liệu Mesh & Nền tảng MLOps Tự động hóa (Data Mesh & MLOps Platform)
* **Chuyển đổi sang Data Mesh:** Chia nhỏ kho dữ liệu nguyên khối thành các **Domain Data Products** độc lập. Khối Bán lẻ sở hữu *Retail Data Product*, Khối Tín dụng sở hữu *Credit Data Product*. Mỗi sản phẩm dữ liệu có schema chuẩn, versioning và SLA cam kết.
* **Hạ tầng Automated DataOps:** Triển khai các công cụ dán nhãn dữ liệu có AI hỗ trợ (AI-assisted Labeling) và pipeline tiền xử lý dữ liệu tự động, loại bỏ hoàn toàn việc can thiệp thủ công.
* **Enterprise Feature Store & Vector DB:** Xây dựng kho lưu trữ đặc trưng tập trung (Feature Store) cho các bài toán phân tích thời gian thực (Scoring, Fraud) và Vector Database (như Milvus/Qdrant/pgvector) chuyên dụng cho RAG.
* **Hệ thống Giám sát Độ trôi (Model Drift Observability):** Theo dõi liên tục phân phối dữ liệu đầu vào và đầu ra. Khi phát hiện độ trễ hoặc độ trôi vượt ngưỡng, hệ thống tự động kích hoạt pipeline huấn luyện lại mô hình (Automated Retraining Loop).

#### Tầng 2: Cổng Điều phối AI & Bảo mật Dùng chung (Enterprise LLM Gateway & Guardrails)
* **Cổng điều phối LLM Gateway:** Điểm tiếp nhận duy nhất cho toàn bộ yêu cầu gọi LLM trong ngân hàng (hỗ trợ OpenAI, Gemini, Claude, Llama 3, DeepSeek...):
  * *Hạn ngạch & Chi phí:* Gán quota token chi tiết cho từng phòng ban; tự động ngắt khi vượt ngân sách.
  * *Chuyển mạch thông minh (Dynamic Model Routing):* Tự động chuyển hướng sang mô hình dự phòng khi nhà cung cấp chính gặp sự cố (High Availability).
  * *Bộ đệm ngữ nghĩa (Semantic Cache):* Tái sử dụng câu trả lời cho các câu hỏi trùng lặp, giảm 30–50% chi phí gọi API.
* **Tường lửa AI (AI Guardrails Layer):**
  * Tự động quét và che giấu (Redact/Mask) thông tin cá nhân (PII) theo Luật Bảo vệ Dữ liệu Cá nhân trước khi gửi ra ngoài.
  * Phát hiện và ngăn chặn các cuộc tấn công Prompt Injection, Jailbreak hoặc rò rỉ dữ liệu nhạy cảm của hệ thống ngân hàng.
* **Continuous Evaluation Harness:** Hệ thống kiểm thử tự động dựa trên **Golden Dataset**. Bất kỳ bản cập nhật mô hình hoặc thay đổi prompt nào cũng phải vượt qua bộ test suite này trước khi được deploy lên production.

#### Tầng 3: Tầng Điều phối Tác tử & Ngữ cảnh Bền vững (Agentic Runtime & Context)
* **Bộ nhớ Ngữ cảnh Đa tầng (Stateful Context Management):** Lưu trữ lịch sử phiên hội thoại có cấu trúc, cho phép các giải pháp như AI Enterprise giải quyết các câu hỏi phức tạp xuyên suốt nhiều bước hội thoại.
* **Công cụ Điều phối Tác tử Đa nhiệm (Multi-Agent Orchestrator):** Cho phép các Agent chuyên biệt (Market Research Agent, Copywriting Agent, Risk Checking Agent) phối hợp nhịp nhàng theo quy trình nghiệp vụ định sẵn.
* **Thư viện Gợi ý Tập trung (Enterprise Prompt Catalog):** Quản lý toàn bộ prompt như mã nguồn (Prompt-as-Code) với quy trình code review, kiểm duyệt bảo mật và đánh giá phiên bản chặt chẽ.

#### Tầng 4: Kênh Tương tác Số & Điều phối Human-in-the-Loop (Channels & HITL Delivery)
* **Tích hợp Kênh Liền mạch:** Cung cấp giao diện trực quan cho quan hệ khách hàng (RM Co-pilot), người dùng số (App, Biz) và cán bộ vận hành.
* **Bộ điều phối Tự tin HITL (HITL Confidence Router):**
  * Mỗi trường thông tin do AI sinh ra (ví dụ: Doanh thu, Lợi nhuận gộp, Nợ ngân hàng khác trong Credit Memo) đều có gắn **Điểm tin cậy (Confidence Score từ 0.0 đến 1.0)**.
  * Các trường đạt điểm cao (>0.9) được tự động chấp thuận. Các trường có điểm nghi ngờ (<0.9) sẽ được đánh dấu nổi bật màu vàng/đỏ và tự động chuyển đến hàng đợi của chuyên viên tín dụng để xác minh nhanh bằng 1 click.
* **Vòng đo lường PBT Khép kín:** Ghi nhận chính xác số giờ làm việc thực tế được cắt giảm trên từng hồ sơ để quy đổi trực tiếp thành giá trị tài chính PBT, khép lại vòng lặp phản hồi cho ban lãnh đạo.

---

## 4. Thiết lập Khung Quản trị Kiến trúc: Cổng "Approval to Build" (Architectural Gate)

Để chấm dứt tình trạng triển khai các use case tự phát, manh mún và tiềm ẩn rủi ro, Khối Kiến trúc Doanh nghiệp (Enterprise Architecture) cần đưa vào vận hành **Cổng Kiểm soát Kiến trúc Bắt buộc ("Approval to Build")**:

```
 [ ĐỀ XUẤT USE CASE ]
        │
        ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                   CỔNG KIỂM SOÁT "APPROVAL TO BUILD"                   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 1. Sẵn sàng Dữ liệu (Data Readiness Check)                             │
 │    • Đã có Data Product chuẩn hóa và Data Domain Owner bảo trợ?        │
 │    • Đã xây dựng Golden Dataset gồm tối thiểu 100+ hồ sơ chuẩn?        │
 │                                                                        │
 │ 2. Đánh giá Kiến trúc & NFR (Architecture & NFR Review)                │
 │    • Tích hợp qua LLM Gateway chuẩn? Có cơ chế Fallback?               │
 │    • Đáp ứng chỉ tiêu độ trễ (Latency SLA) và ngân sách Token?         │
 │                                                                        │
 │ 3. An ninh & Tuân thủ (Security, Privacy & Compliance Gate)            │
 │    • Đã cấu hình bộ lọc AI Guardrails và che giấu PII?                 │
 │    • Có cơ chế kiểm soát mã nguồn và trách nhiệm giải trình (AI for IT)?│
 │                                                                        │
 │ 4. Cam kết Nghiệp vụ & PBT (Business Sponsorship & PBT Case)           │
 │    • Lãnh đạo nghiệp vụ đứng tên PO? Có kế hoạch HITL chi tiết?        │
 │    • Có công thức đo lường PBT cụ thể được Khối Tài chính phê duyệt?   │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
              [ ĐẠT TIÊU CHUẨN ]             [ KHÔNG ĐẠT ]
                    │                                 │
                    ▼                                 ▼
             Cấp phát Hạ tầng,                Từ chối Triển khai,
           Thành lập AI Squad &              Yêu cầu Chuẩn hóa lại
             Bắt đầu Lập trình                Dữ liệu & Nghiệp vụ
```

---

## 5. Lộ trình Triển khai Kiến trúc 4 Giai đoạn (Technical Roadmap)

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │ GIAI ĐOẠN 1 (0 – 3 THÁNG): QUẢN TRỊ NỀN MÓNG & BẢO VỆ AN TOÀN (SHIELD) │
 ├────────────────────────────────────────────────────────────────────────┤
 │ • Triển khai Enterprise LLM Gateway tập trung (OpenAI, Gemini, Local)  │
 │ • Thiết lập AI Guardrails, PII Redaction và Token Quota toàn ngân hàng │
 │ • Ban hành Khung Quản trị AI for IT (Quét bản quyền, SAST/DAST cho AI) │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ GIAI ĐOẠN 2 (3 – 6 THÁNG): CHUẨN HÓA MLOPS & CƠ CHẾ HITL (STABILIZE)   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ • Xây dựng Golden Dataset Benchmark cho các bài toán trọng điểm        │
 │ • Tích hợp Continuous Evaluation Harness vào CI/CD pipeline            │
 │ • Triển khai HITL Confidence Router cho luồng Credit Memo & Lending    │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ GIAI ĐOẠN 3 (6 – 12 THÁNG): CHUYỂN DỊCH DATA MESH & GIÁM SÁT (SCALE)   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ • Chuyển đổi dữ liệu sang mô hình Data Mesh với Domain Data Products   │
 │ • Triển khai Enterprise Feature Store phục vụ bài toán Realtime Scoring│
 │ • Thiết lập hệ thống Model Observability giám sát Drift toàn diện      │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ GIAI ĐOẠN 4 (12+ THÁNG): ĐIỀU PHỐI TÁC TỬ TỰ CHỦ (AUTONOMOUS BANKING)  │
 ├────────────────────────────────────────────────────────────────────────┤
 │ • Vận hành Multi-Agent Orchestration cho các hành trình khách hàng E2E │
 │ • Tự động hóa vòng lặp Closed-Loop Retraining từ phản hồi người dùng   │
 │ • Khép vòng đo lường PBT thời gian thực trên toàn bộ 14 Banking Domains│
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Kết luận & Khuyến nghị Dành cho Lãnh đạo Công nghệ

1. **Ngừng ngay việc phát triển các Use Case manh mún dạng PoC tự phát:** Mọi dự án mới phải đi qua Cổng kiểm soát *Approval to Build* và cam kết chỉ tiêu PBT rõ ràng.
2. **Ưu tiên đầu tư vào Lớp Hạ tầng Tái sử dụng (LLM Gateway, Guardrails, MLOps Platform) trước khi mở rộng ứng dụng:** Đây là nền móng bảo vệ ngân hàng khỏi rủi ro bảo mật, tối ưu hóa hàng triệu USD chi phí bản quyền mô hình và đảm bảo tính sẵn sàng cao.
3. **Giải quyết triệt để vấn đề "Data Dirt":** Muốn có AI thông minh, trước hết dữ liệu phải sạch. Việc chuyển dịch sang kiến trúc **Data Mesh** và gán trách nhiệm sở hữu cho từng Domain nghiệp vụ là điều kiện tiên quyết mang tính sống còn.
4. **Chuẩn hóa luồng phối hợp Người – Máy (Human-in-the-Loop):** AI trong ngân hàng không sinh ra để thay thế hoàn toàn con người mà để trao quyền (Augment). Kiến trúc phải tập trung vào việc tính toán độ tin cậy để giải phóng chuyên viên khỏi 80% công việc thủ công, chỉ giữ lại 20% các quyết định rủi ro then chốt cho con người phê duyệt.
