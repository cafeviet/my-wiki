# Giải pháp Chuyên sâu cho Năm Điểm mù Kỹ thuật

**Khắc phục các lỗ hổng thực thi trong quản trị tác nhân AI doanh nghiệp ngân hàng**

**Chuyên đề kỹ thuật:** Bổ trợ cho [Báo cáo Nghiên cứu Quản trị Agent Doanh nghiệp Ngân hàng](./) · **Phiên bản:** 1.2 · **Ngày cập nhật:** 30/09/2026

> **Tuyên ngôn Thiết kế:**  
> *"Không có công nghệ bảo mật nào tự động mang lại an toàn nếu thiếu ranh giới tin cậy độc lập. Mọi giải pháp kỹ thuật (từ Token Exchange, MCP Gateway đến Distributed Saga) phải được đặt trong kỷ luật Zero Trust và chịu sự phán quyết cuối cùng của Hệ thống Nghiệp vụ Nguồn (System of Record)."*

---

## 1. Tổng quan Năm Điểm mù Kỹ thuật Thực tế

Trong quá trình chuyển đổi từ các thử nghiệm AI đơn lẻ sang triển khai Agent diện rộng tại ngân hàng, các nhóm kỹ thuật thường vấp phải **năm khoảng trống thực thi (Execution Blindspots)**. Đây là những điểm mù kỹ thuật mà các framework mã nguồn mở hoặc sản phẩm thương mại thường che giấu hoặc mô tả đơn giản hóa:

```
┌────────────────────────────────────────────────────────────────────────┐
│             NĂM ĐIỂM MÙ KỸ THUẬT VÀ GIẢI PHÁP KIẾN TRÚC THỰC THI       │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Khoảng trống IAM & Ủy quyền    │ OAuth 2.0 Token Exchange (RFC8693) │
│    (The Identity Delegation Gap)  │ & Workload Identity (SPIFFE)       │
├───────────────────────────────────┼────────────────────────────────────┤
│ 2. Toàn vẹn Giao dịch Phân tán    │ Operation ID, Khóa Chống lặp bền   │
│    (Distributed Transaction Gap)  │ & Compensating Saga có chọn lọc    │
├───────────────────────────────────┼────────────────────────────────────┤
│ 3. Quản trị Giao thức MCP         │ Managed MCP Gateway có Schema &    │
│    (Unmanaged Tool Protocols)     │ Ranh giới mạng/dữ liệu độc lập     │
├───────────────────────────────────┼────────────────────────────────────┤
│ 4. Kiểm thử Hồi quy Bất định      │ CI/CD Evals Pipeline, Golden Test  │
│    (Stochastic Regression in CI)  │ Suites & Ngưỡng chấp nhận rủi ro   │
├───────────────────────────────────┼────────────────────────────────────┤
│ 5. Bất lực của Phân quyền tĩnh    │ ABAC/ReBAC thời gian thực          │
│    (Static RBAC Inadequacy)       │ phối hợp với PDP tập trung         │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 2. Điểm mù 1: Khắc phục Khoảng trống Định danh & Ủy quyền (The IAM Gap)

### 2.1. Thực trạng Kỹ thuật
Phần lớn hệ thống Core Banking, LOS, Payment Hub hiện nay được thiết kế để phục vụ hai mô hình truy cập truyền thống:
1. **Người dùng tương tác trực tiếp:** Xác thực qua Web/App session, token mang danh tính cá nhân (`user_id`).
2. **Hệ thống tích hợp (System-to-System):** Sử dụng chung một tài khoản dịch vụ tĩnh (Static Service Account) hoặc API Key dùng chung lưu trong cấu hình.

Khi Agent tham gia vào hành trình, nếu sử dụng tài khoản dịch vụ backend để gọi API thay mặt người dùng, ngân hàng sẽ đối mặt với **Rủi ro Mất dấu vết chủ thể (Loss of Principal Identity)** và **Rủi ro Leo thang Đặc quyền (Privilege Escalation)**: Agent mang quyền hạn của một Service Account toàn năng để thao tác trên tài khoản khách hàng, hệ thống đích không thể xác định khách hàng thực tế là ai.

### 2.2. Giải pháp Kiến trúc Phân tầng

```text
[Người dùng cuối]                    [Authorization Server]                 [Core Banking / LOS]
       │                                       │                                     │
       │ 1. Access Token ban đầu               │                                     │
       ├──────────────────────────────────────►│                                     │
       │                                       │ 2. Token Exchange (RFC 8693)        │
       │                                       │    sub: user_123                    │
       │                                       │    act: { sub: agent_retail_v1 }    │
       │                                       │    aud: core-banking-api            │
       │                                       │    scope: transfer:prepare          │
       │                                       ├────────────────────────────────────►│
       │                                       │                                     │ 3. Core kiểm tra:
       │                                       │                                     │    • Token còn hạn?
       │                                       │                                     │    • user_123 sở hữu TK?
       │                                       │                                     │    • agent được gọi tool?
