# Đánh giá Sẵn sàng Công nghệ & AI (MBBank)

> **Tài liệu nghiên cứu & đánh giá:** Báo cáo Đánh giá Mức độ Sẵn sàng Công nghệ và Trí tuệ Nhân tạo (CS5. Technology and AI Readiness Assessment) · **Thời gian khảo sát:** Tháng 09/2026.  
> **Đơn vị nghiên cứu:** MBBank (MB) · **Nguồn đối chiếu:** Báo cáo Đánh giá Định kỳ 7 Dự án Chiến lược (31/07/2026), Khảo sát Năng lực Dữ liệu & Phỏng vấn Lãnh đạo Khối Nghiệp vụ & CNTT.  
> **Nguyên tắc xuyên suốt:** AI không thể tạo ra giá trị kinh doanh thực chất nếu chỉ triển khai dưới dạng các "Use Case đơn lẻ, manh mún" (Fragmented Use Cases). Chuyển đổi thành công đòi hỏi tiếp cận theo **Domain nghiệp vụ đầu-cuối (End-to-End Domain Transformation)**, gắn chặt với chỉ tiêu **Lợi nhuận trước thuế (PBT - Profit Before Tax)**, được bảo đảm bởi mô hình tổ chức **Hub-and-Spoke** và hạ tầng **DataOps/MLOps** tự động hóa.
>
> 📌 **Báo cáo Kỹ thuật Chuyên sâu:** [Báo cáo Kiến trúc & Nợ kỹ thuật CNTT](./danh-gia-kien-truc-cntt) — Phân tích nợ kỹ thuật 6 nhóm, bản thiết kế kiến trúc 4 tầng, Enterprise LLM Gateway và Cổng kiểm soát Approval to Build.

---

## 1. Tóm tắt điều hành (Executive Summary)

Đến tháng 9/2026, ngân hàng đã đạt được những bước tiến ban đầu đáng ghi nhận trong hành trình ứng dụng AI:
- Đã đưa vào vận hành **11 trường hợp sử dụng AI (AI Use Cases)** trên nhiều lĩnh vực từ Bán lẻ (Retail), Chăm sóc khách hàng (Contact Center), Vận hành nội bộ (Middle Office) đến Hỗ trợ phát triển CNTT (IT Development).
- Một số giải pháp bước đầu chứng minh hiệu quả và mở rộng quy mô lớn: **AI Fraud** được tích hợp đồng bộ trên hệ sinh thái App, Biz và Thẻ tín dụng; **AI Enterprise** thu hút ~3.000 lượt truy vấn nội bộ/ngày trong 2 tuần đầu; **AI SmartSearch** xử lý từ 200.000 đến 300.000 truy vấn mỗi ngày.
- Đã bước đầu hình thành **Trung tâm AI tập trung (Central AI Center)** trực thuộc Khối CNTT, nắm giữ các năng lực kỹ thuật chuyên sâu về Xử lý ngôn ngữ tự nhiên (NLP), Giọng nói (Speech), Thị giác máy tính (Computer Vision) và Trợ lý ảo (Virtual Assistant).

Tuy nhiên, cuộc kiểm toán năng lực toàn diện đã chỉ ra **ba điểm nghẽn mang tính cấu trúc** đang ngăn cản ngân hàng chuyển hóa năng lực thử nghiệm AI thành giá trị tài chính thực chất:

1. **Bẫy tiếp cận Use Case cục bộ ("Too Small"):** Các giải pháp AI hiện tại chỉ số hóa từng mắt xích đơn lẻ trong quy trình nghiệp vụ (ví dụ: chỉ tóm tắt hồ sơ vay hoặc trích xuất số liệu) thay vì tái cấu trúc toàn diện chuỗi giá trị (End-to-End Workflow). Điều này khiến hiệu quả bị triệt tiêu ở các khâu thủ công liền kề và không tạo ra tác động lũy kế lên kết quả kinh doanh (PBT).
2. **Ngăn cách giữa Nghiệp vụ và Công nghệ (Business–Technology Disconnect):** Khối AI hiện đặt thuần túy trong Khối CNTT, vận hành theo tư duy nghiên cứu kỹ thuật (Technology-first) hơn là giải quyết bài toán kinh doanh. Việc thiếu vắng vai trò **Cầu nối Dịch thuật AI–Nghiệp vụ (AI–Business Translators)** khiến các dự án thiếu sự bảo trợ sở hữu từ nghiệp vụ ngay từ ngày đầu, dẫn đến tỷ lệ hủy bỏ cao (như AI Telesales, AI Mentor) hoặc không đo lường được hiệu quả tài chính sau khi Golive (như AI Credit Memo, AI Credit Scoring).
3. **Nợ kỹ thuật về DataOps & MLOps Nền tảng:** Mặc dù đã có hồ dữ liệu (Data Lake) và hệ thống API phân phối mạnh, nhưng khâu chuẩn bị, làm sạch và dán nhãn dữ liệu vẫn mang tính thủ công cao. Dữ liệu chưa được đóng gói thành các **Sản phẩm Dữ liệu (Data Products)** gắn với chủ sở hữu nghiệp vụ (Data Domains). Đặc biệt, ngân hàng hoàn toàn thiếu vắng các khối dùng chung tối quan trọng cho GenAI như **Cổng định tuyến mô hình (LLM Gateway)**, **Bộ lưu trữ gợi ý chuẩn hóa (Prompt Library)** và cơ chế **Giám sát độ trôi mô hình (Drift Monitoring)**.

---

## 2. Đánh giá Mức độ Sẵn sàng AI theo 5 Chiều Cốt lõi

Khung đánh giá khảo sát toàn diện hệ thống AI của ngân hàng trên 5 chiều kích chiến lược:

| Chiều đánh giá | Câu hỏi then chốt | Thành tựu then chốt đã đạt | Khoảng cách cốt lõi (Gaps) |
|---|---|---|---|
| **1. Tầm nhìn chiến lược & Giá trị (Strategic Vision & Value Realization)** | Ngân hàng đã có tầm nhìn AI rõ ràng và đồng pha với chiến lược kinh doanh tổng thể chưa? | • 11 use cases đã triển khai trên nhiều khối nghiệp vụ.<br>• Một số dự án vượt khỏi pilot lên quy mô toàn hàng (ví dụ: AI Fraud trên App, Biz, Cards). | • **Thiếu chiến lược AI tổng thể** đồng nhất với tầm nhìn chiến lược của MBBank.<br>• Hiểu biết và kỳ vọng về AI chênh lệch lớn giữa các khối/phòng ban.<br>• **Không có chỉ tiêu PBT cụ thể** được xác lập trong lộ trình, dẫn đến việc giải pháp tạo giá trị mờ nhạt hoặc phải hủy bỏ dự án. |
| **2. Phương pháp ứng dụng AI (AI Adoption)** | Ngân hàng đã chọn đúng cách thức ứng dụng AI để tạo ra tác động vật chất đáng kể chưa? | • Giải pháp AI đã phủ từ Khối Bán lẻ (Retail) tới phát triển phần mềm CNTT.<br>• Một số công cụ đạt lưu lượng lớn ban đầu (AI Enterprise đạt ~3.000 truy vấn/ngày trong 2 tuần đầu). | • **Triển khai manh mún (Fragmented use cases)**, chỉ tối ưu 1 bước cục bộ thay vì chuyển đổi quy trình đầu-cuối.<br>• **Thiếu chỉ số KPI về mức độ tiếp nhận (Adoption KPIs)** để đo lường mức độ chuyển đổi số thực tế và tần suất nhân viên sử dụng AI hàng ngày. |
| **3. Mô hình vận hành & Nhân tài (Operating Model & Talent)** | Ngân hàng đã có tổ chức và mô hình vận hành phù hợp để triển khai AI thành công bền vững chưa? | • Đã thành lập Trung tâm AI tập trung (Central AI Center).<br>• Sở hữu năng lực kỹ thuật chuyên sâu về Virtual Assistants, Computer Vision, Speech & NLP. | • **Quyền sở hữu đầu-cuối (E2E ownership) bị phân mảnh** và mơ hồ giữa Khối Nghiệp vụ, Khối Dữ liệu và Trung tâm AI.<br>• **Thiếu hụt vai trò AI–Business Translator**, cản trở nghiêm trọng khả năng thiết kế bài toán và lập kế hoạch use case có tính ứng dụng cao. |
| **4. Dữ liệu & Công nghệ nền tảng (Data & Technology)** | Ngân hàng đã xây dựng nền tảng dữ liệu và công nghệ đủ vững chắc cho AI quy mô lớn chưa? | • Duy trì nền tảng dữ liệu chung cho phép chạy các use case liên phòng ban.<br>• Khả năng cung cấp API kết nối dữ liệu đạt mức cao (High). | • **Chuẩn bị và dán nhãn dữ liệu còn rất thủ công**, làm nghẽn tiến độ huấn luyện và triển khai mô hình.<br>• **Chưa có các cấu phần AI tái sử dụng (Reusable AI Components)** như Thư viện Prompt (Prompt Libraries), Cổng kết nối mô hình (LLM Gateways). |
| **5. Quản trị rủi ro & Tuân thủ (Risk & Governance)** | Ngân hàng đã thiết lập khung kiểm soát rủi ro và quản trị đạo đức AI đầy đủ chưa? | • Hệ thống quản trị dữ liệu và ngân hàng hiện hữu cung cấp nền móng bước đầu để xây dựng khung quản trị AI. | • **Khung quản trị AI (AI Governance Framework) chưa được thiết lập**; thiếu định chế về trách nhiệm giải trình (Accountability), kiểm soát rủi ro thuật toán, an toàn dữ liệu và quyền riêng tư khi dùng GenAI. |

