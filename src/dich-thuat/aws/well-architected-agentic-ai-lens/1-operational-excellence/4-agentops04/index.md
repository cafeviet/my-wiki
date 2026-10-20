# Thực hành tích hợp và quản lý Tools

Các agent dựa vào các Tools và dịch vụ bên ngoài để hoàn thành công việc, và cách các tích hợp đó được quản lý quyết định liệu hành vi agent có giữ nhất quán khi kho Tools tăng trưởng hay không. Không có một registry dùng chung, các giao thức chuẩn hóa, và hành vi dự phòng chung, mỗi Tools mới thêm gánh nặng vận hành và mỗi lỗi Tools đều gây rủi ro gián đoạn agent trên diện rộng.

| AGENTOPS04: Bạn thiết lập các thực hành tích hợp và quản lý Tools như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các agent khám phá các Tools sẵn có và năng lực của chúng thông qua một catalog có thẩm quyền duy nhất thay vì các tích hợp hardcode hay kiến thức truyền miệng.
- Các Tools được tích hợp qua các giao thức chuẩn hóa như [Model Context Protocol (MCP)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/protocol-based-tools-detailed.html) và [Agent-to-Agent (A2A)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/agent-to-agent-protocols.html), để các agent liên vận hành (interoperate) qua các nhà cung cấp và qua các ranh giới nhóm.
- Các lời gọi Tools được xác thực, được ủy quyền theo đặc quyền tối thiểu (least privilege), và có thể kiểm toán đầy đủ ở tầng dịch vụ thay vì theo từng agent.
- Các lỗi Tools được khoanh vùng và định tuyến qua các chuỗi dự phòng (fallback chains) được tài liệu hóa, để một phụ thuộc suy giảm đơn lẻ không lan thành gián đoạn agent trên diện rộng.
- Kho Tools, phân bố phiên bản, và độ tin cậy theo từng Tools được giám sát tập trung, mang lại cho người vận hành tầm nhìn để tiến hóa và ngừng dùng các Tools mà không làm gián đoạn các agent phụ thuộc.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với tích hợp và quản lý Tools như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Không tồn tại registry tập trung. Các nhóm xây dựng các tích hợp agent-tới-Tools điểm-tới-điểm với giao diện của từng Tools. Xác thực, xử lý lỗi, và ghi log là theo từng Tools và không nhất quán. Một Tools suy giảm đơn lẻ thường lan thành các lỗi agent trên diện rộng vì không có kế hoạch dự phòng, và việc sử dụng Tools chỉ thấy được qua các log tùy ứng. |
| 2 | Manh nha (Emerging) | Một registry liệt kê các Tools đang dùng với chủ sở hữu và phiên bản, dù việc áp đặt còn phi chính thức. Hầu hết các Tools mới được phơi bày qua một giao thức chuẩn, thường là [MCP qua Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), thay vì như các tích hợp riêng lẻ. Các chính sách thử lại và timeout cơ bản được áp dụng theo từng Tools, và các nhóm tài liệu hóa các lỗi Tools phổ biến nhất. Ghi log kiểm toán được thu thập nhưng hiện chưa tập trung. |
| 3 | Được định nghĩa (Defined) | Các Tools được phơi bày qua [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) hoặc một registry tương đương và được các agent khám phá qua tìm kiếm ngữ nghĩa. Tích hợp dựa trên giao thức bằng MCP và [A2A trong AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html) là mặc định cho các Tools mới. Xác thực theo từng Tools, ủy quyền bằng [các chính sách Cedar trong Policy trong AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), và ghi log kiểm toán được áp đặt tập trung ở tầng dịch vụ. Các chuỗi dự phòng và ngắt [circuit-breaker](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html) tồn tại cho các Tools quan trọng nhất, và các chỉ số độ tin cậy theo từng Tools được theo dõi trong một dashboard dùng chung. |
| 4 | Chủ động (Proactive) | Registry là nguồn chân lý duy nhất cho các định nghĩa Tools, phiên bản, quyền sở hữu, và lịch trình ngừng dùng, và việc đăng ký là một cổng đối với việc sử dụng trong sản xuất. Các giao thức chuẩn hóa và các chính sách đặc quyền tối thiểu được áp đặt xuyên tổ chức, với các buổi rà soát chính sách Cedar là một phần của quy trình thay đổi. Các chuỗi dự phòng, [lùi lũy thừa và jitter (exponential backoff and jitter)](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), và các ngắt tự động được áp dụng nhất quán dựa trên một phân loại lỗi (error taxonomy) dùng chung. Telemetry của Tools được trang bị đầu-cuối qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), với các cảnh báo và runbook do các nhóm sở hữu Tools quản lý. |
| 5 | Tối ưu (Optimized) | Kho Tools được quản trị bằng policy-as-code. Các Tools mới phải vượt qua các cổng registry, giao thức, chính sách, và khả năng quan sát trước khi bất kỳ agent nào có thể gọi chúng. Các lựa chọn giao thức và chính sách được kiểm định và thắt chặt liên tục bằng phản hồi vòng kín (closed-loop) từ telemetry sản xuất. Các chuỗi dự phòng điều chỉnh tự động dựa trên độ tin cậy lịch sử, và tổ chức đóng góp các cải tiến trở lại các đặc tả giao thức mở mà nó phụ thuộc. Ngừng dùng Tools là thường lệ và rủi ro thấp. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm xây dựng các tích hợp Tools điểm-tới-điểm mà không có registry hay giao thức dùng chung, tạo ra các Tools trùng lặp và tài liệu không nhất quán mà các agent không thể khám phá hay sử dụng tin cậy qua các ranh giới nhóm.
- Các Tools được đăng ký mà không có chuẩn tài liệu hay chủ sở hữu được nêu tên, nên các agent chỉ gặp các lược đồ tham số và mã lỗi không được tài liệu hóa tại runtime.
- Ủy quyền Tools và ghi log kiểm toán được triển khai theo từng Tools thay vì tập trung, để lại các khoảng trống về việc agent nào đã gọi Tools nào và làm suy yếu các buổi rà soát tuân thủ.
- Các chính sách thử lại giống hệt nhau cho mọi Tools, nên các phụ thuộc đã lỗi vĩnh viễn hoặc bị giới hạn tốc độ bị dội bom bằng các lần thử lại mạnh mẽ trong khi các vấn đề nhất thời nhận quá ít lần thử.
- Các Tools bị ngừng dùng hoặc đánh phiên bản mà không thông báo cho các agent phụ thuộc, nên các lỗi tại runtime chỉ bộc lộ khi phiên bản cũ biến mất.

###### Các thực hành tốt

- [AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools](agentops04-bp01.md)
- [AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)](agentops04-bp02.md)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](agentops04-bp03.md)
