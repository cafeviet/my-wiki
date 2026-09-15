# 12-Factor Agents: nguyên lý xây dựng Agent đủ tin cậy để đưa vào production

> **Mục tiêu bài viết:** phân tích `humanlayer/12-factor-agents` như một bộ **nguyên lý kỹ thuật (engineering principles)** cho Agent production, làm rõ hàm ý kiến trúc và mối liên hệ với **Harness Engineering** — đồng thời nói rõ repository này *không* phải là một runtime hay framework.
>
> **Nguồn gốc:** [github.com/humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents). Toàn bộ nội dung bài này được đối chiếu trực tiếp với source ở commit `d20c728` (2025-09-21), xem `40_RESULTS/T001_RESULT`.

**Quy ước nhãn trong bài:** `[Fact]` = đọc trực tiếp từ repository · `[Inference]` = suy luận kiến trúc của người viết · `[Recommendation]` = khuyến nghị áp dụng.

> [!TIP]
> **Đang tìm bản dịch?** → [Bản dịch toàn văn 12-Factor Agents](./bo-12-factor/) — dịch sát nguyên bản, tách thành 13 bài riêng theo cấu trúc repository gốc, kèm đầy đủ 40 hình minh họa gốc và 4 sơ đồ tóm tắt.
>
> Trang này là **bài phân tích kiến trúc**: đọc repository như một bộ nguyên lý kỹ thuật và đối chiếu với Harness Engineering.

---

## 1. 12-Factor Agents là gì?

`[Fact]` Repository này **không phải** một runtime, không phải một framework, và không phải thư viện cài đặt được. Nó là một **bản tuyên ngôn nguyên lý (principles guide)** — tự đặt mình "in the spirit of [12 Factor Apps](https://12factor.net)".

Câu hỏi mà tác giả đặt ra ngay đầu README chính là toàn bộ luận đề của dự án:

> "What are the principles we can use to build LLM-powered software that is actually good enough to put in the hands of production customers?"

Giấy phép cũng nói lên bản chất dự án: **nội dung** theo CC BY-SA 4.0, **code** theo Apache 2.0 — tức phần "code" chỉ là minh hoạ, phần giá trị nằm ở văn bản nguyên lý.

`[Fact]` Bối cảnh tác giả (Dex Horthy / HumanLayer): ông đã thử nhiều framework ("from the plug-and-play crew/langchains to the 'minimalist' smolagents ... to the 'production grade' langraph, griptape"), và quan sát rằng *"I don't see a lot of frameworks in production customer-facing agents"* — hầu hết đội mạnh đang tự dựng stack của họ.

`[Inference]` Đây là lý do repository tồn tại: nó không cạnh tranh với framework ở tầng runtime, mà chiếm tầng **quyết định thiết kế** — nơi các framework thường che mất lựa chọn thay vì phơi ra lựa chọn.

---

## 2. Luận điểm trung tâm

`[Fact]` Phát hiện cốt lõi, nguyên văn từ README:

> "A lot of them are mostly deterministic code, with LLM steps sprinkled in at just the right points to make the experience truly magical."

> "Agents, at least the good ones, don't follow the 'here's your prompt, here's a bag of tools, loop until you hit the goal' pattern. Rather, they are comprised of mostly just software."

`[Fact]` Repository cũng mô tả vòng lặp agent "ngây thơ" gồm 3–4 bước: (1) LLM xác định bước kế tiếp và xuất JSON có cấu trúc, (2) code tất định thực thi tool call, (3) kết quả được ghi lại vào context window, (4) lặp cho tới khi bước kế tiếp là "done" — và nhận xét thẳng rằng *"it turns out this doesn't quite work"*.

`[Inference]` Diễn giải kiến trúc: đây là lập luận **đảo ngược tỉ lệ trách nhiệm**. Trong mô hình "autonomous agent", LLM giữ phần lớn quyền quyết định và software chỉ là bộ thực thi tool. Trong mô hình 12-Factor, **software tất định giữ quyền điều khiển**, còn LLM được gọi vào như một *hàm suy luận* tại những điểm mà quy tắc tất định không viết nổi (hiểu ngôn ngữ tự nhiên, chọn hướng đi mơ hồ, sinh cấu trúc từ văn bản thô).

