# AGENTPERF04-BP01 Tối ưu các mẫu xử lý thông điệp bất đồng bộ

Nhắn tin bất đồng bộ cho các tác nhân vận hành độc lập ở nhịp tối ưu của chúng, với các hàng đợi thông điệp hấp thụ biến thiên **throughput** và san đều tải qua luồng công việc. Các mẫu yêu-cầu-phản-hồi đồng bộ tạo ra ghép cặp chặt khiến một tác nhân hạ nguồn chậm chặn toàn bộ chuỗi thượng nguồn. Bất đồng bộ tách rời các bên sản xuất khỏi các bên tiêu thụ để các tác nhân nhanh không bị các tác nhân chậm giữ lại.

**Kết quả mong muốn:**

- Bạn có giao tiếp tác-nhân-tới-tác-nhân và tác-nhân-tới-dịch-vụ dùng các mẫu bất đồng bộ theo mặc định, với giao tiếp đồng bộ được dành cho các tương tác thực sự đòi hỏi phản hồi tức thời.
- Bạn có các payload thông điệp gọn truyền tham chiếu thay vì dữ liệu nội tuyến.
- Bạn có các tác nhân xử lý thông điệp ở nhịp riêng của chúng mà không bị các bên sản xuất thượng nguồn áp đảo.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng yêu-cầu-phản-hồi HTTP đồng bộ cho mọi giao tiếp tác nhân, tạo ra ghép cặp chặt nơi một tác nhân hạ nguồn chậm chặn toàn bộ chuỗi thượng nguồn.
- Bao gồm các payload lớn (như tài liệu đầy đủ hoặc tệp mã-hóa-base64) trong các thông điệp thay vì truyền tham chiếu (như S3 URI hoặc document ID) và để bên tiêu thụ lấy dữ liệu khi cần.
- Bỏ qua các cơ chế backpressure, cho phép các tác nhân sản-xuất-nhanh áp đảo các tác nhân tiêu-thụ-chậm với các thông điệp xếp hàng và cuối cùng gây timeout.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thực thi tác nhân được tách rời giúp ngăn các tác nhân chậm chặn các tác nhân nhanh.
- Mỗi tác nhân mở rộng độc lập dựa trên độ sâu hàng đợi và tốc độ xử lý riêng của nó.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Với các tác nhân triển khai trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), quản lý phiên tích hợp sẵn của runtime xử lý truyền thông điệp và quản lý trạng thái cho giao tiếp tác-nhân-tới-tác-nhân bên trong một luồng công việc. Với các luồng công việc cần các mẫu nhắn tin tùy chỉnh hoặc tích hợp liên-hệ-thống, [Amazon SQS](https://aws.amazon.com/sqs/) cung cấp nhắn tin điểm-tới-điểm đáng tin và [Amazon SNS](https://aws.amazon.com/sns/) cung cấp fan-out nơi một sự kiện tác nhân duy nhất kích hoạt nhiều tác nhân hạ nguồn. Payload thông điệp nên giữ gọn: truyền S3 URI, khóa DynamoDB, hoặc document ID thay vì dữ liệu nội tuyến, và để bên tiêu thụ lấy các byte theo-yêu-cầu.

Dead letter queue (DLQ) nắm bắt các thông điệp thất bại xử lý sau các lần thử lại, để phân tích lỗi không chặn luồng chính. Khi các hàng đợi tiêu thụ vượt ngưỡng độ sâu, các bên sản xuất nên bị throttle hoặc các bên tiêu thụ được mở rộng. Cảnh báo Amazon CloudWatch trên độ sâu hàng đợi là tín hiệu kích hoạt một trong hai phản ứng. Với các luồng công việc lượng-lớn, kích thước lô SQS và long polling cho phép bạn cân bằng latency và throughput, long polling giảm các lần nhận-rỗng, và kích thước lô lớn hơn phân bổ đều chi phí yêu cầu qua nhiều thông điệp hơn.

### Các bước triển khai

- **Dùng quản lý phiên AgentCore Runtime cho giao tiếp tác-nhân-tới-tác-nhân nơi có thể, và dùng SQS hoặc SNS cho các mẫu nhắn tin tùy chỉnh:** Để runtime xử lý truyền thông điệp và trạng thái bên trong một luồng công việc, và chỉ quay về Amazon SQS hoặc Amazon SNS cho các mẫu tùy chỉnh hoặc tích hợp liên-hệ-thống.
- **Thiết kế các payload thông điệp gọn dùng tham chiếu thay vì dữ liệu nội tuyến:** Truyền S3 URI, khóa DynamoDB, hoặc document ID trong các thông điệp và để bên tiêu thụ lấy payload đầy đủ theo-yêu-cầu.
- **Triển khai dead letter queue cho xử lý thông điệp thất bại với cảnh báo trên độ sâu DLQ:** Định tuyến các thông điệp thất bại sau các lần thử lại tới một DLQ và cảnh báo khi độ sâu DLQ tăng, để phân tích lỗi xảy ra ngoài đường chính.
- **Thêm các cơ chế backpressure throttle các bên sản xuất khi các hàng đợi tiêu thụ vượt ngưỡng độ sâu:** Dùng cảnh báo Amazon CloudWatch trên độ sâu hàng đợi để kích hoạt throttling bên sản xuất hoặc mở rộng bên tiêu thụ trước khi các hàng đợi đạt độ sâu gây-timeout.
- **Cấu hình long polling và kích thước lô cho các bên tiêu thụ SQS dựa trên yêu cầu latency và throughput:** Tinh chỉnh long polling và kích thước lô trên các bên tiêu thụ SQS để cân bằng chi phí nhận-rỗng, latency mỗi-thông-điệp, và throughput.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả](agentperf04-bp02.md)
- [AGENTPERF04-BP03 Thiết kế các mẫu tích hợp hướng-sự-kiện hiệu năng cao](agentperf04-bp03.md)
- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](../5-agentperf05/agentperf05-bp01.md)

**Tài liệu liên quan:**

- [Xây dựng kiến trúc serverless cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/introduction.html)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Amazon SNS](https://aws.amazon.com/sns/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
