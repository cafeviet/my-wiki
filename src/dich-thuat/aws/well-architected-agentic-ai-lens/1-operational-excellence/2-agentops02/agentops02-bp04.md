# AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục

Các agent cải thiện đồng nhịp với việc sử dụng thực tế sẽ vượt trội hơn các agent bị đóng băng tại thời điểm triển khai. Một vòng lặp phản hồi vận hành tốt kết nối các tín hiệu chất lượng, phản hồi người dùng, các dấu hiệu hành vi, và các kết quả kinh doanh với các hành động cải tiến được ưu tiên.

**Kết quả mong muốn:**

- Bạn thu thập và tương quan dữ liệu hiệu năng agent, phản hồi người dùng, và chỉ số kết quả kinh doanh một cách có hệ thống, không phải qua các khảo sát tùy ứng.
- Các vòng lặp phản hồi vận hành liên tục, phát hiện các xu hướng chất lượng gần thời gian thực thay vì qua các buổi rà soát theo quý.
- Các hành động cải tiến được theo dõi từ khi xác định đến khi triển khai và kiểm định.
- Các tín hiệu phản hồi có thể quy về các phiên bản agent cụ thể, để các nhóm biết cải tiến nào đang phản ứng với vấn đề nào.

**Các phản mẫu thường gặp (anti-patterns):**

- Thu thập phản hồi người dùng (như thích/không thích hoặc xếp hạng) mà không kết nối nó với các hành vi agent hay phiên bản Prompt cụ thể, khiến không thể quy các thay đổi chất lượng về các cải tiến.
- Chỉ dựa vào các buổi rà soát thủ công định kỳ thay vì xử lý phản hồi tự động liên tục, cho phép suy giảm chất lượng tồn tại nhiều tuần trước khi được phát hiện.
- Thu thập dữ liệu phản hồi mà không có một quy trình xác định để biến các insight thành hành động cải tiến, tạo ra một backlog tín hiệu ngày càng tăng không bao giờ chuyển thành thay đổi agent.
- Trộn các loại tín hiệu vào một rổ duy nhất, khiến một đợt tăng vọt các cảnh báo chất lượng tự động lấn át một số ít báo cáo người dùng nghiêm trọng đáng được chú ý ngay lập tức.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phản hồi có cấu trúc biến dữ liệu vận hành thành một nguồn tín hiệu cải tiến liên tục, để các agent tiến hóa theo cách sử dụng thực tế thay vì đứng yên sau khi triển khai.
- Ưu tiên hóa dựa trên phản hồi hướng nỗ lực phát triển tới các thay đổi có tác động đo lường được lớn nhất.
- Theo dõi xu hướng theo thời gian bộc lộ các mẫu (trôi lệch dữ liệu, trôi lệch khái niệm, và trôi lệch phạm vi) giúp định hướng tinh chỉnh có chủ đích thay vì chỉnh sửa tản mạn.
- Kiểm định cải tiến mang lại cho nhóm bằng chứng rằng mỗi thay đổi đã đem lại lợi ích như kỳ vọng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Các vòng lặp phản hồi nên theo dõi nhiều hơn một tín hiệu để thực sự hữu ích.

Các chỉ số chất lượng tự động từ [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) và [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) cho thấy các dịch chuyển đo lường được trong chất lượng đầu ra.

Để theo dõi cảm nhận chủ quan, hãy cân nhắc kiểm tra:

- Phản hồi tường minh của người dùng
- Thích/không thích
- Xếp hạng
- Bình luận dạng văn bản tự do

Để xác định xem người dùng có tìm thấy điều họ cần hay không, hãy cân nhắc kiểm tra:

- Các tín hiệu hành vi ngầm định
- Bỏ dở tác vụ
- Tỷ lệ leo thang
- Các mẫu thử lại

Để xác định xem agent có bám sát các mục tiêu của tổ chức bạn hay không, hãy cân nhắc kiểm tra:

- Các chỉ số kết quả kinh doanh
- Tỷ lệ chuyển đổi
- Thời gian giải quyết
- Mức độ hài lòng của khách hàng

Mỗi kênh bắt được các lỗi mà các kênh khác bỏ sót, nên việc thu thập cả bốn con đường chỉ số này và định tuyến chúng qua một đường ống xử lý hợp nhất là thiết kế khả thi tối thiểu.

