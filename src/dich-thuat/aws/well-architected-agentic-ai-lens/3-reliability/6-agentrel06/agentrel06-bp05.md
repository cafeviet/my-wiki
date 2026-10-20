# AGENTREL06-BP05 Triển khai bật/tắt năng lực động

Hạ toàn bộ một tác nhân xuống để sửa một tính năng hành xử sai là không tương xứng. Các cờ tính năng (feature flag) tại ranh giới gateway cho phép người vận hành vô hiệu hóa năng lực bị ảnh hưởng ngay lập tức, giữ cho phần còn lại của tác nhân dùng được trong khi các bản sửa hoặc các cuộc điều tra tiến hành.

**Kết quả mong muốn:**

- Bạn có các công tắc năng lực (capability toggle) vô hiệu hóa các công cụ hoặc tính năng cụ thể mà không cần triển khai lại tác nhân.
- Bạn có các hành vi dự phòng được định nghĩa cho mỗi năng lực để các tác nhân tiếp tục hoạt động khi một tính năng bị vô hiệu hóa.
- Bạn giám sát trạng thái công tắc và mức sử dụng dự phòng để các năng lực biểu hiện suy giảm âm thầm nổi lên qua các tỷ lệ dự phòng tăng cao.

**Các phản mẫu thường gặp (anti-patterns):**

- Đòi hỏi triển khai lại để vô hiệu hóa các năng lực có vấn đề, kéo dài thời gian khắc phục.
- Triển khai các công tắc mà không có hành vi dự phòng, nên việc vô hiệu hóa một năng lực gây ra lỗi tác nhân thay vì chức năng giảm bớt.
- Bỏ qua truyền đạt cho người dùng khi các tính năng không khả dụng, khiến người dùng bối rối về năng lực hiện tại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các vấn đề đặc thù năng lực được khắc phục nhanh chóng mà không cần triển khai lại toàn bộ tác nhân.
- Chức năng tổng thể của tác nhân sống sót qua các công tắc năng lực thông qua các dự phòng nhẹ nhàng.
- Các năng lực mới có thể được triển khai từ từ và hoàn tác ngay lập tức khi có vấn đề xuất hiện.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Bật/tắt ở cấp gateway là điểm kiểm soát. Các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) có thể bật hoặc tắt truy cập công cụ cụ thể cho các tác nhân mà không cần triển khai lại, cung cấp kiểm soát tức thời về việc năng lực nào khả dụng. Các cập nhật chính sách lan truyền nhanh chóng, nên công tắc có thể được lật trong khi một sự cố còn đang diễn ra thay vì chờ một cửa sổ triển khai. Đối với việc bật/tắt chi tiết hơn lúc chạy bên trong logic của tác nhân, dùng một dịch vụ cấu hình được quản lý với cache cục bộ và các khoảng thăm dò (polling interval) cấu hình được để các tác nhân đáp ứng với các thay đổi trong vòng vài giây.

Các hành vi dự phòng là điều làm cho việc bật/tắt an toàn. Định nghĩa tác nhân làm gì khi một năng lực bị vô hiệu hóa. Ví dụ gồm tìm kiếm ngữ nghĩa lùi về tìm kiếm theo từ khóa, suy luận phức tạp lùi về các quy tắc đơn giản hơn, và dữ liệu thời gian thực lùi về các giá trị cache. Tài liệu hóa các hành vi dự phòng bên cạnh các định nghĩa năng lực để người vận hành biết tác động của việc lật mỗi công tắc. Coi các đường dự phòng như mã hạng nhất và kiểm thử chúng cùng với các triển khai chính để chúng thực sự hoạt động khi bạn cần.

Giám sát làm cho hệ thống tự nhận biết. Theo dõi trạng thái công tắc năng lực và mức sử dụng dự phòng qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Các cảnh báo trên các tỷ lệ dự phòng vượt đường cơ sở báo hiệu các năng lực đang gặp vấn đề ngay cả khi không bị tắt tường minh, cho người vận hành cảnh báo sớm trước khi người dùng báo cáo vấn đề. Điều này biến cơ chế công tắc từ một cần gạt thủ công thành một bề mặt phát hiện chủ động.

### Các bước triển khai

- **Triển khai bật/tắt năng lực qua AgentCore Policy:** Dùng các chính sách Cedar trong [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để kiểm soát truy cập công cụ tại ranh giới gateway.
- **Định nghĩa và triển khai các hành vi dự phòng cho mỗi năng lực:** Tài liệu hóa hành vi năng-lực-giảm-bớt tự kích hoạt khi một công tắc bị lật.
- **Kiểm thử các đường dự phòng cùng với các triển khai chính:** Kiểm định rằng các dự phòng tạo ra kết quả chấp nhận được, không chỉ là chúng không báo lỗi.
- **Giám sát trạng thái công tắc và mức sử dụng dự phòng:** Theo dõi cả hai qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).
- **Cấu hình các cảnh báo trên các tỷ lệ dự phòng tăng cao:** Phát hiện các năng lực đang gặp vấn đề trước khi người dùng báo cáo chúng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa](agentrel06-bp01.md)
- [AGENTREL06-BP02 Thiết lập các cơ chế dự phòng cho sự suy giảm của hệ thống kế thừa](agentrel06-bp02.md)
- [AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent](agentrel06-bp04.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](../8-agentrel08/agentrel08-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
