# Hành vi tác nhân có thể dự đoán

Các tác nhân kết hợp các thành phần tính toán, bộ nhớ, nhận thức và điều phối, và mỗi thành phần đều là một điểm mà luồng công việc có thể thất bại. Những tổ chức vận hành tác nhân trên nền nhắn tin bền bỉ, cô lập lỗi theo mô-đun và cấp phát thích ứng sẽ tốn ít thời gian sửa chữa hạ tầng hơn và dành nhiều thời gian hơn để cải thiện năng lực của tác nhân.

| AGENTREL01: Làm thế nào để tôi phát triển các hệ thống tác nhân đáng tin cậy? |
| --- |
|  |

## Mục tiêu năng lực

- Giao tiếp giữa tác nhân với tác nhân và giữa tác nhân với hệ thống chạy qua một nền nhắn tin bền vững (durable messaging substrate), nhờ đó các lỗi thoáng qua được hấp thụ thông qua tính bền vững, cơ chế thử lại và xử lý dead-letter thay vì lan truyền khắp luồng công việc.
- Tính toán, bộ nhớ, nhận thức và điều phối vận hành như các lớp độc lập với hợp đồng (contract) được định nghĩa rõ ràng, nhờ đó một đợt tăng đột biến hay lỗi ở một lớp vẫn được cô lập và các lớp còn lại tiếp tục hoạt động ở một chế độ suy giảm đã biết.
- Mỗi tác nhân chuyên biệt sở hữu một năng lực duy nhất, trạng thái riêng của nó, và phạm vi quyền hạn hẹp, nhờ đó lỗi được cô lập ở đúng tác nhân gặp phải và môi trường rộng hơn vẫn tiếp tục chạy.
- Giao tiếp liên tác nhân tuân theo một phân loại (taxonomy) nhất quán về lược đồ thông điệp, điểm cuối (endpoint) có phiên bản, định dạng lỗi và chính sách thử lại, nhờ đó các tác nhân kết hợp thành luồng công việc mà không cần lớp phiên dịch tùy biến giữa từng cặp.
- Việc cấp phát tính toán, suy luận và tầng mô hình thích ứng theo thời gian thực với các tín hiệu tải và dung lượng, nhờ đó tác nhân duy trì hiệu năng ổn định dưới tải biến động mà không cần lập kế hoạch dung lượng thủ công.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với hành vi tác nhân có thể dự đoán như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Các tác nhân gọi trực tiếp lẫn nhau qua các kênh đồng bộ với định dạng thông điệp tùy tiện và không có hàng đợi bền vững nào giữa chúng. Một tác nhân chậm hoặc lỗi lan sang phần còn lại của luồng công việc, và không có cách nhất quán để truy vết xem chặng nào đã làm mất thông điệp. Dung lượng được cấp phát tĩnh, nên các đợt tăng nhu cầu gây ra tiết lưu (throttling) còn giai đoạn nhu cầu thấp thì lãng phí tài nguyên. |
| 2 | Manh nha (Emerging) | Các đội đã đưa vào một lớp nhắn tin (thường là [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) và [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)) cho các đường tác nhân-tới-tác nhân quan trọng nhất, và các hàng đợi dead-letter bắt các lỗi lặp lại. Các tác nhân chạy trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với sự phân tách lớp cơ bản, và suy luận [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) theo nhu cầu (on-demand) hấp thụ phần lớn biến động dung lượng. Các lược đồ giao tiếp được tài liệu hóa nhưng chưa được thực thi đồng nhất. |
| 3 | Xác lập (Defined) | Nhắn tin bền vững là mặc định cho giao tiếp tác nhân-tới-tác nhân và tác nhân-tới-hệ thống, với các lược đồ đăng ký trong [EventBridge Schema Registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema-registry.html) và các luồng công việc được điều phối qua [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html). Các tác nhân chuyên biệt chạy như các actor đơn mục đích trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với vai trò IAM được thu hẹp phạm vi, giao tiếp qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) hoặc [giao thức A2A](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html), và phơi bày số liệu theo từng tác nhân qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Việc chọn mô hình theo tầng định tuyến các tác vụ đơn giản đến các mô hình nhỏ hơn và công việc suy luận nặng đến các mô hình lớn hơn. |
| 4 | Chủ động (Proactive) | Logic fail-fast, các hành vi dự phòng và bật/tắt năng lực lúc chạy (runtime capability toggling) được thực thi tự động tại ranh giới các lớp, và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thực thi kiểm soát truy cập chuẩn hóa tại ranh giới gateway qua các chính sách [Cedar](https://docs.cedarpolicy.com/). [Suy luận đa Vùng (Cross-Region inference)](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) là mặc định cho các tác nhân vận hành, và [Bedrock Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) bảo đảm cho các đường nhạy độ trễ. Các bài kiểm thử hợp đồng (contract tests) trong CI/CD giúp ngăn thoái lui giao thức, và việc mở rộng theo lịch cấp phát dung lượng trước các mẫu nhu cầu đã biết. |
| 5 | Tối ưu (Optimized) | Nền nhắn tin, sự cô lập lớp, các hợp đồng liên tác nhân và việc cấp phát dung lượng được hiệu chỉnh lại liên tục từ dữ liệu quan trắc (observability) thay vì rà soát theo nhịp cố định. Các luồng công việc mới thừa hưởng mẫu bền bỉ theo mặc định thông qua các mẫu dùng lại và dịch vụ dùng chung, và tổ chức đóng góp lại các mẫu độ tin cậy của tác nhân (topo nhắn tin, phong bì fail-fast, định tuyến mô hình theo tầng) cho các cộng đồng thực hành của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các đội đấu nối giao tiếp tác nhân-tới-tác nhân qua các lời gọi đồng bộ trực tiếp và chỉ phát hiện ra sự ràng buộc khi độ trễ hoặc lỗi của một tác nhân làm sập toàn bộ luồng công việc.
- Các kiến trúc tác nhân được xuất xưởng như một dịch vụ đơn nhất thay vì các lớp tính toán, bộ nhớ, nhận thức và điều phối tách biệt, nên một sự cố ở bất kỳ thành phần nào buộc phải khởi động lại toàn bộ thay vì một bản vá được cô lập.
- Các tác nhân chuyên biệt tích tụ các công cụ không liên quan và các system prompt rộng hơn theo thời gian, mở rộng bán kính lỗi và khiến các sự cố khó tái lập hơn khi trách nhiệm bị nhòe đi.
- Lược đồ thông điệp, định dạng lỗi và chính sách thử lại được định nghĩa theo từng cặp tác nhân thay vì trên toàn đội tác nhân, nên mỗi tác nhân mới đưa vào lớp phiên dịch riêng và mỗi thay đổi đều có nguy cơ phá vỡ một bên tiêu thụ phía dưới.
- Dung lượng được cấp phát cho trường hợp xấu nhất thay vì thích ứng theo nhu cầu. Lưu lượng đỉnh vẫn gây tiết lưu dù chỗ khác còn dư địa nhàn rỗi, và các giai đoạn nhu cầu thấp vẫn phải trả tiền cho dung lượng không dùng.

###### Các thực hành tốt

- [AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ](agentrel01-bp01.md)
- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](agentrel01-bp02.md)
- [AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model](agentrel01-bp03.md)
- [AGENTREL01-BP04 Chuẩn hóa các giao thức giao tiếp](agentrel01-bp04.md)
- [AGENTREL01-BP05 Triển khai cấp phát thích ứng](agentrel01-bp05.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
