# AGENTREL01-BP04 Chuẩn hóa các giao thức giao tiếp

Định dạng thông điệp tùy biến giữa từng cặp tác nhân biến mỗi tích hợp mới thành một dự án kỹ thuật riêng lẻ. Các lược đồ được chuẩn hóa, các điểm cuối có phiên bản và một định dạng lỗi chuẩn tắc (canonical) cho phép các tác nhân kết hợp thành luồng công việc mà không cần lớp phiên dịch tại mỗi ranh giới.

**Kết quả mong muốn:**

- Bạn có một lược đồ thông điệp chuẩn tắc, định dạng lỗi và chính sách thử lại mà mọi tác nhân đều tuân theo.
- Bạn đánh phiên bản các điểm cuối và duy trì tương thích ngược để các tích hợp hiện có vẫn hoạt động khi giao thức tiến hóa.
- Bạn thực thi việc tuân thủ giao thức thông qua các bài kiểm thử hợp đồng tự động trong đường ống CI/CD.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây dựng các mẫu giao tiếp tùy tiện với định dạng thông điệp tùy biến cho từng tương tác, sinh ra các lớp phiên dịch giữa từng cặp tác nhân.
- Tiến hóa các điểm cuối mà không đánh phiên bản hay giữ tương thích ngược, làm hỏng các tích hợp hiện có mỗi lần thay đổi.
- Cho phép mỗi tác nhân tự đặt timeout, logic thử lại và định dạng phản hồi lỗi riêng, sinh ra hành vi lỗi khó lường trên toàn đội.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các lược đồ và hợp đồng nhất quán giảm độ phức tạp tích hợp và loại bỏ mã phiên dịch điểm-tới-điểm.
- Việc điều phối đa tác nhân có thể dự đoán trở nên khả thi vì các tác nhân kết hợp thành luồng công việc mà không cần phụ thuộc mã cứng.
- Có thể đưa vào hoặc thay thế các tác nhân mới mà không cần viết lại các thành phần phụ thuộc.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cung cấp một lớp được quản lý cho việc khám phá tác nhân và gọi công cụ với xác thực và ủy quyền tích hợp sẵn. Bên dưới nó, giao thức Agent-to-Agent (A2A) chuẩn hóa giao tiếp trực tiếp tác nhân-tới-tác nhân và **Model Context Protocol (MCP)** chuẩn hóa tương tác tác nhân-tới-công cụ. Chọn các giao thức này thay vì tự phát minh giao thức riêng mang lại lợi ích mỗi khi một tác nhân mới tham gia mạng lưới.

Nếu mỗi tác nhân phát minh mã lỗi và hướng dẫn thử lại riêng, bên gọi không thể viết một đường xử lý lỗi duy nhất. Một định dạng chuẩn tắc với ba trường (mã lỗi, ID tương quan và hướng dẫn thử lại) bao phủ gần như mọi trường hợp và cho phép bên gọi áp dụng cùng logic bất kể tác nhân nào trả về lỗi. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thực thi ai được gọi cái gì tại ranh giới gateway thông qua các chính sách Cedar, nhờ đó hợp đồng được thực thi trước khi yêu cầu tới tác nhân, thay vì chỉ dựa vào tài liệu.

Đánh phiên bản quan trọng vì giao thức tiến hóa. Đánh phiên bản mọi target của AgentCore Gateway để bên gọi có thể di trú theo nhịp riêng của mình. Đăng ký lược đồ thông điệp cho mỗi loại tương tác của tác nhân để việc tuần tự hóa (serialization) nhất quán qua các ranh giới. Đấu nối các bài kiểm thử hợp đồng vào CI/CD để các thoái lui giao thức bị bắt trước khi triển khai thay vì trong một sự cố.

### Các bước triển khai

- **Định nghĩa phân loại giao tiếp chuẩn tắc:** Ghi lại các lược đồ thông điệp chuẩn, định dạng phản hồi lỗi và chính sách thử lại mà mọi tác nhân đều tuân theo.
- **Cấu hình AgentCore Gateway với các giao thức A2A và MCP:** Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) làm bề mặt được quản lý cho giao tiếp tác nhân-tới-tác nhân và tác nhân-tới-công cụ đã chuẩn hóa.
- **Thực thi kiểm soát truy cập với AgentCore Policy:** Áp dụng các chính sách Cedar qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để gateway từ chối các lời gọi trái phép ngay tại ranh giới.
- **Triển khai xử lý lỗi chuẩn tắc trên mọi giao diện tác nhân:** Truyền một ID tương quan qua mỗi lời gọi và trả về lỗi theo định dạng chuẩn tắc để bên gọi có thể xử lý chúng đồng nhất.
- **Chạy các bài kiểm thử hợp đồng tự động trong CI/CD:** Chặn triển khai khi phát hiện thoái lui giao thức để các chuẩn giao thức vẫn được thực thi khi đội tác nhân lớn lên.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ](agentrel01-bp01.md)
- [AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model](agentrel01-bp03.md)
- [AGENTREL01-BP05 Triển khai cấp phát thích ứng](agentrel01-bp05.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Transform your MCP architecture: Unite MCP servers through AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [Strands Agents A2A Protocol](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agent-to-agent/)
- [Strands Agents MCP Tools](https://strandsagents.com/docs/user-guide/concepts/tools/mcp-tools/)

**Video liên quan:**

- [Integrating MCP Tools with Strands Agents](https://www.youtube.com/watch?v=bHSbjCZZFjE)
- [Breaking multi-agent silos: A2A + MCP in action with Strands Agents](https://www.youtube.com/watch?v=TjTgHA5DjDM)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
