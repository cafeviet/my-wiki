# Factor 4: Tools are just structured outputs (Bản chất Công cụ chỉ là Đầu ra có Cấu trúc)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-04-tools-are-structured-outputs.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-04-tools-are-structured-outputs.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` **Cơ chế gọi công cụ (Tool Calling) không hề có gì bí ẩn hay phức tạp.** Về bản chất kỹ thuật, chúng đơn thuần chỉ là **chuỗi dữ liệu đầu ra có cấu trúc (Structured JSON Outputs)** được sinh ra từ LLM nhằm kích hoạt mã nguồn thực thi tất định phía hệ thống.

![Tool chỉ là output có cấu trúc](/nghien-cuu/agents/12-factor-agents/assets/img/140-tools-are-just-structured-outputs.png)

`[Dịch]` Giả sử hệ thống của bạn cung cấp hai công cụ nghiệp vụ: `CreateIssue` và `SearchIssues`. Việc yêu cầu LLM "chọn và thực thi một trong nhiều công cụ" thực chất chỉ là yêu cầu mô hình sinh ra một payload JSON tuân thủ schema định sẵn để chúng ta parse thành đối tượng dữ liệu tương ứng:

```python
class Issue:
    title: str
    description: str
    team_id: str
    assignee_id: str

class CreateIssue:
    intent: Literal["create_issue"]
    issue: Issue

class SearchIssues:
    intent: Literal["search_issues"]
    query: str
    what_youre_looking_for: str
```

`[Dịch]` Chu trình vận hành theo mô hình này vô cùng tinh gọn:

1. **LLM suy luận & sinh cấu trúc (Structured Generation):** Mô hình phân tích ngữ cảnh và xuất ra payload JSON chuẩn schema.
2. **Hệ thống điều phối tất định (Deterministic Execution):** Tầng runtime nhận payload, kiểm tra tính hợp lệ và kích hoạt hành vi nghiệp vụ tương ứng (gọi REST/gRPC API, ghi database, v.v.).
3. **Phản hồi trạng thái (Context Feeding):** Kết quả thực thi được tuần tự hóa (serialize) và đẩy ngược lại vào Context Window cho chu kỳ suy luận kế tiếp.

`[Dịch]` Mẫu thiết kế này tạo ra sự **phân tách trách nhiệm rành mạch (Clean Separation of Concerns)** giữa Tầng Suy luận của LLM và Tầng Thực thi của Ứng dụng: **LLM ra quyết định về Ý định (*What to do*), trong khi Mã nguồn tất định nắm toàn quyền kiểm soát Phương thức thực hiện (*How to do it*)**. Việc LLM phát sinh một "tool call" không đồng nghĩa với việc bạn bị ép phải gọi trực tiếp một hàm cục bộ tương ứng theo cách cố định.

```python
# Phân nhánh điều phối (Polymorphic Dispatching)
if nextStep.intent == 'create_payment_link':
    stripe.paymentlinks.create(**nextStep.parameters)
    return
elif nextStep.intent == 'wait_for_a_while':
    # Kích hoạt trạng thái tạm dừng bất đồng bộ (Asynchronous Pause)
    await schedule_resume(delay_seconds=300)
    return
else:
    # Xử lý trường hợp ngoại lệ hoặc fallback handler
    handle_unknown_intent(nextStep)
```

`[Dịch]` **Ghi chú kiến trúc:** Trong cộng đồng kỹ thuật, có rất nhiều thảo luận về sự đánh đổi giữa *Plain Prompting*, *Native Tool Calling*, *JSON Mode*, và *Constrained Generation (Schema-Aligned Parsing)*. Bạn có thể tham khảo thêm các phân tích chuyên sâu tại:
- [Prompting vs JSON Mode vs Function Calling vs Constrained Generation vs SAP](https://www.boundaryml.com/blog/schema-aligned-parsing)
- [When should I use function calling, structured outputs, or JSON mode?](https://www.vellum.ai/blog/when-should-i-use-function-calling-structured-outputs-or-json-mode)
- [OpenAI JSON vs Function Calling](https://docs.llamaindex.ai/en/stable/examples/llm/openai_json_vs_function_calling/)

`[Dịch]` "Bước tiếp theo" trong một hệ thống Agent cấp doanh nghiệp **không nhất thiết** chỉ là việc "thực thi một hàm đơn lẻ rồi lấy kết quả". Bạn sẽ mở ra sự linh hoạt vô hạn trong kiến trúc khi coi Tool Call đơn thuần là **một sự kiện phát sinh JSON có cấu trúc nhằm báo hiệu cho State Machine tất định biết cần chuyển đổi trạng thái nào**. Nguyên lý này sẽ kết hợp chặt chẽ với [Factor 8 — Làm chủ luồng điều khiển](./factor-08-so-huu-luong-dieu-khien.md).

---

**Điều hướng:** [← Factor 3: Own your context window](./factor-03-so-huu-context-window.md) · [Mục lục](./) · [Factor 5: Unify execution state and business state →](./factor-05-gop-execution-state-va-business-state.md)

