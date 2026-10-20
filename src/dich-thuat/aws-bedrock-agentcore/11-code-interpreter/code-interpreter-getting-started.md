---
title: "Bắt đầu với AgentCore Code Interpreter"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-getting-started.html"
---

# Bắt đầu với AgentCore Code Interpreter

AgentCore Code Interpreter cho phép các agent (tác tử AI) của bạn thực thi mã Python trong một môi trường an toàn, được quản lý. Agent có thể thực hiện tính toán, phân tích dữ liệu, tạo trực quan hóa và kiểm chứng câu trả lời thông qua việc thực thi mã.

Trang này bao gồm các điều kiện tiên quyết và cung cấp hai cách tiếp cận để bắt đầu:

- **Dùng AWS Strands** - Một framework agent cấp cao giúp đơn giản hóa việc xây dựng AI agent với tích hợp tool (công cụ) sẵn có, quản lý hội thoại và xử lý phiên (session) tự động.

- **Dùng trực tiếp** - Các cách tiếp cận SDK và Boto3 cho phép kiểm soát nhiều hơn việc quản lý phiên và thực thi mã cho các triển khai tùy chỉnh.

###### Topics

- [Prerequisites](#code-interpreter-prerequisites)

- [Configuring your credentials](#code-interpreter-credentials-config)

- [Using AgentCore Code Interpreter via AWS Strands](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-using-strands.html)

- [Using AgentCore Code Interpreter directly](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-using-directly.html)

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy đảm bảo bạn có:

- Tài khoản AWS với credential đã được cấu hình. Xem [Configuring your credentials](#code-interpreter-credentials-config).

- Python 3.10+ đã cài đặt

- Boto3 đã cài đặt. Xem [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html).

- IAM execution role với các quyền cần thiết. Xem [Configuring your credentials](#code-interpreter-credentials-config).

- Quyền truy cập mô hình: Anthropic Claude Sonnet 4.0 đã được [enabled](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html) trong Amazon Bedrock console. Để biết thông tin về việc dùng mô hình khác với Strands Agents, xem phần *Model Providers* trong [Strands Agents SDK documentation](https://strandsagents.com/latest/documentation/docs/).

- AWS Region nơi Amazon Bedrock AgentCore khả dụng. Xem [Supported AWS Regions](/dich-thuat/aws-bedrock-agentcore/02-supported-aws-regions/).

## Cấu hình credential của bạn

Thực hiện các bước sau để cấu hình AWS credential và gắn các quyền cần thiết.

- **Xác minh AWS credential của bạn**

    Xác nhận AWS credential của bạn đã được cấu hình:
    `aws sts get-caller-identity`
    Note: Ghi lại user hoặc credential được trả về ở đây, vì bạn sẽ dùng nó khi gắn các quyền cần thiết.
    Nếu lệnh này thất bại, hãy cấu hình credential của bạn. Để biết thêm thông tin, xem [Configuration and credential file settings in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

- **Gắn các quyền cần thiết**

    IAM user hoặc role của bạn cần quyền để dùng AgentCore Code Interpreter. Gắn chính sách này vào danh tính IAM của bạn:
    Note: Thay thế `<Region>` bằng region bạn chọn (ví dụ, `us-west-2`) và `<account_id>` bằng AWS account ID của bạn trong chính sách dưới đây:

    ```json
    {
        "Version":"2012-10-17",
        "Statement": [
            {
                "Sid": "BedrockAgentCoreCodeInterpreterFullAccess",
                "Effect": "Allow",
                "Action": [
                    "bedrock-agentcore:CreateCodeInterpreter",
                    "bedrock-agentcore:StartCodeInterpreterSession",
                    "bedrock-agentcore:InvokeCodeInterpreter",
                    "bedrock-agentcore:StopCodeInterpreterSession",
                    "bedrock-agentcore:DeleteCodeInterpreter",
                    "bedrock-agentcore:ListCodeInterpreters",
                    "bedrock-agentcore:GetCodeInterpreter",
                    "bedrock-agentcore:GetCodeInterpreterSession",
                    "bedrock-agentcore:ListCodeInterpreterSessions"
                ],
                "Resource": "arn:aws:bedrock-agentcore:<Region>:<account_id>:code-interpreter/*"
            }
        ]
    }
    ```

**Để gắn chính sách này**

Làm theo các bước sau:

- Truy cập IAM console.

- Tìm user hoặc role của bạn từ phản hồi được trả về cho lệnh `get-caller-identity` API.

- Chọn **Add permissions** rồi chọn **Create inline policy**

- Chuyển sang chế độ xem JSON và dán chính sách ở trên

- Đặt tên là `AgentCoreCodeInterpreterAccess` và lưu lại

###### Note

Nếu bạn đang triển khai agent lên Amazon Bedrock AgentCore Runtime (môi trường chạy), bạn cũng cần tạo một IAM execution role với service trust policy. Để biết thêm thông tin, xem [Get started with AgentCore Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/runtime-getting-started).

Các phần sau hướng dẫn bạn cách dùng Amazon Bedrock AgentCore Code Interpreter có và không có agent framework. Việc dùng Code Interpreter trực tiếp mà không có agent framework đặc biệt hữu ích khi bạn muốn thực thi các đoạn mã cụ thể theo cách lập trình.
