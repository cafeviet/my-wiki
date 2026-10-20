---
title: "Bắt đầu với AgentCore Observability"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html"
---

# Bắt đầu với AgentCore Observability

Amazon Bedrock AgentCore Observability (khả năng quan sát) giúp bạn trace, debug, và giám sát hiệu năng agent (tác tử AI) trong các môi trường production. Hướng dẫn này giúp bạn triển khai các tính năng observability trong các ứng dụng agent của mình.

###### Các chủ đề

- [Điều kiện tiên quyết](#prerequisites)

- [Bước 1: Bật transaction search trên CloudWatch](#enabling-transaction-search)

- [Bước 2: Bật observability cho các agent được host trên Amazon Bedrock AgentCore Runtime](#enabling-observability-runtime-hosted)

- [Bước 3: Bật observability cho các agent không được host trên Amazon Bedrock AgentCore](#enabling-observability-non-runtime-hosted)

- [Bước 4: Quan sát agent của bạn với GenAI observability trên Amazon CloudWatch](#agentcore-observability-genai-cloudwatch)

- [Thực hành tốt nhất](#best-practices)

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy chắc chắn bạn có:

- **AWS Account** với thông tin xác thực đã cấu hình ( `aws configure` ) và đã bật quyền truy cập model tới Foundation Model bạn muốn dùng.

- **Python 3.10+** đã cài đặt

- **Bật transaction search** trên Amazon CloudWatch. Chỉ một lần, người dùng lần đầu phải bật [CloudWatch Transaction Search](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Enable-TransactionSearch.html) để xem các span và trace của Amazon Bedrock AgentCore

- **(Chỉ cho agent non-runtime) Thêm thư viện OpenTelemetry** – Bao gồm `aws-opentelemetry-distro` (ADOT) trong file requirements.txt của bạn. Nếu bạn host agent trên AWS Lambda, dùng [AWS Lambda Layer for OpenTelemetry](https://aws-otel.github.io/docs/getting-started/lambda) trên website AWS Distro for OpenTelemetry thay thế.

- **(Chỉ cho agent non-runtime)** Đảm bảo framework của bạn được cấu hình để phát ra các trace (ví dụ, package `strands-agents[otel]`). Đôi khi bạn có thể cần bao gồm auto-instrumentor của framework agent (ví dụ, `opentelemetry-instrumentation-langchain` ).

Amazon Bedrock AgentCore Observability cung cấp hai cách cấu hình giám sát để phù hợp với các nhu cầu hạ tầng khác nhau:

- Các agent được host trên Amazon Bedrock AgentCore Runtime

- Các agent được host non-runtime

Như một thiết lập một lần cho mỗi AWS account, người dùng lần đầu cần bật Transaction Search trên Amazon CloudWatch. Có hai cách để làm điều này, qua API và qua CloudWatch Console.

## Bước 1: Bật transaction search trên CloudWatch

Sau khi bạn bật Transaction Search, có thể mất mười phút để các span sẵn sàng cho tìm kiếm và phân tích. Chọn một trong các tùy chọn dưới đây:

### Tùy chọn 1: Bật transaction search bằng một API

**Để bật transaction search bằng API**

- Tạo một policy cấp quyền ingest span trong CloudWatch Logs bằng AWS CLI.
  Một ví dụ được trình bày dưới đây về cách định dạng lệnh AWS CLI với `PutResourcePolicy`.
  `aws logs put-resource-policy --policy-name MyResourcePolicy --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "TransactionSearchXRayAccess", "Effect": "Allow", "Principal": { "Service": "xray.amazonaws.com" }, "Action": "logs:PutLogEvents", "Resource": [ "arn:partition:logs:region:account-id:log-group:aws/spans:*", "arn:partition:logs:region:account-id:log-group:/aws/application-signals/data:*" ], "Condition": { "ArnLike": { "aws:SourceArn": "arn:partition:xray:region:account-id:*" }, "StringEquals": { "aws:SourceAccount": "account-id" } } } ]}'`

- Cấu hình đích đến của các trace segment.
  Một ví dụ được trình bày dưới đây về cách định dạng lệnh AWS CLI với `UpdateTraceSegmentDestination`.
  `aws xray update-trace-segment-destination --destination CloudWatchLogs`

- **Tùy chọn** Cấu hình lượng span để lập chỉ mục (index).
  Cấu hình phần trăm sampling mong muốn của bạn với `UpdateIndexingRule`.
  `aws xray update-indexing-rule --name "Default" --rule '{"Probabilistic": {"DesiredSamplingPercentage": number}}'`

### Tùy chọn 2: Bật transaction search trong CloudWatch console

**Để bật transaction search trong CloudWatch console**

- Mở CloudWatch console tại [https://console.aws.amazon.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/).

- Trong navigation pane bên dưới **Setup** , chọn **Settings**.

- Chọn **Account** và chọn tab **X-Ray traces**.

- Trong phần **Transaction Search**, chọn **View settings**.

- Trên trang mở ra, chọn **Edit**.

- Chọn **Enable Transaction Search**.

- Chọn **For X-Ray users** và nhập phần trăm trace để lập chỉ mục. Bạn có thể index 1% trace miễn phí và điều chỉnh phần trăm này sau dựa trên nhu cầu của bạn.

- Chọn **Save** . Chờ đến khi **Ingest OpenTelemetry spans** hiển thị **Enabled** trước khi gửi trace.

Bây giờ ta hãy chuyển sang khám phá hai cách cấu hình observability.

## Bước 2: Bật observability cho các agent được host trên Amazon Bedrock AgentCore Runtime

Các agent được host trên Amazon Bedrock AgentCore Runtime được deploy và thực thi trực tiếp bên trong môi trường Amazon Bedrock AgentCore, cung cấp instrumentation tự động với cấu hình tối thiểu. Khi bạn deploy một agent bằng AgentCore CLI, runtime tự động instrument agent của bạn với OpenTelemetry — không cần thêm thư viện OTEL hay cấu hình nào.

Để xem một ví dụ đầy đủ, tham khảo [các mẫu AgentCore Observability trên GitHub](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/06-observe-evaluate-optimize-your-agent/01-observe)

### Tạo dự án agent của bạn

Tạo một dự án mới bằng AgentCore CLI. Việc này thiết lập thư mục dự án, virtual environment, và các dependency của bạn:

```bash
npm install -g @aws/agentcore
agentcore create \
  --project-name StrandsObservability \
  --name StrandsClaudeGettingStarted \
  --language Python \
  --framework Strands \
  --model-provider Bedrock \
  --memory none
cd StrandsObservability/app/StrandsClaudeGettingStarted
uv add strands-agents-tools
cd ../..
```

Trong thư mục agent của dự án, thay thế mã agent mặc định bằng logic agent của riêng bạn. Sau đây là một ví dụ dùng Strands Agents SDK:

```python
## app/StrandsClaudeGettingStarted/main.py
from strands import Agent, tool
from strands_tools import calculator
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

@tool
def weather():
    """Get weather"""
    return "sunny"

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
)
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)

@app.entrypoint
def strands_agent_bedrock(payload):
    """Invoke the agent with a payload"""
    user_input = payload.get("prompt")
    if not isinstance(user_input, str) or not user_input:
        return "Error: 'prompt' must be a non-empty string"
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
```

### Deploy và gọi agent của bạn

Deploy agent lên AgentCore Runtime. AgentCore CLI xử lý việc đóng gói, deploy, và instrumentation OTEL tự động:

```bash
agentcore deploy
```

Sau khi deploy, agent của bạn chạy trên AgentCore Runtime và được instrument tự động bằng OpenTelemetry. Gọi agent của bạn và xem các trace, session, và metric trên bảng điều khiển GenAI Observability trong Amazon CloudWatch:

```bash
agentcore invoke
```

Ngoài ra, bạn có thể gọi agent của mình bằng lập trình qua AWS SDK:

```python
import boto3, json

client = boto3.client('bedrock-agentcore')

response = client.invoke_agent_runtime(
    agentRuntimeArn="YOUR_AGENT_RUNTIME_ARN",
    runtimeSessionId="my-observability-session-001",
    payload=json.dumps({"prompt": "What is 2 + 2?"}),
    qualifier="DEFAULT"
)

print(json.loads(response['response'].read()))
```

## Bước 3: Bật observability cho các agent không được host trên Amazon Bedrock AgentCore

Đối với các agent chạy bên ngoài runtime Amazon Bedrock AgentCore, bạn có thể mang lại các khả năng giám sát tương tự cho các agent được deploy trên hạ tầng của riêng bạn. Điều này cho phép observability nhất quán bất kể agent của bạn chạy ở đâu. Dùng các bước sau để cấu hình các biến môi trường cần thiết để quan sát các agent của bạn.

Để xem một ví dụ đầy đủ, xem [mẫu Agents on Amazon EKS](https://github.com/awslabs/agentcore-samples/tree/main/03-integrations/agents-hosted-outside-runtime/agents-on-eks) trên website GitHub.

### Cấu hình các biến môi trường AWS

```bash
export AWS_ACCOUNT_ID=<account id>
export AWS_DEFAULT_REGION=<default region>
export AWS_REGION=<region>
export AWS_ACCESS_KEY_ID=<access key id>
export AWS_SECRET_ACCESS_KEY=<secret key>
```

### Cấu hình ghi log CloudWatch

Tạo một log group và log stream cho agent của bạn trong Amazon CloudWatch mà bạn có thể dùng để cấu hình các biến môi trường bên dưới.

### Cấu hình các biến môi trường OpenTelemetry

```bash
export AGENT_OBSERVABILITY_ENABLED=true # Activates the ADOT pipeline
export OTEL_PYTHON_DISTRO=aws_distro # Uses AWS Distro for OpenTelemetry
export OTEL_PYTHON_CONFIGURATOR=aws_configurator # Sets AWS configurator for ADOT SDK
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf # Configures export protocol
export  OTEL_EXPORTER_OTLP_LOGS_HEADERS=x-aws-log-group=<YOUR-LOG-GROUP>,x-aws-log-stream=<YOUR-LOG-STREAM>,x-aws-metric-namespace=<YOUR-NAMESPACE>
# Directs logs to CloudWatch groups
export OTEL_EXPORTER_OTLP_TRACES_HEADERS=x-aws-log-group=<YOUR-LOG-GROUP>,x-aws-log-stream=<YOUR-TRACES-LOG-STREAM>
# (Optional) Directs spans to your log group instead of the aws/spans log group. Requires ADOT version 0.18.0 or later.
export OTEL_RESOURCE_ATTRIBUTES=service.name=<YOUR-AGENT-NAME> # Identifies your agent in observability data
export OTEL_AWS_APPLICATION_SIGNALS_ENABLED=false # AWS Lambda Layer for OpenTelemetry only: disables Application Signals
export OTEL_LOGS_EXPORTER=otlp # AWS Lambda Layer for OpenTelemetry only: exports logs over OTLP
export OTEL_METRICS_EXPORTER=awsemf # AWS Lambda Layer for OpenTelemetry only: exports metrics as CloudWatch EMF
```

Thay `<YOUR-AGENT-NAME>` bằng một tên duy nhất để nhận diện agent này trong bảng điều khiển GenAI Observability và log.

###### Lưu ý

Nếu bạn đặt `OTEL_EXPORTER_OTLP_TRACES_HEADERS` để chuyển span đến log group của riêng bạn, bạn cũng phải thêm một Amazon CloudWatch Logs resource policy. Policy phải cho phép X-Ray (`xray.amazonaws.com`) gọi `logs:PutLogEvents` trên log group đó. Dùng cùng policy được trình bày trong [Bật transaction search bằng một API](#enable-transaction-search-api), với ARN của log group trong `Resource`. Nếu thiếu policy này, X-Ray không thể chuyển span đến log group của bạn.

### Tạo một agent cục bộ

```python
# Create agent.py -  Strands agent that is a weather assistant
from strands import Agent
from strands_tools import http_request

# Define a weather-focused system prompt
WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

1. Make HTTP requests to the National Weather Service API
2. Process and display weather forecast data
3. Provide weather information for locations in the United States

When retrieving weather information:
1. First get the coordinates or grid information using https://api.weather.gov/points/{latitude},{longitude} or https://api.weather.gov/points/{zipcode}
2. Then use the returned forecast URL to get the actual forecast

When displaying responses:
- Format weather data in a human-readable way
- Highlight important information like temperature, precipitation, and alerts
- Handle errors appropriately
- Convert technical terms to user-friendly language

Always explain the weather conditions clearly and provide context for the forecast.
"""

# Create an agent with HTTP capabilities
weather_agent = Agent(
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[http_request],  # Explicitly enable http_request tool
)

response = weather_agent("What's the weather like in Seattle?")
print(response)
```

### Chạy agent của bạn với lệnh instrumentation tự động

Với `aws-opentelemetry-distro` trong file requirements.txt của bạn, lệnh `opentelemetry-instrument` sẽ:

- Nạp cấu hình OTEL của bạn từ các biến môi trường

- Tự động instrument Strands, các lệnh gọi Amazon Bedrock, các agent tool và database, cùng các request khác do agent thực hiện

- Gửi các trace đến CloudWatch

- Cho phép bạn trực quan hóa quá trình ra quyết định của agent trong bảng điều khiển GenAI Observability

Dùng lệnh sau để chạy agent của bạn với instrumentation tự động:

```bash
opentelemetry-instrument python agent.py
```

Nếu bạn host agent trên AWS Lambda, dùng [AWS Lambda Layer for OpenTelemetry](https://aws-otel.github.io/docs/getting-started/lambda) trên website AWS Distro for OpenTelemetry. Thêm layer vào function của bạn, rồi đặt biến môi trường `AWS_LAMBDA_EXEC_WRAPPER` thành `/opt/otel-instrument`. Layer khi đó sẽ tự động instrument function của bạn. Với cách tiếp cận này, bạn không cần thêm package `aws-opentelemetry-distro` hay chạy lệnh `opentelemetry-instrument` được mô tả trước đó.

###### ADOT Collector không được hỗ trợ cho agent observability

ADOT Collector không được hỗ trợ cho agent observability. Để gửi telemetry từ một agent được host bên ngoài AgentCore runtime, bạn phải dùng hoặc ADOT SDK hoặc AWS Lambda Layer for OpenTelemetry.

Bây giờ bạn có thể xem các trace, session và metric của mình trên bảng điều khiển GenAI Observability trên Amazon CloudWatch với giá trị **YOUR-AGENT-NAME** mà bạn đã cấu hình trong [các biến môi trường](#configure-opentelemetry-environment-variables) của mình.

Để tương quan (correlate) các trace qua nhiều lần chạy agent, bạn có thể liên kết một session ID với dữ liệu telemetry của bạn bằng OpenTelemetry baggage:

```python
from opentelemetry import baggage, context
ctx = baggage.set_baggage("session.id", session_id)
```

## Bước 4: Quan sát agent của bạn với GenAI observability trên Amazon CloudWatch

Sau khi triển khai observability, bạn có thể xem dữ liệu đã thu thập trong CloudWatch:

### Quan sát agent của bạn

- Mở [GenAI Observability trên CloudWatch console](https://console.aws.amazon.com/cloudwatch/home#gen-ai-observability)

- Bạn có thể xem dữ liệu liên quan đến các lần gọi model và các agent trên Amazon Bedrock AgentCore trên bảng điều khiển.

- Trong tab Bedrock AgentCore bạn có thể xem Agents View, Sessions View và Traces View.

- Agents View liệt kê tất cả các Agent của bạn ở cả trên và ngoài runtime, bạn cũng có thể chọn một agent và xem chi tiết thêm như các runtime metric, session và trace đặc thù cho một agent.

- Trong tab **Sessions View**, bạn có thể điều hướng qua tất cả các session gắn với các agent.

- Trong tab **Trace View**, bạn có thể xem xét các trace và thông tin span của các agent. Cũng có thể khám phá quỹ đạo trace và dòng thời gian bằng cách chọn một trace.

### Xem log trong CloudWatch

**Để xem log trong CloudWatch**

- Mở [CloudWatch console](https://console.aws.amazon.com/cloudwatch/)

- Trong navigation pane bên trái, mở rộng **Logs** và chọn **Log groups**

- Tìm log group của agent bạn:

  Standard logs (stdout/stderr) Location: `/aws/bedrock-agentcore/runtimes/-/[runtime-logs] `

- OTEL structured logs: `/aws/bedrock-agentcore/runtimes/-/runtime-logs`

### Xem các trace và span

**Để xem các trace và span**

- Mở [CloudWatch console](https://console.aws.amazon.com/cloudwatch/)

- Chọn **Transaction Search** từ navigation bên trái

- Location: log stream `spans` trong log group của agent (`/aws/bedrock-agentcore/runtimes/-`), hoặc log stream `default` trong log group `aws/spans` cho các agent dùng span destination dùng chung

- Lọc theo tên dịch vụ hoặc các tiêu chí khác

- Chọn một trace để xem đồ thị thực thi chi tiết

### Xem các metric

**Để xem các metric**

- Mở [CloudWatch console](https://console.aws.amazon.com/cloudwatch/)

- Chọn **Metrics** từ navigation bên trái

- Duyệt đến namespace `bedrock-agentcore`

- Khám phá các metric có sẵn

## Thực hành tốt nhất

- **Bắt đầu đơn giản, rồi mở rộng** - Observability mặc định do Amazon Bedrock AgentCore cung cấp tự động thu thập hầu hết các metric quan trọng, bao gồm các lệnh gọi model, token usage, và thực thi tool.

- **Cấu hình theo giai đoạn phát triển** - Điều chỉnh cấu hình observability của bạn phù hợp với giai đoạn phát triển hiện tại và điều chỉnh dần.

- **Dùng cách đặt tên nhất quán** - Thiết lập các quy ước đặt tên cho các dịch vụ, span, và attribute ngay từ đầu

- **Lọc dữ liệu nhạy cảm** - Ngăn lộ thông tin bảo mật bằng cách lọc dữ liệu nhạy cảm khỏi các attribute và payload của observability.

- **Thiết lập cảnh báo** - Cấu hình các CloudWatch alarm để thông báo cho bạn về các vấn đề tiềm ẩn trước khi chúng ảnh hưởng đến người dùng
