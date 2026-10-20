# AGENTSUS02-BP02 Thiết lập các chiến lược caching Agent hiệu quả

Mỗi lệnh gọi Model trùng lặp, mỗi lần gọi Tools và mỗi lần tra cứu bộ nhớ đều là công việc mà đội hình Agent đã làm một lần. Caching tại mỗi điểm tích hợp biến công việc lặp lại thành một chi phí một lần được phân bổ ra mọi bên gọi, để hiệu quả tài nguyên cải thiện khi các mẫu sử dụng ổn định lại thay vì tăng tuyến tính theo lưu lượng.

**Kết quả mong muốn:**

- Bạn có caching được áp dụng tại mỗi điểm tích hợp — tiền tố prompt (prompt prefix), kết quả Tools, tra cứu bộ nhớ và xác thực thông tin đăng nhập — với TTL khớp với độ biến động của dữ liệu.
- Các lớp cache được chia sẻ trên toàn đội hình Agent để kết quả từ cache của một Agent mang lại lợi ích cho mọi Agent khác.
- Tỷ lệ hit của cache được theo dõi theo từng điểm tích hợp và cải thiện khi các mẫu sử dụng ổn định lại.
- Các chính sách vô hiệu hóa (invalidation) giúp ngăn các phản hồi lỗi thời nơi độ biến động của dữ liệu đòi hỏi sự tươi mới.

**Các phản mẫu thường gặp (anti-patterns):**

- Gọi lặp lại cùng một Model nền với cùng một tiền tố prompt ổn định thay vì cache nó, phải trả tiền để xử lý lại cùng các token trong mỗi lần gọi.
- Cache kết quả Tools và phản hồi Model mà không có chính sách vô hiệu hóa hoặc TTL, tạo ra các câu trả lời lỗi thời trông có vẻ tươi mới.
- Chạy các cache cô lập cho từng Agent không chia sẻ trên toàn đội hình, nên mỗi Agent phải tự làm nóng (re-warm) cache riêng thay vì hưởng lợi từ kết quả đã được cache ở nơi khác.
- Bỏ qua việc đo đạc cache, nên không ai biết điểm tích hợp nào có tỷ lệ hit thấp và sẽ hưởng lợi từ một chiến lược caching khác.

**Lợi ích khi áp dụng thực hành tốt này:**

- Xử lý dư thừa, lệnh gọi API và lưu lượng mạng được giảm tại mỗi điểm tích hợp, để chi phí hạ tầng tăng dưới-tuyến-tính (sublinear) theo mức sử dụng Agent.
- Các lớp cache dùng chung nghĩa là thêm Agent vào đội hình làm tăng tỷ lệ hit của cache thay vì áp lực lên cache.
- Hiệu quả tài nguyên cộng dồn theo thời gian khi tỷ lệ hit của cache tiến dần đến cực đại ở trạng thái ổn định.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Góc nhìn bền vững về prompt caching bổ sung một cân nhắc nữa vào các góc nhìn hiệu năng và chi phí đã có sẵn của lăng kính này. Giá trị của caching không chỉ là độ trễ hay chi phí cho mỗi lệnh gọi. Đó là dấu chân compute và năng lượng tích lũy suốt vòng đời của đội hình, và cách caching được chia sẻ quyết định cách dấu chân tích lũy đó tăng lên.

Các cache cô lập cho từng Agent không cộng dồn. Nếu năm Agent mỗi cái duy trì cache riêng, đội hình làm nóng năm cache thay vì một, và các hit xuyên-Agent không bao giờ xảy ra. Các lớp cache dùng chung được lộ qua năng lực máy chủ MCP của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) đảo ngược điều này. Mọi Agent đọc từ và ghi vào cùng một tầng cache, để kết quả Tools của một Agent trở thành hit cache của Agent kế tiếp. Cùng nguyên tắc áp dụng ở lớp xác thực. [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) cache các token để việc xác thực thông tin đăng nhập xảy ra một lần mỗi phiên trên toàn đội hình thay vì một lần cho mỗi Agent.

[Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) mang lại lợi tức nhanh nhất. Các system prompt ổn định — các phần mở đầu dài định hình hành vi Agent — có thể được cache ở lớp Model để các lần gọi tiếp theo bỏ qua việc xử lý lại tiền tố. Caching ngữ nghĩa (semantic caching) thêm một lớp bổ trợ nơi các truy vấn tương tự (không giống hệt) phục vụ phản hồi từ cache sau một lần khớp dựa trên embedding, điều này đặc biệt có giá trị cho phần "đuôi dài" của các câu hỏi được diễn đạt lại mà người dùng đặt ra.

Vô hiệu hóa là nơi các chiến lược caching có thể thất bại. Một TTL cache được hiệu chỉnh cho việc làm mới hàng ngày trên dữ liệu thực sự thay đổi theo giờ sẽ phục vụ nội dung lỗi thời. Một TTL quá ngắn đến mức không đáng kể làm lãng phí toàn bộ mục đích của cache. Hãy chọn TTL dựa trên tần suất dữ liệu nền thực sự thay đổi, và theo dõi tỷ lệ hit qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để các chiến lược hoạt động kém được tinh chỉnh thay vì để nguyên đó.

### Các bước triển khai

- **Bật prompt caching cho các tiền tố ổn định:** Bật [Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) cho các system prompt ổn định theo các mẫu trong [AGENTPERF03-BP04 Establish efficient agent caching and data access patterns](../../4-performance-efficiency/3-agentperf03/agentperf03-bp04.md) và [AGENTCOST02-BP03 Leverage intelligent caching to reduce redundant model invocations](../../5-cost-optimization/2-agentcost02/agentcost02-bp03.md).
- **Chia sẻ các lớp cache trên toàn đội hình:** Lộ các cache kết quả Tools và cache ngữ nghĩa qua năng lực máy chủ MCP của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để mọi Agent đọc từ và ghi vào cùng một kho.
- **Cache việc xác thực thông tin đăng nhập:** Dùng [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) để cache các token, để phí tổn xác thực xảy ra một lần mỗi phiên thay vì một lần cho mỗi lần gọi Agent.
- **Đặt TTL dựa trên độ biến động của dữ liệu:** Chọn các chính sách vô hiệu hóa được hiệu chỉnh theo tần suất dữ liệu nền thực sự thay đổi — ngắn hơn cho dữ liệu vận hành trực tiếp, dài hơn cho tài liệu tham chiếu ổn định.
- **Giám sát và tinh chỉnh tỷ lệ hit:** Theo dõi tỷ lệ hit của cache theo từng điểm tích hợp qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và điều chỉnh các chiến lược nơi tỷ lệ hit thấp hơn kỳ vọng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP04 Establish efficient agent caching and data access patterns](../../4-performance-efficiency/3-agentperf03/agentperf03-bp04.md)
- [AGENTCOST02-BP03 Leverage intelligent caching to reduce redundant model invocations](../../5-cost-optimization/2-agentcost02/agentcost02-bp03.md)
- [AGENTSUS02-BP01 Tối ưu hóa quản lý ngữ cảnh và sử dụng bộ nhớ](agentsus02-bp01.md)
- [SUS03-BP03 Optimize areas of code that consume the most time or resources](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a4.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- [Effectively use prompt caching on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effectively-use-prompt-caching-on-amazon-bedrock/)
- [Optimize LLM response costs and latency with effective caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
