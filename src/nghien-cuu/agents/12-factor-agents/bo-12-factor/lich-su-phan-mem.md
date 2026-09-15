# Chúng ta đã tới đây thế nào: Lược sử phần mềm

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/brief-history-of-software.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/brief-history-of-software.md) (commit `d20c728`)

> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

---

## Bản dài: chúng ta đã tới đây thế nào

`[Dịch]` Dù bạn mới làm quen với agent hay là một cựu binh gàn dở như tôi, tôi sẽ cố thuyết phục bạn **vứt bỏ phần lớn những gì bạn nghĩ về AI Agent**, lùi lại một bước, và suy nghĩ lại từ những nguyên lý đầu tiên. (tiết lộ trước nếu bạn chưa để ý tới đợt ra mắt OpenAI responses vài tuần trước — nhưng đẩy **thêm** logic agent ra sau một API thì không phải là cách)

### Bạn không nhất thiết phải nghe tôi

`[Dịch]` Phần này không có gì để dịch — tác giả chỉ nhấn mạnh lại lời mời ở trên.

## Agent là phần mềm, và một lược sử ngắn về nó

`[Dịch]` Hãy nói về cách chúng ta tới được đây.

### 60 năm trước

`[Dịch]` Chúng ta sẽ nói rất nhiều về **Directed Graph (đồ thị có hướng — DG)** và người bạn **Acyclic (không chu trình)** của nó, **DAG**. Tôi sẽ bắt đầu bằng việc chỉ ra rằng... thì... **phần mềm chính là một đồ thị có hướng**. Có lý do vì sao trước đây chúng ta biểu diễn chương trình dưới dạng **lưu đồ (flow chart)**.

![Sơ đồ phần mềm như một đồ thị có hướng](/nghien-cuu/agents/12-factor-agents/assets/img/010-software-dag.png)

### 20 năm trước