Hãy dùng thu nạp theo sự kiện (event-driven ingestion) để giữ đường ống của bạn có khả năng mở rộng. [Amazon EventBridge](https://aws.amazon.com/eventbridge/) hoặc một event bus tương đương nhận các sự kiện phản hồi từ mọi kênh và định tuyến chúng tới một tầng xử lý phân loại theo loại (vấn đề chất lượng, khoảng trống năng lực, lỗi Tools, lệch chuẩn hành vi), mức độ nghiêm trọng, và thành phần bị ảnh hưởng. Lưu phản hồi đã xử lý trong [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) với chỉ mục theo agent, loại phản hồi, và khoảng thời gian giúp phân tích xu hướng và truy vấn trở nên khả thi thay vì gian nan.

Hãy cân nhắc triển khai định tuyến theo mức độ nghiêm trọng để tránh làm ngập các nhóm với cảnh báo liên tục. Phản hồi mức độ nghiêm trọng cao, một người dùng báo cáo agent đã làm điều gì đó nguy hiểm, hoặc một sự sụt giảm đột ngột trong một chỉ số chất lượng sẽ đi thẳng tới hàng đợi rà soát tức thời. Phản hồi mức độ nghiêm trọng thấp hơn được tổng hợp thành các buổi rà soát theo lô, bộc lộ các mẫu qua nhiều ngày thay vì đòi hỏi phản ứng ngay lập tức.

Hãy xác minh rằng bạn có một luồng theo dõi cải tiến hiệu quả. Để giữ cho quy trình phản hồi hữu ích và có thể hành động, bạn cần:

- Một luồng công việc bền vững
- Xác định
- Phân tích nguyên nhân gốc
- Thiết kế cải tiến
- Triển khai
- Kiểm định
- Tương quan tới phản hồi cụ thể đã thúc đẩy hành động
- Các chỉ số được so sánh trước và sau mỗi thay đổi

Kiểm định là bước thường bị bỏ qua nhất, và cũng là bước cho nhóm biết một cải tiến có thực sự hiệu quả hay không.

Các dashboard giúp bạn giải quyết tầm nhìn về cả phản hồi lẫn cải tiến. Các xu hướng phản hồi bên cạnh các kết quả cải tiến cung cấp một góc nhìn rõ ràng về việc quỹ đạo chất lượng của agent đang đi lên, đi ngang, hay đi xuống, và cải tiến nào chịu trách nhiệm cho mỗi điểm uốn.

### Các bước triển khai

- **Triển khai thu thập phản hồi đa kênh:** Bao phủ các chỉ số chất lượng tự động (qua [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) và [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)), phản hồi tường minh của người dùng, các tín hiệu hành vi ngầm định, và các chỉ số kết quả kinh doanh.
- **Phân loại phản hồi ngay khi thu nạp:** Phân loại theo loại (vấn đề chất lượng, khoảng trống năng lực, lỗi Tools, lệch chuẩn hành vi), mức độ nghiêm trọng, và thành phần bị ảnh hưởng.
- **Lưu phản hồi đã xử lý để phân tích xu hướng:** Dùng [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) đánh chỉ mục theo agent, loại phản hồi, và khoảng thời gian.
- **Định tuyến theo mức độ nghiêm trọng:** Gửi phản hồi mức độ nghiêm trọng cao tới các hàng đợi rà soát tức thời qua [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html). Tổng hợp các mục mức độ nghiêm trọng thấp hơn để rà soát theo lô.
- **Theo dõi các cải tiến đầu-cuối:** Xây dựng một luồng công việc di chuyển mỗi mục từ xác định qua phân tích nguyên nhân gốc, triển khai, và kiểm định, với các chỉ số được so sánh trước và sau.
- **Xây dựng tầm nhìn vào các xu hướng và kết quả:** Tạo các dashboard hiển thị các xu hướng phản hồi, kết quả cải tiến, và quỹ đạo chất lượng theo thời gian.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](agentops02-bp01.md)
- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](../5-agentops05/agentops05-bp02.md)
- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công phù hợp với hiệu năng cho workload agent](../../4-performance-efficiency/1-agentperf01/agentperf01-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Đánh giá AI agent: Bài học thực tế từ việc xây dựng hệ thống agentic tại Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)

**Video liên quan:**

- [AWS re:Invent 2024 - Elevate application and generative AI observability (COP326)](https://www.youtube.com/watch?v=vxzq8GthOLs)
- [AWS re:Invent 2024 - Responsible generative AI: Evaluation best practices and tools (AIM342)](https://www.youtube.com/watch?v=wuVpCc5a81Y)

**Ví dụ liên quan:**

- [GitHub: Open Source Bedrock Agent Evaluation](https://github.com/aws-samples/open-source-bedrock-agent-evaluation)
- [GitHub: Sample Bedrock Evaluation Adapter](https://github.com/aws-samples/sample-bedrock-evaluation-adapter)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
