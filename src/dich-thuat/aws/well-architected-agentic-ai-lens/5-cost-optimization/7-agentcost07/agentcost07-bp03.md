# AGENTCOST07-BP03 Tạo các vòng lặp phản hồi tối ưu có hệ thống để cải thiện liên tục

Các dự án tối ưu một lần có thể bỏ lỡ các lợi ích dồn tích, khi các đặc tính chi phí-hiệu năng của các hệ thống agent dịch chuyển theo thời gian khi các prompt thay đổi, các công cụ tiến hóa, và các mẫu lưu lượng trôi dạt. Một nhịp xem xét hàng tháng, các thay đổi được A/B-test, và các cổng chi phí trong pipeline triển khai biến tối ưu thành một thực hành liên tục có thể theo kịp hệ thống.

**Kết quả mong muốn:**

- Bạn tổ chức các đợt xem xét tối ưu chi phí hàng tháng theo một chương trình nghị sự có cấu trúc.
- Bạn A/B test các thay đổi có tác động chi phí thông qua định tuyến lưu lượng có kiểm soát trước khi thăng cấp toàn đội.
- Bạn tính các tỷ lệ hiệu quả chi phí-chất lượng để ưu tiên các tối ưu theo giá trị kinh doanh.
- Bạn có các cổng chi phí trong các pipeline triển khai giúp ngăn các hồi quy vô tình.

**Các phản mẫu thường gặp (anti-patterns):**

- Cắt giảm chi phí mà không đo lường tác động chất lượng, làm suy giảm hiệu năng agent và làm hỏng giá trị kinh doanh.
- Coi tối ưu chi phí là một sáng kiến thỉnh thoảng mà không có nhịp thường xuyên, cho phép các sự kém hiệu quả tích lũy.
- Thăng cấp các tối ưu trên toàn bộ đội mà không có A/B testing, phơi bày tất cả người dùng trước sự suy giảm chất lượng tiềm tàng.
- Theo dõi chi phí mà không tương quan chúng với các kết quả kinh doanh hoặc đặt các mục tiêu cải thiện định lượng, làm giảm khả năng ưu tiên dựa trên dữ liệu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các chu kỳ xem xét có hệ thống liên tục xác định các cơ hội tối ưu có tác động cao với trách nhiệm giải trình về tiến độ.
- A/B testing xác thực các giả thuyết tối ưu trước khi triển khai, giúp ngăn các sai lầm tốn kém từ các thay đổi chưa kiểm thử.
- Các cổng chi phí trong các pipeline triển khai chặn các thay đổi làm tăng chi phí mà không có cải thiện năng lực tương ứng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các đợt xem xét hàng tháng thúc đẩy tối ưu liên tục. Cấu trúc nó với bốn phần:

- Các xu hướng hiệu quả chi phí (chi phí trên mỗi quyết định, chi phí trên mỗi lần hoàn thành tác vụ theo các mục tiêu)
- Các cơ hội tối ưu hàng đầu được xếp hạng theo tác động và công sức
- Các kết quả thử nghiệm từ tháng trước
- Lập kế hoạch tháng tiếp theo

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp tracing chi tiết có thể làm lộ các cơ hội vô hình trong các số liệu tổng hợp. Tracing của AgentCore Runtime phân rã chi tiêu theo mẫu suy luận, lần gọi công cụ, và thao tác bộ nhớ, nên bạn có thể thấy nơi nào cần hành động thay vì chỉ biết rằng cần hành động. Đặt các mục tiêu cải thiện hàng quý và theo dõi tiến độ trong các dashboard Amazon CloudWatch và AWS Cost Explorer.

A/B testing là then chốt cho các tối ưu liên tục. Dùng [Amazon Bedrock agent alias routing](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-manage.html) để chia lưu lượng giữa các cấu hình đối chứng (control) và can thiệp (treatment). Với mỗi thử nghiệm, định nghĩa một giả thuyết, các số liệu thành công bao phủ cả chi phí và chất lượng, và một thời gian quan sát tối thiểu cho ý nghĩa thống kê. Với các workload agent nơi chất lượng hoàn thành tác vụ biến thiên nhiều hơn so với các mẫu request-response truyền thống, hãy lập kế hoạch cho ít nhất một quan sát 1 tuần, một phân chia lưu lượng 10%, và ít nhất 1.000 lần hoàn thành tác vụ trước khi kết luận một kết quả. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy các đánh giá chất lượng chuẩn hóa trước và sau mỗi tối ưu để việc giảm chi phí không đi kèm một hồi quy chất lượng.

