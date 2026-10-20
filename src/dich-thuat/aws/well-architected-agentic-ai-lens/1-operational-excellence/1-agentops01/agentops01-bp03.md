# AGENTOPS01-BP03 Phát triển các kịch bản kiểm thử phản ánh chính xác lỗi của các thành phần phụ thuộc, giao thức điều phối và quy trình kinh doanh

Kiểm thử luồng thuận lợi (happy-path) dự đoán agent hành xử ra sao khi mọi thứ đều hoạt động, trong khi kiểm thử lỗi dự đoán chúng hành xử ra sao khi có sự cố ngoài dự kiến. Một tư thế chịu lỗi được xây dựng trên các lỗi được tiêm vào (injected failures), các kịch bản bế tắc, và các quy trình kinh doanh bị gián đoạn là sự khác biệt giữa suy giảm nhã nhặn và một sự cố ngừng hoạt động ngoài dự kiến.

**Kết quả mong muốn:**

- Bạn có một bộ kiểm thử lỗi cho mỗi agent bao phủ các lỗi thành phần phụ thuộc, các sự cố điều phối, và các gián đoạn quy trình kinh doanh.
- Bạn có thể tiêm lỗi vào luồng công việc của agent theo yêu cầu và xác minh rằng xử lý lỗi, suy giảm nhã nhặn, và leo thang hoạt động đúng như thiết kế.
- Bạn duy trì các mẫu lỗi đã biết dưới dạng kiểm thử hồi quy chạy tự động trên mỗi thay đổi hành vi.
- Bạn theo dõi tỷ lệ vượt qua kiểm thử lỗi theo thời gian như một chỉ số chịu lỗi có thể thấy được.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ kiểm thử luồng thuận lợi mà không kiểm định hành vi của agent khi Tools không khả dụng, khi API hết thời gian, hoặc khi nguồn dữ liệu trả về lỗi.
- Chỉ chạy kiểm thử lỗi trong các môi trường unit biệt lập mà không mô phỏng các lỗi phối hợp đa agent như bế tắc, mất thông điệp, hoặc timeout bàn giao.
- Xem các kịch bản kiểm thử lỗi như một bài tập một lần thay vì một bộ hồi quy sống, phát triển theo mỗi sự cố sản xuất.
- Bỏ qua kiểm thử cho các gián đoạn quy trình kinh doanh, thay đổi định dạng thượng nguồn, phê duyệt bị trì hoãn, và từ chối hạ nguồn, khiến agent thất bại âm thầm khi thế giới thực dịch chuyển.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các bộ kiểm thử lỗi trở thành một chuẩn ổn định để so sánh khả năng chịu lỗi của agent qua các lần lặp, cung cấp cơ sở thực nghiệm cho các quyết định cải tiến.
- Kiểm thử chuẩn hóa giúp đánh giá mọi thay đổi agent về tác động chịu lỗi theo cùng một cách, bất kể ai thực hiện thay đổi hay tiến độ khẩn cấp đến đâu.
- Các mẫu lỗi đã biết được nắm bắt dưới dạng kiểm thử hồi quy giúp ngăn tái diễn các vấn đề đã được chẩn đoán trước đó.
- Các xu hướng chịu lỗi có thể thấy được mang lại cho lãnh đạo và người vận hành một góc nhìn chung về việc danh mục agent đang trở nên tin cậy hơn hay mong manh hơn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các chế độ lỗi phân thành ba nhóm, và mỗi nhóm đòi hỏi một tư thế kiểm thử khác nhau.

