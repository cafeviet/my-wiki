# AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ

Agent sinh các tham số công cụ từ đầu ra của mô hình, nghĩa là các đầu vào không hợp lệ hoặc đối kháng có thể tới các công cụ qua suy luận thông thường, không chỉ qua các bên gọi trái phép. Kiểm định theo lược đồ (schema-driven) trên đầu vào và làm sạch trên đầu ra giữ cho công cụ hoạt động trong không gian tham số dự định của chúng và giúp ngăn thông báo lỗi làm lộ chi tiết hệ thống nội bộ.

**Kết quả mong muốn:**

- Bạn kiểm định mọi tham số truyền vào công cụ theo một lược đồ đã định trước khi thực thi, và làm sạch đầu ra của công cụ trước khi trả về cho agent.
- Việc tiêm nhiễm qua các tham số công cụ bị chặn, các đầu vào quá cỡ bị ngăn không làm cạn kiệt tài nguyên, và các thông báo lỗi được làm sạch để tránh rò rỉ thông tin hệ thống nhạy cảm.
- Các lần gọi công cụ hoạt động có thể dự đoán trong các ranh giới đã định, và các thất bại kiểm định được ghi log để phân tích bảo mật.

**Các phản mẫu thường gặp (anti-patterns):**

- Truyền thẳng các tham số thô do agent sinh vào công cụ mà không kiểm tra kiểu hay kiểm định phạm vi, để cho các đầu vào không hợp lệ gây hành vi bất ngờ hoặc tiêm nhiễm.
- Trả các thông báo lỗi thô của công cụ về cho agent mà không làm sạch, làm lộ chi tiết hệ thống nội bộ, stack trace hoặc thông tin hạ tầng có thể dùng để dò tìm sâu hơn.
- Chỉ kiểm định các đầu vào do người dùng cung cấp và bỏ qua kiểm định cho các tham số do suy luận của agent tạo ra, dựa trên giả định rằng mô hình không thể sinh đầu ra không hợp lệ.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm định đầu vào được thực thi theo lược đồ giúp ngăn các công cụ hoạt động ngoài không gian tham số dự định của chúng.
- Các phản hồi lỗi đã làm sạch trả về loại thất bại mà không làm lộ chi tiết hệ thống nội bộ.
- Các kiểm soát timeout, giới hạn bộ nhớ và thực thi kích thước đầu ra giúp ngăn cạn kiệt tài nguyên từ các lần gọi công cụ quá cỡ hoặc chạy dài.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Kiểm định hữu ích hơn khi nó diễn ra ở nhiều lớp so với khi bất kỳ một lớp đơn lẻ nào cố làm toàn bộ công việc. Lớp rẻ nhất và cụ thể nhất là ở chính mô hình. Đầu ra có cấu trúc (structured outputs) của Amazon Bedrock với sử dụng công cụ nghiêm ngặt (strict tool use) ràng buộc việc giải mã của mô hình sao cho các tham số công cụ được sinh luôn tuân theo lược đồ đầu vào đã định. Đặt strict: true trên định nghĩa công cụ, cùng với additionalProperties: false và các ràng buộc enum trên các trường có tập giá trị đóng, giúp ngăn các tham số không hợp lệ như một lớp vấn đề trước khi chúng tới được công cụ. Điều đó không thay thế kiểm định ở tầng ứng dụng, nhưng nó gỡ bỏ một phần lớn công việc khỏi tầng đó. [Bài blog Structured outputs on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/) trình bày các hình dạng tham số và việc thực thi ở cấp mô hình.

Lớp tiếp theo là kiểm định lược đồ trong đường ống gọi công cụ. Với các công cụ được triển khai dưới dạng hàm AWS Lambda, một phép kiểm tra JSON Schema bên trong trình xử lý Lambda, hoặc một Lambda Layer dùng chung, thực thi các ràng buộc kiểu, phạm vi giá trị, giới hạn độ dài chuỗi và mẫu định dạng trước khi logic của hàm chạy. Đây là nơi bắt các trường hợp biên mà strict tool use không bao quát — bất cứ gì liên quan đến quan hệ giữa các trường, các ràng buộc trạng thái bên ngoài, hoặc các giá trị mà mô hình không thể biết.

Policy in Amazon Bedrock AgentCore cung cấp một lớp thứ ba tại gateway. Các chính sách Cedar có thể đánh giá các điều kiện trên các tham số đầu vào của công cụ qua context.input, nên các quy tắc kinh doanh như "số tiền tài chính dưới một ngưỡng được phê duyệt" hoặc "tham số ngày trong một phạm vi chấp nhận được" được thực thi một cách xác định tại gateway trước khi lời gọi tới backend. Giá trị của lớp này là các quy tắc có thể kiểm toán và được quản lý độc lập với mã của công cụ. Giá trị của việc giữ nó tách khỏi hai lớp đầu là các thay đổi về quy tắc kinh doanh không đòi hỏi tái triển khai công cụ.

