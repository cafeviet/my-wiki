# AGENTREL04-BP01 Triển khai mẫu tác nhân trọng tài (arbiter) cho các hệ thống đa tác nhân được phối hợp

Phối hợp ngang hàng giữa các tác nhân tạo ra bế tắc và các hành động xung đột khi mở rộng quy mô. Một **trọng tài (arbiter)** chuyên trách chỉ kích hoạt để giải quyết xung đột bảo toàn quyền tự chủ của tác nhân cho công việc bình thường, đồng thời cung cấp một nơi có thẩm quyền duy nhất để giải quyết tranh chấp tài nguyên dùng chung.

**Kết quả mong muốn:**

- Bạn có một tác nhân trọng tài kích hoạt để giải quyết xung đột trong khi để việc phối hợp thường quy cho các tác nhân chuyên biệt liên quan.
- Bạn lưu các chính sách giải quyết xung đột trong một kho cấu hình để cập nhật chính sách không đòi hỏi triển khai lại trọng tài.
- Bạn leo thang các xung đột không giải quyết được tới con người rà soát một cách tự động.

**Các phản mẫu thường gặp (anti-patterns):**

- Để các tác nhân phối hợp trực tiếp mà không có một trọng tài trung tâm, tạo ra các phụ thuộc vòng và bế tắc khi các yêu cầu xung đột.
- Nhúng logic giải quyết xung đột bên trong các tác nhân chuyên biệt, tạo ra sự trọng tài không nhất quán trên toàn hệ thống.
- Định tuyến mọi tương tác tác nhân qua trọng tài, biến nó thành một nút thắt cổ chai về hiệu năng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Bế tắc và các hành động xung đột được giải quyết bởi một thẩm quyền duy nhất thay vì rò rỉ vào logic nghiệp vụ.
- Hành vi luồng công việc nhất quán đến từ các chính sách trọng tài được áp dụng đồng nhất trên toàn đội.
- Các tác nhân chuyên biệt vẫn độc lập vì logic phối hợp được triển khai trong trọng tài, không phải trong chúng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Thiết kế trọng tài như một thành phần theo hướng sự kiện thay vì một bộ điều phối đồng bộ. Trọng tài đăng ký (subscribe) các sự kiện phối hợp qua Amazon EventBridge hoặc Amazon SQS, chỉ kích hoạt khi một tác nhân chuyên biệt yêu cầu trọng tài một cách tường minh, và công bố các quyết định trở lại các tác nhân yêu cầu. Trọng tài đồng bộ tạo ra một nút thắt cổ chai làm giảm quyền tự chủ của tác nhân.

Hình dạng của chính sách quan trọng ngang với vị trí đặt trọng tài. Ba loại bao phủ hầu hết các xung đột phối hợp thực tế. Xếp thứ tự theo mức ưu tiên xử lý tranh chấp tài nguyên, chấm điểm độ tin cậy (confidence scoring) giải quyết các quyết định xung đột, và các chỉ dẫn hoàn tác (rollback) xử lý các vi phạm ràng buộc. Lưu các chính sách trong Parameter Store, một năng lực của AWS Systems Manager, hoặc Amazon DynamoDB để chúng có thể được cập nhật mà không cần triển khai lại trọng tài. Khi một chính sách hóa ra sai, bản sửa nhanh chóng được áp dụng thay vì chờ một chu kỳ triển khai. Đối với nhu cầu trọng tài thời gian thực, triển khai trọng tài như một dịch vụ đồng bộ được gọi qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), chấp nhận rằng các đường đó sẽ chậm hơn nhưng dành chúng cho các trường hợp bất đồng bộ không chấp nhận được.

Giám sát trọng tài giữ cho việc phối hợp lành mạnh. Theo dõi tần suất xung đột, độ trễ trọng tài và tỷ lệ leo thang qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Dùng Amazon CloudWatch Contributor Insights để xác định các cặp tác nhân hoặc loại tài nguyên thường xuyên liên quan đến xung đột nhất. Đó là các cặp mà việc thiết kế lại giao thức phối hợp mang lại lợi ích cao nhất. Các xung đột không giải quyết được leo thang tới con người rà soát qua các thông báo Amazon SNS hoặc một tích hợp ticketing để chúng không bị âm thầm bỏ qua.

### Các bước triển khai

- **Thiết kế trọng tài như một tác nhân theo hướng sự kiện trên AgentCore Runtime:** Triển khai trọng tài trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) và cho nó đăng ký các sự kiện phối hợp qua EventBridge, chỉ kích hoạt để giải quyết xung đột.
- **Tạo các chính sách giải quyết xung đột trong một kho cấu hình:** Lưu các quy tắc cho tranh chấp tài nguyên, các quyết định xung đột và các vi phạm ràng buộc trong Parameter Store (một năng lực của AWS Systems Manager) hoặc Amazon DynamoDB.
- **Công bố các quyết định qua EventBridge hoặc AgentCore Gateway:** Định tuyến các quyết định trọng tài trở lại các tác nhân bị ảnh hưởng qua EventBridge cho các đường bất đồng bộ hoặc gọi trực tiếp qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cho nhu cầu đồng bộ.
- **Cấu hình cảnh báo CloudWatch và Contributor Insights:** Cảnh báo trên tần suất xung đột bất thường và dùng Contributor Insights để phơi bày các cặp tác nhân và loại tài nguyên dễ tranh chấp nhất.
- **Triển khai leo thang tới con người rà soát:** Định tuyến các xung đột không giải quyết được tới các thông báo Amazon SNS hoặc một tích hợp ticketing để chúng tới được người vận hành.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL04-BP02 Phân loại các tác nhân bằng một phân loại năng lực kỹ lưỡng](agentrel04-bp02.md)
- [AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác](agentrel04-bp03.md)
- [AGENTREL04-BP04 Triển khai các control plane bền bỉ cho việc phối hợp tác nhân](agentrel04-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Customize agent workflows with advanced orchestration techniques using Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/)
- [Multi Agent Collaboration with Strands](https://aws.amazon.com/blogs/devops/multi-agent-collaboration-with-strands/)

**Video liên quan:**

- [Breaking multi-agent silos: A2A + MCP in action with Strands Agents](https://www.youtube.com/watch?v=TjTgHA5DjDM)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Multi-agent tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime/03-advanced-concepts)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
