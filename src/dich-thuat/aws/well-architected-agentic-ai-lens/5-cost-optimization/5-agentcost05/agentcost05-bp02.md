# AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent

Trong các luồng đa agent, chi phí tổng hợp cho bạn biết bạn đã tiêu bao nhiêu nhưng không cho biết những chi phí cụ thể đó đến từ đâu. Tracing với các workflow ID lan truyền qua các ranh giới agent làm cho chi phí luồng công việc rõ ràng hơn, khi nó được phân rã thành thực thi của worker, các lần gọi công cụ, và các thao tác bộ nhớ, giúp bạn ra các quyết định tối ưu kiến trúc dựa trên dữ liệu.

**Kết quả mong muốn:**

- Bạn lan truyền các workflow trace ID qua mọi lần gọi agent, lần gọi công cụ, và thao tác bộ nhớ.
- Bạn tính chi phí-thực-trên-mỗi-lần-hoàn-thành-luồng-công-việc, với chi phí điều phối được theo dõi riêng biệt với chi phí thực thi.
- Bạn so sánh hiệu quả xuyên các mẫu cộng tác khác nhau bằng dữ liệu chi phí thực.
- Bạn trực quan hóa chi phí luồng công việc theo mẫu, vai trò agent, và kết quả kinh doanh.

**Các phản mẫu thường gặp (anti-patterns):**

- Theo dõi chi phí cho từng agent riêng lẻ mà không có tương quan ở cấp luồng công việc, khiến không thể tính chi phí-thực-trên-mỗi-lần-hoàn-thành-luồng-công-việc.
- Kết hợp chi phí supervisor và worker vào một số liệu duy nhất, che khuất liệu các luồng công việc có chịu chi phí điều phối quá mức hay không.
- Triển khai một mẫu đa agent mà không đo lường các khác biệt chi phí giữa các lựa chọn thay thế, bỏ lỡ việc giảm chi phí kiến trúc.
- Phân tích tổng chi phí mà không có phân rã theo vai trò, làm giảm khả năng nhận diện loại agent nào đẩy chi tiêu cao nhất và cần tối ưu có mục tiêu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Khả năng nhìn thấy chi phí luồng công việc đầy đủ cho phép tính chi phí-thực-trên-mỗi-lần-hoàn-thành-luồng-công-việc xuyên các ranh giới agent.
- Các tỷ lệ chi phí điều phối làm lộ khi phối hợp tiêu thụ một phần chi tiêu luồng công việc không tương xứng.
- So sánh chi phí xuyên các mẫu cộng tác biến các quyết định kiến trúc từ phỏng đoán thành các lựa chọn dựa trên dữ liệu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Khả năng nhìn thấy chi phí ở cấp luồng công việc bắt đầu với một workflow trace ID được tạo lúc khởi tạo luồng công việc và lan truyền qua mọi lần gọi agent, lần gọi công cụ, và thao tác bộ nhớ. Không có khóa tương quan đó, chi phí theo từng agent không thể được ghép thành tổng theo từng luồng công việc, và trở nên khó xác định việc cung cấp một kết quả kinh doanh tốn kém đến đâu. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp một cấp bậc ba tầng ánh xạ trực tiếp tới vấn đề này: các phiên (sessions) cho các luồng công việc hoàn chỉnh, các vết (traces) cho các lần gọi agent riêng lẻ, và các span cho độ chi tiết ở cấp thao tác. Với các agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), cách ly phiên giữ các ranh giới chi phí căn chỉnh với các ranh giới thực thi agent, nên không cần các công thức phân bổ phức tạp.

Phân rã hữu ích nhất trong một luồng công việc là sự chia tách orchestrator-so-với-worker. Gắn thẻ các lần gọi supervisor với agent-role:orchestrator và các lần gọi worker với agent-role:worker, rồi tính tỷ lệ chi phí điều phối như chi phí orchestrator chia cho tổng chi phí luồng công việc. Một tỷ lệ cao cho thấy phối hợp đang chi phối thực thi, vốn thường báo hiệu một cấp bậc cần được làm phẳng hoặc các manifest cần được nén. Phân rã chi phí luồng công việc thêm nữa thành token điều phối, token thực thi của worker, chi phí gọi công cụ, và chi phí truy xuất bộ nhớ cho bạn biết thành phần nào cần tối ưu trước.

Chỉ riêng dữ liệu chi phí có thể gây hiểu lầm nếu không có dữ liệu chất lượng để tương quan. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đo lường chất lượng đầu ra cùng với chi phí, vốn biến tối ưu thành một quyết định đánh đổi thay vì một sự tối thiểu hóa trên một trục. Một mẫu luồng công việc rẻ hơn nhưng làm suy giảm chất lượng thực ra không rẻ hơn về mặt kinh doanh, và lớp phủ đánh giá làm cho sự đánh đổi đó tường minh.

Định tuyến một tỷ lệ phần trăm các lần thực thi tới các mẫu cộng tác thay thế và so sánh chi phí-trên-mỗi-lần-hoàn-thành-luồng-công-việc xuyên các mẫu trong các dashboard Amazon CloudWatch và AWS Cost Explorer cho phép các nhóm chọn các kiến trúc dựa trên hành vi thực, chứ không phải các mô hình chi phí lý thuyết. Với các mẫu đặc biệt tối ưu chi phí supervisor, xem [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](../1-agentcost01/agentcost01-bp03.md).

### Các bước triển khai

- **Bật tracing phân tán xuyên các agent:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập các vết phân tán, xuất dữ liệu đo lường sang Amazon CloudWatch với các workflow trace ID lan truyền qua mọi lần gọi.
- **Áp dụng gắn thẻ theo vai trò và tính các tỷ lệ điều phối:** Gắn thẻ mọi lần gọi với agent-role (orchestrator hoặc worker), và tính tỷ lệ chi phí điều phối cho mỗi loại luồng công việc.
- **Trực quan hóa chi phí theo mẫu và cảnh báo trên các ngưỡng:** Xây dựng các dashboard CloudWatch hiển thị các phân phối chi phí luồng công việc theo mẫu cộng tác và vai trò agent, với cảnh báo khi chi phí điều phối vượt các ngưỡng.
- **Chạy các thử nghiệm mẫu:** Định tuyến một tỷ lệ phần trăm các lần thực thi tới các mẫu cộng tác thay thế và so sánh chi phí-trên-mỗi-lần-hoàn-thành-luồng-công-việc xuyên các mẫu.
- **So sánh hiệu quả luồng công việc trong Cost Explorer:** Dùng AWS Cost Explorer để so sánh hiệu quả xuyên các mẫu cộng tác khác nhau theo thời gian.
- **Phân rã chi phí luồng công việc:** Triển khai các hàm tổng hợp chi phí phân rã tổng chi phí luồng công việc thành token điều phối, token thực thi của worker, chi phí gọi công cụ, và chi phí truy xuất bộ nhớ cho mỗi loại luồng công việc.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](../1-agentcost01/agentcost01-bp02.md)
- [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](../1-agentcost01/agentcost01-bp03.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](agentcost05-bp01.md)
- [AGENTCOST05-BP03 Thiết kế phân bổ chi phí nhận biết tenant cho các mô hình định giá AaaS](agentcost05-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)
- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Observability tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
