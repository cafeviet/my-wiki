# AGENTCOST06-BP03 Thiết kế khởi tạo tiết kiệm chi phí thông qua warm pool và caching

Cold start là một chi phí trên mỗi lần gọi đáng kể trong hạ tầng agent, nơi việc nạp model, đăng ký công cụ, và hydrat hóa bộ nhớ chạy ở mọi phiên mới tinh. Bạn có thể giảm các chi phí trên mỗi lần gọi đó thông qua các hệ thống tệp bền vững, session affinity, và nạp ngữ cảnh lười để tái sử dụng kết quả trong khi vẫn scale về không cho các agent hiếm khi được gọi.

**Kết quả mong muốn:**

- Bạn khấu hao các chi phí khởi tạo qua nhiều lần gọi bằng cách cache các tạo tác trên một hệ thống tệp bền vững.
- Bạn có các agent được gọi thường xuyên tái sử dụng các phiên ấm và các agent ít gọi scale về không mà không có phí rảnh.
- Bạn hoãn việc truy xuất ngữ cảnh không thiết yếu tới theo yêu cầu, giữ khởi tạo dưới một ngân sách thời gian cố định.
- Bạn theo dõi tỷ lệ cold start và chi phí khởi tạo theo từng loại agent.

**Các phản mẫu thường gặp (anti-patterns):**

- Thực hiện khởi tạo tốn kém ở mọi lần gọi thay vì cache các tạo tác xuyên các phiên.
- Cho phép các agent được gọi thường xuyên liên tục chịu các cold start mà không có lưu bền phiên hoặc các mẫu warm pool.
- Nạp tất cả ngữ cảnh có khả năng liên quan lúc khởi động thay vì nạp lười theo yêu cầu, làm tăng độ trễ khởi tạo với dữ liệu có thể không bao giờ được dùng.
- Vận hành các agent mà không có khả năng nhìn thấy cold start, bỏ lỡ các cơ hội áp dụng các mẫu warm pool hoặc tối ưu khởi tạo cho các agent có tác động cao. Cold start của agent bao gồm nạp model, đăng ký công cụ, và hydrat hóa bộ nhớ, không chỉ khởi động container.

**Lợi ích khi áp dụng thực hành tốt này:**

- Caching hệ thống tệp bền vững khấu hao các chi phí khởi tạo qua nhiều lần gọi, tránh chi phí lặp lại.
- Quản lý vòng đời phiên duy trì các phiên ấm cho các agent thường xuyên trong khi scale về không cho các agent ít gọi mà không có phí rảnh.
- Nạp ngữ cảnh lười giảm thời gian khởi tạo bằng cách hoãn việc truy xuất không thiết yếu cho đến khi suy luận cần.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) triển khai hành vi warm pool thông qua vòng đời phiên của nó. Các phiên di chuyển qua các trạng thái Active, Idle và Terminated. Active xử lý xử lý, Idle duy trì sự sẵn sàng phiên sau timeout không hoạt động mà không có phí tính toán, và Terminated kết thúc phiên khi hết hạn hoặc đạt maximum lifetime. Các agent được gọi thường xuyên giữ các phiên ấm qua cửa sổ idle trong khi các agent ít gọi scale về không, nên bạn không trả phí công suất rảnh cho các agent không được gọi. Tinh chỉnh idle timeout dựa trên tần suất gọi để cân bằng khả năng đáp ứng với chi phí phiên.

Hệ thống tệp bền vững làm cho caching khởi tạo đáng để triển khai. Hệ thống tệp sống sót qua các chu kỳ dừng và tiếp tục phiên tới 14 ngày, nên các tạo tác khởi tạo tốn kém (trạng thái model, cấu hình công cụ, và dữ liệu tham chiếu được nạp trước) có thể được tính một lần ở lần gọi đầu và tái sử dụng qua nhiều phiên sau. Việc lưu giữ 14 ngày định hình chiến lược caching của bạn: lập kế hoạch làm mới tạo tác và vô hiệu hóa cache vừa với cửa sổ, để dữ liệu đã cache không bao giờ hết hạn âm thầm và không bao giờ lỗi thời vượt quá điểm làm mới.

Session affinity tối ưu chi phí bằng cách giữ cùng runtimeSessionId qua các lần gọi liên quan để các model đã nạp và các cấu hình công cụ đã cache được tái sử dụng. Triển khai theo dõi phiên trong tầng điều phối để các luồng công việc người dùng ánh xạ tới các định danh phiên nhất quán, và giám sát tỷ lệ tái sử dụng phiên để xác nhận định tuyến đang tránh chi phí khởi tạo không cần thiết. Nếu tỷ lệ cold start tăng trên 10%, hãy điều tra cấu hình sai của affinity hoặc idle timeout trước khi tối ưu chính logic khởi tạo.

Hãy cân nhắc *nạp ngữ cảnh lười (lazy context loading)*, nơi dữ liệu được lấy hoặc phân tích chỉ khi nó được yêu cầu. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) hỗ trợ chỉ truy xuất ngữ cảnh khởi động tối thiểu (tác vụ hiện tại của người dùng và lịch sử phiên tức thời), hoãn việc truy xuất bộ nhớ dài hạn và cơ sở tri thức cho đến khi agent thực sự cần dữ liệu. Điều này giữ thời gian khởi tạo dưới một mục tiêu 2 giây bao gồm nạp model và đăng ký công cụ. Giám sát tỷ lệ cold start và chi phí khởi tạo qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), xây dựng các dashboard Amazon CloudWatch cho thời lượng khởi tạo và tái sử dụng phiên theo từng loại agent, và xem xét cấu hình idle timeout hàng tháng dựa trên các mẫu gọi quan sát được.

### Các bước triển khai

- **Cache các tạo tác khởi tạo trên lưu trữ bền vững:** Cấu hình [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với hệ thống tệp bền vững (sống sót tới 14 ngày xuyên các chu kỳ phiên) và triển khai logic khởi tạo kiểm tra các tạo tác đã cache trước khi thực hiện các thao tác tốn kém.
- **Áp dụng session affinity:** Duy trì các giá trị runtimeSessionId nhất quán qua các lần gọi liên quan để trạng thái phiên ấm (các model đã nạp, các cấu hình công cụ đã cache) được tái sử dụng.
- **Hoãn ngữ cảnh không thiết yếu:** Cấu hình [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho nạp lười ngữ cảnh khởi động, hoãn việc truy xuất thêm tới theo yêu cầu trong lúc suy luận, với một mục tiêu thời gian khởi tạo dưới 2 giây.
- **Giám sát tỷ lệ cold start theo từng loại agent:** Đo lường các agent bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để theo dõi độ trễ tạo phiên, thời lượng khởi tạo (nạp model và đăng ký công cụ), và tỷ lệ cold start, với cảnh báo cho các tỷ lệ vượt 10%.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md)
- [AGENTCOST06-BP01 Triển khai khám phá và registry nhẹ cho cộng tác tiết kiệm chi phí](agentcost06-bp01.md)
- [AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tạo tác hiệu quả](agentcost06-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)
- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime advanced concepts](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime/03-advanced-concepts)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
