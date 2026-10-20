# Khả năng quan sát và giám sát cho hệ thống agentic

Khả năng quan sát (observability) trong các hệ thống agentic đòi hỏi nắm bắt không chỉ các chỉ số hạ tầng, mà cả các bước suy luận của agent, các đường quyết định, và các mẫu thực thi luồng công việc. Các cách tiếp cận giám sát truyền thống phải được mở rộng để cung cấp tầm nhìn vào hành vi agent, các lời gọi Tools, và các tương tác đa agent.

| AGENTOPS05: Bạn triển khai khả năng quan sát và giám sát toàn diện cho hệ thống agentic như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các lần thực thi agent tạo ra các vết phân tán (distributed traces) nắm bắt các bước suy luận, các lời gọi Tools, các thao tác bộ nhớ, và các cuộc bàn giao liên agent, với ngữ cảnh vết được lan truyền qua mọi ranh giới dịch vụ.
- Các baseline hành vi được duy trì liên tục cho mỗi agent, và trôi lệch, bất thường, và suy giảm hiệu năng được phát hiện tự động trước khi chúng ảnh hưởng tới người dùng.
- Các quyết định, hành động, và suy luận của agent được nắm bắt trong các log có cấu trúc, truy vấn được và các vết kiểm toán bất biến (immutable), an toàn với PII, hỗ trợ gỡ lỗi, báo cáo tuân thủ, và phân tích pháp lý (forensic).
- Hiệu quả luồng công việc được đo qua một khung KPI được xác định bao phủ các chiều vận hành, chất lượng, hiệu quả, và kinh doanh, và các KPI được báo cáo tới các bên liên quan kỹ thuật và kinh doanh theo nhịp định kỳ.
- Người vận hành có các dashboard đặc thù luồng công việc bộc lộ sức khỏe, các nút thắt cổ chai, và các runbook khắc phục trong vài giây, rút ngắn thời gian trung bình để phát hiện và thời gian trung bình để giải quyết cho các sự cố agent.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với khả năng quan sát và giám sát của các hệ thống agentic như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Khả năng quan sát bị giới hạn ở các chỉ số hạ tầng, như thời lượng [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) và độ trễ [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html). Suy luận agent, các lời gọi Tools, và các thao tác bộ nhớ không được trang bị đo lường. Các log không có cấu trúc và rải rác qua các tài khoản. Các sự cố được chẩn đoán qua đối chiếu log thủ công. Không tồn tại baseline hành vi, KPI agent, hay vết kiểm toán bất biến. |
| 2 | Manh nha (Emerging) | Các luồng công việc agent chính được trang bị truy vết phân tán bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) hoặc các span [OpenTelemetry](https://aws.amazon.com/otel/). Các log JSON có cấu trúc chảy tới [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) với các lược đồ được tài liệu hóa. Tồn tại các [dashboard Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html) cơ bản và các cảnh báo ngưỡng tĩnh. Việc lưu giữ log ban đầu được cấu hình cho các nhu cầu vận hành và tuân thủ. |
| 3 | Được định nghĩa (Defined) | Các lược đồ telemetry được chuẩn hóa qua các agent, và tương quan vết đầu-cuối đạt được qua lan truyền W3C Trace Context. Các baseline hành vi được thu thập và [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) được cấu hình cho các chỉ số then chốt. Một khung KPI bao phủ các chiều vận hành, chất lượng, hiệu quả, và kinh doanh. Các dashboard đặc thù luồng công việc được liên kết với runbook, và các log có cấu trúc được truy vấn qua [Amazon CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html). |
| 4 | Chủ động (Proactive) | Phát hiện bất thường phân biệt trôi lệch dữ liệu (data drift), trôi lệch khái niệm (concept drift), và trôi lệch hiệu năng, và các cảnh báo được định tuyến theo loại và mức độ nghiêm trọng qua các luồng ứng phó tự động. Các KPI được rà soát theo nhịp định kỳ và các baseline điều chỉnh tự động. Các vết kiểm toán bất biến dùng [Amazon S3 Object Lock ở chế độ tuân thủ (compliance mode)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html) với che PII qua [các bộ lọc thông tin nhạy cảm của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html). Các KPI chất lượng tích hợp các điểm số [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html), và các dashboard được chú thích với các sự kiện triển khai để tương quan các thay đổi chỉ số với các thay đổi cấu hình. |
| 5 | Tối ưu (Optimized) | Khả năng quan sát tự chữa lành (self-healing). Phát hiện bất thường kích hoạt khắc phục tự động cho các mẫu đã biết, và dự báo KPI tiên đoán gắn cờ suy giảm trước khi các ngưỡng bị vượt qua. Các vòng lặp học liên tục cấp các tín hiệu khả năng quan sát trở lại vào cấu hình agent, lựa chọn Model, và thiết kế Tools. Tổ chức đóng góp vào các thực hành tốt của ngành cho khả năng quan sát agentic AI. |

## Các vấn đề thường gặp cần lưu ý

- Các tổ chức trang bị đo lường cho các chỉ số hạ tầng nhưng không cho các span đặc thù agent như các vòng lặp suy luận, các lời gọi Tools, và các thao tác bộ nhớ.
- Các nhóm triển khai truy vết mà không lan truyền ngữ cảnh qua các ranh giới agent, tạo ra các mảnh vết rời rạc không thể ghép lại thành luồng công việc mà người vận hành cần để chẩn đoán sự cố.
- Các baseline hành vi được đặt một lần tại thời điểm triển khai và không bao giờ được làm mới, nên sự tiến hóa hành vi chính đáng sinh ra các cảnh báo dương tính giả trong khi trôi lệch dần vốn định nghĩa lại baseline lại không được phát hiện.
- Các log được lưu trong lưu trữ có thể thay đổi (mutable) mà không có kiểm soát toàn vẹn hay che thông tin định danh cá nhân (PII), làm suy yếu giá trị bằng chứng của các vết kiểm toán và đồng thời tạo ra các phơi nhiễm về bảo vệ dữ liệu.
- Các KPI và dashboard được xác định tại thời điểm ra mắt và không bao giờ được xem lại khi các luồng công việc tiến hóa, nên các tổ chức tiếp tục đo các chỉ số không còn phản ánh điều quan trọng trong khi các chế độ lỗi mới không được giám sát.

###### Các thực hành tốt

- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](agentops05-bp01.md)
- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](agentops05-bp02.md)
- [AGENTOPS05-BP03 Triển khai ghi log có cấu trúc và các vết kiểm toán toàn diện](agentops05-bp03.md)
- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent](agentops05-bp04.md)
- [AGENTOPS05-BP05 Tạo các dashboard đặc thù luồng công việc cho sức khỏe vận hành](agentops05-bp05.md)
