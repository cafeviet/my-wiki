# AGENTREL03-BP03 Triển khai quản lý trạng thái toàn diện và phục hồi dựa trên điểm kiểm tra

Các luồng công việc chạy lâu không có điểm kiểm tra phải trả toàn bộ chi phí khởi động lại cho mọi lỗi, bất kể nó xảy ra muộn đến đâu. Lưu bền trạng thái tại các ranh giới tự nhiên và thiết kế mọi bước để idempotent cho phép một tác nhân tiếp tục từ điểm kiểm tra hoàn tất gần nhất thay vì làm lại công việc.

**Kết quả mong muốn:**

- Bạn có trạng thái luồng công việc được lưu bền tại các điểm kiểm tra đều đặn, nhờ đó gián đoạn tiếp tục từ điểm hoàn tất gần nhất thay vì từ đầu.
- Bạn có các bước luồng công việc idempotent tạo ra cùng kết quả khi được phát lại với cùng đầu vào.
- Bạn có một vòng đời điểm kiểm tra với hết hạn dựa trên TTL và dọn dẹp tường minh sau khi hoàn tất.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các luồng công việc tác nhân kéo dài mà không lưu bền trạng thái trung gian, buộc khởi động lại hoàn toàn khi có bất kỳ lỗi nào.
- Triển khai các điểm kiểm tra mà không có bảo đảm idempotency, tạo ra hỏng dữ liệu hoặc các tác dụng phụ trùng lặp khi tiếp tục.
- Bỏ qua dọn dẹp điểm kiểm tra, tích tụ lưu trữ vô thời hạn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chi phí khởi động lại luồng công việc giảm vì việc tiếp tục bắt đầu từ điểm kiểm tra gần nhất.
- Công việc trùng lặp được ngăn ngừa thông qua phục hồi dựa trên điểm kiểm tra idempotent.
- Hiệu quả tính toán cải thiện vì việc phục hồi tránh tính toán lại thừa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Lập điểm kiểm tra chỉ hữu ích nếu việc phục hồi an toàn, và việc phục hồi chỉ an toàn nếu các bước là idempotent. Một bước idempotent tạo ra cùng kết quả dù nó chạy một lần hay năm lần với cùng đầu vào, nghĩa là một lần thử lại hay tiếp tục không thêm các tác dụng phụ trùng lặp. Ràng buộc này định hình mọi thứ phía dưới. Các lời gọi bên ngoài cần idempotency key, các thay đổi trạng thái cần ghi có điều kiện (conditional writes), và các lần phát sự kiện cần logic khử trùng lặp (deduplication). Không có bảo đảm idempotency, phục hồi dựa trên điểm kiểm tra có thể tạo ra các tác dụng phụ trùng lặp hoặc hỏng dữ liệu. Hãy thiết kế mỗi bước để idempotent trước khi triển khai lập điểm kiểm tra.

Lựa chọn runtime quyết định bạn cần tự xây dựng bao nhiêu kỷ luật lập điểm kiểm tra. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) hỗ trợ các khối lượng công việc chạy lâu với lưu trữ phiên được quản lý lưu bền trạng thái hệ thống tệp qua các chu kỳ dừng và tiếp tục, bao phủ trường hợp thô. Đối với lập điểm kiểm tra nhận biết giai đoạn của luồng công việc với redrive từ các điểm lỗi cụ thể, điều phối qua [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html). Step Functions lưu bền trạng thái thực thi tại mỗi chuyển tiếp và cho phép khởi động lại từ điểm lỗi thay vì từ đầu. Đối với các luồng công việc động do các tác nhân giám sát dẫn dắt, các mẫu callback tạm dừng thực thi trong khi tác nhân giám sát quyết định hành động tiếp theo, bảo toàn lợi ích của việc lưu bền trạng thái.

Quản lý vòng đời giữ cho kho điểm kiểm tra không phình vô hạn. Hết hạn dựa trên TTL xử lý trường hợp phổ biến: các luồng công việc không bao giờ hoàn tất cuối cùng cũng lão hóa và bị loại. Dọn dẹp tường minh sau khi hoàn tất thành công thu hồi không gian ngay lập tức. Dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) để lưu bền trạng thái điểm kiểm tra và bối cảnh đặc tả cho các tác nhân cần lập điểm kiểm tra tùy biến. Giám sát sức khỏe kho điểm kiểm tra qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để sự tăng trưởng lưu trữ hoặc độ trễ truy cập nổi lên trước khi việc phục hồi bắt đầu thất bại.

### Các bước triển khai

- **Triển khai các tác nhân trên AgentCore Runtime với lưu trữ phiên được quản lý:** Dùng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cho việc lưu bền trạng thái ở cấp hệ thống tệp qua các chu kỳ dừng và tiếp tục.
- **Điều phối các luồng công việc nhiều bước qua Step Functions:** Dùng [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) để lưu bền trạng thái tại mỗi chuyển tiếp với khả năng redrive từ điểm lỗi.
- **Thiết kế mọi bước luồng công việc để idempotent:** Yêu cầu idempotency key trên các lời gọi bên ngoài và ghi có điều kiện trên các thay đổi trạng thái để các lần thử lại và tiếp tục không đưa vào các tác dụng phụ trùng lặp.
- **Dùng AgentCore Memory cho trạng thái điểm kiểm tra tùy biến:** Lưu bền trạng thái điểm kiểm tra và bối cảnh đặc tả qua [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho các tác nhân có nhu cầu lập điểm kiểm tra riêng.
- **Triển khai quản lý vòng đời điểm kiểm tra:** Đặt hết hạn dựa trên TTL và dọn dẹp tường minh sau khi hoàn tất thành công để kho điểm kiểm tra luôn có giới hạn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn](agentrel03-bp01.md)
- [AGENTREL03-BP02 Kiến trúc các kho bộ nhớ chịu lỗi với dư thừa và failover](agentrel03-bp02.md)
- [AGENTREL07-BP01 Thiết kế luồng công việc theo giai đoạn với phục hồi tăng dần](../7-agentrel07/agentrel07-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
