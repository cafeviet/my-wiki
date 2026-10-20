# Hiệu quả giao tiếp và giao thức

Giao tiếp hiệu quả giữa các tác nhân, **Tools**, và dịch vụ mở rộng các hệ đa tác nhân từ nguyên mẫu tới production mà không để **latency** tăng theo độ phức tạp. Các hệ thống AI dạng tác nhân dựa vào giao tiếp giữa các tác nhân, Tools, dịch vụ, và người dùng thông qua các giao thức và mẫu nhắn tin khác nhau. Hiệu quả của các kênh giao tiếp này ảnh hưởng trực tiếp tới hiệu năng tác nhân. Mỗi trao đổi thông điệp thêm latency, mỗi bắt-tay giao thức tiêu thời gian, và mỗi thao tác tuần tự hóa (serialization) hoặc giải-tuần-tự-hóa (deserialization) dùng tài nguyên compute. Tối ưu giao tiếp đòi hỏi chọn các giao thức phù hợp cho mỗi mẫu tương tác, triển khai nhắn tin bất đồng bộ hiệu quả, và thiết kế các kiến trúc hướng-sự-kiện giảm thiểu polling và xử lý không cần thiết.

| AGENTPERF04: Bạn đạt được giao tiếp và sử dụng giao thức hiệu quả trên các tương tác tác nhân như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Giao tiếp tác-nhân-tới-tác-nhân và tác-nhân-tới-dịch-vụ dùng nhắn tin bất đồng bộ theo mặc định, với các lệnh gọi đồng bộ được dành cho các tương tác thực sự đòi hỏi phản hồi tức thời.
- Các giao thức được chọn theo từng mẫu tương tác, với **MCP** cho tích hợp Tools, **A2A** cho điều phối tác-nhân-tới-tác-nhân, và các giao thức truyền tải streaming như WebSocket cho các tương tác người dùng thời-gian-thực.
- Tích hợp hướng-sự-kiện là dựa-trên-đẩy (push-based) và được lọc chính xác, để các tác nhân chỉ được gọi cho các sự kiện khớp yêu cầu xử lý của chúng và không tiêu compute khi rảnh rỗi.
- Payload thông điệp và sự kiện mang các tham chiếu tới các kho bền thay vì dữ liệu nhúng, giữ thời gian truyền tải thấp và cho các bên tiêu thụ bỏ qua công việc trên các sự kiện đã trở nên không liên quan.
- Gộp kết nối, nén cấp-giao-thức, và caching Token giữ chi phí mỗi-tương-tác phẳng khi số bước-nhảy tác-nhân-tới-tác-nhân và lệnh gọi Tools tăng.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với hiệu quả giao tiếp và giao thức.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Giao tiếp tác nhân chạy trên HTTP/REST đồng bộ với payload JSON đầy đủ trên mọi lệnh gọi. Polling là cơ chế phát-hiện-sự-kiện mặc định. Kết nối được mở mỗi lệnh gọi, và lựa chọn giao thức, kích thước payload, và chi phí xác thực không được theo dõi. Các vấn đề mở rộng chỉ hiện lên sau một đợt gián đoạn hoặc một chuỗi timeout dây chuyền. |
| 2 | Manh nha (Emerging) | Các nhóm đã đưa vào nhắn tin bất đồng bộ qua [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) cho các luồng công việc điểm-tới-điểm và [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) cho fan-out. Dead letter queue được gắn vào các hàng đợi quan trọng và độ sâu hàng đợi được giám sát. Hầu hết các trigger sự kiện vẫn dùng polling, và lựa chọn giao thức không nhất quán giữa các tác nhân. |
| 3 | Đã định nghĩa (Defined) | MCP được chuẩn hóa cho giao tiếp tác-nhân-tới-Tool qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), và [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) với lọc dựa-trên-nội-dung định tuyến các sự kiện dựa-trên-đẩy tới các tác nhân cần chúng. Payload thông điệp truyền tham chiếu thay vì dữ liệu, và các tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) dùng quản lý phiên của runtime cho giao tiếp trong-luồng-công-việc. Hướng dẫn lựa chọn giao thức được ghi tài liệu và tuân theo. |
| 4 | Chủ động (Proactive) | A2A qua AgentCore Runtime xử lý điều phối tác-nhân-tới-tác-nhân có cấu trúc, và [API WebSocket của Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html) phục vụ các tương tác người dùng streaming. Gộp kết nối, nén cấp-giao-thức, và caching Token qua [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) là chuẩn. Khóa idempotency bảo vệ chống phân phối sự kiện trùng lặp. Áp lực ngược (backpressure) trên hàng đợi và latency sự-kiện-tới-lệnh-gọi được cảnh báo và dẫn dắt mở rộng tự động. |
| 5 | Tối ưu (Optimized) | Lựa chọn giao thức, định cỡ hàng đợi, và lọc sự kiện được hiệu chỉnh liên tục từ telemetry production. Chi phí xác thực và tuần tự hóa theo-bước-nhảy được lập ngân sách và tối ưu ở cấp-luồng-công-việc thay vì mỗi dịch vụ. Các mẫu giao tiếp và công việc khả năng-tương-tác chảy lại vào các chuẩn nội bộ và được chia sẻ với cộng đồng AI dạng tác nhân rộng hơn. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm mặc định về HTTP/REST đồng bộ cho mọi giao tiếp tác nhân, tạo ra ghép cặp chặt nơi một thành phần hạ nguồn chậm chặn toàn bộ chuỗi thượng nguồn và lan các vấn đề mở rộng qua luồng công việc.
- Các tác nhân nhận các luồng sự kiện rộng mà không có lọc dựa-trên-nội-dung và chi compute nhận, phân tích, và loại bỏ các sự kiện chúng không bao giờ hành động, điều này phình chi phí và che khuất latency của các sự kiện thực sự quan trọng.
- Payload thông điệp và sự kiện nội tuyến (inline) dữ liệu đầy đủ (tài liệu, tệp mã-hóa-base64, toàn bộ bản ghi) thay vì truyền tham chiếu, nên throughput hàng đợi và truyền tải mạng bị tiêu bởi các payload mà các bên tiêu thụ có thể lấy theo-yêu-cầu.
- Backpressure và dead letter queue vắng mặt, điều này để các bên sản xuất nhanh áp đảo các bên tiêu thụ chậm và che giấu các lỗi thông điệp dai dẳng cho tới khi một timeout hạ nguồn hoặc sự cố mất-dữ-liệu buộc điều tra.
- Chi phí xác thực, thiết lập kết nối, và tuần tự hóa được theo dõi như các chỉ số cấp-dịch-vụ thay vì các chi phí theo-bước-nhảy, nên một luồng công việc với nhiều bước-nhảy tác-nhân-tới-tác-nhân tích lũy latency âm thầm mà không telemetry của dịch vụ đơn lẻ nào phơi bày.

###### Các thực hành tốt

- [AGENTPERF04-BP01 Tối ưu các mẫu xử lý thông điệp bất đồng bộ](agentperf04-bp01.md)
- [AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả](agentperf04-bp02.md)
- [AGENTPERF04-BP03 Thiết kế các mẫu tích hợp hướng-sự-kiện hiệu năng cao](agentperf04-bp03.md)
