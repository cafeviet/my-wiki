# AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi

Một Prompt định hình hành vi agent trực tiếp hơn gần như bất kỳ tài liệu cấu hình nào khác. Hãy tạo một vòng đời Prompt áp dụng kỷ luật ngang tầm mã nguồn, gồm đánh phiên bản, rà soát, đánh giá, và quay lui cho Prompt, giúp tránh trôi lệch Prompt không được phát hiện và các quyết định suy giảm trong tương tác agent.

**Kết quả mong muốn:**

- Bạn quản lý Prompt của agent qua một vòng đời được xác định: soạn thảo, rà soát, kiểm thử, triển khai, giám sát, và ngừng sử dụng.
- Mỗi Prompt sản xuất có lịch sử phiên bản được tài liệu hóa, một hồ sơ đánh giá, và một chủ sở hữu rõ ràng.
- Bạn triển khai cập nhật Prompt độc lập với mã ứng dụng và quay lui về một phiên bản trước trong vòng vài phút.
- Bạn theo dõi tác động hiệu năng của mỗi thay đổi Prompt theo thời gian và có thể quy các dịch chuyển chất lượng về các phiên bản cụ thể.

**Các phản mẫu thường gặp (anti-patterns):**

- Hardcode Prompt trực tiếp trong mã ứng dụng, khiến không thể cập nhật hành vi agent nếu không triển khai lại toàn bộ mã và chặn việc lặp lại Prompt một cách độc lập.
- Triển khai các thay đổi Prompt trực tiếp vào sản xuất mà không đánh giá so với các mốc chuẩn chất lượng, chỉ phát hiện hồi quy sau khi người dùng báo cáo.
- Vận hành mà không có lịch sử phiên bản Prompt, khiến không thể xác định thay đổi Prompt nào đã gây ra hồi quy hành vi hoặc quay lui về một phiên bản tốt đã biết.
- Xem các thay đổi Prompt là quá nhỏ để cần rà soát, để các chỉnh sửa tùy ứng tích tụ thành trôi lệch mà không ai sở hữu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các thay đổi hành vi tuân theo một đường nhất quán, có thể kiểm toán từ soạn thảo tới triển khai, giảm rủi ro vận hành và cho phép quay lui tin cậy.
- Theo dõi hiệu năng Prompt và đánh giá tạo ra một cơ sở thực nghiệm cho việc lặp lại. Mỗi cập nhật được kiểm định so với các tiêu chí chất lượng đo lường được trước khi vào sản xuất.
- Các nhóm có thể triển khai thay đổi Prompt độc lập với mã ứng dụng, rút ngắn vòng lặp phản hồi giữa nhu cầu kinh doanh và hành vi tại runtime.
- Các cập nhật Prompt thất bại được hoàn nguyên trong vài phút thay vì cần ứng phó sự cố.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hãy xem Prompt như các tài liệu vận hành hạng nhất với cùng kỷ luật áp dụng cho mã ứng dụng. Mã ứng dụng đi qua kiểm soát phiên bản, rà soát mã, kiểm thử tự động, triển khai theo giai đoạn, và quay lui được tài liệu hóa. Hầu hết tổ chức không áp dụng bất kỳ điều nào trong số này cho Prompt, dẫn tới hành vi agent trôi lệch. Hãy áp dụng cùng vòng đời cho Prompt như bạn làm với mã, trong đó bạn đặt tên các giai đoạn một cách rõ ràng và yêu cầu các thay đổi tuân theo chúng.

