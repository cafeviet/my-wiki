# AGENTSUS02-BP03 Mở rộng các phụ thuộc dữ liệu, mạng và compute một cách phù hợp

Các khối công việc Agent có một hình thái mà các mặc định hạ tầng đa dụng không phù hợp — suy luận mang tính đột biến, thực thi Tools có độ dài biến thiên, và suy luận nhiều bước khó dự đoán. Điều chỉnh hosting, mạng và lưu trữ theo mẫu quan sát được thay vì một cực đại lý thuyết giữ cho hạ tầng tỷ lệ thuận với công việc dạng tác nhân.

**Kết quả mong muốn:**

- Các tiến trình Agent chạy trên hạ tầng serverless mở rộng theo nhu cầu thay vì cấp phát tĩnh cho tải đỉnh.
- Kết nối riêng được dùng nơi yêu cầu về bảo mật hoặc độ trễ biện minh cho điều đó, không phải mặc định cho mọi khối công việc.
- Hạ tầng Agent được triển khai gần các dịch vụ mà nó phụ thuộc, để giảm thiểu việc truyền dữ liệu xuyên-Region.
- Phản hồi dạng streaming được dùng cho các tương tác hướng người dùng để giảm dấu chân bộ nhớ và cải thiện thời gian đến token đầu tiên (time-to-first-token).
- Hiệu suất sử dụng được giám sát liên tục và việc cấp phát bám theo nhu cầu khối công việc thực tế.

**Các phản mẫu thường gặp (anti-patterns):**

- Áp các cấu hình hạ tầng đa dụng mà không phân tích các mẫu gọi suy luận mang tính đột biến và thời lượng thực thi Tools biến thiên đặc thù cho khối công việc Agent, tạo ra cấp phát dư thừa lãng phí hoặc cấp phát thiếu làm suy giảm hiệu năng.
- Duy trì cấp phát tĩnh bất kể nhu cầu, giảm khả năng hạ tầng thu hẹp trong các giai đoạn hoạt động thấp.
- Định kích cỡ cho các kịch bản cực đại lý thuyết thay vì điều chỉnh đúng kích cỡ theo nhu cầu thực tế, tạo ra hiệu suất sử dụng thấp trong vận hành thông thường.
- Triển khai hạ tầng Agent xa các dịch vụ mà nó phụ thuộc, tạo ra lưu lượng mạng xuyên-Region làm tăng độ trễ và chi phí truyền.

**Lợi ích khi áp dụng thực hành tốt này:**

- Mức tiêu thụ hạ tầng bám theo nhu cầu, thu hẹp khi Agent nhàn rỗi và mở rộng trong các giai đoạn đỉnh.
- Mức tiêu thụ năng lượng giữ tỷ lệ thuận với công việc mà Agent mang lại thay vì năng lực đỉnh lý thuyết của chúng.
- Kết nối riêng và việc đặt cùng Region (Region colocation) giảm độ dài đường mạng và độ trễ nơi điều đó quan trọng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Chạy các Agent trên hạ tầng serverless giải quyết phần lớn vấn đề cấp phát tĩnh ngay từ thiết kế. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) điều chỉnh compute đúng kích cỡ cho mỗi lần gọi với thực thi cô lập theo phiên, để phí tổn điều phối được giới hạn phạm vi trong phiên đang thực sự chạy. Không có đội hình các instance EC2 nhàn rỗi phải định kích cỡ theo nhu cầu trường hợp xấu nhất, vì đơn vị thực thi là lần gọi thay vì instance. Mặc định này giúp các khối công việc mang tính đột biến trở nên hợp túi tiền.

Kết nối riêng (private networking) là chuyện khớp mẫu kết nối với nhu cầu thực tế của khối công việc. Một số Agent xử lý dữ liệu nhạy cảm hoặc có yêu cầu độ trễ đủ chặt đến mức việc định tuyến qua internet công cộng là nút thắt cổ chai. Với các khối công việc đó, [VPC interface endpoints for Amazon Bedrock AgentCore (AWS PrivateLink)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html) thiết lập các đường riêng giảm độ trễ và giữ lưu lượng khỏi internet công cộng. Với các khối công việc không có các yêu cầu đó, PrivateLink thêm độ phức tạp vận hành mà không mang lợi ích tương xứng. Hãy mặc định endpoint công cộng và nâng cấp khối công việc lên PrivateLink khi bảo mật hoặc độ trễ đòi hỏi.

Triển khai hạ tầng Agent trong cùng AWS Region với các endpoint Amazon Bedrock và các dịch vụ AgentCore được truy cập thường xuyên giảm phí tổn truyền dữ liệu xuyên-Region vốn cộng dồn qua hàng nghìn lần gọi mỗi ngày. Về tính khả dụng, [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) phân phối các yêu cầu Model nền qua các Region. Điều này mang tính bổ trợ chứ không mâu thuẫn. Dùng cross-Region inference cho failover và năng lực đột biến, đồng thời giữ đường dữ liệu chính ở địa phương.

Phản hồi dạng streaming thay đổi hồ sơ bộ nhớ của các tương tác hướng người dùng. Không có streaming, Agent tích lũy toàn bộ phản hồi trong bộ nhớ trước khi trả về, nghĩa là bộ nhớ đỉnh tỷ lệ thuận với độ dài phản hồi. Với streaming, các token chảy khi chúng được sinh ra và bộ nhớ giữ trong giới hạn. Bật streaming trong AgentCore giảm dấu chân cho các tương tác dạng dài và cải thiện thời gian đến token đầu tiên cho người dùng. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) lộ dữ liệu hiệu suất sử dụng giữ cho việc cấp phát gắn với nhu cầu khối công việc thực tế.

### Các bước triển khai

- **Chạy các tiến trình Agent trên runtime serverless:** Triển khai lên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) để có mở rộng tự động và cô lập theo phiên, để năng lực thực thi mở rộng theo nhu cầu thay vì các ước lượng đỉnh.
- **Áp kết nối riêng nơi được biện minh:** Cấu hình [VPC interface endpoints for Amazon Bedrock AgentCore (AWS PrivateLink)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html) cho các khối công việc có yêu cầu bảo mật hoặc độ trễ xứng đáng. Mặc định endpoint công cộng cho các trường hợp còn lại.
- **Triển khai trong cùng Region với các phụ thuộc:** Đặt hạ tầng Agent trong Region lưu trữ các endpoint Amazon Bedrock và các dịch vụ AgentCore mà nó dùng nhiều nhất, và bật [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) cho tính khả dụng.
- **Bật streaming cho các phản hồi hướng người dùng:** Bật streaming của AgentCore để các token phản hồi chảy khi chúng được sinh ra, giảm dấu chân bộ nhớ và cải thiện thời gian đến token đầu tiên.
- **Xác thực hiệu suất sử dụng liên tục:** Theo dõi hiệu suất sử dụng hạ tầng qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và điều chỉnh việc cấp phát nơi nhu cầu quan sát được thấp hơn đáng kể so với mức đã cấp phát.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS02-BP01 Tối ưu hóa quản lý ngữ cảnh và sử dụng bộ nhớ](agentsus02-bp01.md)
- [AGENTSUS02-BP04 Đo lường và tối ưu hóa dấu chân môi trường của các khối công việc Agent](agentsus02-bp04.md)
- [SUS02-BP01 Scale workload infrastructure dynamically](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_user_a2.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html)
- [VPC interface endpoints for Amazon Bedrock AgentCore (AWS PrivateLink)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html)
- [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [AWS PrivateLink](https://aws.amazon.com/privatelink/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
