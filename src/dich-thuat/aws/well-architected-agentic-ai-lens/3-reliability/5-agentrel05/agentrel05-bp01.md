# AGENTREL05-BP01 Thiết kế các thành phần suy luận của tác nhân mô-đun, chịu lỗi

Một đường ống suy luận đơn khối thất bại hoàn toàn mỗi khi bất kỳ giai đoạn nào thất bại. Tách nhận thức thành các giai đoạn mô-đun với các giao diện rõ ràng và các dự phòng đặc thù giai đoạn cho phép một tác nhân tiếp tục suy luận, với chất lượng giảm bớt, ngay cả khi một giai đoạn bị suy giảm.

**Kết quả mong muốn:**

- Bạn có đường ống suy luận được phân rã thành các giai đoạn mô-đun với lược đồ đầu vào/đầu ra tường minh.
- Bạn có các dự phòng đặc thù giai đoạn tự kích hoạt khi tỷ lệ lỗi tăng lên.
- Bạn ghi log tầng truy xuất và tầng mô hình được dùng trong mỗi lần gọi để có thể phân tích chất lượng về sau.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy nhận thức của tác nhân như một đường ống đơn khối, nơi bất kỳ lỗi thành phần nào cũng gây ra lỗi nhận thức hoàn toàn.
- Bỏ qua các giao diện giữa các thành phần suy luận, làm giảm khả năng kiểm thử và thay thế độc lập.
- Coi mọi thành phần suy luận đều trọng yếu như nhau mà không phân biệt thành phần thiết yếu với thành phần nâng cao chất lượng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Nhận thức một phần sống sót qua các lỗi thành phần riêng lẻ thông qua cô lập lỗi mô-đun.
- Các thành phần suy luận có thể được tối ưu hoặc thay thế độc lập, mà không cần viết lại toàn bộ đường ống.
- Ranh giới thành phần rõ ràng cô lập nguồn lỗi và đẩy nhanh việc gỡ lỗi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Quyết định kiến trúc đầu tiên là đặt ranh giới giai đoạn ở đâu. Các ranh giới hữu ích cho hầu hết các tác nhân là truy xuất ngữ cảnh, dựng prompt, suy luận mô hình, phân tích cú pháp đầu ra (output parsing) và chọn hành động. Mỗi giai đoạn có một hợp đồng hẹp: đầu vào, đầu ra và các điều kiện lỗi mà nó phát tín hiệu. Triển khai mỗi giai đoạn trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với xử lý lỗi và hành vi dự phòng của riêng nó. Không có sự phân rã này, mọi lỗi đều hiện ra như các lỗi suy luận chung chung, khiến việc gỡ lỗi khó khăn. Ranh giới giai đoạn rõ ràng cho phép nhận diện lỗi chính xác và giải quyết nhanh hơn.

Phân tầng là nơi các giai đoạn thể hiện tính mô-đun của chúng. Đối với truy xuất ngữ cảnh, tầng chính dùng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) cho tìm kiếm ngữ nghĩa, với dự phòng về các phương pháp truy xuất đơn giản hơn khi tầng chính không khả dụng. Đối với suy luận mô hình, triển khai dự phòng tầng mô hình dùng [suy luận đa Vùng của Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) để đảm bảo khả dụng, thay thế bằng các mô hình khác khi mô hình chính bị suy giảm. Đối với các tác nhân đa phương thức, [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) tiền xử lý tài liệu, hình ảnh, âm thanh và video như một giai đoạn suy luận riêng biệt trước khi suy luận dựa trên văn bản, với các dự phòng độc lập cho mỗi phương thức.

Theo dõi tỷ lệ lỗi, độ trễ và tần suất kích hoạt dự phòng theo từng giai đoạn qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Cấu hình các cảnh báo kích hoạt các cơ chế ngắt tự động khi sức khỏe giai đoạn suy giảm. Cơ chế ngắt kích hoạt dự phòng ngay lập tức thay vì chờ lần gọi lỗi tiếp theo. Ghi log tầng truy xuất và tầng mô hình được dùng trong mỗi lần gọi để bạn có thể thấy, nhiều tháng sau, tầng nào đã tạo ra câu trả lời và liệu đường dự phòng có đang được đi vào thường xuyên hơn kỳ vọng hay không.

### Các bước triển khai

- **Phân rã đường ống suy luận thành các giai đoạn riêng biệt:** Định nghĩa lược đồ đầu vào/đầu ra tường minh và triển khai mỗi giai đoạn trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html).
- **Triển khai các cơ chế ngắt tự động giữa các giai đoạn:** Kích hoạt các dự phòng đặc thù giai đoạn khi tỷ lệ lỗi vượt ngưỡng.
- **Xây dựng truy xuất ngữ cảnh theo tầng:** Dùng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) làm tầng chính với các dự phòng đơn giản dần.
- **Triển khai dự phòng tầng mô hình:** Dùng [suy luận đa Vùng của Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) để đảm bảo khả dụng trong lúc mô hình chính bị suy giảm.
- **Giám sát sức khỏe theo từng giai đoạn:** Theo dõi tỷ lệ lỗi, độ trễ và kích hoạt dự phòng qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với các cảnh báo kích hoạt các cơ chế ngắt tự động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](../1-agentrel01/agentrel01-bp02.md)
- [AGENTREL05-BP02 Tạo điều kiện cho thích ứng đáng tin cậy qua các chu kỳ cải tiến dẫn dắt bởi kiểm định](agentrel05-bp02.md)
- [AGENTREL05-BP03 Đặt nền nhận thức của tác nhân trên thông tin thực](agentrel05-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [AWS fail-fast pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html)
- [Strands Agents Agent Loop](https://strandsagents.com/docs/user-guide/concepts/agents/agent-loop/)

**Video liên quan:**

- [AWS re:Invent 2024 - Using Strands Agents to build autonomous, self-improving AI agents (AIM426)](https://www.youtube.com/watch?v=RQfW7eQsXqk)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
