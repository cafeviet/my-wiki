# AGENTSEC09-BP05 Triển khai phát hiện đe dọa ở thời điểm chạy, tương quan sự kiện bảo mật và khắc phục tự động cho agent

Quét tìm các điểm yếu tiềm ẩn. Phát hiện ở thời điểm chạy bắt các cuộc tấn công đang xảy ra ngay bây giờ. Tương quan các sự kiện qua các bề mặt tương tác agent và kích hoạt khắc phục tự động nén khoảng cách giữa một khai thác đang diễn ra và phản hồi kiềm chế nó.

**Kết quả mong muốn:**

- Bạn liên tục giám sát các sự kiện bảo mật từ hoạt động agent, tương quan chúng qua các bề mặt tương tác, và phân tích chúng tìm các chuỗi tấn công nhiều bước.
- Bạn phát hiện các đe dọa đang diễn ra nhắm vào các hệ thống tác tử trong vòng vài phút, với các chuỗi tấn công quan trọng được làm nổi bật ở mức độ nghiêm trọng cao nhất.
- Các luồng công việc khắc phục tự động kích hoạt các hành động kiềm chế và sinh các bản sửa sẵn sàng để hiện thực, giảm thời gian trung bình đến khi phát hiện và thời gian trung bình đến khi khắc phục.
- Các đội bảo mật có một khung nhìn thống nhất về các đe dọa liên quan đến agent cùng với các phát hiện từ quét lỗ hổng và kiểm thử xâm nhập.

**Các phản mẫu thường gặp (anti-patterns):**

- Xử lý các sự kiện bảo mật agent một cách cô lập thay vì tương quan chúng qua các bề mặt tương tác, bỏ sót các chuỗi tấn công nhiều bước nơi các sự kiện riêng lẻ trông vô hại nhưng cùng nhau tạo thành một cuộc tấn công có phối hợp.
- Chỉ dựa vào quét lỗ hổng trước triển khai mà không có phát hiện đe dọa ở thời điểm chạy, để lại một khoảng trống nơi các lỗ hổng được đưa vào qua trôi dạt cấu hình, các tích hợp công cụ mới hoặc các kỹ thuật tấn công mới lạ không được phát hiện cho đến cuộc đánh giá theo lịch tiếp theo.
- Sinh các cảnh báo bảo mật mà không có các luồng công việc khắc phục tự động, tạo ra sự mệt mỏi vì cảnh báo (alert fatigue) nơi các đội bảo mật bị quá tải bởi các phát hiện nhưng thiếu công cụ để hành động nhanh.
- Không tương quan các phát hiện kiểm thử xâm nhập với các tín hiệu phát hiện đe dọa ở thời điểm chạy, bỏ sót mối liên hệ giữa các lỗ hổng đã biết và các ý đồ khai thác đang diễn ra cùng nhau cung cấp một tín hiệu ưu tiên khắc phục độ tin cậy cao.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tương quan sự kiện có AI/ML hỗ trợ nhận diện các cuộc tấn công có phối hợp trải qua nhiều bề mặt tương tác agent, các kỳ thời gian và các tài nguyên.
- Các luồng công việc tự động kích hoạt các hành động kiềm chế và sinh các khuyến nghị sửa khi các đe dọa được phát hiện, đóng vòng lặp giữa phát hiện và ứng phó.
- Các phát hiện tập trung từ quét lỗ hổng, kiểm thử xâm nhập và phát hiện đe dọa ở thời điểm chạy cho phép ưu tiên dựa trên rủi ro trên toàn vòng đời đe dọa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Quét và kiểm thử xâm nhập tìm các điểm yếu trước khi khai thác. Phát hiện ở thời điểm chạy bắt khai thác khi nó xảy ra. Cả hai đều cần thiết vì không cái nào riêng lẻ là đủ. Một hệ thống tác tử thêm bề mặt (công cụ, API, kho bộ nhớ, các agent khác) bị khai thác qua các chuỗi prompt injection, lạm dụng thông tin xác thực, các chuỗi trích xuất dữ liệu và các đường leo thang đặc quyền. Phát hiện phải tương quan qua bề mặt đó, không xử lý mỗi kênh một cách cô lập.

