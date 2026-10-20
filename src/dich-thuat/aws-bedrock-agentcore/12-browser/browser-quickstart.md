---
title: "Bắt đầu với AgentCore Browser"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart.html"
---

# Bắt đầu với AgentCore Browser

AgentCore Browser cho phép các agent (tác tử AI) của bạn tương tác với các trang web thông qua một trình duyệt Chrome được quản lý. Trong hướng dẫn này, bạn sẽ tạo một AI agent điều hướng một website và trích xuất thông tin — trong chưa đầy 5 phút.

###### Topics

- [Prerequisites](#browser-prerequisites)

- [Step 1: Install dependencies](#browser-strands-install)

- [Step 2: Create your agent](#browser-strands-create)

- [Step 3: Run the agent](#browser-strands-run)

- [Step 4: View the browser session live](#browser-strands-live-view)

- [Find your resources](#browser-find-resources)

- [Next steps](#browser-next-steps)

- [Using AgentCore Browser with Nova Act](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-nova-act.html)

- [Using AgentCore Browser with Playwright](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html)

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy đảm bảo bạn có:

- Python 3.10 trở lên ( [python.org/downloads](https://www.python.org/downloads/) )

- Boto3 đã cài đặt ( [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) )

- AWS credential đã cấu hình — xác minh bằng:
    `aws sts get-caller-identity`
    Nếu lệnh này thất bại, xem [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) trong tài liệu AWS CLI.

- Quyền truy cập mô hình Anthropic Claude Sonnet 4.0 đã được [enabled](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html) trong Amazon Bedrock console

- AWS Region nơi Amazon Bedrock AgentCore khả dụng (xem [Supported AWS Regions](/dich-thuat/aws-bedrock-agentcore/02-supported-aws-regions/) )

**Quyền IAM**

Gắn chính sách này vào danh tính IAM của bạn. Trong IAM Console, tìm user hoặc role của bạn, chọn **Add permissions** > **Create inline policy**, chuyển sang chế độ xem JSON và dán:

```json
{
"Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAgentCoreBrowserFullAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock-agentcore:CreateBrowser",
                "bedrock-agentcore:ListBrowsers",
                "bedrock-agentcore:GetBrowser",
                "bedrock-agentcore:DeleteBrowser",
                "bedrock-agentcore:StartBrowserSession",
                "bedrock-agentcore:ListBrowserSessions",
                "bedrock-agentcore:GetBrowserSession",
                "bedrock-agentcore:StopBrowserSession",
                "bedrock-agentcore:UpdateBrowserStream",
                "bedrock-agentcore:ConnectBrowserAutomationStream",
                "bedrock-agentcore:ConnectBrowserLiveViewStream"
            ],
            "Resource": "arn:aws:bedrock-agentcore:<Region>:<account_id>:browser/*"
        },
        {
            "Sid": "BedrockModelAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

###### Note

Thay thế `<Region>` bằng AWS Region thực tế của bạn và `<account_id>` bằng AWS account ID của bạn.

## Bước 1: Cài đặt các dependency

```bash
pip install bedrock-agentcore strands-agents strands-agents-tools playwright nest-asyncio
```

## Bước 2: Tạo agent của bạn

Tạo một tệp có tên `browser_agent.py`:

###### Note

Thay thế `<Region>` bằng AWS Region của bạn (ví dụ, `us-west-2`).

```python
from strands import Agent
from strands_tools.browser import AgentCoreBrowser

# Initialize the Browser tool
browser_tool = AgentCoreBrowser(region="<Region>")

# Create an agent with the Browser tool
agent = Agent(tools=[browser_tool.browser])

# Test the agent with a web search prompt
prompt = "what are the services offered by Bedrock AgentCore? Use the documentation link if needed: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html"
print(f"\n\nPrompt: {prompt}\n\n")

response = agent(prompt)
print("\n\nAgent Response:")
print(response.message["content"][0]["text"])
```

## Bước 3: Chạy agent

```bash
python browser_agent.py
```

Bạn sẽ thấy agent điều hướng website và trả về chi tiết về các dịch vụ AgentCore. Nếu gặp lỗi, hãy kiểm tra lại quyền IAM, quyền truy cập mô hình và AWS credential của bạn.

## Bước 4: Xem phiên trình duyệt trực tiếp

Trong khi agent đang chạy, bạn có thể xem nó theo thời gian thực qua AWS Console:

- Mở [AgentCore Browser Console](https://us-west-2.console.aws.amazon.com/bedrock-agentcore/builtInTools)

- Điều hướng đến **Built-in tools** trong thanh điều hướng bên trái

- Chọn Browser tool (ví dụ, `AgentCore Browser Tool`, hoặc trình duyệt tùy chỉnh của bạn)

- Trong phần **Browser sessions**, tìm phiên đang hoạt động của bạn với trạng thái **Ready**

- Trong cột **Live view / recording**, nhấp vào URL "View live session" được cung cấp

Chế độ xem trực tiếp cung cấp luồng video thời gian thực với các điều khiển tương tác để tiếp quản hoặc nhả quyền điều khiển khỏi tự động hóa.

## Tìm các tài nguyên của bạn

Sau khi dùng AgentCore Browser, xem các tài nguyên của bạn trong AWS Console:

| # | Tài nguyên | Vị trí |
| --- | --- | --- |
| 1 | Live View | Browser Console > Tên Tool > **View live session** |
| 2 | Session Recordings and Replay | Browser Console > Tên Tool > **View recording** |
| 3 | Browser Logs | **CloudWatch** > **Log groups** > `/aws/bedrock-agentcore/browser/` |
| 4 | Recording Files | **S3** > Bucket của bạn > tiền tố `browser-recordings/` |
| 5 | Custom Browsers | **AgentCore Console** > **Built-in tools** > Trình duyệt tùy chỉnh của bạn |
| 6 | IAM Roles | **IAM** > **Roles** > Tìm execution role của bạn |

## Các bước tiếp theo

Giờ khi bạn đã có AgentCore Browser hoạt động, hãy khám phá các tính năng nâng cao sau:

- [Session Recording and Replay](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-session-recording.html) - Ghi và phát lại các phiên để gỡ lỗi

- [Using AgentCore Browser with Nova Act](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-nova-act.html) và [Using AgentCore Browser with Playwright](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html) - Dùng các framework khác như Nova Act hoặc Playwright

- [Fundamentals](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-resource-session-management.html) - Tìm hiểu về các API operation và trình duyệt tùy chỉnh
