# Factor 10: Small, Focused Agents (Kiến trúc Micro-Agents Đơn nhiệm & Chuyên biệt)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-10-small-focused-agents.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Thay vì cố gắng xây dựng những "Monolithic God Agents" khổng lồ ôm đồm mọi nghiệp vụ, giải pháp kiến trúc tối ưu là thiết kế **các Agent nhỏ, chuyên biệt (Micro-Agents / Small Focused Agents)** thực hiện xuất sắc một phạm vi trách nhiệm duy nhất (Single Responsibility Principle). Mỗi Agent chỉ đóng vai trò là một khối xây dựng (Building Block) cấu thành nên một hệ sinh thái phần mềm lớn hơn và phần lớn mang tính tất định.

![Agent nhỏ, tập trung](/nghien-cuu/agents/12-factor-agents/assets/img/1a0-small-focused-agents.png)

`[Dịch]` **Cơ sở Lý luận Kỹ thuật:** Hiệu năng và độ tin cậy của LLM có mối tương quan nghịch với độ dài của chuỗi suy luận liên tục. Một tác vụ càng lớn, chuỗi suy luận càng nhiều bước, Context Window càng phình to thì cơ chế chú ý (Attention Mechanism) của mô hình càng dễ bị phân mảnh hoặc trượt khỏi mục tiêu ban đầu. Bằng cách giới hạn mỗi Agent trong một phạm vi nghiệp vụ hẹp (từ 3–10 bước, tối đa khoảng 20 bước), chúng ta duy trì kích thước Context Window ở mức tối ưu và đảm bảo độ chính xác suy luận đạt đỉnh cao nhất.

> #### Khi dung lượng Context tăng lên, nguy cơ LLM mất tập trung và gặp ảo giác (Hallucination) tăng theo cấp số nhân.

---

### 5 Lợi thế Vận hành của Kiến trúc Micro-Agents

1. **Kiểm soát Ngân sách Context (Manageable Context Budget):** Context Window nhỏ gọn giúp mô hình đạt độ nhạy suy luận cao nhất và giảm thiểu độ trễ phản hồi (TTFT).
2. **Ranh giới Trách nhiệm Minh định (Clear Bounded Contexts):** Mỗi Agent có mục tiêu, bộ công cụ (Tooling Surface) và Persona rõ ràng, triệt tiêu xung đột vai trò.
3. **Độ Tin cậy Vượt trội (High Deterministic Reliability):** Giảm thiểu tối đa nguy cơ Agent bị lạc hướng trong các workflow phức tạp.
4. **Kiểm thử Đơn vị Cô lập (Isolated Unit Testing & Evals):** Dễ dàng thiết lập kịch bản test và benchmark độc lập cho từng Agent mà không phụ thuộc vào toàn bộ hệ thống.
5. **Khả năng Giám sát & Cô lập Sự cố (Fault Isolation & Observability):** Khi một tác vụ thất bại, kỹ sư có thể khoanh vùng chính xác Agent gặp sự cố để tinh chỉnh prompt/tools mà không ảnh hưởng tới các module khác.

---

### Khi Mô hình Tương lai Thông minh hơn, Kiến trúc này còn Hợp lý?

`[Dịch]` *Liệu chúng ta có còn cần chia nhỏ Agent nếu các mô hình thế hệ tiếp theo có thể tự xử lý chuỗi tác vụ 100+ bước?*

`[Dịch]` **Câu trả lời là: HOÀN TOÀN CẦN.** Khi năng lực LLM nâng cấp, phạm vi của một Agent có thể mở rộng tự nhiên để xử lý nhiều bước hơn trong một DAG (Directed Acyclic Graph) lớn hơn. Tuy nhiên, cách tiếp cận mô-đun hóa này đem lại hai giá trị song song: **Đảm bảo hệ thống vận hành tin cậy và hiệu quả NGAY HÔM NAY**, đồng thời cung cấp một cấu trúc phân rã linh hoạt để mở rộng quy mô khi mô hình tiến hóa.

[![Phạm vi agent mở rộng dần](/nghien-cuu/agents/12-factor-agents/assets/img/1a5-agent-scope-grow.gif)](https://github.com/user-attachments/assets/0cd3f52c-046e-4d5e-bab4-57657157c82f)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/1a5-agent-scope-grow.gif">Xem bản ảnh động GIF</a></summary>

![Phạm vi agent mở rộng dần](/nghien-cuu/agents/12-factor-agents/assets/img/1a5-agent-scope-grow.gif)

</details>

`[Dịch]` Việc **chủ động thiết kế phạm vi (Scope Boundary)** của Agent và chỉ mở rộng khi đã kiểm chứng được chất lượng là kỷ luật cốt lõi của kỹ nghệ phần mềm. Như đội ngũ sáng lập NotebookLM từng chia sẻ:

> "Những khoảnh khắc kỳ diệu và đột phá nhất khi xây dựng sản phẩm AI xuất hiện khi chúng tôi thiết kế hệ thống áp sát ranh giới năng lực tối đa của mô hình một cách có kiểm soát."

`[Dịch]` Xây dựng hệ thống Agent thành công không nằm ở việc kỳ vọng một mô hình toàn năng giải quyết mọi thứ, mà nằm ở **kỷ luật kiến trúc** phân rã bài toán phức tạp thành các bài toán con đơn nhiệm và đáng tin cậy.

---

**Điều hướng:** [← Factor 9: Compact Errors into Context Window](./factor-09-nen-loi-vao-context-window.md) · [Mục lục](./) · [Factor 11: Trigger from anywhere, meet users where they are →](./factor-11-kich-hoat-tu-moi-noi.md)

