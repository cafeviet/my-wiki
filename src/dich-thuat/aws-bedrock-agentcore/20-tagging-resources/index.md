---
title: "Gắn thẻ tài nguyên"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/tagging-resources.html"
---

# Gắn thẻ tài nguyên

# Gắn thẻ (tag) cho tài nguyên AgentCore

*Tag* (thẻ) là một nhãn mà bạn gán cho một tài nguyên AWS. Mỗi tag gồm một *key* (khóa) và một *value* (giá trị) tùy chọn, cả hai đều do bạn định nghĩa.

Tag cho phép bạn phân loại tài nguyên AWS theo nhiều cách khác nhau, ví dụ theo mục đích, chủ sở hữu hoặc môi trường. Điều này hữu ích khi bạn có nhiều tài nguyên cùng loại — bạn có thể nhanh chóng xác định một tài nguyên cụ thể dựa trên các tag bạn đã gán.

## Tổng quan về gắn thẻ

Mỗi tag gồm một key và một value tùy chọn. Ví dụ, bạn có thể định nghĩa một bộ tag cho các tài nguyên AgentCore của tài khoản để giúp bạn theo dõi chủ sở hữu và cấp độ stack của từng tài nguyên.

Chúng tôi khuyến nghị bạn thiết kế một bộ tag key đáp ứng nhu cầu cho từng loại tài nguyên. Dùng một bộ tag key nhất quán giúp bạn quản lý tài nguyên dễ dàng hơn. Bạn có thể tìm kiếm và lọc tài nguyên dựa trên các tag bạn thêm vào.

Tag không có ý nghĩa ngữ nghĩa nào đối với AgentCore và được diễn giải nghiêm ngặt như một chuỗi ký tự. Ngoài ra, tag không được tự động gán cho tài nguyên của bạn. Bạn có thể chỉnh sửa tag key và value, và có thể gỡ tag khỏi tài nguyên bất cứ lúc nào. Bạn có thể đặt value của một tag thành chuỗi rỗng, nhưng không thể đặt value thành null. Nếu bạn thêm một tag có cùng key với một tag hiện có trên tài nguyên đó, value mới sẽ ghi đè value cũ. Nếu bạn xóa một tài nguyên, mọi tag của tài nguyên đó cũng bị xóa.

## Các tài nguyên hỗ trợ gắn thẻ

Các tài nguyên AgentCore sau đây hỗ trợ gắn thẻ:

- Agent runtime

- Agent runtime endpoint

- Capacity provider

- Code interpreter

- Browser

- Browser Profile

- Gateway

- Workload identity

- OAuth2 credential provider

- API key credential provider

- Workload identity directory

- Token vault

- AgentCore Memory

- Custom Evaluator

- Online Evaluation Config

- Policy Engine

- Configuration Bundle

- Batch Evaluation

- Recommendation

- AB Test

## Hạn chế đối với tag

Các hạn chế cơ bản sau đây áp dụng cho tag:

- Số lượng tag tối đa cho mỗi tài nguyên – 50

- Với mỗi tài nguyên, mỗi tag key phải là duy nhất, và mỗi tag key chỉ có thể có một value.

- Độ dài key tối đa – 128 ký tự Unicode trong UTF-8

- Độ dài value tối đa – 256 ký tự Unicode trong UTF-8

- Nếu lược đồ gắn thẻ của bạn được dùng trên nhiều dịch vụ và tài nguyên, hãy nhớ rằng các dịch vụ khác có thể có hạn chế về ký tự được phép. Các ký tự thường được phép là: chữ cái, chữ số và khoảng trắng biểu diễn được trong UTF-8, cùng các ký tự sau: + - = . _ : / @.

- Tag key không phân biệt hoa thường, trong khi tag value phân biệt hoa thường.

- Không dùng `aws:`, `AWS:`, hoặc bất kỳ tổ hợp hoa thường nào của tiền tố đó cho key hay value vì nó được dành riêng cho AWS. Bạn không thể chỉnh sửa hoặc xóa các tag key hay value có tiền tố này. Các tag có tiền tố này không tính vào giới hạn số tag trên mỗi tài nguyên của bạn.

## Làm việc với tag

Bạn có thể thêm, chỉnh sửa hoặc xóa tag cho các tài nguyên AgentCore bằng console, API hoặc CLI.

### Thêm tag

Bạn có thể thêm tag khi tạo các tài nguyên AgentCore sau: Agent runtime, Agent runtime endpoint, Code interpreter, Browser, Browser Profile, Gateway, Workload identity, OAuth2 credential provider, API key credential provider, Custom Evaluator, Online Evaluation Config, Policy Engine, Configuration Bundle, Batch Evaluation, Recommendation, AB Test.

**Để thêm tag khi tạo tài nguyên**

- Mở AgentCore console.

- Điều hướng đến loại tài nguyên bạn muốn tạo.

- Làm theo các bước để tạo tài nguyên. Khi đến phần **Tags**, chọn **Add tag**.

- Nhập tag key và tùy chọn nhập tag value.

- Để thêm nhiều tag hơn, chọn **Add tag** lần nữa.

- Hoàn tất quy trình tạo tài nguyên.

**Để thêm tag vào một tài nguyên hiện có**

- Mở AgentCore console.

- Điều hướng đến loại tài nguyên và chọn tài nguyên cụ thể.

- Chọn tab **Tags**.

- Chọn **Add tag**, rồi nhập key và tùy chọn nhập value.

