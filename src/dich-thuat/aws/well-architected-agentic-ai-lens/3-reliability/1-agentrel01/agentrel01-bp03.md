# AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model

Các tác nhân đa mục đích tập trung rủi ro. Một lỗi đơn lẻ ở một chức năng ảnh hưởng tới mọi chức năng khác trong cùng tiến trình. Các tác nhân chuyên biệt đóng gói một năng lực nguyên tử duy nhất, sở hữu trạng thái riêng và giao tiếp qua thông điệp giữ cho ảnh hưởng tương xứng với phạm vi của thành phần đang lỗi.

**Kết quả mong muốn:**

- Bạn có mỗi tác nhân được thu hẹp phạm vi về một chức năng nguyên tử duy nhất với lược đồ đầu vào và đầu ra tường minh.
- Các tác nhân của bạn duy trì trạng thái riêng và trao đổi thông tin qua truyền thông điệp tường minh, không dùng bộ nhớ chung.
- Bạn có thể mở rộng, thay thế hoặc nâng cấp bất kỳ tác nhân nào mà không làm xáo trộn các tác nhân khác.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây dựng các tác nhân đa mục đích kết hợp nhiều chức năng khác nhau trong một thành phần, làm giảm khả năng mở rộng độc lập và mở rộng ảnh hưởng của lỗi.
- Ràng buộc các tác nhân qua trạng thái dùng chung trong bộ nhớ thay vì truyền thông điệp tường minh, nên một sự cố sập ở một tiến trình làm hỏng tiến trình khác.
- Thiết kế các tác nhân như những bộ xử lý đa dụng với năng lực chồng lấn, khiến việc tái lập và khắc phục sự cố khó hơn mức cần thiết.

**Lợi ích khi áp dụng thực hành tốt này:**

- Một lỗi vẫn được cô lập ở đúng tác nhân gặp phải nó, bảo toàn tính toàn vẹn tổng thể của luồng công việc.
- Các tác nhân đơn trách nhiệm dễ kiểm thử theo hướng tất định hơn vì hợp đồng đầu vào–đầu ra nhỏ gọn.
- Mỗi tác nhân mở rộng, triển khai và được thay thế theo lịch riêng, giữ cho phần còn lại của hệ thống ổn định trong quá trình thay đổi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

**Actor model** là một kỷ luật, không phải một tính năng của runtime. Một **runtime** được quản lý có thể cho bạn thực thi được cô lập. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) chạy mỗi tác nhân trong microVM riêng với quyền công cụ dành riêng. Nhưng liệu các tác nhân của bạn có thực sự tuân theo nguyên tắc actor hay không phụ thuộc vào cách bạn thu hẹp phạm vi của system prompt, cách bạn định nghĩa tập công cụ hẹp đến đâu, và các lời gọi liên tác nhân đi qua thông điệp hay trạng thái dùng chung.

Cho mỗi tác nhân một system prompt duy nhất, thu hẹp phạm vi tốt, giới hạn nó vào một miền. Dùng Strands Agents hoặc một khung tác nhân khác, nhưng phép thử là độc lập với khung. Bạn có thể mô tả công việc của tác nhân trong một câu duy nhất mà không dùng chữ "và" không? Nếu không, tác nhân đang gánh hơn một trách nhiệm và nên được tách ra.

Mẫu giao tiếp bám theo hình dạng tương tác. Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để phơi bày các tác nhân như các công cụ MCP có thể khám phá được khi bên gọi coi tác nhân chuyên biệt như một năng lực mà nó gọi khi cần. Dùng [giao thức Agent-to-Agent (A2A)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html) khi các tác nhân cần cộng tác ngang hàng với phản hồi luồng (streaming) hoặc trao đổi nhiều lượt. Giám sát từng tác nhân riêng lẻ. Theo dõi tỷ lệ hoàn thành tác vụ, độ trễ xử lý và tỷ lệ lỗi qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để các sự cố của một tác nhân không bị ẩn dưới số liệu gộp của cả đội.

### Các bước triển khai

- **Phân rã luồng công việc thành các tác nhân chuyên biệt:** Định nghĩa mỗi tác nhân quanh một chức năng nguyên tử duy nhất với lược đồ đầu vào và đầu ra tường minh.
- **Triển khai mỗi tác nhân trên AgentCore Runtime với một vai trò IAM dành riêng:** Chạy mỗi tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với vai trò thực thi được thu hẹp chỉ tới các tài nguyên mà chức năng của tác nhân đó cần.
- **Chọn mẫu giao tiếp liên tác nhân:** Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cho lời gọi kiểu công cụ ràng buộc lỏng, hoặc [giao thức A2A](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html) cho cộng tác ngang hàng với các mẫu tương tác phong phú hơn.
- **Giám sát từng tác nhân độc lập:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với số liệu và cảnh báo theo từng tác nhân để các sự cố của một tác nhân không bị che khuất bởi số liệu gộp cấp đội.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ](agentrel01-bp01.md)
- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](agentrel01-bp02.md)
- [AGENTREL01-BP04 Chuẩn hóa các giao thức giao tiếp](agentrel01-bp04.md)
- [AGENTSUS01-BP01 Design specialized agents with explicit resource boundaries](../../6-sustainability/1-agentsus01/agentsus01-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Deploy A2A servers in AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html)
- [Introducing Amazon Bedrock AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
