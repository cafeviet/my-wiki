# AGENTREL01-BP05 Triển khai cấp phát thích ứng

Cấp phát tĩnh buộc phải chọn giữa trả tiền quá mức cho đỉnh và thất bại dưới tải. Khối lượng công việc của tác nhân dịch chuyển từng phút, nên dung lượng, tầng mô hình và hạn ngạch (quota) phải đáp ứng theo độ phức tạp của tác vụ và nhu cầu hiện tại mà không cần người vận hành can thiệp.

**Kết quả mong muốn:**

- Bạn có cơ chế cấp phát tính toán cho tác nhân tự điều chỉnh cho từng lần gọi mà không cần tinh chỉnh thủ công.
- Bạn định tuyến các tác vụ tới các tầng mô hình phù hợp với độ phức tạp của chúng, với các cơ chế dự phòng khi hạn ngạch bị siết chặt.
- Bạn cấp phát tài nguyên trước các mẫu nhu cầu đã biết và thu nhỏ trong các giai đoạn nhàn rỗi.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy cấp phát tài nguyên tĩnh và trả tiền cho dung lượng đỉnh ngay cả trong các giai đoạn nhu cầu thấp.
- Bỏ qua các số liệu kích hoạt quyết định mở rộng, nên hệ thống không có cơ sở để cấp phát tài nguyên khi cần.
- Coi mọi tác vụ đều cần cùng một mô hình, bỏ qua việc tiết kiệm chi phí và độ trễ khi phân tầng theo độ phức tạp.

**Lợi ích khi áp dụng thực hành tốt này:**

- Hiệu năng giữ nhất quán dưới tải biến động vì tài nguyên bám theo nhu cầu thay vì một kế hoạch cấp phát cố định.
- Ngăn được cạn kiệt tài nguyên trong các đợt tăng đột biến mà không cần con người can thiệp.
- Chi phí giảm trong các giai đoạn nhu cầu thấp thông qua thu nhỏ tự động.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Serverless là mức nền tảng cho tính toán thích ứng. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) lưu trữ các tác nhân với cơ chế mở rộng tích hợp sẵn tự điều chỉnh việc cấp phát tính toán cho từng lần gọi, nhờ đó từng tác nhân không cần quản lý kích cỡ đội (fleet). Đối với suy luận LLM, chế độ theo nhu cầu (on-demand) của Amazon Bedrock mở rộng mà không cần đặt trước dung lượng. [Suy luận đa Vùng của Amazon Bedrock (cross-region inference)](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) phân phối yêu cầu qua các Vùng để giảm tác động của các ràng buộc dung lượng theo vùng.

Phân tầng khớp việc chọn mô hình với khối lượng công việc. Các tác vụ độ phức tạp thấp được định tuyến tới các mô hình Amazon Bedrock nhỏ hơn, nhanh hơn, trong khi suy luận phức tạp được định tuyến tới các mô hình lớn hơn. Bộ định tuyến nên điều chỉnh động dựa trên các tín hiệu độ phức tạp của tác vụ và mức sử dụng hạn ngạch hiện tại, chứ không phải một quy tắc cố định nhúng trong mã. Đối với các tác nhân đối mặt người dùng nhạy độ trễ mà việc tiết lưu là không thể chấp nhận, dùng tầng theo nhu cầu Priority của Amazon Bedrock để cấp phát thông lượng cao cấp. Đối với các khối lượng công việc cần độ trễ thấp nhất quán bất kể nhu cầu dịch vụ tổng thể, dùng Amazon Bedrock Provisioned Throughput với số đơn vị mô hình cố định. Hướng dẫn [Amazon Bedrock Capacity, Limits, and Cost Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html) bao quát các đánh đổi giữa các tầng Flex, Standard, Priority và Reserved.

Giám sát các tín hiệu sức khỏe tổng hợp qua các lớp tác nhân và kích hoạt các hành động mở rộng phối hợp khi hệ thống tiến gần các giới hạn dung lượng. Thông lượng token, độ trễ ở cấp mô hình và tỷ lệ lỗi cho mỗi lớp qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) là các tín hiệu dẫn dắt việc điều chỉnh tầng. Mở rộng theo lịch xử lý nhu cầu được dự đoán. Nếu dữ liệu lịch sử cho thấy một đợt tăng đột biến vào 9 giờ sáng mỗi thứ Hai, hãy cấp phát trước khi đợt tăng ập đến thay vì phản ứng trong lúc đó.

### Các bước triển khai

- **Triển khai các tác nhân trên AgentCore Runtime để mở rộng serverless:** Dùng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để việc cấp phát tính toán tự điều chỉnh cho từng lần gọi mà không cần định kích cỡ đội thủ công.
- **Định tuyến tác vụ theo độ phức tạp tới các mô hình Amazon Bedrock phù hợp:** Triển khai chọn mô hình theo tầng gửi các tác vụ độ phức tạp thấp tới các mô hình nhỏ hơn và các tác vụ suy luận nặng tới các mô hình lớn hơn dựa trên tín hiệu độ phức tạp.
- **Bật suy luận đa Vùng của Amazon Bedrock:** Bật [suy luận đa Vùng (cross-region inference)](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) để phân phối yêu cầu và giảm tác động của các ràng buộc dung lượng theo vùng.
- **Giám sát thông lượng token và độ trễ qua AgentCore Observability:** Theo dõi thông lượng và độ trễ theo từng tầng qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và kích hoạt điều chỉnh tầng khi vượt ngưỡng.
- **Dùng mở rộng theo lịch trước các đợt tăng dự kiến:** Cấp phát trước dựa trên các mẫu lịch sử để dung lượng sẵn sàng trước khi nhu cầu ập đến.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP01 Triển khai một lớp nhắn tin bền bỉ](agentrel01-bp01.md)
- [AGENTREL01-BP02 Thiết lập các lớp mô-đun, cô lập lỗi](agentrel01-bp02.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](../8-agentrel08/agentrel08-bp03.md)
- [AGENTCOST02-BP01 Architect tiered model selection for cost-performance optimization](../../5-cost-optimization/2-agentcost02/agentcost02-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Securely launch and scale your agents and tools on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/securely-launch-and-scale-your-agents-and-tools-on-amazon-bedrock-agentcore-runtime/)
- [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Amazon Bedrock Capacity, Limits, and Cost Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)
- [Effective cost optimization strategies for Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
