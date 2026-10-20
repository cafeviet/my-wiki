# AGENTREL03-BP02 Kiến trúc các kho bộ nhớ chịu lỗi với dư thừa và failover

Lỗi bộ nhớ không cần đồng nghĩa với lỗi tác nhân. Với tính dư thừa, các đường dự phòng và một kỷ luật kiểm thử failover trong điều kiện được kiểm soát, một tác nhân tiếp tục phục vụ các phản hồi năng lực giảm bớt cho tới khi các kho chính của nó phục hồi thay vì trở nên hoàn toàn không khả dụng.

**Kết quả mong muốn:**

- Bạn có hạ tầng bộ nhớ chính với độ bền và tính khả dụng tích hợp sẵn, được hậu thuẫn bởi các kho dự phòng tường minh cho vận hành suy giảm.
- Bạn có logic fail-fast trên truy cập bộ nhớ định tuyến tới dự phòng khi các kho chính không khả dụng.
- Bạn diễn tập failover thường xuyên trong các môi trường phi vận hành để kiểm định hành vi chế độ suy giảm.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các kho bộ nhớ như các điểm lỗi đơn không có sao chép (replication) hay failover, gây mất bộ nhớ hoàn toàn trong các sự cố ngừng hoạt động.
- Để failover ở dạng thủ công, nên việc phục hồi chờ người vận hành và kéo dài thời gian ngừng hoạt động của tác nhân.
- Bỏ qua kiểm thử failover, chỉ phát hiện ra các lỗ hổng khi các sự cố vận hành ép buộc điều đó.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thời gian ngừng hoạt động giảm vì failover tự động tiếp quản trước khi người vận hành có thể can thiệp.
- Các tác nhân tiếp tục hành xử nhất quán trong các sự cố kho bộ nhớ thông qua suy giảm nhẹ nhàng.
- Sao chép bộ nhớ qua các Availability Zone giúp bảo vệ chống mất dữ liệu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cung cấp hạ tầng bộ nhớ được quản lý với độ bền và tính khả dụng tích hợp sẵn, nên đường mặc định vốn đã chịu lỗi. Công việc thiết kế nằm ở đường suy giảm: tác nhân làm gì khi ngay cả kho được quản lý cũng tạm không truy cập được, hoặc khi một kho tùy biến nằm cạnh nó? Logic fail-fast trên truy cập bộ nhớ là câu trả lời đầu tiên. Khi một kho biểu hiện tỷ lệ lỗi tăng, bên gọi ngừng chờ và định tuyến tới một dự phòng. Đối với bộ nhớ ngắn hạn, dự phòng đó là một cache trong tiến trình. Đối với bộ nhớ dài hạn, đó là một cache đọc xuyên (read-through) của các mục được truy cập thường xuyên.

Đối với các tác nhân chạy trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), lưu trữ phiên được quản lý của runtime lưu bền trạng thái ở cấp hệ thống tệp qua các chu kỳ dừng và tiếp tục. Đối với việc lập điểm kiểm tra nhận biết giai đoạn của luồng công việc với khả năng redrive từ các điểm lỗi cụ thể, dùng [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) hoặc điều phối ở cấp khung như LangGraph với AgentCore Memory. Lựa chọn phụ thuộc vào mức độ chi tiết mà việc phục hồi cần. Step Functions cho bạn độ bền cho mỗi bước, trong khi lưu trữ phiên được quản lý cho bạn độ bền toàn tác nhân tại ranh giới phiên.

Kiểm thử thường xuyên kiểm định rằng các cơ chế failover hoạt động như thiết kế. [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) mô phỏng các sự cố kho bộ nhớ trong các môi trường phi vận hành để bạn có thể kiểm định rằng các cơ chế failover kích hoạt đúng và các tác nhân tiếp tục hoạt động ở chế độ suy giảm. Tài liệu hóa hành vi kỳ vọng cho mỗi kịch bản lỗi và so sánh hành vi quan sát được với các kỳ vọng mỗi lần bạn chạy bài kiểm thử. Sự chênh lệch giữa những gì bạn kỳ vọng và những gì thực sự xảy ra là tín hiệu cho thấy một thoái lui đã len vào.

### Các bước triển khai

- **Dùng AgentCore Memory làm kho được quản lý chính:** Mặc định dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) vì độ bền và tính khả dụng tích hợp sẵn của nó.
- **Triển khai logic fail-fast cho truy cập bộ nhớ:** Phát hiện tỷ lệ lỗi tăng trên các lời gọi bộ nhớ và định tuyến tới các kho dự phòng.
- **Duy trì các cache dự phòng trong tiến trình cho bộ nhớ ngắn hạn:** Giữ các phiên hiện tại tiếp tục thông qua một cache phương án cuối cho phép tác vụ hoàn tất.
- **Triển khai cache đọc xuyên cho bộ nhớ dài hạn:** Phục vụ các bản sao cache của các mục được truy cập thường xuyên trong thời gian tạm không khả dụng.
- **Kiểm thử failover với AWS Fault Injection Service:** Dùng [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) để kiểm định hành vi chế độ suy giảm so với các kỳ vọng được tài liệu hóa theo một lịch đều đặn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](../1-agentrel01/agentrel01-bp02.md)
- [AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn](agentrel03-bp01.md)
- [AGENTREL03-BP03 Triển khai quản lý trạng thái toàn diện và phục hồi dựa trên điểm kiểm tra](agentrel03-bp03.md)
- [AGENTREL03-BP04 Triển khai suy giảm nhẹ nhàng cho các thao tác bộ nhớ và trạng thái](agentrel03-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)
- [AWS fail-fast pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Fault Injection Service](https://aws.amazon.com/fis/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
