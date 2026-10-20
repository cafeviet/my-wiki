# AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh

Các Agent nguyên khối (monolithic) cấp phát dư thừa cho đầu vào trường hợp xấu nhất sẽ lãng phí compute mà không có nhật ký kiểm toán đáng tin cậy để theo dõi mức tiêu thụ. Để làm cho mức tiêu thụ có thể truy vết ở mọi lớp, hãy dùng các Agent chuyên biệt với năng lực nguyên tử đơn lẻ và ranh giới tài nguyên tường minh. Cấp cho mỗi Agent một timeout, một mức trần bộ nhớ và một ngân sách token. Khi đó, mỗi đơn vị chi tiêu tài nguyên đều ánh xạ ngược về tác vụ đã gây ra nó.

**Kết quả mong muốn:**

- Bạn đã phân rã các quy trình thành các Agent chuyên biệt, mỗi Agent chịu trách nhiệm cho một năng lực nguyên tử với các giới hạn tài nguyên được khai báo.
- Các Agent cha xếp tầng ngân sách tài nguyên xuống các Agent con qua lớp điều phối, để việc ủy quyền có chi phí compute và token dự đoán được.
- Bạn theo dõi mức tiêu thụ tài nguyên cho mỗi Agent (thời lượng, token và tỷ lệ lỗi) xuyên suốt các chuỗi ủy quyền để việc cấp phát dư thừa trở nên hiển thị.
- Các Agent chuyên biệt tái sử dụng được lộ ra qua một lớp Tools dùng chung, để một Agent được bao ranh giới tốt phục vụ nhiều quy trình cha.

**Các phản mẫu thường gặp (anti-patterns):**

- Cấp phát compute và bộ nhớ cho đầu vào trường hợp xấu nhất bất kể yêu cầu thực tế của tác vụ, tạo ra hiệu suất sử dụng thấp và chi phí không cần thiết.
- Ủy quyền từ Agent cha sang Agent con mà không chuyển kèm timeout, số lần thử lại hoặc ngân sách token, khiến công việc phía dưới không có mức trần chi phí có thể thực thi.
- Triển khai các Agent nguyên khối gộp nhiều năng lực trong một tiến trình, ngăn cản việc mở rộng độc lập và khiến việc quy chi phí theo từng năng lực trở nên bất khả thi.
- Nhân bản việc hiện thực một năng lực (xác thực, trích xuất hoặc biến đổi) qua các quy trình vì không tồn tại Agent dùng chung có ranh giới tài nguyên đã biết.

**Lợi ích khi áp dụng thực hành tốt này:**

- Mức tiêu thụ tài nguyên giữ tỷ lệ thuận với tác vụ, vì mỗi Agent chạy trong các ranh giới phù hợp với năng lực đơn lẻ của nó.
- Việc quy chi phí trở nên hiển thị ở cấp độ Agent. Các Agent bị cấp phát dư thừa hoặc hoạt động kém dễ dàng được nhận diện và điều chỉnh đúng kích cỡ.
- Các Agent chuyên biệt phân bổ chi phí phát triển của chúng ra nhiều quy trình cha khi được lộ ra dưới dạng Tools tái sử dụng được.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Đơn vị chịu trách nhiệm tài nguyên đúng đắn là năng lực, không phải bản triển khai. Khi một tiến trình đơn lẻ xử lý xác thực, làm giàu, trích xuất và ra quyết định, cách duy nhất an toàn để định kích cỡ nó là giả định mọi lệnh gọi đều làm cả bốn. Tách các năng lực đó thành các Agent riêng biệt cho phép mỗi Agent mang theo timeout, mức trần bộ nhớ và ngân sách token phù hợp với công việc thực tế của nó. Điều chỉnh đúng kích cỡ trở thành câu hỏi về từng năng lực thay vì một sự thỏa hiệp trên toàn bộ quy trình.