Các ràng buộc logic không thể diễn đạt dưới dạng lược đồ hoặc các phép so sánh đơn giản cần một cơ chế khác. Kiểm tra Automated Reasoning của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) xác minh rằng các tham số công cụ tuân theo các ràng buộc logic — một phạm vi ngày với ngày bắt đầu trước ngày kết thúc, một tập giá trị phải nhất quán với nhau. Hãy áp dụng Guardrails ở cấp AWS Organization nơi cần thực thi chính sách nhất quán trên tất cả các lần triển khai agent.

Bảo vệ tài nguyên và làm sạch lỗi hoàn thiện bức tranh. Giới hạn timeout và bộ nhớ của hàm AWS Lambda, được định cỡ theo hồ sơ thực thi đã đo của từng công cụ, giới hạn những gì bất kỳ lời gọi đơn lẻ nào có thể tiêu thụ, và concurrency dự trữ của Lambda chặn tổng số lần gọi song song. Các đầu ra công cụ trả về tập dữ liệu lớn cần giới hạn kích thước và phân trang. Các sự kiện cắt bớt (truncation) thuộc về log để một agent không âm thầm suy luận trên một phản hồi cục bộ. Xử lý lỗi bắt các ngoại lệ và trả về các phản hồi có cấu trúc mô tả loại thất bại mà không làm lộ chi tiết nội bộ, stack trace hoặc thông tin hạ tầng. Các nhóm quy tắc do AWS WAF quản lý trên các điểm cuối công cụ dựa trên API bổ sung một bộ lọc ở lớp mạng cho các mẫu tiêm nhiễm phổ biến trước khi yêu cầu tới mã của công cụ.

### Các bước triển khai

- **Ràng buộc tham số ở lớp mô hình:** Bật strict tool use (strict: true) trên các định nghĩa công cụ trong Amazon Bedrock, đặt additionalProperties: false trên mọi lược đồ đầu vào, và định nghĩa các ràng buộc enum cho các trường có tập giá trị hợp lệ giới hạn để chặn các tham số không hợp lệ tại thời điểm giải mã.
- **Thực thi lược đồ trong đường ống gọi:** Định nghĩa các đặc tả JSON Schema cho mọi công cụ và kiểm định các tham số như một lớp middleware bên trong trình xử lý Lambda hoặc một Lambda Layer dùng chung trước khi hàm công cụ chạy.
- **Thêm kiểm tra chính sách Cedar tại gateway:** Định nghĩa các chính sách trong AgentCore Policy với các điều kiện trên context.input để thực thi các quy tắc kinh doanh và ràng buộc tham số một cách xác định, bổ trợ cho kiểm định lược đồ ở cấp ứng dụng.
- **Dùng Automated Reasoning cho các ràng buộc logic:** Cấu hình các chính sách Automated Reasoning của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) cho các đầu vào và đầu ra công cụ đòi hỏi kiểm định ràng buộc logic vượt ra ngoài các quy tắc lược đồ và Cedar.
- **Định cỡ đúng giới hạn Lambda theo từng công cụ:** Đặt giới hạn timeout và bộ nhớ của AWS Lambda dựa trên các hồ sơ thực thi đã đo, với các giới hạn thận trọng giúp ngăn cạn kiệt tài nguyên, và dùng concurrency dự trữ để chặn các lần gọi song song.
- **Làm sạch lỗi:** Hiện thực xử lý lỗi có cấu trúc trong mọi công cụ, trả về các phản hồi đã làm sạch không có chi tiết hệ thống nội bộ, stack trace hoặc thông tin hạ tầng.
- **Phân trang và cắt bớt các đầu ra lớn:** Áp dụng giới hạn kích thước đầu ra cho các công cụ có thể trả về tập dữ liệu lớn, cắt bớt các phản hồi trước khi trả về cho agent, và ghi log mọi sự kiện cắt bớt.
- **Thêm AWS WAF đứng trước các công cụ dựa trên API:** Triển khai AWS WAF với các nhóm quy tắc quản lý trên các điểm cuối công cụ dựa trên API để lọc các mẫu tiêm nhiễm phổ biến ở lớp mạng.
- **Cảnh báo về tỷ lệ thất bại kiểm định:** Công bố các chỉ số Amazon CloudWatch cho các kết quả kiểm định và cấu hình cảnh báo cho các tỷ lệ thất bại tăng cao gợi ý các ý đồ tiêm nhiễm đang diễn ra hoặc các tham số bị sai cấu hình.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC02-BP01 Triển khai ủy quyền công cụ](agentsec02-bp01.md)
- [AGENTSEC02-BP03 Duy trì registry công cụ được phê duyệt kèm đánh giá bảo mật](agentsec02-bp03.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](../8-agentsec08/agentsec08-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Guardrails automated reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning.html)
- [Structured outputs on Amazon Bedrock: Schema-compliant AI responses](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [AWS Lambda best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS WAF](https://aws.amazon.com/waf/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
