# AGENTPERF03-BP05 Triển khai các mẫu truy xuất dạng tác nhân cho truy cập tri thức động, do-tác-nhân-điều-khiển

Các câu hỏi phức tạp thường đòi hỏi thông tin từ nhiều nguồn, tinh chỉnh lặp đi lặp lại, hoặc dữ liệu thời-gian-thực mà một lần truy xuất duy nhất không thể cung cấp. Trong truy xuất dạng tác nhân, tác nhân chủ động kiểm soát quá trình truy xuất như một phần của vòng lặp suy luận của nó, quyết định khi nào truy xuất, truy xuất cái gì, dùng **Tool** truy xuất nào, và liệu ngữ cảnh được truy xuất có đủ trước khi tiếp tục. Mỗi vòng lặp thêm chi phí sinh nhúng (embedding), tìm kiếm vector, re-ranking, và chèn ngữ cảnh, nên vòng lặp truy xuất cần các điều kiện kết thúc tường minh.

**Kết quả mong muốn:**

- Bạn có các tác nhân truy xuất đúng thông tin trong số vòng lặp tối thiểu cần thiết.
- Bạn có các câu hỏi đơn giản được trả lời bằng một lần truy xuất duy nhất và các câu hỏi phức tạp được xử lý qua truy xuất đa-bước (multi-hop) có cấu trúc với các điều kiện kết thúc tường minh.
- Bạn có tác nhân chọn Tool truy xuất phù hợp nhất cho mỗi loại truy vấn.
- Bạn có số vòng lặp truy xuất, latency mỗi-vòng-lặp, và tỷ lệ đủ (sufficiency rate) được theo dõi và tối ưu.

**Các phản mẫu thường gặp (anti-patterns):**

- Coi mọi truy xuất là một bước tiền-xử-lý một-phát duy nhất, buộc tác nhân làm việc với bất kỳ ngữ cảnh nào được truy xuất ở lần thử đầu bất kể độ đủ.
- Cho phép các tác nhân truy xuất lặp lại mà không có ngân sách truy xuất hoặc điều kiện kết thúc, tạo ra các vòng lặp truy xuất vô giới hạn tiêu tốn token và latency mà không hội tụ.
- Định tuyến mọi truy xuất qua một pipeline duy nhất bất kể loại truy vấn, bỏ lỡ các cơ hội dùng các Tools truy xuất nhanh hơn hoặc phù hợp hơn cho các nhu cầu thông tin khác nhau.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thực thi truy-vấn-con song song và định tuyến Tool truy xuất giảm latency đầu-cuối bằng cách chọn nguồn phù hợp nhanh nhất.
- Các ngân sách tường minh giới hạn số vòng lặp và tổng token giữ chi phí truy xuất trong tầm kiểm soát.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Thiết kế truy xuất như một tập Tools tác nhân thay vì một pipeline nguyên khối. Các Tools truy xuất riêng biệt cho các mẫu truy cập tri thức khác nhau cho phép tác nhân định tuyến tới nguồn đúng:

- Một Tool tìm kiếm ngữ nghĩa được hậu thuẫn bởi [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) cho các câu hỏi khái niệm
- Một Tool truy vấn có cấu trúc cho các tra cứu chính xác theo định danh
- Một Tool dữ liệu thời-gian-thực cho thông tin đòi hỏi giá trị hiện tại
- Một Tool tìm kiếm web cho các câu hỏi vượt ra ngoài cơ sở tri thức của tổ chức
- Một Tool xử lý tài liệu được hậu thuẫn bởi [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) để trích xuất dữ liệu có cấu trúc từ hình ảnh, biểu mẫu, và bảng

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) phơi bày các Tools truy xuất dưới dạng các endpoint tương thích MCP, và đăng ký mỗi Tool với các mô tả rõ ràng, nó xử lý loại câu hỏi nào, truy cập nguồn dữ liệu nào, và latency kỳ vọng của nó, hướng dẫn việc lựa chọn Tool của tác nhân.

