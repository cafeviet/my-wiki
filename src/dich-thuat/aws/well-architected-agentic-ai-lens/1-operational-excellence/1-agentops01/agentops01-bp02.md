# AGENTOPS01-BP02 Thiết kế quy trình bàn giao đa agent với leo thang có con người trong vòng lặp

Nếu không có gói ngữ cảnh (context package) có cấu trúc, agent tiếp nhận sẽ phải tái suy ra công việc mà agent trước đó đã hoàn tất. Việc thiếu một đường leo thang được xác định có nghĩa là các quyết định rủi ro cao hoặc độ tin cậy thấp có thể lọt qua khỏi tầm rà soát của con người.

**Kết quả mong muốn:**

- Bạn có các giao thức bàn giao được tài liệu hóa để chuyển giao tác vụ giữa các agent với đầy đủ ngữ cảnh và trách nhiệm rõ ràng.
- Bạn có các đường leo thang định tuyến yêu cầu tới đúng agent hoặc người rà soát khi một agent chạm tới giới hạn năng lực của nó.
- Bạn phát hiện tình trạng bế tắc (deadlock) và hết thời gian (timeout) một cách tự động và giải quyết chúng thông qua các quy trình phục hồi được tài liệu hóa.
- Bạn giám sát độ trễ bàn giao, mức độ đầy đủ của việc chuyển giao ngữ cảnh, và tỷ lệ cộng tác thành công như các chỉ số vận hành hạng nhất.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai bàn giao agent-tới-agent mà không có gói ngữ cảnh có cấu trúc, buộc agent tiếp nhận phải tái suy ra ngữ cảnh và lặp lại công việc mà agent ủy thác đã hoàn tất.
- Chỉ dựa vào leo thang agent-tới-agent mà không xác định các tác nhân agent-tới-con người, khiến các quyết định rủi ro cao hoặc độ tin cậy thấp không có sự giám sát của con người.
- Triển khai luồng công việc đa agent mà không có phát hiện bế tắc hoặc xử lý timeout, cho phép các phụ thuộc vòng (circular dependencies) giữa các agent làm đình trệ luồng công việc vô hạn định.
- Xem lỗi bàn giao như sự kiện hiếm gặp, nên không ai theo dõi tỷ lệ thành công hay mức độ đầy đủ của việc chuyển giao ngữ cảnh cho đến khi một sự cố với khách hàng buộc phải điều tra.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các runbook bàn giao và quy trình leo thang được tài liệu hóa tạo ra các mẫu cộng tác có thể lặp lại giúp giảm độ phức tạp vận hành.
- Các tác vụ cần phán đoán của con người sẽ tin cậy đến được người rà soát mà không tạo ra nút thắt cổ chai trong công việc agent-tới-agent thường lệ.
- Các bàn giao giàu ngữ cảnh giúp tránh suy luận trùng lặp, cắt giảm cả độ trễ và chi phí Token trong luồng công việc đa agent.
- Phát hiện bế tắc và xử lý timeout giữ cho các lỗi phối hợp nhất thời không trở thành sự cố ở cấp độ luồng công việc.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Một cuộc bàn giao là một hợp đồng dữ liệu (data contract) trước khi là một bước trong luồng công việc. Agent gửi phải biết đưa gì vào payload, trong khi agent tiếp nhận phải biết kỳ vọng những gì. Khi hợp đồng đó bị thiếu, mỗi cuộc bàn giao trở thành một cuộc thương lượng ứng biến, trong đó bên tiếp nhận hoặc hỏi thêm thông tin (thêm các vòng qua lại) hoặc đoán mò (thêm lỗi). Các giao thức chuẩn hóa như Model Context Protocol (MCP) và giao tiếp agent-to-agent (A2A) mang lại cho các agent được xây trên các framework khác nhau một vốn từ chung để mô tả tác vụ, công việc đã hoàn tất, các tài liệu bộ nhớ (memory artifacts), và lý do bàn giao, để hợp đồng đó giữ ổn định bất kể lựa chọn công nghệ.

Khám phá (discovery) nên là một phần của hợp đồng dữ liệu. Các agent cần biết những đồng nghiệp nào tồn tại, chúng có thể làm gì, và liệu chúng có đang nhận việc ngay lúc này hay không. [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) cung cấp một catalog tập trung nắm bắt năng lực, tình trạng sẵn sàng, và metadata cho các agent và Tools, giúp định tuyến thông minh khả thi thay vì hardcode. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) sau đó mang lại cho luồng công việc kết nối an toàn và lời gọi Tools qua các agent, với mọi tương tác đều có thể kiểm toán.

Leo thang có hai tác nhân kích hoạt riêng biệt cần cân nhắc:

