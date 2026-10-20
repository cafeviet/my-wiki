# Tối ưu chi phí suy luận và thực thi

Các nhóm thiết kế các mẫu suy luận (reasoning) có ý thức về chi phí ngay từ đầu có thể đạt được ngân sách token dự đoán được và tránh được sự tăng trưởng chi phí thường xuất hiện trong các dự án agentic sau khi ra mắt. Các chu kỳ suy luận của agent tiêu thụ token qua các vòng lặp lặp đi lặp lại plan-execute-verify-reflect, và sự phối hợp đa agent làm tăng chi phí theo cấp số nhân. Khác với các ứng dụng truyền thống nơi chi phí tính toán là dự đoán được, các hệ thống agentic có thể tích lũy chi phí trong các vòng lặp suy luận kéo dài hoặc trong các mẫu giao tiếp agent-với-agent kém hiệu quả.

| AGENTCOST01: Làm thế nào để tối ưu chi phí suy luận và thực thi của agent? |
| --- |
|  |

## Mục tiêu năng lực

- Các chu kỳ suy luận của agent bị giới hạn bởi các điều kiện dừng tường minh và các lối thoát dựa trên độ tin cậy (confidence), nên lượng tiêu thụ token là dự đoán được và tỷ lệ với độ phức tạp của quyết định.
- Sự phối hợp đa agent mở rộng theo độ phức tạp của tác vụ chứ không theo độ dài hội thoại, bởi vì chỉ có ngữ cảnh tối thiểu cần thiết cho mỗi lần bàn giao (handoff) mới được truyền giữa các agent.
- Các cơ chế điều phối được khớp với mức độ tất định (determinism) của từng quyết định định tuyến, nên các lần gọi model đắt tiền chỉ được dùng ở nơi thực sự cần hiểu ngôn ngữ tự nhiên.
- Các cấp bậc agent (hierarchies) nông nhất mà luồng công việc cho phép, với các worker tự chủ hoàn thành các tác vụ con nhiều bước mà không cần supervisor kiểm tra ở từng bước.
- Chi phí suy luận và phối hợp được đo lường như các số liệu riêng biệt, quan sát được, và các đường cơ sở (baseline) chi phí-chất lượng đưa vào việc tinh chỉnh liên tục các ngưỡng, manifest và mẫu ủy quyền (delegation).

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc tối ưu chi phí suy luận và thực thi nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các agent chạy mà không có hợp đồng dừng tường minh. Các vòng lặp suy luận cứ tiếp tục cho đến khi tình cờ thoát ra hoặc hết thời gian. Các luồng đa agent truyền toàn bộ lịch sử hội thoại ở mỗi lần bàn giao, và chi phí điều phối không được tách khỏi chi phí worker. Việc sử dụng token chỉ được xem xét sau một hóa đơn bất ngờ hoặc một sự cố production. |
| 2 | Nhen nhóm (Emerging) | Các nhóm đã áp dụng các hợp đồng dừng cơ bản, bao gồm trần số vòng lặp và ngân sách token ở cấp phiên, và gắn thẻ các lần gọi để chi phí điều phối và chi phí worker có thể được báo cáo riêng. Ngữ cảnh dùng chung cho các agent cộng tác đang bắt đầu thay thế việc chuyển tiếp ngữ cảnh theo từng lần gọi, nhưng chưa phải là mặc định. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) được bật cho hầu hết các agent production, và việc xem xét thủ công chi phí suy luận diễn ra theo các khoảng thời gian đều đặn. |
| 3 | Xác định (Defined) | Có các đường cơ sở chi phí-chất lượng cho từng pha suy luận. Reflection chọn lọc được sử dụng để tự sửa lỗi đầy đủ chỉ chạy khi chất lượng đầu ra ban đầu rơi xuống dưới một ngưỡng. Các lần bàn giao tuân theo lược đồ payload có cấu trúc, và bộ nhớ dùng chung qua [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) là mặc định cho các agent cộng tác. Tỷ lệ token điều phối trên thực thi được theo dõi cho từng luồng công việc, và các nhóm chọn giám sát bằng AI thay vì định tuyến theo luật chỉ sau khi phân tích tính tất định. |
| 4 | Chủ động (Proactive) | Các điều kiện dừng, giới hạn số vòng lặp và chính sách định tuyến được thực thi tại ranh giới control-plane qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) và [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) thay vì dựa vào sự tự kiềm chế của agent. Các mẫu hybrid supervisor chạy trong production, và plan-then-execute là mặc định cho các luồng công việc lặp lại. Việc quy gán chi phí theo tầng được tự động hóa, với cảnh báo [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) trên tỷ lệ điều phối-trên-thực thi và tỷ lệ supervisor-trên-worker. Hiệu quả gọi công cụ được đánh giá trong CI/CD qua [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html). |
| 5 | Tối ưu (Optimized) | Các tham số dừng, nén manifest và độ sâu ủy quyền được hiệu chỉnh lại liên tục từ dữ liệu quan sát thay vì qua các chu kỳ xem xét thủ công. Các mô hình chi phí suy luận và các mục tiêu tỷ lệ supervisor-trên-worker định hướng việc xem xét thiết kế cho mọi luồng công việc mới. Kiến trúc agent tiến hóa chủ yếu để đáp ứng với dữ liệu đo lường chi phí-chất lượng, và tổ chức đóng góp các mẫu và số đo chi phí suy luận trở lại cho các cộng đồng thực hành của mình. |

## Các vấn đề thường gặp cần chú ý

- Các nhóm chạy agent mà không có trần số vòng lặp, ngưỡng độ tin cậy hay ngân sách token tường minh, có thể khiến các vòng lặp suy luận không giới hạn không bị phát hiện cho đến khi xem xét số liệu chi phí hoặc dữ liệu hiệu năng.
- Các luồng đa agent truyền toàn bộ lịch sử hội thoại giữa các agent ở mỗi lần bàn giao, nên chi phí phối hợp mở rộng theo độ dài hội thoại chứ không theo độ phức tạp của tác vụ.
- Các quyết định định tuyến mặc định dùng giám sát bằng AI ngay cả ở nơi một luật đơn giản hoặc một bộ phân loại nhẹ đã đủ, làm phồng chi phí điều phối tại mọi điểm quyết định trong luồng công việc.
- Các cấp bậc agent sâu hơn mức luồng công việc cần, nhân số lần gọi model tại mỗi tầng ủy quyền và tổng hợp mà không tăng chất lượng quyết định.
- Chi phí luồng công việc tổng hợp là số liệu duy nhất được dùng, nên chi phí điều phối và các tỷ lệ chi phí theo tầng vẫn vô hình cho đến khi chúng đã không còn tương xứng với giá trị thực thi.

###### Các thực hành tốt

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](agentcost01-bp01.md)
- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](agentcost01-bp02.md)
- [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](agentcost01-bp03.md)
- [AGENTCOST01-BP04 Thiết kế các cấp bậc agent và mẫu ủy quyền giảm chi phí phối hợp](agentcost01-bp04.md)
