# AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)

Các tích hợp điểm-tới-điểm giữa mỗi agent và mỗi Tools tạo ra một gánh nặng bảo trì tăng theo số lượng tích hợp. Các giao thức chuẩn hóa như MCP và A2A thay thế điều này bằng một hợp đồng dùng chung, mặc định hướng tới khả năng liên vận hành thay vì các Tools được đóng riêng cho từng tích hợp cụ thể.

**Kết quả mong muốn:**

- Các agent tích hợp với Tools qua các giao thức chuẩn hóa (MCP cho lời gọi Tools, A2A cho agent-tới-agent) hỗ trợ khả năng liên vận hành, hành vi nhất quán, và tính di động qua các nhà cung cấp.
- Các lời gọi Tools chạy với các mẫu an toàn: truy cập đặc quyền tối thiểu, xử lý lỗi nhất quán, và log kiểm toán đầy đủ.
- Các agent gọi Tools tin cậy qua các điều kiện mạng và tình trạng sẵn sàng của Tools khác nhau, với các cơ chế dự phòng duy trì tính liên tục dịch vụ.
- Xử lý lỗi tuân theo một phân loại (taxonomy) chuẩn hóa để mọi agent phản ứng với các lỗi nhất thời, vĩnh viễn, và ủy quyền theo cùng một cách.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây dựng các tích hợp điểm-tới-điểm tùy chỉnh cho mỗi cặp agent-Tools thay vì áp dụng các giao thức chuẩn, tạo ra gánh nặng bảo trì tăng theo quy mô.
- Triển khai các lời gọi Tools mà không có xử lý lỗi chuẩn hóa, nên mỗi agent xử lý lỗi khác nhau và không nhất quán.
- Bỏ qua xác thực và ghi log kiểm toán cho các lời gọi Tools, khiến không thể truy vết agent nào đã gọi Tools nào hay liệu nó có được ủy quyền hay không.
- Xem đánh phiên bản giao thức như một suy nghĩ sau cùng, nên một lần nâng cấp Tools âm thầm làm hỏng các agent phụ thuộc vào phiên bản trước.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tích hợp Tools chuẩn hóa với truy cập đặc quyền tối thiểu áp đặt các ranh giới vận hành ở tầng gọi, không chỉ ở logic nội bộ của agent.
- Ghi log kiểm toán mọi lời gọi Tools tạo ra hồ sơ bằng chứng cần thiết cho các buổi rà soát tuân thủ và bảo mật.
- Các mẫu xử lý lỗi dùng chung nghĩa là người vận hành gỡ lỗi Tools theo cùng một cách qua mọi agent.
- Tích hợp dựa trên giao thức cho phép các nhà cung cấp Tools thay đổi backend mà không làm hỏng các agent tiêu thụ, và ngược lại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) là tầng tích hợp chính cho truy cập Tools tương thích MCP. Nó cung cấp xác thực, ủy quyền, và khám phá Tools được quản lý thông qua một giao diện chuẩn hóa, để các agent không phải tự cài đặt lại từng phần này. Đối với giao tiếp agent-tới-agent, [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) hỗ trợ các endpoint giao thức A2A với khám phá agent qua Agent Cards, quản lý vòng đời tác vụ, và trao đổi thông điệp có cấu trúc. Hai thứ kết hợp lại bao phủ hầu hết các bề mặt tích hợp mà không cần hạ tầng tùy chỉnh.

Việc áp đặt đặc quyền tối thiểu cần diễn ra ở tầng giao thức, không phải ở tầng ứng dụng. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) áp dụng các chính sách Cedar để giới hạn phạm vi quyền Tools của mỗi agent tại ranh giới Gateway. Các agent chỉ có thể gọi các Tools mà chính sách của chúng cho phép, bất kể mã nội bộ của chúng cố làm gì. Kiểm tra chạy tại thời điểm có lưu lượng, không phải tại thời điểm rà soát. Hãy thiết lập ghi log kiểm toán qua [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), vốn tạo ra các hồ sơ tuân thủ mà không cần trang bị đo lường tùy chỉnh.

Xử lý lỗi hưởng lợi từ một phân loại các lỗi nhất thời (thử lại với lùi lũy thừa và jitter), lỗi vĩnh viễn (thất bại nhã nhặn), và lỗi ủy quyền (leo thang tới rà soát của con người). Mỗi lớp đòi hỏi một hành vi agent khác nhau, và việc gộp lẫn chúng, như thử lại một lỗi vĩnh viễn hoặc leo thang một timeout nhất thời, tạo ra phản ứng sai ở quy mô lớn. Đối với các Tools quan trọng, hãy triển khai các chuỗi dự phòng thử các phương án thay thế khi Tools chính không khả dụng. Hãy giám sát tỷ lệ lỗi và độ trễ theo từng Tools qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và cấu hình các cảnh báo để phát hiện suy giảm trước khi nó trở thành sự cố.

Đánh phiên bản giao thức thông qua thương lượng năng lực (capability negotiation) bảo toàn tương thích ngược khi các giao thức tiến hóa. Các trường hợp không khớp phiên bản nên khiến bên cũ vận hành ở năng lực đã biết của nó thay vì thất bại, và cả hai bên nên khai báo các phiên bản được hỗ trợ trong lúc bắt tay (handshake).

### Các bước triển khai

- **Phơi bày Tools qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html):** Công bố các năng lực MCP server với [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) áp đặt các kiểm soát truy cập theo từng agent.
- **Triển khai các endpoint giao thức A2A:** Dùng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cho giao tiếp liên agent chuẩn hóa.
- **Định nghĩa các chiến lược đánh phiên bản giao thức:** Dùng thương lượng năng lực để bên cũ và bên mới liên vận hành ở phiên bản chung được hỗ trợ.
- **Triển khai xử lý lỗi chuẩn hóa:** Áp dụng phân loại nhất thời/vĩnh viễn/ủy quyền và các chuỗi dự phòng cho các Tools quan trọng qua mọi agent.
- **Giám sát sức khỏe theo từng Tools qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html):** Theo dõi tỷ lệ lỗi và độ trễ, và cấu hình các cảnh báo để phát hiện chủ động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools](agentops04-bp01.md)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](agentops04-bp03.md)
- [AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent](../1-agentops01/agentops01-bp01.md)
- [AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả](../../4-performance-efficiency/6-agentperf06/agentperf06-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Open Protocols for Agent Interoperability Part 1: Inter-Agent Communication on MCP](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-1-inter-agent-communication-on-mcp)
- [Open Protocols for Agent Interoperability Part 4: Inter-Agent Communication on A2A](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-4-inter-agent-communication-on-a2a/)
- [Introducing agent-to-agent protocol support in Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [Open Protocols for Agent Interoperability Part 2: Authentication on MCP](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-2-authentication-on-mcp/)
- [Agentic AI frameworks: Protocol-based tools](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/protocol-based-tools-detailed.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Building Scalable, Self-Orchestrating AI Workflows with A2A and MCP (DEV415)](https://www.youtube.com/watch?v=9O9zZ1lQWiI)
- [AWS 2025 - AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [AWS 2025 - Integrating MCP Tools with Strands Agents](https://www.youtube.com/watch?v=bHSbjCZZFjE)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore, Gateway](https://catalog.workshops.aws/agentcore-deep-dive/en-US/30-agentcore-gateway)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
