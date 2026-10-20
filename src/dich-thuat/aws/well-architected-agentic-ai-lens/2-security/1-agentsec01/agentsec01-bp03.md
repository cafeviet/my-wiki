# AGENTSEC01-BP03 Giám sát sự lan truyền ảo giác

Một sự kiện ảo giác đơn lẻ được lưu làm bộ nhớ sẽ trở thành sự thật nền tảng (ground truth) cho mọi agent đọc nó tiếp theo. Kiểm tra bám ngữ cảnh (grounding) liên tục và chấm điểm độ tin cậy giữ cho nội dung bịa đặt không đi vào bộ nhớ hay lan tràn qua một luồng công việc đa agent.

**Kết quả mong muốn:**

- Bạn phát hiện thông tin sai lệch trước khi nó lan truyền qua bộ nhớ agent hoặc lan tràn qua các luồng công việc đa agent.
- Bạn dùng chấm điểm độ tin cậy để làm nổi bật các đầu ra ít chắc chắn cho việc kiểm định, và kiểm chứng sự thật (fact-checking) để giúp ngăn dữ liệu ảo giác bị lưu như sự thật nền tảng.
- Khi phát hiện sự lan truyền ảo giác, các mục bộ nhớ bị ảnh hưởng được gắn cờ hoặc cách ly, và các agent phía sau được thông báo để loại bỏ ngữ cảnh có khả năng bị hỏng.

**Các phản mẫu thường gặp (anti-patterns):**

- Lưu thẳng đầu ra của mô hình vào bộ nhớ mà không có ngưỡng độ tin cậy hay kiểm tra bám ngữ cảnh, để cho các sự kiện ảo giác tồn tại và tác động đến các quyết định tương lai.
- Dựa vào chính mô hình sinh ra nội dung để tự báo cáo mức độ bất định, điều này tạo ra các đánh giá nghe có vẻ tự tin ngay cả với nội dung bịa đặt.
- Không lan truyền các cờ ảo giác tới các agent phía sau tiêu thụ bộ nhớ dùng chung, khiến ngữ cảnh bị hỏng âm thầm lan qua luồng công việc và mỗi agent khuếch đại lỗi.
- Không ghi log các sự kiện phát hiện ảo giác, làm giảm khả năng đo lường tần suất hoặc tác động và cản trở các nhóm điều chỉnh ngưỡng phát hiện hay nhận diện các mẫu mang tính hệ thống.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phát hiện sớm bắt các đầu ra ảo giác trước khi chúng lan truyền tới các agent phía sau và tích lũy thành lỗi hệ thống.
- Chấm điểm độ tin cậy cung cấp cơ sở định lượng để quyết định liệu các đầu ra có an toàn để lưu và hành động hay không.
- Giám sát liên tục làm nổi bật các mẫu ảo giác mới để điều chỉnh ngưỡng và tinh chỉnh quy tắc theo thời gian.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Ảo giác tích lũy dần. Một sự thật bịa đặt được lưu trong một phiên sẽ được truy xuất làm ngữ cảnh trong phiên tiếp theo, và agent thứ hai, suy luận dựa trên đầu vào đó, sản sinh một đầu ra thứ hai trông tự nhất quán với một tiền đề sai. Trong các hệ thống đa agent, vấn đề còn tệ hơn vì mỗi bên tiêu thụ phía sau coi bộ nhớ dùng chung là sự thật nền tảng. Phản hồi về mặt thiết kế là bắt các bịa đặt tại điểm chúng sắp đi vào bộ nhớ, gắn cờ chúng kèm bằng chứng, và lan truyền cờ đó tới bất cứ thứ gì đã đọc ngữ cảnh bị ảnh hưởng.

Kiểm tra bám ngữ cảnh của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) là lớp đầu tiên. Nó chấm điểm mỗi đầu ra của mô hình so với ngữ cảnh tham chiếu được cung cấp và từ chối hoặc gắn cờ bất cứ gì dưới ngưỡng. Các ứng dụng có tính an toàn quan trọng chạy với ngưỡng cao hơn, và các tác vụ sáng tạo có thể chạy với ngưỡng thấp hơn. Hãy kết hợp bám ngữ cảnh với mô hình LLM-as-a-Judge cho các chuỗi suy luận phức tạp: định tuyến các đầu ra qua một lần gọi mô hình thứ cấp nhận ngữ cảnh gốc, đầu ra của agent và một prompt đánh giá có cấu trúc, rồi trả về một đánh giá độ tin cậy. Chỉ khớp từ khóa là không đủ ở lớp này. Bộ giám khảo (judge) bắt các mâu thuẫn và tuyên bố không được hậu thuẫn mà các bộ lọc đơn giản bỏ sót.

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho phép kiểm tra này một nơi trú ngụ tự nhiên. Quá trình hợp nhất bộ nhớ dài hạn truy xuất các bộ nhớ hiện có tương tự về mặt ngữ nghĩa và dùng một LLM để quyết định thêm, cập nhật hay bỏ qua thông tin mới, và các bộ nhớ lỗi thời được đánh dấu là INVALID thay vì bị xóa. Điều đó tạo ra một dấu vết bất biến mà bạn có thể lần theo để truy vết cách nội dung ảo giác đã đi vào và lan truyền. Chạy kiểm tra bám ngữ cảnh trước create_event giúp giữ các bịa đặt ở ngoài đường ống trích xuất, và các ghi đè chiến lược bộ nhớ tùy chỉnh cho phép bạn tích hợp kiểm định bám ngữ cảnh vào các prompt trích xuất và hợp nhất theo miền của bạn.