---

## 3. Chuyển dịch Chiến lược: Từ "Use Case Manh mún" sang "Chuyển đổi theo Domain Nghiệp vụ"

### 3.1. Phân tích ba lộ trình tiếp cận ứng dụng AI

Khi xem xét bài toán triển khai AI trên quy mô toàn ngân hàng, có 3 mô hình tiếp cận điển hình:

```
               [ Tiếp cận Toàn ngân hàng (Entire Bank) ]
                       -> Quá lớn (Too Big)
                 (Quá nhiều Domain, Data và Stakeholder;
                   tê liệt phân tích, khó ra kết quả)
                                ▲
                                │
          ┌─────────────────────┴─────────────────────┐
          │                                           │
[ Chuyển đổi theo Domain ]                     [ Tiếp cận theo Use Case ]
     (Transforming a Domain)                         (Use-case Approach)
       -> VỪA VẶN (Just Right)                        -> Quá nhỏ (Too Small)
   (Cân bằng tác động E2E, lãnh đạo              (Hiện trạng của MB: Quá ngách,
     cam kết, kết quả rõ trong ngắn hạn;          manh mún, không tạo sức mạnh tổng hợp
    dễ nhân rộng sang Domain tương tự)             về dữ liệu và nền tảng công nghệ)
```

1. **Toàn ngân hàng (Entire Bank) — "Quá lớn" (Too Big):** Đòi hỏi đồng bộ hàng chục khối phòng ban, hàng trăm luồng dữ liệu và lượng lớn bên liên quan cùng lúc. Hậu quả là dự án kéo dài, chi phí khổng lồ và không thể chứng minh giá trị kinh doanh ngắn hạn.
2. **Từng Use Case đơn lẻ (Use Case) — "Quá nhỏ" (Too Small — *Hiện trạng tại MB*):** Chọn các bài toán cục bộ, thiếu tính kết nối. Kết quả tạo ra các "hòn đảo tự động hóa" rời rạc, không cộng hưởng về mặt dữ liệu, công nghệ hay trải nghiệm khách hàng, và không dịch chuyển được các chỉ số tài chính vĩ mô.
3. **Chuyển đổi theo Domain (Transforming a Domain) — "Tối ưu & Vừa vặn" (Just Right):**  
   Một **Domain** được định nghĩa là một *khu vực nghiệp vụ hoặc chức năng độc lập, có ranh giới rõ ràng, có lãnh đạo chịu trách nhiệm trực tiếp (Accountable Leadership) và có quyền tự chủ đủ lớn để được chuyển đổi đầu-cuối bằng AI*.  
   * **Tác động vật chất nhanh:** Tạo ra bước nhảy vọt về năng suất hoặc doanh thu trong phạm vi được khoanh vùng mà không vướng phải sự phức tạp của toàn ngân hàng.
   * **Bảo trợ nghiệp vụ mạnh mẽ:** Vì bài toán giải quyết trực tiếp nỗi đau và chỉ tiêu PBT của Domain Leader, ban lãnh đạo khối sẽ cam kết nguồn lực và quyết liệt thúc đẩy quản trị thay đổi (Change Management).
   * **Khả năng nhân rộng (Replicability):** Các năng lực dữ liệu, hạ tầng Agent và bài học kinh nghiệm hình thành từ một Domain đầu tiên có thể dễ dàng tái sử dụng cho các Domain tiếp theo.

---

### 3.2. Toàn cảnh 14 Banking Domains và Hiện trạng Triển khai tại Ngân hàng

Đánh giá tiềm năng tác động của 14 miền nghiệp vụ ngân hàng chuẩn mực đối chiếu với danh mục dự án AI hiện tại của MB:

| Nhóm đòn bẩy | STT | Miền nghiệp vụ (Typical Banking Domain) | Tiềm năng tác động (Impact Potential) | Dự án AI hiện hữu tại MBBank | Tình trạng vận hành |
|---|---|---|---|---|---|
| **Tăng trưởng Doanh thu (Revenue Growth)** | 1 | **Thu hút khách hàng mới (Acquisition)** | **Cao (High)** | AI Telesales | **Dừng triển khai (Discontinued)** *(Do khách hàng phàn nàn, chuyển đổi thấp)* |
| | 2 | **Bán chéo & Gia tăng gắn kết (Cross-sell & Relationship Deepening)** | **Cao (High)** | AI Beerich<br>AI Paste2Pay<br>AI SmartSearch | Vận hành (Launched)<br>Vận hành (Launched)<br>Vận hành (Launched) |
| | 3 | **Giữ chân khách hàng (Retention)** | **Cao (High)** | *(Chưa có use case)* | Chưa triển khai (Not attempted) |
| **Tinh gọn Quy trình Đầu-Cuối (E2E Journey & Process)** | 4 | **Onboarding khách hàng tinh gọn E2E** | **Cao (High)** | *(Chưa có use case E2E)* | Trong lộ trình (In roadmap) |
| | 5 | **Cho vay tinh gọn E2E (E2E Streamlined Lending)** | **Cao (High)** | AI Credit Scoring<br>AI Credit Memo | Vận hành (Launched)<br>Vận hành (Launched) |
| | 6 | **Hành trình Tiền gửi và Dịch vụ khác** | Trung bình (Medium) | *(Chưa có use case)* | Chưa triển khai (Not attempted) |
| | 7 | **Tinh gọn Khối Vận hành Trung gian & Hậu sảnh (Middle & Back-Office)** | Trung bình (Medium) | AI Fraud | Vận hành (Launched) *(Triển khai diện rộng trên App, Biz, Cards)* |
| | 8 | **Tối ưu hóa toàn diện Trung tâm Chăm sóc khách hàng (Contact Center)** | **Cao (High)** | AI Customer | Thử nghiệm (Pilot) *(Chất lượng chưa ổn định, nghẽn định tuyến)* |
| **Chuyển đổi Hiệu quả Cấu trúc (Structural Efficiency)** | 9 | Tối ưu mạng lưới mạng lưới chi nhánh & ATM/IDM | Trung bình (Medium) | *(Chưa có use case)* | Chưa triển khai (Not attempted) |
| | 10 | Tối ưu hóa chi phí mua sắm ngoài (External Spend) | Trung bình (Medium) | *(Chưa có use case)* | Chưa triển khai (Not attempted) |
| | 11 | **Hiệu quả phát triển CNTT (IT Efficiency)** | **Cao (High)** | AI for IT | Vận hành (Launched) *(Hỗ trợ dev/test nhưng thiếu chuẩn quản trị)* |
| | 12 | Tối ưu hóa Khối chức năng Doanh nghiệp (Corporate Functions) | Trung bình (Medium) | AI Enterprise<br>AI Mentor | Vận hành (Launched) *(Context yếu, dồn vào tín dụng)*<br>**Dừng triển khai (Discontinued)** *(Nhân viên ít dùng)* |
| **Nền tảng Hỗ trợ Chiến lược (Strategic Enablers)** | 13 | **Năng lực Dữ liệu & Công nghệ (Data & Tech Enablement)** | **Bắt buộc (Enabler)** | Data Platform | Nền tảng chung có sẵn; thiếu MLOps & LLM Gateway |
| | 14 | **Con người & Nhân tài AI (People & Talent)** | **Bắt buộc (Enabler)** | Central AI Unit | Tổ chức tập trung trong IT; thiếu AI Translator |