Ưu tiên hóa cần một khung quyết định. Tính một tỷ lệ hiệu quả chi phí-chất lượng như phần trăm giảm chi phí chia cho phần trăm suy giảm chất lượng. Các tỷ lệ trên 10 cho thấy các cơ hội mạnh nơi hầu hết chất lượng được bảo tồn trên mỗi đồng tiết kiệm, và các tỷ lệ dưới 2 báo hiệu rằng sự suy giảm chất lượng quá lớn so với khoản tiết kiệm chi phí và nên được giảm ưu tiên. Khung này cho phép những người xem xét xếp hạng các tối ưu ứng viên một cách nhất quán so với nhau.

Các tính năng phân bổ chi phí của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) xác định các chi phí do bộ nhớ điều khiển vốn nên đưa vào các thay đổi chính sách lưu giữ. Khi mở rộng các năng lực công cụ agent qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), hãy đo tần suất gọi công cụ và chi phí suy luận trước khi thăng cấp thay vì sau. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cung cấp các ràng buộc tất định nếu phân tích chi phí cho thấy các agent gọi quá mức các công cụ đắt tiền. Các cổng chi phí trong pipeline CI/CD so sánh chi phí-trên-mỗi-tác-vụ ước lượng với phiên bản hiện tại và chặn triển khai khi mức tăng vượt ngưỡng mà không có cải thiện năng lực tương ứng.

### Các bước triển khai

- **Chạy một đợt xem xét tối ưu hàng tháng:** Dùng các dashboard Amazon CloudWatch và AWS Cost Explorer để trực quan hóa xu hướng, với một chương trình nghị sự có cấu trúc bao phủ các xu hướng hiệu quả, các cơ hội, các kết quả thử nghiệm, và các kế hoạch tháng tiếp theo.
- **A/B test các thay đổi có tác động chi phí:** Dùng [Amazon Bedrock agent alias routing](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-manage.html) với các giả thuyết và tiêu chí thành công đã định bao phủ cả chi phí và chất lượng. Cấu hình các phân chia lưu lượng 10%, các thời gian quan sát tối thiểu 1 tuần, và các mức tối thiểu 1.000 lần hoàn thành tác vụ cho ý nghĩa thống kê.
- **Ưu tiên với các tỷ lệ chi phí-chất lượng:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để đo các đánh đổi chi phí-chất lượng và tính các tỷ lệ hiệu quả. Nhắm các tỷ lệ trên 10 cho các cơ hội mạnh và giảm ưu tiên các tỷ lệ dưới 2.
- **Phân tích chi phí pha và bộ nhớ:** Dùng tracing Runtime của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để xác định các mẫu chi phí suy luận theo từng pha, và phân bổ chi phí của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) để tinh chỉnh các chính sách lưu giữ.
- **Đánh giá chi phí mở rộng công cụ trước khi thăng cấp:** Khi thêm các năng lực qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), hãy đo tần suất gọi công cụ và chi phí suy luận trước khi thăng cấp, và dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để ràng buộc việc dùng công cụ đắt tiền.
- **Thêm các cổng chi phí vào CI/CD:** Chặn các triển khai vượt quá các ngưỡng tăng chi phí mà không có cải thiện năng lực tương ứng.
- **Đặt các mục tiêu cải thiện hàng quý:** Theo dõi tiến độ theo các mục tiêu trong đợt xem xét hàng tháng để tối ưu là đo lường được, không phải khát vọng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](../2-agentcost02/agentcost02-bp02.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)
- [AGENTCOST05-BP04 Tạo báo cáo chargeback và ROI](../5-agentcost05/agentcost05-bp04.md)
- [AGENTCOST07-BP01 Triển khai kiểm soát chi phí tự động với các điểm cắt thông minh](agentcost07-bp01.md)
- [AGENTCOST07-BP02 Thiết lập phát hiện bất thường chủ động cho các mẫu chi phí của agent](agentcost07-bp02.md)

**Tài liệu liên quan:**

- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Effective cost optimization strategies for Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- [Operationalizing agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Observability tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
