# AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường

Các cảnh báo ngưỡng tĩnh bắt được các sự cố rõ ràng. Phát hiện bất thường trên các baseline hành vi mở rộng phạm vi bao phủ tới các dịch chuyển dần dần như một tỷ lệ leo thang tăng chậm, một tần suất ảo giác tăng âm thầm, hoặc các mẫu lựa chọn Tools trôi lệch về các phương án kém năng lực hơn, cung cấp tầm nhìn sớm vào các xu hướng hành vi.

**Kết quả mong muốn:**

- Các hồ sơ hành vi baseline được thiết lập theo từng agent và cập nhật liên tục khi hành vi bình thường tiến hóa.
- Các bất thường (các mẫu suy luận bất thường, việc dùng Tools bất ngờ, suy giảm hiệu năng, và trôi lệch hành vi) được phát hiện tự động và định tuyến tới đúng luồng ứng phó.
- Các nhóm nhận được cảnh báo sớm về các vấn đề đang nổi lên trước khi chúng ảnh hưởng tới người dùng.
- Các thay đổi hành vi có thể được truy nguyên về các cập nhật cấu hình cụ thể, cập nhật Model, hoặc các dịch chuyển phân bố đầu vào.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ dựa hoàn toàn vào cảnh báo dựa trên ngưỡng tĩnh mà không có phát hiện bất thường, bỏ lỡ trôi lệch dần dần vốn không bao giờ kích hoạt một ngưỡng đơn lẻ nhưng lại đại diện cho một thay đổi tích lũy đáng kể.
- Thiết lập các baseline hành vi một lần tại thời điểm triển khai mà không cập nhật chúng khi hành vi bình thường tiến hóa, khiến sự tiến hóa chính đáng bị gắn cờ là bất thường.
- Chỉ giám sát các chỉ số hiệu năng mà không có các chỉ số hành vi (các mẫu suy luận, lựa chọn Tools, tỷ lệ leo thang), bỏ lỡ các bất thường không biểu hiện thành các vấn đề hiệu năng.
- Đối xử với mọi bất thường với cùng mức khẩn cấp, tạo ra mệt mỏi cảnh báo (alert fatigue) khiến các nhóm bỏ qua các vấn đề thực sự.
- Không phân biệt trôi lệch dữ liệu (dịch chuyển phân bố đầu vào), trôi lệch khái niệm (thay đổi quan hệ đầu vào-đầu ra), và trôi lệch hiệu năng (suy giảm chất lượng đầu ra), dẫn tới khắc phục sai hướng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Giám sát hành vi mở rộng khả năng quan sát từ các chỉ số hạ tầng tới các mẫu ra quyết định, mang lại tầm nhìn vào các khía cạnh hành vi agent ảnh hưởng nhiều nhất tới các kết quả kinh doanh.
- Phát hiện trôi lệch tạo ra một tín hiệu phản hồi xác định khi các agent cần huấn luyện lại, cấu hình lại, hoặc cập nhật để duy trì sự phù hợp.
- Định tuyến nhận biết mức độ nghiêm trọng giữ cho các nhóm phản ứng nhanh với các bất thường tác động cao mà không làm ngập họ trong các tín hiệu mức độ nghiêm trọng thấp.
- Tương quan các bất thường với các thay đổi cấu hình và Model đẩy nhanh phân tích nguyên nhân gốc.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hãy thiết lập một baseline, vì phát hiện bất thường không có baseline có thể tạo ra các tín hiệu không đáng tin cậy. Thu thập các chỉ số agent trong hai đến bốn tuần, như số vòng lặp suy luận, tần suất lựa chọn Tools, tỷ lệ leo thang, tỷ lệ hoàn thành tác vụ, và các phân bố điểm tin cậy, để thiết lập một baseline cho mỗi agent. [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) Anomaly Detection tạo ra các baseline động tiến hóa tự động và phát hiện các sai lệch qua các dải dựa trên ML, vốn bắt được trôi lệch mà các ngưỡng tĩnh bỏ sót.

