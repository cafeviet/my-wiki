# Factor 12: Make your agent a stateless reducer (Mô hình hóa Agent như một Stateless Reducer)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-12-stateless-reducer.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Sau khi đã kinh qua toàn bộ các nguyên lý từ kiểm soát Prompt, Context Window, Hợp nhất State cho đến Tự chủ Luồng điều khiển, Factor 12 đúc kết toàn bộ kiến trúc Agent về một **mô hình hàm số thuần khiết và thanh lịch nhất: Stateless Reducer**.

![Agent như một stateless reducer](/nghien-cuu/agents/12-factor-agents/assets/img/1c0-stateless-reducer.png)

![Agent như phép foldl](/nghien-cuu/agents/12-factor-agents/assets/img/1c5-agent-foldl.png)

---

### Bản chất Toán học & Kiến trúc của Factor 12

`[Dịch]` Trong lập trình hàm (Functional Programming), một hàm **Reducer** nhận vào trạng thái hiện tại và một sự kiện mới để sinh ra trạng thái tiếp theo:

$$\text{Reducer}(\text{CurrentState}, \text{IncomingEvent}) \longrightarrow \text{NextState}$$

`[Dịch]` Khi kết hợp với [Factor 5 (Hợp nhất Trạng thái thành Event Log)](./factor-05-gop-execution-state-va-business-state.md), toàn bộ vòng đời của Agent thực chất là một phép thu gọn danh sách sự kiện (**`foldl` / `reduce`**):

$$\text{CurrentState} = \text{foldl}(\text{StepReducer}, \text{InitialState}, [\text{Event}_1, \text{Event}_2, \dots, \text{Event}_n])$$

---

### 3 Đỉnh cao Kiến trúc khi Mô hình hóa Agent như một Stateless Reducer

1. **Triệt tiêu Hoàn toàn Trạng thái Ẩn trong Bộ nhớ (Zero In-Memory State Leakage):** Agent runtime không lưu trữ bất kỳ biến trạng thái cục bộ nào trong RAM hay process worker. Trạng thái duy nhất là chuỗi `Thread.events` được lưu trữ bền vững tại State Store.
2. **Khả năng Tái lập Tuyệt đối (Deterministic Replayability & Time-Travel Debugging):** Bạn có thể tua lại (replay) toàn bộ chuỗi sự kiện của một Agent từ đầu đến cuối trong môi trường staging/test để tái hiện chính xác lỗi, benchmark model mới hoặc phân tích hành vi mà không gặp side-effect.
3. **Khả năng Mở rộng Ngang Vô hạn (Horizontal Scalability & Serverless Readiness):** Bất kỳ serverless worker nào (AWS Lambda, Cloud Run, Kubernetes Pod) cũng có thể tiếp nhận và xử lý bất kỳ sự kiện nào của bất kỳ phiên làm việc nào (No Sticky Session required).

---

**Điều hướng:** [← Factor 11: Trigger from anywhere, meet users where they are](./factor-11-kich-hoat-tu-moi-noi.md) · [Mục lục](./) · [Factor 13 (danh dự): Pre-fetch toàn bộ context bạn có thể cần →](./factor-13-pre-fetch-context.md)

