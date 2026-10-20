# AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa

Các agent liên tục lặp lại công việc: các prompt giống hệt nhau, các yêu cầu tương đương về ngữ nghĩa, các bước lập kế hoạch giống nhau qua các tác vụ tương tự. Caching ở các lớp prompt, ngữ nghĩa và plan-template biến sự lặp lại từ một khoản chi phí định kỳ thành một chi phí một lần trả ở lần gọi đầu tiên.

**Kết quả mong muốn:**

- Bạn có prompt caching được bật cho các system prompt ổn định để tiền tố có thể cache được tái sử dụng qua các lần gọi với mức giá giảm.
- Bạn có một semantic cache phục vụ phản hồi cho các yêu cầu tương đương về chức năng vượt trên một ngưỡng tương đồng có thể cấu hình.
- Bạn có các plan template được cache và khởi tạo cho các mẫu tác vụ lặp lại thay vì tạo lại mỗi lần.
- Bạn theo dõi tỷ lệ trúng cache và khoản tiết kiệm chi phí cho mỗi lớp caching.

**Các phản mẫu thường gặp (anti-patterns):**

- Truyền các system prompt và mô tả công cụ giống hệt nhau ở mọi lần gọi với chi phí token đầu vào đầy đủ thay vì mức giá tiền tố đã cache.
- Dùng tra cứu khớp chính xác khi các yêu cầu tương đương về chức năng dùng cách diễn đạt khác nhau, gây trượt cache cho các tác vụ giống hệt về ngữ nghĩa.
- Áp dụng một TTL cache duy nhất cho mọi loại tác vụ mà không phân biệt dữ liệu tham chiếu tĩnh với thông tin nhạy về thời gian, trả về các phản hồi lỗi thời làm suy giảm chất lượng.
- Triển khai các model tùy chỉnh mà không giám sát hiệu năng có cache hỗ trợ, bỏ lỡ các cơ hội xác thực rằng các khoản giảm chi phí kỳ vọng thực sự thành hiện thực.

**Lợi ích khi áp dụng thực hành tốt này:**

- Prompt caching giảm chi phí token đầu vào bằng cách tái sử dụng các chỉ thị hệ thống đã cache qua các lần gọi với mức giá giảm.
- Semantic caching giúp ngăn suy luận dư thừa bằng cách phục vụ các phản hồi đã cache cho các tác vụ tương đương về chức năng.
- Tái sử dụng plan template giảm các lần gọi model cho pha lập kế hoạch của các mẫu tác vụ lặp lại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Caching cho agent hoạt động ở ba lớp riêng biệt, và mỗi lớp có một chế độ lỗi khác nhau.

[Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) là lớp có tác động cao nhất cho các agent với các system prompt lớn, ổn định. Amazon Bedrock lưu trạng thái key-value của tiền tố đã cache và tái sử dụng nó với mức giá giảm. Hãy thiết kế sao cho tiền tố có thể cache (system prompt, mô tả công cụ) ổn định qua các lần gọi, vì bất kỳ nội dung động nào trộn vào đều làm vô hiệu cache. Tái cấu trúc để đưa nội dung đặc thù theo người dùng hoặc theo phiên ra khỏi tiền tố có thể cache.

Semantic caching giải quyết ý tưởng rằng hai yêu cầu có cùng ý nghĩa hiếm khi giống hệt nhau về cách diễn đạt. Tạo một embedding của mỗi yêu cầu đến bằng một model nhẹ và truy vấn [Amazon OpenSearch Service Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) tìm các yêu cầu trước tương tự vượt trên một ngưỡng có thể cấu hình, chẳng hạn cosine similarity lớn hơn 0.95. Ngưỡng giúp bạn tinh chỉnh, vì giá trị cao hơn giảm các dương tính giả nhưng làm giảm tỷ lệ trúng, và giá trị đúng phụ thuộc vào mức độ dung sai biến thiên phản hồi của agent. Lưu các mục cache với TTL được hiệu chỉnh theo yêu cầu độ tươi của từng loại tác vụ, để dữ liệu tham chiếu được cache trong nhiều giờ không làm ô nhiễm các tác vụ cần thông tin thị trường hoặc tồn kho cập nhật.

Đừng bỏ qua plan template caching. Đầu ra lập kế hoạch của agent có tính lặp lại cao cho các mẫu tác vụ lặp lại, như một danh sách kiểm tra onboarding, một phân rã phân loại hỗ trợ, hoặc một kế hoạch luồng công việc báo cáo. Lưu các kế hoạch này theo khóa loại tác vụ và chữ ký tham số đầu vào, và khởi tạo các template đã cache với các tham số hiện tại thay vì tạo lại các kế hoạch mới mỗi lần. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) quản lý trạng thái hội thoại bằng cách trích xuất và lưu bền thông tin then chốt, giảm chi phí token đầu vào từ việc truyền lịch sử lặp lại.

Tính đúng đắn của cache phụ thuộc vào việc vô hiệu hóa (invalidation). Vô hiệu hóa hướng-sự-kiện xóa các mục lỗi thời ngay khi dữ liệu nguồn thay đổi, đó là điều làm cho caching tích cực trở nên an toàn cho dữ liệu biến động vừa phải. Đo tác động bằng AWS Cost Explorer và Amazon CloudWatch tích hợp với [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và cảnh báo khi tỷ lệ trúng rơi xuống dưới mục tiêu.

### Các bước triển khai

- **Bật prompt caching cho các tiền tố ổn định:** Bật [Amazon Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) cho các agent có system prompt lớn hơn 1.000 token, và tái cấu trúc prompt để đưa nội dung động ra khỏi tiền tố có thể cache.
- **Triển khai một lớp semantic cache:** Dựng một chỉ mục OpenSearch Serverless với độ tương đồng dựa trên embedding, cấu hình các ngưỡng tương đồng theo từng loại tác vụ, và đặt TTL theo từng tác vụ. Chỉ chấp nhận lượng tử hóa (quantization) khi tổn thất độ chính xác dưới hai phần trăm về tỷ lệ thành công tác vụ.
- **Cache các plan template:** Đặt khóa các plan template theo loại tác vụ và chữ ký tham số đầu vào, và thực hiện tra cứu trước-khi-gọi trước khi tạo một kế hoạch mới.
- **Dùng bộ nhớ được quản lý cho trạng thái phiên:** Cấu hình các định danh phiên của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) để trạng thái hội thoại nhiều lượt được duy trì mà không cần nối lịch sử thủ công.
- **Thiết kế vô hiệu hóa hướng-sự-kiện và giám sát tỷ lệ trúng:** Nối vô hiệu hóa cache hướng-sự-kiện với các thay đổi dữ liệu nguồn, và tạo các dashboard CloudWatch hiển thị tỷ lệ trúng qua các cache prompt, ngữ nghĩa và plan-template với cảnh báo khi tỷ lệ trúng rơi xuống dưới mục tiêu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng](agentcost02-bp01.md)
- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](agentcost02-bp02.md)
- [AGENTCOST03-BP01 Thiết kế các hệ thống truy xuất tiết kiệm chi phí với bộ nhớ theo tầng](../3-agentcost03/agentcost03-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Prompt Caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- [Effectively use prompt caching on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/effectively-use-prompt-caching-on-amazon-bedrock/)
- [Optimize LLM response costs and latency with effective caching](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
