# AGENTOPS03-BP03 Triển khai các chính sách scaling đặc thù agent và lập kế hoạch dung lượng

Các chính sách scaling được thiết kế cho các workload web điển hình không phù hợp với agent. Độ trễ suy luận Model, tình trạng sẵn sàng của các phụ thuộc Tools, và dung lượng dịch vụ hạ nguồn đều định hình phản ứng đúng đối với tải, và một chính sách bỏ qua chúng hoặc cấp phát dư trong giờ thấp điểm hoặc cấp phát thiếu trong giờ cao điểm.

**Kết quả mong muốn:**

- Dung lượng tính toán của agent scale động theo nhu cầu trong khi tôn trọng các ràng buộc về chi phí, hiệu năng, và quản trị.
- Các quyết định scaling tính đến các yếu tố đặc thù agent: độ trễ suy luận Model, tình trạng sẵn sàng của Tools, và dung lượng dịch vụ hạ nguồn.
- Các ranh giới scaling theo từng môi trường giúp ngăn scaling mất kiểm soát ở phát triển trong khi bảo toàn dư địa dung lượng ở sản xuất.
- Các buổi rà soát dung lượng hàng tháng giữ cho các triển khai đúng kích cỡ khi các mẫu sử dụng tiến hóa.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng các cấu hình scaling giống hệt nhau qua mọi môi trường, hoặc cấp phát dư ở phát triển hoặc cấp phát thiếu ở sản xuất trong các đợt tăng vọt lưu lượng.
- Scaling chỉ dựa trên mức sử dụng CPU và bộ nhớ mà không xét các chỉ số đặc thù agent như độ sâu hàng đợi yêu cầu hay độ trễ suy luận, bỏ lỡ nút thắt cổ chai thực sự.
- Đặt các chính sách scaling một lần tại thời điểm triển khai và không bao giờ xem lại khi các mẫu sử dụng tiến hóa.
- Xem lập kế hoạch dung lượng như một bài tập tài chính theo quý thay vì một bài tập vận hành liên tục, khiến các chính sách lệch nhịp với thực tế.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các chính sách scaling thích ứng với bối cảnh triển khai và mô hình tính toán của agent, giữ dung lượng phù hợp khi các workload chuyển từ nguyên mẫu sang quy mô sản xuất.
- Các ranh giới theo từng môi trường và cấu hình tập trung khiến hành vi scaling nhất quán, có thể kiểm toán, và được quản trị qua các môi trường.
- Các buổi rà soát hàng tháng bắt được trôi lệch giữa dung lượng được cấu hình và các mẫu sử dụng thực tế trước khi nó trở thành vấn đề chi phí hay độ trễ.
- Các chỉ số scaling đặc thù agent bộc lộ nút thắt cổ chai thực sự, thường là dung lượng dịch vụ hạ nguồn hoặc điều tiết Model, mà các chỉ số chung che giấu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) xử lý câu hỏi về scaling cho hầu hết các nhóm thông qua mô hình scaling và định giá dựa trên mức tiêu thụ (consumption-based) tích hợp sẵn. AgentCore Runtime phân bổ tính toán tự động dựa trên nhu cầu, nên không cần các chính sách scaling tùy chỉnh. Đối với các agent triển khai ngoài AgentCore Runtime, chẳng hạn trên [AWS Lambda](https://aws.amazon.com/lambda/) hoặc [Amazon ECS](https://aws.amazon.com/ecs/), các tác nhân kích hoạt scaling phải được cấu hình theo các tín hiệu đặc thù agent: độ sâu hàng đợi yêu cầu, độ trễ phản hồi trung bình, và số lượng lời gọi đồng thời. Chỉ riêng CPU và bộ nhớ là chưa đủ vì các agent thường chờ suy luận Model hoặc các Tools hạ nguồn thay vì bão hòa tính toán cục bộ.

Hãy cấu hình các mức tối đa phù hợp với môi trường để kiểm soát chi phí ở phát triển và duy trì hiệu năng ở sản xuất. Phát triển có thể chạy với các mức tối thiểu rộng rãi và mức tối đa chặt. Chi phí là cân nhắc đầu tiên, nên chính sách nên kỳ vọng các đợt tăng vọt và điều tiết chúng. Ở sản xuất, các mức tối đa nên đủ rộng để hấp thụ các đợt bùng nổ lưu lượng mà không suy giảm độ trễ, và các mức tối thiểu nên giữ đủ dung lượng ấm (warm capacity) để tránh khởi động nguội (cold start) trong các đợt tăng nhu cầu. Staging là điểm giữa giữa phát triển và sản xuất, nên các mức tối đa và tối thiểu cũng nên tương ứng.

Hãy lưu các cấu hình scaling tập trung (chẳng hạn trong một kho tham số tích hợp với agent registry) để các ranh giới điều chỉnh tự động khi một agent chuyển tiếp giữa các giai đoạn vòng đời. Một kho cấu hình cũng mang lại cho nhóm một nơi duy nhất để kiểm toán và điều chỉnh các chính sách, thay vì truy lùng chúng qua các console dịch vụ riêng lẻ.

Nhóm vận hành nên thực hiện các buổi rà soát hàng tháng, phân tích lịch sử sự kiện scaling, các mẫu sử dụng cao điểm, và dư địa dung lượng qua danh mục bằng các chỉ số [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/). Các đầu ra là cụ thể:

- Các agent cần giảm quy mô
- Các agent cần nâng trần
- Các dự báo nhu cầu cho kỳ sắp tới

Không có buổi rà soát này, các chính sách scaling trôi lệch khỏi workload mà chúng đã được điều chỉnh theo. Để có tầm nhìn vận hành ở cấp fleet bao gồm dashboard, phát hiện bất thường, và giám sát hành vi, xem [AGENTOPS05-BP05 Tạo các dashboard đặc thù luồng công việc cho sức khỏe vận hành](../5-agentops05/agentops05-bp05.md).

### Các bước triển khai

- **Chọn nền tảng scaling phù hợp:** Triển khai agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để có scaling tích hợp, hoặc cấu hình các chính sách auto scaling với các chỉ số đặc thù agent cho các triển khai ngoài Runtime.
- **Đặt các ranh giới theo từng môi trường:** Dùng các chính sách rộng rãi cho phát triển, vừa phải cho staging, và sản xuất với các mức tối thiểu cao hơn để hấp thụ các đợt tăng vọt lưu lượng.
- **Tập trung hóa các cấu hình scaling:** Lưu các chính sách trong một kho tham số tích hợp với agent registry để các ranh giới điều chỉnh khi các agent chuyển tiếp giữa các giai đoạn vòng đời.
- **Rà soát dung lượng hàng tháng:** Phân tích các sự kiện scaling, mức sử dụng cao điểm, và dư địa dung lượng trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) để đưa các triển khai về đúng kích cỡ và dự báo nhu cầu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](agentops03-bp01.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](agentops03-bp02.md)
- [AGENTOPS02-BP02 Triển khai phát hiện và khắc phục trôi lệch cấu hình](../2-agentops02/agentops02-bp02.md)
- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent](../5-agentops05/agentops05-bp04.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Chuẩn bị doanh nghiệp cho agentic AI ở quy mô lớn](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/preparing-business.html)
- [Introducing Amazon Bedrock AgentCore: Securely deploy and operate AI agents at any scale](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)
- [Securely launch and scale your agents and tools on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/securely-launch-and-scale-your-agents-and-tools-on-amazon-bedrock-agentcore-runtime/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
