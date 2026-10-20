---
title: "AgentCore Runtime: Host agent hoặc tool"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html"
---

# AgentCore Runtime: Host agent hoặc tool

# Host agent hoặc tool với Amazon Bedrock AgentCore Runtime

Amazon Bedrock AgentCore Runtime (môi trường chạy) cung cấp một môi trường lưu trữ (hosting) an toàn, serverless và được thiết kế chuyên biệt để triển khai và chạy các AI agent (tác tử AI) hoặc tool (công cụ). Nó mang lại những lợi ích sau:

AgentCore Runtime cho phép bạn chuyển đổi bất kỳ mã agent chạy cục bộ nào thành các triển khai cloud-native chỉ với vài dòng mã, bất kể framework bên dưới là gì. Nó hoạt động liền mạch với các framework phổ biến như LangGraph, Strands và CrewAI. Bạn cũng có thể tận dụng nó với các agent tùy chỉnh không dùng framework cụ thể nào.

AgentCore Runtime hoạt động với bất kỳ Large Language Model nào, chẳng hạn các mô hình do Amazon Bedrock, Anthropic Claude, Google Gemini và OpenAI cung cấp.

AgentCore Runtime cho phép agent giao tiếp với các agent và tool khác thông qua Model Context Protocol (MCP) hoặc Agent to Agent (A2A).

Trong AgentCore Runtime, mỗi phiên (session) người dùng chạy trong một microVM riêng biệt với tài nguyên CPU, bộ nhớ và hệ thống tệp được cô lập. Điều này giúp tạo ra sự tách biệt hoàn toàn giữa các phiên người dùng, bảo vệ các quá trình suy luận (reasoning) có trạng thái của agent và giúp ngăn nhiễm chéo dữ liệu giữa các phiên. Sau khi phiên kết thúc, toàn bộ microVM bị hủy và bộ nhớ được làm sạch, mang lại tính bảo mật xác định (deterministic) ngay cả khi làm việc với các quá trình AI không xác định (non-deterministic).

AgentCore Runtime cung cấp hai loại compute. Chọn **microVMs** để có các phiên serverless được quản lý hoàn toàn, khởi động tức thì và co giãn theo nhu cầu, nơi bạn chỉ trả tiền cho những gì mình dùng. Chọn **Instances** để chạy agent trên hạ tầng Amazon EC2 do AWS quản lý trong tài khoản của riêng bạn. Instances hỗ trợ các phiên bền vững kéo dài nhiều ngày, khối lượng công việc tăng tốc bằng GPU, và nhiều agent hợp tác trên một instance dùng chung. Để biết thêm thông tin, xem [Run agents on Instances with capacity providers](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-instances.html).

AgentCore Runtime hỗ trợ cả tương tác thời gian thực và khối lượng công việc chạy dài, cho phép các quá trình suy luận phức tạp của agent và khối lượng công việc bất đồng bộ có thể liên quan đến hợp tác đa agent hoặc các phiên giải quyết vấn đề kéo dài. Các phiên chạy tối đa 8 giờ trên microVMs, hoặc tối đa 14 ngày trên Instances. Để biết thêm thông tin, xem [Configure Amazon Bedrock AgentCore lifecycle settings](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-lifecycle-settings.html).

Runtime hỗ trợ duy trì trạng thái hệ thống tệp qua các chu kỳ dừng/tiếp tục phiên. Các tệp, gói đã cài đặt và build artifact của agent có thể tồn tại qua các lần dừng phiên mà không cần lưu trữ bên ngoài.

Runtime triển khai mô hình giá dựa trên mức tiêu thụ, chỉ tính phí cho tài nguyên thực sự được sử dụng. Không giống các mô hình dựa trên phân bổ (allocation-based) yêu cầu chọn trước tài nguyên, Runtime cấp phát động những gì cần thiết mà không yêu cầu tinh chỉnh kích thước (right-sizing). Dịch vụ này căn chỉnh chi phí CPU với hoạt động xử lý thực tế — thường loại bỏ chi phí trong các giai đoạn chờ I/O khi agent chủ yếu đang chờ phản hồi từ LLM — trong khi vẫn liên tục duy trì trạng thái phiên của bạn.

