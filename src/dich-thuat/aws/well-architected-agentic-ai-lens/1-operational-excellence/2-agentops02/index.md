# Quản lý vòng đời Prompt và cấu hình

Prompt, cấu hình, và quyền của Tools của agent định nghĩa hành vi agent và tiến hóa liên tục khi nhu cầu kinh doanh thay đổi. Quản lý các tài liệu này đòi hỏi cân bằng giữa lặp lại nhanh và sự ổn định, để các thay đổi được theo dõi, kiểm thử, và có thể đảo ngược.

| AGENTOPS02: Bạn quản lý vòng đời Prompt và cấu hình như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Prompt, cấu hình hành vi, và quyền của Tools của agent được quản lý như các tài liệu vận hành hạng nhất với lịch sử phiên bản đầy đủ, quyền sở hữu được tài liệu hóa, và một vòng đời được xác định từ soạn thảo đến ngừng sử dụng.
- Các thay đổi hành vi chỉ đến được sản xuất sau khi vượt qua đánh giá tự động so với các ngưỡng chất lượng đã tài liệu hóa, và chúng đi qua triển khai theo giai đoạn thay vì triển khai toàn bộ lưu lượng.
- Các cấu hình giữ nhất quán qua các môi trường phát triển, staging, và sản xuất, và sự trôi lệch khỏi các baseline được phê duyệt được phát hiện và khắc phục tự động.
- Việc quay lui (rollback) về một baseline hành vi tốt đã biết được tự động hóa, kiểm thử thường xuyên, và hoàn tất trong vòng vài phút kể từ khi quyết định hoàn nguyên.
- Các tín hiệu vận hành, phản hồi người dùng, và chỉ số kết quả kinh doanh chảy vào một backlog cải tiến có cấu trúc, khép lại vòng lặp từ quan sát tới thay đổi đã được kiểm định.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với quản lý vòng đời Prompt và cấu hình như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Prompt và cấu hình hành vi được nhúng trong mã ứng dụng hoặc bảo trì thủ công trong từng môi trường. Các thay đổi được triển khai trực tiếp vào sản xuất mà không có đánh giá, và không có lịch sử phiên bản để quay lui khi một thay đổi gây hồi quy. Khác biệt cấu hình giữa phát triển, staging, và sản xuất là phổ biến và chỉ được nhận ra sau các sự cố. |
| 2 | Manh nha (Emerging) | Prompt và cấu hình hành vi được lưu ngoài mã ứng dụng trong một kho có phiên bản như [Amazon Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html). Các baseline hạ tầng được định nghĩa trong [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) hoặc [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html), và các thay đổi tuân theo một vòng đời được tài liệu hóa với rà soát ngang hàng (peer review). Quay lui khả thi nhưng thủ công. |
| 3 | Được định nghĩa (Defined) | Một vòng đời Prompt đầy đủ (Draft, Review, Active, Archived) được áp đặt qua các cổng phê duyệt [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/approvals-action-add.html), với đánh giá tự động sử dụng [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html) như một cổng thăng hạng. [Phát hiện trôi lệch AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) và [các quy tắc AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html) giám sát trôi lệch cấu hình, và [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html) ghi nhận quy kết thay đổi. Các runbook quay lui được định nghĩa và kiểm thử. |
| 4 | Chủ động (Proactive) | Các thay đổi hành vi được triển khai theo giai đoạn bằng định tuyến có trọng số của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html), với các cổng thăng hạng tự động được điều khiển bởi các chỉ số chất lượng [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html). Kiểm thử A/B so sánh các biến thể hành vi dưới lưu lượng, và [khắc phục tự động](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html) khôi phục các cấu hình được phê duyệt khi phát hiện trôi lệch. Một đường ống phản hồi đa kênh xây dựng trên [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) cấp dữ liệu cho backlog cải tiến. |
| 5 | Tối ưu (Optimized) | Toàn bộ vòng đời là tự phục vụ (self-service) cho các nhóm, với quay lui tự động khôi phục baseline hành vi trong vòng vài phút kể từ khi một ngưỡng chất lượng bị vượt qua. Tính nhất quán liên môi trường được kiểm định liên tục, và [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) tương quan các mốc thời gian triển khai với các xu hướng chất lượng để mọi thay đổi chỉ số đều có thể quy về một phiên bản hành vi cụ thể. Các luồng công việc từ phản hồi tới cải tiến khép lại vòng lặp từ tín hiệu tới thay đổi đã được kiểm định, và tổ chức đóng góp các mẫu của mình trở lại cộng đồng agentic AI rộng lớn hơn. |

## Các vấn đề thường gặp cần lưu ý

- Prompt được nhúng trực tiếp vào mã ứng dụng, khiến bất kỳ thay đổi hành vi nào cũng buộc phải triển khai lại toàn bộ mã và làm cho việc lặp lại hành vi agent một cách độc lập là bất khả thi.
- Các thay đổi cấu hình được áp dụng thông qua chỉnh sửa thủ công trên console trong từng môi trường riêng lẻ, khiến phát triển, staging, và sản xuất trôi lệch khỏi nhau và tạo ra các lỗi kiểu "nó chạy được trong test" khi lên sản xuất.
- Các thay đổi hành vi được đưa thẳng tới 100% lưu lượng mà không có triển khai theo giai đoạn hay đánh giá trước triển khai, khuếch đại tối đa phạm vi tác động của bất kỳ hồi quy nào và không để lại đường an toàn nào để bắt vấn đề sớm.
- Quay lui được xem như một hoạt động thủ công, khám phá thay vì một quy trình đã được kiểm thử, tự động hóa, nên việc phục hồi mất hàng giờ thay vì vài phút khi một thay đổi hành vi gặp trục trặc.
- Phản hồi người dùng, chỉ số chất lượng, và các tín hiệu kết quả kinh doanh được thu thập nhưng không bao giờ được kết nối với các phiên bản Prompt hoặc cấu hình cụ thể, khiến các nhóm không thể quy các thay đổi chất lượng về những thay đổi hành vi đã gây ra chúng.

###### Các thực hành tốt

- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](agentops02-bp01.md)
- [AGENTOPS02-BP02 Triển khai phát hiện và khắc phục trôi lệch cấu hình](agentops02-bp02.md)
- [AGENTOPS02-BP03 Triển khai năng lực đánh phiên bản và quay lui hành vi agent](agentops02-bp03.md)
- [AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục](agentops02-bp04.md)
