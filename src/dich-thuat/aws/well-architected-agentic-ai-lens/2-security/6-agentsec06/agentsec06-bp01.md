# AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent

Mã hóa ở cấp vận chuyển ngừng bảo vệ payload ngay khoảnh khắc một thông điệp đáp vào một hàng đợi hoặc bus sự kiện. Ký và mã hóa ở cấp thông điệp với khóa theo từng vùng tin cậy cho các agent nhận chứng minh bằng mật mã về danh tính người gửi và tính toàn vẹn nội dung, bất kể thông điệp đã nhảy qua bao nhiêu chặng.

**Kết quả mong muốn:**

- Bạn bảo vệ các thông điệp giữa các agent ở cấp thông điệp bằng mã hóa và ký, độc lập với bảo mật ở cấp vận chuyển.
- Các agent nhận kiểm chứng chữ ký thông điệp trước khi hành động theo các chỉ thị từ các agent khác.
- Các thông điệp được lưu trong hàng đợi hoặc bus sự kiện được mã hóa tại chỗ với các khóa được giới hạn phạm vi theo vùng tin cậy phù hợp.
- Các agent không thể giả mạo các thông điệp trông có vẻ phát sinh từ các agent khác trong luồng công việc phối hợp.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ dựa vào mã hóa ở cấp vận chuyển (TLS) mà không có ký ở cấp thông điệp, nên các thông điệp được lưu trong hàng đợi hoặc bus sự kiện không thể được kiểm chứng về việc bị can thiệp tại thời điểm tiêu thụ.
- Dùng một khóa mã hóa dùng chung duy nhất trên mọi agent, nên một sự phơi bày khóa ảnh hưởng đến mọi thông điệp giữa các agent thay vì chỉ những thông điệp trong một vùng tin cậy.
- Không kiểm chứng chữ ký thông điệp trước khi hành động theo các chỉ thị giữa các agent, để cho một agent hành động theo các chỉ thị bị giả mạo hoặc bị can thiệp mà không có kiểm tra toàn vẹn nào.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm chứng tính toàn vẹn ở cấp thông điệp tồn tại vượt ra ngoài lớp vận chuyển, nên các thông điệp được lưu trong hàng đợi hoặc bus sự kiện có thể được kiểm chứng tại thời điểm tiêu thụ.
- Quản lý khóa có giới hạn phạm vi giới hạn tác động của một sự phơi bày khóa vào một vùng tin cậy duy nhất thay vì toàn bộ hệ thống đa agent.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hai thuộc tính riêng biệt đang bị đe dọa: ai đã gửi thông điệp (được bao phủ bởi AGENTSEC03-BP01 cho việc xác thực) và liệu nội dung có đúng là những gì người gửi thực sự gửi. Mã hóa ở cấp vận chuyển cung cấp thuộc tính thứ hai chỉ trong khi thông điệp đang trên đường truyền. Ngay khoảnh khắc thông điệp đáp vào một hàng đợi Amazon SQS, một bus Amazon EventBridge hoặc một state machine AWS Step Functions, không có tầng vận chuyển nào để bảo vệ nó, và bất kỳ chỉnh sửa nào giữa lúc chuyển và lúc tiêu thụ đều vô hình. Ký ở cấp thông điệp cung cấp chứng minh bằng mật mã rằng một thông điệp cụ thể đã được gửi bởi một agent cụ thể và chưa bị chỉnh sửa, bất kể nó đã đi qua bao nhiêu dịch vụ trung gian.

Phạm vi quan trọng. Với giao tiếp agent-tới-agent trực tiếp trong một vùng tin cậy duy nhất, bảo mật ở cấp vận chuyển và xác thực do [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/) cung cấp (TLS 1.2+ với OAuth 2.0 hoặc SigV4) thường là đủ. Hãy xếp thêm ký thông điệp lên trên khi tính toàn vẹn payload cần tồn tại vượt ra ngoài tầng vận chuyển, hoặc khi một agent nhận cần chứng minh bằng mật mã về việc agent cụ thể nào đã gửi một chỉ thị.

Các khóa bất đối xứng AWS KMS là cơ chế. Agent gửi ký payload thông điệp qua API KMS Sign, và agent nhận kiểm chứng chữ ký qua API KMS Verify trước khi hành động theo thông điệp. Điều này cho kiểm chứng tính toàn vẹn đầu-cuối độc lập với lớp vận chuyển: ngay cả khi một thông điệp đi qua nhiều dịch vụ trung gian (load balancer, hàng đợi, bus sự kiện), chữ ký chứng minh nó được tạo bởi người gửi được tuyên bố và chưa bị chỉnh sửa. Các khóa riêng cho từng vùng tin cậy giới hạn phạm vi bị ảnh hưởng bởi một sự phơi bày khóa duy nhất.

