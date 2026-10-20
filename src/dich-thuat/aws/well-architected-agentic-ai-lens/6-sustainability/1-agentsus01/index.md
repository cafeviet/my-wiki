# Khả năng tái sử dụng tài nguyên

Các tổ chức đầu tư vào hạ tầng Agent có thể tái sử dụng sẽ tăng tốc mọi dự án tiếp theo trong khi giảm mức tiêu thụ tài nguyên tích lũy. Khi Agent được sử dụng nhiều hơn, cơ hội tối ưu hóa, chia sẻ và tái sử dụng tài nguyên Agent càng tăng. Tài nguyên dùng chung tạo ra gánh nặng nhỏ hơn cho toàn bộ kiến trúc, mang lại một quy trình bền vững hơn.

| AGENTSUS01: Làm thế nào để bạn xây dựng các khung (framework) bền vững và có thể lặp lại nhằm quản lý compute, bộ nhớ và các tài nguyên Agent chia sẻ được khác? |
| --- |
|  |

## Mục tiêu năng lực

- Mỗi Agent gói gọn một năng lực đơn lẻ, được định nghĩa rõ ràng, với ranh giới tài nguyên tường minh; và những ranh giới đó lan xuống qua cơ chế ủy quyền (delegation) tới các Agent con, để không cây con nào tiêu thụ tài nguyên mà không có mức trần xác định.
- Các mẫu quy trình lặp lại (truy xuất, xác thực, biến đổi và ra quyết định) tồn tại dưới dạng các thành phần có tham số hóa, có thể khám phá được, để các nhóm ghép nối lại thay vì xây lại cho mỗi trường hợp sử dụng mới.
- Hạ tầng chung như connection pool, cache, xác thực và truy cập Model nền (foundation model) được hợp nhất thành các dịch vụ dùng chung, để năng lực mở rộng theo tổng nhu cầu tổng hợp thay vì theo số lượng thực thể Agent.
- Các đường dẫn nhận thức được điều chỉnh đúng kích cỡ theo độ phức tạp của tác vụ, với lựa chọn Model, độ sâu truy xuất và phạm vi bộ nhớ đều khớp với nhu cầu thực tế thay vì mặc định chọn tùy chọn lớn nhất hoặc rộng nhất.
- Các khối công việc chạy dài và tiên phong (frontier) chạy dựa trên các đặc tả tường minh bao trùm tiêu chí thành công, ngân sách tài nguyên và điều kiện kết thúc, với các điểm kiểm tra (checkpoint) giúp khoản đầu tư compute có thể được xem xét đối chiếu với giá trị kinh doanh.

## Các mức độ trưởng thành