> **Nhận xét cốt lõi:**
> 1. Các giải pháp AI thuộc các miền có tiềm năng cao (High Potential) hiện tại còn **quá nhỏ về mặt phạm vi (small in scope)**, chưa tạo được chuyển biến mang tính cách mạng cho toàn bộ hành trình trải nghiệm của khách hàng.
> 2. Các use case được chọn đi đúng xu thế thế giới (Fraud, Scoring, Credit Memo, Contact Center), nhưng bị **chia cắt (fragmented)** thành các khâu độc lập, chưa khép kín quy trình E2E.
> 3. Rất thiếu vắng các sáng kiến mang tính nền tảng dài hạn: **khung mô hình vận hành AI bền vững** và **hạ tầng AI tái sử dụng**.

---

### 3.3. Nghiên cứu Điển hình: Lộ trình Ứng dụng Agentic AI và LLM trên Miền "Vòng đời Khách hàng"

Khi áp dụng phương pháp tiếp cận theo Domain cho miền chiến lược **"Tương tác xuyên suốt Vòng đời Khách hàng" (Customer Lifecycle Engagement)**, ngân hàng có thể triển khai hệ thống đòn bẩy kết hợp giữa Mô hình ngôn ngữ lớn (LLM) và Tác tử AI tự chủ (Agentic AI):

```
       VÒNG ĐỜI KHÁCH HÀNG (CUSTOMER LIFECYCLE DOMAIN)
 ┌──────────────────────┬──────────────────────┬──────────────────────┐
 │    1. THU HÚT        │   2. GIA TĂNG GẮN KẾT│     3. GIỮ CHÂN      │
 │   (Acquisition)      │     (Cross-sell)     │     (Retention)      │
 ├──────────────────────┼──────────────────────┼──────────────────────┤
 │• Thiết kế gói SP ESG │• Loyalty cá nhân hóa │• Cảnh báo sớm rời bỏ │
 │• Tinh gọn luồng vay  │• RM Co-pilot (LLM)   │• Khảo sát NPS toàn diện│
 │• Phân khúc ngoại tệ  │• Đãi ngộ KPI Chi nhánh│• Gói ưu đãi giữ chân  │
 │• Phối thức Digital   │• Gói trả lương Payroll│• Điều phối chuyên viên│
 │• Agentic Campaigning │• Bán chéo số kích hoạt│• Autonomous Retention │
 │• Onboarding 180 ngày │• War-Room số đa kênh │  AI Agent (LLM/Agent)│
 └──────────────────────┴──────────────────────┴──────────────────────┘
```

#### Phân rã Đòn bẩy Kỹ thuật & Nghiệp vụ:

1. **Giai đoạn Thu hút khách hàng (Acquisition):**
   * *Đổi mới sản phẩm:* Đưa ra các gói sản phẩm ngoài ngân hàng truyền thống (Beyond Banking) và sản phẩm tài chính xanh (ESG).
   * *Trải nghiệm số tinh gọn (LLM):* Ứng dụng LLM cung cấp cẩm nang hướng dẫn bán hàng thông minh (AI Sales Guide) cho chuyên viên tư vấn; tính toán hạn mức vay sơ bộ tức thì dựa trên luồng dữ liệu mở.
   * *Phân khúc khách hàng chuyên biệt:* Thiết kế gói vay thế chấp cá nhân hóa cho nhóm khách hàng có thu nhập ngoại tệ.
   * *Chiến dịch tiếp thị số tự chủ (Agentic Campaigning - LLM/Agent):* Triển khai mạng lưới Multi-Agent tự vận hành chiến dịch số: Agent nghiên cứu thị trường (Market Researcher), Agent lập kế hoạch truyền thông (Media Planner), Agent sáng tạo nội dung hình ảnh/văn bản (Visual & Copywriting Agent) và Agent tối ưu hóa SEO tự động.
   * *Hành trình Onboarding 180 ngày tích hợp Agentic AI:* Thiết lập các điểm chạm tương tác liên tục trong 6 tháng đầu đời của khách hàng; nhúng Trợ lý Agentic AI để hỗ trợ giải quyết thắc mắc, tự động đối chiếu giấy tờ và tăng tốc độ kích hoạt tài khoản.
   * *Chiến dịch kích hoạt lại (Win-back):* Tự động lọc danh sách khách hàng ngủ đông (Inactive) theo thời gian và hành vi quá khứ để gửi ưu đãi trúng đích.

2. **Giai đoạn Bán chéo & Thắt chặt Quan hệ (Cross-sell & Relationship Deepening):**
   * *Chương trình khách hàng thân thiết:* Ra mắt chương trình thưởng theo chân dung khách hàng (Cashback chi tiêu, nạp tiền đầu tháng).
   * *Trợ lý AI Hỗ trợ Lực lượng Bán hàng — RM Co-pilot (LLM):* Cung cấp giải pháp huấn luyện tức thì (Instant Coaching), gợi ý kịch bản tư vấn và cung cấp góc nhìn 360 độ về khách hàng cho Relationship Managers (RM) khi đàm phán các sản phẩm phức tạp tại chi nhánh.
   * *Cá nhân hóa tột bậc cho khách hàng trả lương (Payroll - LLM):* Thiết kế các gói tài chính may đo tự động cho khách hàng doanh nghiệp trả lương qua tài khoản.
   * *Bán chéo tự động kích hoạt theo sự kiện (Event-triggered Cross-sell):* Tự động gửi thông báo phê duyệt trước thẻ tín dụng hoặc gói thấu chi ngay trong quá trình khách hàng thực hiện giao dịch thanh toán hàng ngày.
   * *Chiến dịch săn đón tài khoản lương bằng Agentic AI (LLM/Agent):* Hệ thống Agent tự động dò quét luồng thông tin doanh nghiệp, đề xuất gói phúc lợi trả lương và điều phối chiến dịch bán hàng tới các giám đốc nhân sự.
   * *Digital Marketing & Sales War-Room (LLM/Agent):* Xây dựng phòng điều hành kinh doanh số thời gian thực, điều phối thông điệp tiếp thị và đề xuất sản phẩm theo đúng nhu cầu tức thời của khách hàng.

3. **Giai đoạn Giữ chân khách hàng & Phòng ngừa Rời bỏ (Retention):**
   * *Hệ thống cảnh báo sớm (Early Warning Triggers):* Thuật toán tự động phát hiện dấu hiệu khách hàng chuẩn bị chuyển dòng tiền sang ngân hàng khác (giảm số dư bình quân, tất toán sổ tiết kiệm trước hạn) để kích hoạt tái cấu trúc khoản vay hoặc ưu đãi lãi suất tài khoản thanh toán.
   * *Đo lường NPS toàn ngân hàng:* Nhận diện và xóa bỏ có hệ thống các điểm nghẽn gây ức chế trong hành trình số của khách hàng.
   * *Tác tử Giữ chân Chủ động Tự vận hành (Autonomous Proactive Retention AI Agent - LLM/Agent):* Khi phát hiện nguy cơ rời bỏ ở mức cao, AI Agent tự động phân tích lịch sử khách hàng, cấu hình gói giải pháp giữ chân cá nhân hóa (Personalized Win-back Offer) và tự động kích hoạt hành động; nếu khách hàng không phản hồi, Agent sẽ tự động nâng cấp (Escalate) hồ sơ kèm bản tóm tắt nguyên nhân cho chuyên viên tư vấn tiếp quản.

