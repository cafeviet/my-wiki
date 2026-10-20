---
title: "Tìm hiểu các giao diện sẵn có để sử dụng AgentCore"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html"
---

# Tìm hiểu các giao diện sẵn có để sử dụng AgentCore

# Tìm hiểu các giao diện sẵn có để sử dụng Amazon Bedrock AgentCore

Amazon Bedrock AgentCore hỗ trợ nhiều giao diện khác nhau để phát triển và triển khai code agent (tác tử AI) của bạn. Cách đơn giản nhất là dùng AgentCore Python SDK để tạo code agent và dùng AgentCore CLI để triển khai agent của bạn.

AgentCore CLI và AgentCore Python SDK không hỗ trợ tất cả các thao tác AgentCore mà AWS SDK cung cấp. Nếu chúng không hỗ trợ một thao tác AgentCore cụ thể, hãy dùng AWS SDK.

- [AgentCore CLI](#agentcore-cli-configure-deploy)

- [AgentCore Python SDK](#develop-agents-bedroock-agentcore-sdk)

- [Amazon Bedrock AgentCore MCP server](#develop-agents-bedroock-agentcore-mcp-server)

- [AWS SDK](#develop-agents-bedrock-agentcore-aws-sdk)

- [Console Amazon Bedrock AgentCore](#develop-agents-console)

- [AWS Command Line Interface](#bedrock-agentcore-configure-deploy-cli)

## AgentCore CLI

[AgentCore CLI](https://github.com/aws/agentcore-cli) là một công cụ dòng lệnh Node.js để tạo, cấu hình, triển khai và quản lý các agent trên Amazon Bedrock AgentCore. Nó yêu cầu Node.js 20 trở lên.

Cài đặt AgentCore CLI toàn cục bằng npm:

```bash
npm install -g @aws/agentcore
```

AgentCore CLI cung cấp các lệnh chính sau:

- *agentcore create* : Thiết lập một dự án agent mới với framework và nhà cung cấp model bạn ưa thích

- *agentcore deploy* : Triển khai agent của bạn lên hạ tầng AWS

- *agentcore dev* : Chạy agent cục bộ để phát triển và kiểm thử

- *agentcore invoke* : Gọi một agent đã triển khai để kiểm thử

- *agentcore status* : Kiểm tra trạng thái của một agent đã triển khai

Cấu hình được quản lý qua các tệp JSON trong thư mục `agentcore/` của dự án. Các tệp này bao gồm `agentcore.json` cho các thiết lập dự án và `aws-targets.json` cho các mục tiêu triển khai AWS.

Ở bên dưới, AgentCore CLI dùng các CDK construct của AWS từ package `@aws/agentcore-cdk` để provision và quản lý các tài nguyên AWS.

Để có hướng dẫn từng bước, xem [Bắt đầu với AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html).

## AgentCore Python SDK

[AgentCore Python SDK](https://github.com/aws/bedrock-agentcore-sdk-python) cung cấp các primitive Python cho phát triển agent với hỗ trợ tích hợp sẵn cho:

- *Runtime* : Lớp bọc nhẹ trên các thao tác AgentCore trong AWS SDK, cho phép bạn dễ dàng viết code Python cho một agent.

- *Memory* : Lưu trữ bền vững cho lịch sử hội thoại và ngữ cảnh agent

- *Tools* : Các client tích hợp sẵn cho việc diễn giải code và tự động hóa trình duyệt

- *Identity* : Xác thực và quản lý truy cập bảo mật

- *AgentCore Evaluations* : Các công cụ đánh giá tự động để đo lường hiệu năng agent

AgentCore Python SDK hỗ trợ nhiều framework, chẳng hạn như Strands Agents và LangGraph. Nếu bạn đang dùng các dịch vụ AWS khác, bạn sẽ cần dùng AWS SDK để tích hợp các dịch vụ đó vào agent của bạn, song song với code AgentCore Python SDK.

## Amazon Bedrock AgentCore MCP server

AgentCore Model Context Protocol (MCP) server giúp bạn chuyển đổi, triển khai và kiểm thử các agent tương thích AgentCore trực tiếp từ môi trường phát triển bạn ưa thích. Với hỗ trợ tích hợp sẵn cho tích hợp runtime, kết nối gateway và quản lý vòng đời agent, MCP server đơn giản hóa việc chuyển từ phát triển cục bộ sang triển khai production trên các dịch vụ AgentCore.

MCP server hoạt động với các MCP client phổ biến bao gồm Kiro, Cursor, Claude Code và Amazon Q CLI, cung cấp các lệnh hội thoại để tự động hóa các quy trình phát triển agent phức tạp.

Để biết thêm thông tin, xem [Amazon Bedrock AgentCore MCP Server: Vibe coding với trợ lý lập trình của bạn](/dich-thuat/aws-bedrock-agentcore/14-mcp-server/).

## AWS SDK

Bạn có thể dùng AWS SDK để đạt được cùng kết quả như AgentCore Python SDK, cũng như các tác vụ khác mà AgentCore Python SDK không hỗ trợ. Bạn sẽ cần dùng AWS SDK để tương tác với các dịch vụ AWS khác như AWS Lambda và Amazon S3. Bạn cũng sẽ cần AWS SDK nếu bạn không dùng Python làm ngôn ngữ lập trình.

Để cấu hình và triển khai một agent, bạn dùng [AgentCore control plane API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/Welcome.html). Ví dụ, bạn có thể tạo một AgentCore Runtime hoặc tạo một AgentCore Memory.

Tại runtime, bạn dùng [AgentCore data plane API](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/Welcome.html) cho các tác vụ như thêm một memory event vào một AgentCore Memory. Code client gọi agent của bạn dùng thao tác data plane `InvokeAgentRuntime` để gọi một agent mà bạn đã host trong một AgentCore Runtime.

## Console Amazon Bedrock AgentCore

Bạn có thể dùng console AgentCore để tạo và quản lý các dịch vụ AgentCore mà code agent của bạn sử dụng. Bạn có thể lấy các đoạn code minh họa cách gọi một agent được host trong một AgentCore Runtime. Bạn cũng có thể kiểm thử agent của bạn trong agent sandbox. Mở console tại [https://console.aws.amazon.com/bedrock-agentcore/home#](https://console.aws.amazon.com/bedrock-agentcore/home#).

## AWS Command Line Interface

Bạn có thể dùng AWS CLI với các dịch vụ AgentCore mà bạn sử dụng. Dùng [control plane api](https://docs.aws.amazon.com/cli/latest/reference/bedrock-agentcore-control/) để tạo và quản lý dịch vụ. Ví dụ bạn có thể tạo một AgentCore Memory hoặc cập nhật endpoint cho một AgentCore Runtime. Bạn cũng có thể thực hiện các hành động runtime với [data plane API](https://docs.aws.amazon.com/cli/latest/reference/bedrock-agentcore/), điều này có thể hữu ích cho việc kiểm thử một agent.
