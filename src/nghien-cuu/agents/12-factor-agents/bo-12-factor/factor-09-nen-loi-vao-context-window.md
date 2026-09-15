# Factor 9: Compact Errors into Context Window (Nén và Cắt tỉa Lỗi trong Cửa sổ Ngữ cảnh)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-09-compact-errors.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-09-compact-errors.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Một trong những năng lực vượt trội nhất của kiến trúc Agent là khả năng **tự phục hồi lỗi (Self-Healing)**: Khi một lệnh gọi công cụ (Tool Call) thất bại (ví dụ: sai format tham số, API trả về mã lỗi 400/404, hoặc vi phạm schema), các mô hình LLM hiện đại có xác suất rất cao trong việc phân tích stack trace hoặc thông báo lỗi để tự động điều chỉnh payload cho lần gọi kế tiếp.

`[Dịch]` Bạn hoàn toàn có thể triển khai cơ chế này một cách độc lập và tối giản:

```python
thread = {"events": [initial_message]}

while True:
    next_step = await determine_next_step(thread_to_prompt(thread))
    thread["events"].append({
        "type": next_step.intent,
        "data": next_step,
    })
    try:
        result = await handle_next_step(thread, next_step)
    except Exception as e:
        # Bắt ngoại lệ, định dạng lại lỗi và nạp vào Context Window để LLM tự khắc phục
        thread["events"].append({
            "type": "error",
            "data": format_error(e),
        })
        # Tiếp tục vòng lặp để LLM đọc lỗi và thử lại
```

---

### Cơ chế Ngắt Mạch & Giới hạn Số lần Thử lại (Circuit Breaker & Retry Limits)

`[Dịch]` Trong môi trường Production, việc cho phép LLM tự thử lại mà không có rào cản kiểm soát sẽ dẫn đến hiện tượng **vòng xoáy suy luận lặp (Spin-Out Loops)** — LLM liên tục mắc cùng một lỗi và tiêu tốn ngân sách token một cách vô ích.

`[Dịch]` Do đó, kiến trúc bắt buộc phải tích hợp **Bộ đếm Lỗi Liên tiếp (Consecutive Error Counter)** đóng vai trò như một Circuit Breaker:

```python
consecutive_errors = 0
MAX_RETRIES = 3

while True:
    next_step = await determine_next_step(thread_to_prompt(thread))
    
    try:
        result = await handle_next_step(thread, next_step)
        thread["events"].append({
            "type": f"{next_step.intent}_result",
            "data": result,
        })
        # Thực thi thành công -> Reset ngay bộ đếm lỗi
        consecutive_errors = 0
    except Exception as e:
        consecutive_errors += 1
        if consecutive_errors < MAX_RETRIES:
            # Vẫn trong ngưỡng cho phép -> Nạp lỗi vào context để tự sửa
            thread["events"].append({
                "type": "error",
                "data": format_error(e),
            })
        else:
            # Vượt quá ngưỡng chịu lỗi -> Thoát vòng lặp, kích hoạt quy trình leo thang (Escalation)
            await escalate_to_human(thread, e)
            break
```

[![Nén lỗi vào context window](/nghien-cuu/agents/12-factor-agents/assets/img/195-factor-9-errors.gif)](https://github.com/user-attachments/assets/cd7ed814-8309-4baf-81a5-9502f91d4043)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/195-factor-9-errors.gif">Xem bản ảnh động GIF</a></summary>

![Nén lỗi vào context window](/nghien-cuu/agents/12-factor-agents/assets/img/195-factor-9-errors.gif)

</details>

---

### Hai Lợi ích Cốt lõi & Chiến lược Vệ sinh Ngữ cảnh (Context Hygiene)

1. **Khả năng Tự phục hồi Tức thời (Self-Healing):** Giảm thiểu sự gián đoạn của con người đối với các lỗi định dạng hoặc lỗi tạm thời có thể tự khắc phục được.
2. **Tính Bền vững Hệ thống (System Resilience):** Agent có khả năng tự vượt qua các điểm nghẽn cục bộ thay vì sập toàn bộ quy trình.

`[Dịch]` **Chiến lược Nén & Cắt tỉa Ngữ cảnh (Context Compaction & Pruning):**
Khi kết hợp với [Factor 3 (Own your context window)](./factor-03-so-huu-context-window.md) và [Factor 8 (Own your control flow)](./factor-08-so-huu-luong-dieu-khien.md), bạn **không nhất thiết phải lưu giữ toàn bộ stack trace khổng lồ trong Context Window mãi mãi**. Sau khi Agent đã sửa lỗi thành công:
- Hãy **cắt tỉa (prune)** hoặc **nén gọn (compact)** chuỗi lỗi và các lần gọi thất bại trước đó.
- Giữ cho Context Window luôn trong trạng thái tinh gọn, tránh làm loãng cơ chế chú ý (Attention Mechanism) của mô hình.

`[Dịch]` Tuy nhiên, phương pháp triệt để nhất để ngăn ngừa bế tắc lỗi chính là áp dụng [Factor 10 — Thiết kế các Agent nhỏ, chuyên biệt](./factor-10-agent-nho-tap-trung.md).

---

**Điều hướng:** [← Factor 8: Own your control flow](./factor-08-so-huu-luong-dieu-khien.md) · [Mục lục](./) · [Factor 10: Small, Focused Agents →](./factor-10-agent-nho-tap-trung.md)

