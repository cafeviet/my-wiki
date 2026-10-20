# AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh

Các quy trình phê duyệt nặng nề làm chậm công việc thường lệ và bị lách qua trong các trường hợp khẩn cấp. Mặt khác, việc thiếu các quy trình phê duyệt có thể tạo ra các sự cố ngoài dự kiến. Để giữ cho các nhóm của bạn vận hành trong khi vẫn bảo vệ trước các thay đổi thực sự cần soi xét, hãy triển khai kiểm định phân bậc rủi ro (nhẹ cho các thay đổi nhỏ, kỹ lưỡng cho các lần tăng tự chủ).

**Kết quả mong muốn:**

- Các thay đổi agent đáng kể đi qua các luồng kiểm định và phê duyệt được tài liệu hóa trước khi đến được sản xuất.
- Các điểm kiểm tra (checkpoint) kiểm định xác minh rằng các thay đổi đáp ứng các ngưỡng chất lượng, duy trì sự phù hợp hành vi, và tuân thủ các ranh giới vận hành.
- Các quy trình quay lui được xác định và kiểm thử cho mọi loại thay đổi.
- Gánh nặng phê duyệt tỷ lệ thuận với rủi ro thay đổi, không đồng đều qua mọi thay đổi.

**Các phản mẫu thường gặp (anti-patterns):**

- Áp dụng cùng một quy trình phê duyệt nhẹ cho mọi thay đổi bất kể rủi ro, đối xử một điều chỉnh câu chữ Prompt nhỏ giống như một thay đổi làm tăng mức tự chủ agent hoặc thêm quyền truy cập Tools mới.
- Triển khai các luồng phê duyệt yêu cầu con người ký duyệt cho mọi thay đổi mà không phân bậc theo rủi ro, tạo ra các nút thắt cổ chai làm chậm việc lặp lại và khuyến khích việc lách qua.
- Định nghĩa các điểm kiểm tra kiểm định mà không quy định các tiêu chí phải đạt để vượt qua, khiến người phê duyệt không có tiêu chuẩn khách quan và tạo ra các quyết định không nhất quán.
- Không kiểm thử các quy trình quay lui trước khi chúng cần đến, chỉ phát hiện rằng quay lui bị hỏng khi một sự cố đòi hỏi phục hồi nhanh.
- Xem kiểm định như một cổng triển khai một lần thay vì một quy trình liên tục, bỏ lỡ suy giảm chất lượng sau khi triển khai.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các luồng phê duyệt phân bậc rủi ro giúp định tuyến các thay đổi có tác động tiềm năng đáng kể tới sự soi xét phù hợp của con người, trong khi các thay đổi rủi ro thấp tiến hành với ma sát tối thiểu.
- Kiểm định và phê duyệt được tài liệu hóa tạo ra một hồ sơ có thể kiểm toán cho mọi quyết định thay đổi phục vụ mục đích tuân thủ.
- Các quy trình quay lui đã được kiểm thử nén thời gian ứng phó sự cố khi các thay đổi đã được kiểm định vẫn tạo ra kết quả bất ngờ.
- Các cổng kiểm định tự động bắt được các hồi quy trước khi người phê duyệt thấy được thay đổi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phân bậc rủi ro tạo ra một quy trình phê duyệt khả thi.

- Bậc 1, rủi ro thấp, bao phủ các thay đổi câu chữ Prompt nhỏ, các điều chỉnh cấu hình ghi log, và các chỉnh sửa tương tự không thể làm biến đổi hành vi agent một cách thực chất. Những thay đổi này chỉ yêu cầu kiểm định tự động.
- Bậc 2, rủi ro trung bình, bao phủ các tích hợp Tools mới, các thay đổi cấu trúc Prompt, và các điều chỉnh tham số Model. Những thay đổi này yêu cầu kiểm định tự động cộng với rà soát ngang hàng.
- Bậc 3, rủi ro cao, bao phủ các lần tăng mức tự chủ, các danh mục Tools mới, các thay đổi Model, và các sửa đổi Guardrail. Những thay đổi này yêu cầu kiểm định tự động cộng với phê duyệt đa bên liên quan, bao gồm trưởng nhóm kỹ thuật và chủ sở hữu kinh doanh.

