# AGENTSEC01-BP02 Kiểm định và làm sạch đầu vào bộ nhớ

Các lượt ghi vào bộ nhớ agent mà không được kiểm định cho phép nội dung đối kháng tồn tại và tác động đến mọi phiên tiếp theo đọc cùng ngữ cảnh. Kiểm định nhiều lớp ngay tại điểm nạp (ingestion) giữ cho kho bộ nhớ không có các payload tiêm nhiễm, nội dung vi phạm chính sách và ngữ cảnh không nhất quán với tác vụ hiện tại.

**Kết quả mong muốn:**

- Bạn kiểm định mọi dữ liệu đi vào bộ nhớ agent về kiểu, định dạng và nội dung trước khi lưu trữ, đồng thời từ chối hoặc cách ly các đầu vào vi phạm chính sách trước khi chúng tác động đến hành vi của agent.
- Bạn phát hiện và chặn các ý đồ tiêm nhiễm tại lớp nạp bộ nhớ và định tuyến các đầu vào đáng ngờ tới việc con người xem xét.
- Kho bộ nhớ của bạn chỉ chứa dữ liệu đúng lược đồ, đã được làm sạch để các agent phía sau có thể tiêu thụ an toàn.

**Các phản mẫu thường gặp (anti-patterns):**

- Lưu thẳng đầu vào thô, chưa kiểm định của người dùng vào bộ nhớ agent, để cho các payload prompt injection tồn tại và tác động đến các phiên tương lai khi các agent xây dựng chuỗi suy luận dựa trên ngữ cảnh bị ảnh hưởng.
- Chỉ kiểm định tại ranh giới API công khai trong khi bỏ qua kiểm định cho nội dung đi vào bộ nhớ từ các đường ghi khác, bao gồm đầu ra công cụ, thông điệp giữa các agent và quá trình hợp nhất bộ nhớ.
- Không quét tìm các payload tiêm nhiễm được mã hóa hoặc làm rối, bỏ sót các chỉ thị mã hóa base64, các phép thay thế đồng tự Unicode (homoglyph) và những kiểu làm rối khác vượt qua các bộ lọc dựa trên từ khóa nhưng vẫn được các mô hình phía sau diễn giải.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm định nhiều lớp bắt các vấn đề ở cấp cú pháp, ngữ nghĩa và ngữ cảnh trước khi dữ liệu tới kho bộ nhớ.
- Việc chặn nội dung đối kháng tại ranh giới nạp giúp ngăn nó tác động đến suy luận của agent hoặc lan truyền tới các agent phía sau.
- Các chỉ số kiểm định làm nổi bật xu hướng trong tỷ lệ từ chối và các mẫu vấn đề, biến kiểm soát nạp thành tín hiệu vận hành.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Mọi lượt ghi vào bộ nhớ agent đều là một quyết định tin cậy. Đầu vào thô của người dùng là đường ghi hiển nhiên, nhưng nó không phải là đường duy nhất. Đầu ra công cụ đến từ các search API, cơ sở dữ liệu và dịch vụ bên thứ ba mà agent truy vấn. Thông điệp giữa các agent mang nội dung do một agent ghi vào phạm vi của agent khác, và quá trình hợp nhất bộ nhớ tạo ra các bản ghi dài hạn bằng cách tóm tắt hoặc gộp các sự kiện hiện có. Mỗi cái là một đường nạp riêng biệt, và mỗi cái cần cùng một cách xử lý kiểm định. Chỉ kiểm định tại ranh giới API công khai để lộ ba đường còn lại.

Một đường ống nhiều lớp cho mỗi loại vấn đề một nơi để bị bắt. Kiểm định cú pháp dựa trên JSON Schema từ chối kiểu sai, chuỗi quá dài và trường thiếu trước khi bất kỳ điều gì ngữ nghĩa xảy ra. Kiểm định ngữ nghĩa với [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) phát hiện các ý đồ prompt injection, các chủ đề bị cấm và nội dung vi phạm hướng dẫn của tổ chức thông qua API ApplyGuardrail — API này đánh giá nội dung độc lập với các lần gọi mô hình nên bạn có thể chạy nó tại bất kỳ điểm nào trong đường ống. Kiểm định ngữ cảnh kiểm tra xem một đầu vào có nhất quán với tác vụ hiện tại hay không và gắn cờ các bất thường để xem xét.

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho đường ống này một điểm tích hợp tự nhiên. Vì việc trích xuất bộ nhớ dài hạn chạy bất đồng bộ so với việc nạp sự kiện, chạy Guardrails trước khi các sự kiện được ghi qua API create_event sẽ chặn nội dung có hại không cho đi vào đường ống trích xuất, và chạy Guardrails lần nữa trước khi hợp nhất sẽ bắt bất cứ gì đã lọt qua lần kiểm tra đầu tiên. Các chiến lược bộ nhớ dựng sẵn đã lọc PII khỏi các bản ghi dài hạn theo mặc định, nhưng đó không thay thế cho việc thực thi tiêm nhiễm và chính sách — những thứ phải được bổ sung thêm.

