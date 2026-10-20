# AGENTCOST04-BP03 Triển khai caching thông minh và xử lý thất bại cho kết quả công cụ

Chi phí công cụ có thể khó lường khi các agent lặp lại các lần gọi giống hệt hoặc tương đương, và chúng có thể tăng vọt khi các lần thử lại chạy không giới hạn suốt một sự cố dịch vụ. Caching hai lớp, xác thực lược đồ, và các điểm cắt tự động biến các chế độ lỗi đó thành các chi phí dự đoán được, có giới hạn.

**Kết quả mong muốn:**

- Bạn có các semantic cache phạm vi phiên và xuyên phiên giảm các lần gọi công cụ dư thừa.
- Bạn xác thực đầu vào công cụ theo JSON Schema trước khi gọi để giúp ngăn các lần gọi lãng phí trên các yêu cầu sai định dạng.
- Bạn có các điểm cắt tự động dừng thử lại khi tỷ lệ thất bại vượt các ngưỡng, với fallback tự động sang các công cụ thay thế.
- Bạn theo dõi tỷ lệ trúng cache và chi phí thử lại như các số liệu riêng biệt.

**Các phản mẫu thường gặp (anti-patterns):**

- Không cache các kết quả công cụ thường dùng, thực hiện các lần gọi giống hệt lặp lại trong cùng một phiên vốn lãng phí tính toán và chi phí API bên ngoài.
- Chỉ dùng caching khớp chính xác khi các agent diễn đạt cùng yêu cầu theo cách khác nhau, bỏ lỡ các lần trúng cache cho các lần gọi giống hệt về ngữ nghĩa.
- Thử lại các lần gọi công cụ thất bại vô hạn mà không có điểm cắt tự động, nhân chi phí trong lúc suy giảm dịch vụ mà không giải quyết được vấn đề nền tảng.
- Không xác thực các lược đồ đầu vào công cụ trước khi gọi, cho phép các lần gọi sai định dạng lãng phí chi phí gọi mà không tạo ra kết quả dùng được.

**Lợi ích khi áp dụng thực hành tốt này:**

- Caching hai lớp giảm các lần gọi công cụ dư thừa và phí API bên ngoài.
- Các điểm cắt tự động dừng thử lại khi tỷ lệ thất bại vượt các ngưỡng, giúp ngăn các cơn bão thử lại tốn kém.
- Vô hiệu hóa cache hướng-sự-kiện hỗ trợ caching tích cực cho dữ liệu biến động bằng cách xóa các kết quả lỗi thời kịp thời khi dữ liệu nguồn thay đổi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Caching công cụ phải hoạt động ở hai phạm vi để bao phủ cả sự lặp lại hiển nhiên lẫn không hiển nhiên. Lớp phạm vi phiên hoạt động qua [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) và bắt các lần gọi trùng lặp trong một phiên agent duy nhất, một chế độ lỗi phổ biến khi các agent quay lại một nhánh suy luận. Lớp xuyên phiên dùng [Amazon OpenSearch Service Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) cho semantic caching: tạo các embedding của các tham số công cụ và truy vấn các lần gọi trước tương tự vượt trên một ngưỡng cosine similarity trước khi gọi công cụ. TTL của mỗi mục cache nên được hiệu chỉnh theo độ biến động của dữ liệu nền. Ví dụ, yêu cầu độ tươi của một API thời tiết là vài phút, trong khi một cơ sở tri thức tham chiếu tĩnh dung sai được vài giờ hoặc vài ngày.

Xác thực lược đồ có thể giúp ngăn lãng phí. Các agent đôi khi tạo các lần gọi công cụ với kiểu tham số sai, trường bắt buộc bị thiếu, hoặc giá trị enum không hợp lệ, và các lần gọi đó phải trả chi phí phục vụ công cụ và API bên ngoài cho một phản hồi không dùng được. Xác thực JSON schema trong hàm action group Lambda từ chối các yêu cầu sai định dạng trước khi chúng chạm tới các API bên ngoài và trả về một lỗi xác thực cho agent để sửa.

Vô hiệu hóa cache có thể giúp làm cho caching tích cực an toàn hơn. Vô hiệu hóa hướng-sự-kiện lắng nghe các thay đổi dữ liệu nguồn và xóa các mục cache bị ảnh hưởng ngay lập tức, nên dữ liệu biến động vẫn có thể được cache mà không trả về các kết quả lỗi thời. Không có vô hiệu hóa hướng-sự-kiện, các nhóm rơi vào việc phải chọn giữa TTL tích cực (kết quả lỗi thời) hoặc TTL ngắn (tỷ lệ trúng thấp), và cả hai lựa chọn đều bỏ lại chi phí trên bàn.

Để xử lý thất bại, các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thực thi các điểm cắt tự động khi tỷ lệ thất bại vượt các ngưỡng, dừng các cơn bão thử lại trong lúc suy giảm dịch vụ. Fallback tự động sang các công cụ thay thế duy trì chức năng agent trong lúc sự cố, và các ngân sách thử lại cho mỗi phiên suy luận giới hạn tổng số lần thử lại dùng exponential backoff với jitter. Dữ liệu đo lường cache và thử lại được làm lộ qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và Amazon CloudWatch: tỷ lệ trúng theo từng lớp, các chuyển tiếp trạng thái điểm cắt, và chi phí thử lại như một phần trăm của tổng chi phí công cụ. Với caching mở rộng ra ngoài kết quả công cụ vào các lần gọi model, xem [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md).

### Các bước triển khai

- **Triển khai caching hai lớp:** Triển khai một cache in-process phạm vi phiên trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) và một semantic cache [Amazon OpenSearch Service Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) cho tái sử dụng xuyên phiên, với TTL được hiệu chỉnh theo từng công cụ (ngắn cho dữ liệu biến động, dài cho dữ liệu tham chiếu tĩnh).
- **Triển khai semantic caching:** Tạo các embedding tham số và truy vấn OpenSearch Serverless tìm các lần gọi trước tương tự vượt trên một ngưỡng cosine similarity trước khi gọi công cụ.
- **Xác thực đầu vào công cụ:** Triển khai xác thực JSON Schema trong các hàm action group Lambda để từ chối các yêu cầu sai định dạng trước khi chúng chạm tới các API bên ngoài, trả về các lỗi xác thực cho agent sửa.
- **Thực thi các điểm cắt và công cụ fallback:** Cấu hình các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cho các điểm cắt tự động, nối fallback tự động sang các công cụ thay thế khi các điểm cắt kích hoạt, và đặt các ngân sách thử lại cho mỗi phiên suy luận.
- **Giám sát các số liệu cache và thử lại:** Tạo các số liệu Amazon CloudWatch cho tỷ lệ trúng cache, các chuyển tiếp điểm cắt, và chi phí thử lại bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), với cảnh báo cho hiệu năng suy giảm.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md)
- [AGENTCOST04-BP01 Thiết kế lựa chọn công cụ tiết kiệm chi phí để tối thiểu các lần gọi không cần thiết](agentcost04-bp01.md)
- [AGENTCOST04-BP02 Tối ưu chi phí phục vụ công cụ thông qua serverless và chia sẻ tài nguyên](agentcost04-bp02.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Optimize LLM response costs and latency with effective caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Gateway tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
