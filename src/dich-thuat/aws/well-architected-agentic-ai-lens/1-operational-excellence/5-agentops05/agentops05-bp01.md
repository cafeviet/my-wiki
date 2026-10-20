# AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent

Khi một agent tạo ra đầu ra bất ngờ, cuộc điều tra chỉ tốt bằng telemetry của nó. Truy vết phân tán nắm bắt toàn bộ đường thực thi (suy luận, các lời gọi Tools, các thao tác bộ nhớ, và các lời gọi Model) cho phép tái dựng chính xác mọi quyết định và hành động.

**Kết quả mong muốn:**

- Mỗi lần chạy agent tạo ra một vết phân tán hoàn chỉnh bao phủ luồng từ yêu cầu đến phản hồi qua mọi dịch vụ và agent.
- Các nhóm có thể tái dựng chuỗi thao tác chính xác cho bất kỳ lần chạy nào, cho phép gỡ lỗi nhanh và tối ưu có mục tiêu.
- Các dashboard telemetry thời gian thực mang lại cho các nhóm vận hành tầm nhìn liên tục vào sức khỏe agent.
- Dữ liệu vết được lưu giữ theo một chính sách được xác định cho phân tích sau vận hành và tuân thủ.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ trang bị đo lường cho các chỉ số hạ tầng (thời lượng Lambda, độ trễ API Gateway) mà không nắm bắt các span đặc thù agent cho các bước suy luận, các lời gọi Tools, và các thao tác bộ nhớ.
- Triển khai truy vết mà không lan truyền ngữ cảnh vết qua các ranh giới agent, tạo ra các mảnh vết rời rạc không thể tương quan thành các luồng công việc đầu-cuối.
- Nắm bắt telemetry mà không có các lược đồ chuẩn hóa, khiến không thể truy vấn nhất quán qua các agent hay so sánh hành vi qua các phiên bản.
- Lưu giữ các vết mãi mãi vì không ai định nghĩa một chính sách, hoặc lưu giữ chúng quá ngắn để hỗ trợ phân tích xu hướng theo quý.

**Lợi ích khi áp dụng thực hành tốt này:**

- Truy vết phân tán khiến các hoạt động agent như các quyết định và hành động trở nên truy vấn được.
- Telemetry chi tiết cung cấp nền tảng thực nghiệm cho tối ưu, xác định các nút thắt cổ chai và kiểm định các cải tiến bằng dữ liệu.
- Lan truyền ngữ cảnh vết qua các ranh giới agent khiến việc gỡ lỗi luồng công việc đa agent trở nên khả thi.
- Các lược đồ chuẩn hóa cho phép so sánh liên agent và phân tích hồi quy phiên bản-qua-phiên bản.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) là dịch vụ telemetry mặc định cho các agent trên AgentCore Runtime. Trang bị đo lường tương thích OpenTelemetry của nó tự động nắm bắt các lời gọi suy luận LLM, các lời gọi Tools, và các thao tác bộ nhớ mà không yêu cầu mỗi agent tự thêm các span của mình. Đối với các agent xây trên Strands Agents hoặc các framework tùy chỉnh, bản thân vòng lặp agent (agent loop) cần được trang bị đo lường. Các span OpenTelemetry bao quanh mỗi pha thao tác khiến vết trở nên hoàn chỉnh.

Lan truyền ngữ cảnh vết tách các vết hữu ích khỏi các vết bị phân mảnh. Lan truyền W3C Trace Context qua mọi ranh giới agent duy trì tính liên tục trong các luồng công việc phân tán, để một yêu cầu đi qua năm agent tạo ra một vết với năm span, không phải năm vết rời rạc. Không có lan truyền, gỡ lỗi đa agent trở thành đối chiếu thủ công theo mốc thời gian, vốn mở rộng kém và tạo ra các câu trả lời sai khi các yêu cầu đồng thời chồng lấn.

Các lược đồ span chuẩn hóa tạo ra dữ liệu truy vấn được từ telemetry của bạn. Mỗi loại span cần các trường được xác định, như ID Model và số Token cho suy luận, tên Tools và độ trễ cho các lời gọi, và số vòng lặp cho suy luận. Hãy lưu telemetry trong [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) Logs với JSON có cấu trúc để các dashboard và truy vấn hoạt động trên các trường được đặt tên. Cấu hình lấy mẫu (sampling) để nắm bắt 100% các vết lỗi và một tỷ lệ có thể cấu hình các vết thành công. Điều này cân bằng tầm nhìn với chi phí, và các lỗi không bị bỏ rơi.

### Các bước triển khai

- **Trang bị đo lường cho các agent bằng các span OpenTelemetry:** Triển khai trên [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) hoặc thêm trang bị đo lường thủ công bao phủ mọi pha thao tác (suy luận, các lời gọi Tools, các thao tác bộ nhớ).
- **Lan truyền W3C Trace Context qua các ranh giới agent:** Mang ngữ cảnh vết tiến lên trên mọi lời gọi agent-tới-agent, agent-tới-Tools, và agent-tới-dịch vụ.
- **Định nghĩa các lược đồ telemetry chuẩn hóa:** Quy định các trường cho mỗi loại span, và ghi log ở JSON có cấu trúc để truy vấn [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) Logs hiệu quả.
- **Xây dựng các dashboard đầu-cuối:** Trực quan hóa hiệu năng agent với khả năng đào sâu (drill-down) tới từng thành phần vết.
- **Đặt các chính sách lưu giữ:** Cân bằng tầm nhìn với chi phí lưu trữ, với các tầng khác nhau cho telemetry vận hành, tuân thủ, và gỡ lỗi.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](agentops05-bp02.md)
- [AGENTOPS05-BP03 Triển khai ghi log có cấu trúc và các vết kiểm toán toàn diện](agentops05-bp03.md)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](../4-agentops04/agentops04-bp03.md)
- [AGENTPERF01-BP02 Triển khai telemetry hiệu năng toàn diện](../../4-performance-efficiency/1-agentperf01/agentperf01-bp02.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và hỗ trợ phục hồi](../../3-reliability/7-agentrel07/agentrel07-bp03.md)

**Tài liệu liên quan:**

- [Getting started with Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html)
- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Observing agentic AI workloads using Amazon CloudWatch](https://aws.amazon.com/blogs/mt/observing-agentic-ai-workloads-using-amazon-cloudwatch/)
- [Observability and monitoring for serverless agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/observability-and-monitoring.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)
- [AWS re:Invent 2024 - Observability for Reliable Agentic AI with Strands & OpenTelemetry (NTA406)](https://www.youtube.com/watch?v=qJxF4XfMLhk)
- [AWS re:Invent 2024 - Build observable AI agents with Strands, AgentCore, and Datadog (AIM233)](https://www.youtube.com/watch?v=mOAd8grR1BU)
- [AWS 2025 - Strands Agents Observability, Evaluation, & Deployment](https://www.youtube.com/watch?v=VgN-6_tmQHE)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore, Lab 4: Deploy to Production](https://catalog.workshops.aws/agentcore-getting-started/en-US/60-add-runtime)
- [Diving Deep into Bedrock AgentCore, Observability](https://catalog.workshops.aws/agentcore-deep-dive/en-US/70-agentcore-observability)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS X-Ray](https://aws.amazon.com/xray/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
