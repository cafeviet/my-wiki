---
title: "Bắt đầu với AgentCore Gateway"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html"
---
# Bắt đầu với AgentCore Gateway

Trong hướng dẫn khởi động nhanh này, bạn sẽ học cách thiết lập một gateway (cổng) và tích hợp nó vào các Agent (tác tử AI) của mình bằng AgentCore CLI. Về các hướng dẫn và ví dụ đầy đủ hơn, xem [Amazon Bedrock AgentCore Gateway GitHub repository](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/07-centralize-and-govern-your-ai-infrastructure/01-gateway).

###### Lưu ý

AgentCore CLI cung cấp cả các lệnh lẫn một trình hướng dẫn TUI tương tác để quản lý các tài nguyên AgentCore Gateway. Về tài liệu tham chiếu API AWS SDK đầy đủ, xem [AgentCore Control Plane operations](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html).

###### Chủ đề

- [Prerequisites](#gateway-quick-start-prereqs)

- [Step 1: Setup and install](#gateway-quick-start-setup)

- [Step 2: Create gateway](#gateway-quick-start-create-gateway-setup)

- [Step 3: Run the setup](#gateway-quick-start-run-setup)

- [Step 4: Use the gateway with an agent](#gateway-quick-start-use-gateway-with-agents)

- [What you’ve built](#gateway-quick-start-what-youve-built)

- [Troubleshooting](#gateway-quick-start-troubleshooting)

- [Quick validation](#gateway-quick-start-quick-validation)

- [Cleanup](#gateway-quick-start-cleanup)

- [Next steps](#gateway-quick-start-next-steps)

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy đảm bảo bạn có những thứ sau:

- **Tài khoản AWS** đã cấu hình thông tin xác thực. Để cấu hình thông tin xác thực, bạn có thể cài đặt và dùng AWS Command Line Interface bằng cách làm theo các bước tại [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

- **Node.js 20+** đã cài đặt (cho AgentCore CLI).

- **Python 3.10+** đã cài đặt (cho script Agent).

- **Quyền IAM** để tạo role, hàm Lambda, và dùng Amazon Bedrock AgentCore.

- **Quyền truy cập model.** Amazon Bedrock mặc định bật quyền truy cập các foundation model. Để dùng một model không phải foundation model, làm theo [các bước cấp quyền truy cập model](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html#model-access-sdk-step4).

## Bước 1: Thiết lập và cài đặt

Cài đặt AgentCore CLI toàn cục:

```bash
npm install -g @aws/agentcore
```

Tạo một dự án AgentCore mới với một Agent và một gateway:

###### Ví dụ

- `agentcore create --project-name MyGatewayProject --name MyGatewayAgent \
  --language Python --framework Strands --model-provider Bedrock --memory none
cd MyGatewayProject`
                        Các tùy chọn này tạo một Agent Python Strands dùng Amazon Bedrock và không có memory. Ngoài ra, chạy `agentcore create` không kèm tùy chọn và chọn **Agent** trong trình hướng dẫn tương tác.

- Bạn cũng có thể chạy `agentcore create` không kèm cờ để dùng trình hướng dẫn tương tác. Trình hướng dẫn dẫn bạn qua việc chọn tên dự án, framework Agent, model provider, và các tùy chọn khác.

## Bước 2: Tạo gateway

Thêm một gateway và một target vào dự án của bạn bằng AgentCore CLI:

###### Ví dụ

- `# Add a gateway with no inbound auth (simplest for getting started)
agentcore add gateway --name TestGateway --authorizer-type NONE --runtimes MyGatewayAgent

# Add a Lambda function target
agentcore add gateway-target --name TestLambdaTarget --type lambda-function-arn \
  --lambda-arn  \
  --tool-schema-file tools.json \
  --gateway TestGateway`

- Chạy `agentcore` để mở TUI, sau đó chọn **add** và chọn **Gateway** :

- Nhập tên gateway:

- Chọn loại authorizer. Với hướng dẫn nhanh này, chọn **NONE** :

- Cấu hình các tùy chọn nâng cao hoặc chấp nhận các giá trị mặc định:

- Xem lại cấu hình và nhấn **Enter** để xác nhận:

  Tiếp theo, chọn **add** lần nữa và chọn **Gateway Target** để thêm một Lambda function target:

- Nhập tên target.

- Chọn **Lambda function** làm loại target:

- Nhập Lambda ARN và đường dẫn file tool schema, sau đó xác nhận.

Để dùng ủy quyền dựa trên JWT thay thế, chỉ định `--authorizer-type CUSTOM_JWT` với OAuth discovery URL của bạn:

###### Ví dụ

- `agentcore add gateway --name TestGateway \
  --authorizer-type CUSTOM_JWT \
  --discovery-url https://cognito-idp.us-east-1.amazonaws.com//.well-known/openid-configuration \
  --allowed-audience  \
  --runtimes MyGatewayAgent`

- Chạy `agentcore` để mở TUI, sau đó chọn **add** và chọn **Gateway** . Khi được hỏi loại authorizer, chọn **Custom JWT** :

- Nhập tên gateway:

- Chọn **Custom JWT** làm loại authorizer:

- Nhập OAuth discovery URL và allowed audience khi được hỏi.

- Cấu hình các tùy chọn nâng cao hoặc chấp nhận các giá trị mặc định:

- Xem lại cấu hình và nhấn **Enter** để xác nhận:

## Bước 3: Chạy thiết lập

Triển khai dự án của bạn lên AWS:

```bash
agentcore deploy
```

CLI tổng hợp (synthesize) một AWS CDK stack và triển khai gateway, các target, và Agent của bạn lên Amazon Bedrock AgentCore. Việc này mất khoảng 2-3 phút.

## Bước 4: Dùng gateway với một Agent

Truy xuất gateway URL của bạn bằng AgentCore CLI:

```bash
agentcore status
```

Tạo một file mới tên `run_agent.py` và chèn đoạn code sau. Cài đặt các phụ thuộc Python trước:

```bash
pip install strands-agents mcp
```

```python
"""
Agent script to test the Gateway
Run this after setup: python run_agent.py
"""

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
import json
import sys

def create_streamable_http_transport(mcp_url: str):
    return streamablehttp_client(mcp_url)

def get_full_tools_list(client):
    """Get all tools with pagination support"""
    more_tools = True
    tools = []
    pagination_token = None
    while more_tools:
        tmp_tools = client.list_tools_sync(pagination_token=pagination_token)
        tools.extend(tmp_tools)
        if tmp_tools.pagination_token is None:
            more_tools = False
        else:
            more_tools = True
            pagination_token = tmp_tools.pagination_token
    return tools

def run_agent():
    # Get the gateway URL from agentcore status
    gateway_url = "<YOUR_GATEWAY_URL>"  # Replace with URL from 'agentcore status'

    # Model configuration - change if needed
    model_id = "anthropic.claude-3-7-sonnet-20250219-v1:0"

    print("Starting AgentCore Gateway Test Agent")
    print(f"Gateway URL: {gateway_url}")
    print(f"Model: {model_id}")
    print("-" * 60)

    # Setup Bedrock model
    bedrockmodel = BedrockModel(
        model_id=model_id,
        streaming=True,
    )

    # Setup MCP client (no auth token needed for NONE authorizer)
    mcp_client = MCPClient(lambda: create_streamable_http_transport(gateway_url))

    with mcp_client:
        # List available tools
        tools = get_full_tools_list(mcp_client)
        print(f"\nAvailable tools: {[tool.tool_name for tool in tools]}")
        print("-" * 60)

        # Create agent
        agent = Agent(model=bedrockmodel, tools=tools)

        # Interactive loop
        print("\nInteractive Agent Ready!")
        print("Try asking: 'What's the weather in Seattle?'")
        print("Type 'exit', 'quit', or 'bye' to end.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break

            print("\nThinking...\n")
            response = agent(user_input)
            print(f"\nAgent: {response.message.get('content', response)}\n")

if __name__ == "__main__":
    run_agent()
```

### Chạy Agent của bạn

Kiểm thử gateway của bạn bằng cách chạy Agent và tương tác với các tool.

```bash
python run_agent.py
```

Vậy là xong! Agent sẽ khởi động và bạn có thể đặt các câu hỏi như:

- "What’s the weather in Seattle?"

- "What time is it in New York?"

## Những gì bạn đã xây dựng

Qua hướng dẫn bắt đầu này, bạn đã tạo ra các tài nguyên sau:

- **MCP Server (Gateway)** : Một endpoint được quản lý tại `https://gateway-id.gateway.bedrock-agentcore.region.amazonaws.com/mcp`

- **Lambda tools** : Các hàm giả lập trả về dữ liệu thử nghiệm (thời tiết: "72°F, Sunny", giờ: "2:30 PM")

- **AI agent** : Trợ lý chạy bằng Claude có thể khám phá và dùng các tool của bạn

## Xử lý sự cố

Bảng dưới đây cho biết một số vấn đề có thể gặp và giải pháp:

| Vấn đề | Giải pháp |
| --- | --- |
| "No module named 'strands'" | Chạy: `pip install strands-agents` |
| "Model access denied" | Amazon Bedrock mặc định bật quyền truy cập các foundation model. Với một model không phải foundation model, làm theo [các bước cấp quyền truy cập model](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html#model-access-sdk-step4). |
| "AccessDeniedException" | Kiểm tra quyền IAM cho bedrock-agentcore:* |
| Gateway không phản hồi | Chờ 30-60 giây sau khi tạo để DNS lan truyền |

## Kiểm tra nhanh

Chạy các lệnh sau trong terminal để kiểm tra gateway của bạn có hoạt động không.

```bash
# Check your Gateway is working
curl -X POST YOUR_GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Watch live logs
aws logs tail /aws/bedrock-agentcore/gateways/YOUR_GATEWAY_ID --follow
```

## Dọn dẹp

Để gỡ gateway và các target của nó khỏi dự án:

```bash
agentcore remove gateway --name TestGateway
```

Để gỡ tất cả tài nguyên và triển khai lại:

```bash
agentcore remove all
agentcore deploy
```

## Các bước tiếp theo

- **Custom Lambda Tools** : Tạo các hàm Lambda với logic nghiệp vụ của bạn

- **Add Your Own APIs** : Mở rộng Gateway của bạn với các đặc tả OpenAPI cho các dịch vụ thực tế

- **Production Setup** : Cấu hình các VPC endpoint, custom domain, và giám sát