Hãy triển khai Amazon GuardDuty trên mọi tài khoản nơi agent hoạt động để cung cấp phát hiện đe dọa liên tục cho các vai trò IAM của agent, hoạt động API và các mẫu truy cập dữ liệu. [GuardDuty Extended Threat Detection](https://aws.amazon.com/blogs/aws/introducing-amazon-guardduty-extended-threat-detection-aiml-attack-sequence-identification-for-enhanced-cloud-security/) tương quan các tín hiệu bảo mật để nhận diện các chuỗi tấn công đang diễn ra (khám phá đặc quyền theo sau bởi thao túng API, các hoạt động duy trì hiện diện, và trích xuất dữ liệu) và làm nổi bật chúng như các phát hiện chuỗi tấn công mức độ nghiêm trọng nghiêm trọng (critical) với các tóm tắt bằng ngôn ngữ tự nhiên, ánh xạ MITRE ATT&CK và các khuyến nghị khắc phục theo quy tắc.

Với phát hiện đe dọa riêng của agent, hãy cấu hình giám sát GuardDuty trên các nguồn dữ liệu liên quan nhất đến các khối công việc tác tử:

- Các sự kiện quản lý AWS CloudTrail cho các mẫu lời gọi API
- Amazon VPC Flow Logs cho hành vi mạng
- DNS log cho phát hiện chỉ huy-và-kiểm-soát (command-and-control)
- Các data event Amazon S3 cho giám sát truy cập dữ liệu

Hãy bật GuardDuty Runtime Monitoring cho các tài nguyên tính toán chạy các khối công việc agent để phát hiện các đe dọa ở cấp hệ điều hành, bao gồm việc thực thi tiến trình đáng ngờ và các kết nối mạng.

AWS Security Hub CSPM là lớp tổng hợp. Các phát hiện từ Amazon GuardDuty (các đe dọa ở thời điểm chạy), [AWS Security Agent](https://aws.amazon.com/security-agent/) (quét lỗ hổng và kiểm thử xâm nhập), Amazon Macie (phơi bày dữ liệu nhạy cảm) và Amazon Inspector (quét lỗ hổng phần mềm) chuẩn hóa thành AWS Security Finding Format (ASFF) để ưu tiên nhất quán và ứng phó tự động bất kể nguồn. Các insight của Security Hub CSPM tương quan các phát hiện kiểm thử xâm nhập với các tín hiệu phát hiện ở thời điểm chạy, nhận diện các trường hợp nơi các lỗ hổng đã biết đang bị khai thác chủ động (một tín hiệu ưu tiên độ tin cậy cao).

Các quy tắc Amazon EventBridge kích hoạt các hàm AWS Lambda hoặc các luồng công việc AWS Step Functions khi các phát hiện mức độ nghiêm trọng cao được sinh ra. Với các đe dọa riêng của agent, luồng công việc khắc phục thu trạng thái pháp chứng (bộ nhớ agent, các phiên hoạt động, các lần gọi công cụ gần đây) tới Amazon S3, áp dụng các hành động kiềm chế (thu hồi thông tin xác thực, cô lập mạng) như được mô tả trong AGENTSEC07-BP04, sinh các khuyến nghị khắc phục dựa trên loại phát hiện, và tạo các tác vụ khắc phục được theo dõi. Các phát hiện từ kiểm thử xâm nhập của AWS Security Agent bao gồm các bản sửa mã được gợi ý định tuyến trực tiếp tới các nhóm phát triển qua luồng công việc theo dõi khắc phục hiện có.

[Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) thêm một lớp phát hiện bổ trợ. Chấm điểm đánh giá liên tục phát hiện trôi dạt hành vi đi trước hoặc đi kèm các sự cố bảo mật. Một sự sụt giảm đột ngột trong các điểm an toàn hoặc độ đúng đắn kết hợp với một phát hiện GuardDuty cho cùng agent là một tín hiệu độ tin cậy cao đáng điều tra ngay lập tức. Các cảnh báo tổng hợp Amazon CloudWatch được kích hoạt khi cả sự suy giảm điểm đánh giá lẫn một phát hiện GuardDuty xảy ra trong cùng cửa sổ thời gian làm nổi bật các trường hợp đó một cách tự động.

### Các bước triển khai

- **Bật GuardDuty trên các tài khoản agent:** Bật Amazon GuardDuty với giám sát được cấu hình cho các sự kiện AWS CloudTrail, Amazon VPC Flow Logs, DNS log, các data event Amazon S3, và GuardDuty Runtime Monitoring cho các tài nguyên tính toán agent.
- **Tập trung các phát hiện trong Security Hub CSPM:** Tổng hợp các phát hiện từ Amazon GuardDuty, [AWS Security Agent](https://aws.amazon.com/security-agent/), Amazon Macie và Amazon Inspector trong AWS Security Hub CSPM, và cấu hình các insight của Security Hub CSPM để tương quan các phát hiện kiểm thử xâm nhập với các tín hiệu phát hiện đe dọa ở thời điểm chạy.
- **Tự động hóa kiềm chế trên các phát hiện mức độ nghiêm trọng cao:** Dùng các quy tắc Amazon EventBridge và các hàm AWS Lambda để kích hoạt các hành động kiềm chế và sinh các khuyến nghị sửa khi các phát hiện mức độ nghiêm trọng cao được sinh ra.
- **Kết hợp trôi dạt đánh giá với các phát hiện GuardDuty:** Cấu hình các cảnh báo tổng hợp Amazon CloudWatch kết hợp sự suy giảm điểm [Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) với các phát hiện GuardDuty để làm nổi bật các tín hiệu đe dọa độ tin cậy cao.
- **Định tuyến các bản sửa tới các lập trình viên và đo MTTR:** Định tuyến các khuyến nghị khắc phục, bao gồm các bản sửa mã từ AWS Security Agent, tới các nhóm phát triển qua một luồng công việc được theo dõi, và giám sát thời gian trung bình đến khi phát hiện và thời gian trung bình đến khi khắc phục như các chỉ số bảo mật then chốt.
- **Điều chỉnh phát hiện hàng quý:** Rà soát các quy tắc phát hiện, các luồng công việc khắc phục và logic tương quan phát hiện hàng quý dựa trên các mẫu đe dọa quan sát được và các tỷ lệ dương tính giả.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](../7-agentsec07/agentsec07-bp04.md)
- [AGENTSEC09-BP01 Tích hợp quét lỗ hổng có AI hỗ trợ trên toàn vòng đời phát triển](agentsec09-bp01.md)
- [AGENTSEC09-BP02 Tiến hành kiểm thử xâm nhập có nhận thức ngữ cảnh với mô phỏng tấn công đa agent](agentsec09-bp02.md)

**Tài liệu liên quan:**

- [Amazon GuardDuty Extended Threat Detection](https://aws.amazon.com/blogs/aws/introducing-amazon-guardduty-extended-threat-detection-aiml-attack-sequence-identification-for-enhanced-cloud-security/)
- [Tài liệu Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Tài liệu AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Automate cloud security vulnerability assessment and alerting using Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/automate-cloud-security-vulnerability-assessment-and-alerting-using-amazon-bedrock/)
- [How government agencies can transform cybersecurity operations with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/publicsector/how-government-agencies-can-transform-cybersecurity-operations-with-amazon-bedrock-agentcore/)
- [AWS Security Agent](https://aws.amazon.com/security-agent/)

**Dịch vụ liên quan:**

- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)
- [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Macie](https://aws.amazon.com/macie/)
- [Amazon Inspector](https://aws.amazon.com/inspector/)
