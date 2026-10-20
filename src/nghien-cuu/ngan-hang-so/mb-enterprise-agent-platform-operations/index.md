# Enterprise Agent Platform 

> **Nguồn tài liệu nghiên cứu & khảo sát:**
> 1. *Định hướng kiến trúc và các việc ưu tiên triển khai Enterprise Agent Platform tại MB* (Tài liệu Kiến trúc Doanh nghiệp, 07/2026).
> 2. *Báo cáo Giải pháp Agentic AI Khối Vận hành: Tăng tốc – Vững chắc – Hiệu quả* (Báo cáo Trình Tổng Giám đốc & Khối Tín dụng, 2026).  
>
> **Đơn vị nghiên cứu:** MBBank (MB).  
> **Nguyên tắc nền tảng xuyên suốt:** *"Tập trung hóa lớp kiểm soát và năng lực dùng chung, không tập trung hóa cứng lớp phát triển và thực thi Agent."*  
> **Bộ ba nguyên tắc vận hành:** *"AI thực hiện công việc lặp lại (Repetitive Work) — Hệ thống Luật đưa ra quyết định cứng (Deterministic Rules) — Con người chịu trách nhiệm phê duyệt cuối cùng (Human Accountability)."*

---

## 1. Tóm tắt điều hành (Executive Summary)

Giai đoạn 2023–2025 ghi nhận sự bùng nổ của Generative AI với trọng tâm là các trợ lý ảo hỏi – đáp (Chatbot, Q&A), tra cứu văn bản và hỗ trợ soạn thảo nội dung. Tuy nhiên, bước sang năm 2026, làn sóng công nghệ đang chứng kiến sự chuyển dịch mang tính bước ngoặt sang **AI Agent (Tác tử Trí tuệ Nhân tạo)** — các hệ thống phần mềm có khả năng tiếp nhận mục tiêu, phân tích ngữ cảnh, tự chủ sử dụng công cụ (Tool Use), gọi API, truy cập dữ liệu và thực hiện chuỗi hành động nghiệp vụ thay cho con người.

Theo dự báo của Gartner:
* Tỷ lệ các ứng dụng doanh nghiệp tích hợp AI Agent chuyên biệt sẽ tăng vọt từ **dưới 5% (năm 2025) lên khoảng 40% vào cuối năm 2026**.
* Đi kèm với xu hướng này là lời cảnh báo nghiêm khắc về nguy cơ **"Ungoverned AI Agent Sprawl"** (Sự bùng nổ tác tử AI ngoài tầm kiểm soát) diễn ra trên 4 lớp: *Công nghệ*, *Tích hợp*, *Vận hành* và *Quản trị*.

Tại MB, nhu cầu ứng dụng AI Agent đang hình thành rõ nét theo hai gọng kìm:
1. **Các sáng kiến chính thức từ tổ chức:** Bao gồm `AI Enterprise` (khai thác tri thức nội bộ), `AI Customer / Mr. But` (tư vấn tài chính cá nhân), `AI Lending` (tối ưu quy trình cấp tín dụng), `AI Fraud Detection` (phát hiện gian lận thanh toán) và `AI for Coding` (nâng cao năng suất lập trình).
2. **Nhu cầu tự phát từ người dùng và nhóm kỹ thuật:** Sự xuất hiện của các công cụ Personal Agent chạy trên máy trạm cục bộ (như Hermes, OpenClaw, ZeroClaw...) để tự động hóa xử lý văn bản, lập trình và hỗ trợ công việc hàng ngày.

Nếu thiếu vắng một khung kiến trúc nền tảng và cơ chế kiểm soát tập trung, ngân hàng sẽ đối mặt với tình trạng phân mảnh nghiêm trọng: mỗi nhóm tự chọn mô hình (model), tự lưu trữ API key, tự kết nối hệ thống nghiệp vụ và tự vận hành. Điều này làm gia tăng rủi ro lộ lọt dữ liệu khách hàng, mất an toàn thông tin và không thể xác định trách nhiệm pháp lý khi Agent xảy ra sự cố.

Bài nghiên cứu này tổng hợp định hướng xây dựng **Enterprise Agent Platform** kết hợp với bài toán thực chiến tại **Khối Vận hành và Tín dụng**, đưa ra bản thiết kế kiến trúc toàn diện và lộ trình triển khai khả thi cho ngân hàng.

---

## 2. Bối cảnh Thực chiến: Điểm nghẽn Vận hành Thủ công và Bẫy STP tại MB

### 2.1. Thực trạng kiểm soát tuân thủ giao dịch vận hành thủ công

Khảo sát thực tế tại Khối Vận hành MB cho thấy áp lực kiểm soát thủ công đối với các giao dịch tín dụng doanh nghiệp đang ở mức báo động:

```
          ÁP LỰC KIỂM SOÁT THỦ CÔNG TẠI KHỐI VẬN HÀNH MB
 ┌──────────────────────────────────┬──────────────────────────────────┐
 │    GIẢI NGÂN KHÁCH HÀNG DOANH NGHIỆP│        PHÁT HÀNH BẢO LÃNH        │
 ├──────────────────────────────────┼──────────────────────────────────┤
 │• 19 SP Vốn lưu động ngành        │• 96 điều kiện kiểm tra tổng thể  │
 │• 5 SP Tín dụng trung dài hạn     │• Bình quân: 70 điều kiện/PA      │
 │• 155 văn bản quy chuẩn cần check │  - 22 điều kiện hệ thống cấu hình│
 │• 155 điều kiện kiểm soát         │  - 74 điều kiện Nhóm 5 check TAY!│
 │• Bình quân: 106 điều kiện/PA     │• Hồ sơ trả đi trả về liên tục    │
 │  - 51 điều kiện hệ thống cấu hình│  giữa Vận hành, Tín dụng và RM  │
 │  - 104 điều kiện Nhóm 5 check TAY!│                                  │
 └──────────────────────────────────┴──────────────────────────────────┘
```

