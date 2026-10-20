# AGENTSEC03-BP01 Triển khai xác thực mạnh cho các danh tính agent

API key dùng chung và TLS một chiều cho agent đủ khả năng vươn tới mạng để hữu ích và đủ mơ hồ để bị mạo danh. Danh tính bằng mật mã cho cả hai phía của mọi lời gọi, với vòng đời tự động và thu hồi tức thì, là kiểm soát khiến mọi giao tiếp của agent có thể kiểm toán và đảo ngược.

**Kết quả mong muốn:**

- Bạn xác thực mọi giao tiếp agent-tới-agent và agent-tới-dịch vụ bằng các cơ chế mật mã mạnh, với xác thực lẫn nhau (mutual authentication) giúp ngăn mạo danh và chặn bắt.
- Bạn tự động hóa việc quản lý vòng đời chứng chỉ để các chứng chỉ hết hạn không gây thất bại xác thực hay lỗ hổng bảo mật.
- Bạn có thể thu hồi các danh tính agent bị ảnh hưởng ngay lập tức, cắt đứt truy cập trái phép trong vòng vài phút.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng API key dùng chung hoặc token tĩnh để xác thực agent thay vì các cơ chế dựa trên chứng chỉ hoặc OAuth, tạo ra các thông tin xác thực khó xoay vòng và dễ bị trích xuất.
- Hiện thực TLS một chiều (chỉ xác thực máy chủ) mà không có xác thực lẫn nhau, khiến bất kỳ client nào trên một đường mạng được phép có thể chạm tới điểm cuối mà không cần chứng minh danh tính agent của nó.
- Quản lý vòng đời chứng chỉ thủ công, dẫn đến các chứng chỉ hết hạn hoặc gây gián đoạn hoặc được gia hạn mà không có rà soát bảo mật đúng cách.

**Lợi ích khi áp dụng thực hành tốt này:**

- Xác thực dựa trên chứng chỉ hoặc OAuth cung cấp chứng minh danh tính bằng mật mã cho cả hai bên trong mọi giao tiếp của agent.
- Quản lý vòng đời chứng chỉ tự động giảm rủi ro chứng chỉ hết hạn gây gián đoạn hoặc lỗ hổng bảo mật.
- Thu hồi CRL và OCSP cung cấp khả năng cắt đứt truy cập trái phép trong vòng vài phút khi một danh tính agent bị ảnh hưởng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Xác thực cho agent có hai nhiệm vụ riêng biệt: chứng minh agent là chính chủ như nó tuyên bố, và chứng minh điều đó với bên nhận bằng mật mã thay vì qua các phỏng đoán theo đường mạng. Thông tin xác thực tĩnh thất bại ở cả hai bài kiểm tra. Chúng dễ dàng bị sao chép, khó xoay vòng, và người giữ chúng không thể phân biệt với người phát hành. Mẫu thiết kế là danh tính bằng mật mã được quản lý tập trung, với tự động hóa vòng đời và thu hồi như các thao tác hạng nhất chứ không phải là những suy nghĩ chợt đến sau.

[Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html) xử lý phần OAuth của mẫu đó. Nó cung cấp các luồng OAuth 2.0 được quản lý và liên kết danh tính (identity federation) cho các khối công việc tác tử, phát hành, kiểm chứng và xoay vòng token mà không có gánh nặng vận hành của việc tự chạy hạ tầng đó. Mỗi agent đăng ký trong thư mục danh tính agent tập trung và nhận một danh tính duy nhất. API GetWorkloadAccessTokenForJWT phát hành các token truy cập theo từng agent ràng buộc với danh tính của agent yêu cầu. Token vault bảo vệ các token OAuth bằng mã hóa AWS KMS (hỗ trợ khóa do khách hàng quản lý) và thực thi các kiểm soát truy cập theo từng agent để một agent không thể lấy token của agent khác.

