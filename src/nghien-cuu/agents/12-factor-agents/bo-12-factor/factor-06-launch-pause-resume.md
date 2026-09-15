# Factor 6: Launch/Pause/Resume with simple APIs (Khởi chạy, Tạm dừng và Tiếp tục qua API Tối giản)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-06-launch-pause-resume.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-06-launch-pause-resume.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` **Về bản chất, Agent cũng là các chương trình phần mềm.** Do đó, hệ thống cần đáp ứng các tiêu chuẩn kiến trúc quen thuộc về cách thức Khởi chạy (Launch), Truy vấn (Query), Tạm dừng (Pause), Tiếp tục (Resume) và Hủy bỏ (Terminate) vòng đời của chúng.

[![Pause/Resume với API đơn giản](/nghien-cuu/agents/12-factor-agents/assets/img/165-pause-resume-animation.gif)](https://github.com/user-attachments/assets/feb1a425-cb96-4009-a133-8bd29480f21f)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/165-pause-resume-animation.gif">Xem bản ảnh động GIF</a></summary>

![Pause/Resume với API đơn giản](/nghien-cuu/agents/12-factor-agents/assets/img/165-pause-resume-animation.gif)

</details>

`[Dịch]` Trong một kiến trúc hướng dịch vụ (Service-Oriented Architecture), các thành phần tương tác cần tuân thủ 3 khả năng vận hành cốt lõi:

1. **Khởi chạy Tinh gọn (Simple Launch API):** Người dùng, ứng dụng frontend, pipeline tự động hóa hoặc các Agent khác đều có thể khởi tạo một Agent mới thông qua một API endpoint tiêu chuẩn (REST, gRPC, GraphQL hoặc Event Bus).
2. **Tạm dừng Phi trạng thái (Non-blocking Pause / Dehydration):** Khi gặp các tác vụ chạy dài (Long-Running Tasks) như chờ phê duyệt từ con người (HITL), chờ hoàn tất build CI/CD, hoặc chờ batch job, Agent và bộ điều phối tất định phải có khả năng giải phóng tài nguyên tính toán (CPU/Memory/Worker connection) và đưa phiên làm việc vào trạng thái ngủ (Suspended State).
3. **Tiếp tục Bất đồng bộ (Asynchronous Resume / Hydration):** Khi có sự kiện bên ngoài kích hoạt (như Webhook callback từ Stripe/GitHub, phản hồi Slack của người dùng), hệ thống có thể nạp lại trạng thái (Hydrate State) và **tiếp tục chu trình thực thi chính xác từ điểm bị gián đoạn** mà không đòi hỏi tích hợp gắn kết chặt (tight coupling) với worker ban đầu.

`[Dịch]` Nguyên lý này liên kết chặt chẽ với [Factor 5 — Hợp nhất State](./factor-05-gop-execution-state-va-business-state.md) và [Factor 8 — Làm chủ luồng điều khiển](./factor-08-so-huu-luong-dieu-khien.md), nhưng hoàn toàn có thể thiết kế độc lập dưới dạng module điều phối (Orchestration Engine).

`[Dịch]` **Ghi chú kiến trúc quan trọng:** Đa số các AI Orchestration Framework thế hệ cũ chỉ hỗ trợ cơ chế Pause/Resume ở cấp độ thô (toàn bộ workflow) hoặc sau khi một tool đã thực thi xong. Chúng **không** hỗ trợ cơ chế tạm dừng then chốt: *Tạm dừng ngay tại thời điểm LLM vừa đề xuất gọi một Tool nguy hiểm nhưng TRƯỚC KHI Tool đó thực sự được kích hoạt* (xem chi tiết tại [Factor 7](./factor-07-lien-he-con-nguoi-bang-tool-call.md) và [Factor 11](./factor-11-kich-hoat-tu-moi-noi.md)).

---

**Điều hướng:** [← Factor 5: Unify execution state and business state](./factor-05-gop-execution-state-va-business-state.md) · [Mục lục](./) · [Factor 7: Contact humans with tool calls →](./factor-07-lien-he-con-nguoi-bang-tool-call.md)

