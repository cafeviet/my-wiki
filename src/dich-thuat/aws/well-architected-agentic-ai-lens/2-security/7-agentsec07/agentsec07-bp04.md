# AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent

Phát hiện mà không kiềm chế để lại các vấn đề đã được nhận diện nhưng vẫn đang chạy. Kiềm chế mà không phát hiện dựa vào quan sát thủ công. Các đường cơ sở theo từng agent kết hợp với thu hồi thông tin xác thực tự động và thu pháp chứng chặn các agent bị ảnh hưởng trong vòng vài phút trong khi bảo tồn những gì các điều tra viên cần.

**Kết quả mong muốn:**

- Bạn thiết lập các đường cơ sở hành vi theo từng agent và kích hoạt các cảnh báo thời gian thực khi các sai lệch vượt qua các ngưỡng đã định.
- Bạn tự động cô lập các agent thể hiện hành vi bất thường trong vòng vài phút kể từ khi phát hiện qua thu hồi thông tin xác thực và kích hoạt cầu dao ngắt.
- Bạn thu trạng thái pháp chứng trước khi cô lập, và các khả năng ghi đè thủ công cho phép những người ứng phó sự cố cách ly hoặc khôi phục các agent khi cần phán đoán của con người.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ giám sát các chỉ số hạ tầng mà không có các chỉ báo hành vi riêng của agent, bỏ sót các tín hiệu như các mẫu lời gọi API, tần suất quyết định và khối lượng truy cập dữ liệu.
- Triển khai phát hiện bất thường mà không thiết lập các đường cơ sở hành vi trước, tạo ra quá nhiều dương tính giả hoặc các phát hiện bị bỏ sót.
- Dựa vào các quy trình cách ly thủ công đòi hỏi sự can thiệp của con người, để cho một agent bị ảnh hưởng tiếp tục hoạt động hàng giờ trong khi chờ phản hồi của con người.
- Hiện thực cách ly bằng cách dừng tiến trình agent mà không thu hồi thông tin xác thực, nên agent có thể được khởi động lại với cùng danh tính và quyền hạn.
- Không bảo tồn trạng thái và log của agent trước khi cách ly, mất bằng chứng pháp chứng từ bộ nhớ, các phiên hoạt động và các thao tác đang chờ của agent.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thu hồi thông tin xác thực tự động và kích hoạt cầu dao ngắt cô lập các agent bị ảnh hưởng trong vòng vài phút kể từ khi phát hiện.
- Bảo tồn pháp chứng qua việc thu trạng thái trước khi cô lập cung cấp bằng chứng cho việc điều tra mà không dựa vào các log của chính agent.
- Các cầu dao ngắt định tuyến các luồng công việc phụ thuộc tới các đường dự phòng an toàn thay vì cho phép các thất bại lan tràn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các tín hiệu hành vi khác nhau theo loại agent. Một agent RAG và một agent lập trình có các mẫu bình thường rất khác nhau, nên các ngưỡng chung tạo ra hoặc các báo động giả hoặc các phát hiện bị bỏ sót. Hãy bắt đầu với các danh mục chung (tốc độ lời gọi API, khối lượng truy cập dữ liệu, tần suất quyết định, tỷ lệ lỗi, tiêu thụ tài nguyên) nhưng chọn các phép đo cụ thể thực sự có ý nghĩa cho từng agent. Một agent hỗ trợ khách hàng có thể theo dõi khối lượng email gửi đi và các truy xuất xuyên khách hàng, một agent lập trình có thể theo dõi tốc độ commit và các lệnh được thực thi, và một agent phân tích dữ liệu có thể theo dõi khối lượng truy vấn và các phép join xuyên bảng. Phát hiện bất thường Amazon CloudWatch trên các chỉ số được chọn thiết lập các đường cơ sở động thích ứng với các mẫu biến thiên bình thường, giảm dương tính giả so với các ngưỡng tĩnh, và các cảnh báo kích hoạt khi các chỉ số lệch ra ngoài dải phát hiện bất thường.

[Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) thêm một lớp phát hiện ở cấp chất-lượng-hành-vi. Các trình đánh giá dựng sẵn (độ đúng đắn, độ chính xác lựa chọn công cụ, tính hữu ích, độ an toàn) là một điểm khởi đầu, nhưng các trình đánh giá tùy chỉnh nắm bắt các chiều chất lượng quan trọng cho agent của bạn — liệu các đầu ra có tuân theo chính sách của tổ chức bạn, liệu agent có đang dùng các công cụ mong đợi cho miền của nó, và liệu nó có hoàn thành tác vụ được giao. Một sự sụt giảm đột ngột trong các điểm đánh giá đóng vai trò một tín hiệu cảnh báo sớm rằng hành vi đang trôi dạt trước khi các cảnh báo bất thường ở cấp hạ tầng kích hoạt. Các cảnh báo Amazon CloudWatch về các điểm đánh giá cùng với các chỉ số hành vi cho bạn phát hiện phân lớp.

