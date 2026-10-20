# AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người

Chỉ riêng lan truyền danh tính là không đủ khi agent hành động nhân danh người dùng. Các danh tính dịch vụ agent riêng biệt, với các ranh giới tin cậy cứng giúp ngăn việc đảm nhận các vai trò được chỉ định cho con người, giữ cho việc quy kết kiểm toán rõ ràng và chặn một agent bị sai cấu hình leo thang vào không gian danh tính của con người.

**Kết quả mong muốn:**

- Các hành động của agent và của con người có thể phân biệt được trong log kiểm toán, với các danh tính riêng biệt giúp ngăn agent thừa hưởng hoặc đảm nhận quyền hạn của người dùng con người.
- Các danh tính dịch vụ agent riêng được giới hạn phạm vi chỉ ở các quyền hạn cần thiết cho các thao tác tự động, và log kiểm toán quy mọi hành động một cách rõ ràng cho hoặc một agent hoặc một tác nhân con người.
- Các trust policy giúp ngăn agent đảm nhận các danh tính được chỉ định cho con người, với các rào chắn ở cấp tổ chức cung cấp một ranh giới thứ cấp trong các môi trường đa tài khoản.

**Các phản mẫu thường gặp (anti-patterns):**

- Tái sử dụng thông tin xác thực hoặc vai trò IAM của người dùng con người cho việc xác thực agent, khiến không thể phân biệt hành động agent với hành động con người trong log kiểm toán.
- Cho phép agent đảm nhận các vai trò IAM của con người qua chuỗi vai trò (role chaining), mở đường truy cập tới các tài nguyên lẽ ra phải hạn chế với người dùng con người và tạo ra một đường leo thang đặc quyền.
- Dùng một tài khoản dịch vụ dùng chung duy nhất cho nhiều agent, làm giảm khả năng quy kết các hành động cụ thể cho từng agent và làm phức tạp việc ứng phó sự cố.
- Chỉ dựa vào các chính sách IAM ở cấp agent mà không có hạn chế trust policy của vai trò hay các rào chắn đa tài khoản, để ngỏ đường đảm nhận nơi một vai trò agent bị ảnh hưởng vẫn có thể đảm nhận một vai trò con người.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các danh tính riêng biệt tạo ra việc quy kết kiểm toán rõ ràng, phân biệt rành mạch hành động agent với hành động con người.
- Các trust policy từ chối việc đảm nhận bởi các principal agent, với các rào chắn tùy chọn ở cấp tổ chức bổ sung một trần đa tài khoản.
- Quy ước gắn thẻ và đặt tên danh tính agent nhất quán cho phép lọc và phân tích các mẫu hoạt động của agent khi điều tra sự cố.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Có hai kiểu tách biệt quan trọng ở đây và chúng thường bị gộp lại trong thực tế. Tách biệt danh tính (identity separation) nghĩa là agent hoạt động dưới một danh tính dịch vụ tách biệt với bất kỳ danh tính con người nào, dù con người đó là một người vận hành quản lý tài nguyên AWS hay một người dùng ứng dụng tương tác với dịch vụ của agent. Tách biệt quyền hạn (permission separation) nghĩa là danh tính của agent chỉ mang những quyền hạn nó cần cho các tác vụ của mình và không bao giờ thừa hưởng quyền hạn của các danh tính con người. Những điều này áp dụng cho cả hai mô hình (agent hành động tự chủ và agent hành động nhân danh người dùng), nhưng cách ngữ cảnh người dùng chảy qua một lời gọi khác nhau: các agent tự chủ hoạt động chỉ dưới danh tính dịch vụ của chúng, trong khi các agent hành động nhân danh người dùng mang ngữ cảnh của người dùng đó về phía trước dưới dạng các claim token mà agent không bao giờ đảm nhận thông tin xác thực của người dùng. Các danh tính người vận hành con người (xác thực qua IAM Identity Center để truy cập AWS) và các danh tính người dùng ứng dụng (xác thực qua một nhà cung cấp danh tính hướng khách hàng riêng và hoàn toàn không có danh tính AWS) tự chúng là các lớp riêng biệt.

Với các agent hoạt động trên AWS, hãy tạo các vai trò IAM riêng cho từng loại agent làm danh tính dịch vụ của agent, với một quy ước đặt tên (ví dụ, `agent-role-<agent-name>`) phân biệt chúng với các vai trò người vận hành con người, và áp dụng PrincipalType: Agent như một thẻ nhất quán. Các thẻ principal xuất hiện trong các sự kiện AWS CloudTrail chủ yếu cho các lời gọi API mặt phẳng quản lý (management-plane) được thực hiện với các session tag. Với các sự kiện dịch vụ cụ thể không xuất hiện thẻ principal, hãy lọc theo quy ước đặt tên ARN của vai trò agent như tín hiệu chính và coi thẻ như một bộ lọc thứ cấp. Dùng AWS IAM Identity Center cho mọi truy cập của người vận hành con người và di chuyển bất kỳ người vận hành nào vẫn dùng IAM user theo từng tài khoản ra khỏi các danh tính đó. Người dùng ứng dụng thường nằm ngoài cuộc di chuyển này, họ xác thực qua nhà cung cấp danh tính riêng của ứng dụng, và danh tính của họ chảy vào các lời gọi agent dưới dạng các claim token. Cấu hình các Service Control Policy (SCP) trong AWS Organizations từ chối tường minh việc các agent (được nhận diện bằng thẻ) đảm nhận các vai trò trong ranh giới danh tính người vận hành con người, ví dụ từ chối sts:AssumeRole cho bất kỳ principal nào được gắn thẻ là agent đang cố đảm nhận các vai trò được gắn thẻ human-operator.