Với việc nhắn tin bất đồng bộ giữa các agent qua Amazon SQS, hãy bật mã hóa phía máy chủ dùng các khóa AWS KMS do khách hàng quản lý. Cấu hình các khóa riêng cho các vùng tin cậy agent khác nhau để một sự phơi bày khóa ở một vùng không ảnh hưởng đến các thông điệp trong các vùng khác, và dùng các thuộc tính thông điệp SQS để mang chữ ký thông điệp cùng với payload đã mã hóa để các agent nhận kiểm chứng cả tính xác thực lẫn tính toàn vẹn tại thời điểm tiêu thụ.

AgentCore Runtime cung cấp cô lập phiên và xác thực dựng sẵn cho các agent dùng giao thức Agent-to-Agent (A2A). A2A xử lý xác thực cho các tương tác giữa các agent, nhưng với các thông điệp vượt qua các ranh giới tin cậy, mang dữ liệu nhạy cảm, hoặc đi qua các dịch vụ trung gian, ký ở cấp thông điệp xếp thêm lên trên các bảo vệ dựng sẵn của giao thức.

AWS PrivateLink định tuyến các giao tiếp giữa các agent qua các điểm cuối mạng riêng tư, giữ lưu lượng khỏi Internet công cộng. Điều đó bổ trợ cho mã hóa ở cấp thông điệp bằng cách giảm mức phơi bày mạng của lưu lượng giữa các agent. Hãy lưu các ARN khóa ký trong Parameter Store, một năng lực của AWS Systems Manager, cấu hình xoay vòng khóa tự động trong AWS KMS với một kỳ xoay vòng khớp với các yêu cầu bảo mật của bạn, và cấu hình các cảnh báo Amazon CloudWatch cho các bất thường sử dụng khóa (các thao tác ký bất ngờ từ các agent chỉ nên kiểm chứng, các đợt tăng đột biến khối lượng ký gợi ý một vòng lặp mất kiểm soát).

### Các bước triển khai

- **Tạo các cặp khóa KMS giới hạn theo vùng tin cậy:** Cấp phát các cặp khóa bất đối xứng AWS KMS để ký thông điệp, với các khóa riêng cho từng vùng tin cậy agent.
- **Ký thông điệp khi gửi:** Hiện thực việc ký thông điệp trong các agent gửi qua API AWS KMS Sign, đính kèm chữ ký như một thuộc tính metadata thông điệp.
- **Kiểm chứng chữ ký khi nhận:** Hiện thực việc kiểm chứng chữ ký trong các agent nhận qua API AWS KMS Verify, từ chối bất kỳ thông điệp nào thất bại kiểm chứng trước khi xử lý.
- **Mã hóa các hàng đợi SQS bằng các khóa do khách hàng quản lý:** Bật mã hóa phía máy chủ trên các hàng đợi Amazon SQS dùng cho việc nhắn tin bất đồng bộ giữa các agent, dùng các khóa AWS KMS do khách hàng quản lý được giới hạn phạm vi theo từng vùng tin cậy.
- **Xếp ký lên trên A2A cho lưu lượng xuyên ranh giới:** Với các agent trên AgentCore Runtime dùng A2A, thêm ký ở cấp thông điệp cho các giao tiếp vượt qua các ranh giới tin cậy lên trên xác thực dựng sẵn của giao thức.
- **Định tuyến qua PrivateLink:** Cấu hình AWS PrivateLink cho các giao tiếp dịch vụ giữa các agent để giữ lưu lượng trên các điểm cuối mạng riêng tư.
- **Quản lý khóa và cảnh báo về các bất thường:** Lưu các ARN khóa ký trong Parameter Store, một năng lực của AWS Systems Manager, cấu hình xoay vòng khóa tự động trong AWS KMS, và đặt các cảnh báo Amazon CloudWatch cho các bất thường sử dụng khóa.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP01 Triển khai xác thực mạnh cho các danh tính agent](../3-agentsec03/agentsec03-bp01.md)
- [AGENTSEC06-BP02 Triển khai các kiểm soát bảo mật điều phối luồng công việc](agentsec06-bp02.md)
- [AGENTSEC06-BP03 Thiết lập các ranh giới tin cậy giữa các agent](agentsec06-bp03.md)

**Tài liệu liên quan:**

- [Introducing agent-to-agent protocol support in Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [Digital signing with the new asymmetric keys feature of AWS KMS](https://aws.amazon.com/blogs/security/digital-signing-asymmetric-keys-aws-kms/)
- [Code signing using ACM Private CA and AWS KMS asymmetric keys](https://aws.amazon.com/blogs/security/code-signing-aws-certificate-manager-private-ca-aws-key-management-service-asymmetric-keys/)
- [Tài liệu AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [Amazon SQS security best practices](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-security-best-practices.html)

**Dịch vụ liên quan:**

- [AWS Key Management Service](https://aws.amazon.com/kms/)
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [AWS Systems Manager](https://aws.amazon.com/systems-manager/)
- [AWS PrivateLink](https://aws.amazon.com/privatelink/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