`[Dịch]` Khoảng 20 năm trước, chúng ta bắt đầu thấy các **DAG orchestrator** trở nên phổ biến. Đó là những cái tên kinh điển như [Airflow](https://airflow.apache.org/), [Prefect](https://www.prefect.io/), vài tiền bối, và vài cái mới hơn như ([dagster](https://dagster.io/), [inngest](https://www.inngest.com/), [windmill](https://www.windmill.dev/)). Chúng đi theo cùng một **mẫu đồ thị**, với lợi ích cộng thêm là khả năng quan sát (observability), tính module hóa, retry, quản trị, v.v.

![Các DAG orchestrator](/nghien-cuu/agents/12-factor-agents/assets/img/015-dag-orchestrators.png)

### 10–15 năm trước

`[Dịch]` Khi các model ML bắt đầu đủ tốt để hữu dụng, chúng ta bắt đầu thấy các DAG có **model ML xen vào**. Bạn có thể hình dung những bước như "tóm tắt văn bản trong cột này thành một cột mới" hay "phân loại các ticket hỗ trợ theo mức độ nghiêm trọng hoặc sắc thái cảm xúc".

![DAG có model ML](/nghien-cuu/agents/12-factor-agents/assets/img/020-dags-with-ml.png)

`[Dịch]` Nhưng xét cho cùng, nó vẫn chủ yếu là phần mềm tất định (deterministic software) xưa cũ.

### Lời hứa của agent

`[Dịch]` Tôi không phải [người đầu tiên nói điều này](https://youtu.be/Dc99-zTMyMg?si=bcT0hIwWij2mR-40&t=73), nhưng bài học lớn nhất của tôi khi bắt đầu tìm hiểu về agent là: **bạn được phép vứt bỏ DAG đi**. Thay vì kỹ sư phần mềm tự code từng bước và từng trường hợp biên, bạn có thể đưa cho agent **một mục tiêu và một tập chuyển đổi (transitions)**:

![Agent DAG — từ mục tiêu tới đường đi](/nghien-cuu/agents/12-factor-agents/assets/img/025-agent-dag.png)

`[Dịch]` Và để **LLM ra quyết định trong thời gian thực** để tự tìm ra đường đi.

![Agent DAG với các đường đi được LLM chọn](/nghien-cuu/agents/12-factor-agents/assets/img/026-agent-dag-lines.png)

`[Dịch]` Lời hứa ở đây là bạn viết ít phần mềm hơn, bạn chỉ đưa cho LLM các **"cạnh" (edges)** của đồ thị và để nó tự tìm ra các **"nút" (nodes)**. Bạn có thể phục hồi sau lỗi, viết ít code hơn, và có thể phát hiện ra rằng LLM tìm được những cách giải quyết vấn đề mới lạ.

### Agent như những vòng lặp

`[Dịch]` Nói cách khác, bạn có một vòng lặp gồm 3 bước:

1. LLM xác định bước kế tiếp trong workflow, xuất ra JSON có cấu trúc ("tool calling")
2. Code tất định (deterministic code) thực thi lệnh gọi tool
3. Kết quả được ghi thêm (append) vào context window
4. Lặp lại cho tới khi bước kế tiếp được xác định là "done" (xong)

```python
initial_event = {"message": "..."}
context = [initial_event]
while True:
  next_step = await llm.determine_next_step(context)
  context.append(next_step)

  if (next_step.intent === "done"):
    return next_step.final_answer

  result = await execute_step(next_step)
  context.append(result)
```

`[Dịch]` Context ban đầu của chúng ta chỉ là **sự kiện khởi đầu** (có thể là một tin nhắn người dùng, có thể là một cron vừa kích hoạt, có thể là một webhook, v.v.), và chúng ta yêu cầu LLM chọn bước kế tiếp (tool) hoặc xác định rằng đã xong.

`[Dịch]` Đây là một ví dụ nhiều bước:

[![Vòng lặp agent nhiều bước](/nghien-cuu/agents/12-factor-agents/assets/img/027-agent-loop-animation.gif)](https://github.com/user-attachments/assets/3beb0966-fdb1-4c12-a47f-ed4e8240f8fd)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/027-agent-loop-animation.gif">Bản GIF</a></summary>

![Vòng lặp agent nhiều bước](/nghien-cuu/agents/12-factor-agents/assets/img/027-agent-loop-animation.gif)

</details>

`[Dịch]` Và DAG "được hiện thực hóa" (materialized) sinh ra sẽ trông đại khái như sau:

![DAG sinh ra từ vòng lặp agent](/nghien-cuu/agents/12-factor-agents/assets/img/027-agent-loop-dag.png)

### Vấn đề với mẫu "lặp cho tới khi giải xong"

`[Dịch]` Những vấn đề lớn nhất của mẫu này:

- **Agent bị lạc khi context window quá dài** — chúng cứ loanh quanh thử lại đúng một cách tiếp cận hỏng, lặp đi lặp lại
- chỉ có vậy, nhưng thế là đủ để bẻ gãy cả cách tiếp cận

`[Dịch]` Kể cả khi bạn chưa từng tự viết một agent, bạn có lẽ đã thấy vấn đề **context dài** này khi làm việc với các công cụ coding dạng agent. Chúng cứ lạc sau một lúc và bạn phải mở một chat mới.

`[Dịch]` Tôi thậm chí sẽ mạnh dạn nêu ra điều mà tôi nghe qua rất nhiều lần, và **bạn** có lẽ cũng đã tự đúc kết được:

> #### **Kể cả khi model hỗ trợ context window dài hơn và dài hơn nữa, bạn LUÔN LUÔN đạt kết quả tốt hơn với một prompt và context nhỏ, tập trung**

`[Dịch]` Hầu hết những người xây dựng tôi trò chuyện đều **gạt ý tưởng "vòng lặp tool calling" sang một bên** khi họ nhận ra rằng bất cứ thứ gì vượt quá 10–20 lượt sẽ trở thành một mớ hỗn độn mà LLM không thể phục hồi. Kể cả khi agent đúng 90% số lần, con số đó vẫn còn xa "đủ tốt để giao vào tay khách hàng". Bạn có tưởng tượng nổi một web app sập 10% số lần tải trang không?

`[Dịch]` **Cập nhật 2025-06-09** — tôi rất thích cách [@swyx](https://x.com/swyx/status/1932125643384455237) diễn đạt điều này:

<a href="https://x.com/swyx/status/1932125643384455237"><img width="593" alt="Tweet của swyx về vòng lặp tool calling" src="/nghien-cuu/agents/12-factor-agents/assets/img/brief-history-swyx-tweet.png" /></a>

### Cái thực sự hiệu quả — micro agent

`[Dịch]` Một thứ mà tôi **đã** thấy khá nhiều ngoài thực tế là lấy mẫu agent và **rắc nó vào một DAG rộng hơn, tất định hơn**.

![DAG với micro agent xen vào](/nghien-cuu/agents/12-factor-agents/assets/img/028-micro-agent-dag.png)

`[Dịch]` Bạn có thể hỏi — "vậy thì tại sao lại dùng agent làm gì?" — chúng ta sẽ bàn ngay sau đây, nhưng về cơ bản, việc để **model ngôn ngữ quản lý những tập nhiệm vụ được khoanh vùng tốt** giúp dễ dàng đưa **phản hồi trực tiếp từ con người** vào, dịch nó thành các bước workflow mà không bị xoáy vào vòng lặp lỗi context. ([factor 1](./factor-01-ngon-ngu-tu-nhien-thanh-tool-call.md), [factor 3](./factor-03-so-huu-context-window.md), [factor 7](./factor-07-lien-he-con-nguoi-bang-tool-call.md)).

> #### để model ngôn ngữ quản lý những tập nhiệm vụ được khoanh vùng tốt giúp dễ dàng đưa phản hồi trực tiếp từ con người vào... mà không bị xoáy vào vòng lặp lỗi context

### Một micro agent ngoài đời thực

`[Dịch]` Đây là ví dụ về cách code tất định có thể chạy một micro agent chịu trách nhiệm cho các bước human-in-the-loop khi triển khai (deployment).

![Deploybot — tổng quan](/nghien-cuu/agents/12-factor-agents/assets/img/029-deploybot-high-level.png)

- **Con người** Merge PR vào nhánh `main` của GitHub
- **Code tất định** Triển khai lên môi trường staging
- **Code tất định** Chạy test đầu-cuối (e2e) trên staging
- **Code tất định** Giao cho agent để triển khai prod, với context ban đầu: "deploy SHA 4af9ec0 to production"
- **Agent** gọi `deploy_frontend_to_prod(4af9ec0)`
- **Code tất định** yêu cầu con người phê duyệt hành động này
- **Con người** Từ chối hành động kèm phản hồi "can you deploy the backend first?"
- **Agent** gọi `deploy_backend_to_prod(4af9ec0)`
- **Code tất định** yêu cầu con người phê duyệt hành động này
- **Con người** phê duyệt hành động
- **Code tất định** thực thi triển khai backend
- **Agent** gọi `deploy_frontend_to_prod(4af9ec0)`
- **Code tất định** yêu cầu con người phê duyệt hành động này
- **Con người** phê duyệt hành động
- **Code tất định** thực thi triển khai frontend
- **Agent** xác định nhiệm vụ đã hoàn thành thành công, xong!
- **Code tất định** chạy test đầu-cuối trên production
- **Code tất định** nhiệm vụ hoàn tất, HOẶC chuyển sang agent rollback để xem xét lỗi và có thể khôi phục

[![Deploybot — animation](/nghien-cuu/agents/12-factor-agents/assets/img/033-deploybot.gif)](https://github.com/user-attachments/assets/deb356e9-0198-45c2-9767-231cb569ae13)

<details>
<summary><a href="/nghien-cuu/agents/12-factor-agents/assets/img/033-deploybot.gif">Bản GIF</a></summary>

![Deploybot — animation](/nghien-cuu/agents/12-factor-agents/assets/img/033-deploybot.gif)

</details>

`[Dịch]` Ví dụ này dựa trên một [agent mã nguồn mở có thật mà chúng tôi đã phát hành để quản lý việc triển khai tại HumanLayer](https://github.com/got-agents/agents/tree/main/deploybot-ts) — đây là một cuộc trò chuyện thật tôi có với nó tuần trước:

![Deploybot — hội thoại thực tế](/nghien-cuu/agents/12-factor-agents/assets/img/035-deploybot-conversation.png)

`[Dịch]` Chúng tôi **chưa** đưa cho agent này một đống tool hay nhiệm vụ khổng lồ. Giá trị chính nằm ở chỗ **LLM phân tích phản hồi dạng văn bản tự nhiên của con người và đề xuất một hướng hành động cập nhật**. Chúng tôi cô lập nhiệm vụ và context càng nhiều càng tốt để giữ LLM tập trung vào một workflow nhỏ, 5–10 bước.

`[Dịch]` Đây là một [demo support/chatbot kinh điển hơn](https://x.com/chainlit_io/status/1858613325921480922).

### Vậy thực ra một agent là gì?

- **prompt** — nói cho LLM biết phải hành xử thế nào, và nó có những "tool" nào. Output của prompt là một đối tượng JSON mô tả bước kế tiếp trong workflow ("tool call" hay "function call"). ([factor 2](./factor-02-so-huu-prompt.md))
- **câu lệnh switch** — dựa trên JSON mà LLM trả về, quyết định làm gì với nó. (một phần của [factor 8](./factor-08-so-huu-luong-dieu-khien.md))
- **context tích lũy** — lưu danh sách các bước đã xảy ra và kết quả của chúng ([factor 3](./factor-03-so-huu-context-window.md))
- **vòng lặp for** — cho tới khi LLM phát ra một tool call kiểu "Terminal" (hoặc phản hồi văn bản thuần), thêm kết quả của câu lệnh switch vào context window và yêu cầu LLM chọn bước kế tiếp. ([factor 8](./factor-08-so-huu-luong-dieu-khien.md))

![Bốn thành phần của một agent](/nghien-cuu/agents/12-factor-agents/assets/img/040-4-components.png)

`[Dịch]` Trong ví dụ "deploybot", chúng ta nhận được vài lợi ích nhờ **sở hữu luồng điều khiển và việc tích lũy context**:

- Trong **câu lệnh switch** và **vòng lặp for**, ta có thể **chiếm quyền điều khiển** để tạm dừng chờ input từ con người hoặc chờ các nhiệm vụ chạy dài hoàn tất
- Ta có thể **tuần tự hóa (serialize) context window** một cách dễ dàng để pause + resume
- Trong **prompt**, ta có thể tối ưu hết mức cách truyền chỉ dẫn và "những gì đã xảy ra tới giờ" cho LLM

`[Dịch]` [Phần II](https://github.com/humanlayer/12-factor-agents/blob/main/README.md#12-factor-agents) sẽ **hệ thống hóa những mẫu này** để chúng có thể được áp dụng nhằm thêm các tính năng AI ấn tượng vào bất kỳ dự án phần mềm nào, mà không cần phải "all-in" vào những cách hiện thực/định nghĩa thông thường của "AI agent".

---

## Ghi chú của người dịch

> [!NOTE]
> **Vì sao có bản này?** Trang [Vì sao lại là 12-factor agents?](./vi-sao-12-factor.md) dẫn lại phần tóm tắt ngắn trong `README.md`. Đây là **bản dài đầy đủ** từ `content/brief-history-of-software.md` — 12 mục, 15 hình minh họa, bao gồm cả bốn phần mà bản ngắn trong README không có (*"Bạn không nhất thiết phải nghe tôi"*, *"10–15 năm trước"*, *"Vấn đề với mẫu lặp cho tới khi giải xong"*, *"Cái thực sự hiệu quả — micro agent"*, *"Một micro agent ngoài đời thực"*, và *"Vậy thực ra một agent là gì?"*).
>
> **Toàn bộ ảnh** được tải về cục bộ tại `src/public/nghien-cuu/agents/12-factor-agents/assets/img/` để trang không phụ thuộc mạng. Các ảnh GIF động (vòng lặp agent, deploybot) được giữ ở cả hai dạng: link bấm mở bản đầy đủ, và khối `<details>` gập chứa GIF.
>
> **Khác biệt so với nguyên bản:** ảnh `195-factor-09-errors.gif` trong repository gốc bị **sai tên tệp** (tham chiếu `-09-` nhưng tệp thật là `195-factor-9-errors.gif`); bản dịch dùng tên tệp thật nên ảnh hiển thị được.

---

**Điều hướng:** [Mục lục](./) · [Vì sao lại là 12-factor agents? →](./vi-sao-12-factor.md)
