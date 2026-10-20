# Tích hợp hệ thống kế thừa (legacy)

Các tác nhân tích hợp với các hệ thống hiện có thông qua các mẫu bộ chuyển đổi (adapter) và các giao diện trừu tượng hóa sẽ bảo toàn sự ổn định của hệ thống kế thừa trong khi cho phép tự động hóa các quy trình đã thiết lập. Các hệ thống này có thể không được tối ưu cho các tương tác của tác nhân và có thể cần hỗ trợ các giao thức như MCP hoặc A2A. Làm thế nào để các tác nhân tích hợp hiệu quả mà không ảnh hưởng đến độ tin cậy của các quy trình đã thiết lập?

| AGENTREL06: Làm thế nào để các tác nhân tích hợp hiệu quả với các hệ thống hiện có mà không ảnh hưởng đến độ tin cậy của các quy trình đã thiết lập? |
| --- |
|  |

## Mục tiêu năng lực

- Các hệ thống kế thừa được tiếp cận qua các giao diện adapter phơi bày các hợp đồng công cụ bản địa (agent-native) cho tác nhân, nhờ đó các tác nhân không cần hiểu các giao thức đằng sau chúng.
- Các hệ thống kế thừa được bảo vệ khỏi các mẫu gọi bản địa của tác nhân thông qua giới hạn tốc độ (rate limiting) và kiểm soát truy cập áp dụng ở lớp adapter.
- Mỗi phụ thuộc kế thừa có một đường dự phòng được định nghĩa, nhờ đó các sự cố kế thừa gây ra năng lực giảm bớt thay vì lỗi tác nhân hoàn toàn.
- Các thao tác của tác nhân có tác dụng phụ là idempotent, nhờ đó phục hồi dựa trên thử lại là an toàn và không tạo ra các giao dịch trùng lặp hoặc trạng thái không nhất quán.
- Người vận hành có thể vô hiệu hóa và bật lại từng năng lực lúc chạy mà không cần triển khai lại, và mỗi năng lực có một hành vi dự phòng đã được kiểm thử tự kích hoạt khi nó bị tắt.
- Các cơ chế bền bỉ được diễn tập đều đặn thông qua tiêm lỗi và các ngày diễn tập (game day), nhờ đó các khoảng trống được phát hiện trong kiểm thử thay vì trong các sự cố vận hành.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với tích hợp hệ thống kế thừa như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Các tác nhân gọi các hệ thống kế thừa trực tiếp mà không có lớp adapter, nên các mã lỗi và đặc thù giao thức kế thừa rò rỉ vào logic của tác nhân. Không có các dự phòng tường minh, nên các sự cố kế thừa lan thành lỗi tác nhân hoàn toàn. Các lần thử lại được áp dụng mà không có idempotency, có thể tạo ra các giao dịch trùng lặp, và việc vô hiệu hóa một năng lực có vấn đề đòi hỏi triển khai lại. Tính bền bỉ được giả định thay vì kiểm thử. |
| 2 | Manh nha (Emerging) | Các adapter tích hợp được đưa vào cho các hệ thống kế thừa trọng yếu nhất, phơi bày các giao diện công cụ chuyển đổi sang các giao thức kế thừa bên trong. Các dự phòng một lần được thêm vào sau khi các sự cố đầu tiên bộc lộ nhu cầu, và các lần thử lại bắt đầu dùng idempotency key cho một tập nhỏ các thao tác rủi ro cao. Các đội thỉnh thoảng chạy các bài kiểm thử lỗi thủ công trước các bản phát hành lớn. Telemetry về sức khỏe adapter còn một phần và khác nhau theo hệ thống. |
| 3 | Xác lập (Defined) | Các adapter được đăng ký trong [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với một phân loại lỗi chuẩn tắc, nên các tác nhân xử lý các lỗi kế thừa một cách nhất quán. Mỗi phụ thuộc kế thừa có một chiến lược dự phòng khớp: dựa trên cache cho dữ liệu tham chiếu, dựa trên hàng đợi cho các thao tác giao dịch qua [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html), và suy giảm nhẹ nhàng cho dữ liệu thời gian thực. Idempotency được triển khai qua ghi có điều kiện của [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) và hết hạn dựa trên TTL, và việc bật/tắt năng lực qua các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cho phép kiểm soát lúc chạy. Các thí nghiệm [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) chạy theo một lịch xác định. |
| 4 | Chủ động (Proactive) | Sức khỏe tích hợp kế thừa được giám sát qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với các cảnh báo kích hoạt các cơ chế ngắt tự động dùng logic circuit breaker của [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), và các thăm dò phục hồi (recovery probes) bật lại truy cập khi các hệ thống phục hồi. Các idempotency key lan truyền qua các luồng công việc nhiều bước và được chuyển tới các hệ thống bên ngoài hỗ trợ idempotency bản địa. Các hành vi dự phòng được kiểm thử cùng với các triển khai chính, và tỷ lệ kích hoạt dự phòng nuôi việc ưu tiên hóa liên tục cho đầu tư độ tin cậy kế thừa. Các thí nghiệm FIS là một phần của CI/CD, và các ngày diễn tập hằng quý kiểm định các runbook trong điều kiện thực tế. |
| 5 | Tối ưu (Optimized) | Các mẫu adapter, chiến lược dự phòng và cơ chế idempotency được chuẩn hóa trên toàn tổ chức và tinh chỉnh liên tục dựa trên dữ liệu vận hành. Các công tắc năng lực (capability toggle), tỷ lệ kích hoạt dự phòng và các xu hướng sức khỏe kế thừa được tích hợp vào việc ra quyết định cho đầu tư hiện đại hóa hệ thống kế thừa. Hành vi tự chữa lành (tự ngắt, suy giảm nhẹ nhàng và phục hồi) là mặc định, và các ngày diễn tập tập dượt các lỗi đa hệ thống thay vì các sự cố dịch vụ đơn lẻ. Tổ chức công bố các mẫu nội bộ cho tích hợp tác nhân-tới-kế thừa và chia sẻ các chuẩn đo (benchmark) giữa các đội. |

## Các vấn đề thường gặp cần lưu ý

- Các tác nhân ràng buộc trực tiếp với các giao diện kế thừa mà không có lớp adapter, nên các thay đổi giao thức kế thừa gợn sóng qua mã của tác nhân và mỗi tác nhân xử lý các mã lỗi kế thừa theo cách riêng của nó.
- Các phụ thuộc kế thừa được giả định có độ tin cậy của các dịch vụ trên nền đám mây, nên không có đường dự phòng nào tồn tại và một sự cố kế thừa đơn lẻ gây ra lỗi tác nhân hoàn toàn.
- Các lần thử lại được áp dụng mà không có bảo đảm idempotency, nên phục hồi từ các lỗi thoáng qua tạo ra các giao dịch trùng lặp, trạng thái hỏng hoặc sự không nhất quán âm thầm.
- Việc vô hiệu hóa một năng lực có vấn đề đòi hỏi thay đổi mã và triển khai lại, kéo dài thời gian khắc phục trong các sự cố và không khuyến khích việc cắt bỏ các tính năng hành xử sai.
- Các cơ chế ngắt tự động mở khi lỗi nhưng không bao giờ đóng lại sau khi phục hồi vì không có thăm dò nào bật lại truy cập, để năng lực bị suy giảm lâu sau khi hệ thống kế thừa đã lành trở lại.
- Các cơ chế bền bỉ không bao giờ được diễn tập, nên các đường dự phòng, các runbook và cảnh báo chỉ được kiểm thử lần đầu tiên trong một sự cố thực.

###### Các thực hành tốt

- [AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa](agentrel06-bp01.md)
- [AGENTREL06-BP02 Thiết lập các cơ chế dự phòng cho sự suy giảm của hệ thống kế thừa](agentrel06-bp02.md)
- [AGENTREL06-BP03 Kiểm thử hiệu năng hệ thống suy giảm một cách đều đặn](agentrel06-bp03.md)
- [AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent](agentrel06-bp04.md)
- [AGENTREL06-BP05 Triển khai bật/tắt năng lực động](agentrel06-bp05.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