[Amazon Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html) cung cấp đánh phiên bản, metadata, và tích hợp với [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html). Đối với các đường không cần mã (no-code) xây dựng với [Amazon Quick Suite](https://aws.amazon.com/quicksuite/), cùng các giai đoạn được áp dụng qua cấu hình danh tính và chỉ dẫn. Một vòng đời bốn giai đoạn phù hợp với hầu hết các nhóm:

- Draft (đang phát triển, chưa triển khai)
- Review (đang rà soát ngang hàng và đánh giá)
- Active (đã triển khai vào sản xuất)
- Archived (đã ngừng sử dụng nhưng vẫn lưu để kiểm toán)

Hãy đặt cổng cho các chuyển giai đoạn bằng các luồng phê duyệt triển khai trong [AWS CodePipeline](https://aws.amazon.com/codepipeline/) hoặc [AWS Step Functions](https://aws.amazon.com/step-functions/), chứ không phải bằng quy ước.

Mỗi mục Prompt cần metadata bắt buộc: mục đích, agent mục tiêu, hành vi kỳ vọng, tiêu chí đánh giá, và chủ sở hữu. Nên dùng tham số hóa (parameterization) để giảm trùng lặp giữa các agent liên quan. Các tệp điều hướng (steering files) trong Kiro hoặc các quy ước tương đương hệ thống hóa các chuẩn này để chúng được áp dụng tự động trong quá trình phát triển thay vì áp đặt sau khi đã rồi.

[Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) chạy mỗi phiên bản Prompt trên một tập dữ liệu chuẩn hóa và tạo điểm cho thành công tác vụ, độ liên quan của phản hồi, và mức tuân thủ các hướng dẫn hành vi. Một Prompt không đạt các ngưỡng tối thiểu sẽ không được thăng từ review lên active. Một khi đã ở sản xuất, các chỉ số chất lượng được công bố lên [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) dưới dạng chỉ số tùy chỉnh sẽ cảnh báo sớm cho nhóm khi một Prompt đã vượt qua đánh giá bắt đầu suy giảm trong thực tế, kích hoạt một luồng rà soát.

### Các bước triển khai

- **Dựng kho Prompt trung tâm:** Cấu hình [Amazon Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html) với bốn giai đoạn vòng đời (draft, review, active, archived) và các trường metadata bắt buộc (mục đích, agent mục tiêu, hành vi kỳ vọng, tiêu chí đánh giá, chủ sở hữu).
- **Định nghĩa các chuẩn soạn thảo Prompt:** Quy định metadata bắt buộc, quy ước định dạng, và yêu cầu tài liệu. Áp dụng chúng qua các mẫu dùng chung hoặc tệp điều hướng (steering files) để chúng được áp đặt trong quá trình phát triển.
- **Xây dựng các tập dữ liệu đánh giá có phiên bản:** Tạo các tập dữ liệu cho các trường hợp sử dụng chính của mỗi agent và lưu chúng với đánh phiên bản được bật để kết quả đánh giá có thể tái lập.
- **Đặt cổng chuyển tiếp trên đánh giá tự động:** Cấu hình một pipeline [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) chạy trên mỗi lần chuyển từ draft sang review, với các ngưỡng chất lượng tối thiểu.
- **Áp đặt các giai đoạn vòng đời trong CI/CD:** Dùng [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html) để chặn thăng lên active nếu không có phê duyệt và kiểm tra ngưỡng đánh giá.
- **Tham chiếu Prompt theo ID, không theo giá trị:** Triển khai agent với tham chiếu tham số hóa tới kho Prompt thay vì chuỗi hardcode, để Prompt tiến hóa độc lập với mã ứng dụng.
- **Giám sát Prompt active trong sản xuất:** Công bố các chỉ số chất lượng lên [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html), xây dashboard theo từng agent, và cấu hình cảnh báo kích hoạt luồng rà soát khi ngưỡng bị vượt.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS01-BP03 Phát triển các kịch bản kiểm thử phản ánh chính xác lỗi của các thành phần phụ thuộc, giao thức điều phối và quy trình kinh doanh](../1-agentops01/agentops01-bp03.md)
- [AGENTOPS02-BP03 Triển khai năng lực đánh phiên bản và quay lui hành vi agent](agentops02-bp03.md)
- [AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp](../6-agentops06/agentops06-bp01.md)
- [AGENTREL02-BP04 Phát triển các giao thức chỉ dẫn rõ ràng cho agent](../../3-reliability/2-agentrel02/agentrel02-bp04.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)
- [AI agent trong doanh nghiệp: Thực hành tốt với Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)
- [Kiro](https://kiro.dev/)
- [Kiro Steering](https://kiro.dev/docs/steering/)

**Video liên quan:**

- [AWS 2025 - Amazon Bedrock Prompt Management Demo](https://www.youtube.com/watch?v=CE_-zrMvcuk)
- [AWS re:Invent 2024 - Responsible generative AI: Evaluation best practices and tools (AIM342)](https://www.youtube.com/watch?v=wuVpCc5a81Y)

**Ví dụ liên quan:**

- [GitHub: Sample Bedrock Evaluation Adapter](https://github.com/aws-samples/sample-bedrock-evaluation-adapter)
- [GitHub: Sample Bedrock Model Evaluation](https://github.com/aws-samples/sample-bedrock-model-evaluation)
- [GitHub: Amazon Bedrock Samples, GenAI Quick-Start PoCs](https://github.com/aws-samples/genai-quickstart-pocs)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
