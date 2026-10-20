# AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)

Các triển khai agent thủ công và kiểm thử phi chính thức có thể khiến một dự án mắc kẹt ở giai đoạn thí điểm. Một pipeline nhận biết agent (agent-aware), với các cổng đánh giá hành vi, triển khai theo giai đoạn, và quay lui tự động, có thể giúp tổ chức của bạn hiện thực hóa mục tiêu triển khai các cải tiến hành vi hàng ngày.

**Kết quả mong muốn:**

- Các triển khai agent chạy hoàn toàn qua CI/CD với các cổng kiểm định đặc thù agent cho chất lượng Prompt, tính đúng đắn của tích hợp Tools, hồi quy hành vi, và bảo mật.
- Các chiến lược triển khai (blue/green, canary) giới hạn phạm vi tác động khi một hồi quy lọt qua.
- Quay lui tự động khôi phục phiên bản trước trong vòng vài phút nếu các ngưỡng chất lượng bị vượt qua.
- Hạ tầng được định nghĩa dưới dạng mã để các triển khai có thể tái lập và các môi trường giữ nhất quán.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các thay đổi agent qua các thao tác console thủ công hoặc các script một lần mà không có các cổng kiểm định tự động, khiến các triển khai không nhất quán và dễ sai sót.
- Chỉ chạy các unit test truyền thống mà không có đánh giá hành vi đặc thù agent (chất lượng Prompt, độ chính xác lựa chọn Tools, tỷ lệ ảo giác), bỏ lỡ các hồi quy mà unit test không thể phát hiện.
- Triển khai trực tiếp vào sản xuất mà không có triển khai theo giai đoạn (canary, blue/green), khuếch đại tối đa phạm vi tác động của bất kỳ hồi quy nào.
- Xem quay lui như một năng lực lý thuyết chưa bao giờ được diễn tập, nên lần đầu ai đó dùng nó là trong lúc sự cố.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các pipeline tự động giúp mỗi lần triển khai tuân theo cùng một đường đã được kiểm định bất kể ai khởi động nó, giảm sự thiếu nhất quán trong triển khai.
- Các cổng kiểm định hành vi cung cấp bằng chứng thực nghiệm rằng mỗi lần triển khai đáp ứng các tiêu chuẩn chất lượng trước khi vào sản xuất.
- Triển khai theo giai đoạn và quay lui tự động nén thời gian ứng phó sự cố từ hàng giờ xuống vài phút khi các hồi quy xuất hiện.
- Hạ tầng như mã khiến các triển khai có thể tái lập qua các môi trường, loại bỏ một nguồn lỗi phổ biến.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

CI/CD agent chia sẻ hầu hết cấu trúc với CI/CD phần mềm, với một bổ sung thực chất: đánh giá hành vi. Các giai đoạn phù hợp với hầu hết workload agent là:

- Source (mã, Prompt, cấu hình, và các tập dữ liệu đánh giá)
- Build (đóng gói tài liệu và chạy unit test)
- Evaluate (chạy đánh giá hành vi qua [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html))
- Security scan (các lỗ hổng tiêm Prompt và phạm vi IAM)
- Deploy to production (triển khai vào sản xuất)

Độ chính xác hoàn thành tác vụ, tỷ lệ ảo giác, và độ chính xác lựa chọn Tools cần các ngưỡng rõ ràng để chặn thăng hạng khi bị vượt qua. Các ngưỡng đặt quá lỏng tạo ra vượt qua giả (false pass), nhưng các ngưỡng đặt quá chặt chặn việc lặp lại chính đáng. Để hiệu chỉnh, hãy bắt đầu với các ngưỡng điều chỉnh theo baseline hiện tại, rồi thắt chặt chúng khi thành tích chất lượng của agent tăng lên.

