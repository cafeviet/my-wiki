# Bảo vệ hoạt động giám sát của con người và kiềm chế agent

Sự giám sát của con người là một kiểm soát then chốt trong các hệ thống tác tử, nhưng nó chỉ hiệu quả nếu người rà soát có thể đưa ra các quyết định có hiểu biết mà không bị quá tải hay bị dẫn dắt sai. Đồng thời, bạn phải phát hiện và kiềm chế các agent lệch khỏi hành vi dự định của chúng trước khi chúng có thể ảnh hưởng đến các phần khác của hệ thống. Năng lực này bao phủ cả hai mặt: bảo vệ chất lượng của việc rà soát của con người, và hiện thực các cơ chế phát hiện và kiềm chế cho các agent hoạt động ngoài các ranh giới đã định của chúng.

| AGENTSEC07: Bạn bảo vệ sự giám sát của con người khỏi thao túng và phát hiện các agent lừa đảo (rogue) như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các hàng đợi rà soát được ưu tiên và cân bằng tải, và khối lượng công việc của người rà soát được giám sát để tìm các dấu hiệu phê duyệt máy móc (rubber-stamping), để những người rà soát của con người đưa ra các quyết định có hiểu biết thay vì phê duyệt dưới áp lực.
- Mỗi quyết định được trình bày để rà soát mang ngữ cảnh được hiệu chỉnh, bao gồm điểm độ tin cậy, kết quả kiểm tra chính sách, các cờ bất thường và các quyết định tương tự trong quá khứ, để người rà soát khớp mức soi xét của họ với rủi ro thực tế của hành động.
- Các hành động agent rủi ro cao nhận được rà soát độc lập từ nhiều người rà soát đủ điều kiện, với rà soát mù (blind review), logic đồng thuận và leo thang khi bất đồng.
- Các đường cơ sở hành vi tồn tại cho từng agent, và các sai lệch kích hoạt kiềm chế nhanh qua thu hồi thông tin xác thực và kích hoạt cầu dao ngắt, với trạng thái pháp chứng được thu lại trước khi cô lập.
- Các đánh giá bảo mật kết hợp quét tự động liên tục với các bài tập red team và purple team theo lịch nhắm vào các kịch bản thao túng riêng của agent, và các phát hiện chảy ngược trở lại vào các guardrail, các quy tắc phát hiện và các runbook ứng phó sự cố. Các bài tập red team là các mô phỏng đối kháng nơi một đội chuyên trách cố xâm phạm hệ thống agent bằng các kỹ thuật mà một kẻ tấn công thực sẽ dùng. Các bài tập purple team chạy cùng các kịch bản một cách phối hợp với các bên phòng thủ để các quy tắc phát hiện và các runbook được cập nhật dựa trên những gì quan sát được trong quá trình mô phỏng.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc bảo vệ giám sát của con người và kiềm chế agent như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các đường ống rà soát mang tính phi chính thức và được định tuyến tới bất kỳ ai sẵn có, không có các chỉ số khối lượng công việc hay phân loại ưu tiên. Người rà soát đánh giá các quyết định của agent mà không có điểm độ tin cậy, ngữ cảnh lịch sử, hay kiểm chứng độc lập. Hành vi của agent chỉ được quan sát qua các chỉ số hạ tầng, và kiềm chế phụ thuộc vào điều tra thủ công về sau. Các đánh giá bảo mật là một lần hoặc vắng mặt. |
| 2 | Manh nha (Emerging) | Các yêu cầu rà soát chảy qua một hàng đợi có tài liệu với các tầng ưu tiên thô, và phê duyệt một người rà soát áp dụng cho hầu hết các quyết định của agent. Các đầu ra của agent bao gồm các kiểm tra bám ngữ cảnh chung, nhưng người rà soát không thấy các mẫu lịch sử hay các cảnh báo thao túng. Các đánh giá bảo mật chung bao phủ các lần triển khai agent, và các kịch bản red team riêng của agent bị giới hạn. |
| 3 | Được định nghĩa (Defined) | Một đường ống rà soát được ưu tiên được hậu thuẫn bởi [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) và [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) theo dõi các chỉ số thời-gian-đến-quyết-định và tỷ-lệ-phê-duyệt, với các cảnh báo về các mẫu phê duyệt máy móc. Người rà soát thấy các điểm bám ngữ cảnh từ các kiểm tra [bám ngữ cảnh của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html), các cờ sai lệch so với các quyết định lịch sử, và các cảnh báo bằng ngôn ngữ đơn giản cho các ý đồ thao túng được gắn cờ. Các thao tác rủi ro cao yêu cầu rà soát độc lập từ nhiều hơn một người dùng [các trạng thái song song của AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html). Các chỉ số hành vi được công bố dưới dạng các chỉ số tùy chỉnh với [phát hiện bất thường Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html), và các phát hiện từ [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) và [Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html) được tập trung trong [AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html). Các bài tập red team chạy theo một nhịp đã định dùng OWASP Top 10 for Agentic Applications làm thư viện kịch bản khởi đầu. |
| 4 | Chủ động (Proactive) | Chất lượng rà soát được quản lý qua các dashboard và các cảnh báo tổng hợp (composite alarms) tự động leo thang hoặc cách ly khi các chỉ số hành vi rà soát suy giảm. Rà soát mù và logic đồng thuận là mặc định cho các thao tác rủi ro cao, với các bất đồng được định tuyến tới các người rà soát cấp cao. Kiềm chế được tự động hóa qua các quy tắc [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rules.html) thu trạng thái pháp chứng tới [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html), thu hồi thông tin xác thực bằng cách gắn một chính sách deny-all vào vai trò IAM của agent, và phát tán các sự kiện cách ly cho các cầu dao ngắt trong các luồng công việc phụ thuộc. Các hoạt động purple team chạy sau mỗi chu kỳ đánh giá và cập nhật các cấu hình [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html), các quy tắc phát hiện và các runbook dựa trên các mẫu quan sát được. |
| 5 | Tối ưu (Optimized) | Các chỉ số chất lượng rà soát, các đường cơ sở hành vi của agent và các quy trình kiềm chế được điều chỉnh liên tục dựa trên các kết quả, và các kỹ thuật tấn công mới được đưa trực tiếp vào công cụ phát hiện và ứng phó. Các runbook kiềm chế được thực hành định kỳ qua [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) để kiểm chứng rằng việc cô lập, các cầu dao ngắt và việc thu pháp chứng hành xử như mong đợi. Các phát hiện của purple team, các xu hướng đánh giá của [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) và các tín hiệu đe dọa ở thời điểm chạy thúc đẩy việc tinh chỉnh liên tục các guardrail, các ngưỡng phát hiện và việc đào tạo người rà soát. |

