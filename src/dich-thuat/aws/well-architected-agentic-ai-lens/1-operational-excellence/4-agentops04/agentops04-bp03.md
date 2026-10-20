# AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools

Việc Tools gặp lỗi là một thực tế trong các kiến trúc hiện đại. Câu hỏi là liệu agent có suy giảm nhã nhặn sang một phương án thay thế, dự phòng về một quy trình thủ công, hay trả về lỗi và dừng lại. Các chuỗi dự phòng và các ngắt tự động được thiết kế tốt giữ cho các lỗi Tools không trở thành lỗi agent.

**Kết quả mong muốn:**

- Khi Tools gặp lỗi hoặc trở nên không khả dụng, các agent suy giảm nhã nhặn sang các Tools thay thế, các thao tác ở chế độ suy giảm, hoặc leo thang tới quy trình thủ công.
- Các ngắt tự động giúp ngăn các lỗi lan truyền lan rộng qua môi trường agent.
- Các chiến lược thử lại với lùi lũy thừa (exponential backoff) xử lý các lỗi nhất thời một cách trong suốt mà không khuếch đại tải lên các hệ thống đang suy giảm.
- Tỷ lệ thành công theo từng Tools, độ trễ, và các mẫu lỗi được giám sát theo thời gian thực để suy giảm được phát hiện trước khi ảnh hưởng tới người dùng.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các chiến lược thử lại giống hệt nhau cho mọi Tools bất kể đặc tính lỗi, áp dụng các lần thử lại mạnh mẽ cho các Tools đã lỗi vĩnh viễn hoặc quá ít lần thử cho các Tools suy giảm nhất thời.
- Vận hành mà không có các ngắt tự động, nên các agent liên tục gọi các Tools suy giảm vốn hết thời gian một cách nhất quán, lãng phí thời gian và tài nguyên vào các lời gọi khó thành công.
- Không có đường dự phòng khi một Tools gặp lỗi, buộc agent trả về lỗi cho người dùng hoặc dừng hẳn luồng công việc.
- Xem các runbook Tools như tài liệu tùy chọn, nên người vận hành bắt đầu từ đầu ở mỗi sự cố.

**Lợi ích khi áp dụng thực hành tốt này:**

- Giám sát theo từng Tools với phân tích mẫu lỗi mang lại tầm nhìn sâu về độ tin cậy của Tools qua catalog.
- Các runbook vận hành giúp dẫn dắt ứng phó sự cố nhất quán, giảm thời gian trung bình để giải quyết và giúp ngăn các phản ứng tùy ứng vốn tạo ra các vấn đề mới.
- Các ngắt tự động chặn các lỗi lan truyền tại nguồn thay vì để chúng lan qua các agent.
- Suy giảm nhã nhặn qua các chuỗi dự phòng duy trì tính liên tục kinh doanh trong các gián đoạn cục bộ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Các ngắt tự động là kiểm soát hiệu quả duy nhất và mạnh nhất để giúp ngăn lỗi lan truyền. Khi một Tools bắt đầu trả về lỗi trên một ngưỡng, việc tiếp tục gọi nó làm vấn đề tồi tệ hơn. Agent lãng phí thời gian, Tools nhận thêm tải, và độ trễ thượng nguồn leo thang trong khi không hoàn thành gì. Một ngắt tự động chuyển Tools từ hoạt động bình thường sang bị chặn khi tỷ lệ lỗi vượt một ngưỡng (ví dụ, 50% lỗi trong cửa sổ 60 giây) hoặc khi các timeout vượt một ngưỡng (ví dụ, 5 lần timeout liên tiếp). Nó chuyển sang thăm dò (probing) sau một khoảng phục hồi có thể cấu hình (ví dụ, 30 giây). Hãy áp dụng máy trạng thái (state machine) này cho mọi phụ thuộc bên ngoài thay vì chỉ những phụ thuộc đã từng gây sự cố.

Các chính sách thử lại và timeout nên theo từng Tools thay vì toàn cục. Lùi lũy thừa với jitter xử lý các lỗi nhất thời mà không khuếch đại vấn đề. Các chuỗi dự phòng, như chính-sang-phụ-sang-chế-độ-suy-giảm-sang-leo-thang-thủ-công, mang lại cho agent một đường tiến lên khi Tools chính không khả dụng cho các thao tác quan trọng. Thứ tự dự phòng nên nằm trong registry Tools để nó tiến hóa theo kho Tools thay vì được nhúng trong mã của mỗi agent.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) theo dõi số lần gọi, tỷ lệ thành công, tỷ lệ lỗi theo loại, và các phân vị độ trễ (latency percentiles) trên cơ sở từng Tools. Các cảnh báo tổng hợp (composite alarms) tương quan nhiều chỉ số. Một Tools với độ trễ tăng và tỷ lệ timeout tăng là một Tools đang tiến gần tới ngắt, bất kể một tín hiệu riêng lẻ có kích hoạt cảnh báo hay không. Góc nhìn tổng hợp thường bắt được suy giảm sớm hơn so với các ngưỡng đơn chỉ số.

Hãy phát triển các runbook vận hành cho năm kịch bản lỗi Tools phổ biến nhất, và tạo các báo cáo SLA hàng tuần chia sẻ với các chủ sở hữu Tools để các xu hướng độ tin cậy luôn thấy được.

### Các bước triển khai

- **Triển khai các ngắt tự động:** Cấu hình các ngưỡng tỷ lệ lỗi và timeout cho việc chuyển từ bình thường sang bị chặn, cộng với các timeout phục hồi thăm dò, cho mọi phụ thuộc bên ngoài.
- **Định nghĩa các chính sách timeout và thử lại theo từng Tools:** Dùng lùi lũy thừa với jitter phù hợp với đặc tính lỗi của mỗi Tools.
- **Xây dựng các chuỗi dự phòng cho các Tools quan trọng:** Lưu thứ tự dự phòng trong registry Tools để các chuỗi tiến hóa theo kho Tools thay vì bị hardcode trong mỗi agent.
- **Giám sát sức khỏe theo từng Tools qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html):** Dùng các cảnh báo tổng hợp tương quan nhiều chỉ số để phát hiện sớm hơn.
- **Phát triển các runbook vận hành cho các kịch bản lỗi Tools phổ biến:** Bao gồm các bước chẩn đoán và đường leo thang để người vận hành bắt đầu từ một baseline đã biết.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools](agentops04-bp01.md)
- [AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)](agentops04-bp02.md)
- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](../5-agentops05/agentops05-bp01.md)
- [AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả](../../4-performance-efficiency/6-agentperf06/agentperf06-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Lên kế hoạch cho thất bại: Làm sao để workload generative AI kiên cường hơn](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)
- [Effectively building AI agents on AWS Serverless](https://aws.amazon.com/blogs/compute/effectively-building-ai-agents-on-aws-serverless/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
