# Factor 2: Own your prompts (Làm chủ Prompt — Coi Prompt là First-Class Code)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-02-own-your-prompts.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-02-own-your-prompts.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` **Tuyệt đối không ủy thác việc thiết kế Prompt (Prompt Engineering) cho các lớp trừu tượng của framework.**

![Sở hữu prompt của bạn, đừng để framework giấu](/nghien-cuu/agents/12-factor-agents/assets/img/120-own-your-prompts.png)

`[Dịch]` Đây [không phải là quan điểm mới trong cộng đồng AI Engineering](https://hamel.dev/blog/posts/prompt/).

![Vấn đề của cách tiếp cận “hộp đen”](/nghien-cuu/agents/12-factor-agents/assets/img/factor-02-blackbox-problem.png)

`[Dịch]` Nhiều framework hiện nay áp dụng cách tiếp cận "hộp đen" (Black-box Abstraction) dạng:

```python
agent = Agent(
    role="DevOps Engineer",
    goal="Ensure smooth deployments",
    personality="Precise and cautious",
    tools=[tool1, tool2, tool3]
)

task = Task(
    instructions="Deploy backend service",
    expected_output=OutputModel
)

result = agent.run(task)
```

`[Dịch]` Cách đóng gói này rất tiện lợi để dựng nhanh bản PoC (Proof-of-Concept) ban đầu với một số prompt dựng sẵn. Tuy nhiên, trong môi trường Production, sự trừu tượng hóa này trở thành **rào cản kiến trúc nghiêm trọng**: cực kỳ khó tinh chỉnh (fine-tune), không thể kiểm soát chính xác từng token đi vào LLM, và bất khả thi khi cần debug các lỗi hành vi phức tạp.

`[Dịch]` Thay vào đó, **hãy trực tiếp sở hữu prompt của bạn** và đối xử với chúng như **mã nguồn cốt lõi (First-Class Code / First-Class Citizens)**:

```rust
function DetermineNextStep(thread: string) -> DoneForNow | ListGitTags | DeployBackend | DeployFrontend | RequestMoreInformation {
  prompt #"
    {{ _.role("system") }}

    You are a helpful assistant that manages deployments for frontend and backend systems.
    You work diligently to ensure safe and successful deployments by following best practices
    and proper deployment procedures.

    Before deploying any system, you should check:
    - The deployment environment (staging vs production)
    - The correct tag/version to deploy
    - The current system status

    You can use tools like deploy_backend, deploy_frontend, and check_deployment_status
    to manage deployments. For sensitive deployments, use request_approval to get
    human verification.

    Always think about what to do first, like:
    - Check current deployment status
    - Verify the deployment tag exists
    - Request approval if needed
    - Deploy to staging before production
    - Monitor deployment progress

    {{ _.role("user") }}

    {{ thread }}

    What should the next step be?
  "#
}
```

`[Dịch]` *(Ví dụ trên sử dụng [BAML](https://github.com/boundaryml/baml) để định kiểu và sinh prompt, nhưng bạn có thể áp dụng nguyên lý này với bất kỳ công cụ template hóa nào, hoặc thậm chí là string template thuần trong ngôn ngữ lập trình của bạn).*

`[Dịch]` Nếu chữ ký hàm (function signature) ở trên trông có vẻ khác lạ, chúng ta sẽ phân tích sâu cơ chế này tại [Factor 4 — Tool chỉ là output có cấu trúc](./factor-04-tool-chi-la-output-co-cau-truc.md).

---

### Lợi ích Chiến lược của việc Làm chủ Prompt

Dưới lăng kính của Kiến trúc sư Giải pháp, việc kiểm soát trực tiếp Prompt mang lại 5 giá trị cốt lõi:

1. **Kiểm soát Hoàn toàn (Full Deterministic Control):** Viết chính xác các chỉ dẫn nghiệp vụ mà Agent cần, triệt tiêu hoàn toàn các side-effect từ prompt ẩn do framework tự ý chèn vào.
2. **Kiểm thử & Đánh giá Tự động (Evals & CI/CD Pipeline):** Xây dựng bộ test suite, regression tests và eval metrics cho prompt tương tự như quy trình kiểm thử đơn vị (Unit Test) cho code thông thường.
3. **Chu kỳ Lặp Nhanh (Rapid Iteration):** Nhanh chóng điều chỉnh và tối ưu hóa câu từ dựa trên telemetry và metrics thu thập từ môi trường thực tế.
4. **Minh bạch & Kiểm toán (Transparency & Auditing):** Đội ngũ kỹ sư luôn nắm rõ 100% ngữ cảnh và chỉ dẫn đang chi phối hành vi của mô hình.
5. **Khai thác Linh hoạt các Kỹ thuật Nâng cao (Role Hacking & Prefilling):** Dễ dàng áp dụng các kỹ thuật thao túng role (`user`/`assistant`), prefilling nội dung phản hồi, hoặc định hướng token đầu ra mà các framework hộp đen thường khóa cứng.

> **Ghi nhớ:** Prompt chính là **giao diện lập trình (API Interface)** giữa logic phần mềm của bạn và mô hình ngôn ngữ. Việc nắm toàn quyền kiểm soát prompt là điều kiện tiên quyết để xây dựng hệ thống Agent ổn định và sẵn sàng cho môi trường Production.

---

**Điều hướng:** [← Factor 1: Natural Language to Tool Calls](./factor-01-ngon-ngu-tu-nhien-thanh-tool-call.md) · [Mục lục](./) · [Factor 3: Own your context window →](./factor-03-so-huu-context-window.md)

