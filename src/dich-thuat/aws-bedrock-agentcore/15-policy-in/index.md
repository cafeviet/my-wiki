---
title: "Policy trong AgentCore: Kiểm soát tương tác của Agent"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---
# Policy trong AgentCore: Kiểm soát tương tác của Agent

# Policy trong Amazon Bedrock AgentCore: Kiểm soát tương tác của Agent

Policy trong Amazon Bedrock AgentCore cho phép lập trình viên định nghĩa và thực thi các kiểm soát bảo mật cho tương tác của Agent (tác tử AI) với các tool (công cụ) bằng cách tạo một ranh giới bảo vệ quanh các thao tác của Agent. Các Agent có thể thích ứng động để giải quyết những vấn đề phức tạp - từ xử lý các yêu cầu của khách hàng đến tự động hóa quy trình trên nhiều tool và hệ thống. Tuy nhiên, sự linh hoạt này lại đặt ra những thách thức bảo mật mới, vì Agent có thể vô tình hiểu sai các quy tắc nghiệp vụ, hoặc hành động vượt ngoài thẩm quyền đã định.

Với Policy trong AgentCore, lập trình viên có thể tạo các policy engine, tạo và lưu trữ các policy tất định (deterministic) trong đó, và liên kết các policy engine với các gateway. Policy trong AgentCore chặn toàn bộ lưu lượng của Agent đi qua các Amazon Bedrock AgentCore Gateway và đánh giá từng yêu cầu theo các policy đã định nghĩa trong policy engine trước khi cho phép truy cập tool.

