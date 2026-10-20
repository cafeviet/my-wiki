# AGENTPERF07-BP02 Triển khai cô lập hiệu năng và throttling nhận-biết-tenant

Lòng tin vào một dịch vụ tác nhân dùng chung được xây dựng qua hiệu năng nhất quán, có thể dự đoán cho mọi tenant, ngay cả trong các đợt tăng nhu cầu. Trong các triển khai multitenant gộp, cô lập hiệu quả đòi hỏi throttling ở nhiều lớp (API, suy luận, bộ nhớ, và **Tools**), giám sát tiêu tài nguyên theo-tenant, và các cơ chế công bằng thích ứng phân phối các tài nguyên dùng chung một cách công bằng dựa trên tải hiện tại.

**Kết quả mong muốn:**

- Bạn có throttling theo-tenant được cưỡng chế ở mọi lớp tài nguyên dùng chung.
- Bạn có tiêu tài nguyên tenant được giám sát theo thời gian thực với cảnh báo cho các tenant tiệm cận giới hạn của họ.
- Bạn có throttling nhẹ nhàng cung cấp phản hồi rõ ràng cho các tenant bị throttle.
- Bạn có cô lập hiệu năng được xác nhận qua kiểm thử tải thường xuyên mô phỏng các kịch bản hàng-xóm-ồn-ào.

**Các phản mẫu thường gặp (anti-patterns):**

- Áp throttling chỉ ở lớp API gateway mà không cưỡng chế các giới hạn ở các tài nguyên dùng chung hạ nguồn, để các tenant bỏ qua các giới hạn cấp-API qua các thao tác chạy-dài.
- Dùng các giới hạn throttling tĩnh không thích ứng với tải hệ thống hiện tại, lãng phí dung lượng sẵn có trong các thời kỳ tải-thấp hoặc không bảo vệ cô lập trong các thời kỳ tải-cao.
- Throttle mọi tenant như nhau bất kể tầng dịch vụ của họ, không tôn trọng các SLA premium.

**Lợi ích khi áp dụng thực hành tốt này:**

- Throttling đa-lớp phân phối các tài nguyên dùng chung công bằng qua các tenant.
- Các chỉ số tiêu thụ theo-tenant thời-gian-thực hỗ trợ quản lý chủ động.
- Giám sát hiệu năng theo-tenant xác nhận tuân thủ SLA.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Throttling đa-lớp cưỡng chế các giới hạn tenant ở mọi tài nguyên dùng chung. Ở lớp API, các usage plan của [Amazon API Gateway](https://aws.amazon.com/api-gateway/) với các API key theo-tenant cưỡng chế các giới hạn tốc độ yêu cầu và burst. Ở lớp suy luận, xếp hàng yêu cầu nhận-biết-tenant giới hạn các lệnh gọi suy luận [Amazon Bedrock](https://aws.amazon.com/bedrock/) đồng thời theo-tenant. Ở các lớp bộ nhớ và Tools, giới hạn tốc độ theo-tenant áp cho các endpoint dùng chung. Với các tác nhân triển khai trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), cô lập phiên của runtime cung cấp các ranh giới tài nguyên theo-phiên tự nhiên.

Throttling thích ứng điều chỉnh các giới hạn dựa trên tải hệ thống hiện tại: trong các thời kỳ tải-thấp, các tenant có thể burst vượt các giới hạn đường cơ sở của họ để dùng dung lượng sẵn có, và trong các thời kỳ tải-cao, các giới hạn nghiêm ngặt bảo vệ cô lập. Các bảng điều khiển và chỉ số [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) theo-tenant theo dõi lượng yêu cầu, tiêu thụ suy luận, phân vị latency, tỷ lệ throttle, và tỷ lệ lỗi. Cảnh báo kích hoạt khi một tenant tiệm cận giới hạn của họ hoặc khi latency theo-tenant vượt các ngưỡng SLA. Kiểm thử hàng-xóm-ồn-ào thường xuyên, mô phỏng các kịch bản tải-cao cho các tenant riêng lẻ, xác nhận rằng hiệu năng của các tenant khác vẫn trong giới hạn SLA.

### Các bước triển khai

- **Định nghĩa các giới hạn throttling theo-tenant cho mỗi lớp tài nguyên:** Đặt các giới hạn theo-tenant cho số yêu cầu API mỗi giây, số lệnh gọi suy luận đồng thời, hạn ngạch lưu trữ bộ nhớ, và số lệnh gọi Tools mỗi phút.
- **Triển khai các usage plan API Gateway với các API key và giới hạn tốc độ/burst theo-tenant:** Dùng các usage plan của [Amazon API Gateway](https://aws.amazon.com/api-gateway/) với các API key theo-tenant để cưỡng chế các giới hạn tốc độ và burst ở lối vào.
- **Triển khai xếp hàng suy luận nhận-biết-tenant với các giới hạn đồng thời theo-tenant:** Xếp hàng các lệnh gọi suy luận [Amazon Bedrock](https://aws.amazon.com/bedrock/) theo-tenant để không tenant đơn lẻ nào có thể tiêu toàn bộ dung lượng suy luận.
- **Cấu hình throttling thích ứng điều chỉnh các giới hạn dựa trên tải hệ thống hiện tại:** Cho phép burst trong các thời kỳ tải-thấp và cưỡng chế các giới hạn nghiêm ngặt trong các thời kỳ tải-cao để bảo vệ cô lập.
- **Tạo các bảng điều khiển CloudWatch theo-tenant và cấu hình các cảnh báo dựa-trên-SLA:** Công bố các chỉ số theo-tenant trong [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) và cảnh báo khi tiêu thụ tiệm cận giới hạn hoặc latency vượt các ngưỡng SLA.
- **Thiết lập kiểm thử tải hàng-xóm-ồn-ào thường xuyên để xác nhận hiệu quả cô lập:** Lên lịch các kiểm thử tải hàng-xóm-ồn-ào mô phỏng các kịch bản tải-cao cho các tenant riêng lẻ và xác minh các tenant khác vẫn trong SLA.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF07-BP01 Thiết kế các mô hình triển khai tác nhân multi-tenant hiệu quả](agentperf07-bp01.md)
- [AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả](../4-agentperf04/agentperf04-bp02.md)
- [AGENTSUS01-BP04 Mở rộng các đường xử lý nhận thức một cách phù hợp](../../6-sustainability/1-agentsus01/agentsus01-bp04.md)

**Tài liệu liên quan:**

- [Xây dựng các kiến trúc multi-tenant cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-multitenant/introduction.html)
- [Cưỡng chế cô lập tenant, AI dạng tác nhân multi-tenant](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-multitenant/enforcing-tenant-isolation.html)

**Video liên quan:**

- [Xây dựng các tác nhân SaaS multi-tenant với AgentCore (SAS407)](https://www.youtube.com/watch?v=uwXrtyXXuy8)

**Dịch vụ liên quan:**

- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
