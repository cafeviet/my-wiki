# AGENTSUS01-BP04 Điều chỉnh các đường dẫn xử lý nhận thức một cách phù hợp

Suy luận Model nền (foundation model inference) là thao tác tốn năng lượng nhất trong một quy trình Agent, và nó chạy hàng trăm hoặc hàng nghìn lần mỗi ngày. Khớp kích cỡ Model, độ sâu truy xuất và phạm vi bộ nhớ với độ phức tạp thực tế của tác vụ giữ cho mức tiêu thụ tài nguyên nhận thức tỷ lệ thuận với giá trị mang lại, thay vì mặc định mọi lệnh gọi tới Model lớn nhất có sẵn.

**Kết quả mong muốn:**

- Bạn có định tuyến Model phân tầng, để mỗi tác vụ đi tới Model nhỏ nhất đáp ứng ngưỡng chất lượng của nó.
- Độ sâu truy xuất và kích thước cửa sổ ngữ cảnh được điều chỉnh theo phạm vi độ phức tạp của tác vụ, để các tác vụ thường quy không mang theo phí tổn truy xuất của suy luận phức tạp.
- Trích xuất đa phương thức (multimodal) dùng các dịch vụ chuyên dụng khi phù hợp, không dùng Model thị giác thô cho mọi tài liệu.
- Các Agent hoạt động trong ngân sách token và giới hạn tốc độ được thực thi ở lớp runtime cho mỗi Agent.

**Các phản mẫu thường gặp (anti-patterns):**

- Định tuyến mọi yêu cầu tới Model nền lớn nhất mà không kiểm tra xem một Model nhỏ hơn hay một phản hồi từ cache có đáp ứng được ngưỡng chất lượng không, vốn là cơ hội đơn lẻ lớn nhất để giảm năng lượng.
- Cho phép các Agent gọi Model mà không có ngân sách token hay giới hạn đồng thời, cho phép các Agent đơn lẻ tiêu thụ tài nguyên bất cân xứng dưới tải.
- Cấu hình retrieval-augmented generation trả về cùng độ sâu ngữ cảnh cho mọi tác vụ bất kể độ phức tạp, tạo ra các cửa sổ ngữ cảnh quá cỡ và các truy vấn vector dư thừa.
- Gửi ảnh tài liệu thô tới các Model thị giác lớn khi một dịch vụ trích xuất chuyên dụng sẽ trả về cùng dữ liệu có cấu trúc với chi phí compute chỉ bằng một phần nhỏ.

**Lợi ích khi áp dụng thực hành tốt này:**

- Mức tiêu thụ tài nguyên nhận thức mở rộng theo nhu cầu tác vụ thay vì theo số lượng Agent, nên chi phí năng lượng khi mở rộng đội hình Agent giữ tỷ lệ thuận với công việc chúng làm.
- Ngân sách token cho mỗi Agent giúp ngăn một Agent làm cạn kiệt tài nguyên của phần còn lại của đội hình dưới tải.
- Điều chỉnh đúng kích cỡ trên hàng trăm lệnh gọi Model mỗi ngày cộng dồn thành khoản tiết kiệm năng lượng đáng kể mà không thể thấy được trên cơ sở từng lệnh gọi đơn lẻ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Trụ cột Hiệu quả Hiệu năng (Performance Efficiency) đề cập việc chọn Model phân tầng trong [AGENTPERF02-BP02 Implement task-appropriate model selection strategies](../../4-performance-efficiency/2-agentperf02/agentperf02-bp02.md). Trụ cột Tối ưu Chi phí (Cost Optimization) đề cập việc xếp tầng Model (model cascading) trong [AGENTCOST02-BP01 Architect tiered model selection for cost-performance optimization](../../5-cost-optimization/2-agentcost02/agentcost02-bp01.md). Góc nhìn bền vững bổ sung một điều: mục tiêu không phải chỉ là độ trễ hay chi phí đơn lẻ, mà là tổng dấu chân năng lượng và compute trên mỗi đơn vị giá trị kinh doanh mang lại. Một phân loại tác vụ xếp hạng các yêu cầu theo độ phức tạp suy luận, rồi định tuyến chúng tới các Model [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) có kích cỡ phù hợp, giúp định tuyến được điều khiển bởi dữ liệu thay vì mặc định-chọn-lớn-nhất.

