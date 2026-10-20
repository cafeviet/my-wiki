# AGENTCOST03-BP01 Thiết kế các hệ thống truy xuất tiết kiệm chi phí với bộ nhớ theo tầng

Bộ nhớ của agent phải phục vụ hai nhu cầu đối nghịch cùng lúc: truy cập nhanh cho ngữ cảnh hoạt động, và lưu trữ rẻ cho lịch sử hiếm khi được chạm tới. Bộ nhớ theo tầng khớp mỗi lớp dữ liệu với hạ tầng được định giá cho mẫu truy cập thực tế của nó, và truy xuất chọn lọc giữ chi phí token tỷ lệ với những gì tác vụ hiện tại cần.

**Kết quả mong muốn:**

- Bạn có bộ nhớ làm việc ngắn hạn trên lưu trữ hiệu năng cao và bộ nhớ dài hạn trên các tầng tiết kiệm chi phí, với các chuyển tiếp vòng đời tự động giữa chúng.
- Bạn chỉ truy xuất top-K các mục liên quan cho mỗi bước suy luận thay vì nạp toàn bộ kho bộ nhớ vào ngữ cảnh.
- Bạn theo dõi các thao tác truy xuất theo từng phiên và dùng dữ liệu để tinh chỉnh việc gán tầng và các mẫu truy cập.

**Các phản mẫu thường gặp (anti-patterns):**

- Lưu toàn bộ bộ nhớ agent trong lưu trữ hiệu năng cao đắt tiền bất kể tần suất truy cập, phát sinh chi phí không cần thiết cho các tương tác lịch sử hiếm khi được truy cập.
- Truy xuất toàn bộ kho bộ nhớ cho mỗi bước suy luận, tiêu thụ token đầu vào quá mức trong khi truy xuất top-K có mục tiêu đã đủ.
- Dùng lưu trữ đơn tầng cho toàn bộ bộ nhớ bất kể mẫu truy cập, lãng phí tài nguyên vào hạ tầng đồng nhất cho dữ liệu có các hồ sơ truy cập khác biệt.
- Triển khai các hệ thống bộ nhớ mà không giám sát chi phí truy xuất, che giấu các mẫu truy cập kém hiệu quả bên trong chi phí phiên tổng hợp.

**Lợi ích khi áp dụng thực hành tốt này:**

- Lưu trữ theo tầng khớp mỗi loại bộ nhớ với mẫu truy cập của nó, giảm chi phí cho dữ liệu lịch sử mà không hy sinh hiệu năng phiên hoạt động.
- Truy xuất top-K chọn lọc giới hạn ngữ cảnh vào các mục thích đáng nhất, tránh phí token cho dữ liệu lịch sử không liên quan.
- Quản lý vòng đời tầng tự động mở rộng qua hàng nghìn phiên mà không cần can thiệp thủ công hay cấp phát dư.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Chi phí bộ nhớ của agent đến từ hai quyết định: dữ liệu ở đâu và bạn kéo bao nhiêu vào cửa sổ ngữ cảnh của model. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) xử lý quyết định thứ nhất như một dịch vụ được quản lý. Bộ nhớ ngắn hạn lưu ngữ cảnh phiên theo từng lượt trên lưu trữ nhanh, trong khi bộ nhớ dài hạn trích xuất và hợp nhất các hiểu biết then chốt xuyên các phiên vào các tầng rẻ hơn.

Với các agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), điều này loại bỏ nhu cầu xây dựng các tầng lưu trữ và chính sách thăng giáng bằng tay. Khi cần một triển khai tùy chỉnh, hãy định nghĩa các chính sách thăng cấp và giáng cấp tường minh dựa trên tần suất truy cập để các mục được truy cập thường xuyên ở lại trên lưu trữ độ trễ thấp và các mục hiếm khi được truy cập tự động di trú tới các tầng chi phí thấp hơn.

Khối lượng truy xuất là quyết định thứ hai, và nó có tác động trực tiếp lên chi phí token đầu vào. [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) cung cấp truy xuất vector được quản lý với tìm kiếm ngữ nghĩa. *K* (số chunk trả về cho mỗi truy vấn) là núm điều chỉnh chi phí-chất lượng trung tâm: K cao hơn cho agent nhiều ngữ cảnh hơn nhưng đẩy nhiều token hơn vào mỗi lần gọi. Bắt đầu với K=5 và tinh chỉnh theo sự đánh đổi giữa tính đầy đủ và chi phí, chứ không phải theo sự thiên về an toàn.