```

1. **Tác vụ Đại diện Người dùng (Delegated Tasks):**
   * Áp dụng **OAuth 2.0 Token Exchange (RFC 8693)**: Authorization Server phát hành downstream token ngắn hạn với cấu trúc actor claim:
     ```json
     {
       "sub": "user_hoang_nv88",
       "act": {
         "sub": "agent_credit_assistant_v1"
       },
       "aud": "credit-api",
       "scope": "credit:read credit_draft:create",
       "exp": 1759142400
     }
     ```
   * **Ranh giới an ninh quan trọng:** Cấu trúc token trên chỉ biểu đạt chủ thể (`sub`) và tác nhân thực thi (`act.sub`), **hoàn toàn không phải là bằng chứng phê duyệt giao dịch**. Hệ thống nghiệp vụ nguồn (Core/LOS) bắt buộc phải kiểm tra quyền sở hữu tài nguyên tại thời điểm gọi và đối chiếu phê duyệt nghiệp vụ trước khi commit.
2. **Tác vụ Tự chủ Theo lịch / Sự kiện (Autonomous Service Tasks):**
   * Với các Agent chạy ngầm không có người dùng trực tiếp (Batch processing, rà soát giao dịch gian lận ban đêm), tuyệt đối không gán giả lập một `sub` người dùng.
   * Áp dụng **Workload Identity (SPIFFE/SPIRE)**: Cấp phát chứng chỉ mật mã X.509 SVID ngắn hạn (thời gian sống dưới 1 giờ), tự động xoay vòng. Workload Identity chỉ xác thực danh tính tiến trình, thẩm quyền nghiệp vụ phải do chính sách IAM dịch vụ cấp riêng cho phạm vi hẹp.

---

## 3. Điểm mù 2: Toàn vẹn Giao dịch & Mẫu hình Bù trừ (Distributed Saga & Idempotency)

### 3.1. Thực trạng Kỹ thuật
Vòng lặp ReAct của Agent mang tính chất suy luận thăm dò. Khi Agent thực thi chuỗi công cụ gồm nhiều bước:
**Bước 1: Khóa tài sản** → **Bước 2: Tạo hạn mức** → **Bước 3: Gửi thông báo phê duyệt**
Nếu xảy ra mất mạng tại Bước 3 hoặc Agent gặp lỗi crash bộ nhớ, trạng thái giao dịch rơi vào tình trạng phân mảnh (Tài sản khách hàng bị phong tỏa nhưng hạn mức không được kích hoạt).

### 3.2. Giải pháp Kiến trúc Phân tầng

```text
               CƠ CHẾ XỬ LÝ GIAO DỊCH GHI CỦA AGENT
   ┌────────────────────────────────────────────────────────┐
   │ Tool Call (Write Action)                               │
   │ Kèm Operation ID ổn định qua các lần Retry/Resume       │
   └───────────────────────────┬────────────────────────────┘
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │ Hệ thống Đích (Core / LOS): Lưu bền kết quả & Payload  │
   ├───────────────────────────┬────────────────────────────┤
   │ Thành công (Committed)    │ Timeout / Chưa rõ kết quả  │
   │ Trả mã giao dịch Tx_ID    │ Đánh dấu PENDING_RECONCILE │
   └───────────────────────────┴─────────────┬──────────────┘
                                             ▼
                               ┌────────────────────────────┐
                               │ Tra cứu trạng thái nguồn   │
                               │ trước khi cho phép Retry   │
                               └────────────────────────────┘
