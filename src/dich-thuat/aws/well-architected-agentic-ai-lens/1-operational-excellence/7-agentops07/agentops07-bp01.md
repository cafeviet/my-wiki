# AGENTOPS07-BP01 Triển khai các cơ chế ứng phó và phục hồi tự động

Các agent phục hồi từ lỗi mà không cần con người can thiệp giữ cho dịch vụ tiếp tục chạy và mang lại cho nhóm dữ liệu lỗi mà họ cần để giúp ngăn tái diễn. Phục hồi chỉ bằng thủ công mở rộng kém và có thể biến các suy giảm thường lệ thành sự cố.

**Kết quả mong muốn:**

- Các hệ thống agent phát hiện và phục hồi từ các kịch bản lỗi phổ biến một cách tự động, duy trì tính sẵn sàng của dịch vụ và tính liên tục trải nghiệm người dùng.
- Các ngắt tự động giúp ngăn các lỗi lan truyền lan rộng qua môi trường agent.
- Các chiến lược dự phòng giữ cho các agent suy giảm nhã nhặn thay vì thất bại hoàn toàn khi các năng lực chính không khả dụng.
- Các mục tiêu thời gian phục hồi được xác định, đạt được, và kiểm thử thường xuyên.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai logic thử lại mà không có các ngắt tự động, khiến các agent liên tục gọi các dịch vụ đang lỗi và khuếch đại tải lên các hệ thống suy giảm thay vì thất bại nhanh (fail fast).
- Thiết kế các chiến lược dự phòng âm thầm suy giảm chất lượng mà không thông báo cho người dùng, tạo ra một trải nghiệm kém trong đó người dùng nhận các phản hồi chất lượng thấp mà không hiểu tại sao.
- Không xác định các mục tiêu thời gian phục hồi cho các kịch bản lỗi khác nhau, khiến không thể đánh giá các cơ chế phục hồi có đáp ứng các yêu cầu vận hành hay không.
- Triển khai các cơ chế phục hồi hoạt động một cách biệt lập nhưng thất bại khi kết hợp, bỏ lỡ các kịch bản lỗi trong đó nhiều thành phần suy giảm đồng thời.
- Không bao giờ kiểm thử các quy trình phục hồi dưới các điều kiện lỗi thực tế, chỉ phát hiện các vấn đề trong các sự cố sản xuất thực tế.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phục hồi tự động nắm bắt dữ liệu lỗi chi tiết dẫn dắt cải tiến có hệ thống khả năng chịu lỗi của agent, cho phép các nhóm giải quyết các nguyên nhân gốc thay vì liên tục ứng phó với cùng các sự cố.
- Các năng lực tự chữa lành thích ứng với các bối cảnh lỗi khác nhau, tình trạng Tools không khả dụng nhất thời, các gián đoạn dịch vụ hoàn toàn, và suy giảm Model, với các chiến lược phục hồi tỷ lệ thuận với mức độ nghiêm trọng.
- Các ngắt tự động chặn các lỗi lan truyền tại nguồn thay vì để chúng lan rộng.
- Các bài tập kỹ thuật hỗn loạn (chaos engineering) kiểm định rằng phục hồi hoạt động dưới các điều kiện thực tế, không chỉ trên lý thuyết.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hãy thiết lập các ngắt tự động cho mọi phụ thuộc bên ngoài. Lưu trạng thái cho ngắt (khỏe mạnh, suy giảm, và mở) trong một kho dữ liệu nhanh mà mọi agent có thể đọc. Các ngưỡng phụ thuộc vào đặc tính độ tin cậy của mỗi phụ thuộc. Đặt một ngưỡng tỷ lệ lỗi (ví dụ, 50% lỗi trong cửa sổ 60 giây), một ngưỡng timeout (ví dụ, 5 lần timeout liên tiếp), và một khoảng thăm dò phục hồi (ví dụ, thử phục hồi mỗi 30 giây). Phát các chỉ số [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) trên các chuyển trạng thái để sức khỏe ngắt trở nên thấy được qua môi trường.

