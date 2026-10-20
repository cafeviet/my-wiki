# Phục hồi vận hành và giám sát mức tiêu thụ

Các hệ thống agentic phải xử lý các lỗi vận hành một cách nhã nhặn và giúp ngăn hành vi mất kiểm soát (runaway) vốn có thể ảnh hưởng tới các hoạt động kinh doanh. Các cơ chế phục hồi cần cân bằng giữa tự động hóa và leo thang phù hợp, và giám sát mức tiêu thụ phải phát hiện các agent vượt quá các ranh giới vận hành kỳ vọng.

| AGENTOPS07: Bạn thiết lập phục hồi vận hành và giám sát mức tiêu thụ như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các lỗi agent kích hoạt các ngắt tự động, các chuỗi dự phòng, và các luồng phục hồi giúp khôi phục dịch vụ trong các mục tiêu thời gian phục hồi (recovery time objectives) được xác định.
- Tri thức vận hành về hành vi agent, các chế độ lỗi, và các cách giải quyết được nắm bắt tập trung và giữ khả năng tìm kiếm khi con người và hệ thống thay đổi.
- Mỗi thay đổi agent đi qua một luồng được tài liệu hóa, kiểm định cả tính đúng đắn kỹ thuật lẫn sự phù hợp liên tục với các quy trình kinh doanh, chính sách, và nghĩa vụ pháp lý.
- Người vận hành có các runbook đã được kiểm thử, diễn tập mà họ có thể thực thi mà không cần hạ tầng agent, để các hoạt động kinh doanh tiếp tục qua các gián đoạn agent trong trường hợp xấu nhất.
- Các cơ chế phục hồi, các cơ sở tri thức, và các quy trình khẩn cấp được diễn tập thường xuyên, và các phát hiện cấp trở lại các cải tiến cho hạ tầng agent và cho chính các runbook.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với phục hồi vận hành và giám sát mức tiêu thụ như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các lỗi agent được xử lý theo kiểu phản ứng bởi bất cứ ai nhận ra đầu tiên. Các quy trình phục hồi không được tài liệu hóa và các runbook cho các kịch bản xấu nhất bị thiếu. Tri thức vận hành nằm ở từng cá nhân, và quản trị thay đổi đối xử các cập nhật agent như các thay đổi mã chung mà không xét sự phù hợp kinh doanh. |
| 2 | Manh nha (Emerging) | Các lần thử lại và các dự phòng cơ bản được triển khai cho các phụ thuộc quan trọng nhất. Các buổi rà soát sau sự cố (post-incident reviews) được tổ chức cho các sự cố đáng kể và các phát hiện được lưu trữ, dù chúng không được lan truyền có hệ thống vào các runbook. Một tập ban đầu các quy trình phá kính (break-glass) được tài liệu hóa cho các quy trình kinh doanh có tác động cao nhất, và quản trị thay đổi bao phủ rõ ràng các Prompt, Tools, và [mô hình nền tảng (foundation models)](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) của agent. |
| 3 | Được định nghĩa (Defined) | Các ngắt tự động, các chuỗi dự phòng, và các luồng phục hồi bao phủ mọi phụ thuộc bên ngoài và được giám sát trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html). Tri thức vận hành được nắm bắt trong một hệ thống tập trung, tìm kiếm được như [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), với các buổi rà soát sau sự cố cấp các mục trực tiếp. Quản trị thay đổi phân loại các thay đổi agent theo phạm vi kỹ thuật và tác động kinh doanh và định tuyến các phê duyệt tương ứng, và các runbook phá kính được diễn tập qua các bài tập tabletop. |
| 4 | Chủ động (Proactive) | Các mục tiêu thời gian phục hồi được xác định cho mỗi kịch bản lỗi, được theo dõi trong các dashboard, và được kiểm định qua các bài tập kỹ thuật hỗn loạn (chaos engineering) thường xuyên. Các buổi rà soát sự phù hợp kinh doanh chạy theo một nhịp được xác định, và các ánh xạ agent-tới-quy-trình-kinh-doanh sinh ra các thông báo tự động qua [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) khi các quy trình hoặc chính sách thay đổi. Các buổi diễn tập phá kính thực thi đầu-cuối trong các môi trường phi sản xuất, các cập nhật runbook được gắn với các phát hiện diễn tập, và tri thức vận hành có các chủ sở hữu rõ ràng giữ cho các mục cập nhật. |
| 5 | Tối ưu (Optimized) | Phục hồi agent là tự chữa lành và liên tục được điều chỉnh dựa trên telemetry sản xuất, với các ngắt tự động, các dự phòng Model, và các chế độ suy giảm đa agent đều được điều chỉnh so với các kết quả đo được. Tri thức vận hành có thể truy vấn bằng ngôn ngữ tự nhiên qua các trợ lý nội bộ xây trên [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) và được duy trì liên tục như một phần của vận hành bình thường. Các vòng lặp phản hồi quản trị thay đổi rõ ràng dẫn dắt các cải tiến hạ tầng và quy trình kinh doanh. Mức độ sẵn sàng phá kính được đánh giá liên tục qua các buổi diễn tập được trang bị đo lường, và các bài học từ sự cố định hình cả phục hồi tự động lẫn các quy trình dự phòng thủ công trong lần lặp tiếp theo. |

## Các vấn đề thường gặp cần lưu ý

- Logic phục hồi được triển khai theo từng thành phần nhưng không bao giờ được kiểm thử kết hợp, nên các lỗi lan truyền trải qua nhiều thành phần chỉ được phát hiện trong các sự cố thực khi tác động kinh doanh đã đáng kể.
- Các buổi rà soát sau sự cố tạo ra các tài liệu được lưu trữ nhưng không bao giờ được chuyển thành các thay đổi runbook hoặc nền tảng, nên tổ chức trả chi phí học từ mỗi sự cố mà không cộng dồn giá trị.
- Các thay đổi agent được phê duyệt trên các tiêu chí thuần kỹ thuật trong khi các quy trình kinh doanh mà chúng hỗ trợ tiến hóa riêng, tạo ra trôi lệch âm thầm giữa hành vi agent và các quy tắc kinh doanh hiện tại.
- Các runbook phá kính và danh sách liên hệ được tạo một lần và không được bảo trì, nên đến khi cần đến chúng lại tham chiếu các hệ thống đã nghỉ, các Tools đã ngừng vận hành, hoặc những người đã rời đi.
- Các quy trình khẩn cấp được lưu trong các hệ thống phụ thuộc vào chính hạ tầng agent mà chúng được thiết kế để làm việc thay thế, khiến người vận hành không có tài liệu khi cần đến.

###### Các thực hành tốt

- [AGENTOPS07-BP01 Triển khai các cơ chế ứng phó và phục hồi tự động](agentops07-bp01.md)
- [AGENTOPS07-BP02 Thiết lập các hệ thống quản lý tri thức vận hành](agentops07-bp02.md)
- [AGENTOPS07-BP03 Bổ sung quản trị thay đổi để đáp ứng các cải tiến kỹ thuật và các yêu cầu kinh doanh](agentops07-bp03.md)
- [AGENTOPS07-BP04 Triển khai các runbook vận hành phá kính (break-glass)](agentops07-bp04.md)
