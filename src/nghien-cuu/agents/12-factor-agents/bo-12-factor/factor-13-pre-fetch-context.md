# Factor 13 (Danh dự): Pre-fetch Toàn bộ Context bạn có thể cần (Proactive Context Ingestion)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/appendix-13-pre-fetch.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/appendix-13-pre-fetch.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Nếu hệ thống có thể dự đoán với xác suất cao rằng LLM chắc chắn sẽ cần gọi công cụ $X$ ngay tại bước đầu tiên, **đừng lãng phí một chu kỳ gọi mạng (Round-trip Inference) và ngân sách token chỉ để chờ mô hình phát sinh lệnh gọi đó**.

---

### Đối chiếu Kiến trúc: Bị động (Reactive) vs Chủ động Nạp trước (Proactive Pre-fetching)

#### 1. Cách tiếp cận Bị động (Reactive Tool Invocations)
Hệ thống phải chịu độ trễ gấp đôi do LLM phải gọi `list_git_tags` trước:

```jinja
When looking at deployments, you will likely want to fetch the list of published git tags,
so you can use it to deploy to prod.

Here's what happened so far:
{{ thread.events }}

What's the next step?
Answer in JSON format with one of the following intents:
{ intent: 'deploy_backend_to_prod', tag: string } OR 
{ intent: 'list_git_tags' } OR 
{ intent: 'done_for_now', message: string }
```

```python
# Tốn 1 vòng inference chỉ để LLM trả về intent: 'list_git_tags'
thread = {"events": [initial_message]}
next_step = await determine_next_step(thread)

while True:
    match next_step.intent:
        case 'list_git_tags':
            tags = await fetch_git_tags()
            thread["events"].append({"type": 'list_git_tags', "data": tags})
            # Lặp tiếp vòng 2 để LLM quyết định deploy tag nào
        case 'deploy_backend_to_prod':
            deploy_result = await deploy_backend_to_prod(next_step.data.tag)
            thread["events"].append({"type": 'deploy_backend_to_prod', "data": deploy_result})
        case 'done_for_now':
            await notify_human(next_step.message)
            break
```

#### 2. Cách tiếp cận Chủ động (Proactive Pre-fetching)
Tầng mã nguồn tất định nạp sẵn danh sách Git Tags vào Context Window ngay trước khi kích hoạt LLM:

```diff
- When looking at deployments, you will likely want to fetch the list of published git tags,
- so you can use it to deploy to prod.
+ The current git tags are:
+ {{ git_tags }}

Here's what happened so far:
{{ thread.events }}

What's the next step?
Answer in JSON format with one of the following intents:
{
  intent: 'deploy_backend_to_prod',
  tag: string
- } OR {
-   intent: 'list_git_tags'
} OR {
  intent: 'done_for_now',
  message: string
}
```

```diff
thread = {"events": [initial_message]}
+ git_tags = await fetch_git_tags()  # Thực thi tất định siêu tốc
- next_step = await determine_next_step(thread)
+ next_step = await determine_next_step(thread, git_tags)  # LLM suy luận trực tiếp hành động deploy
```

---

### Nguyên lý Đúc kết từ Kiến trúc sư Giải pháp

> #### Nếu bạn đã biết trước mô hình chắc chắn sẽ cần dữ liệu gì, hãy chủ động nạp dữ liệu đó một cách TẤT ĐỊNH (Deterministic Pre-fetching), và dành năng lực suy luận của LLM cho bài toán cốt lõi: phân tích và xử lý kết quả đó.

`[Dịch]` Trong kỹ nghệ xây dựng hệ thống AI Agent, **mọi tối ưu hóa đều quy về [Context Engineering (Kỹ nghệ Ngữ cảnh)](./factor-03-so-huu-context-window.md)**.

---

**Điều hướng:** [← Factor 12: Make your agent a stateless reducer](./factor-12-agent-nhu-stateless-reducer.md) · [Mục lục](./)

