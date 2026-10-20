# AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả

Các mẫu gọi **Tools** được tinh chỉnh tốt giúp độ nhạy bén của tác nhân phản ánh thời gian xử lý thực tế của Tool, không phải chi phí hạ tầng. Mỗi lệnh gọi Tool liên quan đến thiết lập kết nối, tuần tự hóa, truyền tải mạng, xử lý, và giải-tuần-tự-hóa; cắt tỉa mỗi thành phần cộng dồn qua nhiều lệnh gọi Tools trong một tác vụ tác nhân điển hình.

**Kết quả mong muốn:**

- Bạn có các lệnh gọi Tools riêng lẻ thực thi với chi phí tối thiểu vượt ra ngoài thời gian xử lý vốn có của Tool.
- Bạn có gộp kết nối loại các chi phí thiết lập kết nối lặp lại.
- Bạn có các timeout giúp ngăn các Tools chậm chặn thực thi tác nhân.
- Bạn có các cắt-mạch tự động phát hiện các Tools suy giảm và định tuyến tới các lựa chọn thay thế.
- Bạn có các chỉ số gọi theo-Tool cung cấp khả năng thấy các đặc trưng hiệu năng.

**Các phản mẫu thường gặp (anti-patterns):**

- Thiết lập kết nối mới cho mọi lệnh gọi Tool thay vì duy trì các connection pool, thêm hàng trăm mili-giây latency bắt-tay TLS vào mỗi lệnh gọi.
- Triển khai các chiến lược thử lại hung hăng mà không có backoff hoặc jitter, tạo ra các bão-thử-lại áp đảo các Tools vốn đã suy giảm.
- Đặt timeout gọi Tool quá cao hoặc không đặt gì cả, để một lệnh gọi Tool chậm duy nhất chặn tác nhân trong vài giây và vượt ngân sách **latency** tác vụ tổng thể.

**Lợi ích khi áp dụng thực hành tốt này:**

- Gộp kết nối và các kết nối bền giảm chi phí mỗi-lệnh-gọi-Tool.
- Các timeout phù hợp bảo vệ ngân sách latency tác nhân.
- Các cắt-mạch tự động hỗ trợ chuyển-đổi-dự-phòng nhanh tới các lựa chọn thay thế.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Với các Tools được truy cập qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), gateway xử lý quản lý kết nối, xác thực, và định tuyến một cách tự động. Với các endpoint Tool tùy chỉnh, gộp kết nối qua các kết nối HTTP keep-alive hoặc các cấu hình pool riêng-của-framework giữ các phiên TLS ấm qua các lần gọi.

Với các Tools dựa-trên-[AWS Lambda](https://aws.amazon.com/lambda/), khởi tạo các kết nối bên ngoài hàm handler để chúng bền qua các lần gọi trong cùng môi trường thực thi biến một bắt-tay cho mỗi yêu cầu thành một bắt-tay cho mỗi môi trường. Các timeout gọi Tool nên được đặt dựa trên thời gian phản hồi kỳ vọng của Tool, thường gấp hai tới ba lần latency p95.

Các chiến lược thử lại với exponential backoff và jitter xử lý các lỗi tạm thời, với tối đa hai tới ba lần thử lại và một ngân sách thử lại tổng không vượt timeout của Tool. Các mẫu cắt-mạch tự động theo dõi tỷ lệ lỗi Tool và mở mạch khi lỗi vượt một ngưỡng, trả về một kết quả được cache hoặc lỗi ngay lập tức thay vì chờ một timeout khác.

Với các Tools hỗ trợ thao tác batch, gộp lô yêu cầu (một API batch cho nhiều tra cứu mục) giảm chi phí cho mỗi lệnh gọi qua tập. Các chỉ số gọi theo-Tool (phân vị latency, tỷ lệ lỗi, tỷ lệ timeout, và trạng thái cắt-mạch tự động) thuộc về bảng điều khiển hiệu năng tác nhân cạnh các chỉ số vòng-lặp-suy-luận.

### Các bước triển khai

- **Dùng AgentCore Gateway cho truy cập Tool được quản lý nơi có thể, và triển khai gộp kết nối cho các endpoint Tool tùy chỉnh:** Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cho truy cập Tool được quản lý. Với các endpoint tùy chỉnh, bật HTTP keep-alive và các connection pool cấp-framework.
- **Cấu hình các timeout theo-Tool dựa trên latency p95 đã profile:** Định-cỡ timeout của mỗi Tool ở hai tới ba lần latency p95 đo được của nó để các lệnh gọi chậm riêng lẻ không làm khựng tác nhân.
- **Triển khai các chiến lược thử lại với exponential backoff và jitter:** Dùng exponential backoff với jitter và giới hạn thử lại ở hai tới ba để các lỗi tạm thời phục hồi mà không áp đảo các Tools vốn đã suy giảm.
- **Triển khai các mẫu cắt-mạch tự động fast-fail khi các Tools suy giảm:** Theo dõi tỷ lệ lỗi theo-Tool và mở mạch khi lỗi vượt một ngưỡng, trả về một kết quả được cache hoặc lỗi ngay lập tức.
- **Triển khai gộp lô yêu cầu cho các Tools hỗ trợ thao tác batch:** Dùng các API batch khi cần nhiều mục để chi phí mỗi-lệnh-gọi được phân bổ đều qua tập.
- **Giám sát các chỉ số gọi theo-Tool và thiết lập cảnh báo cho các bất thường latency và tỷ lệ lỗi:** Công bố các phân vị latency theo-Tool, tỷ lệ lỗi, tỷ lệ timeout, và trạng thái cắt-mạch tới CloudWatch với cảnh báo trên các bất thường.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu](agentperf06-bp01.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](../2-agentperf02/agentperf02-bp03.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](../3-agentperf03/agentperf03-bp04.md)

**Tài liệu liên quan:**

- [Blog: Xây dựng các máy chủ MCP chạy-dài trên Amazon Bedrock AgentCore với tích hợp Strands Agents](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Các framework, giao thức, và Tools AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