Phát hiện mà không có khả năng truy vết thì tốn kém. Hãy bật ghi log lần gọi mô hình Amazon Bedrock (model invocation logging) và xây dựng các truy vấn Amazon CloudWatch Logs Insights tìm các dấu hiệu ảo giác (tham chiếu đến các tài nguyên không tồn tại, các phát biểu mâu thuẫn trong một phản hồi duy nhất, các đầu ra lệch đáng kể so với ngữ cảnh đầu vào). [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp một phân cấp phiên, dấu vết (trace) và span cho phép bạn tương quan một bất thường ở cấp phiên trở lại span cụ thể nơi nội dung ảo giác phát sinh. AgentCore phát ra dữ liệu span mặc định cho các tài nguyên bộ nhớ, có thể xem trong Amazon CloudWatch Logs và Amazon CloudWatch Application Signals, và các chỉ số ở cấp phiên có sẵn trên trang generative AI observability của CloudWatch. Để có khả năng quan sát sâu hơn, hãy trang bị cho mã của agent AWS Distro for OpenTelemetry (ADOT) nhằm thu thập các chỉ số tùy chỉnh cho điểm bám ngữ cảnh, ngưỡng độ tin cậy và kết quả kiểm định ở từng bước.

Cầu dao ngắt (circuit breaker) giữ một ảo giác đơn lẻ không lan tràn. Khi phát hiện kích hoạt ở một agent, hãy gắn cờ mọi mục bộ nhớ mà agent đó đã ghi trong phiên hiện tại để tái kiểm định trước khi các agent phía sau tiêu thụ, và phát tán sự kiện phát hiện qua Amazon EventBridge để mọi agent trong luồng công việc có thể loại bỏ ngữ cảnh có khả năng bị hỏng. Hãy gắn thẻ các mục bộ nhớ bằng điểm độ tin cậy và kết quả bám ngữ cảnh để cơ sở bằng chứng cho mọi quyết định đều có thể kiểm toán.

### Các bước triển khai

- **Cấu hình ngưỡng bám ngữ cảnh theo từng ca sử dụng:** Đặt các ngưỡng bám ngữ cảnh của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) khớp với hồ sơ rủi ro của từng agent, với ngưỡng cao hơn cho các ứng dụng có tính an toàn quan trọng và thấp hơn cho các tác vụ sáng tạo.
- **Thêm bước LLM-as-a-Judge cho các đầu ra rủi ro cao:** Định tuyến các đầu ra qua một lần gọi mô hình thứ cấp đánh giá tính nhất quán về mặt sự thật so với ngữ cảnh gốc trước khi đầu ra được ghi vào bộ nhớ.
- **Chạy kiểm tra bám ngữ cảnh trước create_event:** Áp dụng kiểm định bám ngữ cảnh tại ranh giới nạp sự kiện của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html), để nội dung ảo giác được lọc trước khi tới đường ống trích xuất và hợp nhất dài hạn.
- **Dùng các ghi đè chiến lược bộ nhớ tùy chỉnh cho bám ngữ cảnh theo miền cụ thể:** Đưa logic kiểm định bám ngữ cảnh vào các prompt trích xuất và hợp nhất thông qua các ghi đè chiến lược tùy chỉnh khi miền của bạn có yêu cầu cụ thể về tính đúng sự thật.
- **Bật ghi log lần gọi mô hình Amazon Bedrock:** Bật ghi log lần gọi mô hình Amazon Bedrock và tạo các truy vấn Amazon CloudWatch Logs Insights phát hiện tham chiếu đến tài nguyên không tồn tại, các phát biểu mâu thuẫn và các sai lệch đáng kể so với ngữ cảnh đầu vào.
- **Cảnh báo về các bất thường trong tính nhất quán đầu ra:** Cấu hình phát hiện bất thường của Amazon CloudWatch trên các chỉ số nhất quán đầu ra để thiết lập đường cơ sở các mẫu bình thường và cảnh báo về các sai lệch gợi ý ảo giác mang tính hệ thống.
- **Trang bị bằng ADOT và AgentCore Observability:** Dùng AWS Distro for OpenTelemetry để thu thập các span tùy chỉnh cho điểm bám ngữ cảnh và kết quả kiểm định, và dùng phân cấp phiên/trace/span trong [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để tương quan các phát hiện trở lại tương tác gốc.
- **Đấu nối một cầu dao ngắt cho việc lan truyền:** Khi một ảo giác kích hoạt, hãy gắn cờ mọi mục bộ nhớ từ phiên hiện tại và phát tán sự kiện phát hiện qua Amazon EventBridge để các agent phía sau có thể loại bỏ ngữ cảnh có khả năng bị hỏng.
- **Gắn thẻ các mục bộ nhớ bằng bằng chứng:** Lưu điểm độ tin cậy và kết quả kiểm tra bám ngữ cảnh cùng với mỗi mục bộ nhớ để tạo ra một bản ghi có thể kiểm toán về cơ sở bằng chứng cho các quyết định của agent.
- **Xem xét log phát hiện định kỳ:** Điều chỉnh ngưỡng, cập nhật quy tắc phát hiện và nhận diện các mẫu mang tính hệ thống bằng cách xem xét log phát hiện ảo giác theo nhịp định kỳ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC01-BP01 Triển khai kiểm soát cô lập và toàn vẹn bộ nhớ](agentsec01-bp01.md)
- [AGENTSEC01-BP02 Kiểm định và làm sạch đầu vào bộ nhớ](agentsec01-bp02.md)
- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)
- [AGENTREL05-BP03 Neo nhận thức của agent vào thông tin thực tế](../../3-reliability/5-agentrel05/agentrel05-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Guardrails contextual grounding](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-grounding.html)
- [Amazon Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [AgentCore Observability: Sessions, traces, and spans](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html)
- [Thực hành tốt Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)
- [Building smarter AI agents: AgentCore long-term memory deep dive](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
