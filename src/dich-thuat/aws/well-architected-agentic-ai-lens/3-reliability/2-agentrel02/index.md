# Thực thi tác vụ có thể dự đoán

Các tác nhân ràng buộc tính ngẫu nhiên của LLM thông qua thiết kế tác vụ nguyên tử, quyền hạn theo nguyên tắc đặc quyền tối thiểu và các giao thức chỉ dẫn rõ ràng sẽ mang lại kết quả có thể dự đoán ngay cả khi các mô hình nền tảng phi tất định. Độ tin cậy của tác nhân vượt ra ngoài hạ tầng hỗ trợ để tới độ tin cậy của việc thực thi đúng tác vụ dự định với dữ liệu phù hợp vào đúng thời điểm.

| AGENTREL02: Làm thế nào để bạn phát triển các hệ thống tác nhân thực thi tác vụ một cách đáng tin cậy với kết quả có thể dự đoán? |
| --- |
|  |

## Mục tiêu năng lực

- Mỗi tác nhân sở hữu một năng lực nguyên tử duy nhất với kiểm tra đầu vào tường minh và một lược đồ đầu ra có cấu trúc, nhờ đó tính ngẫu nhiên của LLM bị giới hạn bởi các hợp đồng hẹp, có thể kiểm thử.
- Mỗi tác nhân vận hành trong một phong bì quyền hạn theo đặc quyền tối thiểu được thực thi ở các lớp danh tính, chính sách và kiểm soát truy cập, nhờ đó một quyết định bất ngờ của mô hình chỉ ảnh hưởng tới các hệ thống được ủy quyền tường minh cho tác nhân đó.
- Các tác nhân phát ra dữ liệu đo lường (telemetry) đặc thù cho tác nhân (prompt, lời gọi công cụ, truy cập bộ nhớ, chất lượng đầu ra) được so sánh với các đường cơ sở (baseline) hành vi, nhờ đó độ trôi (drift) và bất thường được phát hiện trước khi lan thành lỗi.
- Chỉ dẫn tới tác nhân qua các mẫu prompt chuẩn tắc, cấu hình có phiên bản và các lược đồ bàn giao (handoff) tường minh, nhờ đó việc diễn giải mục tiêu nhất quán qua các luồng công việc đơn tác nhân và đa tác nhân.
- Các hành động của tác nhân được định tuyến tới tầng giám sát của con người phù hợp dựa trên rủi ro và khả năng đảo ngược, nhờ đó các quyết định hệ trọng nhận được rà soát mà không làm tăng độ trễ cho công việc thường quy.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với thực thi tác vụ có thể dự đoán như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Các tác nhân là những bộ xử lý đa dụng với system prompt rộng và hợp đồng đầu vào–đầu ra mơ hồ. Quyền hạn ở dạng thô, ghi log chung chung và thiếu các điểm quyết định đặc thù cho tác nhân, prompt là tùy tiện và không đánh phiên bản, và mọi hành động của tác nhân đều nhận cùng một mức rà soát của con người, hoặc không có gì. |
| 2 | Manh nha (Emerging) | Các đội đã bắt đầu phân rã luồng công việc thành các tác nhân đơn mục đích và định nghĩa lược đồ đầu vào và đầu ra. Mỗi tác nhân có một vai trò thực thi IAM riêng, [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) thu thập telemetry theo từng tác nhân, và các mẫu prompt nằm trong tài liệu dùng chung. Một số hành động rủi ro cao cần con người phê duyệt, dù việc phân loại còn phi chính thức. |
| 3 | Xác lập (Defined) | Các tác nhân nguyên tử chạy trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với thực thi [đầu ra có cấu trúc (structured output)](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html) và kiểm định thường xuyên qua [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html). Truy cập bị giới hạn qua [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) và các chính sách [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) được thu hẹp theo từng tác nhân. Các đường cơ sở hành vi dẫn dắt cảnh báo qua [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html), các mẫu prompt được đánh phiên bản, và một khung rủi ro được tài liệu hóa định tuyến các hành động của tác nhân vào các tầng tự chủ (autonomous), thông báo (notify) và phê duyệt (approve). |
| 4 | Chủ động (Proactive) | Các ranh giới truy cập được thực thi qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với các chính sách [Cedar](https://docs.cedarpolicy.com/) tại gateway, và [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) chặn các đầu ra vi phạm chính sách trước khi leo thang tới người rà soát. Việc so sánh phiên bản prompt chạy qua [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trước khi di trú lưu lượng, [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) dẫn dắt việc khắc phục theo đặc quyền tối thiểu từ dữ liệu [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html), và các luồng phê duyệt mang theo timeout, đường leo thang và bối cảnh kiểm toán đầy đủ. |
| 5 | Tối ưu (Optimized) | Các hợp đồng tác vụ nguyên tử, phạm vi đặc quyền tối thiểu, đường cơ sở bất thường, thư viện prompt và các tầng giám sát được hiệu chỉnh lại liên tục từ dữ liệu quan trắc. Các phản hồi tự động cách ly (quarantine) các tác nhân bất thường, các bài kiểm thử hợp đồng đối kháng chặn các thoái lui tiêm prompt (prompt-injection) trong CI/CD, và tổ chức công bố lại các mẫu và số đo độ tin cậy của tác nhân cho các cộng đồng thực hành của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các tác nhân tích tụ trách nhiệm rộng, chồng lấn theo thời gian, nên một hiểu sai đơn lẻ có thể ảnh hưởng tới nhiều năng lực và các dạng lỗi trở nên khó tái lập hơn khi phạm vi mở rộng.
- Các vai trò thực thi IAM và ranh giới chính sách được viết với ký tự đại diện (wildcard) hoặc theo hướng tiện lợi cho lần triển khai đầu tiên, nên phạm vi ảnh hưởng của bất kỳ hành động LLM không dự đoán được nào rộng hơn chức năng hợp lệ của tác nhân.
- Giám sát bắt các tín hiệu hạ tầng nhưng không bắt các điểm quyết định đặc thù cho tác nhân, nên độ trôi hành vi (đầu ra dài hơn, nhiều lời gọi công cụ hơn, hoặc dịch chuyển trong phân bố đầu ra) là vô hình cho tới khi tạo ra một lỗi mà người dùng nhìn thấy.
- Prompt và định dạng bàn giao được từng đội viết tùy tiện, nên các tác nhân diễn giải mục tiêu không nhất quán và các luồng công việc đa tác nhân đổ vỡ khi một bên của bàn giao tiến hóa độc lập.
- Mọi hành động của tác nhân nhận cùng một mức rà soát của con người, hoặc là phê duyệt đồng nhất gây nghẽn cổ chai tự động hóa, hoặc là tự chủ đồng nhất khiến các quyết định hệ trọng được xuất xưởng mà không có giám sát.

###### Các thực hành tốt

- [AGENTREL02-BP01 Thiết kế các tác nhân cho các tác vụ cụ thể và nguyên tử](agentrel02-bp01.md)
- [AGENTREL02-BP02 Giới hạn quyền hạn của tác nhân ở mức truy cập tối thiểu cần thiết](agentrel02-bp02.md)
- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](agentrel02-bp03.md)
- [AGENTREL02-BP04 Phát triển các giao thức chỉ dẫn rõ ràng cho tác nhân](agentrel02-bp04.md)
- [AGENTREL02-BP05 Thiết lập giám sát của con người theo tầng và các luồng phê duyệt](agentrel02-bp05.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