#### Phân rã chi tiết mức độ phức tạp:
* **Đối với nghiệp vụ Giải ngân Khách hàng Doanh nghiệp (KHDN):**
  * Áp dụng cho 19 sản phẩm Vốn lưu động (phân chia theo ngành) và 5 sản phẩm Tín dụng trung dài hạn.
  * Cán bộ vận hành phải đối chiếu với **155 văn bản pháp quy**: bao gồm 8 Quy chế, 59 Phụ lục, 26 Hướng dẫn, 6 Quy trình SUB, 25 Hướng dẫn chi tiết, 24 Quyết định sản phẩm và hơn 20 Chính sách kinh doanh (kèm các email/văn bản điều chỉnh lãi suất phát hành định kỳ 2–4 tuần/lần).
  * Tổng cộng có **155 điều kiện kiểm tra**, bình quân **106 điều kiện trên một phương án giải ngân**. Trong đó:
    * Chỉ có **51 điều kiện** (thuộc nhóm 1–4: Lãi suất, Hạn mức, Checklist, Tài sản bảo đảm) đã được cấu hình tự động trên hệ thống.
    * Còn lại **104 điều kiện thuộc Nhóm 5 bắt buộc phải kiểm tra thủ công bằng tay!** (Ví dụ: 24 điều kiện tài trợ đầu ra, 24 điều kiện tài trợ đầu vào/tạm ứng, 28 điều kiện tài trợ sản phẩm xây lắp, 20 điều kiện giải ngân ngoại tệ, 8 điều kiện không tài trợ...).
* **Đối với nghiệp vụ Phát hành Bảo lãnh:**
  * Tổng cộng 96 điều kiện; bình quân **70 điều kiện trên một phương án**.
  * Hệ thống chỉ mới cấu hình được **22 điều kiện**; còn lại **74 điều kiện thuộc Nhóm 5 phải kiểm tra thủ công** (10 điều kiện thời hạn bảo lãnh, 24 điều kiện bên nhận bảo lãnh/lựa chọn đầu ra, 13 điều kiện trường hợp liên danh/xí nghiệp, 8 điều kiện thỏa thuận hợp đồng, 19 điều kiện sản phẩm xây lắp...).
* **Điểm nghẽn Checklist hồ sơ:**
  * Hệ thống quản lý hiện tại chỉ phân loại và quy định upload tài liệu theo mã định danh (Code file), nhưng **hoàn toàn không có năng lực phát hiện tài liệu bị tải lên sai, mờ hoặc thiếu trang**.
  * Hậu quả: Cán bộ Vận hành (VH), Tín dụng (TD) và Quản lý quan hệ khách hàng (RM) phải mở từng file kiểm tra bằng mắt, dẫn đến tình trạng hồ sơ bị trả đi trả về nhiều lần, kéo dài thời gian xử lý và gây bức xúc cho khách hàng.

---

### 2.2. Bẫy tiếp cận STP (Straight-Through Processing) đơn lẻ

Để giải quyết bài toán trên, ngân hàng đã tìm cách đẩy mạnh tự động hóa luồng thẳng (STP). Tuy nhiên, kết quả thực tế cho thấy giải pháp STP truyền thống đang gặp rào cản lớn và rất khó mở rộng quy mô:

| Tiêu chí khảo sát | Nghiệp vụ Giải ngân Tín dụng | Nghiệp vụ Phát hành Bảo lãnh |
|---|---|---|
| **Mục tiêu STP thiết lập** | Tối đa **20%** phương án (của ~40% tệp khách hàng chuẩn mực) | Tối đa **10%** (Dựa trên 25% bảo lãnh bán hàng × 60% mẫu MB × 70% khả năng STP) |
| **Tiến độ triển khai thực tế** | Đang thí điểm trên tệp khách hàng chọn lọc:<br>• Phân khúc SME Upper: đạt **11%**<br>• Phân khúc Khách hàng lớn (CIB): chỉ đạt **5%** | Mới dừng lại ở giai đoạn khảo sát và đặt đầu bài kỹ thuật |
| **Nguyên nhân khó mở rộng** | • Mẫu biểu đưa vào luồng STP bị giới hạn nghiêm ngặt.<br>• Thời gian cấu hình cho một nhóm sản phẩm mới mất từ **2 đến 3 tháng**.<br>• Tỷ lệ chính xác của các mô hình AI nội bộ chưa đạt ngưỡng tin cậy. |

---

### 2.3. Kiểm toán Năng lực Thực tế của các Mô hình AI Tín dụng tại MB

Kiểm toán kỹ thuật chuyên sâu trên 3 giải pháp DocAI đang vận hành tại Khối Vận hành và Tín dụng làm lộ rõ khoảng cách lớn giữa "Độ chính xác theo trường" và "Độ chính xác toàn diện theo hồ sơ":

