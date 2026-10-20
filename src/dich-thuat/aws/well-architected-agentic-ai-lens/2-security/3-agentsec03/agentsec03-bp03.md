# AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động

Quyền hạn rộng cấp cho một agent bị ảnh hưởng quyền truy cập vượt xa tác vụ mà nó được yêu cầu làm. Giới hạn phạm vi đặc quyền tại mỗi lớp danh tính, hậu thuẫn nó bằng các thông tin xác thực tạm thời, và xếp thêm các điều kiện IAM theo ngữ cảnh sẽ giới hạn phạm vi của bất kỳ lời gọi đơn lẻ nào bị xâm phạm hoặc bị prompt sai.

**Kết quả mong muốn:**

- Agent hoạt động với quyền hạn tối thiểu cần thiết để hoàn thành các tác vụ đã định của nó, với các thông tin xác thực tạm thời tự động hết hạn và các ranh giới quyền hạn động siết chặt khi xử lý dữ liệu nhạy cảm hoặc các thao tác rủi ro cao.
- Các mô hình truy cập vừa-đúng-lúc (just-in-time) giúp giới hạn các quyền hạn được nâng cấp trong thời gian của thao tác đòi hỏi chúng.
- Bạn liên tục kiểm chứng việc giới hạn phạm vi chính sách khi khối công việc tiến hóa, loại bỏ trôi dạt trước khi nó tích lũy.

**Các phản mẫu thường gặp (anti-patterns):**

- Gán các chính sách IAM rộng (ví dụ, s3:* hoặc *) cho các vai trò agent cho tiện, cấp nhiều quyền truy cập hơn hẳn so với mức bất kỳ tác vụ riêng lẻ nào cần.
- Dùng các thông tin xác thực tĩnh dài hạn thay vì các thông tin xác thực tạm thời từ AWS STS, kéo dài cửa sổ phơi bày nếu thông tin xác thực vô tình bị tiết lộ.
- Không hiện thực các ranh giới quyền hạn IAM, cho phép agent tạo hoặc chỉnh sửa các chính sách IAM và leo thang đặc quyền của chính mình.
- Mở rộng quyền hạn agent để đáp lại các lỗi truy cập mà không điều tra xem mẫu truy cập có hợp lệ hay không, tích lũy quyền hạn quá mức qua các cấp phát theo phản ứng mà không bao giờ bị thu hồi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các vai trò IAM đặc quyền tối thiểu giới hạn một agent bị ảnh hưởng chỉ ở các tài nguyên cần cho tác vụ hiện tại của nó.
- Các thông tin xác thực AWS STS tạm thời với thời lượng phiên ngắn giảm rủi ro phơi bày thông tin xác thực dài hạn.
- Các Điều kiện IAM về region, thẻ tài nguyên, cửa sổ thời gian và mạng nguồn bổ sung chiều sâu phòng thủ giới hạn tác động của việc phơi bày thông tin xác thực.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Một agent hoạt động dưới nhiều lớp danh tính, và mỗi lớp là một nơi riêng để áp dụng việc giới hạn phạm vi. **Danh tính agent (agent identity)** là những gì agent cụ thể này là với tư cách một thực thể trong thư mục của bạn (ví dụ, một AgentCore Workload Identity với một ARN duy nhất). **Danh tính dịch vụ (service identity)** là những gì agent chạy dưới đó khi nó gọi các dịch vụ AWS (với AgentCore Runtime, đây là vai trò thực thi IAM được tiến trình Runtime đảm nhận). **Danh tính giao dịch (transaction identity)** là ngữ cảnh theo từng lần gọi được mang cùng một lời gọi agent đơn lẻ, thường được biểu diễn qua các thông tin xác thực phiên AWS STS với các session tag và session policy. Khi một agent hành động nhân danh một người dùng, một **danh tính người dùng (user identity)** được mang thêm trong ngữ cảnh lời gọi dưới dạng các claim token được lan truyền qua chuỗi lời gọi của agent. Việc giới hạn phạm vi quyền hạn áp dụng khác nhau ở từng lớp:

- Các giới hạn năng lực rộng thuộc về danh tính dịch vụ (vai trò IAM, ranh giới quyền hạn)
- Các ràng buộc theo từng thao tác thuộc về giao dịch (session policy, session tag và các Điều kiện IAM)
- Các ràng buộc theo ngữ cảnh người dùng thuộc về danh tính người dùng (ủy quyền dựa trên token được đánh giá tại tài nguyên)

Ở lớp danh tính dịch vụ, hãy thiết kế các vai trò IAM của agent dùng nguyên tắc đặc quyền tối thiểu, bắt đầu với không có quyền hạn nào và chỉ thêm những gì cần cho mỗi tác vụ cụ thể. AWS IAM Access Analyzer sinh các chính sách đặc quyền tối thiểu dựa trên các mẫu truy cập thực tế quan sát được trong log AWS CloudTrail, cho bạn một đường cơ sở dựa trên dữ liệu để giới hạn phạm vi. Các ranh giới quyền hạn IAM trên mọi vai trò agent thiết lập một trần quyền hạn tối đa không thể vượt qua ngay cả khi các chính sách của agent bị chỉnh sửa, điều này quan trọng vì đó là kiểm soát giúp ngăn leo thang đặc quyền khi có gì đó về chính bản thân chính sách thay đổi.

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) hoạt động dưới một vai trò thực thi cho mỗi gateway, với xác thực ra phụ thuộc vào loại target (xem [tham chiếu xác thực ra của AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-outbound-auth.html)). Hãy giới hạn phạm vi vai trò thực thi của gateway chỉ ở các hành động và tài nguyên mà tập các target chung lại cần, và ràng buộc truy cập theo từng target qua cấu hình xác thực ra riêng của target. Ngữ cảnh người dùng được lan truyền qua gateway cho phép các dịch vụ phía sau thực thi kiểm soát truy cập ở cấp người dùng ngoài vai trò ở cấp gateway, nên các thao tác còn bị ràng buộc thêm bởi quyền hạn của người dùng khởi nguồn ngay cả khi vai trò gateway có quyền truy cập tới một target.