Theo dõi số lần hoàn thành tác vụ thành công chia cho tổng compute tiêu thụ cho một tín hiệu tốt hơn so với từng chỉ số đơn lẻ. Một quy trình cho ra câu trả lời đúng ngay lần đầu với một Model nhỏ thì bền vững hơn một quy trình dùng Model lớn nhất mà vẫn phải thử lại. Gắn tag cho các lệnh gọi để tỷ lệ này có thể được tính theo từng danh mục tác vụ, và dùng nó để dịch chuyển các ngưỡng định tuyến theo thời gian. Với [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html), bạn có thể phân phối các yêu cầu không cấp bách tới các Region có hồ sơ năng lượng thuận lợi khi ràng buộc độ trễ cho phép.

Độ sâu truy xuất trong [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) nên là một tham số của tác vụ, không phải một hằng số. Một câu hỏi thường quy với câu trả lời có giới hạn không cần cùng độ trải truy xuất (fanout) như một tác vụ suy luận phức tạp. Truy xuất quá cỡ lãng phí các truy vấn vector và làm phình các cửa sổ ngữ cảnh. Với các khối công việc nặng về tài liệu, [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) trích xuất dữ liệu có cấu trúc từ tài liệu với chi phí compute chỉ bằng một phần nhỏ so với việc định tuyến ảnh thô qua một Model thị giác. Con đường rẻ hơn thường là con đường tốt hơn.

Cấu hình AgentCore Memory với TTL phân tầng và cắt tỉa tự động để bộ nhớ làm việc không phình vô hạn định, và thêm caching ngữ nghĩa (semantic caching) để các truy vấn tương tự phục vụ phản hồi từ cache thay vì gọi lại lặp lại. Thực thi ngân sách token và giới hạn đồng thời cho mỗi Agent qua các ràng buộc thực thi của AgentCore Runtime. Đo mức tiêu thụ thực tế qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để các ngưỡng luôn gắn với thực tế quan sát được.

### Các bước triển khai

- **Triển khai định tuyến Model phân tầng:** Theo các mẫu trong [AGENTPERF02-BP02 Implement task-appropriate model selection strategies](../../4-performance-efficiency/2-agentperf02/agentperf02-bp02.md) và [AGENTCOST02-BP01 Architect tiered model selection for cost-performance optimization](../../5-cost-optimization/2-agentcost02/agentcost02-bp01.md) để hướng các tác vụ tới các Model [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) có kích cỡ phù hợp dựa trên một phân loại độ phức tạp.
- **Điều chỉnh độ sâu truy xuất theo độ phức tạp của tác vụ:** Tham số hóa truy xuất của [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) để các truy vấn vector và token ngữ cảnh mở rộng theo công việc. Dùng giới hạn chặt hơn cho các tác vụ thường quy và chỉ truy xuất rộng hơn cho suy luận phức tạp.
- **Định tuyến trích xuất tài liệu tới các dịch vụ chuyên dụng:** Với các tác vụ đa phương thức, dùng [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) thay vì gửi ảnh thô qua các Model thị giác lớn.
- **Áp dụng chính sách vòng đời bộ nhớ:** Cấu hình AgentCore Memory với TTL phân tầng và cắt tỉa tự động để bộ nhớ làm việc giữ trong giới hạn và các mục cũ được loại bỏ tự động.
- **Thực thi ngân sách và theo dõi hiệu quả:** Đặt ngân sách token và giới hạn tốc độ cho mỗi Agent qua các ràng buộc thực thi của AgentCore Runtime, và theo dõi số lần hoàn thành thành công trên mỗi đơn vị compute tiêu thụ qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để điều chỉnh các ngưỡng định tuyến từ dữ liệu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF02-BP02 Implement task-appropriate model selection strategies](../../4-performance-efficiency/2-agentperf02/agentperf02-bp02.md)
- [AGENTCOST02-BP01 Architect tiered model selection for cost-performance optimization](../../5-cost-optimization/2-agentcost02/agentcost02-bp01.md)
- [AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh](agentsus01-bp01.md)
- [SUS02-BP02 Align SLAs with sustainability goals](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_user_a3.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock model support](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [Effective cost optimization strategies for Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Agentic AI patterns and workflows on AWS - Routing dynamic dispatch patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/routing.html)

**Các video liên quan:**

- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)

**Các ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Các dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