```

1. **Khóa Chống lặp Bền vững (Persistent Idempotency Key):**
   * Sử dụng `Operation_ID` ổn định xuyên suốt chu kỳ sống của tác vụ, được sinh ra từ:
     `Operation_ID = Hash(Session_ID + Task_ID + Step_Index + Payload_Hash)`
   * **Hệ thống đích bắt buộc phải lưu bền (persist) khóa này:** Khi nhận lại cùng một `Operation_ID`, hệ thống trả về kết quả đã ghi nhận thay vì thực thi thêm. Tuyệt đối từ chối nếu gặp lại khóa cũ nhưng payload đã bị thay đổi.
   * **Xử lý Timeout an toàn:** Khi gặp timeout sau lệnh ghi, trạng thái được chuyển thành `PENDING_RECONCILIATION`. Agent **bắt buộc phải gọi công cụ tra cứu trạng thái giao dịch** trước khi quyết định thử lại; cấm tự sinh khóa mới để lách trạng thái chưa rõ.
2. **Saga Bù trừ Có Điều kiện (Compensating Actions with Business Reality):**
   * **Không ảo tưởng về khả năng hoàn nguyên tự động:** Một lệnh chuyển tiền liên ngân hàng đã ra khỏi cổng thanh toán quốc gia thì không thể "rollback" bằng một API bù trừ đơn giản.
   * Chỉ áp dụng Saga cho các bước kỹ thuật có khả năng bù trừ nghiệp vụ hợp lệ:
     * `lockCollateral()` ↔ `unlockCollateral()` (Hợp lệ).
     * `prepareDraft()` ↔ `discardDraft()` (Hợp lệ).
   * Với các bước tài chính không thể hoàn nguyên tức thì: Khi xảy ra sự cố chuỗi, hệ thống chuyển giao dịch sang trạng thái ngoại lệ cần xử lý thủ công (Escalate to Human Operations) và kích hoạt quy trình bồi hoàn (Dispute/Reconciliation Workflow).

---

## 4. Điểm mù 3: Quản trị Giao thức Công cụ Tập trung (Managed MCP Gateway)

### 4.1. Thực trạng Kỹ thuật
**Model Context Protocol (MCP)** do Anthropic khởi xướng đang nhanh chóng trở thành tiêu chuẩn mở kết nối Agent với các công cụ và dữ liệu. Tuy nhiên, MCP nguyên bản chỉ là một giao thức ở tầng ứng dụng/giao tiếp (client-to-server qua stdio hoặc HTTP/SSE). MCP **hoàn toàn không có mô hình bảo mật doanh nghiệp tích hợp sẵn**: không có cơ chế phân quyền chi tiết, không có xác thực mTLS và không bảo đảm an toàn dữ liệu nội bộ.

### 4.2. Giải pháp Kiến trúc Phân tầng

```text
[Runtime Sandbox: Agent]
       │
       │ Lệnh gọi MCP Tool qua mạng nội bộ
       ▼
┌────────────────────────────────────────────────────────┐
│ MANAGED TOOL / MCP GATEWAY (PEP ĐỘC LẬP)                │
├────────────────────────────────────────────────────────┤
│ 1. Schema Enforcement: Kiểm tra cú pháp JSON nghiêm ngặt│
│ 2. Semantic Parameter Check: Kiểm tra hạn mức, số tiền │
│ 3. Authorization Lookup: Hỏi PDP về quyền của User/Agent│
│ 4. Anti-Injection Sanitization: Lọc bỏ payload nguy hiểm│
└───────────────────────────┬────────────────────────────┘
                            │ Forward API Call
                            ▼