```
               ĐỘ CHÍNH XÁC AI NỘI BỘ THEO HỒ SƠ 100%
  ┌─────────────────────────────────────────────────────────────┐
  │ DocAI KHDN (Ủy nhiệm chi):        ██████ 30%                │
  │ DocAI Soạn thảo Văn kiện Tín dụng:████ 19%                  │
  │ DocAI Tài sản Bảo đảm:            █ 5% (Báo động!)          │
  └─────────────────────────────────────────────────────────────┘
   * Mặc dù độ chính xác tính trên từng trường riêng lẻ đạt 81% - 85%
```

#### Chi tiết 3 mảng nghiệp vụ:

1. **DocAI Khách hàng Doanh nghiệp (Ủy nhiệm chi - UNC):**
   * *Độ chính xác trung bình theo trường:* Đạt **85%** (Trường Tên khách hàng đạt 96%; nhưng trường Nội dung chuyển tiền chỉ đạt 60%, Bên thụ hưởng đạt 76%).
   * *Độ chính xác 100% theo hồ sơ:* Chỉ đạt vỏn vẹn **30%**.
   * *Thời gian xử lý OCR:* Bình quân **1 phút 25 giây** trên một chứng từ (trường hợp dài nhất lên tới 3 phút 38 giây).
   * *Lỗi kỹ thuật điển hình:* Mô hình nhận dạng sai khi gặp chuỗi số liên tục lặp lại (`9999`, `8888`) hoặc các cặp số có nét tương đồng (`8666`, `4747`, `0808`); tên bên nhận tiền thường bị thừa hoặc sai dấu tiếng Việt.

2. **DocAI Soạn thảo Tự động Văn kiện Tín dụng (VKTD):**
   * *Phạm vi:* Bóc tách hồ sơ pháp lý phục vụ soạn thảo hợp đồng thế chấp, phụ lục, kết quả đăng ký giao dịch bảo đảm cho Khách hàng Cá nhân (KHCN).
   * *Độ chính xác trung bình theo trường:* Đạt **81%** (Trường Địa chỉ hiện tại rơi xuống mức rất thấp: **13%**).
   * *Độ chính xác 100% theo hồ sơ:* Chỉ đạt **19%**.
   * *Lỗi kỹ thuật điển hình:* Khi gặp dữ liệu địa chỉ không đầy đủ, mô hình không tự phiên âm sang tiếng Việt có dấu (trong khi thử nghiệm trên Microsoft Copilot cho thấy Copilot xử lý thành công yêu cầu này).

3. **DocAI Tài sản Bảo đảm (TSBD):**
   * *Phạm vi:* Hoàn thiện hồ sơ tài sản bảo đảm là Bất động sản chính chủ không có nhà trên đất.
   * *Độ chính xác trung bình theo trường:* Đạt **81%**.
   * *Độ chính xác 100% theo hồ sơ:* Rơi xuống mức nghiêm trọng: **chỉ đạt 5%**!
   * *Điểm nghẽn vận hành:* Mới chỉ xử lý được 3 trong tổng số 5 loại tài liệu bắt buộc trong một bộ hồ sơ tài sản; mô hình đọc sót dữ liệu và không trích xuất theo đúng logic cấu trúc đề bài cung cấp.

#### So sánh Năng lực AI Nội bộ và Microsoft Copilot:
Khối Vận hành đã tiến hành kiểm tra chéo (Benchmark) giữa giải pháp AI nội bộ và Microsoft Copilot trên cùng một tập mẫu dữ liệu:
* **Hồ sơ Pháp lý KHCN:** AI nội bộ đạt **90%** vs Copilot đạt **100%**.
* **Hồ sơ Tài sản Bảo đảm:** AI nội bộ đạt **77%** vs Copilot đạt **97%**.
* **Ủy nhiệm chi (UNC):** AI nội bộ đạt **85%** vs Copilot đạt **95%**.

> **Kết luận rút ra:** Tiếp cận theo hướng cố gắng tự động hóa toàn phần 100% bằng STP thuần túy hoặc phụ thuộc vào một mô hình OCR/LLM đơn lẻ là không khả thi trong môi trường ngân hàng. Cần một **Mô hình Điều phối Tác tử Đa tầng (Agentic AI Orchestration)** kết hợp chặt chẽ với cơ chế **Human-in-the-Loop (HITL)**.

---

## 3. Case Study Quốc tế: Mô hình "AI Lending Operator" tại Ngân hàng X (Úc)

Báo cáo trình Tổng Giám đốc MB đã phân tích case study điển hình từ **Ngân hàng X tại Úc** — định chế tài chính đã tái thiết kế thành công mô hình vận hành tín dụng dựa trên AI:

```
              CASE STUDY: AI LENDING OPERATOR (NGÂN HÀNG X)
                 "AI runs the loan workflow. Humans approve."
             (Mục tiêu tự động hóa Happy-Path: 90% - 95%)

  [ Banker nhập: Customer + Amount ]
                 │
                 ▼
     ┌──────────────────────────────────────────────────────────┐
     │ 1. CASE ORCHESTRATOR: Khởi tạo Loan Case                 │
     │ 2. COLLECT: Thu thập bằng chứng từ Core, CRM, DMS        │
     │ 3. RESOLVE: Policy Agent phân giải chính sách áp dụng    │
     │ 4. DECIDE: Deterministic Rule Engine tính toán LTV, DTI  │
     │ 5. STRUCTURE: Loan Design Agent thiết kế gói vay         │
     │ 6. DRAFT: Document Generation soạn thảo 5/5 tài liệu     │
     │ 7. PROVE: QA + Control Agent kiểm tra chéo hợp đồng     │
     └──────────────────────────┬───────────────────────────────┘
                                │
                 ▼
  [ HUMAN FINAL REVIEW: Phê duyệt, Ký số & Giải ngân ]
```