---

## 4. Tái cấu trúc Mô hình Vận hành & Tổ chức Nhân tài AI

### 4.1. Thực trạng cơ cấu tổ chức AI hiện tại

Hiện tại, đơn vị AI của ngân hàng được tổ chức hoàn toàn tập trung bên trong **Khối Công nghệ Thông tin (IT Division)**:

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

**Hạn chế cố hữu của mô hình hiện tại:**
1. **Thiên lệch kỹ thuật (Technically Focused):** Đội ngũ AI tập trung vào các bài toán thuật toán chuyên biệt (Vision, Speech, Bot) nhưng thiếu sự thấu hiểu sâu sắc về ngữ cảnh kinh doanh ngân hàng và không có luồng chuyển giao tri thức hai chiều với các Khối nghiệp vụ.
2. **Trung tâm CoE còn ở giai đoạn sơ khai:** Các nhiệm vụ của CoE hiện chỉ dừng lại ở nghiên cứu thử nghiệm (AI R&D), thiếu năng lực điều phối nhân sự, thiếu cơ chế thu hút nhân tài thực chiến và thiếu thẩm quyền quản trị danh mục dự án AI toàn hàng.

---

### 4.2. Mô hình Vận hành Mục tiêu: Hub-and-Spoke với Delivery Squads

Để giải quyết triệt để sự chia cắt giữa nghiệp vụ và công nghệ, ngân hàng cần chuyển đổi sang mô hình **Hub-and-Spoke**:

<iframe src="/nghien-cuu/ngan-hang-so/mb-technology-and-ai-readiness/assets/01-target-operating-model.html" width="100%" height="680" style="border:none;border-radius:0.75rem;"></iframe>

Mô hình mục tiêu bao gồm hai cấu phần then chốt:

#### A. AI Enablement Hub (Trung tâm Năng lực AI — CoE)
Đóng vai trò là "Bộ não điều phối và Nền tảng dùng chung" toàn ngân hàng:
* **Nuôi dưỡng & Quản trị Nhân tài (Talent & Chapters):** Tổ chức các Chapter chuyên môn (Data Science Chapter, AI Engineering Chapter, Prompt Engineering Chapter, MLOps Chapter) để đào tạo chuẩn hóa kỹ năng và biệt phái nhân lực vào các Squad nghiệp vụ.
* **Cung cấp Công cụ & Nền tảng Dùng chung (Tools & Central Gateway):** Quản lý LLM Gateway tập trung, Thư viện Prompt được phê duyệt trước, Nền tảng Agent Runtime và hạ tầng tính toán (GPU/Cloud).
* **Chuẩn hóa Thực hành Kỹ thuật & Quản trị Rủi ro:** Thiết lập tiêu chuẩn kiến trúc phần mềm AI, quy định an toàn bảo mật mô hình và khung phòng ngừa rủi ro đạo đức.
* **Vận hành Cổng Kiểm soát "Approval to Build":** Quy trình thẩm định độc lập bắt buộc trước khi bắt đầu lập trình bất kỳ dự án AI nào. Đề bài chỉ được duyệt khi đáp ứng đủ 3 tiêu chí:
  1. *Tính sẵn sàng của dữ liệu (Data Readiness):* Đã có tập dữ liệu sạch, có bản đồ trường thông tin và quyền truy cập hợp lệ.
  2. *Kiểm soát rủi ro & tuân thủ (Risk Checks):* Đã được Khối Pháp chế, Khối Rủi ro và An toàn Thông tin (ISO) thông qua cơ chế kiểm soát rủi ro và bảo vệ quyền riêng tư.
  3. *Cam kết bảo trợ nghiệp vụ (Business Sponsorship & PBT Case):* Có Lãnh đạo nghiệp vụ đứng tên bảo trợ, cam kết chịu trách nhiệm về chỉ tiêu PBT và kế hoạch quản trị thay đổi người dùng.

#### B. AI Delivery Squads (Đội Triển khai Đa chức năng theo Domain)
Các đội ngũ linh hoạt được thành lập riêng cho từng Domain nghiệp vụ (ví dụ: Squad Khách hàng Bán lẻ, Squad Tín dụng, Squad Contact Center):
* **Cơ cấu nhân sự đa ngành trong 1 Squad:**
  * **Product Owner (PO):** Nhân sự thuộc Khối nghiệp vụ, sở hữu bài toán kinh doanh, chịu trách nhiệm về chỉ tiêu PBT và mức độ tiếp nhận của người dùng cuối.
  * **Business Analyst (BA) & Process Engineer:** Phân tích quy trình nghiệp vụ hiện tại, tái thiết kế luồng quy trình đầu-cuối để nhúng AI.
  * **AI–Business Translator:** Vai trò then chốt chuyển hóa bài toán nghiệp vụ thành đặc tả kỹ thuật AI và diễn giải kết quả mô hình cho nghiệp vụ hiểu.
  * **Data Scientist & Data/AI Engineer:** Phát triển mô hình, xây dựng pipeline xử lý dữ liệu và tích hợp API.
  * **AI Solution Architect & Software Engineer:** Thiết kế kiến trúc giải pháp, tích hợp vào hệ thống ngân hàng lõi (Core Banking) và các kênh số.
  * **UX/UI Designer:** Thiết kế giao diện tương tác trực quan, tối ưu trải nghiệm con người cộng tác cùng AI (Human-AI Collaboration).
* **Năng lực nhúng từ Khối Hỗ trợ:**
  * *Hạ tầng (Infrastructure):* Cấp phát tài nguyên tính toán, đường truyền và môi trường an toàn.
  * *Bảo mật (Embedded Security):* Quét lỗ hổng, phân quyền truy cập dữ liệu và thiết lập các lớp tường lửa AI (Guardrails).

---

## 5. Phân tích Chuyên sâu Vòng đời Phát triển AI: Bài học từ Credit Memo AI

Khảo sát thực tế vòng đời triển khai giải pháp **AI Credit Memo** (Hệ thống AI lập tờ trình thẩm định tín dụng tự động) phản ánh chân thực những vấn đề cố hữu trong phương thức phát triển AI hiện tại:

<iframe src="/nghien-cuu/ngan-hang-so/mb-technology-and-ai-readiness/assets/02-ai-delivery-lifecycle.html" width="100%" height="700" style="border:none;border-radius:0.75rem;"></iframe>

### So sánh Chi tiết 5 Giai đoạn Triển khai: Thực trạng vs Khoảng cách vs Chuẩn hóa