- Leo thang agent-tới-agent xảy ra khi một tác vụ cần năng lực nằm ngoài phạm vi của agent hiện tại. Tác nhân này là một quyết định định tuyến.
- Leo thang agent-tới-con người xảy ra khi độ tin cậy giảm dưới ngưỡng, mức rủi ro cao, hoặc ngân sách thử lại (retry budget) đã cạn. Tác nhân này là một quyết định phán đoán.

Trộn lẫn chúng lại hoặc gửi quá nhiều tác vụ thường lệ tới con người (tạo mệt mỏi và nút thắt cổ chai) hoặc gửi quá nhiều quyết định rủi ro cao qua định tuyến tự động (tạo rủi ro). Hãy quy định từng tác nhân riêng biệt và xác minh rằng bạn có thể thấy khi nào mỗi tác nhân được kích hoạt.

Bế tắc xứng đáng được chú ý riêng vì chúng âm thầm. Hai agent có thể chờ nhau vô hạn định trong khi mọi thao tác riêng lẻ đều có vẻ khỏe mạnh.

Một cuộc chờ vượt quá timeout có thể cấu hình là một nghi phạm bế tắc, nhưng phản ứng phải được tự động hóa: gán lại tác vụ, thông báo cho con người, hoặc cả hai. Một bế tắc cần con người phát hiện là một bế tắc kéo dài cho đến khi có người nhận ra.

### Các bước triển khai

- **Tài liệu hóa các runbook bàn giao:** Bao phủ năm kịch bản cộng tác agent-tới-agent hàng đầu, quy định định dạng gói ngữ cảnh, tiêu chí chấp nhận, và kết quả kỳ vọng.
- **Định nghĩa một lược đồ gói ngữ cảnh có cấu trúc:** Bao gồm mô tả tác vụ, công việc đã hoàn tất, các tài liệu bộ nhớ, và lý do bàn giao. Đánh phiên bản lược đồ để bên tiếp nhận có thể từ chối các bàn giao không hợp lệ.
- **Triển khai một agent registry:** Lập catalog năng lực agent, trạng thái sẵn sàng, và tiêu chí chấp nhận bàn giao trong [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) để cho phép khám phá tại runtime và định tuyến thông minh.
- **Kết nối các agent qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html):** Cấu hình kết nối an toàn, lời gọi Tools, và ủy quyền qua các agent với hồ sơ tương tác có thể kiểm toán.
- **Định nghĩa tiêu chí leo thang:** Tách các tác nhân agent-tới-agent (không khớp năng lực) khỏi các tác nhân agent-tới-con người (ngưỡng độ tin cậy, quyết định rủi ro cao, cạn ngân sách thử lại), và trang bị đo lường cho từng loại.
- **Triển khai phát hiện bế tắc:** Cấu hình cảnh báo trên thời lượng thực thi luồng công việc, và tự động hóa việc giải quyết thông qua gán lại tác vụ và thông báo cho con người.
- **Giám sát sức khỏe cộng tác:** Theo dõi tỷ lệ thành công, độ trễ bàn giao, và mức độ đầy đủ của việc chuyển giao ngữ cảnh trong [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/), với cảnh báo trên tỷ lệ lỗi bàn giao.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent](agentops01-bp01.md)
- [AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools](../4-agentops04/agentops04-bp01.md)
- [AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)](../4-agentops04/agentops04-bp02.md)
- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](../5-agentops05/agentops05-bp01.md)
- [AGENTPERF05-BP04 Triển khai các mẫu ủy thác và bàn giao agent hiệu quả](../../4-performance-efficiency/5-agentperf05/agentperf05-bp04.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Các mẫu và luồng công việc agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Các framework, nền tảng, giao thức và công cụ agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Amazon Bedrock Agents and AgentCore Design Patterns (TNC322)](https://www.youtube.com/watch?v=GYlPFmrATjU)
- [AWS re:Invent 2024 - Building Scalable, Self-Orchestrating AI Workflows with A2A and MCP (DEV415)](https://www.youtube.com/watch?v=9O9zZ1lQWiI)
- [AWS re:Invent 2024 - Anti-Money Laundering Multi-agent Orchestration with AWS Strands (DEV326)](https://www.youtube.com/watch?v=VtrfpAVFKdE)

**Ví dụ liên quan:**

- [GitHub: Sample Multi-Agent SaaS Workshop](https://github.com/aws-samples/sample-saas-multi-agents-workshop)
- [GitHub: Sample Agentic Platform on AWS](https://github.com/aws-samples/sample-agentic-platform)
- [GitHub: Sample Bedrock AgentCore Multi-Tenant](https://github.com/aws-samples/sample-bedrock-agentcore-multitenant)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
