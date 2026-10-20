# AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả

Các giao thức chuẩn hóa như Model Context Protocol (**MCP**) và **A2A** (tác-nhân-tới-tác-nhân) cho các tác nhân một cách nhất quán để giao tiếp với **Tools** và với nhau, giảm chi phí mỗi-tương-tác và cho phép khả năng tương tác. Các giao thức khác nhau có các hồ sơ hiệu năng khác nhau, thiết lập kết nối, tuần tự hóa, streaming, ghép kênh (multiplexing), điều này khiến lựa chọn giao thức là một quyết định hiệu năng có ý nghĩa cho giao tiếp tác nhân tần-suất-cao.

**Kết quả mong muốn:**

- Bạn dùng MCP cho tích hợp Tools, A2A cho điều phối tác-nhân-tới-tác-nhân, và các giao thức streaming cho các tương tác tác-nhân-người-dùng thời-gian-thực.
- Bạn có chi phí giao thức được giảm thiểu qua tái dùng kết nối và tuần tự hóa hiệu quả.
- Bạn có hướng dẫn lựa chọn giao thức được ghi tài liệu cho tổ chức.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng các API HTTP hoặc REST với tuần tự hóa JSON cho mọi giao tiếp tác nhân bất kể mẫu tương tác, trả chi phí thiết lập kết nối và tuần tự hóa dài dòng cho các giao tiếp nội bộ tần-suất-cao.
- Triển khai các giao thức giao tiếp tùy chỉnh thay vì áp dụng các chuẩn như MCP và A2A, tạo ra gánh nặng bảo trì và chặn khả năng tương tác với hệ sinh thái tác nhân rộng hơn.
- Thiết lập kết nối mới cho mỗi tương tác tác nhân thay vì gộp và tái dùng chúng, thêm latency bắt-tay không cần thiết.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản lý kết nối phù-hợp-giao-thức giảm chi phí mỗi-tương-tác.
- Các giao thức chuẩn mở ra khả năng tương tác với hệ sinh thái tác nhân rộng hơn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Áp dụng MCP làm giao thức chuẩn cho giao tiếp tác-nhân-tới-Tool. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) phơi bày các Tools dưới dạng các endpoint tương thích MCP mà tác nhân khám phá và gọi qua một giao diện nhất quán. Cho giao tiếp tác-nhân-tới-tác-nhân, giao thức A2A được AgentCore Runtime hỗ trợ cung cấp điều phối liên-tác-nhân có cấu trúc với khám phá agent card, ủy quyền tác vụ, và thu thập kết quả. Các framework như Strands Agents và LangGraph cung cấp hỗ trợ MCP và A2A.

Cho các tương tác tác-nhân-người-dùng thời-gian-thực cần streaming, các kết nối WebSocket qua [Amazon API Gateway](https://aws.amazon.com/api-gateway/) giữ một kênh bền mở thay vì thiết lập lại kết nối mỗi lượt. Gộp kết nối thuộc về mọi đường giao thức, và nén cấp-giao-thức hoàn vốn khi payload vượt vài kilobyte.

Chi phí xác thực là một phần của hồ sơ hiệu năng giao thức. Trong các luồng công việc đa tác nhân phức tạp, xác thực Token, cấp phát chứng chỉ, và đánh giá chính sách tích lũy thành một bên đóng góp latency đo được. AgentCore Identity cung cấp xác thực tác nhân với caching Token, và các vai trò AWS IAM cho xác thực dịch-vụ-tới-dịch-vụ loại việc trao đổi chứng chỉ tường minh khỏi đường tới hạn.

### Các bước triển khai

- **Áp dụng MCP cho giao tiếp tác-nhân-tới-Tool qua AgentCore Gateway:** Phơi bày các Tools dưới dạng các endpoint tương thích MCP qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để các tác nhân khám phá và gọi Tools qua một giao diện nhất quán.
- **Dùng giao thức A2A qua AgentCore Runtime cho điều phối tác-nhân-tới-tác-nhân:** Dùng giao thức A2A được AgentCore Runtime hỗ trợ cho điều phối tác-nhân-tới-tác-nhân, với khám phá agent card, ủy quyền tác vụ, và thu thập kết quả.
- **Triển khai các kết nối WebSocket qua API Gateway cho các tương tác tác-nhân-người-dùng streaming thời-gian-thực:** Dùng các kết nối WebSocket qua [Amazon API Gateway](https://aws.amazon.com/api-gateway/) cho streaming thời-gian-thực để kênh giữ mở thay vì thiết lập lại mỗi lượt.
- **Bật gộp kết nối và nén cấp-giao-thức cho mọi giao tiếp:** Gộp kết nối trên mọi đường giao thức và bật nén khi payload vượt vài kilobyte.
- **Lập ngân sách cho chi phí xác thực và triển khai caching Token qua AgentCore Identity:** Dùng AgentCore Identity với caching Token cho xác thực tác nhân, và dùng các vai trò AWS IAM cho các lệnh gọi dịch-vụ-tới-dịch-vụ để trao đổi chứng chỉ không nằm trên đường tới hạn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF04-BP01 Tối ưu các mẫu xử lý thông điệp bất đồng bộ](agentperf04-bp01.md)
- [AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu](../6-agentperf06/agentperf06-bp01.md)
- [AGENTPERF05-BP02 Triển khai các mô hình cộng tác đa tác nhân được tối ưu](../5-agentperf05/agentperf05-bp02.md)

**Tài liệu liên quan:**

- [Các framework, giao thức, và Tools AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)
- [Blog: Các giao thức mở cho khả năng tương tác tác nhân Phần 1: Giao tiếp liên-tác-nhân trên MCP](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-1-inter-agent-communication-on-mcp)
- [Blog: Các giao thức mở cho khả năng tương tác tác nhân Phần 4: Giao tiếp liên-tác-nhân trên A2A](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-4-inter-agent-communication-on-a2a/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)

**Video liên quan:**

- [AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [Xây dựng các luồng công việc AI tự-điều-phối, có khả năng mở rộng với A2A và MCP (DEV415)](https://www.youtube.com/watch?v=9O9zZ1lQWiI)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