Các policy được xây dựng bằng [ngôn ngữ Cedar](https://www.cedarpolicy.com/en) , một ngôn ngữ mã nguồn mở để viết và thực thi các policy ủy quyền. Điều này cho phép lập trình viên chỉ định chính xác Agent có thể truy cập gì và thực hiện những hành động nào. Policy trong AgentCore cũng cung cấp năng lực soạn thảo policy bằng ngôn ngữ tự nhiên, cho phép lập trình viên mô tả quy tắc bằng tiếng Anh thông thường thay vì viết mã policy chính quy trong Cedar. Việc soạn thảo policy dựa trên ngôn ngữ tự nhiên diễn giải ý định của người dùng, sinh ra các policy ứng viên, kiểm chứng chúng với tool schema, và dùng automated reasoning để kiểm tra các điều kiện an toàn như phát hiện những policy quá dễ dãi (overly permissive), quá hạn chế (overly restrictive), hoặc chứa các điều kiện không bao giờ có thể thỏa mãn - đảm bảo khách hàng phát hiện những vấn đề này trước khi thực thi policy.

Policy trong AgentCore cũng hỗ trợ soạn thảo policy bằng [Dogwood](https://dogwood-policy.github.io/dogwood/index.html) trên website Dogwood Policy, một ngôn ngữ policy mã nguồn mở. Một policy Dogwood duy nhất có thể kết hợp nhiều loại điều kiện ủy quyền. Ở mức đơn giản nhất, bạn viết các quy tắc dựa trên input cho phép hoặc cấm một lời gọi tool dựa trên chính yêu cầu hiện tại — principal là ai, họ đang gọi tool nào, tài nguyên nào liên quan, và các tham số input của lời gọi đó. Sau đó bạn có thể thêm các điều kiện thời gian nhận biết session (session-aware temporal conditions) quyết định dựa trên những gì đã xảy ra trước đó trong cùng session — ví dụ, yêu cầu phải có phê duyệt trước một lần chuyển tiền, chặn một hành động sau khi nó đã chạy một số lần nhất định, hoặc giữ tổng cộng dồn dưới một ngân sách. Bạn cũng có thể tham vấn các information provider, chẳng hạn Guardrails, phát ra một tín hiệu tại thời điểm đánh giá — như điểm content-safety hoặc prompt-attack — và ra quyết định dựa trên điểm được phát ra. Vì các điều kiện dựa trên input, thời gian, và provider đều kết hợp trong một policy dưới cùng một mô hình permit và forbid, bạn có thể xếp lớp chúng để biểu đạt kiểm soát mà các Agent của bạn cần — từ một quy tắc truy cập đơn giản đến một biện pháp bảo vệ đa bước, nhận biết session.

Policy trong AgentCore hỗ trợ các quyền chi tiết dựa trên danh tính người dùng và các tham số input của tool, giúp có thể triển khai an toàn các Agent tự trị ở quy mô doanh nghiệp. Bằng cách đưa các kiểm soát bảo mật ra ngoài mã của Agent, lập trình viên có thể tập trung xây dựng các năng lực Agent sáng tạo trong khi vẫn duy trì các đảm bảo bảo mật mạnh mẽ - loại bỏ nhu cầu triển khai bảo mật tùy chỉnh và giảm rủi ro bị vượt qua policy thông qua thao túng Agent.

###### Chủ đề

- [Key benefits](#policy-benefits)

- [Key features](#policy-features)

- [Getting started with Policy in AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-getting-started.html)

- [Core concepts](/dich-thuat/aws-bedrock-agentcore/15-policy-in/policy-core-concepts)

- [AgentCore Gateway and Policy in AgentCore IAM Permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-permissions.html)

- [Create a policy engine](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-create-engine.html)

- [Create a policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-create-policies.html)

- [Writing policies in natural language](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-natural-language.html)

- [Validate and test policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-validate-policies.html)

- [Use policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-use-policies.html)

- [Example policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/example-policies.html)

- [Advanced features and topics for Policy in AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-advanced.html)

## Lợi ích chính

Policy trong AgentCore cung cấp ba lợi ích chính, cho phép triển khai an toàn và có khả năng mở rộng các Agent trong môi trường doanh nghiệp:

Định nghĩa những hành động mà một Agent được phép thực hiện - bao gồm những tool nào nó có thể gọi và các điều kiện chính xác mà những hành động đó được phép.

Mọi hành động của Agent qua Amazon Bedrock AgentCore Gateway đều bị chặn và đánh giá tại ranh giới bên ngoài mã của Agent - đảm bảo thực thi nhất quán, tất định, và duy trì đáng tin cậy bất kể Agent được hiện thực ra sao.

Viết các policy bằng các prompt ngôn ngữ tự nhiên hoặc trực tiếp trong Cedar (ngôn ngữ policy mã nguồn mở của AWS cho các quyền chi tiết), giúp những người xây dựng với mức độ chuyên môn khác nhau dễ dàng định nghĩa quy tắc cho các Agent của họ. Các nhóm có thể thiết lập ranh giới một lần và áp dụng nhất quán trên tất cả Agent và tool, với mọi quyết định thực thi được ghi log qua CloudWatch metric và log, để các nhóm bảo mật và tuân thủ có thể kiểm toán và kiểm chứng hành vi.

## Tính năng chính

Policy trong AgentCore cung cấp các năng lực toàn diện để quản trị dựa trên policy đối với tương tác của Agent, bao gồm các tính năng chính sau:

- **Policy Enforcement** - Chặn và đánh giá tất cả yêu cầu của Agent theo các policy đã định nghĩa trước khi cho phép truy cập tool

- **Access Controls** - Cho phép kiểm soát chi tiết dựa trên danh tính người dùng và các tham số input của tool

- **Policy Authoring** - Cung cấp hỗ trợ ngôn ngữ policy Cedar để viết các policy rõ ràng, đã được kiểm chứng. Các policy cũng có thể được soạn thảo bằng ngôn ngữ tự nhiên dùng các prompt tiếng Anh, được dịch sang các policy Cedar và kiểm chứng

- **Policy Monitoring** - Cung cấp tích hợp CloudWatch để giám sát các đánh giá và quyết định policy

- **Infrastructure Integration** - Tích hợp với các VPC security group và hạ tầng bảo mật AWS khác

- **Audit Logging** - Duy trì các log chi tiết về các quyết định policy phục vụ tuân thủ và xử lý sự cố

- **Temporal Policies** - Các quy tắc thuộc phạm vi session, suy luận trên lịch sử các hành động trong một cuộc trò chuyện. Để biết thêm thông tin, xem [Temporal policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-temporal.html).
