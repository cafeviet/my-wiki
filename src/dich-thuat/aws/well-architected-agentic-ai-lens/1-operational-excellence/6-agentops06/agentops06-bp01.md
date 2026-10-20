# AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp

Kiểm thử phần mềm truyền thống, như các phép khẳng định khớp chính xác và các unit test xanh-hoặc-đỏ, có thể bỏ lỡ các chế độ lỗi quan trọng trong các hệ thống agentic. Một kim tự tháp kiểm thử bao phủ unit, integration, các bài kiểm thử đầu-cuối, và các lớp bóng (shadow) giúp các nhóm bắt được các hồi quy hành vi trước khi chúng đến được người dùng.

**Kết quả mong muốn:**

- Các hệ thống agent được bao phủ bởi một kim tự tháp kiểm thử gồm unit test, integration test, end-to-end test, và shadow test trong các môi trường sản xuất.
- Các pipeline kiểm thử tự động chạy trên mỗi thay đổi mã và cấu hình, cung cấp phản hồi nhanh về các hồi quy.
- Các chỉ số bao phủ kiểm thử được theo dõi và duy trì trên các ngưỡng xác định cho mọi năng lực agent.
- Các bài kiểm thử dùng đánh giá chất lượng theo ngữ nghĩa (semantic) thay vì so sánh khớp chính xác, để các đầu ra phi tất định không làm hỏng bộ kiểm thử.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ kiểm thử luồng thuận lợi mà không bao phủ các trường hợp biên, các điều kiện lỗi, và các đầu vào đối kháng.
- Chỉ dựa hoàn toàn vào các unit test mà không có integration và end-to-end test, bỏ lỡ các lỗi chỉ nổi lên khi các thành phần tương tác với các Tools và dịch vụ thực.
- Đối xử với kiểm thử agent như kiểm thử phần mềm truyền thống mà không tính đến các đầu ra LLM phi tất định, dùng khớp chuỗi chính xác thay vì các kiểm tra tương đương ngữ nghĩa.
- Chỉ chạy các bài kiểm thử trong các môi trường biệt lập mà không có kiểm thử bóng trong sản xuất, bỏ lỡ các hành vi đặc thù môi trường vốn chỉ biểu hiện với dữ liệu thực và các mẫu lưu lượng.
- Không duy trì các tập dữ liệu kiểm thử khi các năng lực tiến hóa, nên các bài kiểm thử trở nên lỗi thời và mất giá trị phát hiện hồi quy.

**Lợi ích khi áp dụng thực hành tốt này:**

- Một khung kiểm thử kỹ lưỡng cung cấp bằng chứng thực nghiệm cần thiết để kiểm định mỗi lần lặp hành vi, cho phép triển khai một cách tự tin.
- Các quy trình kiểm thử chuẩn hóa giúp kiểm định mọi thay đổi một cách nhất quán, bất kể ai thực hiện hay tiến độ khẩn cấp đến đâu.
- Đánh giá theo ngữ nghĩa chấp nhận sự biến thiên đầu ra chính đáng trong khi vẫn bắt được các hồi quy.
- Kiểm thử bóng kiểm định các thay đổi hành vi so với lưu lượng thực mà không phơi nhiễm người dùng với phiên bản mới.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Bốn lớp bao phủ bề mặt kiểm thử cho hầu hết các hệ thống agent.

Unit test, lớp nền, kiểm thử các thành phần riêng lẻ một cách biệt lập: các mẫu Prompt, logic gọi Tools, truy xuất bộ nhớ, định tuyến quyết định. Các phản hồi LLM có thể được giả lập (mock) ở nơi cần tính tất định, để các unit test giữ nhanh và tái lập được.

Integration test, lớp thứ hai, kiểm định các tương tác agent-Tools và agent-tới-agent trong một môi trường staging với các endpoint thực, vốn là nơi nhiều lỗi thú vị nổi lên.

