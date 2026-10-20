# AGENTSEC02-BP01 Triển khai ủy quyền công cụ

Một agent có quyền truy cập công cụ không bị ràng buộc thì không có ranh giới đặc quyền có ý nghĩa nào. Việc ủy quyền được thực thi bên ngoài tại gateway, kết hợp với lan truyền danh tính và rà soát của con người cho các thao tác biến đổi, thực thi tính tự chủ có giới hạn (bounded autonomy) ở lớp công cụ.

**Kết quả mong muốn:**

- Bạn ủy quyền mọi lần gọi công cụ theo một chính sách đã định trước khi thực thi, với danh tính agent và ngữ cảnh người dùng được lan truyền qua chuỗi ủy quyền.
- Agent chỉ có thể gọi các công cụ trong phạm vi được phê duyệt của nó, và các ý đồ truy cập công cụ trái phép bị chặn và ghi log.
- Các điểm kiểm soát human-in-the-loop chặn các thao tác biến đổi rủi ro cao để những hành động hệ trọng nhận được rà soát trước khi thực thi.

**Các phản mẫu thường gặp (anti-patterns):**

- Cấp cho agent quyền truy cập tràn lan tới mọi công cụ có sẵn thay vì giới hạn phạm vi truy cập tới các công cụ mà mỗi agent cần.
- Dựa vào phán đoán của chính agent để quyết định liệu một lần gọi công cụ có phù hợp hay không, mà không có kiểm tra độc lập nào ở lớp công cụ hay API.
- Không lan truyền ngữ cảnh danh tính người dùng qua các lần gọi công cụ, khiến các dịch vụ phía sau không thể thực thi kiểm soát truy cập ở cấp người dùng và mọi lời gọi chạy với quyền hạn của agent.
- Bỏ qua các kiểm soát human-in-the-loop cho các thao tác biến đổi vì chúng thêm độ trễ, chấp nhận rủi ro không giới hạn cho các hành động khó hoặc không thể đảo ngược.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các chính sách RBAC giới hạn mỗi agent tới các công cụ mà các tác vụ đã định của nó cần, hiện thực hóa truy cập công cụ theo đặc quyền tối thiểu.
- Lan truyền danh tính cho phép các dịch vụ phía sau thực thi kiểm soát truy cập ở cấp người dùng trên các tài nguyên được chạm tới qua các lần gọi công cụ của agent.
- Giới hạn tốc độ và các kiểm soát human-in-the-loop ràng buộc việc thực thi tự chủ vào các thao tác có hồ sơ rủi ro chấp nhận được.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Việc ủy quyền chỉ được hiện thực qua các chỉ thị trong prompt là không đủ vì prompt có thể bị thao túng qua cách diễn đạt đối kháng hoặc prompt injection. Hãy hiện thực việc ủy quyền như một kiểm tra bên ngoài, xác định (deterministic), diễn ra trước khi công cụ thực thi, bất kể agent đi đến lời gọi bằng cách nào. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) là điểm thực thi, và [Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) là bộ máy quy tắc.

Gateway chạy một mô hình bảo mật hai chiều. Ở chiều vào (inbound), nó tuân theo đặc tả ủy quyền MCP và đóng vai trò một máy chủ tài nguyên OAuth, hoạt động với Amazon Cognito, Okta, Auth0 hoặc nhà cung cấp OAuth của riêng bạn. Bạn cấu hình các client ID và audience được phê duyệt để kiểm soát ứng dụng và agent nào có thể chạm tới công cụ của bạn, và Gateway hỗ trợ cả luồng authorization code (3LO) lẫn luồng client credentials (2LO) cho giao tiếp dịch vụ-tới-dịch vụ. Ở chiều ra (outbound), mô hình xác thực phụ thuộc vào loại target: các target AWS Lambda và Smithy model dùng ủy quyền dựa trên IAM thông qua một vai trò bạn cấu hình với quyền hạn giới hạn phạm vi, và các target OpenAPI hỗ trợ API key hoặc grant client credentials OAuth 2LO. Các nhà cung cấp thông tin xác thực tài nguyên của [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html) xử lý việc lưu bộ nhớ đệm token và lưu trữ an toàn, và mỗi target gắn với đúng một cấu hình xác thực để có ranh giới rõ ràng và khả năng kiểm toán.

Policy là nơi việc ủy quyền chi tiết cư trú. Các chính sách Cedar đánh giá mọi yêu cầu agent-tới-công cụ tại gateway trước khi thực thi, với tư thế mặc-định-từ-chối nơi forbid luôn thắng permit. Các điều kiện có thể tham chiếu các claim OAuth từ token JWT (vai trò người dùng, scope, các định danh cấp tenant như patient ID), các tham số đầu vào của công cụ, và ngữ cảnh thời điểm chạy như giờ trong ngày. Điều đó cho phép bạn diễn đạt các quy tắc như "role=clinician có thể sắp lại lịch hẹn cho các bệnh nhân trong panel của họ" như một chính sách xác định thay vì một hy vọng về prompt. Chính sách có thể được viết trực tiếp bằng Cedar hoặc sinh từ ngôn ngữ tự nhiên, và Gateway hỗ trợ chế độ LOG_ONLY để bạn có thể kiểm chứng hành vi chính sách với lưu lượng thực trước khi chuyển sang chế độ enforce.

Quá tải công cụ (tool overload) là một rủi ro riêng. Trình bày cho agent hàng trăm công cụ làm tăng khả năng nó chọn nhầm hoặc theo một đường thực thi kém hiệu quả. Công cụ dựng sẵn x_amz_bedrock_agentcore_search của Gateway phơi bày khám phá công cụ theo ngữ nghĩa để agent định vị các công cụ liên quan qua ngôn ngữ tự nhiên thay vì thấy toàn bộ kho. Điều đó giảm bề mặt mà mô hình phải suy luận trong bất kỳ lượt nào.