Amazon Bedrock AgentCore giới thiệu hai cấu trúc danh tính hỗ trợ sự tách biệt này. **Vai trò thực thi (execution role)** của AgentCore Runtime là một vai trò IAM thông thường được tiến trình Runtime đảm nhận để chạm tới các dịch vụ AWS mà agent phụ thuộc (các lần gọi mô hình, các lời gọi công cụ tới các API AWS, đọc và ghi bộ nhớ). **Workload Identity** của AgentCore là một danh tính riêng của agent được đăng ký trong thư mục AgentCore Identity, tách biệt với bất kỳ vai trò IAM nào, và được dùng để phát hành và kiểm chứng các token giới hạn phạm vi theo agent và để lưu vault các token bên thứ ba thu được nhân danh người dùng. Khi một agent hành động nhân danh một người dùng ứng dụng, nó gọi GetWorkloadAccessTokenForJWT với token truy cập của người dùng từ nhà cung cấp danh tính của ứng dụng. [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html) kiểm chứng token người dùng và trả về một token truy cập khối công việc riêng của agent nhúng ngữ cảnh người dùng dưới dạng các claim, nên chuỗi lời gọi mang cả "agent là ai" lẫn "người dùng là ai" mà agent không bao giờ đảm nhận thông tin xác thực của người dùng hay một vai trò IAM nhân danh người dùng.

Với các agent cần chạm tới các tài nguyên OAuth bên thứ ba nhân danh người dùng, AgentCore Identity điều phối luồng cấp phép authorization code và bảo vệ các token truy cập kết quả trong một token vault được giới hạn phạm vi theo từng danh tính agent và từng người dùng. Một agent không thể lấy các token thu được cho một người dùng khác, và chừng nào token truy cập bên thứ ba còn hợp lệ, agent có thể lấy nó từ vault mà không cần người dùng xác thực lại.

