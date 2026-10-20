# Bảo vệ bộ nhớ và trạng thái của agent

Một trong những lý do khiến AI tác tử (agentic AI) hiệu quả là khả năng thực hiện các tác vụ chạy dài. Để đạt được mục tiêu, agent cần lưu trữ ngữ cảnh, tác vụ và kết quả. Hệ thống bộ nhớ của agent có thể bị nhắm tới để đưa vào thông tin sai lệch hoặc tác động đến quyết định của agent, vì vậy việc bảo vệ bộ nhớ và trạng thái giúp duy trì tính toàn vẹn của agent.

| AGENTSEC01: Bạn bảo vệ bộ nhớ tác tử và quản lý trạng thái giữa các agent một cách an toàn như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Bộ nhớ của agent được phân vùng theo các trục cô lập (isolation axes) quan trọng đối với khối công việc, mỗi principal chỉ được giới hạn ở những namespace mà tác vụ của nó cần.
- Việc phát hiện can thiệp trái phép (tamper detection) chạy trên mỗi lần đọc bộ nhớ, và lịch sử phiên bản chỉ-thêm (append-only versioned history) hỗ trợ tái dựng phục vụ điều tra khi nghi ngờ có ý đồ đầu độc (poisoning).
- Mọi đường ghi vào bộ nhớ — bao gồm đầu vào của người dùng, đầu ra của công cụ (Tools), thông điệp giữa các agent và quá trình hợp nhất (consolidation) — đều đi qua một đường ống kiểm định (validation pipeline) nhiều lớp trước khi dữ liệu tới kho lưu trữ.
- Các ảo giác (hallucinations) được phát hiện và kiềm chế trước khi lan tràn qua các phiên hoặc truyền tới các agent phía sau trong một luồng công việc đa agent.
- Các thao tác bộ nhớ được giám sát liên tục, và các tín hiệu truy cập bất thường hay tiêm nhiễm được định tuyến tới đường ống ứng phó sự cố để xem xét.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc bảo vệ bộ nhớ và trạng thái agent như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Bộ nhớ được dùng chung giữa các agent, người dùng hoặc phiên mà không có phân vùng namespace, được lưu không mã hóa và ghi không kiểm định. Ảo giác lan truyền không được kiểm soát, nhiễm bẩn xuyên phiên không thể phân biệt với hoạt động bình thường, và không có phát hiện can thiệp khi đọc. |
| 2 | Manh nha (Emerging) | Bộ nhớ được phân vùng theo phiên hoặc theo người dùng với việc giới hạn phạm vi cơ bản bằng quản lý danh tính và quyền truy cập (IAM) trên kho lưu trữ, và mã hóa tại chỗ (at rest) được bật. Kiểm định cú pháp kiểm tra kiểu, độ dài và định dạng trước khi ghi bộ nhớ, và các sự kiện bộ nhớ được đưa về log tập trung. Việc phát hiện chủ yếu mang tính phản ứng và phụ thuộc vào việc con người xem xét. |
| 3 | Được định nghĩa (Defined) | Tài nguyên bộ nhớ dùng lược đồ namespace phân cấp, ví dụ [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) với các placeholder theo từng actor và từng phiên, để tự động phân vùng dữ liệu. Kiểm định nhiều lớp kết hợp kiểm tra lược đồ với [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) để thực thi chính sách và lọc thông tin định danh cá nhân (PII), và [kiểm tra bám ngữ cảnh (contextual grounding checks)](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html) chạy trên các đầu ra rủi ro cao trước khi hợp nhất. |
| 4 | Chủ động (Proactive) | Việc xác minh tính toàn vẹn bằng mật mã dùng chữ ký HMAC được hậu thuẫn bởi [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) chạy trên mỗi lần đọc bộ nhớ. Mọi đường ghi dùng chung một đường ống kiểm định, bao gồm đầu ra công cụ và thông điệp giữa các agent. Phát hiện bất thường trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) cảnh báo về các mẫu truy cập bất thường, và một cầu dao ngắt ảo giác (hallucination circuit breaker) phát tín hiệu qua [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) để cách ly các mục bị ảnh hưởng trên các agent phía sau. |
| 5 | Tối ưu (Optimized) | Kiến trúc bộ nhớ được kiểm chứng thông qua các bài tập red-team định kỳ mô phỏng việc đầu độc và lan truyền. Chính sách kiểm định và ngưỡng bám ngữ cảnh thích ứng dựa trên các mẫu quan sát được, và tín hiệu phát hiện được đưa trực tiếp vào việc kiềm chế tự động. Quản trị bộ nhớ được mã hóa thành quy tắc (codified) và có thể kiểm toán. |

## Các vấn đề thường gặp cần lưu ý

- Namespace dùng chung được coi là mặc định thay vì một quyết định thiết kế có chủ đích, khiến một phiên bị ảnh hưởng có thể đọc hoặc ghi đè ngữ cảnh thuộc về một người dùng hoặc tenant khác.
- Kiểm định chỉ áp dụng tại ranh giới API công khai, trong khi đầu ra công cụ, thông điệp giữa các agent và các lượt ghi hợp nhất lại bỏ qua đường ống. Điều này tạo ra một điểm mù cho nội dung phát sinh bên trong hệ thống agent.
- Đầu ra của mô hình (Model) được ghi thẳng vào bộ nhớ dài hạn mà không kiểm tra bám ngữ cảnh, khiến các sự kiện ảo giác tồn tại xuyên phiên và tích lũy dần vì mỗi agent xây dựng chuỗi suy luận của mình trên ngữ cảnh bịa đặt từ các lần chạy trước.
- Giám sát ghi nhận các sự kiện bộ nhớ nhưng không định tuyến tín hiệu nào vào cảnh báo hay ứng phó sự cố, nên việc đầu độc và lan truyền chỉ được phát hiện khi rà soát sau sự cố.
- Chính sách truy cập bộ nhớ được thiết lập một lần khi triển khai và không bao giờ được xem xét lại, khiến quyền hạn trôi dạt khi hệ thống agent tiến hóa và tình trạng đặc quyền tối thiểu (least privilege) suy giảm theo thời gian.

###### Các thực hành tốt

- [AGENTSEC01-BP01 Triển khai kiểm soát cô lập và toàn vẹn bộ nhớ](agentsec01-bp01.md)
- [AGENTSEC01-BP02 Kiểm định và làm sạch đầu vào bộ nhớ](agentsec01-bp02.md)
- [AGENTSEC01-BP03 Giám sát sự lan truyền ảo giác](agentsec01-bp03.md)
