# AGENTREL03-BP04 Triển khai suy giảm nhẹ nhàng cho các thao tác bộ nhớ và trạng thái

Coi mọi lỗi bộ nhớ là chí mạng biến các sự cố phục hồi được thành các đợt ngừng hoạt động toàn phần. Một phân cấp suy giảm tường minh với các chế độ được tài liệu hóa và phục hồi tự động giữ cho các tác nhân hữu ích một phần và minh bạch về trạng thái giảm bớt của chúng.

**Kết quả mong muốn:**

- Bạn có một phân cấp suy giảm bộ nhớ với các chế độ vận hành riêng biệt và hành vi được tài liệu hóa cho mỗi chế độ.
- Bạn chuyển chế độ tự động dựa trên các tín hiệu sức khỏe bộ nhớ, và phục hồi về chế độ đầy đủ khi các kho quay lại.
- Bạn truyền đạt trạng thái suy giảm cho người dùng và các hệ thống điều phối để họ biết điều gì cần chờ đợi.

**Các phản mẫu thường gặp (anti-patterns):**

- Coi mọi lỗi bộ nhớ là chí mạng, gây ra sự không khả dụng hoàn toàn cho các điều kiện lẽ ra có thể xử lý bằng chức năng giảm bớt.
- Không truyền đạt trạng thái bộ nhớ suy giảm cho người dùng, khiến họ bối rối khi các phản hồi thiếu ngữ cảnh kỳ vọng.
- Triển khai suy giảm mà không có đường phục hồi, để các tác nhân ở chế độ suy giảm vô thời hạn sau khi các kho chính quay lại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tính khả dụng dịch vụ một phần vẫn duy trì qua các sự cố kho bộ nhớ thay vì trở thành đợt ngừng hoạt động toàn phần.
- Người dùng và các bộ điều phối thấy các chỉ báo minh bạch về năng lực hiện tại.
- Năng lực đầy đủ quay lại tự động khi các kho bộ nhớ trở lại trực tuyến.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Bắt đầu với phân cấp chế độ. Ba chế độ bao phủ hầu hết các khối lượng công việc của tác nhân. Chế độ đầy đủ có mọi tầng bộ nhớ khả dụng. Chế độ chỉ theo phiên vận hành mà không có bộ nhớ dài hạn, chỉ dùng ngữ cảnh phiên. Chế độ không trạng thái có cả hai tầng không khả dụng và xử lý mỗi yêu cầu độc lập. Đối với mỗi chế độ, định nghĩa hành vi của tác nhân một cách tường minh:

- Ở chế độ chỉ theo phiên, thông báo cho người dùng rằng ngữ cảnh phiên trước không khả dụng
- Ở chế độ không trạng thái, yêu cầu mọi ngữ cảnh cần thiết trong phạm vi tương tác hiện tại.

Không có định nghĩa này, đường dự phòng là bất cứ điều gì mã tình cờ làm, thường không phải điều bạn muốn trong một sự cố.

Các tín hiệu sức khỏe dẫn dắt các chuyển đổi. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch cùng nhau theo dõi tính khả dụng và tỷ lệ lỗi của kho bộ nhớ. Cấu hình các chuyển đổi chế độ tự động khi sức khỏe suy giảm dưới các ngưỡng bạn đặt trước, và phục hồi tự động khi các kho quay lại. Đối với suy giảm bộ nhớ ngắn hạn, các cache dự phòng trong tiến trình cho phép phiên hiện tại tiếp tục. Quản lý phiên của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) duy trì ngữ cảnh làm việc ngay cả khi các kho dài hạn suy giảm, giữ cho hầu hết các cuộc hội thoại mạch lạc qua một đợt ngừng hoạt động một phần.

Truyền đạt trạng thái suy giảm qua các chỉ báo trạng thái có cấu trúc để người dùng và các hệ thống phía dưới hiểu các hạn chế hiện tại. "Tôi không có quyền truy cập các cuộc hội thoại trước của bạn ngay lúc này" là một trải nghiệm tốt hơn một tác nhân âm thầm giả vờ như có và tạo ra ảo giác. Cùng các tín hiệu này nuôi các hệ thống điều phối có thể chọn định tuyến yêu cầu đi nơi khác hoặc hiển thị một biểu ngữ cho người dùng.

### Các bước triển khai

- **Định nghĩa một phân cấp suy giảm bộ nhớ với các chế độ được tài liệu hóa:** Đặc tả các chế độ đầy đủ, chỉ theo phiên và không trạng thái, cùng hành vi tác nhân mà mỗi chế độ quy định.
- **Triển khai các chuyển đổi chế độ tự động:** Kích hoạt các chuyển đổi thông qua các số liệu sức khỏe từ [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch.
- **Duy trì các cache dự phòng trong tiến trình cho bộ nhớ ngắn hạn:** Cho phép các phiên đang hoạt động tiếp tục khi bộ nhớ ngắn hạn suy giảm.
- **Truyền đạt trạng thái suy giảm cho người dùng:** Phơi bày các chỉ báo trạng thái có cấu trúc để người dùng thấy năng lực giảm bớt thay vì phải đoán.
- **Cấu hình phát hiện phục hồi tự động:** Đưa các tác nhân về chế độ đầy đủ khi các kho trở nên khả dụng, mà không cần người vận hành can thiệp.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn](agentrel03-bp01.md)
- [AGENTREL03-BP02 Kiến trúc các kho bộ nhớ chịu lỗi với dư thừa và failover](agentrel03-bp02.md)
- [AGENTREL08-BP04 Theo dõi các số liệu sử dụng bộ nhớ của tác nhân](../8-agentrel08/agentrel08-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