Với các dịch vụ đòi hỏi xác thực dựa trên chứng chỉ thay vì OAuth, AWS Private Certificate Authority (AWS Private CA) là con đường được quản lý để phát hành các chứng chỉ client và máy chủ mTLS nội bộ. AWS Private CA xử lý việc phát hành và hỗ trợ các vòng đời gia hạn tự động, và việc thu hồi chứng chỉ qua CRL hoặc OCSP cung cấp điểm cắt khi một danh tính bị ảnh hưởng. Mutual TLS (mTLS) trên các AWS Application Load Balancer hoặc các cấu hình Amazon API Gateway cho lưu lượng agent-tới-agent một chứng minh đối xứng: cả hai bên xuất trình chứng chỉ, cả hai bên xác minh. Khóa riêng cư trú trong AWS Secrets Manager hoặc Parameter Store, một năng lực của AWS Systems Manager, với mã hóa tại chỗ bằng AWS KMS và các chính sách xoay vòng tự động, nên bản thân khóa không bao giờ trở thành một thông tin xác thực tĩnh dài hạn.

Phát hiện hoàn thiện mẫu này. Amazon GuardDuty gắn cờ các mẫu xác thực bất thường — agent xác thực từ các địa chỉ IP bất ngờ hoặc vào các thời điểm bất thường — và các phát hiện được định tuyến vào AWS Security Hub CSPM để quản lý sự kiện tập trung. Điều đó cho đội bảo mật một nơi duy nhất để thấy khi một danh tính đang được dùng theo những cách không khớp với hồ sơ bình thường của nó, dù bản thân thông tin xác thực đã bị thu hồi hay chưa.

### Các bước triển khai

- **Triển khai AgentCore Identity:** Triển khai [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html) cho việc xác thực agent, cấu hình liên kết danh tính cho truy cập xuyên dịch vụ, và đăng ký mỗi agent trong thư mục danh tính tập trung để có các danh tính duy nhất, có thể theo dõi.
- **Bảo vệ token trong vault:** Cấu hình token vault của AgentCore Identity cho việc lưu trữ token OAuth dùng các khóa AWS KMS do khách hàng quản lý để mã hóa, và thực thi các kiểm soát truy cập nghiêm ngặt theo từng agent cho việc lấy thông tin xác thực.
- **Phát hành chứng chỉ agent từ AWS Private CA:** Thiết lập AWS Private Certificate Authority cho các chứng chỉ danh tính agent, với các vòng đời gia hạn tự động được cấu hình.
- **Thực thi mutual TLS đầu-cuối:** Cấu hình mTLS trên mọi điểm cuối giao tiếp agent-tới-agent qua Application Load Balancer hoặc Amazon API Gateway với xác thực mTLS.
- **Lưu khóa trong Secrets Manager kèm xoay vòng:** Lưu mọi khóa riêng và thông tin xác thực của agent trong AWS Secrets Manager với mã hóa tại chỗ và các chính sách xoay vòng tự động được bật.
- **Bật kiểm tra thu hồi:** Hiện thực thu hồi chứng chỉ qua CRL hoặc OCSP để các chứng chỉ agent bị ảnh hưởng có thể bị vô hiệu hóa ngay lập tức.
- **Cảnh báo về các bất thường xác thực:** Cấu hình Amazon GuardDuty để phát hiện các mẫu xác thực bất thường và định tuyến các phát hiện tới AWS Security Hub CSPM để quản lý sự kiện bảo mật tập trung.
- **Rà soát kho chứng chỉ hàng quý:** Nhận diện và khắc phục các chứng chỉ đang tiến gần đến hạn hoặc dùng các thuật toán đã lỗi thời theo nhịp hàng quý.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người](agentsec03-bp02.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](agentsec03-bp03.md)
- [AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent](../6-agentsec06/agentsec06-bp01.md)

**Tài liệu liên quan:**

- [Securing AI agents with Amazon Bedrock AgentCore Identity](https://aws.amazon.com/blogs/security/securing-ai-agents-with-amazon-bedrock-agentcore-identity/)
- [Tài liệu Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html)
- [AgentCore Identity supported authentication patterns](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/common-use-cases.html)
- [Tài liệu AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Private CA](https://aws.amazon.com/private-ca/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)
- [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/)
