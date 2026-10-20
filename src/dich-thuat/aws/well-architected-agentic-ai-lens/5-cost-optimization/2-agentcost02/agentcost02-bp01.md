# AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng

Chạy mọi tác vụ agent trên model lớn nhất hiện có làm phồng chi phí suy luận lên gấp một bậc độ lớn cho công việc mà các model nhỏ hơn xử lý đúng. Khớp mỗi tác vụ với model rẻ nhất có khả năng đạt chất lượng chấp nhận được, và chỉ leo thang khi độ tin cậy giảm.

**Kết quả mong muốn:**

- Bạn có các tác vụ agent được phân loại thành các tầng độ phức tạp, với một chính sách định tuyến được ghi chép ánh xạ mỗi tầng tới một foundation model cụ thể.
- Bạn có các mẫu cascade leo thang lên các model chi phí cao hơn chỉ khi độ tin cậy của một tầng thấp hơn rơi xuống dưới ngưỡng.
- Bạn theo dõi chi phí trên mỗi phản hồi đúng qua các tầng và làm mới các quyết định định tuyến bằng dữ liệu thay vì trực giác.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng model lớn nhất hiện có cho mọi tác vụ agent mà không đánh giá độ phức tạp tác vụ, làm phồng chi phí suy luận cho các thao tác thường quy.
- Gán cố định model tĩnh mà không có leo thang dựa trên độ tin cậy, dẫn đến hoặc cấp phát dư cho các tác vụ thường quy hoặc cấp phát thiếu cho các trường hợp biên phức tạp.
- Theo dõi chi phí tổng hợp mà không phân rã hiệu năng agent theo tầng model, che giấu các cơ hội chuyển workload sang model rẻ hơn.
- Không giám sát hiệu năng model tùy chỉnh sau khi chuyển sang tầng nhỏ hơn, cho phép khoản tiết kiệm chi phí che khuất sự suy giảm chất lượng ẩn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Lựa chọn theo tầng dành các model đắt tiền cho suy luận thực sự phức tạp và định tuyến các tác vụ thường quy tới các lựa chọn tiết kiệm chi phí.
- Model cascading tối thiểu hóa các lần gọi model cao cấp thông qua leo thang dựa trên độ tin cậy.
- Các model chuyên biệt cho các tác vụ đặc thù theo miền mang lại độ chính xác cao hơn với chi phí thấp hơn so với các lựa chọn đa năng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Độ phức tạp tác vụ là một thuộc tính quan trọng cần đo lường. Tại mỗi lần gọi agent, suy luận bạn cần hoặc là nhẹ (phân loại, chuyển đổi định dạng, trích xuất ý định), trung bình (suy luận nhiều bước, tóm tắt), hoặc thực sự phức tạp (phân tích mở, tối ưu đa ràng buộc). Ba lớp này ánh xạ tới các mức giá khác nhau trong danh mục model [Amazon Bedrock](https://aws.amazon.com/bedrock/), và đối xử với chúng giống hệt nhau nghĩa là bạn trả giá của lớp phức tạp cho mọi tác vụ có độ phức tạp thấp. Phân loại trước và định tuyến tương ứng là nơi phần lớn dư địa chi phí nằm ở đó.

Một bộ tiền phân loại nhẹ cho bạn quyết định định tuyến đó mà không cần gọi model chính trước. Các heuristic theo luật hoặc một model nhỏ có thể phân tích các đặc điểm yêu cầu như độ dài đầu vào, định dạng có cấu trúc hay phi cấu trúc, số ràng buộc và độ sâu suy luận, gán điểm ánh xạ tới các ngưỡng tầng (ví dụ, dưới 0.3 cho đơn giản, 0.3 đến 0.7 cho trung bình, trên 0.7 cho phức tạp). Bộ tiền phân loại phải tốn ít hơn khoản chênh lệch giá giữa các tầng để tạo ra tiết kiệm ròng trên định tuyến lần thử đầu. Với các tác vụ đa phương thức, nguyên tắc còn mở rộng thêm. Định tuyến trích xuất tài liệu tới Amazon Bedrock Data Automation và tương tác âm thanh tới Amazon Nova Sonic thay vì gửi ảnh hoặc âm thanh thô qua các model thị giác đa năng đắt tiền.

Model cascading là một cơ chế fallback khi bộ phân loại không chắc chắn. Cho model tầng thấp hơn trả về một phản hồi có cấu trúc kèm một điểm độ tin cậy tự đánh giá và chỉ leo thang lên tầng kế tiếp khi độ tin cậy rơi xuống dưới một ngưỡng. Các chuỗi fallback sơ cấp, thứ cấp và tam cấp bắt các timeout và lỗi bằng cách đi lên một tầng thay vì thử lại cùng tầng, cải thiện tỷ lệ hoàn thành mà không lãng phí việc thử lại. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) được thiết kế để hỗ trợ nhiều framework và nhà cung cấp LLM, và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thực thi các guardrail giúp ngăn các lần gọi model đắt tiền khi độ phức tạp tác vụ không biện minh cho chi phí.

