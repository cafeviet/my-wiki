# AGENTCOST02-BP04 Triển khai tùy chỉnh model để giảm chi phí dài hạn

Tùy chỉnh các model nhỏ hơn cho một tác vụ khối lượng lớn, lặp lại có thể tối ưu chi phí trên mỗi lần gọi thành một chi phí huấn luyện một lần khấu hao qua mọi lần gọi tương lai. Bài toán chỉ có nghĩa khi khối lượng và độ ổn định tác vụ đủ cao để biện minh cho khoản đầu tư, nên quyết định cần bắt đầu bằng một phép tính điểm hòa vốn (break-even), chứ không phải sự hào hứng với fine-tuning.

**Kết quả mong muốn:**

- Bạn có các model chuyên biệt xử lý các tác vụ khối lượng lớn, lặp lại với chi phí trên mỗi lần gọi thấp hơn đáng kể so với các foundation model đa năng.
- Bạn có một pipeline tùy chỉnh nắm bắt các mẫu quyết định từ production và làm mới các model theo một nhịp đã lên lịch.
- Bạn xác thực chất lượng quyết định bằng A/B testing so với các foundation model trước khi định tuyến lưu lượng production tới một model tùy chỉnh.
- Bạn theo dõi khoản tiết kiệm chi phí suy luận và chất lượng quyết định cạnh nhau để **ROI** dương có thể chứng minh được thay vì giả định.

**Các phản mẫu thường gặp (anti-patterns):**

- Fine-tune trên dữ liệu tổng hợp trình bày sai phân phối tác vụ production, gây kém hiệu năng làm mất khoản tiết kiệm chi phí thông qua tỷ lệ hoàn thành tác vụ thấp hơn.
- Áp dụng tùy chỉnh cho các loại tác vụ khối lượng thấp nơi chi phí huấn luyện vượt quá khoản tiết kiệm suy luận dự kiến, lãng phí công sức vào tối ưu không đạt ROI dương.
- Coi tùy chỉnh là một dự án một lần mà không thích nghi liên tục, cho phép các model chuyên biệt trôi dạt khi các mẫu workload thay đổi.
- Định tuyến lưu lượng production tới các model tùy chỉnh mà không A/B testing so với các foundation model, gây rủi ro suy giảm chất lượng làm hỏng khoản tiết kiệm chi phí.
- Triển khai các model tùy chỉnh mà không đo lường độ trễ suy luận, chi phí token và số liệu chất lượng, làm giảm khả năng xác thực rằng mức giảm chi phí kỳ vọng đã thành hiện thực.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các model nhỏ hơn đã fine-tune đạt độ chính xác tương đương với chi phí trên mỗi lần gọi thấp hơn thông qua tiêu thụ token giảm và suy luận nhanh hơn.
- Các chi phí huấn luyện một lần khấu hao qua hàng nghìn lần gọi, mang lại lợi nhuận dồn tích cho các tác vụ khối lượng lớn.
- Các pipeline thích nghi liên tục giữ các model chuyên biệt căn chỉnh với các mẫu workload đang tiến hóa thay vì suy tàn âm thầm.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Tính chi phí suy luận hàng tháng hiện tại cho loại tác vụ mục tiêu bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), ước lượng mức giảm từ một model tùy chỉnh nhỏ hơn, và so sánh với các chi phí tùy chỉnh một lần cộng với chi phí làm mới liên tục. Khi chi phí suy luận hàng tháng vượt $500 và khối lượng tác vụ vượt 10.000 lần gọi mỗi tháng, tùy chỉnh thường đạt điểm hòa vốn trong vòng 6 đến 12 tháng. Hãy làm cho điểm hòa vốn tường minh: (chi phí huấn luyện một lần + chi phí làm mới hàng quý × chân trời lập kế hoạch theo quý) chia cho khoản tiết kiệm suy luận hàng tháng. Với một lần huấn luyện $5.000 tiết kiệm $400 mỗi tháng, điểm hòa vốn rơi vào tháng 13, mức chấp nhận được cho các workload có vòng đời nhiều năm nhưng không cho các dự án thử nghiệm.

