# AGENTSEC09-BP03 Triển khai kiểm chứng bảo mật liên tục với khắc phục tự động

Các đánh giá định kỳ để lại các năng lực agent mới triển khai bị phơi bày trong nhiều tuần hoặc nhiều tháng. Kiểm chứng theo yêu cầu được tích hợp vào đường ống phát triển, kết hợp với các gợi ý sửa tự động, nén vòng lặp phát-hiện-đến-giải-quyết từ nhiều tuần xuống nhiều giờ.

**Kết quả mong muốn:**

- Bạn chạy kiểm chứng bảo mật liên tục hoặc theo yêu cầu như một phần của đường ống phát triển và triển khai thay vì chỉ trong các cửa sổ đánh giá định kỳ.
- Các phát hiện đã được kiểm chứng đến kèm các bản sửa mã sẵn sàng để hiện thực và các khuyến nghị cấu hình, để các nhóm phát triển khắc phục các vấn đề mà không phải chờ sự can thiệp của đội bảo mật.
- Bạn theo dõi tiến độ khắc phục một cách tự động, và kiểm thử hồi quy xác nhận các bản sửa có hiệu quả và không đưa vào các lỗ hổng mới.

**Các phản mẫu thường gặp (anti-patterns):**

- Giới hạn kiểm thử xâm nhập ở các chu kỳ hằng năm hoặc hàng quý, để các năng lực agent mới triển khai không được kiểm thử trong các kỳ dài vì các hệ thống tác tử tiến hóa nhanh với các tích hợp công cụ mới và các mở rộng năng lực.
- Chuyển giao các phát hiện lỗ hổng mà không có hướng dẫn khắc phục thực tế, tạo ra một nút thắt cổ chai nơi các nhóm phát triển chờ chuyên môn bảo mật để hiểu cách sửa các vấn đề.
- Coi khắc phục tách rời khỏi phát hiện, mất ngữ cảnh giữa nhóm đã nhận diện vấn đề và nhóm phải sửa nó và dẫn đến các bản sửa không đầy đủ xử lý các triệu chứng thay vì các nguyên nhân gốc.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm thử theo yêu cầu kiểm chứng bảo mật bất cứ khi nào các năng lực mới được triển khai hoặc các thay đổi đáng kể được thực hiện, nén cửa sổ phơi bày.
- Các gợi ý sửa tự động cho các nhóm phát triển các thay đổi mã sẵn sàng để hiện thực, đóng vòng lặp giữa phát hiện và giải quyết.
- Tái kiểm thử tự động xác nhận các bản sửa có hiệu quả và không đưa vào các lỗ hổng mới.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Giá trị của kiểm chứng bảo mật tỷ lệ với tốc độ nó chạy so với tốc độ ứng dụng thay đổi. Kiểm thử hàng quý so với một codebase thay đổi hàng tuần để lại phần lớn ứng dụng không được kiểm thử phần lớn thời gian, và các hệ thống tác tử thay đổi nhanh hơn các ứng dụng truyền thống vì các tích hợp công cụ mới và các mở rộng năng lực xuất xưởng liên tục. Tích hợp kiểm chứng vào các đường ống CI/CD để nó chạy trên mỗi thay đổi đáng kể giữ độ bao phủ kiểm thử căn chỉnh với sự tiến hóa của ứng dụng.

Hãy cấu hình các trigger cho kiểm thử theo yêu cầu khi các năng lực agent mới được thêm, các tích hợp công cụ được chỉnh sửa, hoặc các ranh giới quyền hạn được thay đổi. [AWS Security Agent](https://aws.amazon.com/security-agent/) biến kiểm thử xâm nhập từ một quy trình thủ công kéo dài nhiều tuần thành một năng lực theo yêu cầu hoàn thành trong nhiều giờ. Mỗi phát hiện đã được kiểm chứng mang phân tích tác động, một đường tấn công có thể tái tạo, và một bản sửa mã sẵn sàng để hiện thực, đó là thứ cho phép các nhóm phát triển khắc phục mà không phải chờ chuyên môn bảo mật chuyên biệt. Các đội bảo mật định nghĩa các yêu cầu của tổ chức một lần và AWS Security Agent kiểm chứng chúng trong mỗi lần rà soát thiết kế và mã, cung cấp thực thi nhất quán ở quy mô.

Theo dõi khắc phục giám sát tiến độ sửa từ phát hiện đến giải quyết. Hãy lưu các kết quả kiểm thử và trạng thái khắc phục trong một hệ thống tập trung, và cấu hình kiểm thử hồi quy tự động chạy lại các kịch bản kiểm thử liên quan sau khi các bản sửa được áp dụng để xác nhận hiệu quả. Amazon CloudWatch thu các chỉ số kiểm chứng bảo mật quan trọng: thời gian-đến-lúc-phát-hiện, thời gian-đến-lúc-khắc-phục, và các tỷ lệ hiệu quả của bản sửa.

Các hệ thống tác tử cần các trigger kiểm chứng mà các ứng dụng truyền thống không cần. Hãy kích hoạt kiểm chứng bảo mật bất cứ khi nào các system prompt của agent được chỉnh sửa, các công cụ mới được đăng ký, các phạm vi quyền hạn được thay đổi, hoặc các mẫu điều phối đa agent được cập nhật. Các thay đổi này đưa vào các lỗ hổng không được bắt bởi quét ở cấp mã tiêu chuẩn vì chúng ảnh hưởng đến hành vi của agent ở lớp suy luận và điều phối.

### Các bước triển khai

- **Đấu nối kiểm chứng vào CI/CD:** Tích hợp [AWS Security Agent](https://aws.amazon.com/security-agent/) vào các đường ống CI/CD với các trigger cho kiểm chứng bảo mật theo yêu cầu khi các năng lực agent, các tích hợp công cụ hoặc các ranh giới quyền hạn thay đổi.
- **Chạy rà soát mã và thiết kế trên mỗi PR:** Cấu hình các rà soát bảo mật mã và thiết kế tự động chạy trên mỗi pull request, cho các lập trình viên phản hồi thời gian thực trong quá trình phát triển.
- **Định tuyến các phát hiện kèm bản sửa tới các chủ sở hữu:** Thiết lập một luồng công việc khắc phục định tuyến các phát hiện đã được kiểm chứng kèm các bản sửa mã được gợi ý tới nhóm phát triển phù hợp và theo dõi tiến độ đến khi giải quyết.
- **Tái kiểm thử sau các bản sửa một cách tự động:** Hiện thực kiểm thử hồi quy chạy lại các kịch bản kiểm thử bảo mật liên quan sau khi các bản sửa được áp dụng để xác nhận hiệu quả.
- **Đo lường và cải thiện:** Giám sát các chỉ số kiểm chứng bảo mật (thời gian-đến-lúc-phát-hiện, thời gian-đến-lúc-khắc-phục, hiệu quả của bản sửa) trong Amazon CloudWatch và rà soát các xu hướng để nhận diện các cải thiện quy trình.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC09-BP01 Tích hợp quét lỗ hổng có AI hỗ trợ trên toàn vòng đời phát triển](agentsec09-bp01.md)
- [AGENTSEC09-BP02 Tiến hành kiểm thử xâm nhập có nhận thức ngữ cảnh với mô phỏng tấn công đa agent](agentsec09-bp02.md)
- [AGENTSEC07-BP05 Đánh giá bảo mật định kỳ và red teaming](../7-agentsec07/agentsec07-bp05.md)

**Tài liệu liên quan:**

- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [AWS Security Agent FAQs](https://aws.amazon.com/security-agent/faqs/)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
