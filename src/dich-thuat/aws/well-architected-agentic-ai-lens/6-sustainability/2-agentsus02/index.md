# Điều chỉnh tài nguyên đúng kích cỡ

Các Agent điều chỉnh đúng kích cỡ các phụ thuộc của mình (bộ nhớ, cache, compute và mạng) mang lại giá trị tự động hóa mà không đặt tải không bền vững lên các hệ thống chúng phụ thuộc. Lưu lượng Agent tăng làm tăng tải lên các phụ thuộc này. Các khung (framework) bền vững giúp các hệ thống phụ thuộc mở rộng tỷ lệ thuận với lợi ích đạt được thông qua tự động hóa dạng tác nhân.

| AGENTSUS02: Làm thế nào để tôi thiết lập các khung bền vững cho các phụ thuộc của Agent? |
| --- |
|  |

## Mục tiêu năng lực

- Hạ tầng bộ nhớ và ngữ cảnh mở rộng theo nhu cầu ngữ cảnh thực tế thay vì các ước lượng trường hợp xấu nhất, với lưu trữ phân tầng và ngữ cảnh bền vững dùng chung tách biệt các đường truy cập nóng và lạnh.
- Cache được áp dụng tại mọi điểm tích hợp, và các cache dùng chung phân bổ công việc ra toàn đội hình Agent thay vì bị mỗi Agent khám phá lại một cách cô lập.
- Compute, mạng và lưu trữ mở rộng động theo các khối công việc Agent mang tính đột biến, thu hẹp trong các giai đoạn yên ắng và mở rộng trong các đỉnh mà không cần can thiệp thủ công.
- Các lựa chọn về Region và kết nối là có chủ ý, để lưu lượng nằm gần các dịch vụ mà Agent phụ thuộc, và các đường riêng (private path) được dùng nơi bảo mật hoặc độ trễ biện minh cho điều đó.
- Tác động môi trường được đo lường song song với các chỉ số vận hành, và các khối công việc có thể trì hoãn được lập lịch và bố trí theo hướng nhận biết carbon (carbon-awareness) để giảm dấu chân mà không ảnh hưởng đến hiệu năng hướng người dùng.

## Các mức độ trưởng thành

Các mức này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc điều chỉnh tài nguyên đúng kích cỡ nói chung.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Bộ nhớ, cache và hạ tầng của Agent chạy mà không điều chỉnh đúng kích cỡ có chủ ý. Bộ nhớ phình vô giới hạn, cache bị cô lập cho từng Agent nếu chúng tồn tại, và compute được cấp phát tĩnh cho nhu cầu đỉnh. Tác động môi trường không được đo lường, và việc bố trí Region bị coi là chuyện phụ. |
| 2 | Mới nổi (Emerging) | Các nhóm đã áp dụng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) với các chính sách lưu giữ cơ bản và đã bật [Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) cho các system prompt ổn định. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) được dùng cho một số Agent, và [AWS Sustainability](https://docs.aws.amazon.com/sustainability/latest/userguide/what-is-sustainability.html) đã được bật để báo cáo nhưng chưa thông tin cho các quyết định thiết kế. |
| 3 | Đã định hình (Defined) | Bộ nhớ phân tầng với ngữ cảnh bền vững dùng chung qua các namespace của [AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) là mặc định cho các hệ thống đa Agent. Các cache dùng chung được lộ qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) phân bổ công việc ra toàn đội hình. Caching token trong [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) giảm việc xác thực thông tin đăng nhập lặp lại. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) theo dõi các mẫu truy cập bộ nhớ, tỷ lệ hit của cache và các chỉ số hiệu quả, và một đường cơ sở môi trường 30 ngày đã được thiết lập. |
| 4 | Chủ động (Proactive) | Việc mở rộng hạ tầng, bố trí Region và kết nối riêng qua [VPC interface endpoints](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html) được điều khiển bởi các mẫu quan sát được. Nén ngữ cảnh, truy xuất ngữ nghĩa qua [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) và phản hồi dạng streaming là chuẩn mực. Các khối công việc có thể trì hoãn chạy ngoài giờ cao điểm, và [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) định tuyến các khối công việc batch tới các Region có hồ sơ năng lượng thuận lợi nơi độ trễ cho phép. Các bảng điều khiển bền vững kết hợp các chỉ số vận hành và carbon được rà soát theo nhịp định kỳ. |
| 5 | Tối ưu (Optimized) | Các tầng bộ nhớ, chính sách cache và việc cấp phát hạ tầng được hiệu chỉnh liên tục từ telemetry thay vì qua rà soát định kỳ. Dấu chân môi trường là một đầu vào thiết kế hạng nhất cho mọi khối công việc Agent mới, và các cải tiến hiệu quả cộng dồn tuần này qua tuần khác khi độ bao phủ mở rộng. Tổ chức đóng góp lại các mẫu về chi phí suy luận và tính bền vững cho các cộng đồng thực hành của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm xây dựng kiến trúc bộ nhớ phẳng mà không có lưu trữ phân tầng, nên ngữ cảnh truy cập thường xuyên phải cạnh tranh với dữ liệu lưu trữ (archival) cùng một tầng và chi phí truy xuất tăng theo mỗi phiên mới.
- Các tổ chức coi mỗi thực thể Agent như một hệ thống cô lập với cache riêng, bỏ lỡ việc phân bổ toàn-đội-hình vốn biến một lần hit cache thành khoản tiết kiệm cho mọi Agent hỏi cùng câu hỏi.
- Hạ tầng giữ cấp phát tĩnh cho nhu cầu trường hợp xấu nhất, nên hiệu suất sử dụng thấp trong vận hành thông thường và việc thu hẹp động không bao giờ xảy ra.
- Việc bố trí Region bỏ qua nơi các dịch vụ truy cập thường xuyên tồn tại, nên lưu lượng Agent vượt Region một cách không cần thiết và thêm cả độ trễ lẫn truyền dữ liệu vào mỗi lần gọi.
- Các tuyên bố bền vững được đưa ra mà không có đường cơ sở hay theo dõi xu hướng, nên công việc tối ưu hóa không thể được xác thực và các khối công việc có thể trì hoãn vẫn chạy trong giờ cao điểm cùng với lưu lượng hướng người dùng.

###### Các thực hành tốt

- [AGENTSUS02-BP01 Tối ưu hóa quản lý ngữ cảnh và sử dụng bộ nhớ](agentsus02-bp01.md)
- [AGENTSUS02-BP02 Thiết lập các chiến lược caching Agent hiệu quả](agentsus02-bp02.md)
- [AGENTSUS02-BP03 Mở rộng các phụ thuộc dữ liệu, mạng và compute một cách phù hợp](agentsus02-bp03.md)
- [AGENTSUS02-BP04 Đo lường và tối ưu hóa dấu chân môi trường của các khối công việc Agent](agentsus02-bp04.md)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
