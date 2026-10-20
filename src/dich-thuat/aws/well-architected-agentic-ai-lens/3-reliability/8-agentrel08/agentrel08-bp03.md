# AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp

Các bể tài nguyên dùng chung để một tác nhân "ồn ào" bỏ đói phần còn lại. Các tầng ưu tiên với cấp phát tài nguyên dành riêng và phát hiện tranh chấp giữ cho các tác nhân đối mặt người dùng vẫn đáp ứng ngay cả khi các khối lượng công việc nền tăng đột biến.

**Kết quả mong muốn:**

- Bạn có hạ tầng runtime riêng biệt cho các tầng ưu tiên tác nhân khác nhau để các tác nhân ưu tiên cao có tài nguyên dành riêng.
- Bạn theo dõi mức tiêu thụ token cho mỗi tác nhân và thực thi truy cập theo từng tác nhân tới dung lượng mô hình dùng chung.
- Bạn phát hiện tranh chấp sớm qua các tín hiệu tổng hợp và kích hoạt việc giảm thiểu tự động trước khi lỗi xảy ra.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng chung các bể tài nguyên trên mọi tác nhân mà không cô lập, để các tác nhân khối lượng lớn tiêu thụ tài nguyên mà các tác nhân khác cần.
- Bỏ qua quản lý hạn ngạch API, nên việc tiết lưu ảnh hưởng tới mọi tác nhân mỗi khi bất kỳ tác nhân đơn lẻ nào vượt hạn ngạch.
- Coi mọi tác nhân đều quan trọng như nhau, để các đợt tăng đột biến khối lượng công việc nền làm suy giảm các tác nhân đối mặt người dùng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Hiệu năng giữ có thể dự đoán vì cô lập tài nguyên giúp ngăn sự can thiệp chéo giữa các khối lượng công việc.
- Chất lượng dịch vụ cho các tác nhân ưu tiên cao được duy trì thông qua cấp phát tài nguyên theo mức ưu tiên.
- Tranh chấp được phát hiện sớm thông qua giám sát tổng hợp trước khi nó trở thành lỗi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Cô lập bắt đầu ở bề mặt thực thi. Triển khai các thể hiện [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) riêng biệt cho các tầng ưu tiên tác nhân khác nhau, để các tác nhân đối mặt người dùng ưu tiên cao chạy trên các thể hiện Runtime dành riêng với cấp phát tài nguyên riêng mà các tác nhân nền không thể tiêu thụ. Đây là hình thức "vách ngăn" (bulkheading) sạch sẽ nhất cho các khối lượng công việc của tác nhân, các bể riêng biệt về mặt vật lý không thể can thiệp lẫn nhau, không có bộ lập lịch dùng chung đưa vào sự ràng buộc.

Bảo vệ hạn ngạch xử lý trường hợp mô hình dùng chung. Dung lượng suy luận Amazon Bedrock được dùng chung trên toàn tài khoản. Theo dõi mức tiêu thụ token cho mỗi tác nhân qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và các cảnh báo Amazon CloudWatch để bắt các tác nhân riêng lẻ tiến gần các ngưỡng tiêu thụ. Các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) kiểm soát tác nhân nào có thể truy cập mô hình nào. Kết hợp chính sách với các hạn ngạch dịch vụ Amazon Bedrock và [Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) giúp ngăn một tác nhân làm cạn kiệt dung lượng mô hình dùng chung. Đối với các tác nhân nhạy độ trễ cần hiệu năng suy luận có thể dự đoán bất kể nhu cầu dịch vụ tổng thể, Provisioned Throughput cho bạn số đơn vị mô hình cố định và độ trễ có thể dự đoán đi kèm.

Với phát hiện tranh chấp, bạn có thể hành động trước khi sự cố ập tới. Các cảnh báo tổng hợp của Amazon CloudWatch kết hợp nhiều tín hiệu sử dụng tài nguyên thành một điểm số tranh chấp. Các tín hiệu này bao gồm mức sử dụng đồng thời, tốc độ tiêu thụ token và độ sâu hàng đợi. Khi điểm số vượt ngưỡng, kích hoạt việc giảm thiểu tự động. Dùng [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để từ chối truy cập công cụ cho các tác nhân ưu tiên thấp, hoặc kích hoạt suy giảm nhẹ nhàng cho các năng lực không trọng yếu. Giám sát mức sử dụng tài nguyên qua các tầng ưu tiên bằng các bảng điều khiển AgentCore Observability để tranh chấp mới nổi trở nên hiện hữu trước khi nó gây ra các lỗi mà người dùng nhìn thấy.

### Các bước triển khai

- **Triển khai các thể hiện AgentCore Runtime riêng biệt theo từng tầng ưu tiên:** Cho các tác nhân đối mặt người dùng ưu tiên cao cấp phát tài nguyên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) dành riêng.
- **Theo dõi mức tiêu thụ token theo từng tác nhân và thực thi truy cập:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) để kiểm soát truy cập mô hình theo từng tác nhân.
- **Dùng Amazon Bedrock Provisioned Throughput cho các tác nhân nhạy độ trễ:** Dùng [Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) cho hiệu năng suy luận có thể dự đoán.
- **Cấu hình các cảnh báo tổng hợp trên các tín hiệu sử dụng tài nguyên:** Kết hợp các tín hiệu về mức đồng thời, tiêu thụ token và độ sâu hàng đợi qua Amazon CloudWatch thành một điểm số tranh chấp.
- **Triển khai giảm thiểu tranh chấp tự động:** Từ chối truy cập công cụ cho các tác nhân ưu tiên thấp qua AgentCore Policy khi phát hiện áp lực.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL01-BP05 Triển khai cấp phát thích ứng](../1-agentrel01/agentrel01-bp05.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](agentrel08-bp01.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](agentrel08-bp02.md)
- [AGENTREL08-BP04 Theo dõi các số liệu sử dụng bộ nhớ của tác nhân](agentrel08-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Securely launch and scale your agents and tools on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/securely-launch-and-scale-your-agents-and-tools-on-amazon-bedrock-agentcore-runtime/)
- [Amazon Bedrock Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
