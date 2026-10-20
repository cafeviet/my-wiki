# AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent

Nhiều luồng đa agent phải trả tiền cho suy luận AI ở tầng phối hợp cho những quyết định mà các luật có thể xử lý mà không tốn thêm gì. Khớp mỗi quyết định điều phối với cơ chế rẻ nhất có khả năng xử lý nó sẽ loại bỏ chi phí ẩn đó.

**Kết quả mong muốn:**

- Bạn lựa chọn các mẫu điều phối từ phân tích tính tất định của luồng công việc thay vì mặc định dùng giám sát bằng AI.
- Bạn có định tuyến tất định chạy mà không cần gọi model, và các supervisor AI được dành cho những trường hợp thực sự mơ hồ cần hiểu ngôn ngữ tự nhiên.
- Bạn theo dõi chi phí điều phối riêng biệt với chi phí worker và duy trì tiêu chí lựa chọn mẫu được ghi chép.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng supervisor AI cho các luồng công việc tất định, gọi các foundation model đắt tiền cho các quyết định định tuyến mà các luật đơn giản có thể xử lý.
- Mặc định dùng giám sát bằng AI mà không đánh giá liệu logic định tuyến có tuân theo các luật tường minh hay không.
- Chỉ theo dõi chi phí luồng công việc tổng hợp mà không phân rã chi tiêu của orchestrator so với worker, che giấu chi phí phối hợp không tương xứng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Định tuyến theo luật xử lý các nhánh tất định mà không cần gọi model, giảm chi phí cho mỗi quyết định định tuyến xuống gần bằng không.
- Các mẫu hybrid khớp mỗi quyết định định tuyến với cơ chế rẻ nhất có khả năng.
- Tiêu chí lựa chọn mẫu được ghi chép giúp ngăn việc cấp phát dư giám sát bằng AI cho các luồng công việc mới.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Tính tất định của luồng công việc là một thuộc tính, không phải một giả định. Tại mỗi điểm điều phối, quyết định định tuyến hoặc là một lựa chọn trên một tập hữu hạn, có thể liệt kê được các điều kiện (loại tác vụ, phân loại đầu ra, mã lỗi) hoặc là một phán xét trên một không gian đầu vào mở. Lớp thứ nhất không tốn gì để định tuyến bằng luật, còn lớp thứ hai đòi hỏi suy luận của model. Hầu hết các luồng đa agent chứa cả hai, nhưng các nhóm thường trả tiền cho giám sát bằng AI trên toàn bộ luồng công việc vì mẫu mặc định như vậy. Tiến hành phân tích tính tất định ngay từ đầu là sự khác biệt giữa việc tiêu token model cho việc định tuyến mà một câu điều kiện có thể xử lý và việc chỉ tiêu chúng ở nơi đầu vào thực sự đòi hỏi diễn giải ngôn ngữ tự nhiên.

Việc thực thi diễn ra bên ngoài mã của agent. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) chạy các chính sách Cedar tại ranh giới [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), áp dụng các luật định tuyến tất định dựa trên thuộc tính tác vụ, danh tính người dùng hoặc yêu cầu về công cụ mà không cần gọi một lần suy luận. Các worker agent triển khai trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) tại các nút lá nơi suy luận thực sự diễn ra. Giữ định tuyến và suy luận trên các đường ray riêng cho phép mỗi cái tiến hóa độc lập và được giám sát theo các số liệu riêng.

Với định tuyến tất định một phần, một mẫu hybrid theo tầng giúp bạn căn chỉnh chi phí. Một bộ phân loại nhẹ (một model Amazon Bedrock nhỏ hoặc một heuristic theo luật) thử định tuyến theo luật trước và chỉ leo thang lên supervisor AI đầy đủ khi độ tin cậy của nó rơi xuống dưới một ngưỡng đã cấu hình. Tỷ lệ leo thang là tín hiệu cho biết liệu tầng đã được tinh chỉnh đúng chưa. Nếu tỷ lệ quá cao, bộ phân loại cần được tinh chỉnh. Nếu quá thấp, supervisor bị cấp phát dư và bộ phân loại có thể hấp thụ thêm nhiều trường hợp hơn.

Các ngưỡng định lượng cung cấp định tuyến theo luật cho các luồng công việc có ít hơn mười nhánh tất định, một bộ phân loại nhẹ cho định tuyến trên mười đến năm mươi loại, và supervisor AI chỉ cho các không gian loại không giới hạn cần hiểu ngôn ngữ tự nhiên. Tỷ lệ chi phí phối hợp (token supervisor chia cho tổng token luồng công việc) là công cụ chẩn đoán liên tục. Khi nó trôi lên trên đường cơ sở, mẫu cần được đánh giá lại, không phải cần một ngân sách lớn hơn.

### Các bước triển khai

- **Tiến hành phân tích tính tất định của luồng công việc:** Tại mỗi điểm điều phối trong luồng công việc, phân loại quyết định định tuyến là hoàn toàn tất định, tất định một phần, hay mở, và ghi lại lý do như một bản ghi quyết định kiến trúc (architectural decision record) để những người xem xét về sau có thể kiểm toán vì sao mỗi mẫu được chọn.
- **Áp dụng các chính sách Cedar cho định tuyến tất định:** Cấu hình [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với các chính sách Cedar tại [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cho mọi nhánh hoàn toàn tất định, để các quyết định định tuyến này chạy mà không cần gọi model.
- **Chèn một bộ phân loại nhẹ cho định tuyến tất định một phần:** Triển khai một model nhỏ hoặc heuristic theo luật thử định tuyến theo luật trước và chỉ leo thang lên supervisor AI đầy đủ khi độ tin cậy của nó rơi xuống dưới một ngưỡng có thể cấu hình, và ghi log tỷ lệ leo thang như một tín hiệu tinh chỉnh.
- **Tách chi phí điều phối khỏi chi phí worker:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để quy gán token cho tầng orchestrator và tầng worker riêng biệt, tính tỷ lệ chi phí phối hợp cho mỗi luồng công việc, và cảnh báo khi tỷ lệ trôi lên trên đường cơ sở đã ghi cho mẫu đó.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](agentcost01-bp01.md)
- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](agentcost01-bp02.md)
- [AGENTCOST01-BP04 Thiết kế các cấp bậc agent và mẫu ủy quyền giảm chi phí phối hợp](agentcost01-bp04.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](../5-agentcost05/agentcost05-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)
- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Policy tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/08-AgentCore-policy)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
