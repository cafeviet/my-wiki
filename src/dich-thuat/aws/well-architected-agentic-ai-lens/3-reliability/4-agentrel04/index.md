# Điều phối đa tác nhân

Các hệ thống đa tác nhân triển khai phối hợp tập trung, định tuyến dựa trên năng lực và các chuỗi dự phòng định trước sẽ thực thi tác vụ một cách đáng tin cậy ngay cả khi từng tác nhân bị lỗi. Các luồng công việc đa tác nhân phải được điều phối và kiểm soát cao độ để giúp ngăn các lần thực thi tác nhân không đáng tin cậy làm gián đoạn toàn bộ luồng công việc.

| AGENTREL04: Làm thế nào để bạn điều phối các hệ thống đa tác nhân nhằm thực thi tác vụ một cách đáng tin cậy? |
| --- |
|  |

## Mục tiêu năng lực

- Giải quyết xung đột được tập trung ở một **trọng tài (arbiter)** chuyên trách chỉ hành động khi cần phối hợp, nhờ đó các tác nhân chuyên biệt vận hành độc lập mà không phải thương lượng từng bất đồng theo kiểu ngang hàng.
- Các tác nhân được mô tả trong một phân loại năng lực có cấu trúc dẫn dắt định tuyến tất định và thay thế tự động khi một tác nhân ưu tiên không khả dụng.
- Mỗi tác nhân trọng yếu trong một luồng công việc cộng tác có một chuỗi dự phòng tường minh, có thứ tự với các đánh đổi chất lượng được tài liệu hóa, nhờ đó lỗi của từng tác nhân tạo ra năng lực giảm bớt thay vì sụp đổ luồng công việc.
- Bản thân **control plane** có tính dư thừa, bền vững và ràng buộc lỏng với các tác nhân, nhờ đó hạ tầng phối hợp ít nhất cũng đáng tin cậy như các tác nhân mà nó phối hợp.
- Các quyết định trọng tài, kết quả định tuyến, các lần kích hoạt dự phòng và sức khỏe control plane đều quan sát được như telemetry hạng nhất, và các dạng lỗi được kiểm định qua các bài diễn tập tiêm lỗi và phục hồi thảm họa đều đặn.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với điều phối đa tác nhân như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Các tác nhân phối hợp trực tiếp với nhau, nên các xung đột tạo ra bế tắc (deadlock), phụ thuộc vòng, hoặc trạng thái không nhất quán. Điều phối gán cứng các định danh tác nhân cụ thể, các đường dự phòng vắng bóng, và control plane thường chạy như một thể hiện đơn với trạng thái trong bộ nhớ. Các lỗi đa tác nhân chỉ được chẩn đoán sau sự cố. |
| 2 | Manh nha (Emerging) | Một trọng tài trung tâm tồn tại cho việc giải quyết xung đột trọng yếu, và các tác nhân được đăng ký trong một danh mục đơn giản mà các bộ điều phối tham vấn để định tuyến. Logic dự phòng cơ bản xử lý các lỗi của tác nhân chính, dù hành vi dự phòng chỉ diễn ra một lần cho mỗi luồng công việc. Control plane dùng các dịch vụ được quản lý như [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để thực thi, nhưng trạng thái luồng công việc không được lưu bền đầu-tới-cuối. |
| 3 | Xác lập (Defined) | Các chính sách trọng tài được tách ra khỏi mã nhị phân của trọng tài và lưu trong [Parameter Store, một năng lực của AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) hoặc [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html), với việc leo thang tới con người qua [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) cho các xung đột không giải quyết được. Các tác nhân được đăng ký trong [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) với siêu dữ liệu năng lực có cấu trúc và được khám phá qua tìm kiếm ngữ nghĩa. Các chuỗi dự phòng được tài liệu hóa cho mỗi tác nhân trọng yếu, và điều phối luồng công việc dùng [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) cho trạng thái bền vững. |
| 4 | Chủ động (Proactive) | Trọng tài theo hướng sự kiện qua [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html), chỉ kích hoạt để giải quyết xung đột thay vì làm trung gian cho mọi thông điệp. Việc đăng ký năng lực được tự động hóa trong CI/CD để registry luôn khớp với trạng thái đã triển khai. Kiểm tra sức khỏe chủ động qua điểm cuối /ping của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) dẫn dắt việc kích hoạt dự phòng mà không cần chờ timeout, và các bài diễn tập [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) kiểm định các chuỗi dự phòng theo lịch. Các tác nhân dung thứ được các đợt ngừng hoạt động ngắn của control plane vì chúng được thiết kế để hoàn tất công việc đang chạy một cách độc lập. |
| 5 | Tối ưu (Optimized) | Các chính sách trọng tài, quyết định định tuyến và các tầng dự phòng được hiệu chỉnh lại liên tục từ telemetry của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) thay vì qua các chu kỳ rà soát định kỳ. Các điểm nóng tranh chấp và khoảng trống năng lực nổi lên trong [Amazon CloudWatch Contributor Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html) và dẫn dắt việc thiết kế lại có mục tiêu các giao thức phối hợp. Các bài diễn tập phục hồi thảm họa là thường quy, failover của control plane được tự động hóa một cách chứng minh được, và tổ chức đóng góp lại các mẫu điều phối đa tác nhân cho các cộng đồng thực hành nội bộ của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các đội để các tác nhân phối hợp ngang hàng mà không có một trọng tài chuyên trách, tạo ra bế tắc và kết quả không nhất quán mỗi khi các tác nhân tranh giành cùng một tài nguyên.
- Điều phối gán cứng các định danh tác nhân cụ thể, nên định tuyến không thể thích ứng khi các tác nhân được thay thế hoặc trở nên không khả dụng, và các thay đổi tác nhân đòi hỏi thay đổi mã điều phối.
- Các chuỗi dự phòng tồn tại cho các tác nhân trọng yếu nhưng không bao giờ được diễn tập, nên các khoảng trống trong độ phủ bị phát hiện trong các sự cố vận hành thay vì các bài kiểm thử tiêm lỗi.
- Control plane bị coi là một điểm lỗi đơn với trạng thái trong bộ nhớ, nên lỗi của nó làm mất bối cảnh phối hợp và làm gián đoạn mọi tác nhân cùng lúc.
- Chi phí phối hợp gộp và chất lượng là các số liệu duy nhất được theo dõi, nên các điểm nóng tranh chấp và các lỗi khớp năng lực vẫn vô hình cho tới khi chúng chi phối trải nghiệm mà người dùng nhìn thấy.

###### Các thực hành tốt

- [AGENTREL04-BP01 Triển khai mẫu tác nhân trọng tài (arbiter) cho các hệ thống đa tác nhân được phối hợp](agentrel04-bp01.md)
- [AGENTREL04-BP02 Phân loại các tác nhân bằng một phân loại năng lực kỹ lưỡng](agentrel04-bp02.md)
- [AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác](agentrel04-bp03.md)
- [AGENTREL04-BP04 Triển khai các control plane bền bỉ cho việc phối hợp tác nhân](agentrel04-bp04.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
