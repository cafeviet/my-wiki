---
title: "Bắt đầu với AgentCore"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---
# Bắt đầu với AgentCore

# Bắt đầu với Amazon Bedrock AgentCore

Hướng dẫn khởi động nhanh này đưa bạn từ con số không đến một Agent (tác tử AI) đang chạy chỉ trong vài phút bằng AgentCore CLI. Bạn sẽ cài đặt CLI, dựng khung một dự án, kiểm thử cục bộ, triển khai lên AWS, và gọi Agent của mình.

Có hai cách để xây dựng một Agent trên AgentCore, dùng chung một CLI:

- **Managed harness** (khung điều phối được quản lý). Bạn khai báo Agent trong một file cấu hình (model, prompt, tool, memory) và AgentCore chạy vòng lặp giúp bạn. Không cần framework, không cần code điều phối. Đây là hướng phù hợp khi bạn muốn con đường nhanh nhất từ ý tưởng đến một Agent đang chạy. [Tìm hiểu thêm](/dich-thuat/aws-bedrock-agentcore/04-harness/).

- **Code-based agent** (Agent dựa trên mã nguồn). Bạn tự viết vòng lặp của Agent bằng Python với một framework bạn đã quen (Strands, LangGraph, Google ADK, hoặc OpenAI Agents), rồi triển khai lên AgentCore Runtime (môi trường chạy). Bạn kiểm soát hoàn toàn logic điều phối.

Trang này trình bày luồng dựa trên mã nguồn. Về harness, xem [AgentCore harness là gì](/dich-thuat/aws-bedrock-agentcore/04-harness/).

## Đăng ký một tài khoản AWS

### Đăng ký một tài khoản AWS

Để bắt đầu với AWS, bạn cần một tài khoản AWS. Về thông tin tạo tài khoản AWS, xem [Getting started with an AWS account](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html) trong *AWS Account Management Reference Guide*.

## Điều kiện tiên quyết

