# AGENTREL02-BP01 Thiết kế các tác nhân cho các tác vụ cụ thể và nguyên tử

Đầu ra của LLM mang tính ngẫu nhiên, nên phạm vi trách nhiệm của một tác nhân cũng là phạm vi của tính ngẫu nhiên đó. Các tác nhân hẹp, nguyên tử với hợp đồng đầu vào tường minh và lược đồ đầu ra có cấu trúc làm cho các phần khó lường của mô hình trở nên quan sát được, kiểm thử được và kiềm chế được.

**Kết quả mong muốn:**

- Bạn có mỗi tác nhân được thu hẹp phạm vi về một chức năng nguyên tử với kiểm tra đầu vào tường minh và một lược đồ đầu ra có cấu trúc.
- Các tác nhân của bạn được kiểm thử với đầu vào tất định, đại diện trước khi triển khai.
- Bạn theo dõi các số liệu chất lượng theo từng tác nhân (tỷ lệ tuân thủ lược đồ và tỷ lệ hoàn thành tác vụ) để các thoái lui xuất hiện trước khi người dùng nhìn thấy.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây dựng các tác nhân đa mục đích kết hợp nhiều chức năng khác nhau, mở rộng bề mặt cho hành vi khó lường của mô hình.
- Bỏ qua các hợp đồng đầu vào tường minh và lược đồ đầu ra, cho phép các luồng dữ liệu mơ hồ khuếch đại tính ngẫu nhiên của LLM.
- Coi các tác nhân như các bộ xử lý đa dụng không có trách nhiệm rời rạc, khiến việc tái lập sự cố trở nên khó khăn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phạm vi bị ràng buộc thu nhỏ bề mặt cho hành vi khó lường.
- Các đơn vị có thể kết hợp được có thể kiểm định độc lập với các trường hợp kiểm thử tất định.
- Ranh giới vận hành rõ ràng đẩy nhanh việc xác định và khắc phục sự cố.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Thiết kế nguyên tử bắt đầu từ prompt. Một system prompt duy nhất, được định nghĩa tốt, mô tả chính xác một năng lực là ràng buộc dễ thực thi nhất và khó vi phạm âm thầm nhất. Ghép nó với kiểm tra đầu vào tường minh từ chối các yêu cầu ngoài phạm vi trước khi gọi LLM, và một lược đồ đầu ra có cấu trúc ràng buộc định dạng phản hồi. Việc dùng công cụ (gọi hàm) của Amazon Bedrock giới hạn không gian hành động của mô hình vào các thao tác liên quan đến chức năng của tác nhân. Tính năng [đầu ra có cấu trúc (structured output)](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html) của Amazon Bedrock thực thi việc tuân thủ lược đồ JSON ở cấp mô hình để giảm lỗi kiểm định đầu ra.

Triển khai củng cố ranh giới nguyên tử. Mỗi tác nhân chạy trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với bối cảnh thực thi riêng và quyền công cụ dành riêng, nhờ đó một tác nhân bị cấu hình sai hoặc bị xâm nhập không thể vươn ra ngoài phạm vi của nó. Điều này cho bạn một ranh giới vật lý khớp với ranh giới logic bạn đã định nghĩa trong prompt.

Kiểm thử là nơi thiết kế nguyên tử phát huy giá trị. Vì mỗi tác nhân có một hợp đồng hẹp, bạn có thể chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trên các đầu vào đại diện và so sánh đầu ra với kết quả kỳ vọng. Đầu ra của LLM không hoàn toàn tất định ngay cả với temperature=0, nên các bài kiểm thử nên kiểm định tính đúng đắn về ngữ nghĩa thay vì so khớp chuỗi chính xác. Giám sát mỗi tác nhân qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) theo dõi tỷ lệ tuân thủ lược đồ và tỷ lệ hoàn thành tác vụ, với cảnh báo khi các số liệu trôi khỏi đường cơ sở.

### Các bước triển khai

- **Phân rã luồng công việc thành các tác nhân nguyên tử:** Cho mỗi tác nhân một system prompt duy nhất, một tập công cụ bị ràng buộc, và các lược đồ đầu vào/đầu ra tường minh.
- **Triển khai trên AgentCore Runtime với thực thi đầu ra có cấu trúc:** Chạy mỗi tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với quyền công cụ dành riêng và thực thi [đầu ra có cấu trúc của Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html).
- **Triển khai kiểm tra đầu vào từ chối các yêu cầu ngoài phạm vi:** Kiểm định đầu vào trước khi gọi LLM để các yêu cầu dị dạng hoặc ngoài phạm vi không tới được mô hình.
- **Kiểm định hành vi với AgentCore Evaluations:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) với đầu vào đại diện và các trường hợp kiểm thử golden-path, khẳng định tính đúng đắn ngữ nghĩa thay vì chuỗi chính xác.
- **Giám sát các số liệu chất lượng theo từng tác nhân:** Theo dõi tỷ lệ tuân thủ lược đồ và tỷ lệ hoàn thành tác vụ qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với cảnh báo khi lệch khỏi đường cơ sở.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model](../1-agentrel01/agentrel01-bp03.md)
- [AGENTREL02-BP02 Giới hạn quyền hạn của tác nhân ở mức truy cập tối thiểu cần thiết](agentrel02-bp02.md)
- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](agentrel02-bp03.md)
- [AGENTREL02-BP04 Phát triển các giao thức chỉ dẫn rõ ràng cho tác nhân](agentrel02-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Build reliable AI agents with Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [Amazon Bedrock structured output](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)
- [Strands Agents Custom Tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/)

**Video liên quan:**

- [Strands Tools: Building Custom AI Agents with Python](https://www.youtube.com/watch?v=EGhIZCfOvG4)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