Mô hình trách nhiệm chia sẻ (shared responsibility model) quan trọng ở đây. AWS chịu trách nhiệm về hạ tầng AgentCore Memory. Bạn chịu trách nhiệm về phát triển ứng dụng an toàn, kiểm định đầu vào và giúp ngăn chặn prompt injection trong dịch vụ trích xuất bộ nhớ. Các [thực hành tốt của AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html) khuyến nghị cụ thể việc làm sạch đầu vào người dùng bằng guardrails trước khi lưu bền vững qua CreateEvent. Nếu các lượt ghi bộ nhớ của bạn phát sinh từ các HTTP API mà bạn đã vận hành, AWS WAF đặt trước các API đó bổ sung một tầng ở lớp mạng, và việc kiểm định yêu cầu của Amazon API Gateway thực thi ràng buộc lược đồ ở cùng lớp. Với các lượt ghi hoàn toàn diễn ra trong mã của agent thông qua các lệnh gọi SDK trực tiếp, việc kiểm định trong mã của agent trước create_event là con đường đơn giản hơn.

Các đầu vào thất bại cần một phản hồi phân tầng. Các đầu vào rõ ràng có hại bị chặn và ghi log. Các đầu vào mơ hồ đi tới một hàng đợi cách ly Amazon SQS để con người xem xét, được lưu với đủ ngữ cảnh (ID agent, ID phiên, dấu thời gian và nguồn) để hỗ trợ điều tra. Mọi thất bại kiểm định phát ra các chỉ số Amazon CloudWatch để xu hướng tỷ lệ từ chối trở nên hiển thị và có thể cấu hình thành cảnh báo khi có điều gì thay đổi.

### Các bước triển khai

- **Định nghĩa lược đồ JSON cho mọi loại đầu vào bộ nhớ:** Chỉ định kiểu trường, giới hạn độ dài, giá trị cho phép và trường bắt buộc để lớp kiểm định đầu tiên có thể từ chối các đầu vào không hợp lệ một cách xác định.
- **Cấu hình Guardrails cho kiểm định ngữ nghĩa:** Cấu hình [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) với các chủ đề bị cấm, bộ lọc từ và bộ lọc thông tin nhạy cảm được điều chỉnh theo chính sách bảo mật của bạn, và dùng API ApplyGuardrail để kiểm định độc lập với các lần gọi mô hình.
- **Kiểm định mọi đường ghi, không chỉ đầu vào người dùng:** Áp dụng Guardrails cho cả đầu ra công cụ và thông điệp giữa các agent, cũng như nội dung do người dùng cung cấp, trước khi bất kỳ cái nào tới kho bộ nhớ.
- **Kiểm định trước create_event:** Chạy kiểm định trên các sự kiện trước khi chúng đi vào kho ngắn hạn của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) qua create_event, để nội dung có hại không đi vào đường ống trích xuất dài hạn bất đồng bộ.
- **Thêm AWS WAF trên các lượt ghi bộ nhớ đứng trước API:** Triển khai các nhóm quy tắc do AWS WAF quản lý trên các điểm cuối Amazon API Gateway chấp nhận đầu vào bộ nhớ, thực thi lọc tiêm nhiễm ở lớp mạng trước khi yêu cầu tới mã ứng dụng.
- **Cách ly các đầu vào mơ hồ để xem xét:** Định tuyến các thất bại vào một hàng đợi Amazon SQS kèm ID agent, ID phiên, dấu thời gian và nguồn, để con người có thể xem xét mà không chặn đường ống.
- **Phát ra dữ liệu đo lường kiểm định:** Công bố các chỉ số Amazon CloudWatch cho mọi kết quả kiểm định (pass, block hoặc quarantine) và cảnh báo về tỷ lệ từ chối tăng cao gợi ý một vấn đề đang diễn ra.
- **Xem xét các đầu vào bị cách ly thường xuyên:** Dùng hàng đợi cách ly để nhận diện các mẫu tấn công mới, cập nhật cấu hình Guardrail và tinh chỉnh các quy tắc kiểm định theo thời gian.
- **Kiểm thử tiêm nhiễm liên tục:** Áp dụng kiểm thử xâm nhập, phân tích mã tĩnh và kiểm thử bảo mật ứng dụng động (DAST) cho các đường ghi bộ nhớ như một phần của việc kiểm chứng bảo mật định kỳ.
- **Thực thi các điều kiện IAM trên CreateEvent:** Dùng IAM Access Analyzer để kiểm chứng rằng các chính sách tài nguyên bộ nhớ tuân theo đặc quyền tối thiểu, và thêm các điều kiện chính sách giới hạn những vai trò nào có thể gọi API CreateEvent cho các tài nguyên AgentCore Memory cụ thể.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC01-BP01 Triển khai kiểm soát cô lập và toàn vẹn bộ nhớ](agentsec01-bp01.md)
- [AGENTSEC01-BP03 Giám sát sự lan truyền ảo giác](agentsec01-bp03.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](../8-agentsec08/agentsec08-bp01.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Thực hành tốt Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)
- [Amazon Bedrock AgentCore Memory: Building context-aware agents](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/)
- [AWS WAF developer guide](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS WAF](https://aws.amazon.com/waf/)
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