Tầng giá độc lập với kích thước model. [Amazon Bedrock capacity, limits, and cost optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html) tài liệu hóa Flex cho phát triển và kiểm thử với chi phí trên mỗi token thấp nhất, Standard cho production, và Priority chỉ cho các tương tác hướng người dùng nhạy về độ trễ nơi rủi ro bị throttle phải được tối thiểu hóa. Batch inference mang lại tiết kiệm tới 50% cho các workload không nhạy về thời gian như tạo báo cáo, chuẩn bị dữ liệu huấn luyện, hoặc đánh giá offline. Với lưu lượng khối lượng lớn nhất quán, các cam kết Reserved Tier cung cấp tiết kiệm 30 đến 50% so với giá on-demand. Với [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html), bạn có thể benchmark nhiều lựa chọn model theo phân phối tác vụ thực tế của mình, đo lường chi phí trên mỗi phản hồi đúng và làm mới chính sách định tuyến hàng quý khi có các model mới.

### Các bước triển khai

- **Phân loại các tác vụ agent thành các tầng độ phức tạp:** Ghi chép một chính sách định tuyến model ánh xạ mỗi tầng (đơn giản, trung bình và phức tạp) tới một model [Amazon Bedrock](https://aws.amazon.com/bedrock/) cụ thể, và cam kết chính sách như một bản ghi quyết định kiến trúc để những người xem xét về sau có thể kiểm toán lý do.
- **Chọn tầng giá cho mỗi môi trường:** Dùng Flex cho phát triển và kiểm thử, Standard cho production, và Priority chỉ cho các agent hướng người dùng nhạy về độ trễ, và đánh giá các cam kết [Amazon Bedrock Reserved Tier](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html) cho các workload khối lượng lớn nhất quán.
- **Chèn một bộ tiền phân loại độ phức tạp tác vụ:** Triển khai các heuristic theo luật hoặc một lần gọi model nhỏ chấm điểm mỗi yêu cầu theo độ dài đầu vào, cấu trúc, số ràng buộc và độ sâu suy luận trước lần gọi chính, và đảm bảo bộ phân loại tốn ít hơn khoản chênh lệch giá giữa các tầng.
- **Triển khai model cascading dựa trên độ tin cậy:** Cho mỗi phản hồi tầng thấp hơn bao gồm một điểm độ tin cậy tự đánh giá, và leo thang lên tầng kế tiếp khi độ tin cậy rơi xuống dưới ngưỡng đã cấu hình thay vì thử lại ở cùng tầng.
- **Cấu hình các chuỗi fallback cho mỗi loại tác vụ:** Định nghĩa các lựa chọn model sơ cấp, thứ cấp và tam cấp, với leo thang tự động khi timeout hoặc lỗi thay vì thử lại, để các lỗi tạm thời đi lên một tầng thay vì lặp lại cùng chi phí.
- **Định tuyến các tác vụ không nhạy về thời gian tới batch inference:** Dùng [Amazon Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html) cho tạo báo cáo, làm giàu dữ liệu và đánh giá offline để thu về tiết kiệm tới 50% so với giá on-demand.
- **Benchmark các model chuyên biệt so với đa năng:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trên phân phối tác vụ thực tế của bạn, đo lường chi phí trên mỗi phản hồi đúng để các lựa chọn định tuyến được đặt nền trên dữ liệu kết quả.
- **Xem xét các chính sách định tuyến hàng quý:** Dùng AWS Cost Explorer và các dashboard Amazon CloudWatch để kiểm tra tỷ lệ leo thang quan sát được, và điều chỉnh việc gán tầng khi các mẫu leo thang cascade cho thấy các ngưỡng bị tinh chỉnh sai.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST01-BP04 Thiết kế các cấp bậc agent và mẫu ủy quyền giảm chi phí phối hợp](../1-agentcost01/agentcost01-bp04.md)
- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](agentcost02-bp02.md)
- [AGENTCOST02-BP04 Triển khai tùy chỉnh model để giảm chi phí dài hạn](agentcost02-bp04.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Effective cost optimization strategies for Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- [Use Amazon Bedrock Intelligent Prompt Routing for cost and latency benefits](https://aws.amazon.com/blogs/machine-learning/use-amazon-bedrock-intelligent-prompt-routing-for-cost-and-latency-benefits/)
- [Optimizing cost for using foundational models with Amazon Bedrock](https://aws.amazon.com/blogs/aws-cloud-financial-management/optimizing-cost-for-using-foundational-models-with-amazon-bedrock/)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Amazon Bedrock model pricing](https://aws.amazon.com/bedrock/pricing/)
- [Amazon Bedrock capacity, limits, and cost optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)
- [Amazon Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)
- [AWS re:Invent 2024 - Mastering model choice: The 3-step Amazon Bedrock advantage (AIM391)](https://www.youtube.com/watch?v=Vu91YwZxskY)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Công cụ liên quan:**

- [Strands Agents Model Providers](https://strandsagents.com/docs/user-guide/concepts/model-providers/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
