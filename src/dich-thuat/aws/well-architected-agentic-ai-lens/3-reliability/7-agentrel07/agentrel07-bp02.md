# AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi của tác nhân

Thử lại đồng nhất lãng phí công sức cho các lỗi không thể thử lại và tạo ra các cơn "đàn sấm sét" (thundering herd) cho các lỗi thoáng qua. Phân loại lỗi theo loại và áp dụng các chiến lược có mục tiêu, thử lại cho các lỗi thoáng qua, dự phòng cho các lỗi bền vững, leo thang cho các lỗi không thể phục hồi, giữ cho tính khả dụng cao mà không cần can thiệp thủ công.

**Kết quả mong muốn:**

- Bạn phân loại các lỗi của tác nhân thành các loại có thể thử lại và không thể thử lại tại điểm lỗi.
- Bạn dùng exponential backoff với full jitter trên các lỗi có thể thử lại, với số lần thử lại đặc thù theo loại lỗi.
- Bạn thực thi các ngân sách thử lại để giúp ngăn các cơn bão thử lại, và leo thang tới dự phòng hoặc con người rà soát khi các lần thử lại cạn kiệt.

**Các phản mẫu thường gặp (anti-patterns):**

- Áp dụng logic thử lại đồng nhất cho mọi loại lỗi, thử lại các lỗi không thể thử lại vốn sẽ không bao giờ thành công.
- Thử lại ở các khoảng cố định mà không có exponential backoff và jitter, tạo ra các hiệu ứng đàn sấm sét trong quá trình phục hồi.
- Chỉ triển khai phục hồi dựa trên thử lại mà không có các chiến lược dự phòng cho các lỗi vẫn bền vững sau khi thử lại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tính khả dụng giữ ở mức cao vì các lỗi thoáng qua tự giải quyết.
- Việc sử dụng tài nguyên hiệu quả vì các lỗi không thể thử lại không tiêu tốn ngân sách thử lại.
- Các lỗi bền vững được xử lý nhẹ nhàng thông qua các chiến lược dự phòng khi các lần thử lại cạn kiệt.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phân loại lỗi đến trước vì chiến lược phục hồi phụ thuộc vào loại. Các lỗi có thể thử lại bao gồm các lỗi hạ tầng thoáng qua, tiết lưu LLM và tạm không khả dụng, những điều kiện mà một khoảng chờ ngắn và một lần thử lại có khả năng giải quyết. Các lỗi không thể thử lại bao gồm các lỗi xác thực, đầu vào không hợp lệ và từ chối quyền, những điều kiện mà cùng một lời gọi sẽ lỗi theo cùng một cách bất kể bạn thử lại bao nhiêu lần. Gộp cả hai thành một loại duy nhất nghĩa là hoặc thử lại những thứ sẽ không bao giờ thành công, hoặc bỏ cuộc với những thứ lẽ ra đã thành công.

Chiến lược backoff quan trọng ngang với phân loại. Exponential backoff với full jitter dàn trải các lần thử lại theo thời gian, tránh cơn đàn sấm sét mà các lần thử lại khoảng cố định tạo ra trong các lỗi diện rộng. Số lần thử lại đặc thù theo loại lỗi cũng giúp ích: thử lại quyết liệt cho các lỗi thoáng qua, thử lại thận trọng với các khoảng dài hơn cho việc giới hạn tốc độ. Thực thi các ngân sách thử lại ở hai cấp. Với mỗi lần gọi, dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để giới hạn số lần thử lại trong một lần thực thi tác nhân. Điều này giúp ngăn các vòng lặp mất kiểm soát mà không cần phụ thuộc bên ngoài. Xuyên qua các lần gọi, triển khai một circuit-breaker dùng chung được hậu thuẫn bởi một kho độ trễ thấp (ví dụ các bộ đếm nguyên tử của DynamoDB hoặc ElastiCache) theo dõi tổng số lần thử lại tích lũy qua các lần thực thi đồng thời. AgentCore Policy đánh giá trạng thái circuit-breaker như một đầu vào chính sách, từ chối các lần thử lại mới khi ngân sách toàn cục đã cạn. Cách tiếp cận hai tầng này tránh phản mẫu giả định rằng các giới hạn ở cấp một-lần-gọi cung cấp sự bảo vệ toàn hệ thống.

Các luồng công việc tự chữa lành mở rộng thử lại thành phục hồi. Các mẫu lỗi phổ biến có các biện pháp khắc phục có mục tiêu. Tự động tinh chỉnh prompt xử lý các lỗi kiểm định đầu ra LLM, thay thế công cụ xử lý các lỗi gọi công cụ, và tái dựng ngữ cảnh xử lý các lỗi truy cập bộ nhớ. Khi các lần thử lại cạn kiệt, chuyển sang các chiến lược dự phòng hoặc con người rà soát thay vì kết thúc. Ghi log mọi hành động phục hồi qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với siêu dữ liệu có cấu trúc bao gồm số lần thử lại, chiến lược được dùng và kết quả, để hiệu quả phục hồi có thể được phân tích và tinh chỉnh.

### Các bước triển khai

- **Triển khai phân loại lỗi:** Phân loại các lỗi của tác nhân thành các loại có thể thử lại và không thể thử lại tại điểm lỗi.
- **Cấu hình thử lại với exponential backoff và full jitter:** Dùng số lần thử lại đặc thù theo loại lỗi để chiến lược khớp với dạng lỗi.
- **Thực thi các ngân sách thử lại qua AgentCore Policy:** Dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để giúp ngăn các cơn bão thử lại trong các lỗi diện rộng.
- **Xây dựng các luồng công việc tự chữa lành cho các mẫu phổ biến:** Triển khai tinh chỉnh prompt, thay thế công cụ và tái dựng ngữ cảnh như các đường phục hồi có mục tiêu.
- **Ghi log các hành động phục hồi để phân tích:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để bắt số lần thử lại, chiến lược và kết quả.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent](../6-agentrel06/agentrel06-bp04.md)
- [AGENTREL07-BP01 Thiết kế luồng công việc theo giai đoạn với phục hồi tăng dần](agentrel07-bp01.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và tạo điều kiện phục hồi](agentrel07-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
