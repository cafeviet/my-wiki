---
title: "AgentCore MCP Server: Vibe coding với trợ lý lập trình của bạn"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-server.html"
---

# AgentCore MCP Server: Vibe coding với trợ lý lập trình của bạn

# Amazon Bedrock AgentCore MCP Server: Vibe coding với trợ lý lập trình của bạn

Amazon Bedrock AgentCore Model Context Protocol (MCP) server giúp bạn chuyển đổi, triển khai và kiểm thử các agent (tác tử AI) tương thích với Amazon Bedrock AgentCore ngay từ môi trường phát triển ưa thích của bạn. Với hỗ trợ tích hợp sẵn cho việc tích hợp runtime (môi trường chạy), kết nối gateway (cổng) và quản lý vòng đời agent, MCP server đơn giản hóa việc chuyển từ phát triển cục bộ sang triển khai production trên các dịch vụ Amazon Bedrock AgentCore.

MCP server hoạt động với các MCP client phổ biến bao gồm Kiro, Cursor, Claude Code và Amazon Q CLI, cung cấp các lệnh dạng hội thoại để tự động hóa các quy trình phát triển agent phức tạp.

###### Topics

- [Prerequisites](#mcp-prerequisites)

- [Step 1: Install the MCP server](#mcp-install-server)

- [Step 2: Transform an existing agent for AgentCore Runtime compatibility](#mcp-transform-agent)

- [Step 3: Deploy your agent to AgentCore Runtime](#mcp-deploy-agent)

- [Step 4: Test your deployed agent](#mcp-test-agent)

- [Next steps](#mcp-next-steps)

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy xác minh rằng bạn có những điều sau:

- Một tài khoản AWS với các quyền Amazon Bedrock AgentCore

- **Node.js 20+** đã cài đặt (cần thiết cho AgentCore CLI)

- AWS CLI đã cài đặt và cấu hình với credential phù hợp. Để biết hướng dẫn thiết lập, xem [Installing or updating to the latest version of the AWS CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html).

- Một trong các MCP client được hỗ trợ:

    - Kiro

    - Cursor

    - Claude Code

    - Amazon Q CLI

- Một AgentCore agent hiện có được xây dựng bằng một framework được hỗ trợ (Strands Agents, LangGraph, hoặc tương tự)

Để biết thêm thông tin về Amazon Bedrock AgentCore, xem [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/).

### Cài đặt các dependency cần thiết

Cài đặt các gói cần thiết cho việc phát triển Amazon Bedrock AgentCore.

Để cài đặt các gói cần thiết, chạy các lệnh sau:

```bash
# Install the AgentCore CLI
npm install -g @aws/agentcore
```

```bash
# Install the AgentCore Python SDK
pip install bedrock-agentcore
```

## Bước 1: Cài đặt MCP server

Để cài đặt AgentCore MCP server, thêm nó vào tệp cấu hình của MCP client của bạn. Mỗi MCP client lưu cấu hình này ở một vị trí khác nhau.

### Thêm cấu hình MCP server

Chọn MCP client của bạn và thêm cấu hình tương ứng:

#### Với Kiro

Thêm vào `.kiro/settings/mcp.json` (nếu chưa tồn tại, xem [Creating Configuration Files](https://kiro.dev/docs/mcp/configuration/#creating-configuration-files) ):

```json
{
  "mcpServers": {
    "bedrock-agentcore-mcp-server": {
      "command": "uvx",
      "args": [
        "awslabs.amazon-bedrock-agentcore-mcp-server@latest"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_agentcore_docs",
        "fetch_agentcore_doc"
      ]
    }
  }
}
```

#### Với Cursor

Thêm vào `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "bedrock-agentcore-mcp-server": {
      "command": "uvx",
      "args": [
        "awslabs.amazon-bedrock-agentcore-mcp-server@latest"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_agentcore_docs",
        "fetch_agentcore_doc"
      ]
    }
  }
}
```

#### Với Amazon Q

Thực hành tốt nhất là cấu hình MCP server cho từng Q CLI agent riêng lẻ. Để biết hướng dẫn cấu hình, xem [Configuring MCP servers for Amazon Q CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-config-CLI.html).

Với Amazon Q trong các IDE (VS Code và JetBrains), xem [Using MCP servers with Amazon Q in your IDE](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/mcp-ide.html).

#### Với Claude Code

Cấu hình phụ thuộc vào cách cài đặt của bạn:

- **Ứng dụng độc lập (standalone app)**: Thêm vào `~/.claude/mcp.json`

- **Tiện ích mở rộng VS Code**: Cấu hình các MCP server thông qua Claude Code CLI trước, sau đó tiện ích mở rộng sẽ tự động dùng chúng. Xem [Claude Code VS Code documentation](https://docs.claude.com/en/docs/claude-code/vs-code) để biết chi tiết thiết lập.

Với ứng dụng Claude Code độc lập:

```json
{
  "mcpServers": {
    "bedrock-agentcore-mcp-server": {
      "command": "uvx",
      "args": [
        "awslabs.amazon-bedrock-agentcore-mcp-server@latest"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_agentcore_docs",
        "fetch_agentcore_doc"
      ]
    }
  }
}
```

### Xác minh cài đặt MCP server

Để xác minh rằng MCP server đã được kết nối và hoạt động thành công, khởi động lại MCP client của bạn sau khi thêm cấu hình và xác nhận rằng các tool sau đây khả dụng:

- `search_agentcore_docs` - Tìm kiếm tài liệu Amazon Bedrock AgentCore

- `fetch_agentcore_doc` - Lấy các trang tài liệu Amazon Bedrock AgentCore cụ thể

## Bước 2: Chuyển đổi một agent hiện có để tương thích với AgentCore Runtime

Để làm cho mã AgentCore agent hiện có của bạn tương thích với Amazon Bedrock AgentCore Runtime, dùng MCP server để hướng dẫn quá trình chuyển đổi. Ví dụ, nếu bạn có một Strands AgentCore agent, quá trình chuyển đổi sẽ giúp chuyển nó sang tương thích với Amazon Bedrock AgentCore bằng cách cập nhật các import, dependency và cấu trúc ứng dụng.

### Chuyển đổi mã agent của bạn

MCP server hướng dẫn MCP client của bạn thực hiện các thay đổi sau đối với mã AgentCore agent:

#### Thêm các import thư viện runtime

MCP server thêm các import AgentCore cần thiết:

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
```

#### Cập nhật các dependency

MCP server cập nhật tệp `requirements.txt` của bạn:

```nohighlight
bedrock-agentcore
strands-agents
```

#### Khởi tạo ứng dụng AgentCore

MCP server thêm phần khởi tạo ứng dụng:

```python
app = BedrockAgentCoreApp()
```

#### Trang trí (decorate) entrypoint chính

MCP server chuyển đổi hàm handler của bạn:

```python
@app.entrypoint
def handler(event, context):
    # Your agent logic here
    pass
```

#### Thêm application runner

MCP server thêm application runner:

```python
if __name__ == "__main__":
    app.run()
```

### Quy trình chuyển đổi

Để chuyển đổi AgentCore agent của bạn, mở tệp AgentCore agent hiện có (ví dụ, `weather_agent.py`) trong MCP client của bạn và dùng trợ lý AI của MCP client với prompt sau:

```text
Transform this AgentCore agent code to be compatible with AgentCore runtime. Update the imports, dependencies, and application structure as needed.
```

## Bước 3: Triển khai agent của bạn lên AgentCore Runtime

Sau khi chuyển đổi AgentCore agent để tương thích với AgentCore Runtime, triển khai nó bằng AgentCore CLI thông qua MCP client của bạn.

### Triển khai bằng AgentCore CLI

MCP server dùng AgentCore CLI để triển khai AgentCore agent của bạn. Quy trình triển khai bao gồm:

- Tạo cấu hình triển khai

- Build và đóng gói container cho AgentCore agent

- Triển khai lên Amazon Bedrock AgentCore Runtime

- Cung cấp chi tiết triển khai và ARN của AgentCore agent

Để triển khai AgentCore agent của bạn, dùng trợ lý AI của MCP client với prompt sau:

```text
Deploy this AgentCore agent to AgentCore runtime using the AgentCore CLI.
```

MCP server tự động thực thi các lệnh CLI cần thiết.

### Xác minh triển khai

Sau khi triển khai hoàn tất, bạn nhận được xác nhận với các chi tiết sau:

- ARN của AgentCore agent

- Cấu hình runtime

- Trạng thái triển khai

## Bước 4: Kiểm thử agent đã triển khai của bạn

Kiểm thử AgentCore agent đã triển khai của bạn bằng cách gọi (invoke) nó thông qua Amazon Bedrock AgentCore Runtime.

### Gọi agent

MCP server dùng AgentCore CLI để gọi AgentCore agent của bạn và hiển thị kết quả bao gồm:

- Phản hồi của AgentCore agent

- Log thực thi

- Các chỉ số hiệu năng (performance metric)

Để kiểm thử AgentCore agent đã triển khai của bạn, dùng trợ lý AI của MCP client với prompt sau:

```text
Test the deployed AgentCore agent with a sample request.
```

Xem lại kết quả gọi:

```text
AgentCore Agent Response: Hello! I can help you with weather information.
Execution Time: 1.2s
Status: Success
```

## Các bước tiếp theo

Sau khi bạn triển khai và kiểm thử thành công AgentCore agent đầu tiên với Amazon Bedrock AgentCore MCP server, bạn có thể khám phá các năng lực bổ sung:

- *Stateful MCP features* - Xây dựng các MCP server với resource, prompt, elicitation, sampling và progress notification. Xem [Stateful MCP server features](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-stateful-features.html).

- *Tool integration* - Kết nối AgentCore agent của bạn tới Amazon Bedrock AgentCore Gateway (cổng) để truy cập tool bên ngoài

- *Memory integration* - Thêm Amazon Bedrock AgentCore Memory (bộ nhớ) cho bối cảnh hội thoại

- *Identity management* - Triển khai Amazon Bedrock AgentCore Identity (danh tính) để kiểm soát truy cập an toàn

- *Advanced frameworks* - Khám phá tích hợp với LangGraph và các framework khác

Để biết thêm thông tin, xem những nội dung sau:

- [Get started with AgentCore Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/runtime-getting-started)

- [Get started with AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/gateway-quick-start)

- [AgentCore CLI reference](https://github.com/aws/agentcore-cli)