`[Inference]` Hệ quả thực tiễn: mọi thứ khó trong production — retry, timeout, kiểm toán, phê duyệt, chi phí, test — đều là bài toán của software tất định. Càng đẩy quyền quyết định cho LLM, càng nhiều thứ trở thành "không test được". 12-Factor Agents là bộ quy tắc để **kéo ranh giới đó về phía code**.

---

## 3. Bảng tóm tắt 12 factors

`[Fact]` Toàn bộ tiêu đề dưới đây được đối chiếu verbatim với `content/factor-NN-*.md`.

| # | Factor (nguyên bản) | Ý nghĩa kiến trúc | Nhãn |
|---|---|---|---|
| 1 | Natural Language to Tool Calls | Dịch ngôn ngữ tự nhiên → đối tượng có cấu trúc. Đây là điểm chèn (insertion point) cơ bản nhất của LLM. | Fact |
| 2 | Own your prompts | Không giao prompt engineering cho framework. Prompt là tài sản của bạn. | Fact |
| 3 | Own your context window | Context là một **bề mặt kỹ thuật** do bạn dựng, không phải chuỗi message chuẩn. "Everything is context engineering." | Fact |
| 4 | Tools are just structured outputs | Tool bản chất là structured output của LLM, kích hoạt code tất định. | Fact |
| 5 | Unify execution state and business state | Gộp state vận hành (bước hiện tại, trạng thái chờ, retry) với business state. | Fact + caveat |
| 6 | Launch/Pause/Resume with simple APIs | Agent là chương trình — cần API đơn giản để chạy, dừng, hỏi trạng thái, tiếp tục. | Fact |
| 7 | Contact humans with tool calls | Liên hệ con người cũng là một tool call, không phải đường riêng. | Fact |
| 8 | Own your control flow | Luồng điều khiển thuộc về code của bạn, kể cả cấu trúc vòng lặp. | Fact |
| 9 | Compact Errors into Context Window | Nén lỗi và nhét lại vào context để agent tự sửa ("self-healing"). | Fact |
| 10 | Small, Focused Agents | Nhiều agent nhỏ, tập trung, thay vì một agent khổng lồ. | Fact |
| 11 | Trigger from anywhere, meet users where they are | Kích hoạt từ Slack/email/SMS/webhook; agent trả lời qua chính kênh đó. | Fact |
| 12 | Make your agent a stateless reducer | Xem agent như một bộ rút gọn (reducer) phi trạng thái. | Fact (yếu) |

`[Fact]` **Bổ sung quan trọng so với bản tóm tắt trước đó:** repository còn có một factor **không chính thức**, nằm trong mục "Honorable Mentions / other advice":

> **Factor 13: Pre-fetch all the context you might need** — nếu khả năng cao model sẽ gọi tool X, đừng tốn round-trip token để bảo nó đi lấy; hãy nạp trước.

`[Inference]` Việc Factor 13 không được đánh số chính thức là hợp lý: nó là một **tối ưu latency/cost** ở tầng triển khai, không phải một nguyên lý cấu trúc như 12 factor kia. Nhưng nó đáng nhớ vì nó thừa nhận một sự thật vận hành: mỗi vòng LLM là một round-trip đắt và chậm.

---

## 4. Phân tích sâu

### 4.1 Tool as Structured Output — ý tưởng chịu lực nhất

`[Fact]` Nguyên văn: *"Tools don't need to be complex. At their core, they're just structured output from your LLM that triggers deterministic code."*

`[Inference]` Đây là factor **chịu lực nhất** của toàn bộ bộ nguyên lý, vì nó định nghĩa lại ranh giới tin cậy. "Tool call" không phải một quyền năng huyền bí mà model sở hữu; nó chỉ là JSON mà code của bạn parse, đối chiếu schema, rồi **quyết định** có thực thi hay không.

Hệ quả:

- **Tool call = ý định có cấu trúc (structured intent)**, không phải mệnh lệnh đã thi hành.
- Mọi chính sách — allowlist, phân quyền, giới hạn giá trị, yêu cầu phê duyệt — sống ở tầng code tất định, ngay sau bước parse.
- `[Recommendation]` Với hệ thống enterprise, đây là điểm móc nối tự nhiên nhất cho **policy engine**: validate schema trước, validate quyền sau, rồi mới execute.

### 4.2 Context (Factor 3) — bề mặt kỹ thuật, không phải prompt

