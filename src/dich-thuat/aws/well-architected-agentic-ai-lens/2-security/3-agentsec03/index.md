# Quản lý danh tính và quyền hạn của agent

Agent truy cập tài nguyên, gọi công cụ (Tools) và tương tác với các dịch vụ khác theo hai mô hình:

- Một cách tường minh nhân danh một người dùng, nơi một con người khởi tạo yêu cầu và các hành động của agent phải bị giới hạn bởi quyền hạn của người dùng đó
- Một cách tự chủ, nơi agent hành động mà không có con người trong vòng lặp (được kích hoạt bởi một lịch, một sự kiện, một cảnh báo hoặc một agent khác)

Việc quản lý danh tính và quyền hạn cần xử lý cả hai. Nếu không có nó, quyền hạn của agent có thể dẫn đến truy cập trái phép tới tài nguyên và dữ liệu. Để duy trì các ranh giới bảo mật, hãy áp dụng các nguyên tắc đặc quyền tối thiểu (least privilege), tách biệt quyền hạn của agent và của con người, và thiết lập xác thực mạnh cho các danh tính agent.

| AGENTSEC03: Bạn quản lý danh tính, quyền hạn của agent và ngăn chặn leo thang đặc quyền như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Mọi giao tiếp agent-tới-agent và agent-tới-dịch vụ đều xác thực qua các cơ chế có thể kiểm chứng, dù đó là mutual TLS dựa trên chứng chỉ, token OAuth đã ký, hay danh tính khối công việc (workload identity) do nền tảng quản lý.
- Agent hoạt động dưới các danh tính dịch vụ tách biệt với danh tính con người, và các dấu vết kiểm toán quy mọi hành động một cách rõ ràng cho hoặc một agent hoặc một tác nhân con người.
- Khi một agent hành động nhân danh một người dùng, ngữ cảnh người dùng được lan truyền dưới dạng các claim token đã ký qua chuỗi lời gọi mà agent không bao giờ đảm nhận thông tin xác thực của người dùng.
- Agent chạy với quyền hạn tối thiểu mà tác vụ của nó cần, thông qua các thông tin xác thực ngắn hạn (short-lived credentials), ranh giới quyền hạn (permission boundaries) và các Điều kiện IAM (IAM Conditions).
- Tư thế quyền hạn được kiểm chứng liên tục, với phát hiện trôi dạt tự động, các phát hiện truy cập không dùng đến (unused-access) và các cuộc rà soát định kỳ có tài liệu giữ cho đặc quyền căn chỉnh với việc sử dụng thực tế.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc quản lý danh tính và quyền hạn của agent như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Agent xác thực bằng API key dùng chung hoặc token tĩnh, và một số vai trò (role) được tái sử dụng qua các agent và người dùng con người. Quyền hạn rộng, thông tin xác thực dài hạn, và các dấu vết kiểm toán không phân biệt rõ hành động agent với hành động con người. Không có ranh giới quyền hạn, không có đường thu hồi (revocation), và không có nhịp rà soát. |
| 2 | Manh nha (Emerging) | Mỗi agent có một vai trò [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) riêng với quy ước đặt tên và gắn thẻ nhất quán. Chứng chỉ từ [AWS Private Certificate Authority](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html) được dùng nơi cần mutual TLS, thông tin xác thực xoay vòng qua [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html), và [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) ghi log hoạt động agent tách biệt với hoạt động con người. Các chính sách least-privilege ban đầu đã có, mặc dù trôi dạt là phổ biến. |
| 3 | Được định nghĩa (Defined) | [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) tập trung hóa các danh tính khối công việc của agent, việc phát hành token và token vault, với các khóa [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) do khách hàng quản lý bảo vệ các bí mật. Người vận hành con người truy cập AWS qua [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html), và các Service Control Policy (SCP) trong [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html) giúp ngăn agent đảm nhận các vai trò con người. [AWS STS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) phát hành thông tin xác thực ngắn hạn với các session policy, và [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) cung cấp các phát hiện đường cơ sở. |
| 4 | Chủ động (Proactive) | Khi một agent hành động nhân danh một người dùng, [GetWorkloadAccessTokenForJWT](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_GetWorkloadAccessTokenForJWT.html) nhúng ngữ cảnh người dùng dưới dạng các claim để các dịch vụ phía sau thực thi ủy quyền ở cấp người dùng mà agent không giữ thông tin xác thực của người dùng. [Ranh giới quyền hạn IAM (IAM permission boundaries)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) chặn trần mọi vai trò agent, [các Điều kiện IAM (IAM Conditions)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) giới hạn truy cập theo region, thẻ, cửa sổ thời gian và VPC nguồn, và việc nâng đặc quyền vừa-đúng-lúc (just-in-time) với thu hồi tự động xử lý các thao tác đặc quyền cao. [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) và [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) cảnh báo về các thay đổi chính sách gần thời gian thực. |
| 5 | Tối ưu (Optimized) | Việc quản trị danh tính và quyền hạn được mã hóa thành quy tắc đầy đủ, với các đường cơ sở least-privilege được kiểm chứng liên tục dẫn xuất từ dữ liệu CloudTrail và các phát hiện được tổng hợp trong [AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html). Các phát hiện truy cập không dùng đến và xác thực bất thường được đưa vào khắc phục tự động. Các cuộc rà soát truy cập chạy theo nhịp khớp với hồ sơ rủi ro của khách hàng, với việc phê duyệt (sign-off) có dấu thời gian và tài liệu, và các kiểm soát danh tính được kiểm chứng qua các bài tập red-team chống lại các đường mạo danh và leo thang đặc quyền. |

