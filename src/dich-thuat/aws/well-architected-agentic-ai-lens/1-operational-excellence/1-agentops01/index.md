# Thực hành vận hành cho hệ thống agentic AI

Các hệ thống agentic được xây dựng trên nền tảng vận hành vững chắc (với vai trò rõ ràng, bàn giao (handoff) đáng tin cậy, và phục hồi lỗi đã được kiểm thử) sẽ giành được niềm tin của các bên liên quan và mở rộng vào sản xuất (production) một cách tự tin. Các hệ thống này kết hợp tiền lệ và thực hành tốt từ nhiều lĩnh vực kiến trúc, bao gồm AI tạo sinh (generative AI) và phối hợp đa agent (multi-agent coordination). Không thể kết hợp các thực hành này một cách tùy tiện. Chúng phải được lựa chọn và tinh chỉnh một cách thận trọng dựa trên workload đang được xây dựng và bài toán kinh doanh cần giải quyết.

| AGENTOPS01: Bạn thiết lập các thực hành vận hành cho hệ thống agentic AI như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Mỗi agent có một mục đích được tài liệu hóa, tiêu chí thành công đo lường được, và ranh giới tự chủ (autonomy boundaries) mà các bên liên quan có thể truy nguyên về một kết quả kinh doanh cụ thể.
- Phối hợp đa agent diễn ra qua các giao thức bàn giao chuẩn hóa, giúp chuyển giao ngữ cảnh một cách tin cậy và định tuyến công việc tới người rà soát khi ngưỡng độ tin cậy, mức độ rủi ro, hoặc năng lực bị vượt qua.
- Các hệ thống agent được kiểm định trước các chế độ lỗi (failure modes) thực tế trên các thành phần phụ thuộc, giao thức điều phối (orchestration protocols), và quy trình kinh doanh trước khi vào sản xuất, và trên mỗi thay đổi hành vi sau đó.
- Các tín hiệu vận hành, kết quả kiểm thử lỗi, và chỉ số kinh doanh cung cấp thông tin cho một vòng lặp cải tiến liên tục nhằm giữ cho hành vi agent phù hợp với nhu cầu kinh doanh đang tiến hóa.
- Các tài liệu vận hành như bản mô tả công việc (job descriptions), runbook bàn giao, và các kịch bản kiểm thử lỗi được xem là tài liệu sống, luôn được đồng bộ với các agent mà chúng mô tả.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với thực hành vận hành cho hệ thống agentic AI như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Phạm vi agent, bàn giao, và kiểm thử lỗi mang tính tùy ứng (ad-hoc). Tri thức về việc mỗi agent nên làm gì, và các agent tương tác ra sao, nằm ở từng người xây dựng riêng lẻ. Các yêu cầu ngoài phạm vi tạo ra phản hồi khó lường, bàn giao làm mất ngữ cảnh, và các chế độ lỗi thường lần đầu gặp phải trong các sự cố sản xuất. |
| 2 | Manh nha (Emerging) | Mỗi agent có bản mô tả công việc được tài liệu hóa bao gồm mục đích, các bên liên quan, và tiêu chí thành công đo lường được. Các runbook bàn giao cơ bản và đường leo thang tới con người bao phủ những kịch bản phổ biến nhất. Một bộ kiểm thử lỗi ban đầu bao phủ luồng thuận lợi (happy path) và một số ít lỗi thành phần phụ thuộc, và việc rà soát diễn ra theo nhịp không chính thức. |
| 3 | Được định nghĩa (Defined) | Bản mô tả công việc agent, giao thức bàn giao, và bộ kiểm thử lỗi được chuẩn hóa xuyên suốt các nhóm và lưu trong kho dùng chung. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) áp đặt phạm vi tại thời điểm chạy (runtime), các gói ngữ cảnh có cấu trúc đi kèm mọi lần bàn giao, và các kiểm thử lỗi chạy trong CI/CD như một cổng bắt buộc trên các thành phần phụ thuộc, giao thức điều phối, và quy trình kinh doanh. Tỷ lệ bàn giao thành công và tỷ lệ vượt qua kiểm thử lỗi được theo dõi như các chỉ số hạng nhất. |
| 4 | Chủ động (Proactive) | Các kiểm soát vận hành được tự động hóa và dựa trên dữ liệu. [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) hỗ trợ khám phá tại runtime và định tuyến thông minh qua các agent và Tools. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy theo nhịp định kỳ để kiểm định hiệu năng và khả năng chịu lỗi của agent, và các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) trên các chỉ số bàn giao và đánh giá sẽ kích hoạt khắc phục tự động. |
| 5 | Tối ưu (Optimized) | Thực hành vận hành là một hệ thống tự cải thiện, được tinh chỉnh liên tục. Các sự cố sản xuất tự động sinh ra các kịch bản kiểm thử lỗi mới, và bản mô tả công việc agent tiến hóa thông qua phát triển hướng đặc tả (spec-driven development) với các vết kiểm toán tái lập được. Điều phối đa agent sử dụng và đóng góp vào các chuẩn công nghiệp như [Model Context Protocol](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) và [giao tiếp Agent-to-Agent](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html). Các chỉ số về khả năng chịu lỗi và chỉ số kết quả kinh doanh được tương quan theo thời gian thực và trực tiếp cung cấp thông tin cho các quyết định lộ trình. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm định nghĩa agent theo những gì chúng có thể làm thay vì những gì chúng chịu trách nhiệm, khiến người vận hành không có cách rõ ràng để đánh giá agent có hoạt động đúng hay không hoặc quyết định khi nào cần leo thang.
- Các luồng công việc đa agent được lắp ráp từ dưới lên từ năng lực của từng agent riêng lẻ, không có giao thức bàn giao hay đường leo thang tới con người được tài liệu hóa, tạo ra các hệ thống khó vận hành khi một agent đơn lẻ gặp lỗi.
- Kiểm thử lỗi được xem như một giai đoạn thay vì một thực hành sống, khiến khả năng chịu lỗi âm thầm suy giảm theo mỗi thay đổi Prompt, Tools hay Model được đưa ra mà không có kiểm thử hồi quy (regression test) tương ứng.
- Tiêu chí thành công và các chỉ số chịu lỗi được theo dõi trong các silo tách rời khỏi chỉ số kinh doanh, khiến chủ sở hữu agent không thể giải thích tác động kinh doanh của một lỗi phối hợp hay của sự sụt giảm tỷ lệ vượt qua kiểm thử lỗi.
- Các tài liệu vận hành như bản mô tả công việc, runbook, và kịch bản kiểm thử lỗi được viết một lần rồi không bao giờ xem lại, khiến ý định được tài liệu hóa trôi lệch khỏi hành vi thực tế tại runtime.

###### Các thực hành tốt

- [AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent](agentops01-bp01.md)
- [AGENTOPS01-BP02 Thiết kế quy trình bàn giao đa agent với leo thang có con người trong vòng lặp](agentops01-bp02.md)
- [AGENTOPS01-BP03 Phát triển các kịch bản kiểm thử phản ánh chính xác lỗi của các thành phần phụ thuộc, giao thức điều phối và quy trình kinh doanh](agentops01-bp03.md)
