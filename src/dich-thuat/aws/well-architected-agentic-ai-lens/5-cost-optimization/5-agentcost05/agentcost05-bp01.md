# AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent

Việc tính hóa đơn ở cấp tài khoản cho thấy một đội agent tốn bao nhiêu, nhưng nó không cho thấy các chi phí cụ thể đến từ đâu. Theo dõi chi tiết theo agent, luồng công việc và pha suy luận cung cấp chi tiết có thể truy vết về chi tiêu của bạn, vốn biến các chi phí mờ đục thành đầu vào cho tối ưu có mục tiêu.

**Kết quả mong muốn:**

- Bạn có một phân loại thẻ (tag taxonomy) tiêu chuẩn được áp dụng nhất quán qua tất cả các lần gọi agent.
- Bạn theo dõi lượng tiêu thụ token theo từng pha (planning, execution, reflection và verification) riêng biệt.
- Bạn giám sát chi phí gọi công cụ riêng biệt với chi phí suy luận của model.
- Bạn tính chi phí trên mỗi quyết định, chi phí trên mỗi chu kỳ suy luận, và chi phí trên mỗi lần hoàn thành tác vụ như các số liệu agent chính.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ theo dõi việc tính hóa đơn AWS ở cấp tài khoản mà không quy gán theo từng agent hay từng luồng công việc, làm giảm khả năng nhận diện các động lực chi phí.
- Triển khai các agent mà không gắn thẻ tài nguyên nhất quán qua các lần gọi model, các lần thực thi hàm và các thao tác dữ liệu.
- Giám sát tổng chi phí agent mà không phân biệt giữa chi phí điều phối của supervisor, thực thi của worker và các pha suy luận riêng lẻ.
- Chỉ giám sát chi phí hạ tầng mà không tính chi phí trên mỗi lần hoàn thành tác vụ tự chủ, làm giảm khả năng đánh giá kinh tế về hiệu quả của agent.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các số liệu đặc thù theo agent xác định các bất thường chi phí và cho phép so sánh hiệu năng agent xuyên đội.
- Theo dõi token theo từng pha làm lộ pha suy luận nào tiêu thụ token không tương xứng, cho phép tối ưu có mục tiêu.
- Các số liệu liên quan kinh doanh như chi phí trên mỗi lần hoàn thành tác vụ cho phép đánh giá kinh tế về các chiến lược suy luận khác nhau.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Nền tảng của khả năng nhìn thấy chi phí agent là một phân loại thẻ được áp dụng nhất quán ở mọi nơi chi tiêu diễn ra, như:

- agent-id
- agent-role (như supervisor, worker, và specialist)
- workflow-id
- task-type
- Environment trên mọi lần gọi [Amazon Bedrock](https://aws.amazon.com/bedrock/) và phiên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)

Các thẻ này là khóa chính cho mọi quy gán chi phí về sau. Kích hoạt phân bổ chi phí theo thẻ trong AWS Cost Explorer tạo ra các báo cáo theo từng agent và từng luồng công việc mà không cần công việc pipeline tùy chỉnh, nên ngay khi việc gắn thẻ nhất quán, các báo cáo trở nên dùng được.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) phân rã việc thực thi của agent thành các thao tác riêng lẻ với số token và độ trễ thông qua tracing phân tán. Theo dõi theo từng pha trở nên khả thi vì bạn có thể quy gán token cho planning, execution, reflection và verification mà không cần đo lường thủ công. Giá theo mức tiêu thụ và cách ly phiên microVM của AgentCore Runtime giữ các ranh giới chi phí căn chỉnh với các ranh giới thực thi, nên dữ liệu đo lường và việc tính hóa đơn thấy cùng một đơn vị công việc.

Một yêu cầu người dùng đơn lẻ kích hoạt nhiều agent, mỗi agent thực hiện nhiều lần gọi model, lần gọi công cụ, và thao tác bộ nhớ, nên chi phí lần gọi thô phải cuộn lên qua một cấp bậc để hữu ích. Mẫu tổng hợp là:

- Thu thập chi phí theo từng lần gọi từ các phản hồi API của Amazon Bedrock
- Liên kết chúng với agent cha bằng các thẻ phiên
- Cuộn chi phí agent vào tổng luồng công việc bằng workflow-id
- Quy gán chi phí luồng công việc cho các tenant với các triển khai đa tenant

Khi việc tổng hợp đã sẵn sàng, các báo cáo chi phí hoạt động ở mọi cấp: cấp lần gọi cho tối ưu, cấp agent cho so sánh hiệu năng, cấp luồng công việc cho biện minh kinh doanh, và cấp tenant cho tính hóa đơn.

Xuất bản số token theo từng pha như các số liệu tùy chỉnh của Amazon CloudWatch cho phép bạn xây dựng các dashboard cho chi phí trên mỗi quyết định, chi phí trên mỗi chu kỳ suy luận, và chi phí trên mỗi lần hoàn thành tác vụ được phân đoạn theo loại agent. Các cảnh báo CloudWatch trên các ngưỡng chi phí trên mỗi lần hoàn thành tác vụ và các cảnh báo AWS Budgets cho các giới hạn chi tiêu hàng tháng theo từng agent biến việc theo dõi từ một báo cáo thụ động thành một tín hiệu chủ động cho biết nhóm khi kinh tế của một agent đã thay đổi.

### Các bước triển khai

- **Định nghĩa và áp dụng một phân loại thẻ tiêu chuẩn:** Áp dụng các thẻ agent-id, agent-role, workflow-id, task-type và environment một cách nhất quán cho mọi lần gọi [Amazon Bedrock](https://aws.amazon.com/bedrock/) và phiên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), và bật phân bổ chi phí theo thẻ của AWS Cost Explorer.
- **Bật các vết chi phí đầu-cuối:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập các vết phân tán, và xuất dữ liệu đo lường sang Amazon CloudWatch để phân tích chi phí theo từng thao tác.
- **Tổng hợp chi phí theo cấp bậc:** Triển khai một hàm Lambda chạy mỗi 15 phút để thu thập chi phí suy luận model, gọi công cụ và bộ nhớ, lưu các kết quả tổng hợp theo agent và phiên trong một bảng theo dõi chi phí DynamoDB với các lần cuộn từ lần gọi lên agent lên luồng công việc lên tenant.
- **Xây dựng các dashboard chi phí trên mỗi tác vụ:** Tạo các dashboard CloudWatch hiển thị chi phí trên mỗi quyết định, chi phí trên mỗi chu kỳ suy luận, và chi phí trên mỗi lần hoàn thành tác vụ theo loại agent.
- **Cấu hình các cảnh báo và ngân sách:** Đặt các cảnh báo AWS Budgets cho các giới hạn chi tiêu hàng tháng theo từng agent và các cảnh báo CloudWatch cho các ngưỡng chi phí trên mỗi lần hoàn thành tác vụ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](agentcost05-bp02.md)
- [AGENTCOST05-BP03 Thiết kế phân bổ chi phí nhận biết tenant cho các mô hình định giá AaaS](agentcost05-bp03.md)
- [AGENTCOST05-BP04 Tạo báo cáo chargeback và ROI](agentcost05-bp04.md)
- [AGENTCOST07-BP02 Thiết lập phát hiện bất thường chủ động cho các mẫu chi phí của agent](../7-agentcost07/agentcost07-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Using cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Observability tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore - Observability](https://catalog.workshops.aws/agentcore-deep-dive/en-US/70-agentcore-observability)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)
