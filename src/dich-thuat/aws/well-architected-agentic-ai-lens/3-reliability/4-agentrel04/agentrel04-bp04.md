# AGENTREL04-BP04 Triển khai các control plane bền bỉ cho việc phối hợp tác nhân

Một **control plane** bị lỗi kéo theo mọi tác nhân. Áp dụng cùng các nguyên tắc độ tin cậy đã dùng cho tác nhân, tức là dư thừa, trạng thái bền vững và ràng buộc lỏng, cho hạ tầng phối hợp giữ cho các luồng công việc tiếp tục chạy trong các đợt ngừng hoạt động ngắn và bảo toàn trạng thái qua các lần khởi động lại.

**Kết quả mong muốn:**

- Bạn triển khai các tác nhân trên hạ tầng thực thi được quản lý, độ khả dụng cao với dư thừa đa AZ.
- Bạn lưu bền trạng thái luồng công việc để control plane có thể phục hồi mà không mất tiến độ.
- Bạn thiết kế các tác nhân để hoàn tất công việc đang chạy trong các đợt ngừng hoạt động ngắn của control plane thay vì thất bại ngay lập tức.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai control plane như một điểm lỗi đơn không có dư thừa, nên các đợt ngừng hoạt động hạ gục toàn bộ hệ thống đa tác nhân.
- Giữ trạng thái control plane trong bộ nhớ tạm thời (ephemeral), làm mất trạng thái phối hợp mỗi khi control plane khởi động lại.
- Ràng buộc chặt việc thực thi tác nhân với tính khả dụng của control plane, làm giảm khả năng của tác nhân trong việc hoàn tất công việc đang tiến hành trong các đợt ngừng hoạt động ngắn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các luồng công việc đa tác nhân tiếp tục chạy qua các lỗi thành phần của control plane.
- Lưu bền trạng thái bền vững giảm mất trạng thái luồng công việc trong các đợt ngừng hoạt động.
- Ràng buộc lỏng giữ cho các tác nhân năng suất trong thời gian control plane tạm không khả dụng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

AgentCore Runtime được thiết kế như một dịch vụ theo vùng (regional). Kiến trúc các tác nhân của bạn với giả định rằng tính toán bên dưới được phân bố qua các Availability Zone, nhưng hãy kiểm định giả định này cho khối lượng công việc cụ thể của bạn bằng cách xác nhận hành vi điểm cuối trong lúc AZ bị suy yếu (ví dụ dùng các triển khai canary được cô lập theo AZ). Đừng chỉ dựa vào dư thừa ở cấp dịch vụ. Triển khai các mẫu bền bỉ đa AZ của riêng bạn (triển khai đa AZ cho các bộ điều phối tác nhân, failover theo vùng cho các thành phần có trạng thái) để duy trì các mục tiêu khả dụng độc lập với kiến trúc nội bộ của bất kỳ dịch vụ đơn lẻ nào.

Trạng thái bền vững giữ cho việc phục hồi sạch sẽ. [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) lưu bền trạng thái thực thi tại mỗi chuyển tiếp, cung cấp cơ chế thử lại, xử lý lỗi và tiếp-tục-từ-lỗi tích hợp sẵn cho các luồng công việc cần các máy trạng thái tường minh. Không có trạng thái bền vững, mỗi lần khởi động lại control plane đòi hỏi các tác nhân tự phục hồi bối cảnh phối hợp, điều này dễ sai và thường không đầy đủ.

Ràng buộc lỏng là thuộc tính thứ ba, và khó xây dựng vào sau nhất. Các tác nhân nên hoàn tất các tác vụ đang chạy một cách độc lập nếu control plane tạm không khả dụng, thay vì thất bại ngay lập tức khi mất kết nối. Các cơ chế nhịp tim (heartbeat) cho phép các tác nhân báo trạng thái định kỳ để control plane có thể phát hiện các nhịp tim bị lỡ và gán lại tác vụ, bắt các trường hợp một tác nhân đã thực sự ngừng phản hồi. Giám sát điểm cuối /ping của AgentCore Runtime cho mỗi tác nhân như tín hiệu sống (liveness), và cấu hình lớp điều phối để gán lại tác vụ khi các tác nhân ngừng phản hồi. Các cảnh báo tổng hợp (composite alarms) qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) gộp các tín hiệu qua các thành phần phối hợp. Các bài diễn tập phục hồi thảm họa đều đặn kiểm định rằng failover tự động thực sự hoạt động khi bạn cần.

### Các bước triển khai

- **Triển khai các tác nhân trên AgentCore Runtime:** Dùng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) làm hạ tầng thực thi chính vì dư thừa đa AZ tích hợp sẵn của nó.
- **Dùng AWS Step Functions cho các máy trạng thái luồng công việc tường minh:** Chạy các luồng công việc trên [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) để lưu bền trạng thái bền vững và phục hồi tự động.
- **Dùng AgentCore Gateway cho khám phá và gọi tác nhân:** Định tuyến các lời gọi tác nhân qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) vì các đặc tính khả dụng tích hợp sẵn của nó.
- **Thiết kế các tác nhân để hoàn tất công việc đang chạy trong các đợt ngừng hoạt động ngắn của control plane:** Tránh các mẫu đòi hỏi kết nối control plane liên tục.
- **Triển khai phát hiện sống của tác nhân qua điểm cuối /ping của AgentCore Runtime:** Giám sát điểm cuối cho mỗi tác nhân và gán lại tác vụ qua lớp điều phối khi các tác nhân ngừng phản hồi.
- **Chạy các bài diễn tập phục hồi thảm họa đều đặn:** Dùng các cảnh báo tổng hợp của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và các bài diễn tập DR định kỳ để kiểm định failover tự động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL04-BP01 Triển khai mẫu tác nhân trọng tài (arbiter) cho các hệ thống đa tác nhân được phối hợp](agentrel04-bp01.md)
- [AGENTREL04-BP02 Phân loại các tác nhân bằng một phân loại năng lực kỹ lưỡng](agentrel04-bp02.md)
- [AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác](agentrel04-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Video liên quan:**

- [AWS re:Invent 2024 - Architecting scalable and secure agentic AI with AgentCore (AIM431)](https://www.youtube.com/watch?v=wqmeZOT6mmc)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