Các thông tin xác thực tạm thời là cách lớp giao dịch giữ được giới hạn phạm vi. AWS STS AssumeRole với các session policy sinh các thông tin xác thực được giới hạn phạm vi tới các quyền hạn cụ thể cần cho mỗi lần thực thi tác vụ, và các thời lượng phiên ngắn (15 đến 60 phút) làm việc hết hạn trở nên tự động. Với các agent đòi hỏi quyền hạn được nâng cấp cho các thao tác cụ thể, truy cập vừa-đúng-lúc qua AWS IAM Identity Center hoặc các luồng công việc yêu cầu truy cập tùy chỉnh dựa trên Lambda sẽ cấp và thu hồi quyền hạn theo chương trình.

Các Điều kiện IAM là lớp chiều sâu phòng thủ làm cho các thông tin xác thực bị phơi bày kém hữu dụng hơn. aws:RequestedRegion giới hạn các hành động của agent ở các region được phê duyệt. aws:ResourceTag hạn chế truy cập tới các tài nguyên được gắn thẻ để agent dùng. aws:CurrentTime thực thi các hạn chế cửa sổ thời gian. aws:SourceVpc yêu cầu các lời gọi API của agent phát sinh từ các VPC được phê duyệt. Các điều kiện này không giảm các quyền hạn đã nêu của chính sách, nhưng chúng giới hạn các ngữ cảnh mà các quyền hạn đó áp dụng. Ở cấp tổ chức, các Service Control Policy trong AWS Organizations thiết lập các rào chắn phạm vi toàn tổ chức áp dụng cho mọi tài khoản agent, giúp ngăn agent truy cập các dịch vụ hoặc thực hiện các hành động không bao giờ phù hợp bất kể quyền hạn ở cấp tác vụ.

### Các bước triển khai

- **Sinh các chính sách đặc quyền tối thiểu từ dữ liệu sử dụng:** Kiểm toán các vai trò IAM agent hiện có bằng AWS IAM Access Analyzer để nhận diện các chính sách quá phóng khoáng và sinh các khuyến nghị đặc quyền tối thiểu dựa trên các mẫu truy cập thực tế trong log AWS CloudTrail.
- **Áp dụng các ranh giới quyền hạn:** Đặt các ranh giới quyền hạn IAM trên mọi vai trò agent để thiết lập một trần quyền hạn tối đa không thể vượt qua ngay cả khi các chính sách ở cấp tác vụ của agent bị chỉnh sửa.
- **Giới hạn phạm vi vai trò thực thi của Gateway:** Hạn chế vai trò thực thi của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) chỉ ở các hành động và tài nguyên mà các target của nó cần, cấu hình xác thực ra riêng theo loại target, và dùng AgentCore Identity để lan truyền ngữ cảnh người dùng cho việc thực thi ở cấp người dùng phía sau.
- **Phát hành các thông tin xác thực tạm thời với session policy:** Dùng AWS STS AssumeRole với các session policy và các thời lượng phiên ngắn (15 đến 60 phút) cho mọi lần phát hành thông tin xác thực của agent.
- **Thêm các Điều kiện IAM theo ngữ cảnh:** Hạn chế truy cập theo region (aws:RequestedRegion), thẻ tài nguyên (aws:ResourceTag), cửa sổ thời gian (aws:CurrentTime) và mạng nguồn (aws:SourceVpc).
- **Triển khai các SCP phạm vi toàn tổ chức:** Thiết lập các rào chắn phạm vi toàn tổ chức qua các Service Control Policy trong AWS Organizations áp dụng cho mọi tài khoản agent.
- **Hiện thực truy cập vừa-đúng-lúc cho các quyền hạn được nâng cấp:** Dùng IAM Identity Center hoặc các luồng công việc yêu cầu truy cập tùy chỉnh dựa trên Lambda với thu hồi tự động khi thao tác hoàn tất hoặc phiên hết hạn.
- **Rà soát trôi dạt IAM hàng quý:** Lên lịch các cuộc rà soát IAM Access Analyzer mỗi quý để phát hiện trôi dạt quyền hạn, nhận diện truy cập không dùng đến, và loại bỏ các quyền hạn không còn cần thiết.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC02-BP01 Triển khai ủy quyền công cụ](../2-agentsec02/agentsec02-bp01.md)
- [AGENTSEC03-BP01 Triển khai xác thực mạnh cho các danh tính agent](agentsec03-bp01.md)
- [AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người](agentsec03-bp02.md)
- [AGENTSEC03-BP04 Rà soát quyền hạn và truy cập định kỳ](agentsec03-bp04.md)
- [AGENTREL02-BP02 Giới hạn quyền hạn agent tới mức truy cập tối thiểu cần thiết](../../3-reliability/2-agentrel02/agentrel02-bp02.md)

**Tài liệu liên quan:**

- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [Tài liệu Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html)
- [Tài liệu Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html)
- [Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)

**Dịch vụ liên quan:**

- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [AWS IAM Access Analyzer](https://aws.amazon.com/iam/features/analyze-access/)
- [AWS Organizations](https://aws.amazon.com/organizations/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