`[Fact]` *"Everything is context engineering. LLMs are stateless functions that turn inputs into outputs. To get the best outputs, you need to give them the best inputs."*

`[Fact]` Repository liệt kê các thành phần cấu thành context: prompt/instruction; tài liệu hoặc dữ liệu truy hồi (RAG); state, tool call và kết quả trước đó; message/sự kiện từ các lịch sử hội thoại liên quan (memory); và chỉ dẫn về **định dạng structured output** mong muốn.

`[Inference]` Điểm mạnh về mặt kiến trúc: repository tách **"context là gì"** khỏi **"định dạng message trông thế nào"**. Nó nói rõ bạn *không nhất thiết* phải dùng định dạng message chuẩn để truyền context. Điều này mở đường cho việc nén (compaction), tóm tắt, chèn pre-fetch, và tái cấu trúc context theo cost — tất cả đều là quyết định của bạn, không phải của framework.

### 4.3 State (Factor 5) — lời khuyên có caveat, đọc kỹ

`[Fact]` Repository phân biệt:
- **Execution state**: bước hiện tại, bước kế tiếp, trạng thái chờ, số lần retry.
- **Business state**: những gì đã xảy ra trong workflow (danh sách message OpenAI, danh sách tool call và kết quả).

`[Fact]` **Caveat nguyên văn, và đây là chỗ dễ bị trích dẫn sai nhất:** *"This separation creates complexity that may be worthwhile, but may be overkill for your use case. As always, it's up to you to decide what's right for your application. But don't think you `have` to manage them separately."*

`[Inference]` Đây không phải mệnh lệnh "hãy gộp state", mà là **cảnh báo chống over-engineering**. Với agent nhỏ, tách hai loại state là chi phí vô ích. Với hệ thống nhiều agent, chạy dài, có người phê duyệt, việc tách có thể chính đáng. Câu hỏi kiểm tra đúng là: *"Nếu gộp, tôi có mất khả năng nào tôi thực sự cần không?"*

### 4.4 Pause / Resume (Factor 6)

`[Fact]` Nguyên văn: *"Agents are just programs, and we have things we expect from how to launch, query, resume, and stop them."* Ba yêu cầu được nêu: khởi chạy bằng API đơn giản; **pause** khi gặp thao tác dài; **resume từ ngoài** (webhook) mà không cần tích hợp sâu với orchestrator.

`[Fact]` Repository nói rõ factor này *"closely related to factor 5 and factor 8, but can be implemented independently"*.

`[Inference]` Hàm ý lớn nhất: **pause/resume là bài toán persistence, không phải bài toán async**. Nếu không lưu được đủ state để dựng lại context ở lần chạy sau, bạn không resume được — bạn chỉ restart. Đây chính là cây cầu nối Factor 5, 6 và 8.

### 4.5 Human-in-the-loop (Factor 7)

`[Fact]` Lập luận kỹ thuật rất cụ thể: API LLM mặc định buộc model chọn ngay token đầu tiên giữa **plaintext** và **structured data** — một *"HIGH-STAKES token choice"*. Với câu hỏi thời tiết, token đầu là `"the"`; với `fetch_weather`, token đầu là `|JSON>`.

`[Fact]` Khuyến nghị của repository: cho LLM **luôn** xuất JSON, rồi khai báo ý định bằng token ngôn ngữ tự nhiên như `request_human_input` hay `done_for_now` — thay vì phải có một "tool" riêng cho việc hỏi người. Repository cũng tự hạ thấp kỳ vọng: *"you might not get any performance boost from this, but you should experiment"*.

`[Inference]` Đây là lập luận **thống nhất giao diện**: con người trở thành một "tool" giống mọi tool khác, nên control flow không cần nhánh đặc biệt. `[Recommendation]` Với enterprise, đây chính là chỗ đặt **approval gate**: `request_human_input` cho thao tác rủi ro cao — chính xác là điều card Kanban `R3` làm trong hệ handoff của chúng ta.

### 4.6 Control Flow (Factor 8) — yếu tố giải phóng

`[Fact]` *"If you own your control flow, you can do lots of fun things."* Repository liệt kê những thứ có thể chèn khi bạn sở hữu vòng lặp: tóm tắt/cache kết quả tool call; LLM-as-judge trên structured output; nén context window và quản lý memory; logging/tracing/metrics; rate limiting phía client; durable sleep / pause / "wait for event".