### 3 Nguyên tắc Vận hành Cốt lõi của Ngân hàng X:
1. **AI làm công việc lặp lại (AI does the repetitive work):** Tìm kiếm, trích xuất OCR, đọc hiểu tài liệu, dự thảo phương án tín dụng, điều phối tác vụ và giải thích logic đề xuất.
2. **Luật cứng đưa ra quyết định bắt buộc (Rules make hard decisions):** Các công thức tính toán tài chính (DTI, LTV, hạn mức), kiểm tra điều kiện pháp lý bắt buộc (KYC/AML) được thực hiện bởi **Deterministic Rule Engine**, tuyệt đối không để LLM tự suy diễn ngẫu nhiên.
3. **Con người sở hữu trách nhiệm giải trình (Humans own accountability):** Quyền phê duyệt giải ngân cuối cùng, xử lý ngoại lệ chính sách và ký lệnh phát hành văn kiện hoàn toàn thuộc về chuyên viên có thẩm quyền.

### Nguồn Sự thật Duy nhất (Shared Governed State):
Mọi dữ liệu từ lịch sử giao dịch, ảnh chụp chứng từ, liên kết bằng chứng, phiên bản chính sách áp dụng, kết quả kiểm tra điều kiện đến dự thảo hợp đồng đều được ghi nhận vào một hồ sơ điện tử thống nhất (**Single Governed Loan Case**). Chuyên viên tín dụng khi mở màn hình không phải đăng nhập vào 8 hệ thống khác nhau, mà chỉ nhìn thấy một giao diện trực quan duy nhất với đầy đủ bằng chứng đã được thẩm định sẵn trong vòng 5–10 phút.

---

## 4. Thiết kế Quy trình Agentic AI cho Khối Vận hành MB

Áp dụng bài học từ Ngân hàng X kết hợp với hiện trạng 155 văn bản của MB, quy trình xử lý hồ sơ tín dụng và bảo lãnh được tái cấu trúc thành mô hình **Phân luồng Kết hợp (Hybrid STP + 4-Agent Orchestration)**:

<iframe src="/nghien-cuu/ngan-hang-so/mb-enterprise-agent-platform-operations/assets/02-operations-lending-agentic-flow.html" width="100%" height="700" style="border:none;border-radius:0.75rem;"></iframe>

---

### Chi tiết Luồng Vận hành 3 Giai đoạn:

#### Giai đoạn 1: Tiếp nhận & Sàng lọc Ban đầu (Intake & Deterministic First Check)
* Hồ sơ tín dụng hoặc bảo lãnh được tiếp nhận qua kênh số (BPM, iBiz, App).
* **Bộ lọc First Check (Rule-based):** Tự động kiểm tra tức thì các điều kiện cứng trên hệ thống: tra cứu lịch sử tín dụng CIC, điểm xếp hạng tín dụng nội bộ CRA và tính khả dụng của hạn mức (Limit).
* **Phân luồng nghiệp vụ:**
  * *Hồ sơ đạt chuẩn STP (~20%):* Các phương án giải ngân/bảo lãnh đơn giản, nằm trong danh mục rủi ro thấp và tệp khách hàng chuẩn hóa được chuyển thẳng vào luồng STP tự động hóa 100%.
  * *Hồ sơ phức tạp (~80%):* Toàn bộ hồ sơ còn lại được chuyển giao cho **Case Orchestrator** để kích hoạt luồng Agentic AI.

#### Giai đoạn 2: Điều phối Mạng lưới 4 Tác tử AI Chuyên trách (4-Agent Network)
Case Orchestrator tạo lập hồ sơ số duy nhất và điều phối 4 tác tử AI chuyên trách hoạt động theo chuỗi liên hoàn:
1. **AI (1) — Kiểm tra & Phân loại Hồ sơ (Classification & Checklist Agent):**
   * Đối chiếu danh mục tài liệu tải lên với quy định checklist theo từng mã sản phẩm.
   * Xác định hồ sơ đã nộp đúng và đủ thành phần hay chưa; tự động phát hiện tài liệu bị mờ, thiếu trang hoặc tải nhầm mục để cảnh báo RM bổ sung ngay lập tức.
2. **AI (2) — Đọc & Bóc tách Dữ liệu Chi tiết (Deep Extraction Agent):**
   * Thực hiện nhận dạng ký tự quang học (OCR) và trích xuất ngữ nghĩa chuyên sâu trên các tài liệu phức tạp (Hợp đồng mua bán, Hóa đơn VAT, Giấy chứng nhận quyền sử dụng đất, Ủy nhiệm chi, Thư bảo lãnh...).
   * Chuẩn hóa dữ liệu trích xuất thành định dạng JSON có cấu trúc, gán kèm điểm số tin cậy (Confidence Score) cho từng trường thông tin.
3. **AI (3) — Tra cứu Quy chế & Chính sách Tương ứng (Policy & Rule Matching Agent):**
   * Dựa trên loại hình khách hàng và phương án tín dụng, Agent tự động truy vấn kho dữ liệu quy chế nội bộ (155 văn bản quy định) để trích xuất chính xác phiên bản chính sách, điều khoản và điều kiện áp dụng tại thời điểm giao dịch.
