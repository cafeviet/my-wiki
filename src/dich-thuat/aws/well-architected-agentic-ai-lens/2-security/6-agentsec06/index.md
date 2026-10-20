# Điều phối đa agent an toàn

Các hệ thống đa agent đưa vào các thách thức phối hợp không tồn tại trong các kiến trúc đơn agent. Agent cần khám phá các đồng đẳng (peers), chia sẻ năng lực, ủy thác tác vụ và trao đổi ngữ cảnh qua các ranh giới tin cậy. Nếu không có việc kiểm chứng danh tính và bảo mật giao tiếp đúng cách, việc mạo danh agent và can thiệp thông điệp có thể ảnh hưởng đến toàn bộ các luồng công việc đa agent. Các giao thức được chuẩn hóa như Agent-to-Agent (A2A) và Model Context Protocol (MCP) cung cấp khả năng tương tác qua các framework, nhưng các tổ chức phải xếp thêm các kiểm soát bảo mật lên trên các giao thức này để duy trì các ranh giới tin cậy.

| AGENTSEC06: Bạn bảo vệ việc điều phối và phối hợp đa agent như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Agent được phân đoạn thành các vùng tin cậy (trust zones) dựa trên vai trò, năng lực và hồ sơ rủi ro, và giao tiếp giữa các vùng chỉ chảy theo các đường có tài liệu được thực thi ở cả lớp mạng lẫn lớp ứng dụng.
- Các thông điệp giữa các agent vượt qua ranh giới tin cậy hoặc đi qua các dịch vụ trung gian được ký và mã hóa ở cấp thông điệp, để tính toàn vẹn của payload tồn tại vượt ra ngoài tầng vận chuyển (transport).
- Các lớp điều phối thực thi kiểm định lược đồ, các quyền hạn IAM giới hạn phạm vi và các cầu dao ngắt (circuit breakers), nên một thất bại ở một agent không thể lan tràn qua luồng công việc hoặc chuyển hướng nó sang các đường thực thi bất ngờ.
- Các mẫu phối hợp được giám sát liên tục so với các đường cơ sở đã thiết lập, nên các sai lệch được phát hiện chủ động thay vì được phát hiện về sau.
- Mọi bước phối hợp đều có thể quy kết cho một danh tính agent đã được kiểm chứng và được ghi lại để điều tra. Điều này bao gồm việc khám phá agent card (cơ chế của [giao thức A2A](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/) qua đó một agent định vị một đồng đẳng và đọc một agent card JSON mô tả tên, năng lực, các kỹ năng được hỗ trợ và các yêu cầu xác thực của nó), việc ủy thác tác vụ và việc thu thập kết quả.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc điều phối đa agent an toàn như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Agent chạy trong một mạng phẳng không có phân đoạn. Các thông điệp giữa các agent chỉ dựa vào mã hóa ở cấp vận chuyển, không có ký thông điệp hay kiểm chứng danh tính ở phía nhận. Điều phối không có cấu trúc, với các quyền hạn IAM rộng trên các API luồng công việc và không có cầu dao ngắt, và các mẫu phối hợp không được giám sát. |
| 2 | Manh nha (Emerging) | Phân đoạn mạng cơ bản nhóm các agent theo tầng tin cậy, thường qua các [security group](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) hoặc [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) riêng. [Mã hóa phía máy chủ của Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html) giúp bảo vệ các thông điệp trong hàng đợi bằng các khóa [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html). [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) điều phối các luồng công việc với ghi log thực thi được bật, mặc dù các quyền hạn IAM vẫn rộng và các cầu dao ngắt hiện chưa có. |
| 3 | Được định nghĩa (Defined) | Ký ở cấp thông điệp qua [các khóa bất đối xứng AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-concepts.html#asymmetric-cmks) bao phủ các thông điệp vượt qua các ranh giới tin cậy hoặc đi qua các hàng đợi và bus sự kiện, với các khóa riêng cho từng vùng tin cậy. Các state machine của Step Functions được quản lý như mã qua [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html) hoặc [AWS Cloud Development Kit (AWS CDK)](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions-readme.html), [kiểm định đầu vào](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-input-output-processing.html) và [các cầu dao ngắt](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html#error-handling-retrying-after-an-error) đã có, và [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) giữ lưu lượng xuyên vùng trên các đường riêng tư. |
| 4 | Chủ động (Proactive) | [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) với hỗ trợ [giao thức A2A](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/) cấu trúc việc khám phá giữa các agent và việc ủy thác tác vụ, và các [chính sách Cedar](https://docs.cedarpolicy.com/) trong [AgentCore Policy](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) thực thi các ranh giới tin cậy ở lớp công cụ. Các chỉ số phối hợp được thu dưới dạng [các chỉ số tùy chỉnh Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) với các đường cơ sở, và [phát hiện bất thường CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) gắn cờ các sai lệch. Các phát hiện của [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) được tương quan với các log phối hợp trong [AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-what-is.html). |
| 5 | Tối ưu (Optimized) | Các cấu hình ranh giới tin cậy được kiểm chứng liên tục qua các quy tắc [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) quản lý và [tùy chỉnh](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_lambda-functions.html), với các cảnh báo về bất kỳ cấu hình nào tạo ra kết nối xuyên vùng trái phép. [AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đưa các điểm độ chính xác lựa chọn công cụ và độ đúng đắn vào giám sát phối hợp như một lớp cảnh báo sớm. Các runbook ứng phó sự cố cho các bất thường phối hợp được thực hành định kỳ, và các mẫu đã kiểm chứng được gấp trở lại vào kiến trúc tham chiếu của tổ chức. |

## Các vấn đề thường gặp cần lưu ý

- Các hệ thống đa agent được triển khai như một vùng tin cậy duy nhất, nên một vấn đề với bất kỳ một agent nào có thể lan ngang qua toàn bộ mạng trước khi phạm vi được hiểu.
- Các nhóm dựa vào mã hóa ở cấp vận chuyển cho lưu lượng giữa các agent và coi việc ký ở cấp thông điệp là không cần thiết, nghĩa là các thông điệp nằm trong hàng đợi hoặc bus sự kiện không thể được kiểm chứng tại thời điểm tiêu thụ.
- Các quyền hạn IAM của bộ điều phối (orchestrator) ủy quyền cho bất kỳ principal nào bắt đầu, dừng hoặc chỉnh sửa bất kỳ luồng công việc nào trong tài khoản, thay vì giới hạn phạm vi truy cập tới các state machine cụ thể mà mỗi principal cần.
- Giám sát bao phủ các chỉ số hạ tầng và tình trạng agent riêng lẻ nhưng bỏ qua các chỉ số phối hợp, nên các đợt tăng đột biến tốc độ thông điệp giữa các agent, các đường giao tiếp bất ngờ và các thay đổi topo (topology) không được phát hiện.
- Các phát hiện của [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) và các log phối hợp được coi như các luồng dữ liệu riêng biệt, để các điều tra viên không có ngữ cảnh để buộc một bất thường API với luồng công việc đa agent cụ thể mà nó ảnh hưởng.

###### Các thực hành tốt

- [AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent](agentsec06-bp01.md)
- [AGENTSEC06-BP02 Triển khai các kiểm soát bảo mật điều phối luồng công việc](agentsec06-bp02.md)
- [AGENTSEC06-BP03 Thiết lập các ranh giới tin cậy giữa các agent](agentsec06-bp03.md)
- [AGENTSEC06-BP04 Giám sát và phát hiện các bất thường trong phối hợp](agentsec06-bp04.md)
