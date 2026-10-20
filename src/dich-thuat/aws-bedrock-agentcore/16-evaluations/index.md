---
title: "AgentCore Evaluations: Đánh giá hiệu năng agent"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html"
---

# AgentCore Evaluations: Đánh giá hiệu năng agent

# Đánh giá hiệu năng agent với Amazon Bedrock AgentCore Evaluations

Amazon Bedrock AgentCore Evaluations cung cấp các công cụ đánh giá tự động để đo lường mức độ hiệu quả của agent (tác tử AI) hoặc tool (công cụ) của bạn khi thực hiện các tác vụ cụ thể, xử lý các trường hợp biên và duy trì tính nhất quán qua các đầu vào và bối cảnh khác nhau. Dịch vụ này cho phép tối ưu hóa dựa trên dữ liệu và đảm bảo agent của bạn đáp ứng các tiêu chuẩn chất lượng trước và sau khi triển khai.

AgentCore Evaluations tích hợp với các agent framework phổ biến bao gồm **Strands** và **LangGraph** với các thư viện instrumentation **OpenTelemetry** và **OpenInference**. Bên dưới, các trace từ những agent này được chuyển đổi sang một định dạng thống nhất và được chấm điểm bằng kỹ thuật LLM-as-a-Judge cho cả evaluator tích hợp sẵn và evaluator tùy chỉnh.

Mỗi evaluator có một Amazon Resource Name (ARN) duy nhất và một resource policy gắn kèm. ARN của evaluator theo các định dạng sau:

```nohighlight
arn:aws:bedrock-agentcore:::evaluator/Builtin.Helpfulness (for built-in evaluators)
```

```nohighlight
arn:aws:bedrock-agentcore:region:account:evaluator/my-evaluator-id (for custom evaluators)
```

Các evaluator tích hợp sẵn là công khai và mọi người dùng đều có thể truy cập. Các tài nguyên đánh giá tùy chỉnh là riêng tư và chỉ có thể được truy cập bởi những người dùng được cấp quyền một cách rõ ràng. Để cấp quyền, bạn có thể dùng IAM resource-based policy cho evaluator và evaluation configuration, và IAM identity-based policy cho user và role.

Theo mặc định, bạn có thể tạo tối đa 1.000 evaluation configuration cho mỗi AWS Region trong một tài khoản AWS. Dịch vụ hỗ trợ tối đa 1 triệu token đầu vào và đầu ra mỗi phút cho mỗi tài khoản đối với các region lớn.

###### Topics

- [How it works](/dich-thuat/aws-bedrock-agentcore/16-evaluations/how-it-works-evaluations)

- [Telemetry setup and delivery](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks-telemetry.html)

- [Supported agent frameworks](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks.html)

- [Built-in evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-evaluators-overview.html)

- [Third-party evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/third-party-evaluators.html)

- [Custom evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/custom-evaluators.html)

- [Online evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/online-evaluations.html)

- [On-demand evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/on-demand-evaluations.html)

- [Batch evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/batch-evaluations.html)

- [Dataset evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/dataset-evaluations.html)

- [Simulation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/simulation.html)

- [Diagnose AgentCore Evaluation issues with an AI coding assistant](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/diagnose-evaluation-issues.html)

- [Encryption at rest for AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-encryption.html)
