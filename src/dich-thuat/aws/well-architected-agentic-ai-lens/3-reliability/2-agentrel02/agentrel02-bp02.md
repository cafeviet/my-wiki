# AGENTREL02-BP02 Giới hạn quyền hạn của tác nhân ở mức truy cập tối thiểu cần thiết

Quyền hạn rộng biến một chỉ dẫn bị hiểu sai thành một sự cố lan truyền. Truy cập theo đặc quyền tối thiểu giữ cho phạm vi ảnh hưởng của hành vi LLM khó lường luôn hẹp và làm cho hoạt động bất thường dễ nhìn thấy hơn trên nền một đường cơ sở được định nghĩa tốt.

**Kết quả mong muốn:**

- Bạn có mỗi tác nhân chỉ được cấp các quyền cần thiết cho chức năng cụ thể của nó.
- Bạn áp dụng các ranh giới truy cập lúc chạy tại gateway, nhờ đó suy luận của LLM không thể mở rộng tầm với của tác nhân.
- Bạn kiểm toán chính sách tác nhân liên tục và loại bỏ các quyền mà thực tế sử dụng không biện minh được.

**Các phản mẫu thường gặp (anti-patterns):**

- Cấp quyền rộng vượt quá chức năng của tác nhân, cho phép hành vi khó lường vươn tới các hệ thống trái phép.
- Viết các chính sách thô trải rộng nhiều hệ thống, nên một sai lầm đơn lẻ gây tác động vượt tầm.
- Bỏ qua kiểm toán và giám sát các mẫu truy cập của tác nhân, bỏ lỡ các tín hiệu chỉ ra việc lạm dụng quyền.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phạm vi ảnh hưởng vẫn được kiềm chế khi một tác nhân đưa ra quyết định bất ngờ.
- Ranh giới vận hành rõ ràng làm cho hành vi của tác nhân dễ dự đoán hơn.
- Các mẫu truy cập cơ sở làm cho các bất thường dễ nhìn thấy thay vì lẫn trong nhiễu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phòng thủ theo chiều sâu (defense-in-depth) là khung cho việc ủy quyền tác nhân. Không có kiểm soát đơn lẻ nào đủ. AgentCore Identity, AgentCore Policy và IAM đều có vai trò, và sự kết hợp giúp ngăn một lỗ hổng ở lớp này trở thành một đặc quyền không được kiểm soát ở lớp khác. Dùng [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) để quản lý xác thực cho truy cập của tác nhân tới các dịch vụ bên thứ ba thông qua thông tin đăng nhập OAuth và **API** key. Dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để thực thi các ranh giới truy cập lúc chạy thông qua các chính sách Cedar tại ranh giới AgentCore Gateway, độc lập với cách LLM của tác nhân suy luận.

Đối với các tác nhân tương tác với mô hình Amazon Bedrock và Knowledge Bases, dùng các chính sách dựa trên danh tính của IAM với các khóa điều kiện để giới hạn mô hình nào mỗi tác nhân được gọi. Thu hẹp truy cập Memory tới các namespace được chỉ định bằng các điều kiện chính sách IAM. Gắn các chính sách dựa trên danh tính với các khối Condition ràng buộc truy cập theo định danh namespace và bối cảnh phiên (ví dụ bedrock:AgentId, bedrock:SessionId). Với các điều kiện này, các tác nhân vận hành trong ranh giới bộ nhớ được chỉ định mà không rò rỉ chéo namespace. Khi mô hình ủy quyền của AgentCore Memory tiến hóa, hãy áp dụng các chính sách dựa trên tài nguyên khi khả dụng để đơn giản hóa hơn nữa việc cấp quyền ở cấp namespace. Tránh dùng tài nguyên ký tự đại diện trong các chính sách IAM của tác nhân. Cám dỗ dùng * cho tiện lợi là lý do phổ biến nhất khiến đặc quyền tối thiểu âm thầm thoái hóa thành truy cập rộng theo thời gian.

[AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) sinh các khuyến nghị đặc quyền tối thiểu dựa trên các mẫu truy cập thực tế được ghi trong CloudTrail, nhờ đó các chính sách có thể được siết chặt dựa trên những gì tác nhân thực sự dùng thay vì những gì nó được cấp ban đầu. CloudTrail bắt vết kiểm toán, và [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) phát hiện các sai lệch so với hồ sơ vận hành kỳ vọng. Khi các mẫu truy cập đáng ngờ xuất hiện, các phản hồi tự động như thu hồi quyền hoặc cách ly tác nhân giúp ngăn sai lệch trở thành sự cố.

### Các bước triển khai

- **Cấu hình AgentCore Identity và AgentCore Policy:** Dùng [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) cho xác thực và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với Cedar để thực thi các ranh giới truy cập lúc chạy.
- **Tạo các vai trò thực thi IAM dành riêng cho từng tác nhân:** Thu hẹp mỗi vai trò tới các ARN tài nguyên cụ thể và tránh ký tự đại diện.
- **Giới hạn truy cập mô hình Amazon Bedrock và Knowledge Base bằng các khóa điều kiện IAM:** Chỉ cho phép mỗi tác nhân các mô hình và knowledge base mà chức năng của nó cần.
- **Kiểm toán chính sách bằng IAM Access Analyzer:** Dùng [AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) để sinh khuyến nghị đặc quyền tối thiểu từ dữ liệu CloudTrail và khắc phục các chính sách quá dễ dãi.
- **Giám sát các mẫu truy cập và tự động hóa phản hồi:** Theo dõi các mẫu truy cập qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và cấu hình thu hồi quyền hoặc cách ly tự động khi có bất thường.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL02-BP01 Thiết kế các tác nhân cho các tác vụ cụ thể và nguyên tử](agentrel02-bp01.md)
- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](agentrel02-bp03.md)
- [AGENTSEC03-BP01 Implement strong authentication for agent identities](../../2-security/3-agentsec03/agentsec03-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
