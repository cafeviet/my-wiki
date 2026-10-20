# AGENTREL06-BP02 Thiết lập các cơ chế dự phòng cho sự suy giảm của hệ thống kế thừa

Các hệ thống kế thừa mang SLA khả dụng thấp hơn các dịch vụ trên nền đám mây, và các dạng lỗi của chúng thường khó lường. Các đường dự phòng nhận biết sức khỏe, cache cho dữ liệu tham chiếu, hàng đợi cho giao dịch, suy giảm nhẹ nhàng cho thời gian thực, giữ cho các luồng công việc của tác nhân tiếp tục chạy qua các sự cố kế thừa.

**Kết quả mong muốn:**

- Bạn có giám sát sức khỏe trên mọi tích hợp kế thừa với các cảnh báo kích hoạt việc kích hoạt dự phòng.
- Bạn có các dự phòng dựa trên cache cho dữ liệu tham chiếu và các dự phòng dựa trên hàng đợi cho các thao tác giao dịch.
- Bạn phục hồi tự động khi các hệ thống kế thừa quay lại, với các thăm dò định kỳ vô hiệu hóa cơ chế ngắt.

**Các phản mẫu thường gặp (anti-patterns):**

- Giả định các hệ thống kế thừa khớp với độ tin cậy trên nền đám mây, mà không triển khai các dự phòng cho SLA thực tế của chúng.
- Triển khai các dự phòng âm thầm trả về dữ liệu cũ kỹ hoặc không chính xác mà không báo cho các tác nhân hoặc người dùng.
- Bỏ qua giám sát sức khỏe kế thừa, nên các sự cố chỉ trở nên hiện hữu khi các tác vụ của tác nhân thất bại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chức năng tác nhân vẫn khả dụng trong các sự cố kế thừa thông qua các đường dự phòng định trước.
- Kích hoạt dự phòng chủ động thông qua giám sát sức khỏe thay thế việc phát hiện lỗi phản ứng.
- Người dùng và các hệ thống phía dưới thấy các chỉ báo minh bạch về năng lực suy giảm.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Giám sát sức khỏe là điều kiện tiên quyết cho bất kỳ dự phòng tự động nào. Không có tín hiệu sức khỏe, cách duy nhất để biết hệ thống kế thừa đã sập là theo dõi các lỗi mà người dùng nhìn thấy tích tụ. Các thăm dò định kỳ qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch kiểm tra tính khả dụng của điểm cuối và thời gian phản hồi. Các cảnh báo trên các thăm dò đó kích hoạt việc kích hoạt dự phòng trước khi lỗi đối mặt người dùng đầu tiên xảy ra.

Hình dạng dự phòng phụ thuộc vào loại thao tác. Đối với dữ liệu tham chiếu, danh mục sản phẩm, giá trị cấu hình, các tra cứu chủ yếu tĩnh, các dự phòng dựa trên cache phục vụ dữ liệu được truy xuất gần đây trong các sự cố. Chi phí về độ chính xác thấp vì dữ liệu không thay đổi thường xuyên. Đối với các thao tác giao dịch, các dự phòng dựa trên hàng đợi đệm các yêu cầu để phát lại khi hệ thống phục hồi, bảo toàn ý định của mỗi thao tác mà không cố thực hiện nó với một hệ thống không truy cập được. Đối với dữ liệu thời gian thực không thể cache hoặc đệm, giá trực tiếp, tồn kho hiện thời, trạng thái hệ thống tức thời, suy giảm nhẹ nhàng nghĩa là thông báo cho người dùng rằng thông tin tạm không khả dụng thay vì trả về một câu trả lời có vẻ hợp lý nhưng sai.

Các cơ chế ngắt tự động cần tự tháo gỡ, nếu không mọi sự cố sẽ biến thành một sự giáng cấp vĩnh viễn. Dùng các cảnh báo CloudWatch để phát hiện khi tỷ lệ lỗi vượt ngưỡng và kích hoạt các phản hồi tự động, cập nhật các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để từ chối truy cập công cụ hoặc kích hoạt logic circuit breaker dựa trên Lambda. Cấu hình các thăm dò định kỳ kiểm tra tính khả dụng và bật lại truy cập khi hệ thống phục hồi. Giám sát tần suất kích hoạt dự phòng qua AgentCore Observability để nhận diện các hệ thống kế thừa gây ra các vấn đề độ tin cậy không cân xứng. Đó là các ứng viên cho đầu tư hiện đại hóa.

### Các bước triển khai

- **Triển khai giám sát sức khỏe cho mỗi tích hợp kế thừa:** Dùng các thăm dò của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch để kiểm tra tính khả dụng của điểm cuối và thời gian phản hồi.
- **Cấu hình các cảnh báo kích hoạt việc kích hoạt dự phòng:** Cảnh báo trên sự suy giảm sức khỏe để các dự phòng kích hoạt trước khi các lỗi mà người dùng nhìn thấy tích tụ.
- **Triển khai các dự phòng phù hợp với thao tác:** Dự phòng dựa trên cache cho dữ liệu tham chiếu, dự phòng dựa trên hàng đợi cho các thao tác giao dịch, và các thông báo suy giảm nhẹ nhàng cho dữ liệu thời gian thực.
- **Triển khai các cơ chế ngắt tự động với phát hiện phục hồi:** Dùng các cảnh báo CloudWatch để kích hoạt các cập nhật [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) hoặc logic circuit breaker, và chạy các thăm dò định kỳ để bật lại truy cập khi hệ thống phục hồi.
- **Giám sát tần suất kích hoạt dự phòng:** Dùng AgentCore Observability để nhận diện các hệ thống kế thừa liên tục suy giảm, để có thể ưu tiên hóa nỗ lực hiện đại hóa.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác](../4-agentrel04/agentrel04-bp03.md)
- [AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa](agentrel06-bp01.md)
- [AGENTREL06-BP03 Kiểm thử hiệu năng hệ thống suy giảm một cách đều đặn](agentrel06-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
