# AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent

Các chỉ số hạ tầng như CPU, bộ nhớ, và số lần gọi giải thích liệu một agent có đang chạy hay không. Tuy nhiên, các chỉ số này không xác định liệu một agent có thực sự hoạt động hay không. Các chỉ số hiệu năng then chốt (KPI) gắn với các kết quả kinh doanh mang lại cho các nhóm và các bên liên quan một ngôn ngữ chung để bàn luận và cải thiện hiệu năng agent.

**Kết quả mong muốn:**

- Mỗi luồng công việc agent có một tập KPI được xác định, được theo dõi liên tục so với các baseline đã thiết lập.
- Các nhóm xác định suy giảm hiệu năng sớm và tương quan các thay đổi KPI với các cập nhật cấu hình hoặc Model.
- Các nỗ lực tối ưu được ưu tiên dựa trên tác động đo lường được thay vì trực giác.
- Các bên liên quan kinh doanh có tầm nhìn định kỳ vào cách các luồng công việc agent đóng góp vào các kết quả kinh doanh.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ theo dõi các chỉ số hạ tầng (như CPU, bộ nhớ, và số lần gọi) mà không có các KPI đặc thù agent đo các kết quả kinh doanh như tỷ lệ hoàn thành tác vụ và mức độ hài lòng của người dùng.
- Định nghĩa KPI tại thời điểm triển khai và không bao giờ xem lại khi các mục tiêu kinh doanh tiến hóa, đo các chỉ số không còn phản ánh điều quan trọng.
- Thu thập dữ liệu KPI mà không thiết lập các baseline hay ngưỡng cảnh báo, tạo ra các dashboard mà không ai giám sát chủ động.
- Gán trọng số ngang nhau cho các chỉ số vận hành và kinh doanh khi một chỉ số quan trọng gấp mười lần chỉ số kia, tạo ra các dashboard trông cân bằng nhưng gây hiểu lầm.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các KPI cung cấp nền tảng định lượng cho các quyết định dựa trên bằng chứng, để các nhóm đo tác động thay đổi và ưu tiên các cải tiến dựa trên dữ liệu.
- Theo dõi xu hướng bộc lộ các mẫu suy giảm hoặc cải thiện, cung cấp thông tin cho tinh chỉnh liên tục các Prompt, cấu hình, và tích hợp.
- Các chỉ số kết quả kinh doanh kết nối công việc agent với giá trị được mang lại, mang lại cho các bên liên quan các cập nhật định kỳ, cụ thể thay vì các trấn an mơ hồ.
- Cảnh báo dựa trên bất thường bắt được suy giảm dần dần mà các ngưỡng tĩnh bỏ sót.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một khung KPI dùng được bao phủ bốn chiều thay vì một.

- Các KPI vận hành, như tỷ lệ hoàn thành tác vụ, thời gian giải quyết, tỷ lệ lỗi, và tỷ lệ leo thang, đo liệu agent có chạy tin cậy hay không.
- Các KPI chất lượng, như độ chính xác quyết định, tỷ lệ ảo giác, và mức độ hài lòng của người dùng, đo liệu các đầu ra của nó có đúng hay không. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chấm điểm cho tính đúng đắn, tính hữu ích, tính an toàn, và độ chính xác lựa chọn Tools, vốn cung cấp các tín hiệu chất lượng tự động.
- Các KPI hiệu quả, như số Token trên mỗi tác vụ, số lời gọi Tools trên mỗi tác vụ, và chi phí trên mỗi tác vụ, đo liệu agent có tiết kiệm hay không.
- Các KPI kinh doanh, như tỷ lệ đạt được kết quả, mức tuân thủ SLA, và tác động tới mức độ hài lòng của khách hàng, đo liệu agent có xứng đáng với khoản đầu tư hay không.

Bỏ qua bất kỳ chiều nào tạo ra một dashboard trông có vẻ đầy đủ nhưng có thể gây hiểu lầm.

Các baseline khiến các KPI trở nên hữu ích bằng cách cung cấp ngữ cảnh để so sánh. Hãy thiết lập các baseline trong một khoảng quan sát ban đầu (hai đến bốn tuần thường là đủ), rồi cấu hình [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) Anomaly Detection để các baseline điều chỉnh tự động khi các luồng công việc trưởng thành. Đặt các ngưỡng cảnh báo mức cảnh báo (warning) và mức tới hạn (critical), trong đó các cảnh báo khởi động rà soát và các cảnh báo tới hạn quy định nhu cầu hành động.

Các báo cáo KPI hàng tuần qua [Amazon Quick Suite](https://aws.amazon.com/quicksuite/) chia sẻ cùng một dashboard với các bên liên quan kỹ thuật và kinh doanh. Cùng các chỉ số phục vụ cả hai đối tượng để mọi người thấy cùng một quỹ đạo và các cuộc trao đổi về đầu tư và ưu tiên hóa có dữ liệu chung làm nền tảng. Các buổi rà soát theo quý xác minh rằng các định nghĩa KPI vẫn phản ánh các mục tiêu kinh doanh và chỉ số cập nhật.

### Các bước triển khai

- **Định nghĩa một khung KPI bốn chiều:** Bao phủ các chiều vận hành, chất lượng, hiệu quả, và kinh doanh cho mỗi luồng công việc agent, với trọng số đặc thù cho trường hợp sử dụng.
- **Thu thập KPI qua các chỉ số tùy chỉnh của [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html):** Thêm các chiều cho agent, luồng công việc, và môi trường để cùng một chỉ số có thể được cắt lát theo nhiều cách.
- **Thiết lập các baseline và cấu hình phát hiện bất thường:** Dùng [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) Anomaly Detection với các ngưỡng cảnh báo mức cảnh báo và mức tới hạn.
- **Xây dựng các dashboard KPI hàng tuần:** Dùng các báo cáo [Amazon Quick](https://docs.aws.amazon.com/quicksuite/latest/user/welcome.html) chia sẻ với các bên liên quan kỹ thuật và kinh doanh.
- **Rà soát sự phù hợp của KPI theo quý:** Xác minh rằng các định nghĩa vẫn phản ánh các mục tiêu kinh doanh hiện tại, và loại bỏ hoặc thay thế các chỉ số không còn áp dụng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](agentops05-bp01.md)
- [AGENTOPS05-BP05 Tạo các dashboard đặc thù luồng công việc cho sức khỏe vận hành](agentops05-bp05.md)
- [AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục](../2-agentops02/agentops02-bp04.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Đánh giá AI agent: Bài học thực tế từ việc xây dựng hệ thống agentic tại Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)
- [From AI agent prototype to product: Lessons from building AWS DevOps Agent](https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Quick](https://aws.amazon.com/quicksuite/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
