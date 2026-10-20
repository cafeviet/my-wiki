# AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả

Các vòng lặp suy luận không giới hạn tiêu thụ token một cách khó lường và có thể dẫn đến lượng tiêu thụ token cao hơn dự kiến cho các tác vụ thường quy. Một **reflection pattern** có giới hạn cho bạn ngân sách token dự đoán được và giữ được chất lượng quyết định.

**Kết quả mong muốn:**

- Bạn có các điều kiện dừng tường minh cho mọi agent: số vòng lặp tối đa, một ngưỡng độ tin cậy, và một ngân sách token cho mỗi phiên.
- Bạn áp dụng reflection có chọn lọc, chỉ kích hoạt tự sửa lỗi đầy đủ khi chất lượng đầu ra ban đầu rơi xuống dưới một ngưỡng.
- Bạn theo dõi lượng tiêu thụ token và chất lượng quyết định theo từng chu kỳ để các tham số dừng có thể được tinh chỉnh từ dữ liệu thay vì phỏng đoán.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy agent mà không có giới hạn số vòng lặp hoặc trần chi phí, cho phép tiêu thụ token vô hạn mà không tiến triển hướng tới tác vụ.
- Áp dụng reflection và tự sửa lỗi đắt đỏ cho mọi đầu ra, bất kể câu trả lời ban đầu đã tốt hay chưa.
- Vận hành mà không có đo lường token theo từng chu kỳ, nên không ai biết được pha suy luận nào đang đẩy chi phí lên.
- Dùng số vòng lặp cố định thay vì ngưỡng độ tin cậy, dẫn đến hoặc lãng phí token cho những vòng lặp không cần thiết hoặc cắt cụt suy luận phức tạp quá sớm.
- Xây dựng reflection pattern mà không có lan can (guardrail) ngân sách, nên các vòng lặp không giới hạn tiêu thụ token trước khi cảnh báo được kích hoạt.

**Lợi ích khi áp dụng thực hành tốt này:**

- Lượng tiêu thụ token dự đoán được nhờ các chu kỳ suy luận có giới hạn với điều kiện dừng tường minh.
- Reflection chọn lọc giữ được chất lượng quyết định cho các trường hợp mơ hồ trong khi giảm lãng phí token cho các tác vụ đơn giản.
- Các đường cơ sở chi phí-chất lượng cho thấy mẫu suy luận nào mang lại sự đánh đổi tốt nhất, cho phép tinh chỉnh ngưỡng dựa trên dữ liệu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Mỗi vòng lặp reflection giả định rằng một lần lặp nữa sẽ cải thiện câu trả lời nhiều hơn chi phí nó gây ra, điều đó đúng với các tác vụ mơ hồ nhưng thường mất giá trị với các tác vụ đơn giản. Không có hợp đồng đó, các agent sẽ reflection trên mọi đầu ra bất kể reflection có cải thiện chất lượng hay không. Kỷ luật ở đây là phát ra một tín hiệu độ tin cậy có cấu trúc kèm theo mỗi hành động, kiểm tra nó ở tầng điều phối, và cắt ngắn vòng lặp khi độ tin cậy vượt qua một ngưỡng. Nếu không, vòng lặp sẽ chạy cho đến khi chạm trần cứng về số vòng lặp, vốn là kết cục vừa chậm nhất vừa đắt nhất cho trường hợp phổ biến.

Việc thực thi quan trọng ngang bằng với hợp đồng. Trần số vòng lặp chỉ được diễn đạt trong system prompt có thể trôi qua ngưỡng dưới các đầu vào đối kháng hoặc prompt injection. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) áp dụng các chính sách Cedar tại ranh giới [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), nên giới hạn số vòng lặp và token bị từ chối tại tầng lưu lượng thay vì bị phát hiện sau khi đã vượt quá. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cung cấp thực thi cách ly theo phiên và giá theo mức tiêu thụ, nên mỗi phiên mang ngân sách riêng và một phiên chạy hoang không làm hỏng kế toán của các phiên khác.

Reflection chọn lọc tách việc xử lý sự mơ hồ khỏi công việc thường quy rẻ hơn. Chấm điểm đầu ra ban đầu theo một rubric nhẹ, một model nhỏ hoặc một heuristic, và cổng (gate) reflection đầy đủ dựa trên điểm số đó. Gắn thẻ kết quả reflection với loại tác vụ để bạn có thể thấy nơi nào reflection liên tục cải thiện chất lượng và nơi nào nó chỉ thêm chi phí mà không có lợi ích. Các loại không bao giờ hưởng lợi từ reflection nên tắt hẳn trigger. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) hỗ trợ đánh giá chất lượng quyết định theo kiểu LLM-as-a-Judge, cung cấp cho bạn một tín hiệu độ tin cậy khách quan thay vì tín hiệu tự báo cáo từ chính agent đang được đánh giá.

Các pha plan, execute, verify và reflect trong một chu kỳ reflection có cường độ suy luận khác nhau. Định tuyến planning và verification tới các model nhỏ hơn, nhanh hơn trong khi giữ model lớn nhất cho execution sẽ thu được khoản tiết kiệm tích lũy trên các pha chi phí thấp thường xuyên, bù đắp cho chi phí trên mỗi token cao hơn của pha cường độ cao ít xảy ra.

### Các bước triển khai

- **Định nghĩa các điều kiện dừng tường minh cho mỗi agent:** Đặt số vòng lặp tối đa, một ngưỡng độ tin cậy, và một ngân sách token cho mỗi phiên, và thực thi chúng qua các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) tại ranh giới AgentCore Gateway để việc thực thi diễn ra ở tầng lưu lượng thay vì trong mã ứng dụng.
- **Đo lường lượng tiêu thụ token theo từng chu kỳ:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập số token theo từng phiên qua OpenTelemetry, và cấu hình cảnh báo Amazon CloudWatch trên các mẫu bất thường theo chu kỳ.
- **Thiết lập các ngưỡng độ tin cậy khách quan:** Cấu hình [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để chấm điểm chất lượng quyết định theo LLM-as-a-Judge, và neo các ngưỡng dừng sớm vào chất lượng đo được thay vì độ tin cậy tự báo cáo.
- **Cổng reflection dựa trên chất lượng đầu ra ban đầu:** Chấm điểm mỗi đầu ra ban đầu bằng một rubric nhẹ và chỉ kích hoạt lượt reflection đầy đủ khi điểm số rơi xuống dưới một ngưỡng có thể cấu hình, giữ chi phí reflection tránh khỏi các trường hợp đơn giản.
- **Hiệu chỉnh lại ngưỡng theo nhịp:** Xem xét các đường cơ sở chi phí-chất lượng hàng tháng (hoặc hàng quý với các workload ổn định) và điều chỉnh ngưỡng độ tin cậy, giới hạn số vòng lặp và trigger reflection dựa trên phân phối kết quả quan sát được.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](agentcost01-bp02.md)
- [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](agentcost01-bp03.md)
- [AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng](../2-agentcost02/agentcost02-bp01.md)
- [AGENTCOST07-BP01 Triển khai kiểm soát chi phí tự động với các điểm cắt thông minh](../7-agentcost07/agentcost07-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Evaluate models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)
- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)
- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore - Evaluations](https://catalog.workshops.aws/agentcore-deep-dive/en-US/80-agentcore-evaluations)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
