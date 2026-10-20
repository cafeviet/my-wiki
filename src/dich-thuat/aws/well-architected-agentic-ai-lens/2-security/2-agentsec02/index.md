# Bảo vệ việc sử dụng công cụ của agent

Agent tương tác với các hệ thống bên ngoài thông qua công cụ (Tools) như API, cơ sở dữ liệu, hệ thống tệp và các dịch vụ khác. Nếu không có kiểm soát phù hợp, một agent có quyền truy cập công cụ có thể bị điều hướng để thực hiện các hành động ngoài ý muốn. Việc ủy quyền (authorization), kiểm định đầu vào và quản trị công cụ làm giảm rủi ro lạm dụng công cụ và các thao tác trái phép.

| AGENTSEC02: Bạn kiểm soát và bảo vệ việc sử dụng công cụ của agent như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Mọi lần gọi công cụ được ủy quyền theo một chính sách khai báo (declarative policy) trước khi thực thi, với danh tính của agent và ngữ cảnh người dùng khởi nguồn được lan truyền qua chuỗi ủy quyền.
- Agent chỉ gọi các công cụ trong phạm vi được phê duyệt của nó, và tham số cùng phản hồi của công cụ đi qua các phép kiểm tra lược đồ và chính sách giữ các thao tác nằm trong ranh giới đã định.
- Các thao tác biến đổi (mutating) rủi ro cao dừng lại tại một điểm kiểm soát có con người trong vòng lặp (human-in-the-loop), và các giới hạn tốc độ (rate limits) chặn phạm vi tác động khi một agent rơi vào vòng lặp mất kiểm soát.
- Công cụ và các máy chủ MCP lưu trữ chúng chỉ khả dụng với agent sau khi trải qua một cuộc rà soát bảo mật có tài liệu và được đăng ký với phiên bản được ghim (pinned), phân loại dữ liệu và thời hạn rà soát.
- Việc sử dụng công cụ có thể quan sát được đầu-cuối, với các quyết định ủy quyền, thất bại kiểm định và tốc độ gọi được đưa vào các luồng công việc phát hiện và tuân thủ.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc bảo vệ sử dụng công cụ của agent như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Agent được cấp quyền truy cập tràn lan tới các công cụ có sẵn, và việc ủy quyền được ủy thác cho chính khả năng suy luận của agent. Tham số chảy tới công cụ mà không có thực thi lược đồ, các phản hồi lỗi trả về stack trace thô, địa chỉ điểm cuối nội bộ hoặc chi tiết lược đồ cơ sở dữ liệu vào ngữ cảnh của agent, và không có registry hay quản lý phiên bản nào đối với công cụ hoặc các máy chủ MCP lưu trữ chúng. Các thao tác ghi, xóa và tài chính rủi ro cao thực thi mà không có rà soát. |
| 2 | Manh nha (Emerging) | Mỗi agent chạy dưới một danh tính riêng với quyền hạn giới hạn phạm vi trên các công cụ nó cần. Kiểm định lược đồ được áp dụng trong trình xử lý công cụ cho các tham số hướng người dùng, các phản hồi lỗi được làm sạch để chi tiết nội bộ không tới được agent hay người dùng, và các thời gian chờ (timeout) cùng phân bổ bộ nhớ của [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) giới hạn chi phí thời gian chạy và thời gian thực thi của bất kỳ lần gọi công cụ đơn lẻ nào. Công cụ và các máy chủ MCP lưu trữ chúng được ghi trong một danh sách chung, nhưng việc thực thi phụ thuộc vào kỷ luật của người rà soát. |
| 3 | Được định nghĩa (Defined) | Lưu lượng agent-tới-công cụ chảy qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html), nơi tập trung hóa việc ủy quyền vào (inbound) dựa trên OAuth và xác thực ra (outbound) theo từng mục tiêu (target). Công cụ và các máy chủ MCP lưu trữ chúng được đăng ký trong một registry có quản lý phiên bản với quyền hạn có tài liệu, phân loại dữ liệu và thời hạn rà soát, và [sử dụng công cụ nghiêm ngặt (strict tool use)](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) ràng buộc các tham số do mô hình sinh phải tuân theo lược đồ công cụ tại lớp giải mã. |
| 4 | Chủ động (Proactive) | [Policy in Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-policy.html) thực thi các chính sách [Cedar](https://docs.cedarpolicy.com/) với tư thế mặc-định-từ-chối (default-deny) tại gateway, đánh giá mọi lần gọi công cụ theo các điều kiện có nhận thức về danh tính và ràng buộc tham số bên ngoài vòng lặp suy luận của agent. Các điểm kiểm soát human-in-the-loop chặn các thao tác biến đổi rủi ro cao thông qua các mẫu callback của [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html), giới hạn tốc độ chạy ở cả tầng gateway và tầng công cụ, và các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) kích hoạt khi có thất bại ủy quyền và tăng đột biến kiểm định. |
| 5 | Tối ưu (Optimized) | Các kiểm soát ủy quyền công cụ, kiểm định và registry được mã hóa thành quy tắc đầu-cuối và được kiểm chứng liên tục qua các bài tập red-team và phát hiện trôi dạt (drift) tự động bằng [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html). Các luồng công việc khấu hao (deprecation) tự động loại bỏ các công cụ hết hạn và các mục máy chủ MCP, các chính sách thích ứng từ hành vi quan sát được, và việc quản trị máy chủ MCP tập trung (bao gồm đăng ký, ghim phiên bản, kiểm soát egress mạng và khám phá dùng chung) được thực thi nhất quán trên các tài khoản. |

## Các vấn đề thường gặp cần lưu ý

- Quyền truy cập công cụ được cấp ở cấp agent nhưng chỉ được thực thi bởi khả năng suy luận của agent, nên không có gì bên ngoài mô hình giúp ngăn một prompt bị tiêm nhiễm hoặc bị đầu độc gọi các công cụ nằm ngoài phạm vi dự định của agent.
- Kiểm định lược đồ được áp dụng cho các tham số hướng người dùng nhưng không cho các tham số do mô hình sinh, dựa trên giả định rằng mô hình không thể tạo đầu ra không hợp lệ. Trên thực tế, các tham số do mô hình sinh là một bề mặt tấn công mang các payload tiêm nhiễm và các kiểu không hợp lệ.
- Registry được duy trì như tài liệu tĩnh thay vì như các kiểm soát được thực thi tại gateway hoặc tại MCP client, nên agent tiếp tục khám phá và gọi các công cụ chưa được ai rà soát.
- Các máy chủ Model Context Protocol (MCP) từ xa được áp dụng với cùng các giả định rủi ro như công cụ cục bộ, điều này đánh giá thấp mức phơi bày do kết nối mạng, xác thực bên thứ ba và xử lý dữ liệu bên ngoài gây ra.
- Giới hạn tốc độ được coi là một kiểm soát chi phí thay vì một kiểm soát bảo mật, nên một vòng lặp mất kiểm soát hoặc một prompt injection kích hoạt hàng loạt lần gọi công cụ chạy đủ lâu để ảnh hưởng đến các hệ thống phía sau trước khi những người ứng phó can thiệp.

###### Các thực hành tốt

- [AGENTSEC02-BP01 Triển khai ủy quyền công cụ](agentsec02-bp01.md)
- [AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ](agentsec02-bp02.md)
- [AGENTSEC02-BP03 Duy trì registry công cụ được phê duyệt kèm đánh giá bảo mật](agentsec02-bp03.md)
