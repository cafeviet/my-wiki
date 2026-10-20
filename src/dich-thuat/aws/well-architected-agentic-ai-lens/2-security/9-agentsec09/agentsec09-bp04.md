# AGENTSEC09-BP04 Thiết lập các môi trường kiểm thử giới hạn phạm vi và được kiểm soát cho các đánh giá bảo mật agent

Kiểm thử xâm nhập chạy các ý đồ khai thác thực đối với các agent sản xuất có thể kích hoạt các lời gọi công cụ, làm hỏng bộ nhớ, hoặc phơi bày dữ liệu nhạy cảm. Các môi trường kiểm thử giới hạn phạm vi với các thông tin xác thực riêng và trạng thái agent cô lập cho phép các nhóm chạy các đánh giá kỹ lưỡng mà không mạo hiểm tác động đến sản xuất.

**Kết quả mong muốn:**

- Bạn tiến hành các đánh giá bảo mật cho các hệ thống AI tác tử trong các môi trường được kiểm soát với phạm vi được định nghĩa rõ ràng, các thông tin xác thực riêng và sự cô lập khỏi các hệ thống sản xuất.
- Bạn quản lý các thông tin xác thực kiểm thử qua các dịch vụ vault an toàn với xoay vòng tự động, và các hoạt động kiểm thử được ghi log trong tài khoản của bạn để có khả năng kiểm toán đầy đủ.
- Môi trường kiểm thử tái tạo hành vi agent sản xuất đủ sát để tạo ra các phát hiện hợp lệ trong khi kiềm chế phạm vi của các ý đồ khai thác.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các bài kiểm thử xâm nhập trực tiếp đối với các hệ thống tác tử sản xuất mà không có các kiểm soát phạm vi, mạo hiểm việc các agent thực thi các lời gọi công cụ đối với các cơ sở dữ liệu sản xuất, gửi các thông điệp tới người dùng thực, hoặc kích hoạt các luồng công việc phía sau để đáp lại các đầu vào kiểm thử.
- Dùng các thông tin xác thực dùng chung hoặc dài hạn cho kiểm thử bảo mật, tạo ra rủi ro phơi bày thông tin xác thực nơi các thông tin xác thực kiểm thử có thể bị bắt trong các log, các tạo phẩm kiểm thử hoặc các báo cáo phát hiện.
- Không cô lập các thể hiện agent kiểm thử khỏi bộ nhớ và trạng thái agent sản xuất, để cho các đầu vào kiểm thử và các payload tấn công làm ô nhiễm bộ nhớ agent sản xuất và tác động đến hành vi agent tương lai đối với người dùng thực.

**Lợi ích khi áp dụng thực hành tốt này:**

- Cô lập môi trường cho phép đánh giá bảo mật kỹ lưỡng, bao gồm các ý đồ khai thác thực, mà không mạo hiểm tác động đến sản xuất hoặc làm hỏng dữ liệu.
- Các dịch vụ vault giới hạn sự phơi bày thông tin xác thực trong quá trình kiểm thử và hỗ trợ xoay vòng tự động sau các chu kỳ đánh giá.
- Các log kiểm thử được lưu trong tài khoản của bạn cung cấp khả năng nhìn thấy đầy đủ về các hoạt động kiểm thử phục vụ tuân thủ và điều tra sự cố.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một agent đang được kiểm thử bảo mật là một agent đang thực thi các ý đồ khai thác. Trong sản xuất, một agent chạy một payload khai thác sẽ thực sự gọi công cụ nó được bảo gọi, gửi email nó được bảo gửi, và ghi vào bộ nhớ nó được bảo chỉnh sửa. Yêu cầu kiềm chế do đó mang tính cấu trúc: môi trường kiểm thử cần trông đủ giống sản xuất để tạo ra các phát hiện hợp lệ, và nó cần được tách khỏi sản xuất đủ để các ý đồ khai thác không thể chạm tới các tài nguyên thực.

Hãy cấp phát các môi trường kiểm thử riêng tái tạo kiến trúc agent, các tích hợp công cụ và các luồng dữ liệu của sản xuất trong khi duy trì sự cô lập. Hãy dùng các thể hiện agent riêng với các kho bộ nhớ, các điểm cuối công cụ và các ranh giới quyền hạn của riêng chúng. Cấu hình các môi trường kiểm thử để dùng các phiên bản giả (mock) hoặc sandbox của các dịch vụ bên ngoài nơi không cần kết nối sản xuất đầy đủ cho các kết quả kiểm thử hợp lệ.