Kiểm định tự động nên chạy trước bất kỳ phê duyệt nào của con người. Các ngưỡng điểm [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html), các kiểm thử hồi quy hành vi, các security scan, và các mốc chuẩn hiệu năng đều đặt cổng cho việc thăng hạng. Một thay đổi không vượt qua kiểm định tự động sẽ không bao giờ tiêu tốn thời gian rà soát của con người, để nhóm tập trung vào các quyết định thực sự cần phán đoán.

Định tuyến phê duyệt cần xử lý các timeout. Một thay đổi chờ một người phê duyệt không sẵn có trong nhiều ngày có nguy cơ bị lách qua hoặc bị bỏ rơi. Leo thang khi timeout, hoặc thông qua phê duyệt tự động cho các thay đổi rủi ro thấp hoặc leo thang tới một người phê duyệt dự phòng cho các thay đổi rủi ro cao hơn, giữ cho quy trình tiếp tục vận hành.

Quay lui là một đường phục hồi cho các thay đổi đã vượt qua kiểm định nhưng vẫn tạo ra kết quả bất ngờ. Quay lui tự động được kích hoạt bởi các vi phạm ngưỡng chất lượng sau triển khai là mặc định, trong khi quay lui thủ công vẫn sẵn có cho các trường hợp biên. Đối với các mẫu giám sát của con người phân bậc trong bối cảnh độ tin cậy, xem [AGENTREL02-BP05 Thiết lập các luồng giám sát và phê duyệt của con người phân bậc](../../3-reliability/2-agentrel02/agentrel02-bp05.md).

### Các bước triển khai

- **Định nghĩa một phân loại thay đổi phân bậc rủi ro:** Nêu rõ các tiêu chí cho Bậc 1, Bậc 2, và Bậc 3 để các thay đổi được phân loại nhất quán.
- **Định nghĩa các điểm kiểm tra kiểm định tự động:** Bao gồm các ngưỡng điểm đánh giá từ [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html), các kiểm thử hồi quy, các security scan, và các mốc chuẩn hiệu năng.
- **Triển khai các luồng phê duyệt:** Định tuyến các thay đổi theo bậc với leo thang khi timeout cho các người phê duyệt không phản hồi.
- **Tự động hóa quay lui khi vượt ngưỡng chất lượng:** Nối các chỉ số chất lượng sau triển khai với các luồng hoàn nguyên.
- **Kiểm thử các quy trình quay lui theo quý:** Tài liệu hóa các kết quả và cập nhật các quy trình khi runtime tiến hóa.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp](agentops06-bp01.md)
- [AGENTOPS06-BP02 Đánh giá và theo dõi hiệu năng agent liên tục](agentops06-bp02.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](../3-agentops03/agentops03-bp02.md)
- [AGENTREL02-BP05 Thiết lập các luồng giám sát và phê duyệt của con người phân bậc](../../3-reliability/2-agentrel02/agentrel02-bp05.md)
- [AGENTSEC04-BP02 Có con người trong vòng lặp cho các quyết định quan trọng](../../2-security/4-agentsec04/agentsec04-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Operationalizing agentic AI, Part 1: A stakeholder's guide](https://aws.amazon.com/blogs/machine-learning/operationalizing-agentic-ai-part-1-a-stakeholders-guide/)
- [Preparing your business for agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/preparing-business.html)
- [Advancing AI agent governance with Boomi and AWS: A unified approach to observability and compliance](https://aws.amazon.com/blogs/machine-learning/advancing-ai-agent-governance-with-boomi-and-aws-a-unified-approach-to-observability-and-compliance)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