Các mức này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với khả năng tái sử dụng tài nguyên nói chung.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Agent được cấp phát cho các kịch bản trường hợp xấu nhất mà không có hợp đồng tài nguyên tường minh, và các Agent con được ủy quyền không kế thừa ràng buộc nào. Quy trình được xây lại từ đầu cho mỗi trường hợp sử dụng, không có thư viện mẫu dùng chung hay danh mục thành phần tái sử dụng được. Mỗi Agent tự thiết lập kết nối riêng tới các dịch vụ bên ngoài, nhân bản hạ tầng qua các thực thể. Lệnh gọi Model nền mặc định chọn Model lớn nhất có sẵn, và các Agent chạy dài chạy mà không có đặc tả hay điểm kiểm tra. |
| 2 | Mới nổi (Emerging) | Các nhóm bắt đầu phân rã quy trình thành các Agent chuyên biệt với giới hạn timeout và bộ nhớ cơ bản được cấu hình cho mỗi Agent. Một số mẫu quy trình lặp lại đã được trích xuất thành template, dù việc khám phá còn không chính thức. Một vài dịch vụ dùng chung (thường là một cache trung tâm hoặc một đường xác thực chung) đang chạy production. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) được bật cho hầu hết các Agent production, và các đợt rà soát thủ công mức tiêu thụ tài nguyên diễn ra theo nhịp định kỳ. |
| 3 | Đã định hình (Defined) | Agent chuyên biệt là mẫu mặc định, được triển khai trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) với ranh giới tài nguyên tường minh, và các mẫu quy trình tái sử dụng được công bố qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) dưới dạng các công cụ MCP có thể khám phá. Các cache dùng chung như [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/BestPractices.html) là chuẩn mực, và xác thực chạy qua [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html). Định tuyến Model phân tầng và truy xuất có phạm vi dựa trên [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) đã được áp dụng cho hầu hết quy trình, và các Agent chạy dài chạy với đặc tả được ghi chép. |
| 4 | Chủ động (Proactive) | Ngân sách tài nguyên được thực thi ở lớp điều phối (orchestration) thông qua [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html) và AgentCore Policies thay vì dựa vào sự tự tiết chế của Agent. Thư viện mẫu được duy trì, quản trị và đo đạc để một tối ưu hóa đơn lẻ lan tỏa đến mọi quy trình tiêu dùng. [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) phân phối lưu lượng Model, và [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) xử lý trích xuất tài liệu thay cho các Model thị giác lớn. Các Agent frontier chạy với ngân sách xếp tầng, đánh giá dựa trên điểm kiểm tra, và lưu giữ trạng thái qua [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html). |
| 5 | Tối ưu (Optimized) | Ranh giới tài nguyên, ngưỡng định tuyến, chính sách lưu giữ và template đặc tả được hiệu chỉnh liên tục từ dữ liệu [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) thay vì qua các chu kỳ rà soát thủ công. Dịch vụ dùng chung và thư viện mẫu là điểm ghép nối mặc định cho các quy trình mới, và việc phát triển mới không tái sử dụng thành phần hiện có là ngoại lệ. Hiệu quả sử dụng tài nguyên (số lần hoàn thành thành công trên mỗi đơn vị compute) là một chỉ số hạng nhất song song với chi phí và độ trễ, và tổ chức đóng góp lại các mẫu tái sử dụng cùng phép đo bền vững cho các cộng đồng thực hành (community of practice) của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm cấp phát Agent cho kịch bản trường hợp xấu nhất và để Agent cha ủy quyền công việc cho Agent con mà không xếp tầng ngân sách tài nguyên, nên tình trạng tiêu thụ mất kiểm soát ở một cây con chỉ được phát hiện sau hóa đơn hàng tháng.
- Logic quy trình lặp lại bị xây lại cho mỗi trường hợp sử dụng mới, tích lũy mã trùng lặp và nợ kiểm thử trong khi bỏ lỡ lợi ích kiến trúc tái tạo được: chỉ tối ưu một mẫu dùng chung một lần rồi lan tỏa cải tiến khắp nơi.
- Mỗi Agent tự thiết lập kết nối, cache và luồng xác thực riêng thay vì tiêu dùng dịch vụ dùng chung, nên chi phí hạ tầng tăng tuyến tính theo số lượng Agent thay vì theo tổng nhu cầu tổng hợp.
- Mọi yêu cầu đều được định tuyến tới Model nền lớn nhất, truy xuất không giới hạn trên các knowledge base, và bộ nhớ phình to mà không được cắt tỉa, nên phí tổn nhận thức trở nên bất cân xứng với giá trị mà mỗi tương tác mang lại.
- Các Agent chạy dài và frontier chạy mà không có đặc tả, ngân sách tài nguyên hay điểm kiểm tra, nên chúng thăm dò các nhánh không liên quan và tiêu tốn compute kéo dài mà không có cơ chế trách nhiệm gắn kết quả với giá trị kinh doanh.

###### Các thực hành tốt

- [AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh](agentsus01-bp01.md)
- [AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được](agentsus01-bp02.md)
- [AGENTSUS01-BP03 Tối ưu hóa việc sử dụng tài nguyên thông qua dịch vụ dùng chung](agentsus01-bp03.md)
- [AGENTSUS01-BP04 Điều chỉnh các đường dẫn xử lý nhận thức một cách phù hợp](agentsus01-bp04.md)
- [AGENTSUS01-BP05 Áp dụng tác vụ theo hướng đặc tả (specification-driven) cho các Agent frontier và quy trình chạy dài](agentsus01-bp05.md)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
