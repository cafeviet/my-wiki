# AGENTSEC07-BP03 Nhiều người rà soát cho các thao tác quan trọng

Một người rà soát duy nhất là một điểm thất bại đơn lẻ, cho cả các lỗi ngay thẳng lẫn tấn công phi kỹ thuật (social engineering). Các cuộc rà soát độc lập, mù cho các quyết định rủi ro cao là mẫu chiều sâu phòng thủ, quen thuộc dưới tên nguyên tắc bốn-mắt (four-eyes principle), giữ việc phê duyệt đơn phương ra khỏi đường đi.

**Kết quả mong muốn:**

- Các quyết định agent rủi ro cao nhận được rà soát độc lập từ nhiều người rà soát đủ điều kiện, với các quy trình rà soát mù giúp ngăn thiên kiến neo (anchoring bias).
- Bạn giải quyết các bất đồng qua leo thang thay vì mặc định về phê duyệt.
- Bạn ghi log mọi quyết định rà soát với các danh tính người rà soát và các dấu thời gian phục vụ mục đích kiểm toán.

**Các phản mẫu thường gặp (anti-patterns):**

- Cho mỗi người rà soát thấy quyết định của người rà soát trước đó trước khi họ nộp quyết định của chính mình, đưa vào thiên kiến neo làm suy yếu tính độc lập.
- Mặc định về phê duyệt khi các người rà soát bất đồng, để một người rà soát phê duyệt đơn lẻ thực chất ghi đè một người rà soát chặn.
- Gán nhiều lần rà soát cho các người rà soát từ cùng một nhóm hoặc chuỗi báo cáo, làm giảm tính độc lập của quy trình.

**Lợi ích khi áp dụng thực hành tốt này:**

- Nhiều cuộc rà soát độc lập cung cấp chiều sâu phòng thủ cho sự giám sát của con người, loại bỏ điểm thất bại đơn lẻ trong quy trình rà soát.
- Các quyết định, danh tính và dấu thời gian của từng người rà soát được ghi log hỗ trợ tuân thủ và cho phép điều tra các bất thường phê duyệt.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Thực thi song song điều phối tốt các luồng công việc nhiều người rà soát. Các nhánh thực thi song song của AWS Step Functions gửi một yêu cầu rà soát độc lập tới một người rà soát khác nhau qua Amazon SNS, và luồng công việc chờ mọi nhánh hoàn tất trước khi đánh giá đồng thuận. Rà soát mù đến từ việc không bao gồm các quyết định của người rà soát trước đó trong nội dung thông báo, để mỗi người rà soát đánh giá quyết định một cách độc lập.

Logic đồng thuận thuộc về một hàm AWS Lambda đánh giá các quyết định đã thu thập. Các luồng công việc hai người rà soát đòi hỏi phê duyệt nhất trí. Ba người rà soát trở lên dùng luật đa số với leo thang cho các quyết định chia rẽ, và các đường leo thang định tuyến các bất đồng tới một người rà soát cấp cao có khả năng nhìn thấy đầy đủ các quyết định riêng lẻ và lý do của chúng.

Lựa chọn người rà soát quan trọng ngang với cơ chế. Hãy chọn các người rà soát từ các nhóm hoặc đơn vị tổ chức khác nhau để tối đa hóa tính độc lập. Các người rà soát chia sẻ một người quản lý hoặc làm việc chặt chẽ với nhau có xu hướng đi đến cùng một kết luận vì các lý do xã hội hơn là phân tích. AWS IAM Identity Center quản lý các danh tính người rà soát để các lần gán được theo dõi và có thể kiểm toán.

Các bản ghi kiểm toán cư trú trong Amazon S3 với danh tính người rà soát, dấu thời gian, quyết định (chấp thuận hoặc từ chối), và lý do tùy chọn. Hãy gắn thẻ các bản ghi bằng ID thao tác agent liên quan để cho phép tương quan với các log thực thi của agent trong các cuộc điều tra.

### Các bước triển khai

- **Điều phối các cuộc rà soát song song mù:** Thiết kế các luồng công việc nhiều người rà soát trong AWS Step Functions với các nhánh song song, một nhánh cho mỗi người rà soát, gửi các yêu cầu rà soát mù độc lập qua Amazon SNS.
- **Hiện thực đồng thuận và leo thang:** Đánh giá các quyết định đã thu thập trong một hàm AWS Lambda — nhất trí cho các luồng hai người rà soát, luật đa số với leo thang cho ba người trở lên.
- **Định tuyến các quyết định chia rẽ tới các người rà soát cấp cao:** Cấu hình các đường leo thang cho các người rà soát cấp cao khả năng nhìn thấy các quyết định riêng lẻ và lý do.
- **Chọn các người rà soát từ các nhóm khác nhau:** Dùng AWS IAM Identity Center để quản lý các danh tính người rà soát và theo dõi các lần gán, và rút các người rà soát từ các đơn vị tổ chức khác nhau.
- **Lưu bền vững các quyết định tới S3:** Lưu mọi quyết định rà soát trong Amazon S3 với danh tính người rà soát, dấu thời gian và lý do quyết định, gắn thẻ các bản ghi bằng ID thao tác agent để tương quan với các log thực thi.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](../4-agentsec04/agentsec04-bp02.md)
- [AGENTSEC07-BP01 Triển khai quản lý tải nhận thức](agentsec07-bp01.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](agentsec07-bp04.md)

**Tài liệu liên quan:**

- [AWS Step Functions parallel states](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html)
- [Human approval in Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html)
- [Implement human-in-the-loop confirmation with Amazon Bedrock Agents](https://aws.amazon.com/blogs/machine-learning/implement-human-in-the-loop-confirmation-with-amazon-bedrock-agents/)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon SNS](https://aws.amazon.com/sns/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/)