Đánh giá đủ truy xuất (retrieval sufficiency evaluation) là một đánh giá nhẹ sau mỗi vòng lặp truy xuất, thường được chạy bởi một Model nhỏ hơn, nhanh hơn. Trình đánh giá phán đoán liệu ngữ cảnh được truy xuất có đủ, nhận diện các khoảng trống, và hình thành các truy vấn được tinh chỉnh. Một giới hạn vòng lặp truy xuất cực đại (thường 2-3 vòng lặp) giúp ngăn các vòng lặp vô giới hạn. Nếu tác nhân chưa truy xuất đủ ngữ cảnh trong ngân sách, nó tiếp tục với ngữ cảnh tốt nhất sẵn có và truyền đạt sự bất định.

Với các câu hỏi phức tạp đòi hỏi nhiều nguồn, phân rã truy vấn (query decomposition) chia câu hỏi thành các truy-vấn-con tập trung và chạy các truy-vấn-con độc lập một cách đồng thời. Các ngân sách hiệu năng truy xuất theo-tác-vụ, suy ra từ SLO latency tổng thể của tác vụ, giữ mẫu lặp trong mục tiêu của khối công việc.

### Các bước triển khai

- **Triển khai các Tools truy xuất riêng biệt cho các mẫu truy cập tri thức khác nhau:** Đăng ký một Tool tìm kiếm ngữ nghĩa, một Tool truy-vấn-có-cấu-trúc, một Tool dữ liệu thời-gian-thực, một Tool tìm kiếm web, và một Tool xử lý tài liệu qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với các mô tả rõ ràng hướng dẫn việc lựa chọn Tool của tác nhân.
- **Triển khai đánh giá đủ truy xuất như một đánh giá nhẹ sau-truy-xuất:** Dùng một Model nhỏ, nhanh để phán đoán liệu ngữ cảnh được truy xuất có đủ, nhận diện các khoảng trống, và hình thành các truy vấn được tinh chỉnh cho vòng lặp tiếp theo.
- **Cấu hình giới hạn vòng lặp truy xuất cực đại với dự phòng nhẹ nhàng về ngữ cảnh tốt-nhất-sẵn-có:** Giới hạn vòng lặp ở 2-3 cho hầu hết tác vụ, và khi ngân sách cạn kiệt tiếp tục với ngữ cảnh tốt nhất thu được và truyền đạt sự bất định thay vì lặp vô giới hạn.
- **Triển khai phân rã truy vấn cho các câu hỏi phức tạp, chạy các truy-vấn-con độc lập một cách đồng thời:** Chia các câu hỏi đa-nguồn thành các truy-vấn-con tập trung và tỏa ra song song để latency truy-vấn-con không tích lũy tuần tự.
- **Định nghĩa các ngân sách hiệu năng truy xuất theo-tác-vụ dựa trên SLO latency tổng thể:** Phân bổ một phần tường minh của SLO latency của tác vụ cho truy xuất để mẫu lặp không thể âm thầm tiêu ngân sách dành cho suy luận hoặc các lệnh gọi Tools hạ nguồn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác](agentperf03-bp03.md)
- [AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt](agentperf03-bp02.md)
- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](../2-agentperf02/agentperf02-bp01.md)
- [AGENTREL05-BP03 Đặt nhận thức tác nhân trên nền thông tin thực](../../3-reliability/5-agentrel05/agentrel05-bp03.md)
- [AGENTCOST03-BP02 Tối ưu chi phí qua nén và cắt tỉa context window thông minh](../../5-cost-optimization/3-agentcost03/agentcost03-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Blog: Xây dựng tìm kiếm thông minh với Amazon Bedrock và Amazon OpenSearch Service cho các giải pháp RAG lai](https://aws.amazon.com/blogs/machine-learning/building-intelligent-search-with-amazon-bedrock-and-amazon-opensearch-for-hybrid-rag-solutions/)

**Ví dụ liên quan:**

- [GitHub: RAG nâng cao dùng Bedrock và SageMaker AI](https://github.com/aws-samples/sample-advanced-rag-using-bedrock-and-sagemaker)

**Dịch vụ liên quan:**

- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)
- [Amazon Bedrock AgentCore Gateway](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
