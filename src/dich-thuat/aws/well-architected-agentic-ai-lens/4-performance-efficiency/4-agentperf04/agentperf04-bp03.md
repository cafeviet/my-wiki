# AGENTPERF04-BP03 Thiết kế các mẫu tích hợp hướng-sự-kiện hiệu năng cao

Các tác nhân phản ứng với sự kiện theo thời gian thực, thay đổi dữ liệu, hành động người dùng, và cảnh báo hệ thống, mang lại kết quả kinh doanh nhanh hơn các tác nhân polling để tìm việc. Các đăng ký sự kiện quá rộng kích hoạt các tác nhân cho các sự kiện không liên quan, thiếu lọc khiến các tác nhân xử lý và loại bỏ các sự kiện chúng không cần. Định tuyến kém hiệu quả thêm các trễ đẩy thời gian phản hồi vượt kỳ vọng người dùng.

**Kết quả mong muốn:**

- Bạn có các luồng công việc tác nhân được kích hoạt bởi các sự kiện được lọc chính xác khớp yêu cầu xử lý của chúng, với latency tối thiểu giữa phát-sự-kiện và gọi-tác-nhân.
- Bạn có các lược đồ sự kiện hiệu quả chỉ bao gồm metadata định tuyến, với các tác nhân lấy ngữ cảnh đầy đủ theo-yêu-cầu.
- Bạn có các mẫu hướng-sự-kiện hỗ trợ cả chế độ xử lý thời-gian-thực lẫn batch.

**Các phản mẫu thường gặp (anti-patterns):**

- Đăng ký các tác nhân vào các luồng sự kiện rộng mà không lọc, buộc các tác nhân nhận và xử lý các sự kiện chúng loại bỏ ngay và lãng phí tài nguyên compute.
- Dùng phát-hiện-sự-kiện dựa-trên-polling thay vì phân-phối-sự-kiện dựa-trên-đẩy, thêm latency và tiêu compute trong các thời kỳ rảnh rỗi.
- Bao gồm các payload dữ liệu đầy đủ trong các sự kiện thay vì các tham chiếu sự kiện, phình kích thước sự kiện và thời gian truyền tải mạng khi hầu hết các bên tiêu thụ chỉ cần một tập con.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phân phối dựa-trên-đẩy giảm latency giữa xảy-ra-sự-kiện và gọi-tác-nhân.
- Lọc tại bus sự kiện giảm lãng phí compute bằng cách chỉ gọi các tác nhân cho các sự kiện liên quan.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Dùng [Amazon EventBridge](https://aws.amazon.com/eventbridge/) làm bus sự kiện chính cho các trigger luồng công việc tác nhân, với các luật lọc dựa-trên-nội-dung định tuyến các sự kiện tới các tác nhân cụ thể dựa trên các thuộc tính sự kiện. Với các luồng throughput-cao, [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) với Lambda event source mapping hỗ trợ xử lý batch mà không ép các tác nhân vào lệnh gọi mỗi-sự-kiện. Payload sự kiện nên mang metadata, định danh, và thông tin định tuyến, dữ liệu đầy đủ thuộc về [Amazon S3](https://aws.amazon.com/s3/) hoặc [Amazon DynamoDB](https://aws.amazon.com/dynamodb/), với các tham chiếu trong sự kiện. EventBridge Schema Registry chuẩn hóa các định dạng sự kiện qua tổ chức để các bên tiêu thụ có thể tạo các code binding từ lược đồ thay vì phân tích JSON một-lần.

Với các tác nhân cần phản ứng với thay đổi cơ sở dữ liệu, [Amazon DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) kích hoạt các tác nhân trực tiếp từ thay đổi dữ liệu mà không cần polling. Khử trùng lặp sự kiện dùng khóa idempotency giúp ngăn các tác nhân xử lý cùng một sự kiện hai lần, liên quan bất cứ khi nào phân-phối-ít-nhất-một-lần là mặc định. Cho xử lý sự kiện phức tạp đòi hỏi tương quan nhiều sự kiện trước khi kích hoạt một tác nhân, [AWS Step Functions](https://aws.amazon.com/step-functions/) hoặc [EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/) tổng hợp và biến đổi các sự kiện trước khi gọi tác nhân.

### Các bước triển khai

- **Cấu hình các luật EventBridge với lọc dựa-trên-nội-dung để định tuyến các sự kiện tới các tác nhân cụ thể:** Dùng lọc dựa-trên-nội-dung trên [Amazon EventBridge](https://aws.amazon.com/eventbridge/) để các tác nhân chỉ nhận các sự kiện có thuộc tính khớp trách nhiệm của chúng.
- **Thiết kế các lược đồ sự kiện tối thiểu với tham chiếu thay vì payload đầy đủ, được đăng ký trong EventBridge Schema Registry:** Giữ payload sự kiện ở metadata định tuyến và định danh, lưu dữ liệu đầy đủ trong S3 hoặc DynamoDB, và đăng ký các lược đồ trong EventBridge Schema Registry để các bên tiêu thụ có thể tạo binding.
- **Triển khai DynamoDB Streams cho các trigger tác nhân do-thay-đổi-dữ-liệu:** Dùng [Amazon DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) để kích hoạt các tác nhân trực tiếp từ thay đổi dữ liệu mà không cần polling.
- **Triển khai khóa idempotency cho khử trùng lặp sự kiện trong logic xử lý tác nhân:** Áp khóa idempotency để các tác nhân không xử lý cùng một sự kiện hai lần dưới phân-phối-ít-nhất-một-lần.
- **Giám sát các chỉ số xử lý sự kiện: latency sự-kiện-tới-lệnh-gọi, hiệu quả lọc, và throughput:** Công bố các chỉ số này tới CloudWatch để lọc và định tuyến có thể được tinh chỉnh từ hành vi đo được.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF04-BP01 Tối ưu các mẫu xử lý thông điệp bất đồng bộ](agentperf04-bp01.md)
- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](../5-agentperf05/agentperf05-bp01.md)
- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](../1-agentperf01/agentperf01-bp03.md)

**Tài liệu liên quan:**

- [Xây dựng kiến trúc serverless cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/introduction.html)
- [Blog: Xây dựng tác nhân AI hiệu quả trên AWS Serverless](https://aws.amazon.com/blogs/compute/effectively-building-ai-agents-on-aws-serverless/)

**Dịch vụ liên quan:**

- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
