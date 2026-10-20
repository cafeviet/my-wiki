# AGENTREL06-BP03 Kiểm thử hiệu năng hệ thống suy giảm một cách đều đặn

Các tuyên bố về tính bền bỉ chưa từng được kiểm thử trong các điều kiện lỗi thực chỉ là những nguyện vọng. Kỹ thuật hỗn loạn (chaos engineering), tiêm lỗi và kiểm thử tải dưới tài nguyên hạn chế một cách đều đặn phơi bày các khoảng trống trong độ phủ dự phòng trong khi môi trường còn an toàn để phá vỡ.

**Kết quả mong muốn:**

- Bạn có các mẫu thí nghiệm (experiment template) cho các kịch bản lỗi dễ ảnh hưởng đến độ tin cậy của tác nhân nhất.
- Bạn có các tiêu chí chấp nhận (acceptance criteria) được tài liệu hóa cho mỗi kịch bản, bao quát kích hoạt dự phòng kỳ vọng, mức suy giảm chấp nhận được và thời gian phục hồi.
- Bạn chạy các thí nghiệm tiêm lỗi ít nhất hằng tháng và theo dõi các phát hiện qua một backlog cải thiện tính bền bỉ.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ kiểm thử các kịch bản happy-path, chỉ phát hiện ra các khoảng trống về tính bền bỉ trong các sự cố vận hành.
- Chạy kiểm thử suy giảm không thường xuyên, để các thoái lui về tính bền bỉ tích tụ giữa các chu kỳ.
- Kiểm thử các thành phần riêng lẻ trong cô lập mà không có các kịch bản lỗi toàn luồng công việc.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các khoảng trống về tính bền bỉ được phát hiện trước khi chúng đến các sự cố vận hành.
- Các cơ chế dự phòng được kiểm định so với các điều kiện lỗi thực thay vì giả định.
- Sự bảo đảm về tính bền bỉ theo kịp sự tiến hóa của hệ thống thông qua các chu kỳ kiểm thử đều đặn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) là cách được quản lý để tiêm các lỗi có kiểm soát vào hạ tầng tác nhân, tiết lưu, lỗi node, phân mảnh mạng, và quan sát hành vi của hệ thống. Một thí nghiệm chỉ hữu ích bằng các tiêu chí chấp nhận mà nó được so sánh với, nên mỗi kịch bản cần các kỳ vọng được tài liệu hóa. Định nghĩa dự phòng nào nên kích hoạt, mức suy giảm năng lực nào chấp nhận được, và việc phục hồi nên mất bao lâu. Chạy thí nghiệm mà không có tiêu chí cho bạn một bản demo thú vị. Chạy nó với tiêu chí cho bạn một bài kiểm thử thoái lui (regression test).

Hằng tháng là tần suất tối thiểu giữ cho các thoái lui về tính bền bỉ không tích tụ giữa các chu kỳ. Tích hợp kiểm thử suy giảm vào CI/CD chặn triển khai vận hành khi các bài kiểm thử thất bại, và đó là nơi sự bảo đảm về tính bền bỉ thực sự được thực thi. Chạy các thí nghiệm trong các môi trường phi vận hành được thu hẹp phạm vi đủ chặt để bạn không gây ra các sự cố mà bạn đang cố ngăn chặn.

Các ngày diễn tập (game day) mở rộng thực hành sang sự sẵn sàng vận hành. Các ngày diễn tập hằng quý nơi đội vận hành cố ý gây ra các lỗi trong các môi trường giống vận hành kiểm định nhiều hơn là các cơ chế dự phòng kỹ thuật. Chúng cũng diễn tập các runbook vận hành, cấu hình cảnh báo và phản ứng của đội dưới áp lực thời gian. Các phát hiện được tài liệu hóa trong một backlog cải thiện tính bền bỉ và theo dõi tới khắc phục. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) giám sát hành vi hệ thống trong các bài kiểm thử và xác nhận rằng việc phát hiện suy giảm kích hoạt đúng.

### Các bước triển khai

- **Tạo các mẫu thí nghiệm FIS cho các kịch bản rủi ro cao:** Xây dựng các mẫu [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) cho các dạng lỗi dễ ảnh hưởng đến độ tin cậy của tác nhân nhất, được thu hẹp phạm vi vào các môi trường phi vận hành.
- **Định nghĩa các tiêu chí chấp nhận theo từng kịch bản:** Tài liệu hóa kích hoạt dự phòng kỳ vọng, mức suy giảm chấp nhận được và thời gian phục hồi để mỗi thí nghiệm có một mốc đạt/không đạt.
- **Tích hợp kiểm thử suy giảm vào CI/CD:** Chặn triển khai vận hành khi các bài kiểm thử thất bại để sự bảo đảm về tính bền bỉ được thực thi thay vì chỉ là nguyện vọng.
- **Chạy các thí nghiệm ít nhất hằng tháng:** Lên lịch các thí nghiệm FIS theo một nhịp đều đặn và theo dõi kết quả để phát hiện các thoái lui về tính bền bỉ.
- **Chạy các ngày diễn tập hằng quý:** Diễn tập các runbook vận hành, cảnh báo và các quy trình phản ứng của đội trong các điều kiện lỗi có kiểm soát nhưng thực tế.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa](agentrel06-bp01.md)
- [AGENTREL06-BP02 Thiết lập các cơ chế dự phòng cho sự suy giảm của hệ thống kế thừa](agentrel06-bp02.md)
- [AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent](agentrel06-bp04.md)

**Tài liệu liên quan:**

- [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Dịch vụ liên quan:**

- [AWS Fault Injection Service](https://aws.amazon.com/fis/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