Thiết kế chỉ mục là một cân nhắc chi phí ít hiển nhiên hơn nhưng vẫn quan trọng. Với các Knowledge Bases dùng [Amazon OpenSearch Service Serverless](https://aws.amazon.com/opensearch-service/features/serverless/), các tham số HNSW (ef_construction và m) cân bằng chi phí xây chỉ mục với độ chính xác truy vấn và recall. OpenSearch Serverless tính phí dựa trên khối lượng dữ liệu được lập chỉ mục và tính toán truy vấn, nên tinh chỉnh các tham số này là một quyết định chi phí trực tiếp, không chỉ là một quyết định chất lượng. Giá trị ef_construction cao hơn cải thiện recall nhưng làm tăng cả chi phí xây và truy vấn, trong khi giá trị thấp hơn giảm chi phí nhưng có nguy cơ bỏ sót các mục liên quan.

Ngoài ra, hãy cân nhắc gom lô truy xuất (retrieval batching). Nạp trước toàn bộ ngữ cảnh tác vụ lúc khởi tạo và cache nó trong bộ nhớ làm việc của agent tránh chi phí truy xuất theo từng bước. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp dữ liệu đo lường tương thích OpenTelemetry xác định mẫu truy xuất nào đẩy tiêu thụ token cao nhất, và các truy vấn Amazon CloudWatch Logs Insights làm lộ các mẫu truy cập nên định hình việc gán lại tầng.

### Các bước triển khai

- **Áp dụng bộ nhớ theo tầng được quản lý:** Tích hợp [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho bộ nhớ ngắn hạn và dài hạn với quản lý vòng đời tự động, và ghi chép các namespace mà mỗi agent ghi vào và đọc từ.
- **Cấu hình truy xuất chọn lọc:** Dùng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) với tìm kiếm ngữ nghĩa top-K, bắt đầu ở K=5 và tinh chỉnh dựa trên chất lượng suy luận và chi phí token quan sát được.
- **Tinh chỉnh các tham số chỉ mục vector:** Điều chỉnh HNSW ef_construction và m trên kho lưu trữ nền [Amazon OpenSearch Service Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) để cân bằng chi phí xây chỉ mục, độ trễ truy vấn và độ chính xác recall cho workload của bạn.
- **Nạp trước ngữ cảnh lúc khởi tạo tác vụ:** Thay các lần truy xuất theo từng bước bằng một lần nạp trước theo lô lúc bắt đầu tác vụ, được cache trong ngữ cảnh làm việc để model không phải trả chi phí truy xuất ở mỗi bước suy luận.
- **Đo lường các thao tác truy xuất:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và đặt cảnh báo Amazon CloudWatch khi tần suất truy xuất vượt quá các giới hạn kỳ vọng cho mỗi phiên.
- **Xem xét các mẫu truy cập hàng tuần:** Chạy các truy vấn CloudWatch Logs Insights để làm lộ các mẫu truy xuất đắt tiền và các mục chưa từng được truy cập, và dùng kết quả để gán lại tầng và loại bỏ các mục chết.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả](../1-agentcost01/agentcost01-bp02.md)
- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md)
- [AGENTCOST03-BP02 Tối ưu chi phí thông qua nén và cắt tỉa cửa sổ ngữ cảnh một cách thông minh](agentcost03-bp02.md)
- [AGENTCOST03-BP03 Triển khai lưu bền trạng thái và quản lý vòng đời tối ưu chi phí](agentcost03-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)
- [AWS 2025 - AgentCore Memory: Episodic Memory & Patterns](https://www.youtube.com/watch?v=1EEIGsKIjGA)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore - Lab 2: Memory](https://catalog.workshops.aws/agentcore-getting-started/en-US/30-add-memory)
- [Diving Deep into Bedrock AgentCore - Memory](https://catalog.workshops.aws/agentcore-deep-dive/en-US/50-agentcore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