[Core Banking / LOS APIs / Database Internal]
```

1. **Ranh giới Mạng và Rào chắn Độc lập:**
   * Không cho phép Agent kết nối trực tiếp tới MCP Server nội bộ không qua kiểm duyệt.
   * Toàn bộ MCP Server phục vụ nghiệp vụ ngân hàng phải chạy sau **Managed Tool / MCP Gateway**.
   * Kết nối giữa Gateway và MCP Servers bắt buộc mã hóa qua **mTLS** kèm chứng chỉ Workload Identity.
2. **Ba Lớp Kiểm soát Tham số Công cụ:**
   * *Lớp 1 (Strict Schema Validation):* Bắt buộc kiểm tra tham số đầu vào khớp 100% với JSON Schema đã được phê duyệt trong danh mục công cụ; từ chối mọi trường lạ (Unknown fields).
   * *Lớp 2 (Semantic & Resource Limits):* Kiểm tra ngữ nghĩa nghiệp vụ: số tiền chuyển không vượt hạn mức ngày, tài khoản thụ hưởng phải nằm trong danh mục cho phép.
   * *Lớp 3 (Anti-Injection & Sanitization):* Loại bỏ các chuỗi ký tự điều khiển có thể gây SQL Injection, Command Injection hoặc Prompt Leakage trước khi lệnh được chuyển tiếp tới API ngân hàng.

---

## 5. Điểm mù 4: Kiểm thử Hồi quy Hành vi Bất định trong CI/CD (Agent Evals Pipeline)

### 5.1. Thực trạng Kỹ thuật
Khác với phần mềm truyền thống có tính tiền định (cùng input luôn ra cùng output), Agentic AI dựa trên mô hình xác suất. Một thay đổi nhỏ trong system prompt, một phiên bản cập nhật trọng số từ nhà cung cấp mô hình (Model Drift), hoặc dữ liệu ngữ cảnh thay đổi đều có thể làm đứt gãy chuỗi suy luận đang vận hành ổn định. Các bài kiểm thử Unit Test/Integration Test truyền thống hoàn toàn bất lực trước hành vi bất định này.

### 5.2. Giải pháp Kiến trúc Phân tầng

```text
                       QUY TRÌNH CI/CD AGENT EVALUATION
 ┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
 │ Code / Prompt / Tool      │ ──► │ Deterministic Tests       │ ──► │ Golden Evals Pipeline     │
 │ Commit vào Git Repository │     │ (Unit tests, Schema validation│ │ (Chạy 500-1000 ca mẫu     │
 └───────────────────────────┘     │  Policy syntax check)     │     │  kiểm tra hành vi model)  │
                                   └───────────────────────────┘     └─────────────┬─────────────┘
                                                                                   ▼
 ┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
 │ Production Release        │ ◄── │ Phê duyệt Nghiệp vụ       │ ◄── │ Đánh giá Bộ Chỉ số Cứng   │
 │ (Canary Deployment 5-10%) │     │ (Business Owner sign-off) │     │ (Tỷ lệ lọt vi phạm,       │
 └───────────────────────────┘     └───────────────────────────┘     │  Tool precision, FinOps)  │
                                                                     └───────────────────────────┘
```

1. **Phân tách Hai Lớp Kiểm thử trong Pipeline:**
   * *Lớp Kiểm thử Tiền định (Deterministic Gates):* Kiểm thử unit test cho logic công cụ, kiểm thử cú pháp JSON schema, kiểm tra tính hợp lệ của chính sách OPA/Cedar và kiểm tra máy trạng thái (State machine).
   * *Lớp Đánh giá Hành vi Mô hình (Golden Evals Gates):* Đưa Agent chạy qua bộ dữ liệu chuẩn gồm hàng trăm kịch bản đại diện thực tế trong quá khứ (Golden Dataset).
2. **Thiết lập Bộ Chỉ số Đo lường theo Cấp độ Rủi ro:**
   * Không áp dụng các con số phần trăm lý thuyết chung chung. Ngưỡng chấp nhận phải do **Chủ sở hữu nghiệp vụ và Ban Quản lý Rủi ro phê duyệt** dựa trên mức tổn thất tối đa có thể chấp nhận:
     * *Tỷ lệ vi phạm chính sách lọt qua kiểm soát (Safety Violation Rate):* Phải bằng 0% đối với các kịch bản liên quan đến tiền và dữ liệu bí mật.
     * *Độ chính xác gọi công cụ (Tool-calling Precision):* Đạt ngưỡng thỏa thuận SLA (ví dụ: ≥ 98%).
     * *Tỷ lệ chặn nhầm (False Positive Rate):* Không vượt quá ngưỡng ảnh hưởng trải nghiệm khách hàng (ví dụ: ≤ 1%).
     * *Độ biến động chi phí token (FinOps Cost Variance):* Cảnh báo nếu chi phí trung bình trên mỗi ca hoàn thành vượt quá 15% so với baseline.
3. **Triển khai Canary và Giám sát Độ trôi Hành vi:**
   * Khi đổi mô hình hoặc cập nhật prompt lớn, bắt buộc triển khai dạng **Canary (5–10% lưu lượng)** và so sánh kết quả song song (Shadow/A-B Testing) trước khi thay thế hoàn toàn phiên bản cũ.

---

## 6. Điểm mù 5: Dịch chuyển sang Phân quyền Thuộc tính Thời gian thực (ABAC/ReBAC)

### 6.1. Thực trạng Kỹ thuật
Mô hình phân quyền theo vai trò (Role-Based Access Control - RBAC) truyền thống gán quyền tĩnh cho người dùng hoặc tài khoản dịch vụ (Ví dụ: `Role: Credit_Officer` → có quyền `Approve_Loan`). 

Trong môi trường Agentic AI, RBAC bộc lộ lỗ hổng chí mạng:
* Một nhân viên tín dụng có quyền duyệt vay, nhưng **Agent của nhân viên đó không thể tự ý kích hoạt quyền duyệt vào lúc nửa đêm, từ một địa chỉ IP lạ, hoặc khi điểm tin cậy của phiên làm việc đang ở mức thấp**.
* RBAC không thể đánh giá được ngữ cảnh động của phiên tương tác giữa người dùng và tác nhân AI.

### 6.2. Giải pháp Kiến trúc Phân tầng

```text
                  MÔ HÌNH PHÂN QUYỀN ĐỘNG ABAC CHO AGENT