4. **AI (4) — Kiểm tra Chéo Điều kiện Tín dụng (Compliance & Condition Cross-Check Agent):**
   * Đối chiếu dữ liệu thực tế do AI (2) bóc tách với danh sách điều kiện do AI (3) cung cấp.
   * Tự động kiểm tra toàn diện 106 điều kiện giải ngân (bao gồm 104 điều kiện nhóm 5 trước đây phải làm thủ công) và 70 điều kiện bảo lãnh.
   * Xuất báo cáo kiểm tra chi tiết: Xác nhận các điều kiện Đạt (Pass), Không đạt (Fail) và cảnh báo các điểm nghi ngờ.

#### Giai đoạn 3: Kho Lưu trữ Dữ liệu Tập trung & Phê duyệt Nghiệp vụ (Human-in-the-Loop)
* Toàn bộ dữ liệu, liên kết văn bản gốc và kết quả đối chiếu từ 4 tác tử AI được hợp nhất vào **Kho Dữ liệu Tập trung (Central Data Store)** để bảo đảm tính toàn vẹn và phục vụ kiểm toán sau này.
* **Giao diện Phê duyệt Nghiệp vụ (HITL Interface):**
  * Hồ sơ không bị chuyển thành một "hộp đen". Cán bộ Tín dụng và Quản lý Phê duyệt (1 cấp hoặc 2 cấp) chỉ cần xem bản tổng hợp kết quả đã được AI kiểm tra chéo sẵn.
  * Các trường thông tin có độ tin cậy thấp hoặc vi phạm chính sách sẽ được đánh dấu cảnh báo để chuyên viên tập trung thẩm định, giúp rút ngắn 70–80% thời gian xử lý thủ công.

---

### Chuẩn Hiệu năng Xử lý & Ngân sách Thời gian Tác vụ (Performance Benchmarks)

Báo cáo Khối Vận hành đã xác lập định mức ngân sách thời gian xử lý chi tiết nhằm bảo đảm trải nghiệm người dùng và tính khả thi kỹ thuật:

#### 1. Định mức Thời gian Xử lý OCR theo Độ dài Tài liệu:

| Số lượng Trang PDF | Thời gian Xử lý OCR / Layout (Chỉ đọc văn bản) | Tổng Thời gian Bóc tách Trường & Kiểm tra Tự động Hoàn tất |
|---|---|---|
| **4 trang** | 7 – 20 giây | **20 – 55 giây** |
| **10 trang** | 13 – 38 giây | **25 – 70 giây** |
| **20 trang** | 23 – 68 giây | **35 – 100 giây** |
| **30 trang** | 33 – 98 giây | **45 – 130 giây** |
| **50 trang** | 53 – 158 giây | **65 – 190 giây** |

#### 2. Ngân sách Thời gian cho Từng Tác vụ Kỹ thuật Thành phần:
* **Xác thực API Gateway & kiểm tra quyền truy cập:** 50 – 200 ms.
* **Kiểm tra cấu trúc yêu cầu & các trường bắt buộc:** 10 – 50 ms.
* **Kiểm tra khóa định danh chống trùng lặp (Idempotency Key):** 20 – 100 ms.
* **Tạo hồ sơ số (Case) & sự kiện kiểm toán ban đầu:** 50 – 200 ms.
* **Truy xuất thông tin khách hàng & ảnh chụp KYC:** 200 ms – 1 giây.
* **Truy xuất quyền sở hữu tài khoản, trạng thái & số dư:** 200 ms – 1 giây.
* **Truy xuất thông tin người thụ hưởng đã lưu:** 100 – 500 ms.
* **Kiểm tra định dạng BIC, mã quốc gia & tài khoản:** 10 – 100 ms.
* **Xác thực người thụ hưởng bên ngoài trước giao dịch:** 0.5 – 5 giây (tạm thời).
* **Ánh xạ biểu mẫu có cấu trúc từ API vào hồ sơ:** 10 – 100 ms.
* **Diễn giải chỉ thị phi cấu trúc bằng mô hình LLM:** **6 – 15 giây**.
* **Truy xuất các đoạn chính sách & phiên bản quy chế liên quan:** 200 ms – 1 giây.
* **Lưu cập nhật hồ sơ & trạng thái kiểm tra (Checkpoint):** 50 – 200 ms cho mỗi lần ghi.

---

## 5. Kiến trúc Mục tiêu: Enterprise Agent Platform tại MB

Để hỗ trợ quy trình vận hành phức tạp trên, đồng thời quản lý được toàn bộ hệ sinh thái Agent trong toàn ngân hàng mà không rơi vào bẫy "Agent Sprawl", tài liệu kiến trúc đề xuất xây dựng **Enterprise Agent Platform**:

<iframe src="/nghien-cuu/ngan-hang-so/mb-enterprise-agent-platform-operations/assets/01-enterprise-agent-platform-architecture.html" width="100%" height="700" style="border:none;border-radius:0.75rem;"></iframe>

---

### 5.1. Triết lý Thiết kế: "Mở ở Lớp Phát triển, Thống nhất ở Lớp Kiểm soát"

