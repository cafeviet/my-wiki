# Suy giảm nhẹ nhàng và quản lý cấu hình

Các tác nhân phát hiện sự suy giảm một cách chính xác thông qua telemetry kỹ lưỡng và duy trì cấu hình nhất quán trên mọi thể hiện sẽ đưa ra các quyết định có căn cứ về khi nào kích hoạt **suy giảm nhẹ nhàng (graceful degradation)**. Quản lý cấu hình nhất quán giúp các tác nhân có thông tin đáng tin cậy, cập nhật về các năng lực và hạn chế trên toàn môi trường tác nhân.

| AGENTREL08: Làm thế nào để các tác nhân xác định khi nào và ở đâu suy giảm nhẹ nhàng là phù hợp? |
| --- |
|  |

## Mục tiêu năng lực

- Cấu hình của tác nhân nằm trong một nguồn tập trung, có phiên bản, được kiểm định lược đồ (schema-validated), nhờ đó mọi thể hiện chạy cùng các thiết lập hiện thời và độ trôi được phát hiện tự động.
- Các thay đổi cấu hình triển khai từ từ với hoàn tác tự động, và các giá trị nhạy cảm được giữ trong kho tham số được mã hóa với kiểm soát truy cập chi tiết.
- Telemetry ở cấp giai đoạn bao phủ mọi pha của quá trình xử lý tác nhân (truy xuất ngữ cảnh, suy luận, thực thi công cụ, sinh phản hồi), nhờ đó các quyết định suy giảm có căn cứ thay vì phản ứng.
- Phát hiện bất thường và các cảnh báo tổng hợp kết hợp các tín hiệu qua các giai đoạn thành một trạng thái sức khỏe hữu ích duy nhất, kích hoạt suy giảm nhẹ nhàng tự động.
- Cô lập tài nguyên tách các tác nhân đối mặt người dùng ưu tiên cao khỏi các khối lượng công việc nền, và sự tranh chấp được phát hiện qua các điểm số tổng hợp trước khi nó gây ra lỗi.
- Việc sử dụng bộ nhớ được theo dõi theo từng tầng (trong ngữ cảnh, phiên ngắn hạn, bền vững dài hạn) với các phản hồi tự động cho tóm tắt, tỉa (pruning) và hợp nhất trước khi sự cạn kiệt tạo ra các lỗi âm thầm.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với suy giảm nhẹ nhàng và quản lý cấu hình như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Cấu hình được gán cứng trong mã của tác nhân, nên mọi thay đổi tham số đòi hỏi triển khai lại. Telemetry chỉ tồn tại ở ranh giới yêu cầu, che giấu sự suy giảm ở cấp giai đoạn. Các tác nhân dùng chung một bể tài nguyên duy nhất, nên bất kỳ đợt tăng đột biến khối lượng công việc nào cũng làm suy giảm mọi tenant. Việc sử dụng bộ nhớ chỉ được giám sát ở cấp hạ tầng, và sự cạn kiệt trong ngữ cảnh tạo ra các lỗi âm thầm. Suy giảm nhẹ nhàng được kích hoạt thủ công, nếu có. |
| 2 | Manh nha (Emerging) | Cấu hình được tập trung nhưng quản lý thủ công, với đánh phiên bản một lần và kiểm định lược đồ hạn chế. Các số liệu [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) cơ bản bắt độ trễ suy luận và tỷ lệ lỗi, nhưng telemetry ở cấp giai đoạn còn một phần. Cô lập tài nguyên là phi chính thức, với các khối lượng công việc nặng đôi khi được đặt trên hạ tầng riêng. Sự tăng trưởng bộ nhớ được theo dõi cho một vài thành phần rò rỉ đã biết, và các phản hồi suy giảm được viết kịch bản nhưng do người vận hành kích hoạt. |
| 3 | Xác lập (Defined) | Cấu hình lúc chạy được quản lý qua một dịch vụ trung tâm như [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) với kiểm định JSON Schema và triển khai từ từ, và các bí mật (secret) nằm trong [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) hoặc các [tham số SecureString của Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-about.html). [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bắt telemetry ở cấp giai đoạn, và [ghi log gọi mô hình Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) ghi số lượng token và độ trễ theo từng lần gọi. Các tầng ưu tiên có các thể hiện [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) riêng biệt, và việc sử dụng bộ nhớ được theo dõi theo từng tầng với các cảnh báo tại 80% mức sử dụng cửa sổ ngữ cảnh. |
| 4 | Chủ động (Proactive) | [Phát hiện bất thường của CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) thiết lập các đường cơ sở tự động, và [các cảnh báo tổng hợp của CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm_How_To.html) kết hợp các tín hiệu đa giai đoạn thành suy giảm nhẹ nhàng tự động. Sự tranh chấp tài nguyên được phát hiện qua các điểm số tổng hợp kết hợp mức đồng thời, mức tiêu thụ token và độ sâu hàng đợi, và việc giảm thiểu được tự động hóa qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html). [Amazon Bedrock Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) cho các tác nhân nhạy độ trễ dung lượng dành riêng. Sự tăng trưởng bộ nhớ được phân tích qua [CloudWatch Metric Math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html), và các phản hồi tóm tắt, tỉa và hợp nhất được tự động hóa. Giám sát độ trôi cảnh báo trên các đội cấu hình chạy các phiên bản hỗn hợp. |
| 5 | Tối ưu (Optimized) | Các chính sách suy giảm và mẫu cấu hình được tinh chỉnh liên tục dựa trên dữ liệu vận hành. Các điểm số sức khỏe tổng hợp, các ngưỡng bất thường và các quy tắc giảm thiểu tự động được tinh chỉnh từ các kết quả quan sát được thay vì trực giác. Các phản hồi quản lý bộ nhớ tự chữa lành trên mọi tầng, và việc cấp phát tài nguyên điều chỉnh động dựa trên mức ưu tiên và nhu cầu quan sát được. Tổ chức công bố các mẫu telemetry và cấu hình dùng lại được trong nội bộ và chia sẻ các chuẩn đo về hiệu quả suy giảm nhẹ nhàng giữa các đội. |