## Các vấn đề thường gặp cần lưu ý

- Năng lực rà soát được lên kế hoạch chỉ theo khối lượng, không có các chỉ số phát hiện phê duyệt máy móc khi các hàng đợi ùn lại, nên sự giám sát của con người suy giảm âm thầm dưới tải khi người rà soát phê duyệt nhanh hơn khả năng đánh giá của họ.
- Người rà soát thấy các khuyến nghị của agent mà không có điểm độ tin cậy, các cờ bất thường, hay các quyết định tương tự trong quá khứ, và áp dụng cùng mức soi xét cho các hành động rủi ro cao và rủi ro thấp vì họ không có cơ sở để hiệu chỉnh sự chú ý của mình.
- Các thao tác rủi ro cao phụ thuộc vào một người phê duyệt duy nhất, hoặc nhiều người rà soát được phép thấy quyết định của nhau trước khi nộp quyết định của chính mình, biến quá trình rà soát thành hoặc một điểm thất bại đơn lẻ hoặc một bài tập về thiên kiến neo (anchoring bias).
- Phát hiện agent lừa đảo dựa vào các chỉ số hạ tầng thay vì các đường cơ sở hành vi theo từng agent, và việc cách ly đòi hỏi một con người hành động, nên một agent hoạt động ngoài phạm vi dự định của nó tiếp tục chạy hàng giờ khi những người ứng phó huy động lực lượng.
- Các đánh giá bảo mật là một lần, chung chung, hoặc tách rời khỏi các agent mà chúng dự định bảo vệ, nên các phát hiện không bao giờ chuyển hóa thành các guardrail, quy tắc phát hiện hay runbook sự cố được cập nhật.

###### Các thực hành tốt

- [AGENTSEC07-BP01 Triển khai quản lý tải nhận thức](agentsec07-bp01.md)
- [AGENTSEC07-BP02 Chỉ báo độ tin cậy rõ ràng và các cảnh báo thao túng](agentsec07-bp02.md)
- [AGENTSEC07-BP03 Nhiều người rà soát cho các thao tác quan trọng](agentsec07-bp03.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](agentsec07-bp04.md)
- [AGENTSEC07-BP05 Đánh giá bảo mật định kỳ và red teaming](agentsec07-bp05.md)
