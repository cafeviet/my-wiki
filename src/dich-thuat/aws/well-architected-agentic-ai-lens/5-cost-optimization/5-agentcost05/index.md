# Khả năng nhìn thấy và quy gán chi phí của agent

Các tổ chức đo lường chi phí agent ở cấp chu kỳ suy luận đưa ra các quyết định tối ưu dựa trên dữ liệu vốn dồn tích khoản tiết kiệm trên toàn bộ đội agent của họ. Việc theo dõi chi phí truyền thống thất bại với các hệ thống agentic vì chi phí trải khắp các chu kỳ suy luận, các luồng đa agent, các lần gọi công cụ, và các ranh giới tenant mà việc tính hóa đơn tiêu chuẩn không nắm bắt được.

| AGENTCOST05: Làm thế nào để triển khai quy gán chi phí (cost attribution)? |
| --- |
|  |

## Mục tiêu năng lực

- Chi tiêu của agent có thể quy gán được ở cấp chu kỳ suy luận, agent, luồng công việc và tenant thay vì chỉ ở cấp tài khoản.
- Chi phí điều phối (orchestration overhead) và chi phí thực thi của worker có thể tách biệt, để các nhóm có thể biết mỗi đồng được chi ở đâu.
- Các vết chi phí (cost traces) theo mọi lần bàn giao trong các luồng đa agent, tạo ra một chi phí-thực-trên-mỗi-lần-hoàn-thành-luồng-công-việc.
- Các định danh tenant chảy qua mọi thao tác của agent, hỗ trợ tính hóa đơn theo mức tiêu thụ, phát hiện hàng xóm ồn ào (noisy-neighbor), và thực thi quota.
- Dữ liệu đo lường kỹ thuật được dịch sang các số liệu kinh doanh. Chi phí trên mỗi quyết định, chi phí trên mỗi lần hoàn thành tác vụ, và **ROI** so với các quy trình thủ công được báo cáo, và chúng có sẵn cho các bên liên quan kinh doanh qua các dashboard tự phục vụ.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với khả năng nhìn thấy và quy gán chi phí của agent nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Chi phí agent chỉ hiển thị ở cấp tài khoản AWS. Không có phân loại thẻ (tag taxonomy) tiêu chuẩn, và các báo cáo [AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html) không thể tách các agent, luồng công việc hay tenant. Các nhóm phản ứng với các cú sốc hóa đơn sau khi sự việc đã xảy ra vì thiếu quy gán theo từng agent và từng pha suy luận. |
| 2 | Nhen nhóm (Emerging) | Một phân loại thẻ tiêu chuẩn (agent-id, agent-role, workflow-id, task-type, environment) được áp dụng cho các lần gọi [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) và các phiên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html). [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) xuất các vết sang [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html), và phân bổ chi phí theo thẻ được kích hoạt trong AWS Cost Explorer. Các báo cáo theo từng agent và từng luồng công việc tồn tại, nhưng độ bao phủ không đồng đều và quy gán đa tenant còn hạn chế. |
| 3 | Xác định (Defined) | Các workflow trace ID lan truyền qua mọi lần gọi agent, lần gọi công cụ, và thao tác bộ nhớ. Các tỷ lệ chi phí điều phối, chi phí-trên-mỗi-chu-kỳ-suy-luận, và chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ được theo dõi trên các [dashboard CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html). Cảnh báo [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) và [cảnh báo CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html) thúc đẩy can thiệp kịp thời. Các định danh tenant chảy qua [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) cho các triển khai đa tenant. |
| 4 | Chủ động (Proactive) | Việc tổng hợp chi phí cuộn lên chi phí theo lần gọi, agent, luồng công việc và tenant một cách tự động. Các quota cấp tenant được thực thi qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với [các chính sách Cedar](https://docs.cedarpolicy.com/), và các cảnh báo noisy-neighbor kích hoạt khi tiêu thụ vượt quá ba lần đường cơ sở lịch sử. Các dashboard hướng-kinh-doanh trong [Amazon Quick](https://docs.aws.amazon.com/quicksuite/latest/user/welcome.html) kết hợp [AWS Cost and Usage Reports](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html) và dữ liệu đo lường quan sát để hiển thị ROI so với các quy trình thủ công. Hạ tầng thử nghiệm định tuyến lưu lượng tới các mẫu cộng tác thay thế để các quyết định kiến trúc được đưa ra với dữ liệu chi phí-chất lượng. |
| 5 | Tối ưu (Optimized) | Quy gán chi phí được tinh chỉnh liên tục và định hình các quyết định thiết kế agent của tổ chức. Việc tạo thuật kể tự động từ một model [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) nhỏ giải thích các động lực chi phí và đề xuất các tối ưu với các ước lượng tiết kiệm định lượng. Phân tích điểm hòa vốn pooled-so-với-dedicated định hướng việc bố trí tenant, các mô hình định giá theo từng tenant thích nghi với các mẫu tiêu thụ, và các đơn vị kinh doanh xem xét các thuật kể chi phí theo một nhịp hàng tháng cố định. Khả năng nhìn thấy chi phí là một đầu vào cốt lõi cho các quyết định đầu tư hàng quý thay vì một báo cáo sau khi sự việc đã xảy ra. |

## Các vấn đề thường gặp cần chú ý

- Báo cáo chi phí dừng ở cấp tài khoản AWS, nên các nhóm không thể tách chi phí điều phối của supervisor khỏi thực thi của worker hay xác định pha suy luận nào tiêu thụ token không tương xứng.
- Các phân loại thẻ tồn tại trên giấy nhưng được áp dụng không nhất quán qua các lần gọi model, các lần thực thi hàm, và các thao tác dữ liệu, vốn âm thầm phá vỡ quy gán theo từng agent và từng luồng công việc.
- Các luồng đa agent được phân tích từng agent một vì không có workflow trace ID nào lan truyền qua các lần bàn giao, tạo ra các chi phí điều phối phình lên mà không được để ý.
- Các triển khai đa tenant thiếu ngữ cảnh tenant trong các chiều số liệu và các thẻ phân bổ chi phí, vốn giúp ngăn tính hóa đơn theo mức tiêu thụ và cho phép các tenant noisy-neighbor đẩy việc scale hạ tầng cho tất cả.
- Dữ liệu chi phí nằm bên trong các dashboard kỹ thuật, nên các bên liên quan kinh doanh chỉ thấy số token thô và thời gian thực thi Lambda, và không thể dịch chi tiêu agent thành các kết quả kinh doanh hay ROI so với các quy trình thủ công.

###### Các thực hành tốt

- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](agentcost05-bp01.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](agentcost05-bp02.md)
- [AGENTCOST05-BP03 Thiết kế phân bổ chi phí nhận biết tenant cho các mô hình định giá agent as a service (AaaS)](agentcost05-bp03.md)
- [AGENTCOST05-BP04 Tạo báo cáo chargeback và ROI](agentcost05-bp04.md)
