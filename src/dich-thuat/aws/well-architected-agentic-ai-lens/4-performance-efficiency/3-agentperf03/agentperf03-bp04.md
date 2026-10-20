# AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả

Các tác nhân liên tục lấy cùng một dữ liệu hưởng lợi từ **caching**; phá vỡ vòng lặp truy xuất dư thừa tăng tốc mọi vòng lặp suy luận. Các khối công việc dạng tác nhân thường truy cập cùng các đầu ra **Tools**, tài liệu được truy xuất, các nhúng (embedding) được tính, và dữ liệu cấu hình qua nhiều vòng lặp suy luận, phiên, hoặc tác nhân trong một luồng công việc đa tác nhân. Không có caching, mỗi lần truy cập trả toàn bộ **latency** và chi phí của thao tác gốc.

**Kết quả mong muốn:**

- Bạn có caching đa-lớp loại bỏ các tính toán và lấy-dữ-liệu dư thừa qua các vòng lặp suy luận, phiên, và tác nhân.
- Bạn có tỷ lệ trúng cache được giám sát và tối ưu.
- Bạn có các chính sách vô hiệu hóa cache (invalidation) được tinh chỉnh để cân bằng yêu cầu độ mới với các lợi ích hiệu năng.

**Các phản mẫu thường gặp (anti-patterns):**

- Không triển khai caching nào cả, buộc các tác nhân lấy-lại cùng tài liệu, tính-lại cùng embedding, và gọi-lại cùng Tools trên mỗi vòng lặp suy luận.
- Dùng một TTL cache duy nhất cho mọi loại dữ liệu mà không cân nhắc yêu cầu độ mới, tạo ra hoặc dữ liệu cũ (TTL quá dài) hoặc tỷ lệ trúng kém (TTL quá ngắn).
- Thiết kế khóa cache chỉ dựa trên khớp chuỗi chính xác, bỏ lỡ các lần trúng cache cho các truy vấn tương-đương-ngữ-nghĩa dùng cách diễn đạt khác.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các lần trúng cache giảm đáng kể latency cho truy cập dữ liệu lặp lại.
- Loại các lệnh gọi suy luận LLM dư thừa và các lệnh gọi API bên ngoài giảm chi phí.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Caching được áp ở nhiều lớp của ngăn xếp tác nhân, và mỗi lớp có kỷ luật vô hiệu hóa riêng.

Ở lớp suy luận LLM, [prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) cache và tái dùng các tiền tố prompt chung (như chỉ dẫn hệ thống và định nghĩa Tools) qua các lần gọi, giảm cả latency lẫn chi phí cho các phần lặp lại của prompt; phần tiết kiệm prompt caching chồng chất thêm khi kết hợp với tầng giá Flex của Amazon Bedrock cho các khối công việc phát triển và kiểm thử.

Ở lớp truy xuất, cache các kết quả truy vấn RAG dưới các khóa cache ngữ nghĩa (tương đồng dựa-trên-nhúng) thay vì khớp chuỗi chính xác cho phép các truy vấn tương-đương-ngữ-nghĩa chia sẻ kết quả được cache.

Ở lớp gọi Tools, cache các đầu ra Tools dựa trên các tham số đầu vào với TTL khớp yêu cầu độ mới của dữ liệu, một giá cổ phiếu được cache có TTL rất khác một mô tả công ty được cache.

Làm-ấm cache (cache warming) có giá trị nơi mẫu truy cập có thể dự đoán. Nếu các tác nhân thường truy cập cùng các mục cơ sở tri thức trong giờ làm việc, làm-ấm-trước cache trước các thời kỳ cao điểm tránh phạt trượt-lần-đầu cho những người dùng sớm. Các mẫu truy cập dữ liệu hưởng lợi từ gộp lô (batching): lấy nhiều mục trong một vòng-đi-về (round trip) thay vì thực hiện các yêu cầu riêng lẻ tuần tự giảm cả latency lẫn chi phí kết nối.

Giám sát tỷ lệ trúng cache, phần tiết kiệm latency, và phần tiết kiệm chi phí theo từng lớp cache trong Amazon CloudWatch khiến caching thành một tham số có thể tinh chỉnh.

### Các bước triển khai

- **Nhận diện dữ liệu có thể cache trên toàn ngăn xếp tác nhân:** Liệt kê các tiền tố prompt LLM, kết quả RAG, đầu ra Tools, trạng thái phiên, và dữ liệu cấu hình, mỗi cái có mẫu truy cập, yêu cầu độ mới, và lớp cache riêng.
- **Bật prompt caching của Amazon Bedrock cho các tiền tố prompt chung được chia sẻ qua các lần gọi:** Bật [prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) và cấu trúc prompt để chỉ dẫn hệ thống và định nghĩa Tools xuất hiện trước nội dung biến thiên, cho phép tiền tố được cache được tái dùng qua các yêu cầu.
- **Triển khai caching kết quả truy xuất với khóa cache ngữ nghĩa và TTL riêng-cho-loại-dữ-liệu:** Cache các kết quả RAG dưới các khóa tương đồng dựa-trên-nhúng để các truy vấn tương-đương-ngữ-nghĩa chia sẻ kết quả, và tinh chỉnh TTL theo nhu cầu độ mới của mỗi loại dữ liệu thay vì áp một TTL toàn cục duy nhất.
- **Triển khai caching đầu ra Tools với TTL được hiệu chỉnh theo yêu cầu độ mới của dữ liệu:** Cache các đầu ra Tools dưới các khóa tham-số-đầu-vào với TTL khớp tốc độ dữ liệu mỗi Tool thay đổi, TTL ngắn cho dữ liệu thời-gian-thực, TTL dài cho dữ liệu tham chiếu tĩnh.
- **Giám sát tỷ lệ trúng cache và phần tiết kiệm latency theo từng lớp cache dùng CloudWatch:** Công bố tỷ lệ trúng, tỷ lệ trượt, và phần tiết kiệm latency theo từng lớp cache dưới dạng chỉ số CloudWatch để TTL và chiến lược làm-ấm có thể được tinh chỉnh từ dữ liệu thay vì giả định.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP01 Triển khai các hệ thống quản lý bộ nhớ phân tầng](agentperf03-bp01.md)
- [AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác](agentperf03-bp03.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](../2-agentperf02/agentperf02-bp03.md)

**Tài liệu liên quan:**

- [Prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- [Blog: Dùng prompt caching hiệu quả trên Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effectively-use-prompt-caching-on-amazon-bedrock/)
- [Blog: Tối ưu chi phí và latency phản hồi LLM với caching hiệu quả](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
