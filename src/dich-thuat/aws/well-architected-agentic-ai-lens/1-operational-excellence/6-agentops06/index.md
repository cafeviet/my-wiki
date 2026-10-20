# Các khung kiểm thử, đánh giá và kiểm định

Các quy trình kiểm thử và đánh giá có hệ thống xác nhận chất lượng, độ tin cậy, và sự phù hợp của agent với các mục tiêu kinh doanh thông qua cả kiểm thử phần mềm truyền thống lẫn đánh giá chất lượng đặc thù AI. Không có một khung bao phủ mọi giai đoạn của vòng đời agent, các hồi quy chất lượng từ các thay đổi Prompt, cập nhật Tools, hoặc cập nhật Model sẽ đến được người dùng trước khi bất kỳ ai nhận ra.

| AGENTOPS06: Bạn triển khai các khung kiểm thử, đánh giá và kiểm định như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các agent được kiểm định ở mọi lớp, từ các thành phần biệt lập đến toàn bộ luồng công việc chạy ở chế độ bóng sản xuất (production-shadow), trước khi các thay đổi đến được người dùng.
- Các chỉ số về chất lượng, an toàn, hiệu quả, và sự phù hợp kinh doanh được đo liên tục so với các mốc chuẩn (benchmark) được kiểm soát phiên bản, với các hồi quy được bộc lộ ngay khi chúng xuất hiện.
- Quản trị thay đổi tỷ lệ thuận với rủi ro. Các thay đổi rủi ro thấp đi qua các cổng tự động, và các thay đổi rủi ro cao nhận rà soát của SME và chủ sở hữu kinh doanh.
- Các tập dữ liệu đánh giá, Prompt, và các rubric chấm điểm được đánh phiên bản và giữ cập nhật khi các năng lực agent và các trường hợp sử dụng tiến hóa.
- Các đường quay lui cho Prompt, Tools, Model, và các phiên bản agent được xác định, diễn tập, và nối với chính telemetry phát hiện các vi phạm ngưỡng chất lượng.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với các khung kiểm thử, đánh giá và kiểm định như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Kiểm thử là một lần và tập trung vào luồng thuận lợi. Các nhóm dựa vào việc kiểm tra thủ công các đầu ra agent và các phép khẳng định khớp chính xác không thường xuyên, bỏ lỡ các lỗi chỉ xuất hiện trong các đường dùng Tools, đa agent, hoặc lưu lượng sản xuất. Không tồn tại các chỉ số đánh giá chính thức ngoài các smoke test tại thời điểm triển khai. Các phê duyệt là email hoặc chat phi chính thức, và quay lui là một lần triển khai lại thủ công, chưa được kiểm thử một tài liệu cũ hơn. |
| 2 | Manh nha (Emerging) | Các unit test và integration test tồn tại cho các thành phần suy luận, Tools, và bộ nhớ lõi, và chạy trong một pipeline [CI/CD](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html). Đánh giá được thực hiện tại các mốc then chốt bằng [Amazon Bedrock model evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) và các tiêu chí chấp nhận được tài liệu hóa. Các luồng phê duyệt phân biệt ít nhất hai bậc rủi ro, và các quy trình quay lui được tài liệu hóa theo từng agent. Độ bao phủ các trường hợp biên, các đầu vào đối kháng (adversarial), và các lần chạy bóng sản xuất vẫn chắp vá. |
| 3 | Được định nghĩa (Defined) | Một kim tự tháp kiểm thử bốn lớp, bao phủ unit, integration, đầu-cuối, và bóng (shadow), là chuẩn xuyên các nhóm agent, với [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) cung cấp các bộ đánh giá dựng sẵn như các cổng chất lượng chuẩn hóa. Đánh giá liên tục theo dõi chất lượng đầu ra, an toàn, hiệu quả, và sự phù hợp kinh doanh theo thời gian, và các luồng phê duyệt phân bậc rủi ro định tuyến các thay đổi theo phạm vi tác động. Các quy trình quay lui được tự động hóa qua các tác nhân kích hoạt pipeline và được diễn tập thường xuyên. |
| 4 | Chủ động (Proactive) | Kiểm thử bóng chạy song song với sản xuất cho mọi bản phát hành đáng kể, với các phân kỳ được phân loại qua các vết [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) tương quan với các điểm đánh giá. Đánh giá trực tuyến (online) lấy mẫu các tương tác trực tiếp liên tục, với các ngưỡng kích hoạt quay lui tự động qua các cảnh báo triển khai. Các phê duyệt phân bậc rủi ro bao gồm các chủ sở hữu kinh doanh và SME cho các thay đổi làm tăng mức tự chủ, và các tập dữ liệu đánh giá tiến hóa tự động từ dữ liệu sự cố và phản hồi. Các chỉ số chất lượng, an toàn, và kinh doanh được theo dõi qua các phiên bản agent như các tài liệu phát hành hạng nhất. |
| 5 | Tối ưu (Optimized) | Kiểm thử, đánh giá, và kiểm định là một hệ thống tích hợp, tự chữa lành. Các bộ đánh giá tùy chỉnh mã hóa các tiêu chuẩn chất lượng đặc thù tổ chức và được đánh phiên bản cùng các agent chúng bao phủ. Policy-as-code diễn đạt các quy tắc phân bậc rủi ro và định tuyến phê duyệt, và quay lui đúng đắn có thể chứng minh được, được kiểm thử theo quý qua các bài tập game-day. Chấm điểm đánh giá, so sánh bóng, và phản hồi của con người cấp cho một vòng lặp cải tiến liên tục cập nhật các tập dữ liệu, Prompt, và Guardrails một cách tự động. Tổ chức đóng góp các mẫu và các bộ đánh giá trở lại các cộng đồng nội bộ và các diễn đàn bên ngoài. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm dừng lại ở các unit test tất định và bỏ qua kiểm thử bóng trên lưu lượng thực, nên các agent được đưa ra với hành vi chưa biết trên các trường hợp biên, các đầu vào đối kháng, và các phân bố dữ liệu sản xuất.
- Chất lượng được đo một lần tại thời điểm phát hành và không bao giờ được đo lại, nên trôi lệch dữ liệu, suy tàn Prompt (prompt decay), và các cập nhật Model thượng nguồn âm thầm xói mòn chất lượng đầu ra giữa các bản phát hành.
- Mọi thay đổi đi qua hoặc một hội đồng nặng nề hoặc một buổi rà soát đóng dấu cao su, vốn hoặc gây nghẽn các chỉnh sửa nhỏ hoặc cho qua các lần tăng tự chủ mà không có sự soi xét của SME.
- Các tập dữ liệu kiểm thử và đánh giá được tạo một lần và không bao giờ được làm mới, nên các điểm số vẫn xanh trong khi các chế độ lỗi thực tế không được phát hiện.
- Các quy trình quay lui nằm trong một runbook nhưng không bao giờ được diễn tập, nên lần thử thực tế đầu tiên trong lúc sự cố phát hiện ra các kho tài liệu bị hỏng, các quyền bị thiếu, hoặc các không khớp phiên bản Prompt và Tools.

###### Các thực hành tốt

- [AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp](agentops06-bp01.md)
- [AGENTOPS06-BP02 Đánh giá và theo dõi hiệu năng agent liên tục](agentops06-bp02.md)
- [AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh](agentops06-bp03.md)