Hai dịch vụ bảo mật AWS thêm các tín hiệu bổ trợ mà bạn không cần tự trang bị. Amazon GuardDuty phân tích AWS CloudTrail, VPC flow log và DNS log để phát hiện các mẫu lời gọi API bất thường cho các vai trò IAM (các region bất ngờ, các tổ hợp dịch vụ bất thường, các IP được biết là độc hại), điều bắt được hành vi agent mà các chỉ số CloudWatch sẽ bỏ sót trừ khi bạn đo lường nó một cách tường minh. Amazon Macie kiểm tra các đối tượng Amazon S3 và các mẫu truy cập để tìm sự phơi bày dữ liệu nhạy cảm (các bucket được agent truy cập chứa các khối lượng bất thường PII hoặc thông tin xác thực), điều này trực giao với các chỉ số ở cấp API. AWS Security Hub CSPM tập trung các cảnh báo bất thường CloudWatch, các phát hiện GuardDuty và Macie để một bất thường từ một nguồn có thể được tương quan với các nguồn khác trong quá trình điều tra thay vì được xử lý cô lập.

Khi phát hiện bất thường kích hoạt trên một ngưỡng mức độ nghiêm trọng đã định, các quy tắc Amazon EventBridge gọi hoặc một hàm AWS Lambda hoặc một tài liệu AWS Systems Manager Automation. Lambda phù hợp với logic kiềm chế có các đường mã tùy chỉnh, các lời gọi API bên ngoài, hoặc rẽ nhánh có điều kiện hưởng lợi từ sự linh hoạt lập trình đầy đủ. SSM Automation phù hợp khi trình tự kiềm chế là một chuỗi các bước được định nghĩa rõ (các định nghĩa bước gốc, các tham số và khôi phục mà không cần mã) và bạn muốn cùng một mẫu runbook cho kiềm chế tự động và thủ công. Dù cách nào, trình tự chạy theo thứ tự này: thu một ảnh chụp pháp chứng bộ nhớ hiện tại, các phiên hoạt động và các thao tác đang chờ của agent tới Amazon S3, rồi thu hồi thông tin xác thực của agent bằng cách gắn một chính sách deny-all vào vai trò IAM của nó (bảo tồn vai trò cho phân tích pháp chứng), rồi phát tán một sự kiện cách ly qua Amazon EventBridge để thông báo các luồng công việc phụ thuộc kích hoạt logic cầu dao ngắt của chúng.

Các cầu dao ngắt trong các luồng công việc AWS Step Functions phụ thuộc vào các agent có thể cách ly xử lý tác động phía sau. Các trạng thái catch phát hiện sự không sẵn có của agent và định tuyến việc thực thi luồng công việc tới một đường dự phòng an toàn thay vì thất bại với một lỗi không được xử lý. Một giao diện ghi đè thủ công qua các runbook AWS Systems Manager Automation cho phép những người ứng phó sự cố cách ly hoặc khôi phục các agent qua một quy trình được kiểm soát, có thể kiểm toán, và việc ủy quyền nhiều người cho việc khôi phục giúp ngăn tái kích hoạt sớm.

### Các bước triển khai

- **Chọn các chỉ số riêng của agent và thiết lập đường cơ sở cho chúng:** Chọn các chỉ số có ý nghĩa cho từng agent từ các danh mục chung, cấu hình phát hiện bất thường Amazon CloudWatch trên chúng, và thiết lập các đường cơ sở trong quá trình vận hành bình thường.
- **Thêm cảnh báo sớm dựa trên đánh giá:** Triển khai [Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) với các trình đánh giá dựng sẵn và tùy chỉnh, và cấu hình các cảnh báo Amazon CloudWatch về các điểm đánh giá.
- **Tập trung các phát hiện bảo mật:** Bật Amazon GuardDuty và Amazon Macie cho mọi tài khoản agent và tập trung các phát hiện trong AWS Security Hub CSPM.
- **Tự động hóa kiềm chế khi vượt ngưỡng:** Hiện thực các quy tắc Amazon EventBridge gọi AWS Lambda hoặc AWS Systems Manager Automation khi mức độ nghiêm trọng của bất thường vượt các ngưỡng, và tuần tự hóa thu pháp chứng, thu hồi thông tin xác thực và phát tán sự kiện cách ly.
- **Đấu nối các cầu dao ngắt vào các luồng công việc phụ thuộc:** Cấu hình các trạng thái catch trong các luồng công việc AWS Step Functions phụ thuộc vào các agent có thể cách ly, định tuyến tới các đường dự phòng an toàn khi agent không sẵn có.
- **Cung cấp một runbook thủ công với ủy quyền nhiều người:** Tạo các runbook AWS Systems Manager Automation cho cách ly và khôi phục thủ công với ủy quyền nhiều người được yêu cầu cho việc khôi phục.
- **Kiểm thử hàng quý:** Chạy các bài kiểm thử quy trình kiềm chế mỗi quý để kiểm chứng việc cô lập, các cầu dao ngắt và việc thu pháp chứng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)
- [AGENTSEC06-BP02 Triển khai các kiểm soát bảo mật điều phối luồng công việc](../6-agentsec06/agentsec06-bp02.md)
- [AGENTSEC06-BP04 Giám sát và phát hiện các bất thường trong phối hợp](../6-agentsec06/agentsec06-bp04.md)
- [AGENTREL02-BP03 Triển khai phát hiện bất thường hành vi và giám sát](../../3-reliability/2-agentrel02/agentrel02-bp03.md)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các thất bại thực thi của agent](../../3-reliability/7-agentrel07/agentrel07-bp02.md)

**Tài liệu liên quan:**

- [Amazon CloudWatch anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
- [Tài liệu Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Tài liệu Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)
- [Amazon Macie](https://aws.amazon.com/macie/)
- [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [AWS Systems Manager](https://aws.amazon.com/systems-manager/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
