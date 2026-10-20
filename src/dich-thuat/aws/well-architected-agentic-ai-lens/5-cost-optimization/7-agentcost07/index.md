# Quản trị chi phí agent và tối ưu liên tục

Các tổ chức triển khai các kiểm soát chi phí phân lớp (bao gồm thực thi ngân sách, phát hiện bất thường, và các đợt xem xét tối ưu có hệ thống) có thể triển khai các agent tự chủ với chi tiêu bị giới hạn ở nhiều tầng. Các agent tự chủ có thể tạo ra các mẫu chi phí khó lường mà các kiểm soát ngân sách truyền thống không xử lý tốt.

| AGENTCOST07: Làm thế nào để thiết lập quản trị chi phí agent và tối ưu liên tục? |
| --- |
|  |

## Mục tiêu năng lực

- Chi tiêu của agent bị giới hạn ở nhiều tầng, bao gồm các ngân sách theo chu kỳ, theo tác vụ, và theo ngày, với các điểm cắt tự động dừng suy luận chạy hoang và gọi công cụ trước khi chi phí đáng kể phát sinh.
- Các mẫu leo thang chi phí đặc thù theo agent như các cú tăng đột biến token vòng lặp suy luận, các cơn bão gọi công cụ, và tăng trưởng bộ nhớ được phát hiện trong vòng vài phút sau khi xảy ra, thay vì vài ngày sau qua dữ liệu tính hóa đơn.
- Quản trị chi phí bảo tồn quyền tự chủ của agent bằng cách dùng throttling phân cấp và các quy trình phê duyệt thay vì tắt máy nhị phân, để các agent tiếp tục hoàn thành các tác vụ dưới áp lực với thông lượng giảm.
- Tối ưu chi phí là một thực hành tổ chức liên tục, với các đợt xem xét hàng tháng, các thay đổi được A/B-test, và phân tích đánh đổi chi phí-chất lượng định lượng đưa vào các mục tiêu cải thiện hàng quý.
- Các tín hiệu chi phí được dịch thành giá trị kinh doanh, với chi phí trên mỗi quyết định, chi phí trên mỗi lần hoàn thành tác vụ, và lợi tức đầu tư được báo cáo cùng với chi tiêu để các quyết định đầu tư được đặt nền trên các kết quả thay vì chi tiêu thô.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc quản trị chi phí agent và tối ưu liên tục nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Quản trị chi phí agent không chính thức và phản ứng. Các agent được triển khai mà không có giới hạn ngân sách theo từng agent hay các điểm cắt tự động, và các khoản vượt chi được phát hiện qua các hóa đơn hàng tháng thay vì các tín hiệu thời gian thực. Phát hiện bất thường dựa vào giám sát hạ tầng chung vốn bỏ lỡ các chế độ lỗi đặc thù theo agent, và không có nhịp xem xét thường trực nào cho tối ưu chi phí. |
| 2 | Nhen nhóm (Emerging) | Các ngân sách cấp tài khoản và các cảnh báo cơ bản được thiết lập qua [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html), và một tập nhỏ các giới hạn ngân sách cấp agent tồn tại cho các agent chi tiêu cao nhất. Dữ liệu đo lường cơ sở được thu thập qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) gắn cờ các sai lệch tính hóa đơn thô. Tối ưu chi phí diễn ra như các dự án ad-hoc được kích hoạt bởi các khoản vượt chi thay vì theo một nhịp thường xuyên. |
| 3 | Xác định (Defined) | Các giới hạn ngân sách phân cấp (theo chu kỳ, theo tác vụ, theo ngày) và các điểm cắt tự động về số vòng lặp và token được thực thi một cách tất định qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) và [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html). [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) vận hành trên các số liệu AgentCore Observability với các ngưỡng 2σ và 3σ, và các bộ phát hiện tùy chỉnh bắt các cú tăng đột biến vòng lặp suy luận và các cơn bão gọi công cụ. Một đợt xem xét tối ưu chi phí hàng tháng chạy theo một chương trình nghị sự tiêu chuẩn, và các runbook điều tra được thiết lập cho các loại bất thường phổ biến. |
| 4 | Chủ động (Proactive) | Quản trị chi phí là chủ động và tích hợp với việc giao hàng. Throttling phân cấp bảo tồn chức năng agent dưới áp lực, và các quy trình phê duyệt cổng các thay đổi năng lực có tác động chi phí. A/B testing qua [Amazon Bedrock agent alias routing](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-alias.html) xác thực các tối ưu trước khi thăng cấp, và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) định lượng các đánh đổi chi phí-chất lượng. Các cổng chi phí trong pipeline CI/CD chặn các hồi quy, và các mục tiêu cải thiện hàng quý được theo dõi theo chi phí trên mỗi quyết định và chi phí trên mỗi lần hoàn thành tác vụ. |
| 5 | Tối ưu (Optimized) | Quản trị chi phí được mã hóa, được xác thực liên tục, và tự điều chỉnh. Các chính sách ngân sách, các điểm cắt, và throttling phân cấp được thực thi dưới dạng mã, và các ngưỡng bất thường được làm mới tự động từ các đường cơ sở cuộn. Các vòng lặp phản hồi tối ưu chạy liên tục, với các A/B test, các tỷ lệ hiệu quả chi phí-chất lượng, và các runbook đưa ngược trở lại vào thiết kế agent để các chế độ lỗi tái diễn được thiết kế loại bỏ. Chi phí, chất lượng, và các kết quả kinh doanh được báo cáo cùng nhau, và tổ chức chia sẻ các mẫu kỹ thuật chi phí ra bên ngoài và đóng góp vào thực hành ngành. |