┌────────────────────────────────────────────────────────────────────────┐
│ YÊU CẦU THỰC THI CÔNG CỤ (Tool Call Request)                           │
│ Mang thông tin: User_ID, Agent_ID, Action, Resource, Context           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ BỘ QUYẾT ĐỊNH CHÍNH SÁCH TẬP TRUNG (PDP - Policy Decision Point)       │
├────────────────────────────────────────────────────────────────────────┤
│ Đánh giá hàm quyết định đa chiều:                                      │
│ Quyết định = f(Subject, Action, Resource, Context)                     │
│                                                                        │
│ • Subject:  User có thẩm quyền + Agent có chứng chỉ hợp lệ            │
│ • Action:   Lệnh duyệt vay (approve_loan)                              │
│ • Resource: Khoản vay cụ thể, giá trị nằm trong hạn mức phân công      │
│ • Context:  Thời gian trong giờ hành chính, IP mạng nội bộ,           │
│             Phiên đã có xác nhận sinh trắc học, Rủi ro phiên thấp      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ├── Cho phép (Permit) ──► Chuyển lệnh tới SoR
                                    └── Từ chối (Deny)   ──► Chặn & Cảnh báo SIEM
```

1. **Kiến trúc ABAC/ReBAC với Open Policy Agent (OPA) hoặc Cedar:**
   * Tách rời hoàn toàn mã nguồn nghiệp vụ khỏi logic phân quyền. Chính sách bảo mật được viết dưới dạng mã khai báo (Policy-as-Code) và được phiên bản hóa trong Git.
2. **Bốn Chiều Thuộc tính Đánh giá Động:**
   `Quyết định Truy cập = f(Subject, Action, Resource, Context)`
   * **Subject (Chủ thể):** Gồm định danh kép của Người dùng ủy nhiệm (`user_id`, chức vụ, chi nhánh) + Định danh tác nhân (`agent_id`, phiên bản, chứng chỉ workload).
   * **Action (Hành động):** Lệnh gọi công cụ cụ thể (`read_customer_data`, `approve_loan_limit`, `initiate_transfer`).
   * **Resource (Tài nguyên):** Đối tượng đích cụ thể (Mã hồ sơ vay `LOS_9921`, số tiền vay `500.000.000 VND`, phân hạng khách hàng).
   * **Context (Ngữ cảnh thời gian thực):** Thời gian thực hiện, vị trí mạng, trạng thái xác thực 2 lớp (MFA), điểm đánh giá rủi ro phiên (Session Risk Score), và trạng thái vòng đời của tác vụ.
3. **Nguyên tắc Phủ quyết Tuyệt đối (Strict Deny Precedence):**
   * Nếu bất kỳ điều kiện thuộc tính nào không thỏa mãn (ví dụ: tác vụ thực hiện ngoài khung giờ quy định hoặc thiếu chữ ký xác nhận payload), PDP lập tức trả về `DENY`. Hệ thống đích tuyệt đối không mở đường vòng.

---

## 7. Kết luận Kỹ thuật

Năm giải pháp chuyên sâu trên tạo thành **Vành đai Kiểm soát Tương tác (Controlled Interaction Perimeter)** bao bọc quanh tác nhân AI. Việc hiện thực hóa các giải pháp này bảo đảm rằng ngân hàng có thể tận dụng tối đa năng lực suy luận linh hoạt của AI mà không bao giờ đánh đổi tính toàn vẹn, an toàn thông tin và trách nhiệm giải trình của các hệ thống cốt lõi.

*Lưu ý kiến trúc chiến lược:* Bên cạnh năm điểm mù kỹ thuật tầng thực thi trên, rủi ro mang tính sống còn là **Nợ nhận thức (Cognitive Debt)** — sự xói mòn tri thức và khả năng làm chủ hệ thống của con người khi Agent sinh mã — được quản trị tập trung ở cấp Enterprise Architecture thông qua nền tảng **MB Landscape (MBL)** (Xem chi tiết tại [Mục 8.2 của Báo cáo Tổng quan](./index.md#82-diem-mu-kien-truc-chien-luoc-no-nhan-thuc-cognitive-debt-va-su-menh-he-thong-mb-landscape-mbl)).