Hãy quản lý các thông tin xác thực kiểm thử qua AWS Secrets Manager, lưu các thông tin xác thực tĩnh (username và password) một cách an toàn và hỗ trợ cấp phát thông tin xác thực động qua các hàm AWS Lambda cho các kịch bản xác thực phức tạp hơn. [AWS Security Agent](https://aws.amazon.com/security-agent/) hỗ trợ cả các thông tin xác thực tĩnh được lưu trong AWS Secrets Manager lẫn các thông tin xác thực động được truy cập qua các hàm AWS Lambda, cho xác thực linh hoạt thích ứng với các kiến trúc ứng dụng khác nhau. Hãy xoay vòng các thông tin xác thực kiểm thử sau mỗi chu kỳ đánh giá và kiểm toán các log truy cập thông tin xác thực để phát hiện bất kỳ việc dùng trái phép nào.

Định nghĩa phạm vi là một điều kiện tiên quyết, không phải một suy nghĩ chợt đến sau. Hãy chỉ định trước mỗi cuộc đánh giá những điểm cuối agent, các tích hợp công cụ và các kho dữ liệu nào nằm trong phạm vi và những cái nào bị loại trừ tường minh. Với kiểm thử xâm nhập của AWS Security Agent, hãy cung cấp các URL đích, các chi tiết xác thực, mã nguồn và tài liệu để agent có thể phát triển ngữ cảnh ứng dụng trong phạm vi đã định. Mọi log kiểm thử được lưu trong Amazon CloudWatch trong tài khoản của bạn để có khả năng nhìn thấy đầy đủ.

Với các hệ thống đa agent, hãy kiểm thử các đường giao tiếp agent-tới-agent một cách cô lập trước khi kiểm thử toàn bộ chuỗi điều phối. Cách tiếp cận đó nhận diện các vi phạm ranh giới tin cậy và các vấn đề ủy thác ở cấp tương tác riêng lẻ trước khi chúng tích lũy trong các kịch bản đa agent phức tạp. Phân đoạn mạng và các chính sách IAM giúp ngăn các thể hiện agent kiểm thử chạm tới các tài nguyên sản xuất.

### Các bước triển khai

- **Cấp phát các môi trường kiểm thử cô lập:** Tái tạo kiến trúc agent sản xuất với các kho bộ nhớ, các điểm cuối công cụ và các ranh giới quyền hạn cô lập.
- **Quản lý các thông tin xác thực trong Secrets Manager:** Lưu các thông tin xác thực kiểm thử trong AWS Secrets Manager với các chính sách xoay vòng tự động, hoặc dùng các hàm AWS Lambda cho cấp phát thông tin xác thực động cho các kịch bản xác thực phức tạp.
- **Định nghĩa và ghi tài liệu phạm vi kiểm thử:** Chỉ định các điểm cuối agent, các tích hợp công cụ và các kho dữ liệu nằm trong phạm vi cho mỗi cuộc đánh giá, với các loại trừ tường minh cho các tài nguyên sản xuất nhạy cảm.
- **Kiềm chế phạm vi ở các lớp mạng và IAM:** Cấu hình phân đoạn mạng và các chính sách IAM giúp ngăn các thể hiện agent kiểm thử truy cập các tài nguyên sản xuất.
- **Kiểm chứng việc ghi log kiểm thử trong CloudWatch:** Xác nhận mọi log kiểm thử được thu trong Amazon CloudWatch trong tài khoản của bạn, và rà soát các log sau mỗi cuộc đánh giá để xác nhận việc tuân thủ phạm vi và nhận diện các tương tác ngoài ý muốn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC09-BP02 Tiến hành kiểm thử xâm nhập có nhận thức ngữ cảnh với mô phỏng tấn công đa agent](agentsec09-bp02.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](../3-agentsec03/agentsec03-bp03.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](../7-agentsec07/agentsec07-bp04.md)

**Tài liệu liên quan:**

- [Security Considerations for AWS Security Agent and AI assisted penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)
- [AWS Security Agent FAQs](https://aws.amazon.com/security-agent/faqs/)
- [Tài liệu AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS Well-Architected Framework, Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

**Dịch vụ liên quan:**

- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
