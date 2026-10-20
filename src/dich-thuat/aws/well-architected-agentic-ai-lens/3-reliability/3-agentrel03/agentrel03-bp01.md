# AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn

Một kho bộ nhớ không phân biệt duy nhất làm nhòe ngữ cảnh hội thoại với kiến thức bền vững và kéo dữ liệu cũ kỹ hoặc không liên quan vào các tác vụ đang hoạt động. Phân loại bộ nhớ tại thời điểm nạp và định tuyến mỗi mục tới đúng tầng giữ cho việc truy xuất có thể dự đoán và chi phí lưu trữ khớp với thời gian mỗi loại thực sự cần tồn tại.

**Kết quả mong muốn:**

- Bạn có một phân loại bộ nhớ tường minh phân biệt ngữ cảnh phiên ngắn hạn với kiến thức bền vững dài hạn.
- Các tác nhân của bạn phân loại thông tin tại thời điểm nạp và định tuyến nó tới tầng phù hợp với các thẻ siêu dữ liệu.
- Bạn lưu giữ mỗi loại bộ nhớ theo một chính sách khớp với yêu cầu độ bền của nó.

**Các phản mẫu thường gặp (anti-patterns):**

- Lưu toàn bộ bộ nhớ trong một kho không phân biệt duy nhất, nên các tác nhân truy xuất các mục cũ kỹ hoặc không liên quan trong các tác vụ đang hoạt động.
- Chạy mà không có chính sách lưu giữ hay đuổi (eviction) cho bộ nhớ ngắn hạn, để ngữ cảnh phiên tích tụ vô thời hạn.
- Bỏ qua phân loại tại thời điểm nạp, khiến việc truy xuất nhắm đích và lưu giữ phù hợp trở nên bất khả thi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Truy xuất có thể dự đoán thông qua phân loại tường minh định tuyến thông tin tới đúng kho.
- Chi phí lưu trữ khớp với yêu cầu độ bền thay vì một cửa sổ lưu giữ cào bằng cho tất cả.
- Giảm ô nhiễm ngữ cảnh vì dữ liệu phiên thoáng qua không thể làm nhiễm kiến thức dài hạn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một phân loại bộ nhớ là nền tảng. Tối thiểu, hãy phân biệt ngắn hạn (thu hẹp phạm vi vào một cuộc hội thoại đơn) với dài hạn (bền vững qua các phiên). Đối với các tác nhân phức tạp, mở rộng phân loại để bao gồm bộ nhớ tình tiết (episodic memory, bản ghi các tương tác quá khứ cụ thể) và bộ nhớ ngữ nghĩa (semantic memory, kiến thức miền tổng quát). Phân loại nên được tài liệu hóa trong tài liệu tham khảo dễ tiếp cận bên cạnh mã, vì các quyết định phân loại diễn ra tại thời điểm nạp và phải nhất quán qua các tác nhân ghi vào bộ nhớ dùng chung.

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cung cấp các namespace bộ nhớ theo phiên và bền vững, xử lý phần hạ tầng bên dưới. Dùng bộ nhớ phiên cho ngữ cảnh ngắn hạn thu hẹp phạm vi vào một cuộc hội thoại đơn, bộ nhớ bền vững cho kiến thức xuyên phiên, và bộ nhớ dùng chung cho các sự kiện mà nhiều tác nhân tiêu thụ. [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) xử lý RAG trên các kho ngữ liệu tài liệu bên ngoài, tài liệu chính sách, danh mục sản phẩm và tài liệu tham khảo miền, những thứ bổ sung cho bộ nhớ của tác nhân bằng kiến thức của tổ chức.

Logic phân loại thuộc về một thành phần riêng trong luồng xử lý của tác nhân, không rải rác khắp các prompt. Đánh giá mỗi mẩu thông tin theo nguồn (lượt hội thoại so với kết quả tác vụ), phạm vi thời gian (theo phiên so với xuyên phiên), và loại nội dung (thủ tục so với sự kiện). Định tuyến tương ứng và gắn thẻ siêu dữ liệu để việc truy xuất về sau có thể lọc chính xác. Giám sát các mẫu truy cập bộ nhớ qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để bắt các bộ nhớ bị phân loại sai. Tín hiệu thường là tỷ lệ truy xuất cao bất ngờ từ sai tầng.

### Các bước triển khai

- **Định nghĩa một phân loại bộ nhớ:** Tài liệu hóa các tiêu chí phân loại cho mỗi loại bộ nhớ (ngữ cảnh phiên, kiến thức bền vững, bản ghi tình tiết) và chính sách lưu giữ phù hợp với mỗi loại.
- **Cấu hình các namespace AgentCore Memory:** Cấp phát [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) với các namespace theo phiên và bền vững ánh xạ tới phân loại.
- **Triển khai logic phân loại tại thời điểm nạp:** Đánh giá mỗi mục theo các tiêu chí phân loại và định tuyến tới tầng phù hợp với các thẻ siêu dữ liệu.
- **Dùng Amazon Bedrock Knowledge Bases cho các kho ngữ liệu bên ngoài:** Bổ sung cho bộ nhớ của tác nhân bằng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) cho RAG trên kiến thức của tổ chức.
- **Giám sát các mẫu truy cập để phát hiện lỗi phân loại:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để phát hiện tỷ lệ truy xuất cao bất ngờ từ sai tầng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP02 Kiến trúc các kho bộ nhớ chịu lỗi với dư thừa và failover](agentrel03-bp02.md)
- [AGENTREL03-BP03 Triển khai quản lý trạng thái toàn diện và phục hồi dựa trên điểm kiểm tra](agentrel03-bp03.md)
- [AGENTREL03-BP04 Triển khai suy giảm nhẹ nhàng cho các thao tác bộ nhớ và trạng thái](agentrel03-bp04.md)
- [AGENTSUS02-BP01 Optimize context management and memory utilization](../../6-sustainability/2-agentsus02/agentsus02-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Memory: Building context-aware agents](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/)
- [Building smarter AI agents: AgentCore long-term memory deep dive](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Strands Agents Session Management](https://strandsagents.com/docs/user-guide/concepts/agents/conversation-management/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)
- [AWS re:Invent 2024 - Make agents remember with AgentCore Memory (AIM331)](https://www.youtube.com/watch?v=Sh0Ro00_rpA)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore - Lab 2: Memory](https://catalog.workshops.aws/agentcore-getting-started/en-US/30-add-memory)
- [Diving Deep into Bedrock AgentCore - Memory](https://catalog.workshops.aws/agentcore-deep-dive/en-US/50-agentcore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