Enterprise Agent Platform **không** phải là một công cụ duy nhất để tạo Agent, cũng **không** phải là một runtime tập trung bắt buộc mọi nhóm phải lập trình trên đó. Ngân hàng phục vụ đồng thời 3 nhóm đối tượng:
1. **Người dùng nghiệp vụ:** Sử dụng các Agent hoặc template có sẵn thông qua giao diện Web hoặc Microsoft Teams.
2. **Người dùng có hiểu biết công nghệ (BA, Kiến trúc sư, Chuyên viên dữ liệu):** Cấu hình Agent và workflow trực quan thông qua công cụ Low-code.
3. **Đội ngũ Developer:** Tự chủ phát triển các Agent chuyên sâu bằng code, tự do lựa chọn framework phù hợp nhất với bài toán (LangGraph, Google ADK, OpenAI Agents SDK, Semantic Kernel, Hermes...).

> **Nguyên tắc vàng:** *Tổ chức không chuẩn hóa cách mọi Agent được viết, nhưng bắt buộc phải chuẩn hóa cách mọi Agent được định danh, cấp quyền, sử dụng model, gọi tool, ghi nhận log và thu hồi khi có rủi ro.*

---

### 5.2. Bản đồ 14 Cấu phần Kiến trúc Nền tảng

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │ LAYER 1: AGENT FRONTEND (KÊNH GIAO DIỆN TƯƠNG TÁC)                     │
 │ Web Portal · Microsoft Teams (Kênh bổ trợ) · Desktop Workspace · APIs  │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 2: INGRESS AGENT GATEWAY (CỔNG TIẾP NHẬN TẬP TRUNG)              │
 │ Xác thực Danh tính · Định tuyến Yêu cầu · Áp dụng Quota & Rate Limit   │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 3: AGENT RUNTIMES (MÔI TRƯỜNG THỰC THI ĐA DẠNG)                  │
 │ ├─ Personal Agent Runtime: Sandbox cá nhân (Hermes, OpenClaw...)       │
 │ └─ Enterprise Agent Runtime: Multi-Agent Workflows, LangGraph, BPM     │
 └───────────────────┬───────────────────────────────┬────────────────────┘
                     │                               │
 ┌───────────────────▼────────────────┐ ┌────────────▼────────────────────┐
 │ LAYER 4: ENTERPRISE MODEL GATEWAY  │ │ LAYER 5: TOOL / MCP GATEWAY    │
 │ • Quản lý hạn ngạch Token & Chi phí│ │ • Chuẩn hóa Model Context Proto│
 │ • Chuyển mạch Dự phòng (Failover)  │ │ • Phân quyền Tool Call (R/W)   │
 │ • AI Guardrails & Che giấu PII     │ │ • Xác thực Phê duyệt Hành động │
 └───────────────────┬────────────────┘ └────────────┬────────────────────┘
                     │                               │
                     └───────────────┬───────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 6: EGRESS AGENT GATEWAY (CỔNG KẾT NỐI MẠNG ĐI RA)                │
 │ Kiểm soát Network Path Outbound · Áp Allowlist/Denylist · Chặn rò rỉ   │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │ LAYER 7: GOVERNANCE, SECURITY & OBSERVABILITY (QUẢN TRỊ TẬP TRUNG)     │
 │ • Agent IAM & Identity Delegation • AI Asset Registries (Agent/Tool)   │
 │ • Agent Observability (Audit Trail)• Control Plane (Kill-switch Dừng) │
 └────────────────────────────────────────────────────────────────────────┘