- **Node.js 20 trở lên.** AgentCore CLI được phân phối dưới dạng gói npm. Kiểm tra bằng `node --version`. Cài đặt từ [nodejs.org](https://nodejs.org) nếu cần.

- **npm.** Đi kèm với Node.js.

- **Một tài khoản AWS đã cấu hình thông tin xác thực.** Cấu hình qua AWS CLI, biến môi trường, hoặc một AWS profile. Xem [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

- **Python 3.10 trở lên** (cho mã Agent). Kiểm tra bằng `python3 --version`.

- **Quyền IAM.** Danh tính của bạn cần quyền để gọi API AgentCore và để đảm nhận (assume) các CDK bootstrap role dùng trong quá trình triển khai. Xem [Use the AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html#runtime-permissions-cli).

- **Quyền truy cập model.** Amazon Bedrock mặc định bật quyền truy cập các foundation model. Các model có sẵn bao gồm Amazon Nova, Anthropic Claude, Meta Llama, và các model của Mistral AI. Để dùng các model không phải foundation model, làm theo [các bước cấp quyền truy cập model](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html#model-access-sdk-step4).

- **Docker.** Chỉ cần thiết nếu bạn chọn build type `Container`. Build type mặc định `CodeZip` không cần Docker.

## Bước 1: Cài đặt AgentCore CLI

```bash
npm install -g @aws/agentcore
```

Kiểm tra:

```bash
agentcore --version
```

###### Lưu ý

Nếu lệnh này báo lỗi thay vì trả về số phiên bản, có nghĩa là một lệnh `agentcore` cũ của Python đang che khuất lệnh npm trên `PATH` của bạn. Điều này xảy ra nếu trước đó bạn đã cài gói pip `bedrock-agentcore-starter-toolkit`, và thường gặp nhất trên Windows. Chạy `pip uninstall bedrock-agentcore-starter-toolkit`, sau đó mở một terminal mới và thử lại.

Để cập nhật về sau, chạy lại lệnh cài đặt hoặc `agentcore update`. Mã nguồn và báo lỗi: [agentcore-cli on GitHub](https://github.com/aws/agentcore-cli).

## Bước 2: Tạo dự án của bạn

```bash
agentcore create
```

Trình hướng dẫn tương tác trước tiên hỏi bạn muốn xây dựng gì:

- **Harness** - Một vòng lặp Agent dựa trên cấu hình, được quản lý. Không cần framework hay code điều phối. Xem [AgentCore harness là gì](/dich-thuat/aws-bedrock-agentcore/04-harness/).

- **Agent** - Một Agent dựa trên mã nguồn dùng framework bạn chọn, triển khai lên AgentCore Runtime.

- **Skip** - Tạo cấu trúc dự án mà không có Agent. Thêm sau bằng `agentcore add`.

Nếu bạn chọn **Agent**, trình hướng dẫn tiếp tục với:

- **Framework** - Strands Agents (khuyến nghị), LangChain/LangGraph, Google Agent Development Kit, hoặc OpenAI Agents SDK

- **Model provider** - Amazon Bedrock, Anthropic, OpenAI, hoặc Gemini

- **Memory** - Không có, chỉ short-term, hoặc cả long-term và short-term

- **Build type** - CodeZip (mặc định) hoặc Container

Bạn cũng có thể truyền cờ trực tiếp để tạo một Agent dựa trên mã nguồn:

```bash
agentcore create \
  --project-name MyProject \
  --name MyAgent \
  --language Python \
  --framework Strands \
  --model-provider Bedrock \
  --memory none \
  --build CodeZip
```

Về tất cả các lệnh và tùy chọn khả dụng, xem [AgentCore CLI reference](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-cli-reference.html).

### Các build type

- `CodeZip` (mặc định) đóng gói code của bạn vào một file zip và tải lên Amazon S3. Build type này không cần Docker.

- `Container` build và triển khai một container image. Build type này yêu cầu một Docker daemon đang chạy.

### Cấu trúc dự án

`agentcore create` tạo ra cấu hình dự án dùng chung và một cấu trúc ứng dụng khác nhau cho Agent dựa trên mã nguồn và cho harness:

###### Ví dụ

```text
MyProject/
├── AGENTS.md
├── README.md
├── agentcore/
│   ├── agentcore.json
│   ├── aws-targets.json
│   └── cdk/
└── app/
    └── MyAgent/
        ├── main.py
        ├── pyproject.toml
        ├── README.md
        ├── model/
        ├── mcp_client/
        └── skills/
```

```text
MyHarnessProject/
├── AGENTS.md
├── README.md
├── agentcore/
│   ├── agentcore.json
│   ├── aws-targets.json
│   └── cdk/
└── app/
    └── MyHarness/
        ├── harness.json
        └── system-prompt.md
```

Các file quan trọng:

- `agentcore/agentcore.json` - File cấu hình chính. Nó định nghĩa các Agent, harness, memory store, gateway, thông tin xác thực (credential), và các tài nguyên khác của bạn. Các lệnh `agentcore add` và `agentcore remove` quản lý file này.

- `agentcore/aws-targets.json` - Các tài khoản AWS và Region để triển khai.

- `agentcore/.env.local` - Bí mật cục bộ, chẳng hạn API key cho các model provider.

- `app/` - Thư mục ứng dụng. Một Agent dựa trên mã nguồn chứa một entrypoint và các phụ thuộc. Một harness chứa `harness.json` và `system-prompt.md`.

## Bước 3: Kiểm thử cục bộ

```bash
cd MyProject
agentcore dev
```

`agentcore dev` tạo một môi trường ảo Python, cài đặt các phụ thuộc, khởi động một server cục bộ có hot reload, và mở **agent inspector** trong trình duyệt để bạn có thể trò chuyện với Agent, kiểm tra trace, và duyệt các tài nguyên dự án. Các thay đổi mã được tự động nhận vào.

## Bước 4: Triển khai Agent của bạn

```bash
agentcore deploy
```

Deploy:

- Đóng gói code của bạn thành một artifact zip (hoặc build một container nếu dùng `--build Container`)

- Dùng AWS CDK bên dưới để tổng hợp (synthesize) và cấp phát tài nguyên

- Tạo một AgentCore Runtime endpoint cho Agent của bạn

- Cấu hình logging CloudWatch và Observability (khả năng quan sát)

Lần deploy đầu tiên mất vài phút trong khi CDK thực hiện bootstrap tài khoản của bạn. Các lần deploy sau nhanh hơn.

Xem trước những gì sẽ thay đổi mà không thực sự triển khai:

```bash
agentcore deploy --dry-run
```

Kiểm tra trạng thái:

```bash
agentcore status
```

## Bước 5: Gọi Agent đã triển khai

```bash
agentcore invoke --prompt "Hello, what can you do?"
```

Nếu Agent của bạn có cấu hình payments, hãy cung cấp payment context tại thời điểm gọi:

```bash
agentcore invoke \
  --prompt "Access https://example-x402-merchant.com/paid-api" \
  --payment-instrument-id <INSTRUMENT_ID> \
  --auto-session \
  --payment-user-id user@example.com
```

Đó là toàn bộ vòng lặp. Lặp lại trên `app/MyAgent/main.py`, kiểm thử với `agentcore dev`, triển khai với `agentcore deploy`, gọi với `agentcore invoke`.

## Thêm năng lực cho dự án của bạn

`agentcore add` quản lý các tài nguyên trong `agentcore.json`. Chạy nó không kèm đối số để mở menu tương tác, hoặc nhắm trực tiếp vào một tài nguyên.

```bash
agentcore add memory        # Store conversation context
agentcore add agent         # Add a second agent to the same project
agentcore add gateway       # Connect external APIs/tools through Gateway
agentcore add credential    # Add an API key for a non-Bedrock provider
agentcore add evaluator     # Quality evaluation
agentcore add payment-manager   # Payments: create a payment manager
agentcore add payment-connector # Payments: link a payment provider
```

Mỗi lệnh add dựng khung cấu hình và hỏi các giá trị bắt buộc. Sau khi thêm, chạy `agentcore deploy` để cấp phát.

Đi sâu vào các năng lực bạn có thể gắn thêm:

- [AgentCore Memory](/dich-thuat/aws-bedrock-agentcore/07-memory/) - bộ nhớ short-term và long-term, các chiến lược truy hồi

- [AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/) - kết nối được quản trị đến các API và MCP server

- [AgentCore Browser](/dich-thuat/aws-bedrock-agentcore/12-browser/) - duyệt web được quản lý cho các Agent

- [AgentCore Code Interpreter](/dich-thuat/aws-bedrock-agentcore/11-code-interpreter/) - thực thi mã trong sandbox

- [AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/) - OAuth, credential provider dạng API key, workload identity

- [AgentCore Observability](/dich-thuat/aws-bedrock-agentcore/13-observability/) - trace, log, và metric trong CloudWatch

- [AgentCore VPC](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-vpc.html) - chạy các Agent bên trong VPC của bạn

- [AgentCore Payments](/dich-thuat/aws-bedrock-agentcore/10-payments/) - thanh toán vi giao dịch cho các Agent qua x402

## Xem log và trace

```bash
# Stream recent logs
agentcore logs

# Filter
agentcore logs --since 30m --level error
agentcore logs --query "timeout"

# List recent traces
agentcore traces list

# Get a specific trace
agentcore traces get <trace-id>
```

## Xử lý sự cố

Xác minh thông tin xác thực của bạn bằng `aws sts get-caller-identity`. Đảm bảo danh tính của bạn có các quyền trong [Use the AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html#runtime-permissions-cli).

Amazon Bedrock mặc định bật quyền truy cập các foundation model. Để dùng một model không phải foundation model, làm theo [các bước cấp quyền truy cập model](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html#model-access-sdk-step4).

Chạy `agentcore deploy --verbose` để hiển thị các sự kiện triển khai ở cấp tài nguyên. CLI kiểm tra trạng thái AWS CDK bootstrap. Nếu cần bootstrap, việc triển khai tương tác sẽ hỏi xác nhận. `agentcore deploy --yes` phê duyệt thao tác bootstrap mà không hỏi.

Chạy `agentcore dev --port 3000` để dùng một cổng cục bộ khác.

Chạy `agentcore validate` để kiểm tra cấu hình dự án.

Để biết thêm thông tin, xem [Troubleshoot Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html).

## Dọn dẹp

```bash
agentcore remove all
agentcore deploy
```

`remove all` đặt lại cấu hình. Lệnh `deploy` tiếp theo phát hiện trạng thái rỗng và gỡ bỏ các tài nguyên trong tài khoản của bạn.

## Các bước tiếp theo

- [AgentCore harness là gì](/dich-thuat/aws-bedrock-agentcore/04-harness/) - con đường dựa trên cấu hình đến một Agent đang chạy. Dùng bất kỳ model nào, kết nối tới các tool, lưu bền trạng thái, triển khai trong VPC của bạn, và chuyển sang code khi bạn cần.

- [AgentCore code samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples) - các ví dụ đầu cuối trên nhiều framework và năng lực.
