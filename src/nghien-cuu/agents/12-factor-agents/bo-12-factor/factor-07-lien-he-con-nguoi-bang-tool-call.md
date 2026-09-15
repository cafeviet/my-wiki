# Factor 7: Contact humans with tool calls (Tương tác với Con người Dưới dạng Lệnh gọi Tool)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-07-contact-humans-with-tools.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Theo cơ chế mặc định của hầu hết các LLM API, mô hình luôn phải đối mặt với một **quyết định token đầu tiên mang tính đánh đổi rất cao (High-Stakes First-Token Dilemma)**: *Nên sinh phản hồi dạng văn bản thuần (Plaintext) cho người dùng, hay sinh cấu trúc dữ liệu JSON để gọi hàm (Tool Call)?*

![Liên hệ con người bằng lệnh gọi tool](/nghien-cuu/agents/12-factor-agents/assets/img/170-contact-humans-with-tools.png)

`[Dịch]` Hệ thống đang đặt toàn bộ rủi ro vào token đầu tiên: Nếu là câu trả lời `"Thời tiết ở Tokyo..."`, token đầu tiên sẽ là một từ ngữ tự nhiên; nhưng nếu là lệnh gọi hàm `fetch_weather`, token đầu tiên sẽ là một ký tự đặc biệt quy ước bắt đầu khối JSON.

`[Dịch]` Để tăng độ ổn định và tất định của kiến trúc, một giải pháp hiệu quả là **bắt buộc LLM luôn luôn xuất ra định dạng JSON có cấu trúc (Strict JSON Generation)**. Trong mô hình này, ngay cả việc trò chuyện, xin ý kiến con người (`request_human_input`) hay báo hiệu hoàn tất nhiệm vụ (`done_for_now`) cũng đều được định nghĩa thành các **Tool Call có cấu trúc định kiểu rõ ràng**:

```python
class Options:
    urgency: Literal["low", "medium", "high"]
    format: Literal["free_text", "yes_no", "multiple_choice"]
    choices: List[str]

# Định nghĩa Schema cho tương tác Human-in-the-Loop
class RequestHumanInput:
    intent: Literal["request_human_input"]
    question: str
    context: str
    options: Options

# Xử lý phân nhánh trong vòng lặp điều phối của Agent
if nextStep.intent == 'request_human_input':
    thread.events.append({
        "type": "human_input_requested",
        "data": nextStep
    })
    # Lưu vết trạng thái xuống Database và gửi thông báo cho con người
    thread_id = await save_state(thread)
    await notify_human(nextStep, thread_id)
    return  # Giải phóng worker, tạm dừng an toàn và chờ callback ngoại vi
else:
    # Điều phối các hành vi nghiệp vụ khác
    pass
```

`[Dịch]` Khi con người phản hồi thông qua Slack, Email, SMS hoặc Web portal, một Webhook Ingress Gateway sẽ tiếp nhận sự kiện và đánh thức (resume) luồng xử lý:

```python
@app.post('/webhook')
async def handle_human_response(req: Request):
    payload = await req.json()
    thread_id = payload["threadId"]
    
    # Nạp lại trạng thái (Hydrate State) từ Database
    thread = await load_state(thread_id)
    thread.events.append({
        "type": "response_from_human",
        "data": payload["response"]
    })
    
    # Tiếp tục chu trình suy luận tiếp theo
    next_step = await determine_next_step(thread_to_prompt(thread))
    thread.events.append(next_step)
    await handle_next_step(thread, next_step)

    return {"status": "accepted"}
```

`[Dịch]` Mẫu thiết kế này là sự kết hợp hoàn hảo giữa [Factor 3 (Context Window)](./factor-03-so-huu-context-window.md), [Factor 4 (Structured Outputs)](./factor-04-tool-chi-la-output-co-cau-truc.md), [Factor 5 (Unified State)](./factor-05-gop-execution-state-va-business-state.md), [Factor 6 (Pause/Resume)](./factor-06-launch-pause-resume.md), và [Factor 8 (Control Flow)](./factor-08-so-huu-luong-dieu-khien.md).

---

### 5 Giá trị Cốt lõi của Mẫu Thiết kế Human-as-a-Tool

1. **Chỉ dẫn Tường minh & Định kiểu Chặt chẽ (Explicit Schema):** Cho phép LLM yêu cầu chính xác định dạng câu trả lời mong muốn từ con người (văn bản tự do, xác nhận Yes/No, hoặc danh sách lựa chọn trắc nghiệm).
2. **Kiến trúc Vòng lặp Ngoài (Outer Loop Architecture):** Vượt ra khỏi mô hình Chatbot truyền thống (`Human -> Agent`). Hỗ trợ xuất sắc các workflow tự động chạy ngầm theo lịch (Cron/Event-driven) có khả năng chủ động liên hệ con người khi cần (`Agent -> Human`).
3. **Điều phối Đa người dùng (Multi-Stakeholder Collaboration):** Dễ dàng định tuyến yêu cầu phê duyệt tới đúng cá nhân/phòng ban và ghi nhận phản hồi vào chuỗi sự kiện chung.
4. **Mở rộng Sang Giao tiếp Đa Agent (Agent-to-Agent Delegation):** Cùng một cấu trúc request/response này có thể tái sử dụng nguyên vẹn để Agent này gửi yêu cầu hỗ trợ tới một Agent chuyên trách khác.
5. **Độ Bền vững & Khả năng Kiểm toán (Durability & Compliance):** Toàn bộ tương tác giữa AI và Con người đều được lưu trữ thành các sự kiện có cấu trúc (Event Log), đáp ứng đầy đủ yêu cầu kiểm toán an toàn thông tin doanh nghiệp.

[Đọc thêm về Outer Loop Agents tại bài phân tích chuyên sâu này](https://theouterloop.substack.com/p/openais-realtime-api-is-a-step-towards).

![Outer loop agents](/nghien-cuu/agents/12-factor-agents/assets/img/175-outer-loop-agents.png)

---

**Điều hướng:** [← Factor 6: Launch/Pause/Resume with simple APIs](./factor-06-launch-pause-resume.md) · [Mục lục](./) · [Factor 8: Own your control flow →](./factor-08-so-huu-luong-dieu-khien.md)