Lỗi thành phần phụ thuộc là dễ xử lý nhất. Tools trả về lỗi 5xx, API hết thời gian, cơ sở tri thức trả về kết quả rỗng, và suy luận Model bị điều tiết (throttle) hoặc suy giảm. Những lỗi này ánh xạ gọn gàng tới đánh giá agent và tiêm lỗi tổng hợp (synthetic fault injection). [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) cung cấp đánh giá tự động về cách agent xử lý các trường hợp biên và kịch bản lỗi, sử dụng các bộ đánh giá dựng sẵn và tùy chỉnh để chấm điểm hành vi agent so với kết quả kỳ vọng. Đối với tiêm lỗi ở cấp hạ tầng như độ trễ mạng hoặc cạn kiệt dung lượng, [AWS Fault Injection Service](https://aws.amazon.com/fis/) bổ trợ cho các đánh giá agent bằng cách kiểm định rằng các chính sách thử lại, dự phòng (fallback), và ngắt (cutoff) hoạt động đúng như tài liệu ở tầng hạ tầng.

Các sự cố điều phối khó hơn vì chúng đòi hỏi nhiều hơn một thành phần đơn lẻ bị lỗi. Mất thông điệp, giao nhận trùng lặp, thông điệp sai thứ tự, bế tắc, timeout bàn giao, và hỏng gói ngữ cảnh đều nảy sinh từ các tương tác giữa các agent chứ không phải từ hành vi của bất kỳ agent đơn lẻ nào. Hãy kiểm thử các kịch bản này bằng cách mô phỏng lỗi phối hợp trong luồng công việc đa agent của bạn. Tiêm timeout bàn giao, làm hỏng gói ngữ cảnh, và kích hoạt các yêu cầu đồng thời để bộc lộ các điều kiện tranh chấp (race conditions). Hãy quyết định mô phỏng các lỗi này trong môi trường staging dùng chung hay trong một môi trường chaos chuyên dụng. Môi trường đầu bắt các hồi quy nhanh hơn, trong khi môi trường sau giảm phạm vi tác động trong quá trình kiểm thử khám phá.

Các gián đoạn quy trình kinh doanh là nhóm thường bị bỏ sót nhất vì chúng không trông giống lỗi hạ tầng. Khi một nhóm thượng nguồn thay đổi lược đồ đầu vào, khi một phê duyệt bắt buộc bị trì hoãn, hoặc khi một hệ thống hạ nguồn từ chối đầu ra của agent, mã của agent vẫn nguyên vẹn và mọi phụ thuộc đều phản hồi, nhưng luồng công việc vẫn thất bại. Các kịch bản kiểm thử phải bao phủ cách agent hành xử khi quy trình kinh doanh dịch chuyển, như thất bại nhã nhặn, thông điệp lỗi có ý nghĩa, leo thang phù hợp, và không hỏng hóc âm thầm. Các kiểm thử này bảo vệ trước chế độ lỗi mà hệ thống trông có vẻ khỏe mạnh với giám sát nhưng lại cho ra các kết quả sai hoặc không đầy đủ.

Hãy dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để duy trì và chạy các tập dữ liệu đánh giá nắm bắt các mẫu lỗi đã biết dưới dạng kiểm thử hồi quy. Tích hợp bộ đánh giá vào pipeline CI/CD như một cổng bắt buộc để các lần triển khai bị chặn khi xuất hiện hồi quy trong xử lý lỗi. Theo dõi tỷ lệ vượt qua trong [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) và cấu hình cảnh báo khi các chỉ số chịu lỗi suy giảm. Lợi ích vận hành cộng dồn, vì mỗi sự cố sản xuất trở thành cơ hội để thêm một kịch bản kiểm thử, và bộ kiểm thử ngày càng sắc bén theo thời gian.

### Các bước triển khai

- **Lập catalog các chế độ lỗi đã biết cho mỗi agent:** Sắp xếp theo lỗi thành phần phụ thuộc, sự cố điều phối, và gián đoạn quy trình kinh doanh, với một chủ sở hữu được nêu tên cho mỗi nhóm.
- **Tạo kiểm thử cho lỗi thành phần phụ thuộc:** Mô phỏng Tools không khả dụng, API hết thời gian, lỗi nguồn dữ liệu, và suy giảm suy luận Model bằng đánh giá tập dữ liệu của [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) và các bộ đánh giá tùy chỉnh.
- **Tạo kiểm thử cho sự cố điều phối:** Bao phủ lỗi giao tiếp, điều kiện bế tắc, lỗi bàn giao, và hỏng gói ngữ cảnh bằng cách mô phỏng lỗi phối hợp trong luồng công việc đa agent.
- **Tạo kiểm thử cho gián đoạn quy trình kinh doanh:** Mô phỏng thay đổi quy trình thượng nguồn, thay đổi định dạng đầu vào, và từ chối của hệ thống hạ nguồn, và xác minh thất bại nhã nhặn và leo thang có ý nghĩa.
- **Tích hợp tiêm lỗi hạ tầng ở nơi phù hợp:** Dùng [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) cho các lỗi ở cấp hạ tầng (điều tiết, cạn kiệt dung lượng, độ trễ mạng) ảnh hưởng tới luồng công việc agent.
- **Đặt cổng triển khai trên hồi quy xử lý lỗi:** Biến bộ đánh giá thành một giai đoạn CI/CD bắt buộc, chặn thăng hạng khi xuất hiện hồi quy về khả năng chịu lỗi.
- **Duy trì các tập dữ liệu đánh giá như các bộ hồi quy sống:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để theo dõi tỷ lệ vượt qua, và cảnh báo khi có suy giảm qua [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html).
- **Rà soát và mở rộng các kịch bản theo quý:** Đưa vào các mẫu lỗi phát hiện trong các sự cố sản xuất để bộ kiểm thử phát triển cùng hệ thống.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](../2-agentops02/agentops02-bp01.md)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](../4-agentops04/agentops04-bp03.md)
- [AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp](../6-agentops06/agentops06-bp01.md)
- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công phù hợp với hiệu năng cho workload agent](../../4-performance-efficiency/1-agentperf01/agentperf01-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Đánh giá AI agent: Bài học thực tế từ việc xây dựng hệ thống agentic tại Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [Lên kế hoạch cho thất bại: Làm sao để workload generative AI kiên cường hơn](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)

**Video liên quan:**

- [AWS re:Invent 2024 - Best practices for generative AI observability (COP404)](https://www.youtube.com/watch?v=sRjm6HS6yYU)
- [AWS re:Invent 2024 - Unlock the power of generative AI with AWS Serverless (SVS319)](https://www.youtube.com/watch?v=y0jImhzqR1U)

**Ví dụ liên quan:**

- [GitHub: Open Source Bedrock Agent Evaluation](https://github.com/aws-samples/open-source-bedrock-agent-evaluation)
- [GitHub: Sample Agentic Platform on AWS](https://github.com/aws-samples/sample-agentic-platform)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [AWS Fault Injection Service](https://aws.amazon.com/fis/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