## Các vấn đề thường gặp cần chú ý

- Các agent được triển khai lên production mà không có giới hạn ngân sách theo từng agent hay các điểm cắt tự động về số vòng lặp và token, để lại các vòng lặp suy luận chạy hoang và các cơn bão gọi công cụ như một chế độ lỗi chi phí chính.
- Các kiểm soát chi phí được coi là loại trừ lẫn nhau với quyền tự chủ của agent, nên các nhóm hoặc cấp quyền chi tiêu không giới hạn hoặc hạn chế các agent nặng nề đến mức việc hoàn thành tác vụ chịu ảnh hưởng.
- Phát hiện bất thường được cấu hình trên các số liệu hạ tầng chung thay vì trên các tín hiệu đặc thù theo agent như tiêu thụ token theo từng phiên, tần suất gọi công cụ, và tăng trưởng bộ nhớ, vốn cho phép leo thang do agent điều khiển ẩn trong nhiễu tổng hợp.
- Các bất thường được phát hiện nhưng không được định tuyến. Các nhóm phản ứng với mọi cảnh báo theo cùng một cách, và công việc chẩn đoán ad-hoc làm chậm việc giải quyết vì không có các runbook phân biệt các cú tăng đột biến vòng lặp suy luận, các cơn bão công cụ, và tăng trưởng bộ nhớ.
- Tối ưu chi phí được chạy như một sáng kiến thỉnh thoảng thay vì một thực hành liên tục, nên các sự kém hiệu quả tích lũy giữa các dự án và các tối ưu được thăng cấp toàn đội mà không có A/B testing hay phân tích đánh đổi chi phí-chất lượng.

###### Các thực hành tốt

- [AGENTCOST07-BP01 Triển khai kiểm soát chi phí tự động với các điểm cắt thông minh](agentcost07-bp01.md)
- [AGENTCOST07-BP02 Thiết lập phát hiện bất thường chủ động cho các mẫu chi phí của agent](agentcost07-bp02.md)
- [AGENTCOST07-BP03 Tạo các vòng lặp phản hồi tối ưu có hệ thống để cải thiện liên tục](agentcost07-bp03.md)