`[Fact]` Ví dụ ba nhánh control flow: `request_clarification` (model cần thêm thông tin → thoát vòng lặp, chờ người); `fetch_git_tags` (thao tác rẻ → thực thi, gắn vào context, quay lại model ngay); `deploy_backend` (rủi ro cao → thoát vòng lặp, chờ người phê duyệt).

`[Inference]` Đây là factor **có tính "giải phóng" cao nhất**: nó nói rằng có nhiều loại tool call cần **thoát khỏi vòng lặp**, chứ không phải cứ lặp tới khi xong. Khi vòng lặp thuộc về framework, những nhánh này trở nên khó hoặc bất khả. Cụ thể hơn: **chi phí, độ trễ, rủi ro và khả năng kiểm toán đều được quyết định ở đây.**

### 4.7 Error Recovery (Factor 9) — chi phí gần bằng 0

`[Fact]` Lợi ích "self-healing": với tác vụ ngắn, LLM thất bại một tool call thì có khả năng đọc thông báo lỗi / stack trace và điều chỉnh ở lần gọi sau. Repository nhấn mạnh: *"Most frameworks implement this, but you can do JUST THIS without doing any of the other 11 factors."*

`[Inference]` Đây là factor **rẻ nhất và nên làm đầu tiên** — một `try/except` gắn lỗi vào context rồi lặp lại. Nó cũng là ví dụ cho thấy bộ nguyên lý này được thiết kế **dùng rời rạc được**, không phải all-or-nothing.

### 4.8 Small, Focused Agents (Factor 10)

`[Fact]` Định cỡ cụ thể: giữ agent trong khoảng **3–10, tối đa khoảng 20 bước**, vì *"As context grows, LLMs are more likely to get lost or lose focus."* Lợi ích được nêu: context dễ quản lý, trách nhiệm rõ, độ tin cậy cao hơn, dễ test, dễ debug.

`[Fact]` Repository **tự đặt câu hỏi ngược** — "What if LLMs get smarter?" — và trả lời: vẫn cần. Lý do: agent nhỏ cho kết quả *ngay hôm nay*, đồng thời chuẩn bị để **mở rộng dần** scope khi context window trở nên đáng tin hơn.

`[Inference]` Đây thực chất là lời khuyên **quản lý rủi ro theo độ phức tạp**, tương tự việc refactor một codebase lớn thành các module có ranh giới rõ — repository tự so sánh như vậy. `[Recommendation]` Ranh giới agent nên trùng với ranh giới **trách nhiệm và quyền hạn**, vì đó cũng là ranh giới bạn muốn kiểm toán.

### 4.9 Event-driven triggers (Factor 11)

`[Fact]` Ba lợi ích được nêu: **meet users where they are** (Slack/email/SMS → giao diện giống "đồng nghiệp số"); **outer loop agents** (agent được kích hoạt bởi sự kiện, cron, sự cố, chạy 5–90 phút rồi hỏi người khi tới điểm quan trọng); **high stakes tools** (nếu loop con người vào nhanh, có thể cho agent quyền thao tác rủi ro cao hơn như gửi email ra ngoài, cập nhật production data).

`[Inference]` Đây là chỗ bộ nguyên lý **chạm vào governance** chứ không chỉ kỹ thuật. `[Fact]` Repository nói rõ *"Maintaining clear standards gets you auditability"*. `[Inference]` Muốn cho agent quyền cao hơn, phải có kênh đưa con người vào nhanh — năng lực tổ chức, không phải năng lực model.

### 4.10 Stateless Reducer (Factor 12) — đọc có mức

`[Fact]` **Đây là factor yếu nhất về mặt bằng chứng, và repository tự nói vậy:** *"Okay so we're over 1000 lines of markdown at this point. This one is mostly just for fun."* Nội dung chính chỉ là hai hình minh hoạ (stateless reducer, agent như `foldl`).

`[Inference]` Giá trị thật của nó là **khung khái niệm**: nếu agent là hàm `(state, event) → state`, thì mọi lần "resume" chỉ là phát lại tập sự kiện — không cần lưu stack thực thi. `[Recommendation]` Hãy trình bày nó như **cách nghĩ**, không phải yêu cầu thi hành; đừng dùng nó để biện minh cho một thiết kế cụ thể.

---

## 5. Mapping sang Harness Engineering