## Các vấn đề thường gặp cần lưu ý

- Cấu hình được gán cứng hoặc tập trung một phần, nên các thay đổi tham số đòi hỏi triển khai lại và độ trôi cấu hình giữa các thể hiện chỉ được phát hiện qua các lỗi phía dưới.
- Các thay đổi cấu hình được áp dụng mà không kiểm định hay triển khai theo giai đoạn, để các giá trị cấu hình sai tới môi trường vận hành và làm suy giảm hành vi tác nhân tức thì.
- Telemetry chỉ được bắt ở ranh giới yêu cầu, nên một sự gia tăng độ trễ hoặc tỷ lệ lỗi tổng thể không cho tín hiệu nào về giai đoạn xử lý nào chịu trách nhiệm.
- Mọi tác nhân dùng chung một bể tài nguyên và hạn ngạch thượng nguồn duy nhất, nên một tác nhân nền khối lượng lớn làm suy giảm độ trễ của các tác nhân đối mặt người dùng và việc tiết lưu lan qua các khối lượng công việc.
- Giám sát bộ nhớ dừng ở các số liệu hạ tầng, nên sự cạn kiệt trong ngữ cảnh và các rò rỉ bộ nhớ dần dần tạo ra sự suy giảm đầu ra âm thầm không có chỉ báo dẫn dắt.
- Các ngưỡng cảnh báo tĩnh hoặc bắn quá thường xuyên trong các dịch chuyển lưu lượng thường quy hoặc bỏ lỡ sự suy giảm dần dần, nên suy giảm nhẹ nhàng kích hoạt phản ứng thay vì chủ động.

###### Các thực hành tốt

- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](agentrel08-bp01.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](agentrel08-bp02.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](agentrel08-bp03.md)
- [AGENTREL08-BP04 Theo dõi các số liệu sử dụng bộ nhớ của tác nhân](agentrel08-bp04.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