```

#### Phân tích Chi tiết các Cấu phần Cốt lõi:

1. **Ingress Agent Gateway:** Điểm vào tập trung bảo vệ hệ sinh thái Agent. Tiếp nhận request từ các kênh giao diện, xác thực người dùng, áp dụng chính sách truy cập ban đầu và định tuyến chính xác đến runtime tương ứng; ngăn chặn việc người dùng hoặc ứng dụng gọi trực tiếp vào Agent.
2. **Personal Agent Runtime vs Enterprise Agent Runtime:**
   * *Personal Runtime:* Dành cho các công cụ như Hermes, OpenClaw chạy trên máy trạm cá nhân của kỹ sư, phục vụ hỗ trợ coding, tóm tắt tài liệu nội bộ. Được khoanh vùng trong sandbox, giới hạn quyền chạy lệnh command/script và bắt buộc trỏ model endpoint về Model Gateway.
   * *Enterprise Runtime:* Chạy trên hạ tầng máy chủ tập trung của ngân hàng, quản lý phiên bản theo quy trình CI/CD, có khả năng rollback, tạm dừng hoặc thu hồi theo thời gian thực.
3. **Enterprise Model Gateway:**
   * Ngăn chặn hoàn toàn tình trạng lập trình viên tự lấy thẻ tín dụng hoặc dùng API key cá nhân kết nối ra ngoài.
   * Quản lý hạn ngạch token, chi phí và phân bổ ngân sách AI cho từng khối nghiệp vụ.
   * Hỗ trợ chuyển mạch dự phòng thông minh (Dynamic Model Routing): tự động chuyển sang mô hình dự phòng khi nhà cung cấp chính bị quá tải hoặc ngừng hoạt động.
4. **Tool / MCP Gateway & MCP Server:**
   * **Đây là chốt chặn quan trọng nhất của kỷ nguyên Agent.** Tool là thứ biến AI từ "trả lời câu hỏi" thành "thực hiện hành động".
   * Áp dụng giao thức chuẩn hóa **Model Context Protocol (MCP)** do Anthropic khởi xướng để chuẩn hóa cách Agent đọc file, truy vấn cơ sở dữ liệu và gọi API hệ thống.
   * Phân tách nghiêm ngặt giữa:
     * *Tool chỉ đọc (Read-only Tools):* Truy vấn số dư, tra cứu quy chế, đọc thông tin hồ sơ.
     * *Tool có khả năng ghi dữ liệu (State-changing Tools):* Khởi tạo giao dịch, cập nhật hạn mức, kích hoạt giải ngân -> Bắt buộc phải có xác nhận của con người (Human Approval).
5. **Egress Agent Gateway:** Kiểm soát toàn bộ lưu lượng mạng đi ra ngoài (Outbound Traffic) từ các Agent. Chặn đứng nguy cơ Agent tự ý gửi dữ liệu nội bộ đến các máy chủ hoặc dịch vụ lạ trên Internet thông qua cơ chế danh sách cho phép (Allowlist).
6. **Agent IAM & Identity Delegation (Ủy quyền Danh tính):**
   * Định danh duy nhất cho từng thực thể: `Agent ID`, `Tool ID`, `User ID`.
   * **Giải quyết bài toán ủy quyền danh tính (Delegated Authority):** Phân biệt rõ Agent đang hành động với tư cách độc lập hay hành động thay mặt người dùng nào. Quyền hạn tối đa của Agent không bao giờ được vượt quá quyền hạn của người dùng ủy quyền cho nó.
7. **Agent Control Plane & AI Asset Registries:**
   * Quản lý tập trung 3 danh mục tài sản số: *Agent Registry* (ai sở hữu, đang chạy ở đâu), *Tool/MCP Registry* (danh sách công cụ được phép dùng) và *Model Registry* (danh mục mô hình được cấp phép).
   * **Nút ngắt khẩn cấp (Kill-Switch):** Cung cấp thẩm quyền cho đội ngũ quản trị rủi ro có thể vô hiệu hóa, tạm dừng hoặc thu hồi quyền truy cập của bất kỳ Agent nào trong vòng vài giây khi phát hiện hành vi bất thường.

---

## 6. Lộ trình Thực thi 5 Việc Ưu tiên trong Giai đoạn Đầu

Tài liệu kiến trúc nhấn mạnh: **MB không nên cố gắng xây dựng toàn bộ Enterprise Agent Platform như một khối đồ sộ ngay từ ngày đầu**, vì phạm vi quá lớn sẽ dẫn đến chậm trễ và lãng phí nguồn lực. Trong giai đoạn đầu, ngân hàng cần tập trung vào **5 điểm kiểm soát tối thiểu nhưng có tác động bảo vệ lớn nhất**:

```
                       LỘ TRÌNH 5 VIỆC ƯU TIÊN BAN ĐẦU
 ┌───────────────────────────────────┬───────────────────────────────────┐
 │ 1. Thử nghiệm Personal Agent      │ 2. Triển khai Enterprise          │
 │    Runtime có kiểm soát           │    Model Gateway                  │
 │    • Đánh giá Hermes, OpenClaw    │    • Điểm truy cập mô hình chung  │
 │    • Giới hạn quyền workspace/cmd │    • Quản lý Quota, Token, Cost   │
 │    • Cấu hình endpoint tập trung  │    • Lọc PII & Logging tập trung  │
 ├───────────────────────────────────┼───────────────────────────────────┤
 │ 3. Triển khai Ingress/Egress      │ 4. Triển khai Tool / MCP Gateway  │
 │    Agent Gateway                  │    • Chuẩn hóa Model Context Proto│
 │    • Chặn kết nối tự do vào/ra    │    • Quản lý danh mục MCP Servers │
 │    • Kiểm soát biên mạng an toàn  │    • Phân quyền Tool Read vs Write│
 ├───────────────────────────────────┴───────────────────────────────────┤
 │ 5. Đánh giá Microsoft Teams như Kênh Agent Frontend Bổ trợ            │
 │    • Khai thác luồng làm việc sẵn có của khối CNTT & Vận hành         │
 │    • Thí điểm các tác vụ tra cứu, giao việc và xác nhận phê duyệt     │
 └───────────────────────────────────────────────────────────────────────┘