Hãy chọn các chỉ số của bạn một cách cẩn thận. Các chỉ số hiệu năng (độ trễ, tỷ lệ lỗi) là cần thiết nhưng chưa đủ. Các chỉ số hành vi, các mẫu suy luận, tần suất lựa chọn Tools, tỷ lệ leo thang, và các phân bố chất lượng đầu ra là nơi trôi lệch tinh vi xuất hiện lần đầu và là nơi bất thường ảnh hưởng tới người dùng thường xảy ra nhất.

Định tuyến theo mức độ nghiêm trọng giúp ngăn mệt mỏi cảnh báo làm xói mòn tính hữu ích của hệ thống.

- Các bất thường hiệu năng kích hoạt điều tra tự động
- Các bất thường hành vi kích hoạt rà soát của con người
- Các bất thường liên quan tới bảo mật kích hoạt leo thang tức thời

Ba hàng đợi phục vụ các vòng lặp vận hành khác nhau, và việc trộn lẫn chúng có thể tạo ra nhiễu và phản ứng dưới mức. Hãy tương quan các bất thường với các sự kiện triển khai trên các dashboard.

Các cập nhật baseline luân phiên (rolling) giữ cho hệ thống phù hợp với thay đổi chính đáng. Khi các agent tích lũy việc sử dụng và trưởng thành, hành vi bình thường dịch chuyển, và một baseline bị đóng băng tại thời điểm triển khai rốt cuộc sẽ gắn cờ mọi ngày là bất thường. Nhịp cập nhật nên phản ánh sự ổn định của agent: các cửa sổ luân phiên hàng tuần phù hợp với các agent đang lặp lại tích cực, hàng tháng hoặc lâu hơn cho các agent sản xuất ổn định.

### Các bước triển khai

- **Định nghĩa các chỉ số hành vi theo từng agent:** Bao phủ các mẫu suy luận, việc dùng Tools, tỷ lệ leo thang, và chất lượng đầu ra bên cạnh các chỉ số hiệu năng.
- **Thu thập các baseline và cấu hình [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) Anomaly Detection:** Dùng một khoảng quan sát đại diện và cấu hình các dải phát hiện bất thường trên các chỉ số hành vi then chốt.
- **Định tuyến các bất thường theo loại và mức độ nghiêm trọng:** Các bất thường hiệu năng tới điều tra tự động, hành vi tới rà soát của con người, bảo mật tới leo thang tức thời.
- **Xây dựng các dashboard giám sát hành vi:** Hiển thị các mẫu theo thời gian và tương quan với các thay đổi cấu hình hoặc Model.
- **Cập nhật các baseline trên cơ sở luân phiên:** Phản ánh sự tiến hóa chính đáng trong khi duy trì độ nhạy với các bất thường thực sự.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](agentops05-bp01.md)
- [AGENTOPS05-BP03 Triển khai ghi log có cấu trúc và các vết kiểm toán toàn diện](agentops05-bp03.md)
- [AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục](../2-agentops02/agentops02-bp04.md)
- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](../../3-reliability/2-agentrel02/agentrel02-bp03.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và khoanh vùng agent](../../2-security/7-agentsec07/agentsec07-bp04.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Launching Amazon CloudWatch generative AI observability](https://aws.amazon.com/blogs/mt/launching-amazon-cloudwatch-generative-ai-observability-preview/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)
- [Advancing AI agent governance with Boomi and AWS](https://aws.amazon.com/blogs/machine-learning/advancing-ai-agent-governance-with-boomi-and-aws-a-unified-approach-to-observability-and-compliance)

**Video liên quan:**

- [AWS re:Invent 2024 - Move beyond reactive: Transform cloud ops with AWS DevOps Agent (COP362)](https://www.youtube.com/watch?v=JajBEYle67I)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
