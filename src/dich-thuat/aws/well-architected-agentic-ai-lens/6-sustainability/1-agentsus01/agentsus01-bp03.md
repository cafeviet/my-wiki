# AGENTSUS01-BP03 Tối ưu hóa việc sử dụng tài nguyên thông qua dịch vụ dùng chung

Mỗi Agent tự cấp phát connection pool, cache hoặc hàng đợi xử lý riêng đều trả chi phí cho hạ tầng mà không Agent nào khác trong đội hình hưởng lợi. Dịch vụ dùng chung biến những sự trùng lặp đó thành một phần hạ tầng duy nhất mà mọi Agent cùng dùng, để hạ tầng mở rộng theo nhu cầu tổ chức thay vì theo số lượng Agent.

**Kết quả mong muốn:**

- Bạn có hạ tầng chung — connection pool, cache và hàng đợi xử lý — được hợp nhất thành các lớp dịch vụ dùng chung mà mọi Agent gọi thay vì nhân bản.
- Các Agent tiêu dùng dịch vụ dùng chung qua một trừu tượng hóa Tools, để bản hiện thực có thể thay đổi mà không ràng buộc với bên gọi.
- Cache và pooling dùng chung giảm tổng số lệnh gọi dư thừa tới các hệ thống bên ngoài.
- Hiệu suất sử dụng dịch vụ dùng chung được giám sát để năng lực mở rộng theo nhu cầu thực tế thay vì các đỉnh lý thuyết.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai một cache, connection pool và hàng đợi riêng cho mỗi Agent, nên chi phí hạ tầng tăng tuyến tính theo số lượng Agent.
- Để mỗi Agent tự mở kết nối riêng tới các dịch vụ bên ngoài và lấy lặp đi lặp lại cùng dữ liệu tham chiếu, tạo ra lưu lượng mạng dư thừa và lãng phí compute.
- Coi mỗi quy trình Agent như một hệ thống cô lập, bỏ lỡ cơ hội hợp nhất các hàm chung như xác thực, ghi log hoặc xếp hàng thành một lớp dùng chung.
- Duy trì việc cấp phát tĩnh bất kể nhu cầu thực tế, nên hạ tầng dùng chung mang theo năng lực đỉnh ngay cả trong các giai đoạn hiệu suất sử dụng thấp.

**Lợi ích khi áp dụng thực hành tốt này:**

- Một tối ưu hóa đơn lẻ cho hạ tầng dùng chung cải thiện mọi Agent dùng nó, phân bổ công việc vận hành ra toàn đội hình.
- Khoản đầu tư hạ tầng tăng theo nhu cầu tổ chức thay vì tỷ lệ với số lượng Agent.
- Việc mở rộng động trên các thành phần dùng chung thu hẹp tài nguyên khi nhu cầu thấp, điều khó làm được khi mỗi Agent chạy stack cô lập riêng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Hạ tầng mà Agent cần thì lặp lại nhiều hơn công việc chúng làm. Xác thực, cache, xếp hàng, connection pooling và truy xuất xuyên-Agent đều trông giống nhau bất kể Agent nào đang gọi. Khi mỗi Agent tự cấp phát bản sao riêng của phần "ống nước" này, tổ chức trả tiền cho cùng một hạ tầng N lần và tối ưu nó theo từng nhóm một. Hợp nhất thành các lớp dùng chung đảo ngược điều này: hạ tầng được tối ưu một lần và mọi bên gọi đều hưởng lợi.

Một cache dùng chung mà các Agent gọi trực tiếp theo tên host tạo ra sự ràng buộc chặt. Thay đổi bản hiện thực nghĩa là phải cập nhật mọi bên gọi. Lộ các dịch vụ dùng chung qua năng lực máy chủ MCP của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) đặt một giao diện ổn định phía trước bản hiện thực. Tầng cache, backend hàng đợi hoặc connection pool có thể thay đổi mà các Agent không hề hay biết. [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) tập trung hóa xác thực để từng Agent không phải tự quản lý thông tin xác thực riêng, đây là dạng đơn giản nhất của hạ tầng dùng chung mang lại lợi tức tức thời.

Riêng với cache, lựa chọn hiện thực phụ thuộc vào mẫu dữ liệu. [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/BestPractices.html) phù hợp với dữ liệu nóng đa dụng có mẫu truy cập linh hoạt, còn [Amazon DynamoDB Accelerator (DAX)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html) phù hợp với trạng thái Agent lưu trên DynamoDB cần đọc ở mức micro-giây mà không cần một tầng cache riêng. Cả hai đều được chia sẻ qua các Agent sau khi cấp phát. [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) phân phối các yêu cầu Model nền qua các Region để tính khả dụng được chia sẻ ở tầng suy luận, không chỉ ở tầng ứng dụng.

Triển khai chính các Agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html). Mô hình serverless của nó nghĩa là ngay từ đầu không có dấu chân hạ tầng nào để mỗi Agent phải hợp nhất, điều này bổ trợ cho mẫu dịch vụ dùng chung ở tầng hỗ trợ. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) lộ tỷ lệ hit của cache, độ sâu hàng đợi và tần suất gọi cho mỗi dịch vụ dùng chung, để dữ liệu hiệu suất sử dụng điều khiển các quyết định mở rộng thay vì các ước lượng đỉnh lý thuyết.

### Các bước triển khai

- **Nhận diện các nhu cầu hạ tầng chung:** Liệt kê "ống nước" bị nhân bản qua các bản triển khai hiện tại và hợp nhất mỗi thứ thành một lớp dịch vụ dùng chung: Connection pool
- Cache
- Hàng đợi
- Xác thực
- **Triển khai cache dùng chung:** Cấp phát [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/BestPractices.html) cho dữ liệu nóng đa dụng hoặc [Amazon DynamoDB Accelerator (DAX)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html) cho trạng thái lưu trên DynamoDB, để dữ liệu truy cập thường xuyên được đọc từ một cache thay vì lấy lại theo từng Agent.
- **Lộ các dịch vụ dùng chung qua một giao diện ổn định:** Công bố hạ tầng dùng chung dưới dạng Tools MCP qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để các Agent tiêu dùng mà không ràng buộc với bản hiện thực.
- **Tập trung hóa xác thực:** Dùng [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) để quản lý thông tin xác thực một lần thay vì để mỗi Agent tự quản lý riêng.
- **Phân phối suy luận Model:** Bật [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) để năng lực Model nền được gom chung qua các Region nhằm đảm bảo tính khả dụng.
- **Theo dõi hiệu suất sử dụng và mở rộng dựa trên dữ liệu:** Giám sát các thông tin sau qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và điều chỉnh năng lực dựa trên mức dùng quan sát được thay vì các ước lượng trường hợp xấu nhất: Tỷ lệ hit của cache
- Độ sâu hàng đợi
- Mẫu gọi

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh](agentsus01-bp01.md)
- [AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được](agentsus01-bp02.md)
- [SUS03-BP02 Remove or refactor workload components with low or no use](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a3.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon ElastiCache best practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/BestPractices.html)
- [Amazon DynamoDB Accelerator (DAX)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)
- [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Strands Agents Tools](https://github.com/strands-agents/tools)

**Các ví dụ liên quan:**

- [GitHub: aws-samples/serverless-patterns](https://github.com/aws-samples/serverless-patterns)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
