# AGENTCOST01-BP04 Thiết kế các cấp bậc agent và mẫu ủy quyền giảm chi phí phối hợp

Chi phí supervisor trong các cấp bậc agent tăng theo độ dài dòng của các mô tả năng lực và tần suất kiểm tra (check-in). Các manifest gọn và các worker tự chủ giữ cho chi phí phối hợp tỷ lệ với độ phức tạp của luồng công việc chứ không theo số bước.

**Kết quả mong muốn:**

- Các cấp bậc agent của bạn dùng cấu trúc điều phối nông nhất có khả năng quản lý luồng công việc.
- Bạn có các supervisor agent vận hành trên các manifest năng lực đã nén nhằm tối thiểu token đầu vào cho mỗi quyết định định tuyến.
- Các worker agent của bạn hoàn thành các tác vụ con nhiều bước một cách tự chủ, chỉ leo thang lên supervisor để giao tác vụ và xác thực kết quả.
- Bạn theo dõi chi phí orchestrator như một hạng mục riêng với một tỷ lệ chi phí supervisor-trên-worker mục tiêu.

**Các phản mẫu thường gặp (anti-patterns):**

- Đưa các mô tả năng lực dài dòng bằng ngôn ngữ tự nhiên của mọi worker vào các prompt định tuyến, làm phồng chi phí token vốn sau đó mở rộng tuyến tính theo số lượng worker.
- Yêu cầu supervisor kiểm tra sau mỗi bước con, làm nhân chi phí phối hợp trong khi worker lẽ ra có thể hoàn thành công việc nhiều bước một cách tự chủ.
- Chỉ theo dõi chi phí luồng công việc tổng hợp mà không phân rã chi tiêu orchestrator so với worker, nên chi phí phối hợp không tương xứng bị ẩn trong tổng số.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các manifest năng lực đã nén giảm chi phí token đầu vào của supervisor cho mỗi quyết định định tuyến.
- Các worker tự chủ loại bỏ các lượt đi-về của supervisor cho các quyết định trung gian.
- Việc quy gán chi phí theo tầng làm nổi lên các cơ hội tối ưu nơi chi phí phối hợp vượt quá giá trị thực thi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Chi phí supervisor có hai động lực chính: mỗi quyết định định tuyến đắt bao nhiêu và định tuyến diễn ra bao nhiêu lần.

Cái thứ nhất được điều khiển bởi kích thước manifest. Các supervisor mô tả worker bằng những đoạn văn ngôn ngữ tự nhiên phải trả tiền cho những đoạn văn đó ở mỗi lần gọi định tuyến, và chi phí đó mở rộng tuyến tính theo số lượng worker. Các manifest năng lực ngắn, có cấu trúc (mô tả, lược đồ đầu vào, lược đồ đầu ra, dưới 200 token mỗi cái) cắt giảm chi phí này mà không hy sinh chất lượng định tuyến, vì supervisor không cần văn xuôi để chọn giữa các worker có các lược đồ khác biệt.

Cái thứ hai được điều khiển bởi việc chuyển tiếp ngữ cảnh (context relay). Khi ngữ cảnh chảy từ cha đến worker thông qua supervisor, mọi byte của ngữ cảnh đó được truyền hai lần: một lần vào supervisor, và một lần vào worker như một phần của phản hồi định tuyến. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) loại bỏ sự nhân đôi đó bằng cách cho các worker đọc ngữ cảnh dùng chung trực tiếp từ bộ nhớ bằng actor ID và session ID của phiên, để supervisor chỉ định tuyến chứ không chuyển tiếp. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) giảm nó thêm nữa bằng cách hỗ trợ khám phá công cụ lúc chạy qua Model Context Protocol, nên prompt của supervisor không cần liệt kê mọi công cụ mà các worker có thể gọi. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) kiểm soát công cụ nào mỗi worker được phép gọi một cách tự chủ, khiến việc chuyển các quyết định xuống dưới trở nên an toàn mà không mất kiểm soát quản trị.

Các worker được thiết kế với đủ quyền tự chủ về công cụ và tiêu chí thành công rõ ràng có thể hoàn thành các tác vụ con nhiều bước, trả về một kết quả có cấu trúc duy nhất kèm một điểm độ tin cậy. Supervisor sau đó ra một quyết định chấp nhận-hoặc-từ-chối hiệu quả thay vì suy luận lại từ đầu ở mỗi bước trung gian. Với các luồng công việc có các mẫu phân rã lặp lại, cách tiếp cận plan-then-execute nén thêm nữa, trong đó một lần gọi supervisor tạo ra toàn bộ kế hoạch tác vụ, rồi các worker thực thi kế hoạch mà không cần giám sát thêm.

Theo dõi tỷ lệ chi phí supervisor-trên-worker. Đặt một mục tiêu (ví dụ, token supervisor không quá 15% token worker) và cảnh báo khi bị vượt. Một vi phạm thường báo hiệu rằng cần nén manifest, tăng quyền tự chủ của worker, hoặc áp dụng plan-then-execute.

### Các bước triển khai

- **Nén các mô tả năng lực của worker:** Thay các mô tả năng lực bằng ngôn ngữ tự nhiên bằng các manifest có cấu trúc (mô tả, lược đồ đầu vào, lược đồ đầu ra) dưới 200 token mỗi cái, và dùng khám phá công cụ lúc chạy của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để tránh liệt kê công cụ trong prompt của supervisor.
- **Thiết kế lại worker để hoàn thành nhiều bước một cách tự chủ:** Cho mỗi worker đủ quyền tự chủ về công cụ và tiêu chí thành công rõ ràng để hoàn thành tác vụ con từ đầu đến cuối, và yêu cầu worker phát ra một điểm độ tin cậy trong mọi phản hồi để supervisor có thể ra quyết định chấp nhận-hoặc-từ-chối mà không cần suy luận lại.
- **Áp dụng policy và bộ nhớ dùng chung để truy cập ngữ cảnh trực tiếp:** Cấu hình [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) qua Gateway để thực thi ranh giới truy cập công cụ của worker, và cấp phát [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) để các worker đọc ngữ cảnh dùng chung trực tiếp thay vì nhận nó được chuyển tiếp qua supervisor.
- **Theo dõi tỷ lệ chi phí supervisor-trên-worker:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để quy gán token theo tầng, xây dựng các dashboard Amazon CloudWatch hiển thị tỷ lệ supervisor-trên-worker cho mỗi luồng công việc, và cảnh báo khi tỷ lệ vượt quá mục tiêu 15%.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](agentcost01-bp02.md)
- [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](agentcost01-bp03.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](../5-agentcost05/agentcost05-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Multi-agent tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime/03-advanced-concepts)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