```

1. **Ưu tiên 1 — Đánh giá và Lựa chọn Personal Agent Runtime Thử nghiệm có Kiểm soát:**
   * Thừa nhận nhu cầu thực tế của các kỹ sư đang sử dụng các công cụ như Hermes, OpenClaw để tăng năng suất.
   * Ban hành danh sách các runtime được phép sử dụng trong môi trường sandbox; cấu hình bắt buộc chặn tự ý đọc source code dự án mật, không cho phép lưu credential cá nhân và bắt buộc kết nối model qua Model Gateway.
2. **Ưu tiên 2 — Triển khai Enterprise Model Gateway:**
   * Cung cấp một model endpoint thống nhất cho toàn bộ các nhóm dự án AI tại MB.
   * Giám sát chặt chẽ chi phí gọi API, áp đặt hạn ngạch token theo đơn vị và thiết lập cơ chế tự động che giấu dữ liệu định danh khách hàng (PII Masking).
3. **Ưu tiên 3 — Triển khai Ingress & Egress Agent Gateway:**
   * Thiết lập chốt kiểm soát lưu lượng mạng ở cả hai chiều; bảo đảm mọi Agent chỉ được giao tiếp qua các đường dẫn mạng được bảo vệ, ngăn chặn triệt để nguy cơ tấn công từ bên ngoài và rò rỉ dữ liệu ra bên ngoài.
4. **Ưu tiên 4 — Triển khai Tool / MCP Gateway:**
   * Thí điểm tích hợp các MCP Server đầu tiên phục vụ tra cứu dữ liệu CIC, thông tin tài khoản và văn bản quy chế.
   * Thiết lập cơ chế kiểm soát nghiêm ngặt đối với các tool có khả năng thay đổi dữ liệu, bắt buộc phải có bước xác thực 2 lớp hoặc xác nhận từ chuyên viên.
5. **Ưu tiên 5 — Đánh giá Microsoft Teams như Kênh Agent Frontend Bổ trợ:**
   * Nhận diện Microsoft Teams là không gian làm việc hàng ngày của hàng ngàn cán bộ nhân viên MB.
   * Xây dựng bot tương tác tích hợp qua Ingress Gateway để nhân viên có thể gọi Agent tra cứu quy trình, nhận thông báo nhắc việc và xác nhận phê duyệt các tác vụ tín dụng đơn giản ngay trên Teams chat.

---

## 7. Bảng Thuật ngữ Đối chiếu Song ngữ (Bilingual Glossary)

| Thuật ngữ Tiếng Anh | Nghĩa Tiếng Việt / Chú giải bối cảnh |
|---|---|
| **AI Agent** | Tác tử AI; hệ thống phần mềm có khả năng tự chủ tiếp nhận mục tiêu, sử dụng công cụ, gọi API và thực hiện chuỗi hành động. |
| **Agent Control Plane** | Mặt phẳng điều khiển tác tử; tầng quản trị vòng đời, chính sách, chi phí và cấu hình hệ sinh thái Agent. |
| **Agent Guardrails** | Rào chắn an toàn tác tử; lớp kiểm soát đầu vào, đầu ra, ngăn chặn prompt injection và che giấu thông tin nhạy cảm. |
| **Agent Sprawl** | Sự bùng nổ tác tử ngoài tầm kiểm soát; hiện tượng Agent phát triển tự phát, phân mảnh gây rủi ro bảo mật và chi phí. |
| **Case Orchestrator** | Bộ điều phối hồ sơ nghiệp vụ; thành phần trung tâm quản lý trạng thái, luồng công việc và phối hợp các Agent chuyên trách. |
| **Deterministic Rule Engine** | Công cụ quy tắc xác định; hệ thống tính toán và kiểm tra logic cứng (như tỷ lệ LTV, DTI) không phụ thuộc vào LLM. |
| **DocAI** | Trí tuệ nhân tạo xử lý tài liệu; công nghệ kết hợp OCR và LLM để đọc, hiểu và bóc tách dữ liệu từ văn bản. |
| **Egress Agent Gateway** | Cổng kiểm soát mạng đi ra của Agent; chốt chặn kiểm tra các kết nối mạng outbound và áp dụng allowlist. |
| **Golden Dataset** | Tập dữ liệu vàng chuẩn mực; bộ dữ liệu kiểm thử đa dạng, chất lượng cao dùng để đánh giá và benchmark mô hình. |
| **Human-in-the-Loop (HITL)** | Quy trình có con người can thiệp; cơ chế phân luồng tự động để chuyên viên xác nhận các kết quả có độ tin cậy thấp. |
| **Identity Delegation** | Ủy quyền danh tính; cơ chế phân định rõ Agent đang hành động với quyền hạn được ủy quyền từ người dùng nào. |
| **Ingress Agent Gateway** | Cổng tiếp nhận tác tử; điểm vào tập trung xác thực, định tuyến và kiểm soát hạn ngạch cho mọi yêu cầu gọi Agent. |
| **Model Context Protocol (MCP)** | Giao thức ngữ cảnh mô hình; chuẩn mở giúp Agent kết nối và sử dụng các công cụ, dữ liệu bên ngoài một cách thống nhất. |
| **Model Gateway** | Cổng điều phối mô hình; hạ tầng quản lý tập trung truy cập LLM, quota token, chi phí và chuyển mạch dự phòng. |
| **Personal Agent Runtime** | Môi trường thực thi tác tử cá nhân; phần mềm Agent chạy cục bộ trên máy trạm (như Hermes, OpenClaw). |
| **Straight-Through Processing (STP)** | Xử lý luồng thẳng tự động; quy trình xử lý giao dịch tự động 100% từ đầu đến cuối không cần con người can thiệp. |
| **Tool / MCP Gateway** | Cổng kiểm soát công cụ; điểm quản lý phân quyền và kiểm soát việc Agent gọi tool hoặc kích hoạt hành động nghiệp vụ. |
| **Ungoverned AI Agents** | Các tác tử AI tự phát; các công cụ Agent hoạt động ngoài khung kiểm soát và chính sách an toàn của doanh nghiệp. |

---

## 8. Quy ước Cấu trúc Thư mục

Toàn bộ bài nghiên cứu, sơ đồ và bằng chứng số liệu được tổ chức theo quy chuẩn của Kho Tri thức:

```text
nghien-cuu/
└── ngan-hang-so/
    └── mb-enterprise-agent-platform-operations/
        ├── index.md                                        # Bài nghiên cứu toàn văn
        ├── assets/                                         # Mã nguồn sơ đồ JSON & bản HTML kết xuất
        │   ├── 01-enterprise-agent-platform-architecture.workflow.json
        │   ├── 01-enterprise-agent-platform-architecture.html
        │   ├── 02-operations-lending-agentic-flow.workflow.json
        │   └── 02-operations-lending-agentic-flow.html
        └── evidence/                                       # Hồ sơ số liệu gốc trích xuất từ 2 tài liệu
            └── combined-evidence.json
```
