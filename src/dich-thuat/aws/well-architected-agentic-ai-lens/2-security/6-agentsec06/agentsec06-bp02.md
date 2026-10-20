# AGENTSEC06-BP02 Triển khai các kiểm soát bảo mật điều phối luồng công việc

Lớp điều phối là nơi một kiểm tra yếu đơn lẻ lan tràn thành một thất bại toàn hệ thống. Các kiểm soát truy cập trên các state machine, kiểm định đầu vào trên các chuyển tiếp, và các cầu dao ngắt trên các tác vụ agent giữ các luồng công việc đa agent trên các đường thực thi được phê duyệt thay vì các đường bất ngờ.

**Kết quả mong muốn:**

- Lớp điều phối luồng công việc thực thi các kiểm soát truy cập nghiêm ngặt giúp ngăn chỉnh sửa trái phép các định nghĩa luồng công việc hoặc trạng thái thực thi.
- Kiểm định state machine giúp giữ các luồng công việc trên các mẫu thực thi mong đợi, và các cầu dao ngắt được thiết kế để chặn các thất bại ở một agent lan tràn qua toàn bộ luồng công việc.
- Bạn ghi log mọi lần thực thi luồng công việc với đủ chi tiết để tái dựng đường thực thi phục vụ các cuộc điều tra bảo mật.

**Các phản mẫu thường gặp (anti-patterns):**

- Cấp các quyền hạn IAM rộng để bắt đầu, dừng hoặc chỉnh sửa các luồng công việc Step Functions mà không hạn chế truy cập tới các state machine cụ thể, để cho bất kỳ principal nào có quyền hạn luồng công việc chỉnh sửa hoặc kích hoạt bất kỳ luồng công việc nào trong tài khoản.
- Không hiện thực kiểm định đầu vào trong các định nghĩa state machine, để cho các payload đầu vào được chế tạo điều hướng các luồng công việc vào các đường thực thi bất ngờ.
- Không hiện thực các cầu dao ngắt, nên một agent đơn lẻ đang thất bại lan tràn các thất bại qua toàn bộ luồng công việc mà không có cơ chế tự động nào để dừng thử lại một bước bị hỏng.
- Dùng các cấu hình thử lại (retry) quá phóng khoáng, để cho một agent lặp đi lặp lại thử cùng một thao tác trước khi bất kỳ cầu dao ngắt nào kích hoạt và có khả năng khuếch đại vấn đề gốc.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm định trạng thái và thực thi lược đồ đầu vào giữ các luồng công việc trong các ranh giới đã định.
- Các cầu dao ngắt tự động dừng các thất bại lan tràn và định tuyến các lần thực thi bị ảnh hưởng tới các đường cách ly để điều tra.
- Ghi log AWS Step Functions ghi lại mọi chuyển tiếp trạng thái, đầu vào, đầu ra và sự kiện lỗi để có khả năng tái dựng thực thi đầy đủ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hai mẫu điều phối nằm trong phạm vi ở đây. Các state machine AWS Step Functions xử lý các luồng công việc xác định nơi đường thực thi được định nghĩa trong JSON và bộ điều phối thực thi việc tuần tự hóa. [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/) với giao thức A2A xử lý các luồng công việc được ủy thác cho agent nơi một agent điều phối quyết định động các sub-agent nào để gọi. Hầu hết các kiểm soát dưới đây áp dụng cho cả hai, và các khác biệt được nêu ra tại chỗ.

Hãy bắt đầu với IAM. Cấu hình các chính sách cho AWS Step Functions hạn chế các quyền hạn bắt đầu, dừng và chỉnh sửa luồng công việc tới các principal và state machine cụ thể, dùng các chính sách dựa trên tài nguyên trên các định nghĩa state machine để giúp ngăn chỉnh sửa trái phép, và hiện thực các Điều kiện IAM hạn chế việc thực thi tới các lược đồ đầu vào được phê duyệt. Hãy quản lý các định nghĩa state machine như hạ tầng dưới dạng mã (infrastructure as code) qua AWS CloudFormation hoặc AWS CDK, điều giúp ngăn các chỉnh sửa phi chính thức và cung cấp lịch sử thay đổi có quản lý phiên bản.

