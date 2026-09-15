# Factor 5: Unify execution state and business state (Hợp nhất Trạng thái Thực thi và Trạng thái Nghiệp vụ)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-05-unify-execution-state.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-05-unify-execution-state.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Trong kỹ nghệ phần mềm truyền thống, nhiều hệ sinh thái hạ tầng cố tình phân tách rạch ròi giữa **Execution State (Trạng thái Thực thi/Vận hành)** và **Business State (Trạng thái Nghiệp vụ)**. Đối với các hệ thống AI Agent, sự phân tách này thường kéo theo hàng loạt tầng trừu tượng phức tạp để theo dõi bước hiện tại (step pointer), bước tiếp theo, trạng thái chờ (waiting/suspended), số lần retry, v.v. Việc tách đôi trạng thái tạo ra sự phức tạp lớn về đồng bộ dữ liệu (State Synchronization Overhead) mà trong đa số trường hợp là **hoàn toàn dư thừa (Accidental Complexity)**.

`[Dịch]` Dưới góc độ thiết kế giải pháp:

- **Execution State (Trạng thái Thực thi):** Con trỏ bước hiện tại, trạng thái chờ tín hiệu (suspended/blocked), số lần thử lại (retry count), thông tin orchestrator worker, v.v.
- **Business State (Trạng thái Nghiệp vụ):** Toàn bộ lịch sử chuỗi hành động và dữ liệu đã diễn ra trong phiên làm việc của Agent (danh sách tin nhắn, lệnh gọi tool, kết quả phản hồi từ API, phản hồi của người dùng).

`[Dịch]` Khuyến nghị kiến trúc cốt lõi: **HÃY HỢP NHẤT (UNIFY) HAI TRẠNG THÁI NÀY LÀM MỘT.**

[![Gộp execution state và business state](/nghien-cuu/agents/12-factor-agents/assets/img/155-unify-state-animation.gif)](https://github.com/user-attachments/assets/e5a851db-f58f-43d8-8b0c-1926c99fc68d)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/155-unify-state-animation.gif">Xem bản ảnh động GIF</a></summary>

![Gộp execution state và business state](/nghien-cuu/agents/12-factor-agents/assets/img/155-unify-state-animation.gif)

</details>

`[Dịch]` Trong thực tế, bạn hoàn toàn có thể thiết kế hệ thống theo mô hình **Event Sourcing**, trong đó **toàn bộ Execution State có thể được suy luận (derived) trực tiếp từ chuỗi sự kiện trong Context Window / Thread History**. Bản thân các trạng thái vận hành (đang chờ phê duyệt, vừa gặp lỗi cần retry, đã hoàn tất) thực chất chỉ là phép chiếu (projection/metadata) từ chuỗi sự kiện đã xảy ra từ trước tới nay.

`[Dịch]` Tất nhiên, hệ thống vẫn có thể có một số metadata nhạy cảm hoặc kỹ thuật không nên gửi trực tiếp cho LLM (như `session_id`, database transaction lock, credentials). Tuy nhiên, nguyên tắc kiến trúc là **tối thiểu hóa tối đa các biến trạng thái nằm ngoài luồng sự kiện chính**. Bằng cách kết hợp với [Factor 3 — Chủ động kiểm soát Context Window](./factor-03-so-huu-context-window.md), bạn nắm toàn quyền quyết định dữ liệu nào trong State Store được serialize gửi cho LLM.

---

### 7 Lợi thế Kiến trúc của Mô hình Hợp nhất Trạng thái (Unified State Pattern)

1. **Nguồn Chân lý Duy nhất (Single Source of Truth - SSOT):** Triệt tiêu hoàn toàn nguy cơ lệch pha (Dual-Write / State Desynchronization) giữa cơ sở dữ liệu nghiệp vụ và runtime state của agent.
2. **Tuần tự hóa Tinh gọn (Trivial Serialization & Hydration):** Đối tượng `Thread` (danh sách `Event`) có thể serialize thành JSON/Protobuf và nạp lại vào bộ nhớ cực kỳ đơn giản.
3. **Gỡ lỗi & Khả năng Truy vết (Time-Travel Debugging & Auditability):** Toàn bộ diễn tiến vòng đời của Agent được ghi lại minh bạch trong một chuỗi sự kiện duy nhất (Append-Only Event Log).
4. **Tiến hóa Schema Linh hoạt (Schema Evolution):** Dễ dàng mở rộng hành vi hệ thống bằng cách bổ sung các Event Type mới mà không cần can thiệp tái cấu trúc cơ sở dữ liệu phức tạp.
5. **Khả năng Phục hồi sau Sự cố (Fault Tolerance & Point-in-time Recovery):** Khi worker bị sập (crash) hoặc restart, chỉ cần tải lại chuỗi `Thread` từ database để tái tạo trạng thái và tiếp tục thực thi.
6. **Phân nhánh Ngữ cảnh (Speculative Execution & Context Forking):** Dễ dàng "fork" một luồng làm việc tại bất kỳ thời điểm nào bằng cách sao chép một tập con sự kiện (event slice) sang một Session ID mới để thử nghiệm các nhánh suy luận khác nhau.
7. **Chiếu Dữ liệu Ra Giao diện (UI Projection & Observability):** Việc chuyển đổi chuỗi `Thread` thành báo cáo Markdown hoặc giao diện trực quan cho người dùng theo dõi trở nên vô cùng dễ dàng (tương tự mô hình Read Model trong CQRS).

---

**Điều hướng:** [← Factor 4: Tools are just structured outputs](./factor-04-tool-chi-la-output-co-cau-truc.md) · [Mục lục](./) · [Factor 6: Launch/Pause/Resume with simple APIs →](./factor-06-launch-pause-resume.md)

