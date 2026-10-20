---
title: "Bắt đầu với AgentCore harness"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html"
---

# Bắt đầu

Bạn có thể sử dụng harness (khung điều phối) thông qua [AgentCore CLI](https://github.com/aws/agentcore-cli) hoặc trực tiếp bằng các AWS SDK như `boto3`. CLI là con đường nhanh nhất cho hầu hết lập trình viên; các SDK dành cho mục đích sử dụng lập trình từ ứng dụng của riêng bạn.

## Điều kiện tiên quyết

- Thông tin xác thực AWS đã được cấu hình trong một trong các [region được hỗ trợ](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html).

- Đối với CLI: Node.js 20+

- Đối với SDK/boto3: Python 3.10+, [đã cài boto3](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html), và một IAM execution role mà harness có thể assume. Xem [chính sách execution role](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-security.html#harness-execution-role-policy) để biết quyền tối thiểu.

## Bắt đầu

Tạo harness với một tên và execution role:

```bash
aws bedrock-agentcore-control create-harness \
  --harness-name "MyHarness" \
  --execution-role-arn "arn:aws:iam::123456789012:role/MyHarnessRole"
```

Poll `get-harness` cho đến khi `"status": "READY"`. Ghi lại giá trị `arn` trong phản hồi.

```bash
aws bedrock-agentcore-control get-harness \
  --harness-id "MyHarness-XyZ123"
```

Gọi từ Python. Nếu bạn không chỉ định model, harness sẽ mặc định dùng Anthropic Claude Sonnet 4.6 trên Amazon Bedrock:

```python
import boto3

client = boto3.client("bedrock-agentcore", region_name="us-west-2")

response = client.invoke_harness(
    harnessArn="arn:aws:bedrock-agentcore:us-west-2:123456789012:harness/MyHarness-XyZ123",  # Replace with your harness ARN
    runtimeSessionId="1234abcd-12ab-34cd-56ef-1234567890ab",
    messages=[{
        "role": "user",
        "content": [{"text": "Research three tropical vacation options under $3k."}]
    }],
)

for event in response["stream"]:
    if "contentBlockDelta" in event:
        delta = event["contentBlockDelta"].get("delta", {})
        if "text" in delta:
            print(delta["text"], end="", flush=True)
    elif "runtimeClientError" in event:
        print(f"\nError: {event['runtimeClientError']['message']}")
```

Cài đặt AgentCore CLI:

```bash
npm install -g @aws/agentcore
```

Tạo một dự án harness ở chế độ không tương tác bằng các cờ:

```bash
agentcore create --name myresearchagent --model-provider bedrock
```

Deploy và gọi:

```bash
agentcore deploy
agentcore invoke --harness myresearchagent \
  --session-id "$(uuidgen)" \
  "Research three tropical vacation options under $3k, within five hours of NYC."
```

Phản hồi được stream về terminal của bạn. Dùng lại cùng một `--session-id` giữa các lần gọi để tiếp tục cuộc trò chuyện trong cùng một môi trường.

Để thêm nhiều harness vào một dự án hiện có, dùng `agentcore add harness`. Để sinh một script invoke Python độc lập, thêm `--with-invoke-script`.

Các cờ hữu ích:

- `--no-browser` (`-b`) - dùng terminal TUI thay cho trình kiểm tra (inspector) trên trình duyệt

- `--logs` (`-l`) - chạy ở chế độ không tương tác với log ra stdout

- `--port ` (`-p`) - đặt cổng dev server (mặc định 8080)

- `--no-traces` - tắt việc thu thập OTEL trace cục bộ

Cài đặt AgentCore CLI:

```bash
npm install -g @aws/agentcore
```

Chạy `agentcore create` không kèm cờ để khởi động wizard tương tác:

```bash
agentcore create
```

- Nhập tên dự án của bạn:

- Chọn **Harness** làm loại dự án:

- Chọn model provider của bạn:

- Chọn môi trường của bạn (default, container URI, hoặc Dockerfile):

- Cấu hình Memory (bộ nhớ):

- (Tùy chọn) Cấu hình các thiết lập nâng cao (tools, auth, network, lifecycle, limits, truncation, session storage):

- Xem lại cấu hình và xác nhận:

Sau khi xác nhận, wizard sẽ scaffold dự án của bạn. Deploy bằng `agentcore deploy`, rồi gọi bằng `agentcore invoke`.

Kiểm tra trạng thái dự án bất cứ lúc nào với `agentcore status`:

- Phát triển cục bộ

Nếu muốn kiểm thử harness trong môi trường cục bộ, bạn có thể chạy dev server:

```bash
agentcore dev
```

Khi bạn chạy `agentcore dev`, CLI trước tiên deploy các tài nguyên harness lên AWS, tạo IAM role, harness, và bất kỳ memory hay credential nào đã cấu hình trong dự án của bạn:

Sau khi deploy hoàn tất, nó khởi động một server cục bộ và mở agent inspector trong trình duyệt của bạn, nơi bạn có thể trò chuyện với harness, kiểm tra các trace, và duyệt các tài nguyên của dự án:

Mở rộng **Harness Settings** để xem và ghi đè cấu hình harness cho phiên hiện tại:

Đó là tất cả những gì bạn cần để chạy một harness. Các phần sau sẽ trình bày mọi thứ bạn có thể cấu hình.

###### Lưu ý

Giá trị `runtimeSessionId` phải dài ít nhất 33 ký tự. Dùng một UUID hoặc định danh tương tự. Dùng lại cùng một session ID giữa các lần gọi để tiếp tục cuộc trò chuyện trong cùng một môi trường.

## Tài liệu API

Để biết thêm chi tiết, xem API Reference:

- [CreateHarness API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateHarness.html)

- [GetHarness API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_GetHarness.html)

- [UpdateHarness API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_UpdateHarness.html)

- [DeleteHarness API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_DeleteHarness.html)

- [ListHarnesses API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_ListHarnesses.html)

- [ListHarnessVersions API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_ListHarnessVersions.html)

- [InvokeHarness API](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_InvokeHarness.html)

- [InvokeAgentRuntimeCommand API](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_InvokeAgentRuntimeCommand.html)

- [CreateHarnessEndpoint API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateHarnessEndpoint.html)

- [GetHarnessEndpoint API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_GetHarnessEndpoint.html)

- [UpdateHarnessEndpoint API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_UpdateHarnessEndpoint.html)

- [DeleteHarnessEndpoint API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_DeleteHarnessEndpoint.html)

- [ListHarnessesEndpoints API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_ListHarnessesEndpoint.html)

## Định dạng phản hồi streaming

`InvokeHarness` trả về một luồng (stream) các sự kiện. Các loại sự kiện chính là:

- `messageStart` - bắt đầu một message mới (bao gồm `role`)

- `contentBlockStart` - bắt đầu một content block (text, `toolUse`, hoặc `toolResult`)

- `contentBlockDelta` - nội dung tăng dần (`text`, input của `toolUse`, nội dung `toolResult`, `reasoningContent`)

- `contentBlockStop` - kết thúc một content block

- `messageStop` - kết thúc message (bao gồm `stopReason`)

- `metadata` - các chỉ số về token usage và latency

- `hookEvent` - một lifecycle hook đã cấu hình được kích hoạt. Các sự kiện Lambda hook bao gồm decision đã áp dụng và lý do tùy chọn. Xem [Lifecycle hooks](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-lifecycle-hooks.html).

- `runtimeClientError` - lỗi trong quá trình thực thi

Giá trị `stopReason` trong `messageStop` cho biết vì sao message được stream hiện tại đã kết thúc:

- `end_turn` - agent (tác tử AI) đã hoàn tất bình thường

- `tool_use` - model yêu cầu một hoặc nhiều tool. Harness có thể tiếp tục với các tool do harness thực thi. Nếu đây là `messageStop` cuối cùng trong luồng phản hồi đã hoàn tất, harness đang chờ một kết quả hàm inline.

- `tool_result` - harness đã stream một hoặc nhiều kết quả tool; có thể có thêm output từ model tiếp theo

- `max_tokens` - đã đạt giới hạn token mỗi lượt của model

- `max_iterations_exceeded` - đã chạm giới hạn `maxIterations`

- `timeout_exceeded` - đã chạm giới hạn `timeoutSeconds`

- `max_output_tokens_exceeded` - đã cạn ngân sách `maxTokens`

- `hook_stopped` - một decision `deny` từ Lambda hook `before_invocation` hoặc `after_tool_call` đã dừng lần gọi