`[Fact]` **Repository không định nghĩa và không sử dụng thuật ngữ "Harness Engineering".** Chuỗi này không xuất hiện trong toàn bộ hướng dẫn. Vì vậy mọi mapping dưới đây là `[Inference]` — diễn giải của người viết, không phải phát biểu của repository.

`[Inference]` Nếu hiểu **Harness** là phần vỏ tất định bọc quanh model để biến suy luận thành hành vi có thể vận hành (điều khiển vòng lặp, dựng context, quản lý state, gọi tool, kiểm soát người), thì bộ nguyên lý này thực chất là **đặc tả yêu cầu cho Harness**.

| Factor | Ánh xạ vào tầng Harness | Mức độ |
|---|---|---|
| 3 — Own your context window | Context builder: dựng/nén/tái cấu trúc input, không phó mặc cho framework | Rất mạnh |
| 4 — Tools are structured outputs | Tool gateway: parse + validate + authorize trước khi execute | Rất mạnh |
| 8 — Own your control flow | Loop engine: quyết định lặp, thoát, chờ, phê duyệt | Rất mạnh |
| 5 — Unify state | State store: gộp execution + business state | Mạnh (có caveat) |
| 6 — Launch/Pause/Resume | Durable execution: lưu đủ state để dựng lại context | Mạnh |
| 12 — Stateless reducer | Mô hình khái niệm cho replay/reducer trong Harness | Khái niệm |
| 1, 2, 4 | Prompt/tool contract layer | Mạnh |
| 7, 11 | Human/interface layer: approval gate, kênh tương tác | Mạnh |
| 9, 10 | Reliability layer: self-heal, chia nhỏ agent | Vừa |

`[Inference]` Đọc theo cách này, đóng góp chịu lực nhất của repository cho Harness Engineering là **4 + 8**: tool call là *ý định có cấu trúc* do Harness diễn giải, và luồng điều khiển thuộc về Harness. Hai điều này chính là định nghĩa vận hành của một Harness — mọi thứ còn lại là chi tiết triển khai.

`[Fact]` Một **phản biện công bằng** cần nêu: `[Fact]` repository *không* hoàn toàn chống framework. README viết: *"There are some core principles that make agents great, and you will get most/all of them if you pull in a framework. BUT, the fastest way I've seen ... is to take small, modular concepts from agent building, and incorporate them into their existing product."* `[Fact]` Repository còn tự liên kết framework của chính mình (`humanlayer/kubechain`) kèm chú thích tự trào *"We ignored all our own advice"*. `[Inference]` Vậy luận điểm đúng đắn là: **sở hữu các quyết định**, chứ không nhất thiết phải viết tay mọi thứ.

---

## 6. Điều 12-Factor Agents chưa bao phủ đầy đủ cho enterprise

`[Inference]` Đây là **suy luận dựa trên sự vắng mặt (gap-by-omission)** — repository không tuyên bố về những thiếu hụt này. Các chủ đề dưới đây không xuất hiện như những factor riêng trong hướng dẫn:

| Lĩnh vực enterprise | Trạng thái trong repo | Hàm ý |
|---|---|---|
| Security / threat model | Không có factor riêng | Prompt injection, tool poisoning, data exfiltration cần lớp phòng thủ ngoài bộ nguyên lý |
| Identity / Authorization | Không có factor riêng | Không định nghĩa danh tính agent, uỷ quyền, delegation, scoping quyền |
| Cost governance | Chỉ gián tiếp (Factor 13 pre-fetch, Factor 10 context nhỏ) | Không có ngân sách token/agent, quota, hay accounting theo tenant |
| Runtime isolation | Không có | Không bàn sandbox, container, egress policy cho tool thực thi |
| Lifecycle governance | Không có | Không bàn versioning agent, rollout, deprecation, migration state |
| Formal evaluation | Không có | Factor 10 nhắc "easier testing" như lợi ích, nhưng không định nghĩa eval, eval set, hay gate |
| Observability chuẩn hoá | Chỉ là gợi ý trong Factor 8 ("logging, tracing, and metrics") | Không có mô hình trace/schema thống nhất giữa các agent |
| Multi-tenant / data boundaries | Không có | Không bàn cô lập dữ liệu giữa khách hàng |