[Knowledge distillation](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html) chuyển giao năng lực từ một model giáo viên lớn tới một model học trò nhỏ hơn với chi phí trên mỗi lần gọi thấp hơn. Dữ liệu huấn luyện nên đến từ các log lần gọi production được lọc lấy các lần hoàn thành thành công, độ tin cậy cao. Các phương pháp fine-tuning tiết kiệm tham số như QLoRA lượng tử hóa trọng số model gốc xuống độ chính xác bốn-bit và chỉ huấn luyện các tham số adapter, khiến fine-tuning trên một GPU khả thi cho các nhóm nhỏ hơn. Các job [Amazon Bedrock model customization](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html) và [Amazon SageMaker AI Training Jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html) với QLoRA hỗ trợ fine-tuning mà không cần quản lý hạ tầng huấn luyện, và [Amazon Bedrock Custom Model Import](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html) đưa kết quả vào Amazon Bedrock để phục vụ.

Xác thực giúp ngăn các hồi quy chất lượng xảy ra từ các tối ưu chi phí này. Với [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), bạn có thể chia lưu lượng production giữa foundation model và model tùy chỉnh trong lúc A/B testing, và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy các đánh giá LLM-as-a-Judge trên cả hai nhánh. Chỉ chấp nhận lượng tử hóa khi tổn thất độ chính xác nằm trong ngưỡng chất lượng chấp nhận được của bạn về tỷ lệ thành công tác vụ. Hãy coi tùy chỉnh là một pipeline: định kỳ trích xuất các ví dụ chất lượng cao từ các log production, lên lịch các job làm mới hàng quý, và cổng thăng cấp dựa trên xác thực A/B để trôi dạt không dồn lại âm thầm giữa các lần làm mới.

### Các bước triển khai

- **Tiến hành phân tích chi phí-lợi ích của tùy chỉnh:** Tính chi phí suy luận hàng tháng hiện tại cho các loại tác vụ khối lượng lớn, xác định nơi chi phí huấn luyện khấu hao trong chân trời lập kế hoạch của bạn, và so sánh khoản đầu tư fine-tuning (tính toán huấn luyện cộng với bảo trì liên tục) với khoản tiết kiệm suy luận tích lũy dự kiến.
- **Chọn lọc dữ liệu huấn luyện từ các log production:** Trích xuất các ví dụ chất lượng cao từ các log lần gọi production bằng cách lọc lấy các lần gọi có tỷ lệ lỗi thấp và độ trễ chấp nhận được bằng các số liệu AgentCore Observability. Nhắm 500 đến 1.000 ví dụ cho mỗi loại tác vụ. Truy vấn Amazon CloudWatch tìm các lần gọi có độ trễ nằm trong khoảng p50 đến p90 và không có error_type, xem xét thủ công một mẫu để xác minh chất lượng, và lưu tập dữ liệu đã chọn lọc trong Amazon S3.
- **Chạy distillation hoặc fine-tuning:** Dùng các job [Amazon Bedrock model customization](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html) hoặc [Amazon SageMaker AI Training Jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html) với QLoRA, và xác thực bằng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trên một tập kiểm thử giữ riêng.
- **Import và A/B test các model tùy chỉnh:** Dùng [Amazon Bedrock Custom Model Import](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html) và triển khai qua [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), định tuyến một lát lưu lượng tới model tùy chỉnh trước khi thăng cấp nó xử lý khối lượng production.
- **Lên lịch các job làm mới hàng quý:** Tự động hóa trích xuất dữ liệu huấn luyện và huấn luyện lại theo nhịp hàng quý, với xác thực A/B như cổng thăng cấp để bắt trôi dạt tại mỗi lần làm mới thay vì tại lần xem xét hàng năm.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng](agentcost02-bp01.md)
- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](agentcost02-bp02.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Model customization in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html)
- [Amazon Bedrock Custom Model Import](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Evaluate models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS re:Invent 2024 - Mastering model choice: The 3-step Amazon Bedrock advantage (AIM391)](https://www.youtube.com/watch?v=Vu91YwZxskY)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon SageMaker AI](https://aws.amazon.com/sagemaker-ai/)
- [Amazon S3](https://aws.amazon.com/s3/)
