# Multi-tenancy và tối ưu tài nguyên

Một dịch vụ tác nhân multitenant được thiết kế tốt cho các tổ chức phục vụ nhiều nhóm và khách hàng từ hạ tầng dùng chung trong khi mang lại hiệu năng nhất quán, có thể dự đoán cho từng bên. Các triển khai tác nhân multitenant phải cô lập khối công việc của một tenant sao cho nó không thể làm suy giảm hiệu năng mà các tenant khác trải nghiệm, và đồng thời tối ưu mức dùng tài nguyên tổng thể để kiểm soát chi phí. Điều này đòi hỏi thiết kế các mô hình triển khai cung cấp các ranh giới cô lập phù hợp, triển khai các cơ chế throttling và hạn ngạch (quota) cưỡng chế phân bổ tài nguyên công bằng, và định-cỡ-đúng các cấu hình compute serverless cho bản chất bùng-nổ (bursty) của các khối công việc tác nhân.

| AGENTPERF07: Bạn quản lý cô lập hiệu năng multitenant và tối ưu mức dùng tài nguyên như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các triển khai tenant được tổ chức thành các tầng với các hồ sơ hiệu năng, cô lập, và chi phí tường minh, thay vì một hình dạng duy nhất áp đồng đều cho mọi tenant.
- Các tầng gộp (pooled) chia sẻ hạ tầng được quản lý cung cấp cô lập cấp-phiên, và các tầng premium hoặc doanh nghiệp thêm các tài nguyên chuyên dụng nơi cần cô lập mạnh hơn.
- Throttling được cưỡng chế ở mọi lớp tài nguyên dùng chung (API, suy luận, bộ nhớ, Tools), để các tenant không thể bỏ qua các giới hạn ở biên qua các thao tác hạ nguồn chạy-dài.
- Throttling thích ứng cho các tenant dùng dung lượng dư trong các thời kỳ tải-thấp và snap về đường cơ sở trong lúc tranh chấp, đồng thời tôn trọng ưu tiên tầng.
- Ngữ cảnh tenant lan truyền qua toàn ngăn xếp, và các bảng điều khiển theo-tenant theo dõi latency, tỷ lệ lỗi, trạng thái throttle, và tiêu tài nguyên đối chiếu SLA của tầng.
- Cô lập được xác nhận qua kiểm thử hàng-xóm-ồn-ào (noisy-neighbor) thường xuyên, để các tuyên bố hiệu năng của mô hình triển khai được đo lường thay vì giả định.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với multi-tenancy và tối ưu tài nguyên.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các tenant được phục vụ từ một triển khai dùng chung duy nhất không có cơ chế cô lập hoặc từ hạ tầng siloed trùng lặp không có chính sách tầng. Throttling, nếu có, chỉ ở biên API và dùng các giới hạn tĩnh. Không có telemetry theo-tenant, nên các hiệu ứng hàng-xóm-ồn-ào và vi phạm SLA được phát hiện sau khi khách hàng báo cáo. Onboarding tenant đòi hỏi cấp phát hạ tầng thủ công cho mỗi khách hàng mới. |
| 2 | Manh nha (Emerging) | Một số nhỏ các tầng (standard và premium, tùy chọn enterprise) được ghi tài liệu với SLA hiệu năng, yêu cầu cô lập, và giá. Tầng standard chạy trên hạ tầng gộp như [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với cô lập cấp-phiên. [Các usage plan của Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) cưỡng chế các giới hạn tốc độ theo-tenant ở biên. Dữ liệu được cô lập theo tầng dùng các partition key [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) cho các tầng gộp. |
| 3 | Đã định nghĩa (Defined) | Throttling được cưỡng chế ở mọi lớp dùng chung, không chỉ ở biên. Xếp hàng nhận-biết-tenant giới hạn đồng thời theo-tenant trên các lệnh gọi [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html), và các lớp bộ nhớ cùng Tools cưỡng chế các giới hạn theo-tenant riêng của chúng. Các tenant premium dùng các tài nguyên chuyên dụng như [provisioned throughput của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html). Ngữ cảnh tenant lan truyền qua các lớp runtime, bộ nhớ, và Tools. Các bảng điều khiển theo-tenant trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) theo dõi tiêu thụ và tuân thủ SLA. |
| 4 | Chủ động (Proactive) | Throttling thích ứng nới các giới hạn trong các thời kỳ tải-thấp và siết trong lúc tranh chấp, tôn trọng ưu tiên tầng để các tenant premium giữ dung lượng. Onboarding cho các tenant tầng-standard là cấu-hình-điều-khiển qua các mẫu [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) hoặc [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) thay vì một bản dựng hạ tầng riêng chế. Cảnh báo kích hoạt trên độ-gần-giới-hạn theo-tenant và vi phạm SLA, và kiểm thử hàng-xóm-ồn-ào chạy theo nhịp thường xuyên để xác nhận các tuyên bố cô lập đối chiếu tải thực. |
| 5 | Tối ưu (Optimized) | Định nghĩa tầng, chính sách throttling, và mô hình triển khai được tinh chỉnh liên tục đối chiếu dữ liệu vận hành. Onboarding hoàn toàn tự-phục-vụ cho các tầng standard và premium với các guardrail giúp ngăn các cấu hình không-phù-hợp-tầng. Chi phí và hiệu năng theo-tenant được báo cáo tới các bảng điều khiển hướng-tenant, và hiệu quả cô lập được xác nhận qua các kịch bản chaos và hàng-xóm-ồn-ào tự động. Tổ chức công bố các mẫu tham chiếu multitenant tái dùng nội bộ và đóng góp các benchmark qua các nhóm. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm triển khai hạ tầng cô lập hoàn toàn cho mọi tenant bất kể nhu cầu, lãng phí dung lượng cho các tenant mà yêu cầu của họ sẽ được đáp ứng bởi các tài nguyên gộp.
- Các nhóm dùng một triển khai gộp duy nhất không có cô lập theo-lớp, để các tenant lượng-lớn tiêu dung lượng không cân xứng và làm suy giảm hiệu năng cho mọi bên khác.
- Throttling chỉ được cưỡng chế ở biên API, nên các tenant bỏ qua các giới hạn ở biên qua các thao tác suy luận, bộ nhớ, hoặc Tools chạy-dài làm bão hòa các tài nguyên dùng chung hạ nguồn.
- Throttling dùng các giới hạn tĩnh vốn không dùng dung lượng dư trong các thời kỳ tải-thấp cũng không bảo vệ cô lập trong các thời kỳ tải-cao, và các tenant premium bị throttle giống hệt các tenant standard.
- Onboarding tenant đòi hỏi cấp phát hạ tầng trên mỗi khách hàng mới, nên thời gian onboarding và chi phí vận hành tăng tuyến tính theo số tenant.
- Cô lập được giả định thay vì kiểm thử, nên các thay đổi tinh vi (một Tool mới, một prompt nặng hơn, một dịch chuyển trong hỗn hợp lưu lượng) bào mòn ranh giới cô lập một cách âm thầm và chỉ hiện lên trong một sự cố thực.

###### Các thực hành tốt

- [AGENTPERF07-BP01 Thiết kế các mô hình triển khai tác nhân multitenant hiệu quả](agentperf07-bp01.md)
- [AGENTPERF07-BP02 Triển khai cô lập hiệu năng và throttling nhận-biết-tenant](agentperf07-bp02.md)