Với các công cụ thực hiện thao tác biến đổi (ghi vào cơ sở dữ liệu, gửi email đi, giao dịch tài chính), rà soát human-in-the-loop thuộc về đường thực thi, không phải prompt. Các mẫu callback của AWS Step Functions cho phép một agent tạm dừng và chờ phê duyệt. Luồng công việc gửi một yêu cầu phê duyệt qua Amazon SNS hoặc Amazon SES và chỉ tiếp tục sau khi một con người phản hồi trong một thời gian chờ đã định. Hãy cấu hình các đường leo thang (escalation) cho các timeout để một phản hồi trễ không âm thầm chặn một hành động hợp lệ. Giới hạn tốc độ ở cả cấp Gateway lẫn cấp API công cụ giúp ngăn cạn kiệt tài nguyên: các usage plan và throttling của Amazon API Gateway thực thi giới hạn tốc độ theo từng agent, và concurrency dự trữ của AWS Lambda chặn số lần gọi công cụ song song tối đa. Gateway công bố các chỉ số sử dụng, gọi, hiệu năng và lỗi tới Amazon CloudWatch và tích hợp với AWS CloudTrail để có một dấu vết kiểm toán đầy đủ, nên các vòng lặp mất kiểm soát và các mẫu gọi bất ngờ nổi lên thành tín hiệu.

### Các bước triển khai

- **Cấu hình OAuth vào cho Gateway:** Tạo một [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) và đấu nối ủy quyền OAuth vào với nhà cung cấp danh tính của bạn (Amazon Cognito, Okta, Auth0 hoặc nhà cung cấp OAuth của riêng bạn), chỉ định các client ID và audience được phê duyệt.
- **Thêm target với thông tin xác thực ra được giới hạn phạm vi:** Đăng ký các API công cụ làm target gateway, cấu hình các vai trò IAM cho target Lambda và Smithy và API key hoặc OAuth 2LO cho target OpenAPI, và quản lý thông tin xác thực ra qua các nhà cung cấp thông tin xác thực tài nguyên của [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html).
- **Viết các chính sách Cedar cho việc ủy quyền:** Tạo một bộ máy chính sách trong [Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) và định nghĩa các chính sách Cedar với các điều kiện có nhận thức về danh tính trên các claim OAuth (vai trò người dùng, scope, ID người dùng) và các tham số đầu vào của công cụ. Viết trực tiếp bằng Cedar hoặc sinh chính sách từ mô tả ngôn ngữ tự nhiên.
- **Kiểm chứng chính sách ở LOG_ONLY trước khi thực thi:** Liên kết bộ máy chính sách với Gateway ở chế độ LOG_ONLY, xem xét các log khả năng quan sát để xác nhận các chính sách tạo ra các quyết định permit và deny như mong đợi, rồi chuyển sang chế độ enforce.
- **Bật khám phá công cụ theo ngữ nghĩa:** Chọn tham gia công cụ dựng sẵn x_amz_bedrock_agentcore_search để agent định vị các công cụ liên quan qua các truy vấn ngôn ngữ tự nhiên thay vì suy luận trên toàn bộ kho.
- **Thêm phê duyệt human-in-the-loop cho các công cụ biến đổi:** Đấu nối các mẫu callback của AWS Step Functions cho các công cụ rủi ro cao, gửi yêu cầu phê duyệt qua Amazon SNS hoặc Amazon SES, và cấu hình các đường leo thang cho các timeout của người rà soát.
- **Chặn concurrency và tốc độ yêu cầu:** Thực thi giới hạn tốc độ theo từng agent qua các usage plan của Amazon API Gateway và chặn số lần gọi song song bằng concurrency dự trữ của AWS Lambda để giúp ngăn cạn kiệt tài nguyên.
- **Giám sát các quyết định ủy quyền:** Dùng các chỉ số Amazon CloudWatch và tích hợp AWS CloudTrail của Gateway để theo dõi các lần gọi công cụ, thất bại ủy quyền và các sự kiện giới hạn tốc độ, và cấu hình cảnh báo cho các đợt tăng đột biến thất bại ủy quyền.
- **Rà soát ủy quyền công cụ hàng quý:** Loại bỏ các quyền hạn không dùng và siết chặt các ranh giới truy cập theo nhịp định kỳ khi khối công việc và công cụ tiến hóa.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ](agentsec02-bp02.md)
- [AGENTSEC02-BP03 Duy trì registry công cụ được phê duyệt kèm đánh giá bảo mật](agentsec02-bp03.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](../3-agentsec03/agentsec03-bp03.md)
- [AGENTREL02-BP02 Giới hạn quyền hạn agent tới mức truy cập tối thiểu cần thiết](../../3-reliability/2-agentrel02/agentrel02-bp02.md)
- [AGENTCOST04-BP01 Thiết kế lựa chọn công cụ tiết kiệm chi phí để giảm thiểu các lần gọi không cần thiết](../../5-cost-optimization/4-agentcost04/agentcost04-bp01.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html)
- [Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Apply fine-grained access control with Bedrock AgentCore Gateway interceptors](https://aws.amazon.com/blogs/machine-learning/apply-fine-grained-access-control-with-bedrock-agentcore-gateway-interceptors/)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [Tài liệu Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-identity.html)

**Ví dụ liên quan:**

- [Healthcare appointment agent with Policy enforcement (GitHub)](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases/healthcare-appointment-agent)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
