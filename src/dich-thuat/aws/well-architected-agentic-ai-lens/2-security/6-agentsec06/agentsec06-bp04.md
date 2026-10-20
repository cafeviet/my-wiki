# AGENTSEC06-BP04 Giám sát và phát hiện các bất thường trong phối hợp

Truy vết phân tán cho bạn biết điều gì đã xảy ra trên một yêu cầu. Giám sát phối hợp cho bạn biết khi nào nhiều yêu cầu bắt đầu hành xử khác với đường cơ sở. Theo dõi tốc độ thông điệp giữa các agent, tần suất luồng công việc và các thay đổi topo so với các đường cơ sở đã thiết lập bắt các vấn đề qua tác động quan sát được của chúng lên sự phối hợp trước khi chúng leo thang thành các sự kiện bảo mật.

**Kết quả mong muốn:**

- Bạn phát hiện các mẫu phối hợp bất thường như các đường giao tiếp agent bất ngờ, các tần suất tương tác bất thường, hoặc các đợt tăng đột biến độ trễ phối hợp gần thời gian thực và kích hoạt các cảnh báo để điều tra.
- Bạn thiết lập các hồ sơ phối hợp đường cơ sở cho từng luồng công việc agent, để phát hiện bất thường thống kê bắt các sai lệch trước khi chúng gây tác động đáng kể.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ giám sát các chỉ số hạ tầng (CPU, bộ nhớ và mạng) mà không theo dõi các chỉ số phối hợp riêng của agent, bỏ sót các tín hiệu ở cấp phối hợp mang tính chỉ báo nhất về các vấn đề đa agent.
- Không thiết lập các đường cơ sở phối hợp trước khi triển khai phát hiện bất thường, điều này tạo ra hoặc quá nhiều dương tính giả hoặc các phát hiện bị bỏ sót.
- Coi các phát hiện của Amazon GuardDuty và các log phối hợp agent như các luồng dữ liệu riêng biệt, để các điều tra viên không có ngữ cảnh đa agent biến các bất thường ở cấp API thành tín hiệu hữu ích.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các đường cơ sở hành vi bắt các sai lệch phối hợp trước khi chúng lan truyền qua hệ thống đa agent.
- Các bản đồ dịch vụ so sánh các đường giao tiếp quan sát được với kiến trúc ranh giới tin cậy mong đợi, kiểm chứng topo liên tục.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Truy vết phân tán (AGENTSEC05-BP02) tái dựng điều gì đã xảy ra trong một yêu cầu cụ thể. Phát hiện bất thường phối hợp là một vấn đề khác. Đó là một hệ thống cảnh báo sớm chủ động theo dõi liệu các mẫu phối hợp qua nhiều yêu cầu theo thời gian có đang trôi dạt khỏi đường cơ sở hay không. Truy vết mang tính phản ứng và tập trung vào điều tra. Giám sát phối hợp mang tính phòng ngừa và tập trung vào đường cơ sở.

Hãy bắt đầu bằng cách định nghĩa các chỉ số phối hợp cho từng luồng công việc đa agent:

- Tốc độ thông điệp giữa các agent
- Tần suất thực thi luồng công việc
- Độ trễ phản hồi của agent
- Tỷ lệ lỗi theo từng cặp agent
- Các thay đổi topo của đồ thị phối hợp

Hãy công bố những chỉ số này dưới dạng các chỉ số tùy chỉnh Amazon CloudWatch, thiết lập các đường cơ sở bằng cách thu thập chúng trong quá trình vận hành bình thường, và cấu hình phát hiện bất thường Amazon CloudWatch để tự động nhận diện các sai lệch thống kê.

[Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/) cung cấp nền tảng. Phân cấp phiên, trace và span ghi lại các tương tác giữa các agent, và các chỉ số mặc định trên trang generative AI observability của Amazon CloudWatch làm nổi bật các mẫu ở cấp phiên. Với các agent dùng giao thức A2A trên AgentCore Runtime, vòng đời yêu cầu có cấu trúc (khám phá agent card, ủy thác tác vụ, thu thập kết quả) sinh các sự kiện quan sát được tại mỗi bước phối hợp, mà bạn có thể dùng để xây dựng các bản đồ topo phối hợp và phát hiện khi các agent giao tiếp ngoài các mẫu mong đợi của chúng.

[Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) bổ trợ cho giám sát phối hợp bằng cách liên tục chấm điểm hành vi của agent về độ chính xác lựa chọn công cụ, độ đúng đắn và các chiều chất lượng khác. Nếu một agent phối hợp bắt đầu chọn các công cụ bất ngờ hoặc sinh các đầu ra không đúng, các sụt giảm điểm đánh giá có thể đóng vai trò một tín hiệu cảnh báo sớm trước khi bất thường phối hợp trở nên hiển thị ở cấp luồng công việc. Các cảnh báo Amazon CloudWatch về điểm đánh giá xếp lớp với các chỉ số phối hợp cho bạn một cách tiếp cận phát hiện hai giai đoạn.

Amazon GuardDuty giám sát các mẫu lời gọi API cho mọi vai trò IAM của agent. Các mô hình học máy của nó phát hiện các mẫu gọi bất thường: một agent đột nhiên gọi các dịch vụ nó chưa từng truy cập, hoặc gọi các API vào các thời điểm bất thường hoặc từ các vị trí bất ngờ. Hãy tích hợp các phát hiện GuardDuty với AWS Security Hub CSPM để ưu tiên tập trung, và tương quan chúng với các log phối hợp agent để kết nối các bất thường ở cấp API với các luồng công việc đa agent cụ thể. Các truy vấn Amazon CloudWatch Logs Insights thêm một lớp nữa, phân tích các log phối hợp agent tìm các mẫu như các agent nhận chỉ thị từ các nguồn bất ngờ, các vòng lặp phối hợp có thể chỉ báo hành vi mất kiểm soát, và các agent cố truy cập các tài nguyên ngoài phạm vi đã định của chúng. Hãy lên lịch các truy vấn này chạy định kỳ và công bố kết quả tới một dashboard bảo mật.

### Các bước triển khai

- **Định nghĩa và công bố các chỉ số phối hợp:** Thu tốc độ thông điệp giữa các agent, tần suất thực thi, độ trễ phản hồi và tỷ lệ lỗi theo từng cặp agent qua các chỉ số tùy chỉnh Amazon CloudWatch cho từng luồng công việc đa agent.
- **Thiết lập các đường cơ sở và bật phát hiện bất thường:** Thu thập các chỉ số trong quá trình vận hành bình thường và cấu hình phát hiện bất thường Amazon CloudWatch trên các chỉ số then chốt.
- **Xây dựng các bản đồ topo:** Dùng các bản đồ dịch vụ của [Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/) và các sự kiện vòng đời yêu cầu A2A để xây dựng các bản đồ topo phối hợp, và cảnh báo về các thay đổi topo bất ngờ lệch khỏi kiến trúc ranh giới tin cậy có tài liệu.
- **Xếp các đánh giá làm cảnh báo sớm:** Triển khai [Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) để liên tục chấm điểm hành vi của agent, và cấu hình các cảnh báo Amazon CloudWatch về điểm đánh giá như một lớp cảnh báo sớm cho các vấn đề phối hợp.
- **Tương quan GuardDuty với các log phối hợp:** Bật Amazon GuardDuty cho mọi tài khoản agent, tích hợp các phát hiện với AWS Security Hub CSPM, và tạo các quy tắc tương quan kết nối các bất thường API với các log phối hợp agent cụ thể.
- **Chạy các truy vấn Logs Insights theo lịch:** Xây dựng các truy vấn Amazon CloudWatch Logs Insights cho các mẫu sự kiện bảo mật phối hợp và công bố kết quả tới một dashboard bảo mật theo một nhịp định kỳ.
- **Ghi tài liệu runbook ứng phó:** Thiết lập một runbook ứng phó sự cố cho các cảnh báo bất thường phối hợp định nghĩa các bước điều tra, các đường leo thang và các hành động khắc phục.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent](agentsec06-bp01.md)
- [AGENTSEC06-BP03 Thiết lập các ranh giới tin cậy giữa các agent](agentsec06-bp03.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](../7-agentsec07/agentsec07-bp04.md)
- [AGENTREL02-BP03 Triển khai phát hiện bất thường hành vi và giám sát](../../3-reliability/2-agentrel02/agentrel02-bp03.md)

**Tài liệu liên quan:**

- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
- [Tài liệu Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Amazon CloudWatch anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/)
