# Factor 8: Own your control flow (Làm chủ Luồng Điều khiển Hệ thống)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-08-own-your-control-flow.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` **Khi bạn trực tiếp sở hữu và kiểm soát Luồng Điều khiển (Control Flow), bạn sẽ mở ra khả năng kiến trúc nên những hệ thống Agent cực kỳ mạnh mẽ, an toàn và có tính dự đoán cao.**

![Sở hữu luồng điều khiển](/nghien-cuu/agents/12-factor-agents/assets/img/180-control-flow.png)

`[Dịch]` Thay vì phó mặc hoàn toàn cho các hàm trừu tượng kiểu `agent.run()` tự chạy vòng lặp vô hạn `while (!done)`, bạn hãy tự thiết kế State Machine và cấu trúc điều phối phù hợp với chính xác bài toán nghiệp vụ của mình. Đặc biệt, việc tự chủ luồng điều khiển cho phép bạn quyết định **khi nào tiếp tục vòng lặp đồng bộ** và **khi nào cần thoát vòng lặp an toàn** để chờ phản hồi từ con người hoặc các pipeline chạy dài ngoại vi.

`[Dịch]` Ngoài ra, việc làm chủ control flow là điểm tựa để bạn tích hợp các thành phần hệ thống quan trọng:
- Cơ chế Caching và Tóm tắt kết quả Tool Invocations
- Đánh giá chất lượng đầu ra theo thời gian thực (LLM-as-a-Judge Guardrails)
- Nén ngữ cảnh động và [Quản lý Bộ nhớ (Context Hygiene)](./factor-03-so-huu-context-window.md)
- Telemetry phân tán (Distributed Tracing, Logging, Latency & Token Metrics)
- Rate Limiting và Circuit Breaker bảo vệ API phía client
- Cơ chế Tạm dừng Bền vững (Durable Sleep / Event-driven Wait)

---

### Mô hình Phân nhánh Điều khiển 3 Nhánh (3-Branch Control Flow Pattern)

`[Dịch]` Đoạn mã dưới đây minh họa mô hình điều phối tất định với 3 kịch bản điều khiển điển hình:

1. **Yêu cầu làm rõ (`request_clarification`):** LLM cần thêm dữ liệu từ con người $\rightarrow$ Lưu DB, gửi thông báo, **thoát vòng lặp (`break`)** và giải phóng tài nguyên worker.
2. **Đọc dữ liệu an toàn (`fetch_open_issues`):** LLM cần dữ liệu từ Linear API $\rightarrow$ Thực thi đồng bộ, bổ sung kết quả vào chuỗi sự kiện, **tiếp tục vòng lặp suy luận (`continue`)**.
3. **Thao tác có rủi ro cao (`create_issue` / `deploy_backend`):** LLM đề xuất ghi dữ liệu / thay đổi hệ thống $\rightarrow$ Đưa vào cổng chờ phê duyệt (Approval Gate), lưu DB, **thoát vòng lặp (`break`)** chờ con người xác nhận.

```python
async def handle_next_step(thread: Thread):
    while True:
        # Bước 1: Suy luận hành động kế tiếp từ LLM
        next_step = await determine_next_step(thread_to_prompt(thread))

        # Nhánh 1: Cần tương tác với con người -> Tạm dừng bất đồng bộ
        if next_step.intent == 'request_clarification':
            thread.events.append({
                "type": "request_clarification",
                "data": next_step,
            })
            await send_message_to_human(next_step)
            await db.save_thread(thread)
            break  # Thoát vòng lặp worker, chuyển sang chế độ chờ Webhook

        # Nhánh 2: Thao tác đọc dữ liệu an toàn -> Tiếp tục vòng lặp đồng bộ
        elif next_step.intent == 'fetch_open_issues':
            thread.events.append({
                "type": "fetch_open_issues",
                "data": next_step,
            })
            issues = await linear_client.issues()
            thread.events.append({
                "type": "fetch_open_issues_result",
                "data": issues,
            })
            continue  # Truyền context mới nạp cho LLM để suy luận bước tiếp theo

        # Nhánh 3: Tác vụ nhạy cảm có side-effect -> Chờ phê duyệt (Approval Gate)
        elif next_step.intent == 'create_issue':
            thread.events.append({
                "type": "create_issue",
                "data": next_step,
            })
            await request_human_approval(next_step)
            await db.save_thread(thread)
            break  # Thoát vòng lặp an toàn, chờ quyết định duyệt từ người quản trị
```

---

### Điểm Chèn Sinh tử: Khoảng trống giữa Lựa chọn và Thực thi Công cụ

`[Dịch]` Yêu cầu tính năng quan trọng nhất đối với một hệ thống Agent cấp Enterprise là khả năng **can thiệp (intercept), tạm dừng và tiếp tục luồng thực thi ĐẶC BIỆT tại khoảng trống giữa thời điểm LLM "Lựa chọn công cụ" (Tool Selection) và thời điểm hệ thống "Thực thi công cụ" (Tool Execution)**.

`[Dịch]` Nếu framework không cung cấp khả năng can thiệp ở cấp độ chi tiết này, bạn sẽ bị đẩy vào thế bế tắc với 3 lựa chọn tồi tệ:

1. **Giữ kết nối chờ trong bộ nhớ (In-memory Busy Waiting):** Dùng các hàm `while sleep()` nghẽn luồng; hệ thống sẽ mất trắng trạng thái nếu process bị crash/restart.
2. **Hạn chế Agent ở tác vụ tầm thường:** Chỉ dám giao cho Agent các tác vụ an toàn, đọc dữ liệu rủi ro thấp như tìm kiếm hay tóm tắt văn bản.
3. **Thực thi liều lĩnh ("YOLO Execution"):** Trao cho Agent quyền gọi API nguy hiểm (xóa DB, deploy production, chuyển tiền) và chỉ biết cầu nguyện rằng mô hình không gặp ảo giác (hallucination).

`[Dịch]` Mô hình này liên kết chặt chẽ với [Factor 5 (Unified State)](./factor-05-gop-execution-state-va-business-state.md) và [Factor 6 (Launch/Pause/Resume)](./factor-06-launch-pause-resume.md).

Sơ đồ dưới đây minh họa **State, Tạm dừng/Tiếp tục, và Con người trong Vòng lặp** — cơ chế nền tảng cho Bộ tứ Factor 5, 6, 7, 8:

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/04-trang-thai-con-nguoi.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

---

**Điều hướng:** [← Factor 7: Contact humans with tool calls](./factor-07-lien-he-con-nguoi-bang-tool-call.md) · [Mục lục](./) · [Factor 9: Compact Errors into Context Window →](./factor-09-nen-loi-vao-context-window.md)