| Giai đoạn vòng đời | Thực trạng triển khai tại MB (Current Practice) | Khoảng cách cốt lõi phát hiện (Gaps Identified) | Khung chuẩn hóa mục tiêu (Target AI Framework) |
|---|---|---|---|
| **1. Khởi tạo & Định vị (Ideation & Scoping)** | • Vấn đề được thảo luận giữa Lãnh đạo cấp cao (Chairman) và Khối nghiệp vụ.<br>• Yêu cầu kinh doanh được bàn giao cho IT đánh giá tính khả thi.<br>• IT tự lập kế hoạch triển khai use case. | • **Thiếu Squad đa chức năng ngay từ Ngày đầu (Day 1)** để đồng bộ giữa bài toán kinh doanh, tiêu chí rủi ro và khả năng công nghệ.<br>• **Không xây dựng Business Case và ROI tài chính đầy đủ**; không gắn với chỉ tiêu PBT cụ thể. | **Đồng thiết kế Đa chức năng (Cross-Functional Co-design):**<br>PO Nghiệp vụ, Kiến trúc sư AI và Chuyên gia Rủi ro cùng ngồi lại thiết lập Business Case, xác định ranh giới rủi ro và chỉ tiêu PBT trước khi đưa qua cổng "Approval to Build". |
| **2. Dữ liệu & Thử nghiệm (Intelligence & Prototyping)** | • Thử nghiệm nhiều mô hình LLM khác nhau; lựa chọn mô hình Google Gemini dựa trên độ chính xác vượt trội.<br>• Sử dụng các tập tài liệu mẫu rời rạc do đơn vị nghiệp vụ cung cấp để kiểm tra kết quả. | • **Thiếu một "Tập Dữ liệu Vàng" (Golden Dataset) chuẩn mực** gồm đầy đủ các mẫu hồ sơ vay từ đơn giản đến cực kỳ phức tạp để đo lường độ chính xác và nguy cơ ảo giác (Hallucination). | **Xây dựng Golden Dataset Benchmark:**<br>Thành lập bộ kiểm thử chuẩn mực được nghiệp vụ và rủi ro phê duyệt; thiết lập pipeline tự động đánh giá độ chính xác, tỷ lệ ảo giác và khả năng trích xuất trên nhiều văn bản phức tạp. |
| **3. Xây dựng MVP (Inception & MVP Build)** | • Thiết kế quy trình E2E, trường thông tin và định dạng dữ liệu bằng cách gửi bảng khảo sát cho các đơn vị kinh doanh.<br>• Lập trình viên tự liên hệ lẻ tẻ với cán bộ nghiệp vụ khi gặp vướng mắc. | • **Thiếu đội ngũ đồng thiết kế theo thời gian thực (Real-time Co-design)**.<br>• **Chưa xây dựng cơ chế Human-in-the-Loop (HITL) có cấu trúc** để tự động điều hướng dữ liệu có độ tin cậy thấp đến chuyên viên tín dụng xác minh. | **Quy trình Realtime Co-design & HITL:**<br>Lập trình viên và cán bộ nghiệp vụ ngồi làm việc chung (Pairing); tích hợp cơ chế HITL tự động gắn cờ các trường thông tin có độ tin cậy thấp (Low Confidence) và chuyển trực tiếp cho RM phê duyệt nhanh. |
| **4. Thử nghiệm (Pilot & Validation)** | • Bắt đầu triển khai thử nghiệm theo từng đợt, khởi động với sản phẩm Cho vay Thế chấp nhà ở (Mortgage). | • **Thiếu thiết kế thử nghiệm có kiểm soát (Controlled Pilot / A/B Testing)**.<br>• **Không đo lường các chỉ số kinh doanh thực tế** (như số giờ thực tế tiết kiệm được trên mỗi tờ trình), chỉ đo các chỉ số kỹ thuật của mô hình. | **Thử nghiệm Có kiểm soát & Đo lường Chỉ số Cứng:**<br>Thiết kế nhóm đối chứng (Control Group) so sánh với nhóm dùng AI; đo lường trực tiếp số giờ tiết kiệm thực tế, thời gian quay vòng hồ sơ (Turnaround Time) và tỷ lệ chấp thuận hồ sơ. |
| **5. Mở rộng & Tự chủ (Independence & Scale)** | • Mở rộng giải pháp trên toàn bộ hệ thống cho vay Bán lẻ (Retail) và Doanh nghiệp (Corporate).<br>• Chuẩn bị triển khai cho vay Mua ô tô (Auto Loan) và Vay kinh doanh. | • **Chưa xây dựng quy trình kiểm thử hồi quy (Regression Testing)** khi cập nhật mô hình.<br>• **Hoàn toàn thiếu cơ chế giám sát độ trôi dữ liệu (Data/Model Drift)** và vòng lặp đóng (Closed-loop) để liên tục tái huấn luyện mô hình. | **Tự động hóa MLOps & Quản trị Độ trôi:**<br>Thiết lập hệ thống quan sát mô hình (Model Observability) liên tục phát hiện trôi dữ liệu; tự động chạy kiểm thử hồi quy trước mỗi bản cập nhật; thu thập phản hồi của RM để đóng vòng cải tiến mô hình. |

---

## 6. Đánh giá Hạ tầng Dữ liệu, DataOps và MLOps Nền tảng

Đánh giá chi tiết **19 thành phần năng lực dữ liệu phục vụ AI** được chia thành 4 tầng kiến trúc chuỗi giá trị và 4 trụ cột vận hành:

<iframe src="/nghien-cuu/ngan-hang-so/mb-technology-and-ai-readiness/assets/03-data-and-mlops-readiness.html" width="100%" height="700" style="border:none;border-radius:0.75rem;"></iframe>

### Bảng Đánh giá Chi tiết 19 Thành phần Dữ liệu & MLOps

