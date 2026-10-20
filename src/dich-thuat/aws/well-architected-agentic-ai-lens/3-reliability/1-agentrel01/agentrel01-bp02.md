# AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi

Các kiến trúc tác nhân đơn khối (monolithic) buộc mọi lỗi phải trở thành lỗi toàn hệ thống. Tách tính toán, bộ nhớ, suy luận và điều phối thành các lớp có thể mở rộng độc lập với ranh giới fail-fast giữ cho phạm vi ảnh hưởng nhỏ. Các đội tiếp tục phục vụ yêu cầu ở năng lực giảm bớt thay vì trở nên không khả dụng.

**Kết quả mong muốn:**

- Ngăn xếp tác nhân của bạn được tách thành các lớp riêng biệt (tính toán, bộ nhớ, suy luận, điều phối và tích hợp công cụ) với các hợp đồng API được tài liệu hóa tại mỗi ranh giới.
- Bạn có hành vi fail-fast trên các lời gọi liên lớp, với các chế độ dự phòng được định nghĩa cho mỗi trạng thái suy giảm.
- Bạn có thể bật/tắt các năng lực không thiết yếu lúc chạy mà không cần triển khai lại.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các tác nhân đơn khối, nơi một lỗi ở bất kỳ thành phần nào buộc phải khởi động lại toàn bộ cho các sự cố lẽ ra nên được cô lập.
- Vận hành mà không có cơ chế ngắt tự động, cho phép độ trễ hoặc tỷ lệ lỗi ở một thành phần lan qua mọi lời gọi phụ thuộc.
- Coi mọi năng lực đều thiết yếu như nhau, bỏ lỡ cơ hội giữ chức năng cốt lõi khả dụng khi các thành phần không thiết yếu bị lỗi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các đội có thể phát triển, kiểm thử và triển khai từng lớp một cách độc lập mà không bị chặn bởi phần còn lại của ngăn xếp.
- Cô lập lỗi thu hẹp việc xử lý sự cố về đúng lớp thực sự lỗi thay vì cả hệ thống.
- Suy giảm nhẹ nhàng (graceful degradation) giữ cho tác nhân vẫn đáp ứng ngay cả khi từng lớp không khả dụng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

**Runtime** của AgentCore tổ chức các năng lực thành các lớp riêng biệt (Runtime, Memory, Gateway và Identity), mỗi lớp có thể định địa chỉ một cách độc lập. Hãy thiết kế các tác nhân của bạn để coi chúng như các miền lỗi tách biệt. Nếu Memory trở nên không khả dụng, logic định tuyến (Gateway) và xác thực (Identity) của tác nhân vẫn nên tiếp tục hoạt động. Triển khai kiểm tra sức khỏe theo từng lớp và cấu hình chính sách thời gian chờ (timeout) và thử lại độc lập cho mỗi lớp, thay vì coi AgentCore như một phụ thuộc đơn khối.

Khi tỷ lệ lỗi của một lớp phía dưới tăng lên, bên gọi nên ngừng chờ timeout và kích hoạt một dự phòng. Ví dụ gồm dùng ngữ cảnh chỉ theo phiên thay vì bộ nhớ dài hạn, dùng một mô hình Amazon Bedrock thay thế thay vì mô hình chính, hoặc dùng một câu trả lời được lưu trong cache thay vì truy xuất mới. Không có fail-fast, mỗi lời gọi suy giảm sẽ tiêu tốn ngân sách luồng (thread budget) và lan độ trễ trở lại người dùng. [Hướng dẫn mẫu fail-fast của AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html) bao quát các cơ chế này.

Việc bật/tắt năng lực lúc chạy giữ cho phạm vi ảnh hưởng nhỏ trong một sự cố. Nếu một công cụ chập chờn, hãy tắt công cụ đó và giữ phần còn lại của tác nhân hoạt động thay vì hạ toàn bộ tác nhân xuống. Công bố trạng thái sức khỏe có cấu trúc theo từng lớp qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để các thành phần phía dưới tự động thích ứng với trạng thái bật/tắt. Bản đồ dịch vụ (service maps) cung cấp cho người vận hành góc nhìn cần thiết để tương quan sức khỏe từng lớp với các triệu chứng mà người dùng nhìn thấy.

### Các bước triển khai

- **Phân rã kiến trúc thành các lớp với hợp đồng được tài liệu hóa:** Tách tác nhân thành các lớp riêng biệt cho tính toán, bộ nhớ, nhận thức, điều phối và tích hợp công cụ. Công bố hợp đồng API tại mọi ranh giới.
- **Triển khai mỗi lớp độc lập trên AgentCore Runtime:** Chạy mỗi lớp trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) không dùng chung tài nguyên thực thi giữa các lớp.
- **Triển khai logic fail-fast cho mỗi lời gọi liên lớp:** Với mỗi ranh giới lời gọi, định nghĩa ngưỡng tỷ lệ lỗi kích hoạt cơ chế ngắt và hành vi dự phòng thay thế.
- **Công bố sức khỏe lớp có cấu trúc qua AgentCore Observability:** Phát các tín hiệu sức khỏe theo từng lớp qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để các thành phần phía dưới có thể thích ứng và người vận hành có thể truy vết suy giảm về nguồn gốc.
- **Đấu nối bật/tắt năng lực lúc chạy:** Xây dựng một **control plane** vô hiệu hóa các năng lực không thiết yếu mà không cần triển khai lại, để người vận hành có thể kiểm soát sự cố khi chúng diễn ra.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ](agentrel01-bp01.md)
- [AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model](agentrel01-bp03.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](../8-agentrel08/agentrel08-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Operationalizing agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [AWS fail-fast pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Architecting scalable and secure agentic AI with AgentCore (AIM431)](https://www.youtube.com/watch?v=wqmeZOT6mmc)
- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
