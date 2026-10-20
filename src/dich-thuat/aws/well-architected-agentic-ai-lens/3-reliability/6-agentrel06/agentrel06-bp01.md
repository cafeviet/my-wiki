# AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa

Các hệ thống kế thừa phơi bày các giao diện được dựng cho các bên gọi đồng bộ, tất định, trong khi các tác nhân là bất đồng bộ và xác suất. Các lớp adapter phiên dịch giữa hai thế giới để các tác nhân có thể dùng các năng lực hiện có mà phía kế thừa không cần thay đổi.

**Kết quả mong muốn:**

- Bạn có các adapter tích hợp phơi bày các giao diện công cụ MCP được thiết kế cho tác nhân tiêu thụ và chuyển đổi sang các giao thức kế thừa bên trong.
- Bạn thực thi xử lý lỗi chuẩn tắc ánh xạ các mã lỗi kế thừa thành các loại mà tác nhân có thể diễn giải đồng nhất.
- Bạn giới hạn tốc độ ở lớp adapter để tốc độ gọi do tác nhân dẫn dắt không làm quá tải các hệ thống kế thừa.

**Các phản mẫu thường gặp (anti-patterns):**

- Đòi hỏi phải sửa đổi hệ thống kế thừa để hỗ trợ tích hợp tác nhân, thêm rủi ro triển khai và ma sát tổ chức.
- Ràng buộc các tác nhân trực tiếp với các giao diện kế thừa mà không có adapter, phơi bày các tác nhân trước độ phức tạp đặc thù của kế thừa.
- Bỏ qua giới hạn tốc độ trên các lời gọi tới hệ thống kế thừa, tạo ra quá tải làm suy giảm hiệu năng cho mọi bên tiêu thụ.

**Lợi ích khi áp dụng thực hành tốt này:**

- Sự ổn định của hệ thống kế thừa được bảo toàn thông qua các lớp adapter che chắn nó khỏi các mẫu tương tác của tác nhân.
- Các tác nhân và các hệ thống kế thừa tiến hóa theo các lịch độc lập thông qua các giao diện trừu tượng hóa.
- Việc áp dụng tác nhân tăng tốc vì tích hợp không đòi hỏi sửa đổi kế thừa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Các adapter giải quyết sự vênh trở kháng (impedance mismatch) giữa tác nhân và kế thừa. Phơi bày năng lực kế thừa như một công cụ MCP với một lược đồ mà tác nhân có thể suy luận về. Bên trong, chuyển đổi sang bất cứ gì hệ thống kế thừa nói: SOAP, screen scraping, truy vấn cơ sở dữ liệu, hoặc các tệp batch. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) đăng ký các adapter như các công cụ có thể khám phá với các chính sách xác thực nhất quán. Các tác nhân sau đó gọi các năng lực kế thừa qua cùng mẫu lời gọi công cụ mà chúng dùng cho các năng lực trên nền đám mây. [Bài blog về hợp nhất các máy chủ MCP qua AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/) bao quát mẫu hợp nhất nhiều adapter đằng sau một giao diện gateway duy nhất.

Ánh xạ lỗi làm cho adapter thực sự hữu ích. Các hệ thống kế thừa phát ra các mã lỗi đặc thù cho kiến trúc của chúng, và phơi bày trực tiếp các mã đó buộc mỗi tác nhân phải hiểu mọi hệ thống kế thừa. Một phân loại lỗi chuẩn tắc (hết thời gian kết nối, lỗi xác thực, vượt giới hạn tốc độ và hệ thống không khả dụng) cho phép các tác nhân áp dụng logic xử lý nhất quán mà không cần biết các chi tiết của từng hệ thống kế thừa. Việc phiên dịch từ mã kế thừa sang loại chuẩn tắc diễn ra bên trong adapter.

Giới hạn tốc độ giúp bảo vệ phía kế thừa. Các hệ thống kế thừa được định cỡ cho lưu lượng theo nhịp con người, không phải cho một tác nhân có thể gọi công cụ nhanh như LLM sinh ra các lời gọi công cụ. Giới hạn tốc độ ở cấp ứng dụng trong lớp adapter tiết lưu tốc độ gọi do tác nhân dẫn dắt về mức mà hệ thống kế thừa có thể chịu được. Kết hợp điều này với các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) giới hạn tác nhân nào có thể gọi các adapter kế thừa. Giám sát sức khỏe adapter qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để phát hiện các vấn đề độ tin cậy tích hợp kế thừa trước khi chúng trở thành sự cố.

### Các bước triển khai

- **Triển khai các adapter tích hợp phơi bày các giao diện công cụ MCP:** Chuyển đổi sang các giao thức kế thừa bên trong để các tác nhân thấy một giao diện lời gọi công cụ đồng nhất.
- **Đăng ký các adapter trong AgentCore Gateway:** Phơi bày các adapter qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với xác thực và khám phá để tác nhân gọi.
- **Triển khai ánh xạ lỗi chuẩn tắc:** Phiên dịch các mã lỗi kế thừa thành một phân loại nhất quán mà tác nhân có thể xử lý đồng nhất.
- **Thực thi kiểm soát truy cập và giới hạn tốc độ:** Dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cho kiểm soát truy cập và triển khai giới hạn tốc độ ở cấp ứng dụng trong adapter để bảo vệ các hệ thống kế thừa.
- **Giám sát sức khỏe adapter qua AgentCore Observability:** Phát hiện các vấn đề độ tin cậy tích hợp kế thừa qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP02 Thiết lập các cơ chế dự phòng cho sự suy giảm của hệ thống kế thừa](agentrel06-bp02.md)
- [AGENTREL06-BP03 Kiểm thử hiệu năng hệ thống suy giảm một cách đều đặn](agentrel06-bp03.md)
- [AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent](agentrel06-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Transform your MCP architecture: Unite MCP servers through AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Adding agentic AI to legacy apps with AgentCore (MAM345)](https://www.youtube.com/watch?v=_-X-N0J02UI)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
