# 12-Factor Agents — Bản dịch toàn văn

Bản dịch tiếng Việt trọn bộ 12-Factor Agents của [Dex Horthy](https://github.com/dexhorthy) / [HumanLayer](https://humanlayer.dev), tách thành từng bài riêng theo đúng cấu trúc [repository gốc](https://github.com/humanlayer/12-factor-agents).

**Đối chiếu nguồn:** commit [`d20c728`](https://github.com/humanlayer/12-factor-agents/tree/d20c728368bf9c189d6d7aab704744decb6ec0cc) (2025-09-21).

> [!NOTE]
> **Quy ước dịch:** nội dung dịch trung thành với văn bản gốc, giữ giọng văn ngôi thứ nhất của tác giả. Thuật ngữ kỹ thuật cốt lõi (*Harness, Agent, Runtime, Model, Context, Prompt, Token, Tool, Reducer, Control Flow*) giữ nguyên tiếng Anh kèm chú giải tiếng Việt ở lần xuất hiện đầu. Code **không dịch** — chỉ dịch chú thích và văn bản giải thích.
>
> **Quy ước trình bày:** `[Dịch]` = văn bản dịch từ nguyên bản · `[Ghi chú]` = chú thích của người dịch.
>
> **Hình ảnh:** **toàn bộ 40 hình minh họa** trong repository gốc được tải về cục bộ tại `assets/img/` (38 tệp, ~38 MB) và chèn đúng vị trí như nguyên bản — không còn phụ thuộc vào máy chủ GitHub. Các ảnh GIF động (vòng lặp agent, unify state, pause/resume, compact errors, scope grow, deploybot) giữ nguyên dạng: bấm vào ảnh để mở bản đầy đủ, kèm khối `<details>` gập chứa GIF.

---

## Bối cảnh

- [Chúng ta đã tới đây thế nào: Lược sử phần mềm](./lich-su-phan-mem) — từ flow chart tới DAG orchestrator, tới lời hứa của agent, và vì sao mô hình "lặp cho tới khi xong" không trụ được
- [Vì sao lại là 12-factor agents?](./vi-sao-12-factor) — hành trình 70–80% chất lượng, và vì sao nên lấy khái niệm module hóa thay vì dấn hết vào framework

## 12 Factor

| # | Factor | Định nghĩa & Trọng tâm Kiến trúc (SA Focus) |
|---|---|---|
| 1 | [Natural Language to Tool Calls](./factor-01-ngon-ngu-tu-nhien-thanh-tool-call) | Chuyển đổi Ngôn ngữ Tự nhiên thành Lệnh gọi Công cụ Định kiểu (Typed Tool Calls) |
| 2 | [Own your prompts](./factor-02-so-huu-prompt) | Làm chủ Prompt — Coi Prompt là First-Class Code, loại bỏ trừu tượng hộp đen |
| 3 | [Own your context window](./factor-03-so-huu-context-window) | Chủ động kiểm soát Context Window — Tối đa hóa Mật độ Thông tin & Attention Budget |
| 4 | [Tools are just structured outputs](./factor-04-tool-chi-la-output-co-cau-truc) | Bản chất Công cụ chỉ là Đầu ra có Cấu trúc (Structured JSON Outputs) |
| 5 | [Unify execution state and business state](./factor-05-gop-execution-state-va-business-state) | Hợp nhất Trạng thái Thực thi và Trạng thái Nghiệp vụ thành một Event Log duy nhất |
| 6 | [Launch/Pause/Resume with simple APIs](./factor-06-launch-pause-resume) | Khởi chạy, Tạm dừng và Tiếp tục qua API Tối giản phục vụ tác vụ chạy dài |
| 7 | [Contact humans with tool calls](./factor-07-lien-he-con-nguoi-bang-tool-call) | Tương tác với Con người Dưới dạng Lệnh gọi Tool (Human-as-an-Async-Tool) |
| 8 | [Own your control flow](./factor-08-so-huu-luong-dieu-khien) | Làm chủ Luồng Điều khiển Hệ thống bằng State Machine tất định |
| 9 | [Compact Errors into Context Window](./factor-09-nen-loi-vao-context-window) | Nén và Cắt tỉa Lỗi trong Cửa sổ Ngữ cảnh (Self-Healing & Context Hygiene) |
| 10 | [Small, Focused Agents](./factor-10-agent-nho-tap-trung) | Kiến trúc Micro-Agents Đơn nhiệm & Chuyên biệt (Single Responsibility Principle) |
| 11 | [Trigger from anywhere](./factor-11-kich-hoat-tu-moi-noi) | Kích hoạt Đa kênh — Tiếp cận Người dùng tại Mọi Điểm Chạm (Multi-Channel Ingress) |
| 12 | [Make your agent a stateless reducer](./factor-12-agent-nhu-stateless-reducer) | Mô hình hóa Agent như một Stateless Reducer `(State, Event) => NextState` |

## Bổ sung

- [Factor 13 (Danh dự): Pre-fetch toàn bộ context bạn có thể cần](./factor-13-pre-fetch-context) — Kỹ thuật Chủ động Nạp trước Tri thức (Deterministic Pre-fetching)

---

## Sơ đồ tóm tắt (do người dịch vẽ)

Bốn sơ đồ dưới đây **không có trong nguyên bản** — chúng được vẽ thêm để tóm tắt kiến trúc cốt lõi của bộ nguyên lý. Hình minh họa gốc của từng factor nằm trong chính bài tương ứng.

**Bản đồ 12 factor theo tầng vận hành** — từ tầng đầu vào (dạy LLM sinh hành động) tới tầng vỏ vận hành (state, control flow) và tầng sản phẩm:

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/03-ban-do-12-factor.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

**Vòng lặp agent và 4 điểm chèn** — bốn nơi bạn có thể can thiệp thay vì giao hết cho model:

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/01-vong-lap-agent.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

**Vòng lặp naive vs vòng lặp do bạn sở hữu:**

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/02-naive-vs-so-huu.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

**Trạng thái bền vững, tạm dừng và con người trong vòng lặp:**

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/04-trang-thai-con-nguoi.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

---

**Xem thêm:** [Bản phân tích kiến trúc](../phan-tich-kien-truc) — đọc repository như một bộ nguyên lý kỹ thuật và đối chiếu với Harness Engineering.