`[Inference]` Cần nói rõ: **đây là thiếu hụt hợp lý, không phải lỗi của repository.** Nó tự giới hạn ở tầng "nguyên lý thiết kế agent", nên không có nghĩa vụ bao phủ governance hay security. Nhưng nếu đọc bộ nguyên lý này như một kiến trúc enterprise hoàn chỉnh thì đó là **hiểu sai phạm vi** — và đây là cái bẫy dễ mắc nhất.

`[Recommendation]` Cách dùng đúng: 12 factor là **tầng giữa** của một kiến trúc lớn hơn. Phía trên cần thêm: identity/authorization, cost governance, eval. Phía dưới cần thêm: sandbox, observability, data isolation.

---

## 7. Khi nào nên áp dụng / khi nào không

`[Inference]` **Nên áp dụng khi:**

- Sản phẩm đã có hình dạng tương đối rõ và workflow chính là **deterministic** — LLM chỉ chèn vào vài điểm.
- Cần đưa agent vào tay khách hàng thật, cần debug được sự cố cụ thể.
- Có yêu cầu phê duyệt của con người hoặc kiểm toán thao tác.
- Cần pause/resume qua thao tác dài mà không giữ tiến trình chạy suốt.
- Đội ngũ đã có kinh nghiệm software engineering và muốn tái dùng nó, thay vì học một abstraction mới.

`[Inference]` **Không nên (hoặc chưa nên) áp dụng khi:**

- Còn đang **khám phá bài toán** — chưa biết workflow nào là tất định. Ở giai đoạn này, framework cho tốc độ thử nghiệm.
- Prototype/demo ngắn hạn, tuổi thọ thấp.
- Bài toán thực sự mở (ví dụ nghiên cứu tự do), nơi không tồn tại graph tất định để viết.
- Đội ngũ nhỏ, không có nhu cầu vận hành dài hạn, và lợi ích sở hữu không bù được chi phí tự viết.

`[Inference]` Lưu ý về **thứ tự áp dụng**: repository nói Factor 9 có thể làm độc lập, và Factors 5/6/8 liên quan chặt nhưng *"can be implemented independently"*. Nghĩa là bộ nguyên lý này **không phải all-or-nothing** — một trong những điểm mạnh bị đánh giá thấp của nó.

---

## 8. Câu hỏi kiến trúc cần đặt ra

`[Recommendation]` Bộ câu hỏi dưới đây dùng để kiểm tra một thiết kế agent hiện có:

1. **Context:** Context window của tôi được dựng bởi code của tôi hay bởi framework? Tôi có kiểm soát được việc nén/tóm tắt/tái cấu trúc không?
2. **Tool contract:** Sau khi parse tool call, tôi có một tầng tất định validate schema **và** quyền trước khi execute không? Tool call có được coi là *ý định* hay bị coi là mệnh lệnh?
3. **State:** Nếu process chết giữa chừng, tôi dựng lại được context ở đúng điểm dừng không? State nào là execution state, state nào là business state, và việc tách đó có thực sự cần thiết?
4. **Control flow:** Những nhánh nào cần **thoát vòng lặp** (chờ người, chờ sự kiện, phê duyệt)? Vòng lặp có cho phép chèn các nhánh đó không?
5. **Human loop:** Kênh đưa con người vào nhanh tới mức nào? Có dùng được cho thao tác rủi ro cao không?
6. **Failure:** Lỗi có được nén lại và đưa vào context để tự sửa không, hay chỉ được log?
7. **Ranh giới agent:** Một agent của tôi chạy tối đa bao nhiêu bước? Nếu vượt 20 bước, tôi chia ở đâu — và ranh giới chia có trùng với ranh giới trách nhiệm/quyền hạn không?
8. **Enterprise gap:** Ai giữ security, identity, authorization, cost governance, runtime isolation, lifecycle governance, formal evaluation — nếu không phải repo này?
9. **Kiểm toán:** Với mỗi hành vi, tôi chứng minh được *ai/khi nào/dựa trên bằng chứng gì* đã cho phép nó chạy?
10. **Đo lường:** Tôi có eval set và gate đủ để biết thay đổi prompt/context/model làm agent tốt hơn hay tệ hơn không?

---

## 9. Kết luận

`[Inference]` Giá trị lâu bền của `12-factor-agents` không nằm ở 12 con số, mà ở **một lập luận chống trừu tượng hoá quá mức**. Khi ngành đang bán "autonomous agents", repository này đưa ra một phản đề đơn giản và khó phản bác: agent tốt trong production là **phần mềm tất định với LLM chèn vào đúng chỗ**.