## Các vấn đề thường gặp cần lưu ý

- API key dùng chung hoặc token tĩnh vẫn còn được dùng để xác thực agent, không có nhịp xoay vòng hay đường thu hồi nào được xác định. Thông tin xác thực trở thành một bí mật dài hạn phân phối qua các môi trường, và bất kỳ sự tiết lộ nào cũng phơi bày mọi agent đang giữ nó cho đến khi từng cái được xoay vòng.
- Vai trò agent và vai trò con người bị mờ ranh giới, dù là qua tái sử dụng vai trò, chuỗi vai trò (role chaining), hay thiếu các rào chắn trong trust policy và SCP, nên các dấu vết kiểm toán không thể phân biệt rành mạch hành động agent với hành động con người khi điều tra sự cố.
- Quyền hạn của agent được mở rộng theo phản ứng để đáp lại các lỗi access-denied mà không điều tra xem mẫu truy cập có nhất quán với phạm vi dự định của agent hay không, dẫn đến sự phình đặc quyền (privilege creep) đều đặn mà không cuộc rà soát đơn lẻ nào bắt được và đẩy các vai trò agent về tư thế quyền hạn rộng mà các agent tự chủ không nên có.
- Các cuộc rà soát truy cập cho các danh tính agent được tiến hành theo nhịp thừa hưởng từ các cuộc rà soát người dùng con người (hằng năm hoặc sau sự cố), mặc dù quyền hạn agent có thể trôi dạt nhanh hơn nhiều khi các công cụ, prompt và mẫu điều phối mới được thêm vào, nên người rà soát không thể phân biệt các quyền hạn thực sự không dùng với các quyền hạn được giữ cho các thay đổi năng lực agent sắp tới.
- Truy cập ủy quyền (delegated access) được hiện thực bằng cách để agent đảm nhận vai trò của người dùng thay vì mang ngữ cảnh người dùng dưới dạng các claim token đã ký, điều này làm sụp đổ dấu vết kiểm toán và cấp cho agent toàn bộ tập quyền hạn của người dùng trong suốt thời gian của phiên.

###### Các thực hành tốt

- [AGENTSEC03-BP01 Triển khai xác thực mạnh cho các danh tính agent](agentsec03-bp01.md)
- [AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người](agentsec03-bp02.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](agentsec03-bp03.md)
- [AGENTSEC03-BP04 Rà soát quyền hạn và truy cập định kỳ](agentsec03-bp04.md)