Amazon Cognito cung cấp một lựa chọn thay thế cho các tổ chức đã chuẩn hóa trên các Cognito user pool. Cùng nguyên tắc (agent mang cả danh tính của chính nó lẫn ngữ cảnh của người dùng dưới dạng các claim token) có thể được hiện thực ngoài AgentCore Identity. Mẫu được mô tả trong [Empower AI agents with user context using Amazon Cognito](https://aws.amazon.com/blogs/security/empower-ai-agents-with-user-context-using-amazon-cognito/) dùng các user pool của [Amazon Cognito](https://aws.amazon.com/cognito/): agent xác thực qua luồng client credentials trong khi truyền token của người dùng như ngữ cảnh bổ sung qua tham số yêu cầu aws_client_metadata, và một [Lambda trigger tiền-sinh-token (pre-token-generation)](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html) kiểm chứng token người dùng và tiêm một claim onBehalfOf vào token truy cập của agent trước khi phát hành. JWT kết quả nhận diện agent trong claim sub của nó và người dùng trong claim onBehalfOf của nó, tạo ra một token duy nhất mà các lớp ủy quyền phía sau có thể đánh giá. Đây là một phần mở rộng tùy chỉnh xây dựng trên các trigger hook của Cognito, không phải một tính năng gốc của Cognito, và nó bổ trợ cho mẫu AgentCore chứ không thay thế nó. Để ủy quyền trên token kết quả, các máy chủ tài nguyên có thể đánh giá các claim trực tiếp, hoặc đưa chính sách ra ngoài tới một dịch vụ như [Amazon Verified Permissions](https://aws.amazon.com/verified-permissions/) dùng Cedar (một lựa chọn trực giao với việc bạn dùng AgentCore Identity hay mẫu Cognito).

Khi một agent gọi một công cụ qua AgentCore Gateway, gateway hoạt động dưới vai trò thực thi của riêng nó (một vai trò cho mỗi gateway) và xác thực ra áp dụng cho target phụ thuộc vào loại target (xem [tham chiếu xác thực ra của AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-outbound-auth.html) để biết chi tiết). Ngữ cảnh người dùng lan truyền qua gateway để các dịch vụ phía sau có thể thực thi ủy quyền ở cấp người dùng, và gateway không bao giờ thay thế một danh tính IAM cho người dùng hay xác thực lại như người dùng đối với các dịch vụ phía sau.

Cấu hình [CloudTrail với advanced event selector](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) để thu các lời gọi API của agent, bao gồm các data event cho các dịch vụ do agent gọi nơi khả năng nhìn thấy vượt ra ngoài các sự kiện mặt phẳng quản lý là quan trọng. Bật các data event của AgentCore để các thao tác đối với AgentCore Memory, Gateway và Runtime được ghi log cùng với các sự kiện mặt phẳng quản lý. Các truy vấn Amazon CloudWatch Logs Insights được lọc theo các mẫu ARN vai trò agent cho các dashboard hoạt động agent riêng. Để phân tích dựa trên SQL theo thời gian, hãy đưa các log CloudTrail tới Amazon S3 và truy vấn chúng bằng Amazon Athena (xem AGENTSEC05-BP01).

Với các hệ thống đa agent nơi một agent cha trực tiếp đảm nhận vai trò IAM của một agent con (ví dụ, gọi sts:AssumeRole trước khi gọi agent con trong cùng tài khoản), hãy dùng các tên phiên vai trò (role session name) bao gồm định danh của agent cha để chuỗi hiển thị trong CloudTrail. Với giao tiếp A2A định tuyến qua AgentCore Runtime, mỗi agent chạy dưới phiên vai trò thực thi độc lập của riêng nó và không có chuỗi vai trò IAM nào. Hãy dùng các định danh tương quan (correlation identifier) được lan truyền qua thông điệp A2A (xem AGENTSEC05-BP02) để tái dựng đồ thị lời gọi agent-tới-agent.

### Các bước triển khai

- **Kiểm toán và đổi tên các vai trò agent:** Nhận diện bất kỳ vai trò IAM nào được dùng chung giữa agent và người dùng con người, và tạo các vai trò riêng cho agent với một quy ước đặt tên nhất quán (ví dụ, `agent-role-<agent-name>`).
- **Gắn thẻ các vai trò agent nhất quán:** Áp dụng các thẻ PrincipalType: Agent và AgentName: `<name>` cho mọi vai trò IAM của agent để lọc và giám sát.
- **Chuyển người vận hành con người sang IAM Identity Center:** Cấu hình AWS IAM Identity Center cho mọi truy cập của người vận hành con người và di chuyển bất kỳ người vận hành nào vẫn dùng IAM user theo từng tài khoản.
- **Thực thi ranh giới agent-tới-con-người qua các SCP:** Triển khai các Service Control Policy trong AWS Organizations từ chối việc các agent (được nhận diện bằng thẻ) đảm nhận các vai trò người vận hành con người, tạo ra một ranh giới cứng giữa các không gian danh tính.
- **Đăng ký Workload Identity cho các luồng on-behalf-of:** Đăng ký các Workload Identity của agent trong [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html) cho các agent hành động nhân danh người dùng, và dùng GetWorkloadAccessTokenForJWT để tạo các token giới hạn phạm vi theo agent nhúng ngữ cảnh người dùng dưới dạng các claim cho việc ủy quyền phía sau.
- **Bật CloudTrail với các data event của AgentCore:** Bật các advanced event selector bao gồm các data event của AgentCore, và xây dựng các truy vấn Amazon CloudWatch Logs Insights được lọc theo các mẫu ARN vai trò agent cho các dashboard hoạt động agent riêng.
- **Phân tích bằng Athena theo thời gian:** Đưa các log AWS CloudTrail tới Amazon S3 và dùng Amazon Athena để phân tích dựa trên SQL các mẫu hoạt động agent so với con người theo thời gian phục vụ báo cáo tuân thủ và phân tích xu hướng dài hạn.
- **Đặt tên phiên để quy kết:** Hiện thực các quy ước đặt tên phiên vai trò bao gồm các định danh agent (và các định danh agent cha cho các chuỗi ủy quyền) để quy kết rõ ràng trong các hệ thống đa agent.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP01 Triển khai xác thực mạnh cho các danh tính agent](agentsec03-bp01.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](agentsec03-bp03.md)
- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)

**Tài liệu liên quan:**

- [AWS CloudTrail best practices](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/best-practices-security.html)
- [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [Securing AI agents with Amazon Bedrock AgentCore Identity](https://aws.amazon.com/blogs/security/securing-ai-agents-with-amazon-bedrock-agentcore-identity/)
- [Empower AI agents with user context using Amazon Cognito](https://aws.amazon.com/blogs/security/empower-ai-agents-with-user-context-using-amazon-cognito/)
- [Tài liệu Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html)
- [AgentCore Identity supported authentication patterns](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/common-use-cases.html)

**Dịch vụ liên quan:**

- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
- [AWS Organizations](https://aws.amazon.com/organizations/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Cognito](https://aws.amazon.com/cognito/)
- [Amazon Verified Permissions](https://aws.amazon.com/verified-permissions/)