Kiểm định đầu vào thuộc về bên trong định nghĩa state machine, không phải bên ngoài nó. Với việc lọc JSONPath dựng sẵn của Step Functions và các hàm kiểm định AWS Lambda, bạn có thể kiểm định rằng các đầu vào luồng công việc tuân theo các lược đồ mong đợi trước khi truyền chúng tới các tác vụ agent, từ chối các đầu vào lệch khỏi các mẫu mong đợi. Xử lý lỗi của Step Functions bắt và ghi log các thất bại kiểm định mà không làm lộ chi tiết lỗi cho các bên gọi.

Các cầu dao ngắt dùng logic xử lý lỗi và thử lại của Step Functions. Hãy đặt các giới hạn thử lại thận trọng với backoff hàm mũ (exponential backoff) cho các thất bại tác vụ agent, và hiện thực các trạng thái catch định tuyến các lần thực thi thất bại tới một đường cách ly thay vì thử lại vô thời hạn. Amazon EventBridge phát ra các sự kiện cầu dao ngắt khi các ngưỡng thất bại bị vượt qua, kích hoạt các cảnh báo và khắc phục tự động. Với các luồng công việc đa agent dùng giao thức A2A trên AgentCore Runtime, vòng đời yêu cầu có cấu trúc (khám phá agent card, ủy thác tác vụ, thu thập kết quả) cung cấp các điểm tự nhiên để kiểm định đầu vào, kiểm tra ủy quyền và áp dụng logic cầu dao ngắt trước khi tiếp tục.

Ghi log thực thi làm cho việc điều phối có thể kiểm toán. Hãy bật ghi log thực thi Step Functions tới Amazon CloudWatch Logs ở cấp ALL để thu mọi chuyển tiếp trạng thái, dữ liệu đầu vào/đầu ra và các sự kiện lỗi. Cấu hình các chính sách lưu giữ log căn chỉnh với các yêu cầu tuân thủ và tạo các truy vấn Amazon CloudWatch Logs Insights cho các kịch bản điều tra phổ biến như nhận diện các luồng công việc đã đi các đường thực thi bất ngờ hoặc kích hoạt các cầu dao ngắt.

### Các bước triển khai

- **Giới hạn IAM của Step Functions tới các state machine cụ thể:** Cấu hình các chính sách IAM với truy cập đặc quyền tối thiểu được giới hạn phạm vi tới các state machine cụ thể và các thao tác thực thi.
- **Quản lý các state machine như IaC:** Dùng AWS CloudFormation hoặc AWS CDK cho các định nghĩa state machine để giúp ngăn các chỉnh sửa trái phép và giữ lịch sử phiên bản.
- **Kiểm định các đầu vào bên trong các state machine:** Hiện thực kiểm định đầu vào trong các định nghĩa state machine dùng lọc JSONPath và các hàm kiểm định AWS Lambda, từ chối các đầu vào lệch khỏi các lược đồ mong đợi.
- **Cấu hình các cầu dao ngắt với các trạng thái catch:** Đặt các giới hạn thử lại thận trọng và hiện thực các trạng thái catch định tuyến các thất bại tới các đường cách ly thay vì thử lại vô thời hạn.
- **Ghi log mọi lần thực thi ở cấp ALL:** Bật ghi log thực thi Step Functions tới Amazon CloudWatch Logs ở cấp ALL với các chính sách lưu giữ căn chỉnh với các yêu cầu tuân thủ.
- **Cảnh báo về các sự kiện cầu dao ngắt:** Tạo các cảnh báo Amazon CloudWatch cho các lần kích hoạt cầu dao ngắt và các quy tắc Amazon EventBridge để định tuyến các sự kiện bảo mật luồng công việc tới đường ống giám sát.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](../4-agentsec04/agentsec04-bp02.md)
- [AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent](agentsec06-bp01.md)
- [AGENTSEC06-BP03 Thiết lập các ranh giới tin cậy giữa các agent](agentsec06-bp03.md)
- [AGENTREL07-BP01 Thiết kế các luồng công việc theo từng giai đoạn với phục hồi tăng dần](../../3-reliability/7-agentrel07/agentrel07-bp01.md)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các thất bại thực thi của agent](../../3-reliability/7-agentrel07/agentrel07-bp02.md)

**Tài liệu liên quan:**

- [AWS Step Functions security documentation](https://docs.aws.amazon.com/step-functions/latest/dg/security.html)
- [Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [Using the circuit breaker pattern with Step Functions and DynamoDB](https://aws.amazon.com/blogs/compute/using-the-circuit-breaker-pattern-with-aws-step-functions-and-amazon-dynamodb/)
- [AWS Prescriptive Guidance: Circuit breaker pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html)
- [Introducing agent-to-agent protocol support in Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
