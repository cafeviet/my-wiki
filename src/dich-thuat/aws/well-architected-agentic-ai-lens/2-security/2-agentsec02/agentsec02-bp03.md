# AGENTSEC02-BP03 Duy trì registry công cụ được phê duyệt kèm đánh giá bảo mật

Mọi công cụ mà agent có thể chạm tới đều là một phần của bề mặt đặc quyền hiệu dụng của nó. Một registry có quản lý phiên bản với các ranh giới bảo mật có tài liệu, được thực thi tại thời điểm gọi, giữ các công cụ chưa được thẩm định hoặc đã khấu hao ra khỏi đường gọi của agent.

**Kết quả mong muốn:**

- Bạn duy trì một registry tập trung, có quản lý phiên bản của các công cụ được phê duyệt, mỗi công cụ có ranh giới bảo mật có tài liệu, quyền hạn yêu cầu, các mức phân loại dữ liệu và một đánh giá lỗ hổng hiện hành.
- Agent chỉ có thể truy cập các công cụ hiện diện trong registry, và các công cụ chưa được phê duyệt bị chặn theo mặc định.
- Bạn liên tục kiểm chứng registry về tuân thủ, và các công cụ đã khấu hao được loại bỏ khỏi quyền truy cập của agent một cách tự động.

**Các phản mẫu thường gặp (anti-patterns):**

- Cho phép agent khám phá và gọi bất kỳ công cụ hoặc máy chủ MCP có sẵn nào mà không có rà soát bảo mật trước và phê duyệt registry.
- Duy trì registry công cụ như một tài liệu tĩnh thay vì một kiểm soát được thực thi, khiến agent có thể vượt qua nó và gọi trực tiếp các công cụ chưa được phê duyệt.
- Không phân biệt giữa các công cụ được lưu trữ cục bộ và các máy chủ MCP từ xa trong đánh giá rủi ro, đánh giá thấp phạm vi mở rộng từ kết nối mạng bên ngoài.
- Bỏ qua ghim phiên bản cho các công cụ được phê duyệt, khiến agent nhận các phiên bản mới chưa trải qua rà soát bảo mật.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tư thế từ-chối-theo-mặc-định (deny-by-default) ràng buộc các năng lực của agent vào một tập công cụ và thao tác đã được phê duyệt trước, đã được rà soát bảo mật.
- Quản lý phiên bản giúp ngăn agent dùng các phiên bản công cụ chưa được rà soát và cung cấp một dấu vết kiểm toán về phiên bản nào đã được phê duyệt và khi nào.
- Các kiểm tra tuân thủ tự động phát hiện trôi dạt so với registry được phê duyệt và kích hoạt các luồng công việc khắc phục.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một registry công cụ phải được thực thi tại thời điểm chạy để có hiệu quả. Hãy ghi các công cụ được phê duyệt vào một registry và cấu hình đường gọi để từ chối các công cụ không có trong danh sách. Mẫu thiết kế là một registry mà agent không thể vượt qua: các công cụ chỉ có thể chạm tới qua một target gateway, agent chỉ được ủy quyền qua một bộ máy chính sách với ngữ nghĩa mặc-định-từ-chối, và một quy trình tuân thủ ngoài băng (out-of-band) phát hiện trôi dạt giữa registry và những gì thực sự được cấu hình.

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) cung cấp điểm tập trung cho lưu lượng agent-tới-công cụ. Mỗi target gateway đại diện cho một dịch vụ backend hoặc một nhóm API được phơi bày dưới dạng công cụ cho agent, với các lược đồ công cụ đã định, các cấu hình xác thực và các kiểm soát truy cập. Tuy nhiên, riêng Gateway không phải là deny-by-default: thêm một target làm nó ngay lập tức truy cập được như một công cụ MCP đối với bất kỳ agent nào chạm tới điểm cuối gateway. Để giới hạn agent nào có thể gọi công cụ nào, hãy xếp thêm các chính sách Cedar của [Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) với tư thế mặc-định-từ-chối, Gateway Interceptor cho logic truy cập tùy chỉnh dựa trên Lambda, hoặc cả hai. Lớp chính sách là thứ biến một registry đã được điền dữ liệu thành một ủy quyền được thực thi.

