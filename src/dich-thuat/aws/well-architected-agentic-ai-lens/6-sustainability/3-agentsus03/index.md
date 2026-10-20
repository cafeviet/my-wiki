# Quản trị Agent (Agent governance)

Các tổ chức thiết kế có chủ ý cách các Agent tương tác với người dùng và các quy trình kinh doanh sẽ duy trì được cả giá trị tự động hóa lẫn chuyên môn nội bộ khi việc áp dụng mở rộng quy mô. Khi các Agent sinh sôi, có rủi ro rằng chuyên môn nội bộ sẽ bị pha loãng hoặc mất đi cho các quy trình được tự động hóa hoàn toàn. Các mẫu quản lý tương tác Agent phải được thiết kế và duy trì có chủ ý, thiết lập các cách tiếp cận tái sử dụng được dựa trên nhu cầu tổ chức thực tế.

| AGENTSUS03: Làm thế nào để tôi thiết lập các mẫu bền vững cho tương tác của Agent với người dùng và các quy trình kinh doanh? |
| --- |
|  |

## Mục tiêu năng lực

- Các năng lực tổ chức được phân loại có chủ ý qua các tầng con-người-sở-hữu, Agent-tăng-cường và tự-động-hóa-hoàn-toàn, với ranh giới rõ ràng được thực thi bởi các chính sách định tuyến và guardrail.
- Việc phát triển Agent nhắm vào các quy trình mà tổ chức đã thành thạo, để tự động hóa tăng tốc các quy trình đã kiểm chứng thay vì thay thế cho việc khám phá quy trình.
- Các Agent xuất xưởng kèm theo các đặc tả khai báo, đồ thị phụ thuộc và tài liệu chính sách luôn được cập nhật khi Agent tiến hóa, để tri thức tổ chức được bảo tồn ở dạng dễ truy cập.
- Một danh mục trung tâm các Agent đã triển khai ghi lại chủ sở hữu, mục đích, phụ thuộc và mức sử dụng, và các nhóm tham vấn nó trước khi xây dựng Agent mới.
- Danh mục Agent được hợp lý hóa (rationalize) chủ động, với các Agent không hoạt động được gắn cờ để rà soát, được loại bỏ qua một vòng đời có cấu trúc, và hạ tầng thu hồi được trả về nguồn dùng chung.

## Các mức độ trưởng thành

Các mức này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với quản trị Agent nói chung.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các Agent được xây và triển khai mà không phân tầng năng lực, gán quyền sở hữu hay giám sát danh mục. Tài liệu mỏng, việc loại bỏ chỉ diễn ra một lần, và tri thức tổ chức chỉ nằm ở các nhà phát triển ban đầu thay vì được ghi lại trong bất kỳ đặc tả nào. |
| 2 | Mới nổi (Emerging) | Các nhóm đã phân loại năng lực thành các tầng con-người-sở-hữu, Agent-tăng-cường và tự-động-hóa-hoàn-toàn, và [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) đã được áp dụng cho việc chuyển lên cấp cao (escalation) trong các tình huống nhiều rủi ro. Cấu hình khai báo trong [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) nắm bắt đặc tả Agent cơ sở. Siêu dữ liệu quyền sở hữu cơ bản được ghi lại cho mỗi Agent đã triển khai. |
| 3 | Đã định hình (Defined) | Các quy trình được ghi chép cung cấp cho việc phát triển Agent qua các nguồn RAG của [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), và định tuyến của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) tách các tác vụ thường quy khỏi các trường hợp cần phán đoán của con người. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) so sánh đầu ra Agent với các đường cơ sở của chuyên gia, và các chương trình luân phiên giữ cho các chuyên gia lĩnh vực (subject matter expert) luôn thực hành công việc nền tảng. Một danh mục Agent trung tâm với quyền sở hữu và mục đích được duy trì. |
| 4 | Chủ động (Proactive) | Tài liệu tạo ở thời điểm chạy sinh ra qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) xác thực các đặc tả thiết kế đối chiếu với hành vi thực tế, và việc thăng cấp lên production bị chặn cửa (gated) dựa trên tài liệu hiện hành. Các chỉ số [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) gắn cờ các Agent không hoạt động để chủ sở hữu rà soát, và một vòng đời loại bỏ có cấu trúc chuyển các Agent qua các trạng thái hoạt động, đang rà soát, ngừng dùng (deprecated) và đã loại bỏ. Các đợt rà soát hợp lý hóa danh mục hàng quý là một nhịp thường trực. |
| 5 | Tối ưu (Optimized) | Quản trị mang tính liên tục thay vì định kỳ. Các chỉ số sức khỏe danh mục (tổng số Agent, phần trăm có sử dụng tích cực, phần trăm có tài liệu hiện hành) được rà soát ở cấp tổ chức. Độ hiện hành của đặc tả, các đường cơ sở đánh giá và việc phân tầng năng lực điều chỉnh dựa trên telemetry vận hành, và tổ chức chia sẻ các mẫu quản trị Agent của mình với các cộng đồng thực hành. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm tự động hóa các quy trình chưa quen thuộc hoặc hiểu chưa thấu, nơi tiêu chí quyết định và chỉ số thành công chưa được ghi chép, nên việc phát triển Agent lãng phí tài nguyên vào các phương pháp chưa được kiểm chứng.
- Các tổ chức bỏ qua việc phân tầng năng lực, nên các Agent rốt cuộc xử lý các quyết định nhiều rủi ro hoặc mơ hồ vốn nên được định tuyến tới các chuyên gia con người, và chuyên môn lĩnh vực âm thầm mai một.
- Các nhóm coi việc phát triển Agent như các tạo tác chỉ-là-mã (code-only) mà không nắm bắt các mẫu ra quyết định của chuyên gia và lý do đằng sau logic kinh doanh, để tri thức tổ chức bị khóa bên trong các bản hiện thực mà chỉ các nhà phát triển ban đầu hiểu.
- Các Agent được triển khai mà không gán quyền sở hữu hay theo dõi mức sử dụng, nên không có cơ sở để đánh giá liệu một Agent có còn mang lại giá trị hay đã rơi vào tình trạng không dùng.
- Các nhóm xây các Agent mới cho các năng lực vốn đã tồn tại ở nơi khác trong tổ chức vì không ai tìm trong danh mục trước, tạo ra các bản hiện thực dư thừa và làm suy yếu việc tái sử dụng.

###### Các thực hành tốt

- [AGENTSUS03-BP01 Duy trì các kỹ năng và năng lực tổ chức](agentsus03-bp01.md)
- [AGENTSUS03-BP02 Xây dựng các Agent phản chiếu các kỹ năng và năng lực tổ chức của bạn](agentsus03-bp02.md)
- [AGENTSUS03-BP03 Duy trì các đặc tả toàn diện cho Agent và hệ thống dạng tác nhân](agentsus03-bp03.md)
- [AGENTSUS03-BP04 Loại bỏ các Agent không dùng và ngăn tình trạng bùng nổ Agent (agent sprawl)](agentsus03-bp04.md)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
