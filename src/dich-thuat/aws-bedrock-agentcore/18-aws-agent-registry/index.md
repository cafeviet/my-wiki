---
title: "AWS Agent Registry: Lập catalog và khám phá tài nguyên AI tập trung"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---

# AWS Agent Registry: Lập catalog và khám phá tài nguyên AI tập trung

# AWS Agent Registry: Khám phá và quản lý các agent, tool và tài nguyên

- [AWS Agent Registry là gì?](#registry-what-is)

- [Tại sao dùng AWS Agent Registry?](#registry-why-use)

- [Cách hoạt động](#registry-how-it-works)

- [Truy cập AWS Agent Registry](#registry-accessing)

- [Các dịch vụ liên quan](#registry-related-services)

- [Các khả năng chính](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-key-capabilities.html)

- [Khái niệm và thuật ngữ](/dich-thuat/aws-bedrock-agentcore/18-aws-agent-registry/registry-concepts)

- [Điều kiện tiên quyết](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-prerequisites.html)

- [Các trường hợp dùng mẫu](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-use-cases.html)

- [Bắt đầu với AWS Agent Registry](/dich-thuat/aws-bedrock-agentcore/18-aws-agent-registry/registry-get-started)

- [Tạo và quản lý các registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-managing-registries.html)

- [Tạo và quản lý các registry record](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-managing-records.html)

- [Tuyển chọn registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-curating.html)

- [Khám phá registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-searching.html)

- [Thông báo (Amazon EventBridge)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-eventbridge.html)

- [Dùng AWS Agent Registry với AWS Organizations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-organizations.html)

- [Chia sẻ một registry qua nhiều tài khoản với AWS RAM](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-cross-account-sharing.html)

- [Ghi log các lời gọi API Registry với AWS CloudTrail](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-cloudtrail.html)

- [VPC và AWS PrivateLink với AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-privatelink.html)

- [IAM Permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-iam-permissions.html)

- [Bảo vệ dữ liệu trong AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-data-protection.html)

- [Dùng service-linked role cho AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-service-linked-role-agent-registry.html)

- [Khắc phục sự cố](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-troubleshooting.html)

- [Hướng dẫn di chuyển registry toàn diện](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-faq.html)

## AWS Agent Registry là gì?

AWS Agent Registry là một dịch vụ khám phá được quản lý hoàn toàn, cung cấp một catalog tập trung để tổ chức, tuyển chọn và khám phá các tài nguyên trên toàn tổ chức của bạn. Với AWS Agent Registry, bạn có thể xuất bản các MCP server, tool (công cụ), agent (tác tử AI), agent skill và các tài nguyên tùy chỉnh vào một registry có thể tìm kiếm, kiểm soát truy cập qua một quy trình phê duyệt, và cho phép cả người dùng con người lẫn các agent AI khám phá đúng tool và agent thông qua tìm kiếm lai (hybrid), duyệt catalog và một endpoint MCP nguyên bản.

## Tại sao dùng AWS Agent Registry?

Khi các tổ chức mở rộng việc sử dụng các agent AI và tool, việc khám phá đúng tài nguyên trở nên ngày càng khó khăn. Các nhóm xây dựng MCP server, triển khai agent và tạo các tool chuyên biệt — nhưng nếu không có một catalog trung tâm, các tài nguyên này vẫn bị phân mảnh và khó tìm. Điều này cũng gây ra trùng lặp công sức và tăng nợ kỹ thuật khi các nhóm xây lại các tài nguyên vốn đã tồn tại đơn giản vì họ không thể khám phá ra chúng. AWS Agent Registry giải quyết vấn đề này bằng cách cung cấp:

- **Khám phá tập trung** – Một nơi duy nhất để tìm mọi tài nguyên đã xuất bản trên toàn tổ chức của bạn, có thể tìm kiếm bởi cả con người lẫn agent.

- **Quản trị và tuyển chọn** – Một quy trình phê duyệt đảm bảo chỉ những record đáp ứng các tiêu chí của tổ chức về bảo mật, tuân thủ và chất lượng mới có thể được khám phá. Quản trị viên kiểm soát những gì builder trong tổ chức của họ có thể khám phá và sử dụng, và có thể gỡ bỏ khả năng khám phá của các tài nguyên bất cứ lúc nào.

- **Các loại tài nguyên linh hoạt** – Đăng ký các MCP server, agent, skill và bất kỳ tài nguyên tùy chỉnh nào. AWS Agent Registry xác thực các record MCP và agent theo các schema giao thức tương ứng của chúng, và hỗ trợ metadata tùy chỉnh cho mọi loại tài nguyên.

- **Tìm kiếm lai (hybrid)** – Kết hợp hiểu biết ngữ nghĩa với khớp từ khóa để cả các truy vấn ngôn ngữ tự nhiên lẫn tra cứu tên chính xác đều trả về kết quả liên quan.

- **Duyệt catalog** – Phân trang qua các record đã phê duyệt với bộ lọc, hoặc lấy chi tiết cho nhiều record cùng lúc, để xây dựng các trải nghiệm khám phá kiểu thư mục.

- **Truy cập MCP-native** – Registry khả dụng tại một endpoint MCP từ xa, cho phép các client tương thích MCP tương tác trực tiếp với registry bằng Model Context Protocol.

- **Ủy quyền linh hoạt** – Chọn giữa credential AWS IAM hoặc JSON Web Token (JWT) từ nhà cung cấp danh tính doanh nghiệp của bạn để kiểm soát ai có thể tìm kiếm, duyệt và gọi endpoint MCP của registry.

## Cách hoạt động

AWS Agent Registry được tổ chức xoay quanh hai tài nguyên cốt lõi:

- **Registries** – Một registry là một catalog mà bạn tạo trong tài khoản AWS của mình. Mỗi registry có Name, Description, cấu hình Authorization (IAM hoặc JWT), các thiết lập phê duyệt và tập record riêng. Bạn có thể tạo một registry duy nhất cho toàn tổ chức, tạo các registry được tổ chức theo loại tài nguyên (chẳng hạn agent registry, MCP server registry hoặc skill registry), theo giai đoạn phát triển (production, QA, development), theo nhóm hoặc đơn vị kinh doanh — bất kỳ cách thiết lập nào phù hợp nhất với bạn.

- **Registry records** – Một record đại diện cho một tài nguyên riêng lẻ được xuất bản vào một registry. Mỗi record ghi lại metadata chính mô tả tài nguyên bên dưới — cung cấp thông tin về nó là gì, nó làm gì, và có thể tìm thấy nó như thế nào.

### Quy trình làm việc điển hình

- **Tạo một registry** – Một quản trị viên tạo một registry và cấu hình các thiết lập ủy quyền và phê duyệt.

- **Xuất bản record** – Một publisher tạo các registry record mô tả các MCP server, agent hoặc tool của họ, và gửi chúng để phê duyệt.

- **Tuyển chọn registry** – Một curator (hoặc quản trị viên) xem xét các record đang chờ phê duyệt và phê duyệt hoặc từ chối chúng; họ cũng deprecate các record không còn được dùng.

- **Khám phá tài nguyên** – Người tiêu dùng/Người dùng cuối tìm kiếm, duyệt catalog các record đã phê duyệt, hoặc kết nối tới endpoint MCP của registry để tìm các tài nguyên liên quan đến nhu cầu của họ.

Bạn có thể tìm hiểu thêm về cách cấu hình IAM Permissions đặc thù cho từng Persona trong [Các Persona chính](/dich-thuat/aws-bedrock-agentcore/18-aws-agent-registry/registry-concepts#registry-concept-personas).

## Truy cập AWS Agent Registry

Bạn có thể tương tác với AWS Agent Registry bằng cách gọi trực tiếp các API công khai của dịch vụ Registry qua AWS CLI hoặc AWS SDK, hoặc bằng cách gọi endpoint MCP của registry với bất kỳ client tương thích MCP hợp lệ nào.

## Các dịch vụ liên quan

- [Host agent hoặc tool với Amazon Bedrock AgentCore Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/) – Triển khai và chạy các agent và MCP server mà bạn đăng ký.

- [Amazon Bedrock AgentCore Gateway: Kết nối bảo mật các tool và tài nguyên khác tới Gateway của bạn](/dich-thuat/aws-bedrock-agentcore/08-gateway/) – Chuyển đổi các API và hàm Lambda thành các tool tương thích MCP có thể được đăng ký.

- [Cung cấp quản lý danh tính và credential cho các ứng dụng agent với Amazon Bedrock AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/) – Quản lý các nhà cung cấp danh tính (identity) và credential được dùng cho ủy quyền registry dựa trên JWT.

- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) – Nhận thông báo khi các registry record được gửi để phê duyệt.

- [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) – Ghi log và giám sát mọi lời gọi API tới AWS Agent Registry.