Các môi trường phát triển cần một kiểm soát thứ hai. Khi lập trình viên và agent tương tác với các máy chủ MCP qua các công cụ dựa trên IDE, một MCP registry — một allowlist JSON của các máy chủ được phê duyệt lưu trữ trên một điểm cuối HTTPS như Amazon S3 hoặc một máy chủ web nội bộ — cung cấp cho client một danh sách máy chủ để tải khi khởi động và đồng bộ lại định kỳ (thường mỗi 24 giờ). Các máy chủ không có trong registry bị chặn, và nếu một máy chủ cài đặt cục bộ bị loại khỏi registry, client sẽ chấm dứt nó và giúp ngăn nó được thêm lại. Registry hỗ trợ ghim phiên bản để một phiên bản mới tự động khởi động lại client với phiên bản đã cập nhật, và định dạng tệp tuân theo [chuẩn mở MCP Registry](https://github.com/modelcontextprotocol/registry) nên khoản đầu tư không bị gắn với một công cụ hay nhà cung cấp duy nhất. Việc quản trị MCP registry có thể được cấu hình ở cấp tổ chức với các ghi đè ở cấp tài khoản, ví dụ tắt MCP cho tổ chức theo mặc định nhưng bật nó với một allowlist cụ thể cho một số nhóm nhất định.

Ở quy mô doanh nghiệp, một trung tâm máy chủ MCP tập trung hợp nhất những gì lẽ ra sẽ trở thành sự bùng nổ các kết nối theo từng nhóm. Các nhóm phát triển các máy chủ MCP cho chức năng cụ thể của họ, nhưng các máy chủ được lưu trữ tập trung và truy cập được trên toàn tổ chức qua một registry dùng chung hoặc một discovery API được hậu thuẫn bởi Amazon DynamoDB, ghi mục lục các máy chủ có sẵn cùng mô tả, định nghĩa công cụ và yêu cầu truy cập của chúng. Truy cập ở cấp mạng dùng AWS PrivateLink và VPC endpoint để agent chỉ kết nối tới các máy chủ tin cậy do tổ chức lưu trữ, và mỗi máy chủ chạy như một container cô lập trên Amazon ECS với AWS Fargate để mở rộng độc lập mà không ảnh hưởng đến các máy chủ khác.

Các máy chủ MCP từ xa cần một rà soát bảo mật tăng cường. Chúng đưa vào kết nối mạng tới các dịch vụ bên ngoài, mở rộng phạm vi vượt ngoài tầm kiểm soát trực tiếp của tổ chức. Hãy đánh giá các cơ chế xác thực, các thực hành xử lý dữ liệu và mức phơi bày mạng, đồng thời áp dụng các kiểm soát mạng như VPC endpoint và security group để giới hạn kết nối tới các điểm cuối cần thiết. Khi đưa các công cụ vào Gateway hoặc MCP registry, hãy quét các đặc tả API tìm rủi ro bảo mật, kiểm chứng xác thực, đánh giá xử lý dữ liệu, làm giàu metadata công cụ bằng mô tả, ví dụ sử dụng và đặc tính hiệu năng, và nhóm các API vào các target gateway theo miền kinh doanh, yêu cầu ủy quyền ra và loại API.

Gateway hỗ trợ sáu loại target:

- Hàm Lambda
- REST API của API Gateway
- Lược đồ OpenAPI
- Mô hình Smithy
- Máy chủ MCP bên ngoài
- Các template dựng sẵn từ các nhà cung cấp tích hợp

Các template dựng sẵn cung cấp các tích hợp được tuyển chọn, cấu hình sẵn cho các nền tảng SaaS phổ biến bao gồm Salesforce, Slack, Jira, Asana, Zendesk và ServiceNow, với một tập con API nhà cung cấp đã được thẩm định phơi bày qua gateway. Định tuyến mọi truy cập công cụ qua Gateway (các dịch vụ nội bộ, các máy chủ MCP bên ngoài và các tích hợp SaaS gốc) hợp nhất xác thực, thực thi lược đồ và đánh giá chính sách dưới một điểm cuối. Các IDE như Kiro, Claude Code và Cursor kết nối qua Amazon Bedrock AgentCore MCP Server, cầu nối các MCP client dựa trên IDE tới điểm cuối gateway.

Phát hiện tuân thủ liên tục giữ cho registry có thể thực thi theo thời gian. Hãy duy trì một kho cấu hình trong Parameter Store, một năng lực của AWS Systems Manager hoặc AWS AppConfig, cùng với cấu hình gateway, với các mục cho tên công cụ, phiên bản được phê duyệt, các quyền hạn IAM yêu cầu, mức phân loại dữ liệu, ngày rà soát bảo mật và ngày hết hạn. Dùng các quy tắc AWS Config để kiểm chứng rằng các lần triển khai agent chỉ tham chiếu các công cụ được registry phê duyệt, và kích hoạt các thông báo Amazon EventBridge cho việc không tuân thủ. Các luồng công việc khấu hao tự động loại bỏ các công cụ hết hạn khỏi registry, cập nhật các cấu hình agent và giúp ngăn việc tiếp tục sử dụng.

### Các bước triển khai

- **Xây dựng registry có cấu trúc:** Tạo một registry công cụ trong Parameter Store, một năng lực của AWS Systems Manager hoặc AWS AppConfig, với các mục cho mỗi công cụ được phê duyệt bao gồm phiên bản, quyền hạn, phân loại dữ liệu và metadata rà soát.
- **Thêm các công cụ được phê duyệt làm target Gateway:** Với lưu lượng agent-tới-công cụ, đăng ký các công cụ được phê duyệt làm target [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) với các lược đồ công cụ đã định, các cấu hình xác thực ra và các kiểm soát truy cập. Nhóm các target theo miền kinh doanh, yêu cầu ủy quyền và loại API.
- **Công bố một MCP registry cho phát triển:** Tạo một tệp JSON MCP registry tuân theo [chuẩn mở MCP Registry](https://github.com/modelcontextprotocol/registry), lưu trữ nó trên một điểm cuối HTTPS, và cấu hình nó trong cài đặt quản trị của tổ chức với ghim phiên bản cho mỗi mục máy chủ.
- **Định nghĩa quy trình rà soát bảo mật:** Thiết lập một cuộc rà soát bao gồm quét đặc tả API, đánh giá quyền hạn, lập bản đồ luồng dữ liệu và kiểm chứng cơ chế xác thực, với các phát hiện được ghi vào mục registry và một ngày hết hạn rà soát.
- **Xây dựng một trung tâm tập trung ở quy mô doanh nghiệp:** Với các lần triển khai đa LOB (line of business), hiện thực một trung tâm máy chủ MCP tập trung với một discovery API được hậu thuẫn bởi Amazon DynamoDB, truy cập ở cấp mạng qua AWS PrivateLink và VPC endpoint, và lưu trữ container cô lập trên Amazon ECS với AWS Fargate.
- **Thực thi mặc-định-từ-chối qua Policy:** Cấu hình các chính sách Cedar trong AgentCore Policy để chỉ các công cụ được cho phép tường minh mới có thể được gọi, cung cấp một lớp thực thi thứ hai ngoài cấu hình target Gateway.
- **Áp dụng rà soát tăng cường cho các máy chủ MCP từ xa:** Đánh giá mức phơi bày mạng và xác thực bên ngoài, và áp dụng VPC endpoint và security group để giới hạn kết nối.
- **Phát hiện trôi dạt registry liên tục:** Triển khai các quy tắc AWS Config để phát hiện các cấu hình agent tham chiếu các công cụ chưa được phê duyệt, và kích hoạt các thông báo Amazon EventBridge để khắc phục.
- **Tự động hóa khấu hao:** Cho các công cụ hết hạn quá ngày rà soát của chúng, loại chúng khỏi các target Gateway và MCP registry, và cập nhật các cấu hình agent để giúp ngăn việc tiếp tục sử dụng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC02-BP01 Triển khai ủy quyền công cụ](agentsec02-bp01.md)
- [AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ](agentsec02-bp02.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](../3-agentsec03/agentsec03-bp03.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html)
- [Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Transform your MCP architecture: Unite MCP servers through AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)
- [Enterprise governance: control your MCP servers and models](https://kiro.dev/blog/enterprise-governance-mcp-and-models/)
- [MCP governance for Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/mcp-governance.html)
- [Accelerating AI innovation: Scale MCP servers for enterprise workloads with Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerating-ai-innovation-scale-mcp-servers-for-enterprise-workloads-with-amazon-bedrock/)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [Parameter Store, a capability of AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

**Ví dụ liên quan:**

- [Accelerating AI Innovation: Scaling Model Context Protocol Servers for Enterprise Workloads on AWS (GitHub)](https://github.com/aws-samples/sample-deploy-mcp-servers-at-scale-on-aws)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Systems Manager](https://aws.amazon.com/systems-manager/)
- [AWS Config](https://aws.amazon.com/config/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [AWS AppConfig](https://aws.amazon.com/systems-manager/features/appconfig/)
- [Amazon ECS](https://aws.amazon.com/ecs/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
