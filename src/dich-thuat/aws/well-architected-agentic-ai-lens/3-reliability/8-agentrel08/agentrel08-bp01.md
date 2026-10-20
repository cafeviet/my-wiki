# AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán

Khi các thể hiện tác nhân khác nhau chạy với cấu hình khác nhau, các vấn đề độ tin cậy phát sinh vừa khó tái lập vừa khó tin cậy hơn. Cấu hình tập trung với đánh phiên bản, kiểm định và phân phối tự động giữ cho mọi thể hiện ở cùng một trạng thái hiện thời và biến việc hoàn tác thành việc đổi một con trỏ phiên bản.

**Kết quả mong muốn:**

- Bạn có cấu hình tập trung với đánh phiên bản và kiểm định cho mọi thiết lập mà các tác nhân đọc động.
- Bạn có các chiến lược triển khai, triển khai từ từ cho các thay đổi thường quy, tức thời cho các trường hợp khẩn cấp, với hoàn tác tự động khi có lỗi.
- Bạn phát hiện độ trôi cấu hình trên toàn đội tác nhân và khắc phục nó tự động.

**Các phản mẫu thường gặp (anti-patterns):**

- Gán cứng cấu hình trong mã của tác nhân, đòi hỏi triển khai lại để thay đổi các giá trị và làm giảm khả năng điều chỉnh động.
- Quản lý cấu hình mà không đánh phiên bản, khiến không thể xác định thay đổi nào gây ra thoái lui hoặc hoàn tác sạch sẽ.
- Áp dụng các thay đổi cấu hình mà không kiểm định, để các giá trị cấu hình sai tới môi trường vận hành.

**Lợi ích khi áp dụng thực hành tốt này:**

- Hành vi của tác nhân giữ nhất quán qua các thể hiện thông qua quản lý tập trung.
- Các thay đổi cấu hình được xuất xưởng an toàn thông qua kiểm định và triển khai từ từ với khả năng hoàn tác.
- Các vấn đề vận hành được giải quyết nhanh hơn thông qua điều chỉnh động mà không cần triển khai lại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Cấu hình tập trung là mẫu hợp nhất. Các năng lực cấu hình của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) quản lý các thiết lập của tác nhân một cách tập trung với đánh phiên bản và kiểm định. Cấu hình lúc chạy mà các tác nhân đọc động bao gồm chọn mô hình, tính khả dụng của công cụ, giới hạn tốc độ, cờ tính năng và các ngưỡng vận hành. Dùng một dịch vụ cấu hình được quản lý với các bộ kiểm định JSON Schema thực thi sự tuân thủ trước khi triển khai. Kiểm định ở lớp cấu hình bắt các giá trị tồi trước khi chúng trở thành sự cố vận hành.

Chiến lược triển khai giữ cho các thay đổi cấu hình an toàn. Triển khai từ từ xử lý trường hợp thường quy. Lan truyền cấu hình mới tới một tỷ lệ phần trăm nhỏ của đội, theo dõi các thoái lui, rồi mở rộng. Hoàn tác tự động khi có lỗi đảo ngược thay đổi khi có sự cố. Triển khai tức thời xử lý trường hợp khẩn cấp nơi cấu hình hiện tại đang tích cực phá vỡ môi trường vận hành và việc chữa trị không thể chờ triển khai từ từ. Có sẵn cả hai chế độ, và biết chế độ nào áp dụng cho mỗi thay đổi, là điều giữ cho hệ thống đáp ứng nhanh mà không liều lĩnh.

Phát hiện độ trôi khép kín vòng lặp. Việc phát hiện thay đổi cấu hình trong các hàm của tác nhân ghi log khi các phiên bản thay đổi, cho phép tương quan các thay đổi hành vi với các bản triển khai cụ thể. Đối với các giá trị cấu hình nhạy cảm, dùng kho tham số được mã hóa với kiểm soát truy cập chi tiết. Giám sát độ trôi cấu hình trên toàn đội tác nhân qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), cảnh báo khi các thể hiện đang chạy với các phiên bản cấu hình khác nhau. Độ trôi kéo dài thường là dấu hiệu cho thấy việc triển khai đã lan ra một phần hoặc một ghi đè thủ công đã được áp dụng và bị quên.

### Các bước triển khai

- **Định nghĩa các hồ sơ cấu hình (configuration profile) theo từng miền:** Xây dựng các hồ sơ cho chọn mô hình, tính khả dụng của công cụ, giới hạn tốc độ và cờ tính năng. Áp dụng kiểm định JSON Schema cho mỗi hồ sơ.
- **Cấu hình các chiến lược triển khai:** Dùng triển khai từ từ cho các thay đổi thường quy và triển khai tức thời cho các trường hợp khẩn cấp, với hoàn tác tự động khi có lỗi.
- **Triển khai ghi log phát hiện thay đổi cấu hình:** Ghi log các thay đổi phiên bản để các thay đổi hành vi có thể được tương quan với các bản triển khai.
- **Dùng kho tham số được mã hóa cho các giá trị nhạy cảm:** Áp dụng kiểm soát truy cập chi tiết trên các bí mật.
- **Giám sát độ trôi cấu hình:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để cảnh báo khi các thể hiện chạy các phiên bản cấu hình khác nhau.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP05 Triển khai bật/tắt năng lực động](../6-agentrel06/agentrel06-bp05.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](agentrel08-bp02.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](agentrel08-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Make agents a reality with Amazon Bedrock AgentCore: Now generally available](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-is-now-generally-available/)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Operationalizing agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
