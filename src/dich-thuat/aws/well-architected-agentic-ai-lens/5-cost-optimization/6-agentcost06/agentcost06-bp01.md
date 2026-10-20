# AGENTCOST06-BP01 Triển khai khám phá và registry nhẹ cho cộng tác tiết kiệm chi phí

Triển khai hạ tầng service-mesh cho khám phá agent mang một chi phí cố định không scale xuống khi lưu lượng scale xuống. Bạn có thể giữ chi phí registry tỷ lệ với kích thước đội thông qua khám phá được quản lý qua việc trình ra công cụ, các registry dựa trên mức tiêu thụ, và caching metadata tích cực.

**Kết quả mong muốn:**

- Bạn dùng hạ tầng dựa trên mức tiêu thụ cho khám phá agent, chỉ tính phí cho các thao tác thực tế.
- Bạn phục vụ các tra cứu năng lực lặp lại từ một cache metadata thay vì cơ sở dữ liệu.
- Bạn giữ chi phí tỷ lệ với kích thước đội thông qua lập chỉ mục hiệu quả và các lần ghi theo lô.
- Bạn giám sát chi phí theo từng truy vấn để chúng không tăng âm thầm khi đội mở rộng.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai service mesh được quản lý cho các tra cứu năng lực đơn giản trong khi một cơ sở dữ liệu NoSQL với giá theo mức tiêu thụ đã đủ.
- Thực hiện các tra cứu registry lặp lại cho cùng metadata agent ở mọi lần gọi mà không caching.
- Dùng các quét toàn bảng thay vì các truy vấn có mục tiêu với các chỉ mục phù hợp, tiêu thụ dung lượng đọc không cần thiết.
- Vận hành các registry khám phá agent mà không giám sát chi phí theo từng truy vấn, vốn scale theo kích thước đội và tăng âm thầm khi đội mở rộng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Registry dựa trên mức tiêu thụ tránh chi phí hạ tầng cố định, chỉ tính phí cho các thao tác đọc và ghi thực tế.
- Caching metadata phục vụ các tra cứu năng lực lặp lại mà không có truy vấn cơ sở dữ liệu, tránh hầu hết các phí đọc.
- Các cập nhật năng lực theo lô giảm chi phí ghi bằng cách tích lũy các thay đổi thành các thao tác đơn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Khám phá agent qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) loại bỏ nhu cầu về hạ tầng registry tùy chỉnh trong nhiều kịch bản. Khi bạn trình ra các agent chuyên biệt như công cụ qua các khả năng MCP server của Gateway, các agent khác khám phá và gọi chúng mà không cần một registry riêng. AgentCore Gateway xử lý trao đổi thông tin xác thực, dịch giao thức, và kết hợp nhiều công cụ vào các endpoint hợp nhất dưới giá theo mức tiêu thụ. Cách tiếp cận này phù hợp khi các agent chủ yếu tương tác qua các mẫu gọi công cụ và các ngữ nghĩa khám phá tích hợp sẵn của Gateway khớp với các yêu cầu cộng tác của bạn.

Khi các điều kiện đó không giữ đúng, bạn có thể xây dựng một registry nhẹ tùy chỉnh dùng [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) với chế độ dung lượng on-demand và các global secondary index cho các truy vấn năng lực được lọc. Lập chỉ mục các năng lực agent theo loại và loại tác vụ để các truy vấn khám phá chỉ đọc các phân vùng liên quan thay vì quét toàn bộ registry. Khi các đội agent tăng lên, các truy vấn khám phá kém hiệu quả quét toàn bộ các tập năng lực nhân chi phí và làm suy giảm độ trễ cùng lúc, nên các truy vấn có mục tiêu qua các global secondary index trở thành đường cơ sở vận hành, không phải một tối ưu.

Caching metadata giúp bạn tối ưu chi phí một registry được thiết kế cho khả năng mở rộng. Một tra cứu năng lực trúng cache về cơ bản không tốn gì, trong khi một tra cứu rơi xuống DynamoDB phát sinh một phí đọc. Cấu hình các TTL phản ánh tần suất metadata năng lực thực sự thay đổi (thường là giờ, không phải giây), và dùng hệ thống tệp bền vững trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để cache metadata registry xuyên các chu kỳ dừng và tiếp tục phiên.

Giám sát trở nên ngày càng quan trọng, khi chi phí đọc registry scale theo khối lượng truy vấn, và các phí theo từng truy vấn tích lũy khi đội tăng lên. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch theo dõi chi phí đọc, tỷ lệ trúng cache, và khối lượng lần gọi API khám phá, với cảnh báo cho các mẫu bất thường trước khi chúng trở thành một khoản mục đáng điều tra.

### Các bước triển khai

- **Đánh giá khám phá dựa trên Gateway trước:** Xác định xem semantic tool selection của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) có đáp ứng các yêu cầu khám phá của bạn hay không. Nếu có, trình ra các agent qua các khả năng MCP server của Gateway và tránh registry tùy chỉnh hoàn toàn.
- **Dùng lưu trữ dựa trên mức tiêu thụ với lập chỉ mục hiệu quả:** Với các registry tùy chỉnh, dùng [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) với chế độ dung lượng on-demand. Thiết kế một global secondary index trên capability-category để các truy vấn được lọc theo loại năng lực hoặc loại tác vụ chỉ đọc các phân vùng liên quan.
- **Triển khai một cache metadata:** Cấu hình các TTL phù hợp với tần suất metadata năng lực thay đổi, và dùng hệ thống tệp bền vững của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để cache xuyên các chu kỳ phiên.
- **Giám sát chi phí registry:** Theo dõi chi phí đọc và tỷ lệ trúng cache bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch, với cảnh báo cho các mẫu bất thường.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md)
- [AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tạo tác hiệu quả](agentcost06-bp02.md)
- [AGENTCOST06-BP03 Thiết kế khởi tạo tiết kiệm chi phí thông qua warm pool và caching](agentcost06-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [AWS 2025 - AgentCore Registry: Discover, Govern, and Reuse AI Agents at Scale](https://www.youtube.com/watch?v=rIcOJrE-fTk)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Gateway tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