Ngân sách sẽ mất tác dụng ngay khoảnh khắc một lệnh ủy quyền vượt qua ranh giới mà không mang theo nó. Lớp điều phối phải truyền lượng thời gian còn lại, số token còn lại và ngân sách thử lại vào mỗi lần gọi Agent con. Trong [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html), điều đó nghĩa là đặt TimeoutSeconds và số lần thử lại trên mỗi trạng thái lồng nhau. Trong một orchestrator dựa trên Strands, điều đó nghĩa là truyền ngân sách còn lại như một phần tham số gọi Agent con. Không có sự xếp tầng đó, tổng chi phí quy trình là vô hạn định bất kể Agent cấp cao nhất hứa hẹn điều gì.

Khi một Agent xác thực dữ liệu được bao ranh giới tốt phục vụ hàng chục quy trình cha thông qua năng lực máy chủ MCP của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), chi phí phát triển và tối ưu hóa của nó được phân bổ ra mọi bên gọi. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) cung cấp môi trường thực thi cô lập theo phiên (session-isolated), giúp mỗi lần gọi mang theo ngữ cảnh tài nguyên riêng của nó. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) hoạt động ở ranh giới lưu lượng để từ chối các lệnh gọi vượt quá giới hạn đã khai báo trước khi chúng tiêu thụ năng lực.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) thu thập thời lượng, số lượng token và tỷ lệ lỗi cho mỗi lần gọi xuyên suốt các chuỗi ủy quyền, nên bức tranh hiệu suất sử dụng cho mỗi Agent là như nhau ở mọi cấp của hệ phân cấp. Hãy rà soát mức tiêu thụ theo Agent hàng tháng để tìm những Agent luôn chạy thấp hơn nhiều so với giới hạn đã khai báo. Đó là những ứng viên đầu tiên cho việc điều chỉnh đúng kích cỡ.

### Các bước triển khai

- **Phân rã quy trình thành các Agent năng lực đơn lẻ:** Nhận diện các hàm nguyên tử trong mỗi quy trình và triển khai mỗi hàm như một Agent riêng trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) với giới hạn timeout, bộ nhớ và token tường minh. Các hàm nguyên tử phổ biến gồm: Xác thực
- Trích xuất
- Biến đổi
- Quyết định
- **Xếp tầng ngân sách qua các ranh giới ủy quyền:** Cấu hình lớp điều phối ([AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html) hoặc một orchestrator dựa trên Strands) để truyền các thông tin sau vào mỗi lần gọi Agent con, nhằm công việc phía dưới kế thừa mức trần chi phí của Agent cha: Thời gian còn lại
- Số lần thử lại
- Ngân sách token
- **Lộ các Agent chuyên biệt dưới dạng Tools tái sử dụng được:** Công bố các Agent qua năng lực máy chủ MCP của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để các quy trình cha gọi chúng mà không phải nhúng bản sao riêng.
- **Thực thi giới hạn ở lớp lưu lượng:** Áp các quy tắc Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) ở ranh giới Gateway để từ chối các lệnh gọi vượt giới hạn tài nguyên đã khai báo trước khi chúng tiêu thụ năng lực.
- **Đo đạc mức tiêu thụ và rà soát hàng tháng:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập các thông tin sau cho mỗi Agent: Thời lượng gọi
- Số lượng token
- Tỷ lệ lỗi

Rà soát hiệu suất sử dụng trong Amazon CloudWatch hàng tháng để điều chỉnh ranh giới đúng kích cỡ đối chiếu với mức dùng thực tế.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được](agentsus01-bp02.md)
- [AGENTSUS01-BP03 Tối ưu hóa việc sử dụng tài nguyên thông qua dịch vụ dùng chung](agentsus01-bp03.md)
- [SUS03-BP01 Optimize software and architecture for asynchronous and scheduled jobs](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a2.html)
- [COST09-BP03 Supply resources dynamically](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_manage_demand_resources_dynamic.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [AWS Step Functions - Nested workflows](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html)
- [Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Strands Agents](https://strandsagents.com/)

**Các ví dụ liên quan:**

- [Build multi-agent systems with LangGraph and Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/)
- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
