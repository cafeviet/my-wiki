# AGENTSEC07-BP01 Triển khai quản lý tải nhận thức

Một người rà soát của con người chỉ hiệu quả tương xứng với mức khối lượng công việc cho phép. Ưu tiên hóa, quản lý hàng đợi và các tốc độ rà soát tối đa giữ cho sự giám sát của con người neo vào phán đoán thực sự thay vì phê duyệt máy móc do mệt mỏi.

**Kết quả mong muốn:**

- Những người rà soát của con người nhận một khối lượng quyết định có thể quản lý được, được ưu tiên tốt, với đủ ngữ cảnh và thời gian để đưa ra các phán đoán có hiểu biết.
- Bạn giám sát các hàng đợi rà soát để tìm sự tích lũy tồn đọng, với leo thang tự động hoặc cân bằng tải giúp ngăn bất kỳ người rà soát đơn lẻ nào bị quá tải.
- Các chỉ số chất lượng rà soát phát hiện các dấu hiệu phê duyệt máy móc chỉ báo quá tải nhận thức.

**Các phản mẫu thường gặp (anti-patterns):**

- Định tuyến mọi quyết định của agent cần rà soát tới một hàng đợi duy nhất mà không ưu tiên hóa, nên các quyết định bảo mật ưu tiên cao chờ phía sau các phê duyệt thường lệ.
- Không giám sát khối lượng công việc của người rà soát hay độ sâu hàng đợi, để cho các tồn đọng tích lũy âm thầm cho đến khi người rà soát bắt đầu phê duyệt mà không đánh giá đầy đủ.
- Không đặt tốc độ rà soát tối đa cho mỗi người, nên một người rà soát duy nhất có thể được giao một số lượng quyết định không giới hạn trong một khoảng ngắn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản lý khối lượng công việc giữ người rà soát ở vị thế đưa ra các quyết định thực sự, có hiểu biết thay vì phê duyệt máy móc dưới áp lực.
- Các chỉ số chất lượng rà soát (thời gian rà soát trung bình, tỷ lệ phê duyệt) làm nổi bật khi quá trình giám sát đang đổ vỡ, cho phép can thiệp trước khi nó thất bại âm thầm.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Các hàng đợi tiêu chuẩn của Amazon SQS không hỗ trợ thứ tự ưu tiên một cách gốc, nên lớp ưu tiên hóa phải nằm bên trên hàng đợi. Một lựa chọn thô là các hàng đợi Amazon SQS riêng cho từng tầng ưu tiên (cao, trung bình, thấp), nơi hàm gán poll ưu tiên cao trước và chỉ lùi về các tầng thấp hơn khi tầng trên rỗng. Một lựa chọn linh hoạt hơn dùng một hàng đợi nạp duy nhất được tiêu thụ bởi một hàm AWS Lambda phân loại mỗi yêu cầu theo ưu tiên và ghi nó vào một bảng Amazon DynamoDB với một sort key dựa trên ưu tiên và thời gian gửi. Hàm gán người rà soát truy vấn DynamoDB tìm các mục chưa được gán có ưu tiên cao nhất, đánh dấu chúng là đã gán, và chuyển chúng tới người rà soát. Mẫu DynamoDB cho bạn toàn quyền kiểm soát logic ưu tiên hóa, hỗ trợ tái-ưu-tiên các mục đang chờ, và giữ một bản ghi bền vững của mọi yêu cầu rà soát bất kể trạng thái hiện tại của chúng. Các mục không được gán ngay nằm lại trong DynamoDB thay vì nằm trong một hàng đợi với một visibility timeout đang hết hạn.

Phân loại ưu tiên là về tác động tiềm tàng của việc hành động tiến hành sai: một phê duyệt sai càng gây thiệt hại thì ưu tiên càng cao. Các yếu tố cụ thể bao gồm độ nhạy dữ liệu (PII, hồ sơ tài chính, thông tin y tế), khả năng đảo ngược (các thao tác xóa, giao tiếp bên ngoài và giao dịch tài chính không thể hoàn tác), liệu hành động có phải là một thao tác lần đầu cho agent này (không có đường cơ sở hành vi, nên người rà soát không thể khớp mẫu để rút gọn phán đoán, và bản thân thao tác lần đầu là một tín hiệu đáng điều tra), và độ nhạy thời gian (các thao tác trở nên khó đảo ngược hơn theo thời gian, hoặc nơi sự trì hoãn có cái giá riêng của nó). Hãy tự động hóa việc phân loại bằng cách gắn thẻ các yêu cầu rà soát với metadata từ ngữ cảnh gọi công cụ của agent, các thẻ phân loại dữ liệu trên các tài nguyên đích, và các mẫu sử dụng lịch sử của agent.

