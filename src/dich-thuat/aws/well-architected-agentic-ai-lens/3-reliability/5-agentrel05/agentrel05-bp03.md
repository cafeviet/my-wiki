# AGENTREL05-BP03 Đặt nền nhận thức của tác nhân trên thông tin thực

Dữ liệu huấn luyện có một mốc cắt và một tác nhân chỉ suy luận từ kiến thức của mô hình có thể tạo ảo giác về hiện tại. Sinh tăng cường truy xuất (RAG) đặt nền mỗi câu trả lời trên thông tin hiện thời, đặc thù miền và giảm tỷ lệ ảo giác như một hệ quả kèm theo.

**Kết quả mong muốn:**

- Bạn có các đường ống truy xuất đặt nền suy luận của tác nhân trên thông tin hiện thời, đặc thù miền.
- Bạn kiểm định độ mới của kiến thức và gắn cờ nội dung vượt quá các ngưỡng cũ kỹ (staleness).
- Bạn xử lý các lỗi truy xuất một cách nhẹ nhàng, để các tác nhân tiếp tục với kiến thức của mô hình trong khi truyền đạt sự bất định.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ dựa vào dữ liệu huấn luyện của mô hình cho kiến thức đặc thù miền, tạo ra các đầu ra có thể lỗi thời hoặc không chính xác.
- Chạy truy xuất mà không kiểm định độ mới, khiến các tác nhân suy luận từ dữ liệu cũ kỹ.
- Coi truy xuất là một phụ thuộc cứng, nên các lỗi truy xuất lan thành lỗi tác nhân.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tỷ lệ ảo giác giảm vì suy luận được đặt nền trên thông tin sự kiện được truy xuất.
- Độ chính xác về sự kiện cải thiện thông qua truy cập kiến thức hiện thời, đặc thù miền.
- Độ tin cậy được duy trì khi môi trường vận hành tiến hóa thông qua các cập nhật knowledge base.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) xử lý các cơ chế của RAG, nạp tài liệu, chunking, embedding và lưu trữ vector, nên hầu hết việc thiết lập là cấu hình chứ không phải hạ tầng. Cấu hình các nguồn dữ liệu phản ánh miền của tác nhân và thiết lập đồng bộ hóa tự động để giữ nội dung hiện thời. Các thông báo sự kiện S3 kích hoạt các thao tác đồng bộ khi tài liệu nguồn được cập nhật, và API nạp trực tiếp của Knowledge Bases xử lý nội dung theo chương trình. Chiến lược chunking quan trọng. Các đoạn (chunk) nhỏ hơn tạo ra truy xuất sự kiện chính xác, trong khi các đoạn lớn hơn tạo ra hiểu biết ngữ cảnh tốt hơn. Các mô hình reranking chấm điểm lại các đoạn được truy xuất để có ngữ cảnh chất lượng cao hơn.

Một knowledge base được điền lúc khởi chạy và không bao giờ làm mới sẽ trở thành nguồn của các câu trả lời sai theo thời gian. Theo dõi các dấu thời gian nạp và gắn cờ nội dung vượt quá các ngưỡng cũ kỹ trước khi nó được phục vụ. Đối với thông tin đòi hỏi độ chính xác thời gian thực (giá, tồn kho và trạng thái hệ thống), cache là không đủ. Triển khai các hàm công cụ mà các tác nhân gọi để truy xuất dữ liệu từ các nguồn có thẩm quyền qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), và coi nguồn có thẩm quyền là nguồn sự thật duy nhất.

[Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) trích xuất dữ liệu có cấu trúc từ tài liệu, biểu mẫu và bảng, để các tác nhân suy luận trên nội dung đã trích xuất thay vì hình ảnh thô. Việc đánh giá chất lượng ngữ cảnh được truy xuất lọc các kết quả liên quan thấp và khử trùng lặp các đoạn dư thừa trước khi tiêm vào prompt. Nếu không, cửa sổ ngữ cảnh lấp đầy nhiễu làm át tín hiệu. Xử lý các lỗi truy xuất bằng cách cho phép tác nhân tiếp tục với kiến thức của mô hình trong khi truyền đạt sự bất định về độ hiện thời của thông tin. Một câu minh bạch "Tôi đang làm việc từ kiến thức tổng quát thay vì dữ liệu hiện thời" tốt hơn việc âm thầm dựa vào dữ liệu huấn luyện.

### Các bước triển khai

- **Cấu hình Amazon Bedrock Knowledge Bases với đồng bộ hóa tự động:** Thiết lập [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) với các nguồn dữ liệu phù hợp với miền và các đường ống đồng bộ được kích hoạt bởi các thay đổi nguồn.
- **Triển khai kiểm định độ mới của kiến thức:** Theo dõi các dấu thời gian nạp và gắn cờ nội dung cũ kỹ trước khi nó được phục vụ.
- **Dùng reranking của Knowledge Bases:** Chấm điểm lại các đoạn được truy xuất để tiêm ngữ cảnh chất lượng cao hơn.
- **Triển khai các công cụ truy xuất dữ liệu thời gian thực qua AgentCore Gateway:** Dùng các hàm công cụ của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cho thông tin đòi hỏi độ chính xác hiện thời.
- **Xử lý các lỗi truy xuất một cách nhẹ nhàng:** Cho phép các tác nhân tiếp tục với kiến thức của mô hình trong khi truyền đạt sự bất định về độ hiện thời của thông tin.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn](../3-agentrel03/agentrel03-bp01.md)
- [AGENTREL05-BP01 Thiết kế các thành phần suy luận của tác nhân mô-đun, chịu lỗi](agentrel05-bp01.md)
- [AGENTREL05-BP02 Tạo điều kiện cho thích ứng đáng tin cậy qua các chu kỳ cải tiến dẫn dắt bởi kiểm định](agentrel05-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Advanced agentic RAG Systems: Deep dive with Bedrock (AIM425)](https://www.youtube.com/watch?v=bu2cD1pCFTs)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agent-samples - Knowledge Base integration](https://github.com/awslabs/amazon-bedrock-agent-samples/tree/main/examples/agents/agent_with_knowledge_base_integration)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