Triển khai sản xuất sử dụng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cho scaling được quản lý, đánh phiên bản, và khả năng quan sát. Lệnh agentcore deploy đẩy các phiên bản mới, và định tuyến có trọng số dựa trên endpoint xử lý các mẫu blue/green và canary. Các cảnh báo [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) theo dõi các chỉ số chất lượng sau triển khai và kích hoạt quay lui tự động khi các ngưỡng bị vượt qua. Chính các cảnh báo chạy trong triển khai theo giai đoạn cũng đóng vai trò như tác nhân kích hoạt quay lui. Hạ tầng như mã qua [AWS CDK](https://aws.amazon.com/cdk/) hoặc [AWS CloudFormation](https://aws.amazon.com/cloudformation/) giúp mọi tài nguyên có thể tái lập.

Một quy trình quay lui chưa bao giờ được diễn tập là một quy trình có thể không hoạt động khi nhóm cần nó. Các buổi diễn tập quay lui có chủ đích trong quá trình kiểm định pipeline xác nhận rằng việc hoàn nguyên hoạt động trước khi nhóm phải phụ thuộc vào nó.

### Các bước triển khai

- **Xây dựng các giai đoạn pipeline:** Cấu hình các giai đoạn source, build, đánh giá hành vi, security scan, và triển khai sản xuất với các công cụ phù hợp cho từng giai đoạn.
- **Đặt đánh giá hành vi làm một cổng:** Tích hợp [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) với các ngưỡng độ chính xác hoàn thành tác vụ và tỷ lệ ảo giác để chặn thăng hạng khi bị vượt qua.
- **Triển khai lên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html):** Dùng đánh phiên bản tích hợp và định tuyến có trọng số dựa trên endpoint cho các triển khai blue/green hoặc canary.
- **Tự động hóa quay lui khi vượt ngưỡng chất lượng:** Nối các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) với các luồng công việc hoàn nguyên triển khai để các vi phạm ngưỡng chất lượng kích hoạt hoàn nguyên ngay lập tức.
- **Đánh phiên bản mọi tài liệu triển khai:** Gắn thẻ mỗi tập tài liệu bằng ID lần chạy pipeline để truy vết, và lưu trong một kho có phiên bản bền vững.
- **Kiểm định toàn bộ pipeline:** Kích hoạt có chủ đích một quay lui trong quá trình kiểm định pipeline để xác nhận các quy trình hoàn nguyên hoạt động trước khi chúng thực sự cần đến.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](agentops03-bp01.md)
- [AGENTOPS02-BP03 Triển khai năng lực đánh phiên bản và quay lui hành vi agent](../2-agentops02/agentops02-bp03.md)
- [AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh](../6-agentops06/agentops06-bp03.md)
- [AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tài liệu hiệu quả](../../5-cost-optimization/6-agentcost06/agentcost06-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)
- [Triển khai AI agent trên Amazon Bedrock AgentCore bằng GitHub Actions](https://aws.amazon.com/blogs/machine-learning/deploy-ai-agents-on-amazon-bedrock-agentcore-using-github-actions/)
- [Strands Agents](https://strandsagents.com/)
- [CI/CD and automation for serverless AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/cicd-and-automation.html)
- [Kiro Hooks](https://kiro.dev/docs/hooks/)

**Video liên quan:**

- [AWS 2025 - Deploy Production-Ready Agents in 22 Minutes with AgentCore Runtime](https://www.youtube.com/watch?v=Q-tYIAuv9WI)
- [AWS 2025 - Deploy ANY AI Agent to Production in Minutes - AgentCore Tutorial](https://www.youtube.com/watch?v=N7FGbBq1mI4)
- [AWS 2025 - Strands Agents Observability, Evaluation, & Deployment](https://www.youtube.com/watch?v=VgN-6_tmQHE)
- [AWS re:Invent 2024 - Building AI Agents with Serverless, Strands, and MCP (NTA405)](https://www.youtube.com/watch?v=LwubRSoJcIM)
- [AWS re:Invent 2024 - Develop AI Agents faster with SageMaker AI Studio & AgentCore (AIM388)](https://www.youtube.com/watch?v=UL_7a2GEu10)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore, Lab 4: Deploy to Production](https://catalog.workshops.aws/agentcore-getting-started/en-US/60-add-runtime)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/cdk/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