Amazon CloudWatch theo dõi bảng rà soát DynamoDB để tìm sự tích lũy tồn đọng (các mục chưa được gán theo tầng ưu tiên), thời gian-đến-lúc-gán trung bình, và thời gian-đến-lúc-quyết-định trung bình. Các cảnh báo kích hoạt khi các mục ưu tiên cao còn chưa được gán vượt qua các ngưỡng đã định.

Cân bằng tải người rà soát phân phối các quyết định qua các người rà soát sẵn có dựa trên khối lượng công việc hiện tại. Amazon DynamoDB theo dõi số lượng gán và tình trạng sẵn có của người rà soát, và một hàm gán dựa trên AWS Lambda định tuyến các quyết định mới tới người rà soát có tải hiện tại thấp nhất. Hãy cấu hình các giới hạn gán tối đa cho mỗi người rà soát trong mỗi cửa sổ thời gian để giúp ngăn quá tải.

Các chỉ số chất lượng rà soát là chỉ báo trễ (trailing indicator). Hãy theo dõi thời gian rà soát trung bình, tỷ lệ phê duyệt, và tỷ lệ đảo ngược quyết định (các trường hợp mà một người rà soát thứ hai ghi đè người đầu tiên), công bố các chỉ số tới Amazon CloudWatch, và cảnh báo về các mẫu gợi ý phê duyệt máy móc: các thời gian rà soát ngắn bất thường hoặc các tỷ lệ phê duyệt cao bất thường trong các kỳ có khối lượng hàng đợi cao. Leo thang tự động định tuyến các quyết định chưa được rà soát vượt qua các ngưỡng thời gian đã định tới các người rà soát cấp cao, hoặc kích hoạt một mặc định an toàn (thường là chặn thao tác) để giúp ngăn các trì hoãn vô thời hạn.

Các ranh giới phê duyệt — một phê duyệt còn hiệu lực bao lâu, liệu nó có thể bị thu hồi, liệu các thao tác rủi ro cao có yêu cầu xác nhận lại nâng cấp (step-up) — được bao phủ trong AGENTSEC04-BP02, tài liệu này trình bày chi tiết các mẫu tin cậy bền vững quyết định phạm vi và vòng đời của mỗi quyết định phê duyệt.

### Các bước triển khai

- **Thiết lập đường ống nạp-phân-loại-lưu:** Dùng một hàng đợi nạp Amazon SQS, một trình phân loại AWS Lambda gán ưu tiên, và một bảng rà soát Amazon DynamoDB với một sort key trên ưu tiên và thời gian gửi.
- **Xây dựng hàm gán người rà soát:** Truy vấn bảng DynamoDB tìm các mục chưa được gán có ưu tiên cao nhất, đánh dấu chúng là đã gán, và chuyển chúng tới người rà soát phù hợp.
- **Chặn số lượng gán cho mỗi người rà soát và leo thang:** Đặt các giới hạn gán rà soát tối đa cho mỗi người rà soát trong mỗi cửa sổ thời gian và cấu hình leo thang tự động khi các giới hạn bị đạt hoặc các mục ưu tiên cao già quá các ngưỡng.
- **Đo lường chất lượng rà soát:** Theo dõi thời gian rà soát trung bình, tỷ lệ phê duyệt và tỷ lệ đảo ngược trong Amazon CloudWatch, và cấu hình các cảnh báo về các mẫu gợi ý phê duyệt máy móc.
- **Giám sát bảng rà soát:** Cảnh báo về sự tích lũy tồn đọng theo tầng ưu tiên, thời gian-đến-lúc-gán trung bình, và thời gian-đến-lúc-quyết-định trung bình, và cảnh báo khi các mục ưu tiên cao già quá các ngưỡng.
- **Rà soát các chỉ số tải định kỳ:** Dùng các chỉ số tải nhận thức để tinh chỉnh logic ưu tiên hóa và việc lập kế hoạch năng lực người rà soát theo một nhịp định kỳ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](../4-agentsec04/agentsec04-bp02.md)
- [AGENTSEC07-BP03 Nhiều người rà soát cho các thao tác quan trọng](agentsec07-bp03.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](agentsec07-bp04.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [AWS Step Functions human approval](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html)
- [Implement human-in-the-loop confirmation with Amazon Bedrock Agents](https://aws.amazon.com/blogs/machine-learning/implement-human-in-the-loop-confirmation-with-amazon-bedrock-agents/)

**Dịch vụ liên quan:**

- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon SNS](https://aws.amazon.com/sns/)