AgentCore Runtime, được vận hành bởi AgentCore Identity (danh tính), gán các danh tính riêng biệt cho các AI agent và tích hợp liền mạch với nhà cung cấp danh tính doanh nghiệp của bạn như Okta, Microsoft Entra ID hoặc Amazon Cognito, cho phép người dùng cuối của bạn xác thực vào chỉ những agent mà họ có quyền truy cập. Ngoài ra, Runtime cho phép các luồng xác thực đi ra (outbound) để truy cập an toàn các dịch vụ bên thứ ba như Slack, Zoom và GitHub — dù hoạt động thay mặt người dùng hay tự động (dùng OAuth hoặc API key).

AgentCore Runtime cung cấp khả năng truy vết (tracing) tích hợp chuyên biệt để nắm bắt các bước suy luận của agent, các lần gọi tool và các tương tác với mô hình, mang lại tầm nhìn rõ ràng vào quá trình ra quyết định của agent, một năng lực quan trọng để gỡ lỗi và kiểm toán hành vi của AI agent.

AgentCore Runtime có thể xử lý payload 100MB, cho phép xử lý liền mạch nhiều phương thức (văn bản, hình ảnh, âm thanh, video) với nội dung media phong phú hoặc tập dữ liệu lớn.

AgentCore Runtime hỗ trợ cả các lệnh gọi HTTP API và các kết nối WebSocket bền vững cho luồng dữ liệu song hướng thời gian thực, cho phép các ứng dụng tương tác với phản hồi tức thì và bối cảnh hội thoại được duy trì.

AgentCore Runtime được cung cấp qua một SDK toàn diện, duy nhất, cho phép truy cập tinh gọn vào toàn bộ năng lực của AgentCore bao gồm Memory (bộ nhớ), Tools và Gateway (cổng). Cách tiếp cận tích hợp này loại bỏ công sức tích hợp thường cần khi xây dựng hạ tầng agent tương đương từ các thành phần rời rạc.

###### Note

Đã có sẵn phiên bản nền tảng mới hơn, V2. Nó khởi động agent của bạn từ một snapshot để giữ cho cold start nhanh và ổn định bất kể mức đồng thời hay kích thước image, đồng thời giảm chi phí cho các agent luôn bật hoặc có tải đột biến. Để biết thêm thông tin, xem [Platform versions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html#runtime-platform-versions).

###### Topics

- [How it works](/dich-thuat/aws-bedrock-agentcore/06-runtime/runtime-compute-how-it-works)

- [Understand the AgentCore Runtime service contract](/dich-thuat/aws-bedrock-agentcore/06-runtime/runtime-service-contract)

- [IAM Permissions for AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html)

- [Get started with AgentCore Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/runtime-getting-started)

- [Optimize your agent for Amazon Bedrock AgentCore Runtime V2](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-v2-optimize.html)

- [Use any agent framework](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html)

- [Use any foundation model](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-model.html)

- [Deploy MCP servers in AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp.html)

- [Stateful MCP server features](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-stateful-features.html)

- [Deploy A2A servers in AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html)

- [Deploy AG-UI servers in AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui.html)

- [Use isolated sessions for agents](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html)

- [File system configurations for AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-filesystem-configurations.html)

- [Handle asynchronous and long running agents with Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html)

- [Stream agent responses](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/response-streaming.html)

- [Bidirectional streaming](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-bidirectional-streaming.html)

- [Pass custom headers to Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-header-allowlist.html)

- [Authenticate and authorize with Inbound Auth and Outbound Auth](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html)

- [AgentCore Runtime versioning and endpoints](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agent-runtime-versioning.html)

- [Invoke an AgentCore Runtime agent](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-invoke-agent.html)

- [Shell execution](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-shell-execution.html)

- [Observe agents in Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-observability.html)

- [Security best practices for AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html)

- [Troubleshoot AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html)
