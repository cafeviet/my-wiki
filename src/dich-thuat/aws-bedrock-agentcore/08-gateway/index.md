---
title: "AgentCore Gateway"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---
# AgentCore Gateway

# Amazon Bedrock AgentCore Gateway: Một cổng AI an toàn cho các Agent, tool, và model

Amazon Bedrock AgentCore Gateway (cổng) là một AI gateway được quản lý hoàn toàn, cung cấp một điểm vào duy nhất và an toàn cho lưu lượng dạng agentic—kết nối các Agent (tác tử AI) tới các tool (công cụ), tới các Agent khác, và tới các large language model (LLM). Thay vì chỉ đóng vai trò một MCP tool gateway, Gateway định tuyến và bảo mật mọi lưu lượng agentic qua một endpoint duy nhất: nó chuyển đổi các API, hàm Lambda, và các dịch vụ hiện có thành các tool tương thích Model Context Protocol (MCP); đặt các Agent khác và các dịch vụ HTTP đằng sau các passthrough target (bao gồm cả lưu lượng Agent-to-Agent (A2A)); và định tuyến các yêu cầu suy luận (inference) trên nhiều model provider qua một endpoint định tuyến theo model, thống nhất. Gateway hỗ trợ OpenAPI, Smithy, và Lambda làm các loại tool input, và là giải pháp duy nhất cung cấp cả ingress authentication toàn diện lẫn egress authentication trong một dịch vụ được quản lý hoàn toàn. Gateway cũng cung cấp tích hợp 1-click với một số tool phổ biến như Salesforce, Slack, Jira, Asana, và Zendesk. Gateway loại bỏ hàng tuần phát triển mã tùy chỉnh, cấp phát hạ tầng, và triển khai bảo mật, để lập trình viên tập trung xây dựng các ứng dụng Agent sáng tạo.

###### Chủ đề

- [Key benefits](#gateway-benefits-using)

- [Key capabilities](#gateway-core-concepts-connectivity-layer)

- [Get started with AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/gateway-quick-start)

- [Core concepts for Amazon Bedrock AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/gateway-core-concepts)

- [Amazon Bedrock AgentCore Gateway features](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-features.html)

- [Supported targets for Amazon Bedrock AgentCore gateways](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-supported-targets.html)

- [Prerequisites for using the Amazon Bedrock AgentCore gateway service](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-prerequisites.html)

- [Set up an Amazon Bedrock AgentCore gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building.html)

- [Use an AgentCore gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using.html)

- [Add rules to a gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-rules.html)

- [Fine-grained access control for Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-fine-grained-access-control.html)

- [Debug and assess your gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building-debug.html)

- [Advanced features and topics for Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-advanced.html)

## Lợi ích chính

Biến đổi các tài nguyên doanh nghiệp hiện có thành các tool sẵn sàng cho Agent chỉ với vài dòng code. Thay vì bỏ ra hàng tháng viết mã tích hợp tùy chỉnh và quản lý hạ tầng, lập trình viên có thể tập trung xây dựng các năng lực Agent khác biệt trong khi Gateway đảm nhận công việc nặng nhọc không tạo khác biệt là quản lý tool và bảo mật ở quy mô doanh nghiệp. Gateway cũng cung cấp tích hợp 1-click với một số tool phổ biến như Salesforce, Slack, Jira, Asana, và Zendesk.

Cho phép các Agent của bạn khám phá và tiếp cận các tool, các Agent khác, và các model qua một endpoint duy nhất và an toàn. Bằng cách kết hợp nhiều nguồn—từ các API và hàm Lambda đến các Agent khác và các model provider—vào một giao diện thống nhất, lập trình viên có thể xây dựng và mở rộng các quy trình Agent nhanh hơn mà không cần quản lý nhiều kết nối hay triển khai lại các tích hợp.

Khi tập hợp tool của bạn phát triển, hãy giúp các Agent tìm và dùng đúng tool thông qua tìm kiếm theo ngữ cảnh. Năng lực semantic search tích hợp giúp các Agent sử dụng hiệu quả các tool khả dụng dựa trên bối cảnh nhiệm vụ, cải thiện hiệu năng Agent và giảm độ phức tạp phát triển ở quy mô lớn.

Quản lý cả inbound authentication (xác minh danh tính Agent) và outbound authentication (kết nối tới các tool) trong một dịch vụ duy nhất. Xử lý các luồng OAuth, làm mới token, và lưu trữ thông tin xác thực an toàn cho các dịch vụ bên thứ ba.

Làm việc với các framework mã nguồn mở phổ biến bao gồm CrewAI, LangGraph, LlamaIndex, và Strands Agents. Tích hợp với bất kỳ model nào trong khi vẫn duy trì bảo mật và độ tin cậy cấp doanh nghiệp.

Loại bỏ việc quản lý hạ tầng với một dịch vụ được quản lý hoàn toàn, tự động mở rộng theo nhu cầu. Các năng lực observability (khả năng quan sát) và kiểm toán tích hợp giúp đơn giản hóa việc giám sát và xử lý sự cố.

## Năng lực chính

Gateway cung cấp các năng lực chính sau:

- **Security Guard** - Quản lý ủy quyền OAuth để đảm bảo chỉ những người dùng và Agent hợp lệ mới có thể truy cập các tool và tài nguyên.

- **Translation** - Chuyển đổi các yêu cầu của Agent dùng các giao thức như Model Context Protocol (MCP) thành các yêu cầu API và các lời gọi Lambda, loại bỏ nhu cầu quản lý tích hợp giao thức hay hỗ trợ phiên bản.

- **Composition** - Kết hợp nhiều API, hàm, tool, Agent, và model provider đằng sau một endpoint duy nhất để Agent truy cập gọn gàng, bao gồm cả định tuyến theo model đối với lưu lượng suy luận trên các provider.

- **Secure Credential Exchange** - Xử lý việc chèn thông tin xác thực cho từng tool, cho phép các Agent dùng các tool có yêu cầu xác thực khác nhau một cách liền mạch.

- **Semantic Tool Selection** - Cho phép các Agent tìm kiếm trên các tool khả dụng để tìm những tool phù hợp nhất cho các bối cảnh cụ thể, cho phép Agent dùng hàng nghìn tool trong khi vẫn giảm thiểu kích thước prompt và giảm độ trễ.

- **Infrastructure Manager** - Cung cấp một giải pháp serverless với observability và kiểm toán tích hợp, loại bỏ chi phí quản lý hạ tầng.