End-to-end test, lớp thứ ba, kiểm định các luồng công việc hoàn chỉnh, và đây là nơi đánh giá theo ngữ nghĩa quan trọng hơn khớp chính xác. [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) xử lý đánh giá chất lượng theo ngữ nghĩa mà các bài kiểm thử end-to-end cần. 13 bộ đánh giá dựng sẵn của AgentCore Evaluations cung cấp các cổng chất lượng chuẩn hóa trong các pipeline CI/CD (tính đúng đắn, tính hữu ích, tính an toàn, và độ chính xác lựa chọn Tools), để các hồi quy về chất lượng đầu ra có thể phát hiện được mà không cần so sánh chính xác từng bit. Các bộ đánh giá tùy chỉnh bao phủ các yêu cầu đặc thù kinh doanh.

Shadow test, lớp trên cùng, chạy các phiên bản mới song song với sản xuất trên lưu lượng thực bằng phản chiếu lưu lượng (traffic mirroring), so sánh các đầu ra mà không phục vụ các phản hồi của phiên bản mới. Điều này bắt được hành vi đặc thù môi trường mà staging không thể tái tạo. Chi phí là hạ tầng để chạy các suy luận song song, và giá trị là bắt được các vấn đề trước khi người dùng gặp phải. Đối với các nhóm phát triển agent với Kiro, các hook có thể kích hoạt các lần chạy kiểm thử khi lưu tệp và trước khi triển khai.

Hãy tích hợp kiểm thử tự động vào các pipeline CI/CD để mọi lớp chặn triển khai khi thất bại. Duy trì các tập dữ liệu kiểm thử với đánh phiên bản, và rà soát chúng thường xuyên để thêm các trường hợp sử dụng mới và các chế độ lỗi phát hiện trong sản xuất. Kim tự tháp chỉ mạnh lên theo thời gian nếu bộ kiểm thử phát triển cùng hệ thống.

### Các bước triển khai

- **Định nghĩa bốn lớp kiểm thử:** Phạm vi, công cụ, và tiêu chí thành công cho unit, integration, end-to-end, và shadow test.
- **Triển khai unit test và integration test:** Giả lập các phụ thuộc ở lớp unit. Dùng các endpoint staging thực cho integration test.
- **Tạo các kịch bản end-to-end với đánh giá theo ngữ nghĩa:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) cho đánh giá chất lượng thay vì các phép khẳng định khớp chính xác.
- **Thêm kiểm thử bóng với phản chiếu lưu lượng:** Kiểm định các thay đổi hành vi so với các đầu vào thực tế mà không phơi nhiễm người dùng.
- **Tích hợp các bài kiểm thử vào CI/CD:** Chạy toàn bộ bộ kiểm thử trên mỗi commit và chặn triển khai khi thất bại.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS06-BP02 Đánh giá và theo dõi hiệu năng agent liên tục](agentops06-bp02.md)
- [AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh](agentops06-bp03.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](../3-agentops03/agentops03-bp02.md)
- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công phù hợp với hiệu năng cho workload agent](../../4-performance-efficiency/1-agentperf01/agentperf01-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Đánh giá AI agent: Bài học thực tế từ việc xây dựng hệ thống agentic tại Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [LLM-as-a-judge on Amazon Bedrock Model Evaluation](https://aws.amazon.com/blogs/machine-learning/llm-as-a-judge-on-amazon-bedrock-model-evaluation/)
- [Evaluate models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html)
- [Evaluating AI agents for production: A practical guide to Strands Evals](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/)
- [From AI agent prototype to product: Lessons from building AWS DevOps Agent](https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent)
- [Kiro Hooks](https://kiro.dev/docs/hooks/)

**Video liên quan:**

- [AWS 2025 - Strands Agents Observability, Evaluation, & Deployment](https://www.youtube.com/watch?v=VgN-6_tmQHE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples, Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)
- [GitHub: awslabs/amazon-bedrock-agent-samples, RAGAS evaluation](https://github.com/awslabs/amazon-bedrock-agent-samples/tree/main/examples/agents/ragas_evaluation_bedrock_agents)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore, Lab 5: Evaluate Agent Performance](https://catalog.workshops.aws/agentcore-getting-started/en-US/65-evaluation)
- [Diving Deep into Bedrock AgentCore, Evaluations](https://catalog.workshops.aws/agentcore-deep-dive/en-US/80-agentcore-evaluations)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
