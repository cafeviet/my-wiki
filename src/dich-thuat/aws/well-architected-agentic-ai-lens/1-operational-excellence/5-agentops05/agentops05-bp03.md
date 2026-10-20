# AGENTOPS05-BP03 Triển khai ghi log có cấu trúc và các vết kiểm toán toàn diện

Các log dạng văn bản tự do trông có vẻ hữu ích cho đến khi ai đó cố truy vấn chúng ở quy mô lớn. Các log có cấu trúc, các vết kiểm toán bất biến, và các chính sách lưu giữ được xác định biến log của bạn thành một công cụ vận hành chủ động cung cấp bằng chứng cho tuân thủ.

**Kết quả mong muốn:**

- Mọi quyết định, hành động, và tương tác của agent được nắm bắt trong các log có cấu trúc, truy vấn được.
- Các vết kiểm toán là bất biến và có bằng chứng chống giả mạo (tamper-evident), cung cấp một hồ sơ đáng tin cậy cho mục đích tuân thủ pháp lý và quản trị.
- Các chính sách lưu giữ log cân bằng nhu cầu vận hành và tuân thủ với chi phí lưu trữ.
- Các nhóm được ủy quyền truy vấn dữ liệu log hiệu quả qua các giao diện được xác định.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng ghi log văn bản tự do không có cấu trúc vốn không thể truy vấn hay phân tích cú pháp hiệu quả ở quy mô lớn.
- Chỉ ghi log các lỗi và ngoại lệ mà không nắm bắt các thao tác thành công, tạo ra một bức tranh không đầy đủ làm giảm khả năng tái dựng toàn bộ chuỗi.
- Lưu các log trong lưu trữ có thể thay đổi (mutable) mà không có kiểm soát toàn vẹn, tạo ra các vết kiểm toán có thể bị thay đổi và do đó không thể tin cậy cho tuân thủ.
- Ghi log thông tin nhạy cảm, thông tin định danh cá nhân (PII) hoặc thông tin xác thực (credentials), trong các vết suy luận agent, tạo ra rủi ro tuân thủ và bảo mật.
- Vận hành mà không có các chính sách lưu giữ, tạo ra khối lượng log không giới hạn vốn trở nên đắt để lưu trữ và khó tìm kiếm.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các vết kiểm toán bất biến, có cấu trúc cung cấp nền tảng bằng chứng cho tuân thủ pháp lý và chứng minh rằng các agent vận hành trong các ranh giới được ủy quyền.
- Ghi log có cấu trúc với các giao diện truy vấn hiệu quả biến dữ liệu log từ một hồ sơ thụ động thành một công cụ vận hành chủ động, cho phép điều tra sự cố nhanh và trích xuất mẫu.
- Che PII tại thời điểm ghi giúp ngăn thông tin nhạy cảm đến được lưu trữ log, giảm rủi ro bảo vệ dữ liệu.
- Lưu giữ theo tầng giữ các log liên quan tới tuân thủ sẵn có trong nhiều năm trong khi loại bỏ các log gỡ lỗi ngắn hạn vốn sẽ tích tụ chi phí.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Ghi log có cấu trúc là một kỷ luật định dạng xác minh rằng các thực hành ghi log khác của bạn hoạt động đúng. JSON của bạn nên có một lược đồ chuẩn hóa để nó truy vấn được, bao gồm:

- Timestamp (mốc thời gian)
- Trace ID
- Agent ID
- Session ID
- Loại thao tác
- Lý do quyết định (decision rationale)
- Kết quả

Các log văn bản tự do đòi hỏi các tìm kiếm regex để trả lời các câu hỏi đơn giản, trong khi các log có cấu trúc trả lời chúng qua các truy vấn [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/) Insights trên các trường được đặt tên. Hãy áp đặt lược đồ, ngay cả khi nó đơn giản.

Chính sách lưu giữ của bạn nên phụ thuộc vào mục đích của các log.

- Log vận hành (30–90 ngày) hỗ trợ điều tra sự cố và phân tích xu hướng gần đây.
- Log tuân thủ (1–7 năm tùy các yêu cầu pháp lý) hỗ trợ kiểm toán và điều tra pháp lý.
- Log gỡ lỗi (7–14 ngày) hỗ trợ phát triển và đắt để giữ vượt quá thời gian đó.

Áp dụng các chính sách lưu giữ khác nhau cho các luồng log khác nhau, thay vì một chính sách cho tất cả, cắt giảm chi phí lưu trữ đáng kể mà không mất thông tin log quan trọng.

Che PII nên diễn ra trước khi các log đến được lưu trữ. Các bộ lọc thông tin nhạy cảm của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) phát hiện và che PII tại thời điểm ghi, vốn là nơi đáng tin cậy duy nhất để làm điều đó. Một khi PII đã ở trong log, mọi truy cập hạ nguồn trở thành một mối lo về bảo vệ dữ liệu.

Đối với các log quan trọng về tuân thủ, [Amazon S3](https://aws.amazon.com/s3/) với Object Lock ở chế độ Compliance cung cấp lưu trữ bất biến hỗ trợ các yêu cầu pháp lý cho các vết kiểm toán có bằng chứng chống giả mạo. [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) nắm bắt các hành động agent ở cấp API như một bổ sung hạ tầng, và [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) nắm bắt các chuỗi suy luận agent, các lời gọi Tools, và các tài liệu quyết định một cách tự động cho các agent trên AgentCore Runtime.

Hãy thiết lập các mẫu truy vấn được lưu (saved query templates) để giảm độ trễ điều tra. Đối với các log kiểm toán bất biến tập trung vào bảo mật với toàn vẹn mã hóa (cryptographic integrity), xem [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tài liệu quyết định](../../2-security/5-agentsec05/agentsec05-bp01.md).

### Các bước triển khai

- **Định nghĩa một lược đồ log JSON:** Bao phủ trace ID, loại thao tác, lý do quyết định, và kết quả như các trường chuẩn cho mọi thao tác agent.
- **Cấu hình lưu giữ theo tầng:** Tách các luồng log vận hành (30–90 ngày), tuân thủ (1–7 năm), và gỡ lỗi (7–14 ngày).
- **Che PII trước khi ghi:** Tích hợp các bộ lọc thông tin nhạy cảm của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) vào đường ống ghi log.
- **Dùng lưu trữ bất biến cho các log tuân thủ:** Ghi các vết kiểm toán vào [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) với Object Lock ở chế độ Compliance.
- **Tạo các mẫu truy vấn được lưu:** Bao phủ các mẫu phân tích vận hành phổ biến để ứng phó sự cố không bắt đầu từ màn hình trắng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](agentops05-bp01.md)
- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](agentops05-bp02.md)
- [AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)](../4-agentops04/agentops04-bp02.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và hỗ trợ phục hồi](../../3-reliability/7-agentrel07/agentrel07-bp03.md)
- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tài liệu quyết định](../../2-security/5-agentsec05/agentsec05-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Observing agentic AI workloads using Amazon CloudWatch](https://aws.amazon.com/blogs/mt/observing-agentic-ai-workloads-using-amazon-cloudwatch/)
- [Getting started with Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html)
- [Advancing AI agent governance with Boomi and AWS](https://aws.amazon.com/blogs/machine-learning/advancing-ai-agent-governance-with-boomi-and-aws-a-unified-approach-to-observability-and-compliance)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
