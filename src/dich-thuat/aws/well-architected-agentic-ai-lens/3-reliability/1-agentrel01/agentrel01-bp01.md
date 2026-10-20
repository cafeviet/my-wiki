# AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ

Các lời gọi tác nhân-tới-tác nhân trực tiếp làm ràng buộc các dạng lỗi với nhau. Khi một tác nhân lỗi, mọi thứ phía sau cũng lỗi theo. Một lớp nhắn tin với tính bền vững, cơ chế thử lại và xử lý dead-letter hấp thụ các lỗi thoáng qua và cho phép luồng công việc tiếp tục từ chỗ nó đã dừng.

**Kết quả mong muốn:**

- Các tác nhân của bạn giao tiếp qua một lớp nhắn tin trung gian có tính bền vững, thử lại và xử lý dead-letter thay vì các lời gọi đồng bộ trực tiếp.
- Bạn có trạng thái luồng công việc bền vững, sống sót qua việc khởi động lại hoặc mất bất kỳ thành phần đơn lẻ nào.
- Bạn có thể truy vết mọi thông điệp của tác nhân xuyên qua ranh giới đồng bộ và bất đồng bộ.

**Các phản mẫu thường gặp (anti-patterns):**

- Đấu nối các tác nhân qua các lời gọi đồng bộ trực tiếp, khiến một lỗi đơn lẻ lan theo mọi tác nhân phụ thuộc.
- Vận hành hạ tầng nhắn tin không có tính bền vững, khiến việc phục hồi luồng công việc trở nên bất khả thi sau khi một thành phần ngừng hoạt động.
- Coi mọi tương tác là đồng bộ, tạo ra các nút thắt cổ chai chặn hoạt động độc lập của tác nhân.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tính bền vững và thử lại giới hạn các lỗi thoáng qua bên trong lớp nhắn tin thay vì phơi bày chúng thành các sự cố ngừng hoạt động của tác nhân.
- Xử lý dead-letter giúp ngăn các thông điệp độc hại (poison message) chặn việc thực thi luồng công việc lành mạnh.
- Một nền nhắn tin bền vững là nền tảng cho các mẫu điều phối nâng cao, bao gồm saga và arbiter.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Mỗi lời gọi tác nhân-tới-tác nhân là một quyết định về sự ràng buộc. Lời gọi đồng bộ gắn tính khả dụng của bên gọi với tính khả dụng của bên bị gọi. Trong một mạng lưới tác nhân, điều đó nhân lên nhanh chóng. Năm tác nhân với bốn phụ thuộc đồng bộ, và tích khả dụng tụt xuống dưới SLA của bất kỳ tác nhân đơn lẻ nào. Một lớp nhắn tin phá vỡ sự ràng buộc bằng cách đệm lời gọi trong hạ tầng bền vững. Bên gọi phát ra một thông điệp rồi tiếp tục công việc. Bên nhận xử lý nó theo lịch riêng, với việc thử lại và định tuyến dead-letter được xử lý bên ngoài mã của chính tác nhân.

Việc chọn mẫu bám theo hình dạng tương tác. Dùng [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) cho định tuyến dựa trên nội dung, nơi một sự kiện đơn lẻ được phân phát (fan out) tới nhiều bên tiêu thụ, với EventBridge Schema Registry ghi lại hợp đồng giữa các tác nhân. Dùng [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) cho phân phối điểm-tới-điểm bền vững với thời gian chờ hiển thị (visibility timeout) cấu hình được và hàng đợi dead-letter. Dùng Amazon SNS cho phân phát tới nhiều bên tiêu thụ phía dưới.

Tính bền vững của luồng công việc gắn lớp nhắn tin với kết quả kinh doanh. Một thông điệp đã tới hàng đợi của nó vẫn cần điều phối để phối hợp công việc nhiều bước xuyên các tác nhân. [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) lưu bền trạng thái thực thi tại mỗi chuyển tiếp bước, nhờ đó việc phục hồi bắt đầu từ bước hoàn tất gần nhất thay vì từ đầu. Không có tính bền vững đó, một lỗi ở bước năm của luồng bảy bước sẽ thực thi lại mọi bước trước đó, lãng phí tính toán và có nguy cơ gây ra các tác dụng phụ trùng lặp. Xử lý dead-letter bổ trợ cho tính bền vững. Các thông điệp độc hại được cô lập để phân loại xử lý thay vì chặn lưu lượng lành mạnh phía sau chúng.

### Các bước triển khai

- **Lập bản đồ mọi đường giao tiếp của tác nhân và phân loại nó:** Ghi lại mỗi tương tác là giao tiếp trực tiếp đồng bộ (A2A), gọi công cụ ràng buộc lỏng (MCP), hay theo hướng sự kiện bất đồng bộ qua [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html).
- **Cấu hình quy tắc EventBridge và hàng đợi SQS:** Thiết lập định tuyến dựa trên nội dung của Amazon EventBridge cho các đường theo hướng sự kiện và các hàng đợi [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) cho nhắn tin điểm-tới-điểm bền vững.
- **Định nghĩa lược đồ sự kiện trong EventBridge Schema Registry:** Đăng ký một lược đồ cho mỗi loại thông điệp của tác nhân để bên gửi và bên nhận thống nhất về hợp đồng.
- **Cấu hình hàng đợi dead-letter với phân loại xử lý tự động:** Định tuyến các thông điệp lỗi lặp lại tới các DLQ và đấu nối cảnh báo Amazon CloudWatch để người vận hành thấy các thông điệp độc hại trước khi chúng chặn lưu lượng.
- **Trang bị công cụ đo cho lớp nhắn tin với AgentCore Observability:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để truy vết phân tán, nhờ đó bạn có thể theo dõi một thông điệp xuyên qua EventBridge, SQS và ranh giới tác nhân.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](agentrel01-bp02.md)
- [AGENTREL01-BP03 Thiết kế các tác nhân chuyên biệt theo nguyên tắc actor model](agentrel01-bp03.md)
- [AGENTREL01-BP04 Chuẩn hóa các giao thức giao tiếp](agentrel01-bp04.md)

**Tài liệu liên quan:**

- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Operationalizing agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)

**Dịch vụ liên quan:**

- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [Amazon SQS](https://aws.amazon.com/sqs/)
- [Amazon SNS](https://aws.amazon.com/sns/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