Hệ quả là một danh sách các **lằn ranh trách nhiệm** phải thuộc về bạn: context của bạn, prompt của bạn, state của bạn, control flow của bạn. Ánh xạ sang Harness Engineering, đây là **đặc tả cho phần vỏ tất định** — không phải cho model, và không phải cho framework.

Điều repository **không** làm: nó không giải quyết security, identity, authorization, cost governance, runtime isolation, lifecycle governance, hay formal evaluation. Đọc nó như một kiến trúc enterprise hoàn chỉnh là hiểu sai phạm vi. Đọc nó như tầng giữa của một kiến trúc lớn hơn thì nó là một trong những tài liệu cô đọng và thực dụng nhất hiện có.

---

## 10. Sources / Nguồn

**Repository chính:**
- [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) — đối chiếu ở commit `d20c728368bf9c189d6d7aab704744decb6ec0cc` (2025-09-21)

**Từng factor (đã đọc trực tiếp):**
- [How We Got Here: A Brief History of Software](https://github.com/humanlayer/12-factor-agents/blob/main/content/brief-history-of-software.md)
- [Factor 1: Natural Language to Tool Calls](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-01-natural-language-to-tool-calls.md)
- [Factor 2: Own your prompts](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-02-own-your-prompts.md)
- [Factor 3: Own your context window](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md)
- [Factor 4: Tools are just structured outputs](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-04-tools-are-structured-outputs.md)
- [Factor 5: Unify execution state and business state](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-05-unify-execution-state.md)
- [Factor 6: Launch/Pause/Resume with simple APIs](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-06-launch-pause-resume.md)
- [Factor 7: Contact humans with tool calls](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md)
- [Factor 8: Own your control flow](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md)
- [Factor 9: Compact Errors into Context Window](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-09-compact-errors.md)
- [Factor 10: Small, Focused Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md)
- [Factor 11: Trigger from anywhere, meet users where they are](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-11-trigger-from-anywhere.md)
- [Factor 12: Make your agent a stateless reducer](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md)
- [Factor 13 (honorable mention): Pre-fetch all the context you might need](https://github.com/humanlayer/12-factor-agents/blob/main/content/appendix-13-pre-fetch.md)

**Nguồn tham chiếu được repository trích dẫn:**
- [12 Factor Apps](https://12factor.net) — nguồn cảm hứng cho định dạng bộ nguyên lý
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents) — mô hình agent mà repository phản biện
- [Library patterns: Why frameworks are evil](https://tomasp.net/blog/2015/library-frameworks/)
- [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- [Function Calling vs Structured Outputs vs JSON Mode](https://www.vellum.ai/blog/when-should-i-use-function-calling-structured-outputs-or-json-mode)

**Metadata repository (điểm thời gian — chụp lúc 2026-09-14T16:36+07:00 qua GitHub REST API):**

| Chỉ số | Giá trị |
|---|---|
| Stars | 25.842 |
| Forks | 1.967 |
| Open issues | 27 |
| Ngày tạo repo | 2025-03-30 |
| Lần push cuối (`pushed_at`) | 2025-09-21 |
| Branch mặc định | `main` |

> [!WARNING]
> Các chỉ số star/fork là **số chụp tại một thời điểm** và sẽ lệch theo thời gian. `pushed_at` (2025-09-21) là tín hiệu trung thực nhất về lần thay đổi nội dung cuối; trường `updated_at` của API phản ánh thay đổi metadata, không phải commit nội dung. Nội dung hướng dẫn ổn định, chưa có commit mới trong khoảng 12 tháng tính tới thời điểm chụp.

**Phân định nhãn trong bài này:**
- `[Fact]` — đọc trực tiếp từ source repository, trích dẫn nguyên văn khi quan trọng.
- `[Inference]` — suy luận kiến trúc của người viết, bao gồm toàn bộ mục 5 (Harness Engineering) và mục 6 (khoảng trống enterprise).
- `[Recommendation]` — khuyến nghị áp dụng, không phải phát biểu của repository.

**Bằng chứng thực thi:** xem `30_EXECUTION/T002_EXECUTION_LOG` và `40_RESULTS/T001_RESULT` trong handoff `12-FACTOR-AGENTS-WIKI`.