Các chiến lược dự phòng cần được thiết kế cho mỗi năng lực, không phải sao chép từ một mẫu. Các lỗi Tools nhận các chuỗi dự phòng: các Tools thay thế với các năng lực tương đương, rồi suy giảm nhã nhặn, rồi leo thang thủ công. Các lỗi suy luận LLM nhận các chuỗi dự phòng Model định tuyến tới các Model thay thế (chẳng hạn Claude 3.5 Sonnet sang Claude 3 Haiku) khi Model chính không khả dụng. Các lỗi phối hợp đa agent nhận các chế độ dự phòng đơn agent xử lý các tác vụ với năng lực giảm bớt thay vì thất bại hoàn toàn. Mỗi dự phòng nên thông báo cho người dùng khi chất lượng bị suy giảm, chứ không âm thầm trả về một câu trả lời tệ hơn.

[AWS Step Functions](https://aws.amazon.com/step-functions/) hoặc điều phối luồng công việc bền vững tương đương xử lý các luồng phục hồi với xử lý lỗi tích hợp, logic thử lại, và các giao dịch bù trừ (compensating transactions). Các endpoint health check cho mỗi agent xác minh tình trạng sẵn sàng của phụ thuộc và báo cáo trạng thái sức khỏe tổng thể.

Giám sát các thời gian phục hồi thực tế so với các mục tiêu cho nhóm biết liệu các cơ chế có thực sự đáp ứng các yêu cầu vận hành hay không. Các bài tập kỹ thuật hỗn loạn theo quý kiểm định rằng phục hồi hoạt động dưới các điều kiện thực tế thay vì chỉ trong các kịch bản luồng thuận lợi mà thiết kế ban đầu dự kiến. Đối với phục hồi tự động tập trung vào độ tin cậy với các mẫu phân loại-định tuyến-leo thang, xem [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi agent](../../reliability-pillar/agentrel07/agentrel07-bp02.xml).

### Các bước triển khai

- **Triển khai các ngắt tự động cho mọi phụ thuộc bên ngoài:** Xác định các ngưỡng cho tỷ lệ lỗi, số lần timeout, và thăm dò phục hồi theo từng phụ thuộc.
- **Thiết kế các chuỗi dự phòng theo từng năng lực agent:** Quy định các Tools, Model, và các thao tác ở chế độ suy giảm thay thế, và thông báo cho người dùng khi chất lượng bị suy giảm.
- **Xây dựng các luồng phục hồi bền vững:** Dùng [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) hoặc tương đương với xử lý lỗi, logic thử lại, và các giao dịch bù trừ.
- **Cấu hình các endpoint health check:** Xác minh tình trạng sẵn sàng của phụ thuộc và báo cáo trạng thái sức khỏe tổng thể cho mỗi agent.
- **Xác định các RTO theo từng kịch bản lỗi:** Giám sát các thời gian phục hồi thực tế so với các mục tiêu trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html).
- **Chạy các bài tập kỹ thuật hỗn loạn theo quý:** Tiêm lỗi trong các môi trường phi sản xuất để kiểm định các cơ chế phục hồi dưới các điều kiện thực tế.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS07-BP03 Bổ sung quản trị thay đổi để đáp ứng các cải tiến kỹ thuật và các yêu cầu kinh doanh](agentops07-bp03.xml)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](../agentops04/agentops04-bp03.xml)
- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](../agentops05/agentops05-bp02.xml)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi agent](../../reliability-pillar/agentrel07/agentrel07-bp02.xml)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Agentic AI in the Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)
- [From AI agent prototype to product: Lessons from building AWS DevOps Agent](https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent)
- [Introducing Amazon Bedrock AgentCore: Securely deploy and operate AI agents at any scale](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