- Chọn **Save changes**.

Bạn có thể thêm tag khi tạo tài nguyên hoặc vào các tài nguyên hiện có bằng AgentCore API.

**Thêm tag khi tạo tài nguyên**

Bạn có thể thêm tag khi tạo tài nguyên bằng các API operation sau:

- [CreateAgentRuntime](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateAgentRuntime.html) – Bao gồm tag trong tham số `tags`.

- [CreateAgentRuntimeEndpoint](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateAgentRuntimeEndpoint.html) – Bao gồm tag trong tham số `tags`.

- [CreateCapacityProvider](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateCapacityProvider.html) – Bao gồm tag trong tham số `tags`.

- [CreateCodeInterpreter](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateCodeInterpreter.html) – Bao gồm tag trong tham số `tags`.

- [CreateBrowser](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateBrowser.html) – Bao gồm tag trong tham số `tags`.

- [CreateBrowserProfile](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateBrowserProfile.html) – Bao gồm tag trong tham số `tags`.

- [CreateGateway](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateGateway.html) – Bao gồm tag trong tham số `tags`.

- [CreateWorkloadIdentity](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateWorkloadIdentity.html) – Bao gồm tag trong tham số `tags`.

- [CreateOAuth2CredentialProvider](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateOAuth2CredentialProvider.html) – Bao gồm tag trong tham số `tags`.

- [CreateAPIKeyCredentialProvider](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateAPIKeyCredentialProvider.html) – Bao gồm tag trong tham số `tags`.

- [CreateEvaluator](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateEvaluator.html) – Bao gồm tag trong tham số `tags`.

- [CreateOnlineEvaluationConfig](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateOnlineEvaluationConfig.html) – Bao gồm tag trong tham số `tags`.

- [CreatePolicyEngine](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreatePolicyEngine.html) – Bao gồm tag trong tham số `tags`.

- [CreatePaymentCredentialProvider](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreatePaymentCredentialProvider.html) - Bao gồm tag trong tham số `tags`.

- [CreatePaymentManager](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreatePaymentManager.html) - Bao gồm tag trong tham số `tags`.

- [CreateConfigurationBundle](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateConfigurationBundle.html) – Bao gồm tag trong tham số `tags`.

- [StartBatchEvaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_StartBatchEvaluation.html) – Bao gồm tag trong tham số `tags`.

- [StartRecommendation](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_StartRecommendation.html) – Bao gồm tag trong tham số `tags`.

- [CreateABTest](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_CreateABTest.html) – Bao gồm tag trong tham số `tags`.

**Thêm tag vào các tài nguyên hiện có**

Dùng operation [TagResource](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_TagResource.html) để thêm tag vào các tài nguyên hiện có.

Bạn có thể dùng CLI để thêm tag vào các tài nguyên AgentCore.

**Để thêm tag vào một tài nguyên**

Dùng lệnh `tag-resource`:

```bash
aws bedrock-agentcore tag-resource \
    --resource-arn arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/example-runtime \
    --tags Key=Environment,Value=Production Key=Team,Value=AI
```

### Quản lý tag

Bạn có thể chỉnh sửa tag value cho các tài nguyên hiện có trong console.

**Để chỉnh sửa tag cho một tài nguyên hiện có**

- Mở AgentCore console.

- Điều hướng đến loại tài nguyên và chọn tài nguyên cụ thể.

- Chọn tab **Tags**.

- Để chỉnh sửa một tag, sửa trực tiếp key hoặc value.

- Chọn **Save changes**.

Bạn có thể dùng AgentCore API để liệt kê và quản lý tag cho tài nguyên.

**Liệt kê tag**

Dùng operation [ListTagsForResource](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_ListTagsForResource.html) để liệt kê các tag của một tài nguyên.

**Cập nhật tag**

Dùng operation [TagResource](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_TagResource.html) để cập nhật tag hiện có bằng cách thêm value mới cho các key hiện có.

Bạn có thể dùng CLI để liệt kê và quản lý tag cho các tài nguyên AgentCore.

**Để liệt kê tag của một tài nguyên**

Dùng lệnh `list-tags-for-resource`:

```bash
aws bedrock-agentcore list-tags-for-resource \
    --resource-arn arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/example-runtime
```

**Để cập nhật tag cho một tài nguyên**

Dùng lệnh `tag-resource` để cập nhật tag hiện có:

```bash
aws bedrock-agentcore tag-resource \
    --resource-arn arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/example-runtime \
    --tags Key=Environment,Value=Staging
```

### Xóa tag

Bạn có thể gỡ tag khỏi tài nguyên trong console.

**Để xóa tag khỏi một tài nguyên**

- Mở AgentCore console.

- Điều hướng đến loại tài nguyên và chọn tài nguyên cụ thể.

- Chọn tab **Tags**.

- Để xóa một tag, chọn **Remove** bên cạnh tag đó.

- Chọn **Save changes**.

Bạn có thể dùng AgentCore API để gỡ tag khỏi tài nguyên.

**Gỡ tag**

Dùng operation [UntagResource](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_UntagResource.html) để gỡ tag khỏi một tài nguyên.

Bạn có thể dùng CLI để gỡ tag khỏi các tài nguyên AgentCore.

**Để gỡ tag khỏi một tài nguyên**

Dùng lệnh `untag-resource`:

```bash
aws bedrock-agentcore untag-resource \
    --resource-arn arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/example-runtime \
    --tag-keys Environment Team
```