| STT | Thành phần năng lực | Tầng kiến trúc | Xếp hạng trưởng thành | Hiện trạng thực tế tại MBBank |
|---|---|---|---|---|
| 1 | **Nguồn Dữ liệu (Sources - Nội bộ & Bên ngoài)** | Thu thập (Provisioning) | **Vừa (Medium)** | Dữ liệu then chốt đã được định danh và truy cập được; tuy nhiên chưa mở rộng khả năng tự phục vụ (Self-service access) cho các nhóm AI. |
| 2 | **DataOps & MLOps Pipeline** | Trụ cột Hỗ trợ (Enabler) | **THẤP (Low)** | **Nghẽn nghiêm trọng:** Công tác dán nhãn, làm sạch và chuẩn bị dữ liệu hầu như làm thủ công; tồn tại độ lệch lớn (mismatch) giữa môi trường thử nghiệm và sản xuất. |
| 3 | **Chất lượng Dữ liệu (Data Quality)** | Trụ cột Hỗ trợ (Enabler) | **Vừa (Medium)** | Có các đợt kiểm tra dữ liệu định kỳ, nhưng thiếu quy chuẩn tự động để giám sát liên tục, cảnh báo sớm và quy trình giải quyết sự cố dữ liệu. |
| 4 | **An toàn Thông tin (Information Security)** | Trụ cột Hỗ trợ (Enabler) | **Vừa (Medium)** | Các biện pháp kiểm soát chuẩn mực đã được áp dụng cho dữ liệu trọng yếu, nhưng chưa được nhúng đồng bộ xuyên suốt các nền tảng AI mới. |
| 5 | **Hạ tầng Dữ liệu (Data Infrastructure)** | Trụ cột Hỗ trợ (Enabler) | **Vừa (Medium)** | Đáp ứng tốt nhu cầu tính toán và lưu trữ hiện tại, nhưng chưa được kiểm thử chịu tải khi số lượng bài toán AI mở rộng quy mô lớn. |
| 6 | **Mô hình Vận hành Dữ liệu (Data Operating Model)** | Trụ cột Hỗ trợ (Enabler) | **THẤP (Low)** | **Quyền sở hữu dữ liệu không rõ ràng**; xuất hiện nhiều dự án thử nghiệm (PoC) tự phát, thiếu cơ chế quản trị và phân quyền tập trung. |
| 7 | **Tích hợp Dữ liệu (Integration)** | Lưu trữ (Aggregation) | **Vừa (Medium)** | Đã xây dựng các kết nối chuẩn mực đối với các hệ thống CNTT cốt lõi của ngân hàng. |
| 8 | **Miền Dữ liệu (Data Domains)** | Lưu trữ (Aggregation) | **THẤP (Low)** | **Dữ liệu vẫn bị gom theo các kho kỹ thuật vật lý (Data Stores)** thay vì tổ chức thành các Domain nghiệp vụ có gán người chịu trách nhiệm (Data Domain Owners). |
| 9 | **Quản trị Dữ liệu Chủ (MDM - Master Data)** | Lưu trữ (Aggregation) | **Vừa (Medium)** | Đã định danh khách hàng duy nhất (Common Customer ID) trên các hệ thống core; tuy nhiên dữ liệu từ các công ty con (Subsidiaries) chưa được đồng bộ. |
| 10 | **Kho Lưu trữ (Repositories - Data Lake/Warehouse)** | Lưu trữ (Aggregation) | **Vừa (Medium)** | Dữ liệu cốt lõi đã được gom tụ về Kho dữ liệu và Hồ dữ liệu tập trung (Data Lake). |
| 11 | **Sản phẩm Dữ liệu (Data Products)** | Lưu trữ (Aggregation) | **Vừa (Medium)** | Một số logic xử lý nghiệp vụ đã được xây dựng sẵn thành các bảng phân tích, nhưng chưa đóng gói hoàn chỉnh thành Data API. |
| 12 | **Cổng Phân phối & API (Distribution & Endpoints)** | Phân phối (Consumption) | **CAO (High)** | **Điểm sáng vượt trội:** Hệ sinh thái API nội bộ phát triển mạnh mẽ, sẵn sàng phân phối dữ liệu cho các ứng dụng tiêu thụ. |
| 13 | **Năng lực Tiêu thụ Dữ liệu (Consumption)** | Phân phối (Consumption) | **Vừa (Medium)** | Phần lớn các phòng ban nghiệp vụ có thể truy cập tự do vào các điểm dữ liệu cốt lõi để lập báo cáo. |
| 14 | **Ứng dụng May đo Tùy biến (Custom Applications)** | Ứng dụng (Applications) | **THẤP (Low)** | Thiếu các bộ công cụ dữ liệu đóng gói sẵn để các đội ngũ phát triển nhanh các ứng dụng AI chuyên biệt cho từng phòng ban. |
| 15 | **Ứng dụng Cốt lõi (Core Applications)** | Ứng dụng (Applications) | **Vừa (Medium)** | Giao diện chuẩn mực giữa các ứng dụng lõi được duy trì ổn định. |
| 16 | **Cơ chế Ưu tiên Đề tài Dữ liệu (Data Priority Model)** | Quản trị Vận hành | **THẤP (Low)** | **Ưu tiên phụ thuộc vào yêu cầu vụ việc của từng cá nhân/đơn vị**, thiếu một lộ trình chiến lược có trọng tâm về giá trị kinh doanh. |
| 17 | **Quản trị Kiến trúc Dữ liệu (Architecture Governance)** | Quản trị Vận hành | **Vừa (Medium)** | Tiêu chuẩn kiến trúc chung đã được ban hành, nhưng vẫn còn nhiều ngoại lệ kỹ thuật chưa được xử lý triệt để. |
| 18 | **Nhân sự, Nguồn lực & Văn hóa (Talent & Resourcing)** | Quản trị Vận hành | **THẤP (Low)** | **Khoảng cách lớn về kỹ năng và dung lượng nhân sự:** Rất thiếu hụt Kỹ sư Dữ liệu (Data Engineers), Kỹ sư MLOps và Chuyên gia AI. |
| 19 | **Chỉ số Đo lường Dữ liệu (Data Metrics)** | Quản trị Vận hành | **Vừa (Medium)** | Có đo lường các chỉ số kỹ thuật về chất lượng dữ liệu, nhưng **hoàn toàn chưa có bộ chỉ số toàn hàng đo lường mức độ tái sử dụng dữ liệu và tác động tài chính**. |

---

## 7. Báo cáo Kiểm toán Thực tế 11 AI Use Cases tại MBBank

Đánh giá thực trạng vận hành, chỉ số đo lường và rào cản kỹ thuật của toàn bộ 11 giải pháp AI đã triển khai tại ngân hàng:

```
                  DANH MỤC 11 AI USE CASES TẠI MBBANK
 ┌──────────────────────┬──────────────────────┬──────────────────────┐
 │    CONTACT CENTER    │  SUPPORT & NỘI BỘ    │ ACQUISITION / LENDING│
 ├──────────────────────┼──────────────────────┼──────────────────────┤
 │1. AI Customer (Pilot)│4. AI for IT (Launch) │8. AI Telesales (STOP)│
 │2. AI Paste2Pay (L)   │5. AI Enterprise (L)  │9. AI Credit Score (L)│
 │3. AI SmartSearch (L) │6. AI Fraud (Launch)  │10. AI Credit Memo (L)│
 │                      │7. AI Mentor (STOP)   │11. AI Beerich (L)    │
 └──────────────────────┴──────────────────────┴──────────────────────┘
```

| STT | Tên Use Case | Miền nghiệp vụ | Trạng thái | Chỉ số đo lường hiện tại (Impact Metric) | Quy mô lưu lượng thực tế | Rào cản & Thách thức vận hành cốt lõi |
|---|---|---|---|---|---|---|
| 1 | **AI Customer** | Contact Center | Thử nghiệm (Pilot) | Thời gian xử lý thủ công (Manual processing time) | Đang thử nghiệm | • **Chất lượng không ổn định:** Hiệu năng trả lời dao động mạnh tùy theo chủ đề và độ phức tạp của câu hỏi.<br>• **Định tuyến chưa trọn vẹn:** Yêu cầu của khách hàng không được điều hướng chính xác đến nguồn dữ liệu hoặc chuyên gia phù hợp. |
| 2 | **AI Paste2Pay** | Contact Center | Vận hành (Launched) | Số lượng giao dịch xử lý/ngày (# of requests/day) | Đã Golive thực tế | • **Thách thức trích xuất dữ liệu đa phương thức:** Khách hàng dán thông tin thanh toán dưới nhiều định dạng tự do phức tạp, gây khó khăn cho khâu bóc tách và điều phối giao dịch. |
| 3 | **AI SmartSearch** | Contact Center | Vận hành (Launched) | Số lượng lượt tìm kiếm (# of queries) | **200.000 – 300.000 lượt/ngày** | • Hoạt động ổn định ở lưu lượng rất cao, không gặp rào cản kỹ thuật lớn. |
| 4 | **AI for IT** | Hỗ trợ CNTT (IT Support) | Vận hành (Launched) | Thời gian lập trình và kiểm thử (Dev & test time) | Nội bộ Khối CNTT | • **Chưa có khung quản trị AI (AI Governance undefined):** Thiếu cơ chế kiểm soát mã nguồn sinh ra bởi AI, thiếu quy định trách nhiệm giải trình và tiêu chuẩn rà quét an toàn bảo mật. |
| 5 | **AI Enterprise** | Hỗ trợ Vận hành (Support) | Vận hành (Launched) | Số lượng lượt truy vấn (No. of queries) | ~3.000 lượt/ngày (trong 2 tuần đầu) | • **Yếu kém khi xử lý câu hỏi phức tạp:** Mô hình không duy trì được ngữ cảnh xuyên suốt giữa các lượt hội thoại (Multi-turn context).<br>• **Lệch pha nhu cầu:** ~70% lượng truy vấn tập trung cục bộ vào mảng Tín dụng (Credit), các khối khác ít sử dụng. |
| 6 | **AI Fraud** | Hỗ trợ Rủi ro (Risk Support) | Vận hành (Launched) | Số lượng hồ sơ gian lận được phân tích (Fraud case analysis) | **Triển khai diện rộng trên App, Biz và Cards** | • Triển khai thành công nhất ngân hàng, quy mô lớn, vận hành ổn định không phát sinh điểm nghẽn nghiêm trọng. |
| 7 | **AI Mentor** | Hỗ trợ Nhân sự (HR Support) | **DỪNG TRIỂN KHAI (Discontinued)** | Không có (N/A) | Đã tắt hệ thống | • **Tỷ lệ nhân viên sử dụng quá thấp:** Trải nghiệm không thiết thực, nhân viên không thấy động lực sử dụng công cụ hàng ngày. |
| 8 | **AI Telesales** | Thu hút Khách hàng (Acquisition) | **DỪNG TRIỂN KHAI (Discontinued)** | Không có (N/A) | Đã tắt hệ thống | • **Khách hàng phản ứng tiêu cực:** Tỷ lệ không hài lòng rất cao do kịch bản gọi tự động thiếu tự nhiên và gây phiền hà.<br>• **Tỷ lệ chuyển đổi kinh doanh cực thấp:** Gần như không đem lại giá trị doanh thu bù đắp chi phí vận hành. |
| 9 | **AI Credit Scoring** | Bán chéo & Thu hút (X-Sell) | Vận hành (Launched) | Tỷ lệ chuyển đổi khách hàng tiềm năng (Lead conversion) | Vận hành trên luồng cấp tín dụng số | • **Tỷ lệ chuyển đổi thực tế rất hạn chế:** Chỉ đạt ~5% đối với Thẻ tín dụng cao cấp (Affluent Cards), ~0.2% đối với Vay tín chấp cao cấp (Affluent USL) và ~13% đối với hạn mức Doanh nghiệp vừa và nhỏ (SME).<br>• **Thiếu quản trị tác động mô hình đầu-cuối:** Chuyển đổi, doanh thu thực thu và tỷ lệ nợ xấu (Risk) chưa được gắn kết theo dõi cùng nhau. |
| 10 | **AI Credit Memo** | Hậu sảnh Tín dụng (Middle-Office) | Vận hành (Launched) | Thời gian xử lý tờ trình (Processing time) | Áp dụng trên gói Cho vay Thế chấp Bán lẻ và KHDN | • **Đo lường tác động chưa đầy đủ:** Mặc dù ghi nhận hiệu quả giảm giờ làm kỹ thuật của chuyên viên, nhưng giá trị đóng góp vào PBT của module thẩm định tín dụng mới vẫn chưa được lượng hóa độc lập. |
| 11 | **AI Beerich** | Hậu sảnh (Middle-Office) | Vận hành (Launched) | Độ chính xác phân loại giao dịch (Accuracy) | Vận hành thực tế | • **Chất lượng dữ liệu đầu vào kém:** Khi xử lý khối lượng giao dịch cực lớn, hệ thống buộc phải lùi về sử dụng các tập quy tắc tĩnh (Rule-based) thay vì dùng mô hình AI do dữ liệu giao dịch bị nhiễu. |

---

## 8. Bốn Quy luật Thất bại Điển hình và Bài học Kiến trúc

Từ việc mổ xẻ 11 use cases, rút ra 4 nguyên nhân gốc rễ dẫn đến thất bại hoặc tắc nghẽn của các dự án AI ngân hàng:

```
                    4 NGUYÊN NHÂN GỐC RỄ GÂY NGHẼN AI
 ┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
 │    BẪY CHỈ SỐ        │   SỤP ĐỔ DO DỮ LIỆU  │   TRẢI NGHIỆM KÉM    │  CÔ LẬP VẬN HÀNH     │
 │   (Metric Trap)      │  (Data Dirt Trap)    │   (UX & Change Gap)  │  (Isolated Island)   │
 ├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
 │Chỉ đo chỉ số kỹ thuật│Dữ liệu gốc nhiễu,    │Kịch bản cứng nhắc    │AI nằm riêng trong IT,│
 │(queries, dev-time)   │thiếu chuẩn hóa buộc  │(AI Telesales) hoặc   │thiếu gắn kết với quy │
 │mà không gắn với PBT  │phải lùi về rule-base │không thiết thực      │trình thực tế của RM  │
 │và doanh thu ròng.    │tĩnh (AI Beerich).    │khiến user rời bỏ.    │tại chi nhánh.        │
 └──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

1. **Bẫy Chỉ số Kỹ thuật (The Technical Metric Trap):**  
   Hầu hết các dự án chỉ theo dõi các chỉ số hoạt động (Activity Metrics) như số lượt query, thời gian xử lý của mô hình, số dòng code sinh ra... mà không gắn với **Chỉ số Giá trị Kinh doanh Cứng (Hard Business Outcomes)**. Khi Lãnh đạo cấp cao hỏi: *"Giải pháp AI này đóng góp bao nhiêu tỷ đồng vào PBT quý này?"*, các đội ngũ dự án hoàn toàn lúng túng. Điều này giải thích vì sao các dự án như AI Telesales hay AI Mentor nhanh chóng bị dừng cấp vốn khi ngân hàng rà soát hiệu quả đầu tư.
2. **Sụp đổ do Dữ liệu Bẩn (The Data Dirt Trap):**  
   Trường hợp của **AI Beerich** là minh chứng điển hình: Một mô hình Machine Learning hiện đại dù được tinh chỉnh tinh vi đến đâu cũng sẽ trở nên vô dụng nếu dữ liệu giao dịch đầu vào bị phân mảnh, thiếu định danh chuẩn và chất lượng kém. Việc thiếu vắng tầng DataOps tự động hóa buộc kỹ sư phải "vá víu" bằng các tập luật tĩnh (Hardcoded Rules), làm mất đi hoàn toàn lợi thế linh hoạt của AI.
3. **Thất bại do Trải nghiệm & Quản trị Thay đổi (UX & Change Management Failure):**  
   **AI Telesales** thất bại vì áp đặt công nghệ tự động một cách máy móc lên khách hàng mà không thấu hiểu tâm lý hành vi, dẫn đến việc bị khách hàng coi là tin rác (Spam) và gây tổn hại đến hình ảnh thương hiệu. Tương tự, **AI Mentor** thất bại vì không được tích hợp mượt mà vào luồng làm việc tự nhiên của nhân viên, dẫn đến việc bị lãng quên sau đợt phát động ban đầu.
4. **Hòn đảo Cô lập giữa IT và Nghiệp vụ (The Siloed Tech Island):**  
   Tại giải pháp **AI Credit Memo**, lập trình viên phải tự mình đi khảo sát và gõ cửa từng phòng ban để hỏi cấu trúc tài liệu vay. Việc thiếu vắng vai trò Cầu nối (AI Translator) và cơ chế làm việc chung thời gian thực (Realtime Co-design) khiến thời gian xây dựng MVP bị kéo dài gấp đôi và giải pháp khi đưa ra không khớp hoàn toàn với thực tiễn phê duyệt tín dụng của RM.

---

## 9. Khuyến nghị Kiến trúc & Lộ trình Thực thi

Để nâng tầm năng lực AI và đưa ngân hàng trở thành tổ chức vận hành dựa trên AI (AI-Rewired Bank), ngân hàng cần triển khai ngay 4 sáng kiến chiến lược:

```
                     LỘ TRÌNH 4 HÀNH ĐỘNG CHIẾN LƯỢC
 ┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
 │1. TÁI CẤU TRÚC ĐỘI   │2. HẠ TẦNG DÙNG CHUNG │3. DATA MESH & DOMAIN │4. QUẢN TRỊ & PBT     │
 │(Domain AI Pods)      │(LLM Gateway & Tools) │(Domain Data Products)│(Approval to Build)   │
 ├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
 │Chuyển từ team IT tập │Xây dựng LLM Gateway, │Chuyển đổi dữ liệu hồ │Thiết lập cổng kiểm   │
 │trung sang các Squad  │Prompt Catalog, Golden│thành các Data Product│soát, bắt buộc chỉ    │
 │đa chức năng gắn chặt │Dataset Benchmark và  │có Domain Owner rõ    │tiêu PBT và đo lường  │
 │với Domain nghiệp vụ. │Eval Harness toàn hàng│ràng, tự động DataOps │Adoption KPIs hàng quý│
 └──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

### 1. Tái cơ cấu Tổ chức theo mô hình Domain AI Pods
* Giải thể cơ cấu phát triển AI cô lập trong IT; thành lập các **AI Delivery Squads đa chức năng** cắm thẳng vào các Domain kinh doanh trọng điểm (Bán lẻ, Tín dụng Doanh nghiệp, Contact Center).
* Tuyển dụng và đào tạo đội ngũ **AI–Business Translators** để làm cầu nối ngôn ngữ giữa lãnh đạo nghiệp vụ và kỹ sư thuật toán.
* Trao quyền sở hữu bài toán và quyền quyết định backlog AI cho Product Owner nghiệp vụ.

### 2. Thiết lập Hạ tầng AI Nền tảng Dùng chung (AI Foundation)
* Xây dựng **Cổng định tuyến LLM Gateway tập trung**: Quản lý hạn ngạch (Rate Limit), cân bằng tải giữa các mô hình (OpenAI, Gemini, Local Open-source Models), chuẩn hóa định dạng dữ liệu và kiểm soát chi phí Token toàn ngân hàng.
* Thiết lập **Thư viện Gợi ý Chuẩn hóa (Prompt Catalog & Registry)** có kiểm soát phiên bản (Versioning) và quy trình phê duyệt an toàn.
* Chuẩn hóa **Hạ tầng Đánh giá (Eval Harness)** và xây dựng các **Tập Dữ liệu Vàng (Golden Datasets)** chuyên biệt cho từng nghiệp vụ ngân hàng để kiểm thử tự động trước khi triển khai.

### 3. Chuyển dịch Kiến trúc Dữ liệu sang Data Mesh & Data Products
* Xóa bỏ các kho dữ liệu cô lập kỹ thuật; tổ chức dữ liệu theo **Domain Nghiệp vụ (Data Domains)** và chỉ định rõ **Chủ sở hữu Dữ liệu (Data Owner)** chịu trách nhiệm về chất lượng dữ liệu của khối mình.
* Đóng gói dữ liệu thành các **Sản phẩm Dữ liệu (Data Products)** có tài liệu hướng dẫn, SLA chất lượng và API phân phối mở cho các nhóm AI dễ dàng tiêu thụ.
* Đầu tư mạnh mẽ vào **DataOps/MLOps Pipeline**: Tự động hóa khâu tiền xử lý, dán nhãn dữ liệu và giám sát độ trôi mô hình (Model Drift) trong môi trường sản xuất.

### 4. Thể chế hóa Khung Quản trị AI & Chỉ số Đo lường PBT
* Đưa vào vận hành cổng kiểm soát **"Approval to Build"**: Kiên quyết từ chối cấp phát tài nguyên cho các dự án AI phong trào, thiếu cam kết bảo trợ nghiệp vụ hoặc không chứng minh được tính sẵn sàng của dữ liệu.
* Thay thế toàn bộ các chỉ số đo lường hình thức bằng **Hệ thống Đo lường Tác động Tài chính (PBT Value Framework)**: Mỗi use case khi nghiệm thu phải chứng minh được giá trị doanh thu tăng thêm hoặc chi phí giờ làm tiết kiệm được quy đổi thành tiền.
* Thiết lập bộ chỉ số **Adoption KPIs** theo dõi tần suất nhân viên sử dụng AI hàng ngày và tỷ lệ luồng công việc được tự động hóa thực chất.

---

## 10. Bảng Thuật ngữ Kỹ thuật & Nghiệp vụ (Bilingual Glossary)

| Thuật ngữ Tiếng Anh | Nghĩa Tiếng Việt / Chú giải bối cảnh |
|---|---|
| **AI Adoption** | Mức độ ứng dụng và thẩm thấu AI vào quy trình nghiệp vụ thực tế của ngân hàng. |
| **AI–Business Translator** | Cầu nối dịch thuật nghiệp vụ – công nghệ; nhân sự hiểu sâu nghiệp vụ ngân hàng và năng lực AI để thiết kế use case. |
| **AI Delivery Squad** | Đội ngũ triển khai AI đa chức năng, gắn trực tiếp với một miền nghiệp vụ (Domain). |
| **AI Enablement Hub (CoE)** | Trung tâm năng lực AI tập trung; cơ quan quản trị nền tảng, công cụ, tiêu chuẩn và nhân tài AI. |
| **Agentic AI** | Trí tuệ nhân tạo tác tử tự chủ; có khả năng lập kế hoạch, sử dụng công cụ và tự động ra quyết định theo mục tiêu. |
| **Approval to Build Gate** | Cổng kiểm soát phê duyệt phát triển; rào chắn thẩm định dữ liệu, rủi ro và cam kết nghiệp vụ trước khi code. |
| **Controlled Pilot (A/B Testing)** | Thử nghiệm có kiểm soát; phương pháp đo lường so sánh giữa nhóm ứng dụng AI và nhóm đối chứng truyền thống. |
| **Credit Memo** | Tờ trình thẩm định tín dụng; văn bản tổng hợp đánh giá rủi ro và đề xuất hạn mức cấp tín dụng cho khách hàng. |
| **Data Domain** | Miền dữ liệu nghiệp vụ; ranh giới dữ liệu thuộc quyền sở hữu và quản trị của một khối chức năng cụ thể. |
| **Data Product** | Sản phẩm dữ liệu; dữ liệu đã được làm sạch, đóng gói kèm logic nghiệp vụ và phân phối qua API chuẩn. |
| **DataOps / MLOps** | Quy trình kỹ thuật tự động hóa chu kỳ phát triển, kiểm thử, triển khai và giám sát dữ liệu / mô hình học máy. |
| **End-to-End (E2E) Transformation** | Chuyển đổi toàn diện đầu-cuối; tái thiết kế trọn vẹn cả chuỗi quy trình thay vì số hóa từng khâu lẻ tẻ. |
| **Golden Dataset** | Tập dữ liệu vàng; bộ dữ liệu chuẩn mực đa dạng được gán nhãn chính xác dùng để đánh giá và benchmark mô hình. |
| **Human-in-the-Loop (HITL)** | Quy trình kiểm soát có con người can thiệp; tự động định tuyến các kết quả AI có độ tin cậy thấp cho chuyên viên duyệt. |
| **LLM Gateway** | Cổng điều phối mô hình ngôn ngữ lớn; hạ tầng trung gian quản lý định tuyến, cân bằng tải, hạn ngạch và chi phí Token. |
| **Model Drift** | Hiện tượng trôi mô hình; sự suy giảm độ chính xác của mô hình AI theo thời gian do dữ liệu thực tế thay đổi. |
| **Profit Before Tax (PBT)** | Lợi nhuận trước thuế; chỉ số tài chính tối hậu dùng để đánh giá hiệu quả kinh tế thực tế của các giải pháp AI. |
| **Prompt Library / Catalog** | Bộ lưu trữ và quản lý mẫu gợi ý chuẩn hóa; thư viện prompt được kiểm duyệt phiên bản và độ an toàn. |
| **Relationship Manager (RM)** | Chuyên viên quản lý quan hệ khách hàng; cán bộ kinh doanh trực tiếp tư vấn và quản lý danh mục khách hàng. |
| **Turnaround Time (TAT)** | Thời gian quay vòng xử lý; tổng thời gian từ lúc tiếp nhận yêu cầu đến khi bàn giao kết quả cuối cùng. |
| **Use Case Silos / Fragmentation** | Tình trạng triển khai use case manh mún, cục bộ; các giải pháp AI rời rạc không có sự kết nối và cộng hưởng. |

---

## 11. Quy ước Cấu trúc Thư mục

Bài nghiên cứu này được lưu trữ theo quy chuẩn cấu trúc 2 tầng của Kho Tri thức:

```text
nghien-cuu/
└── ngan-hang-so/
    └── mb-technology-and-ai-readiness/
        ├── index.md                                        # Bản nghiên cứu toàn văn
        ├── assets/                                         # Mã nguồn sơ đồ JSON & bản HTML kết xuất
        │   ├── 01-target-operating-model.workflow.json
        │   ├── 01-target-operating-model.html
        │   ├── 02-ai-delivery-lifecycle.workflow.json
        │   ├── 02-ai-delivery-lifecycle.html
        │   ├── 03-data-and-mlops-readiness.workflow.json
        │   └── 03-data-and-mlops-readiness.html
        └── evidence/                                       # Dữ liệu nguồn và hồ sơ kiểm toán đối chiếu
            ├── slide-summary.txt
            ├── 11-use-cases-audit.json
            └── 19-data-elements-assessment.json
```
