# AGENTSUS02-BP01 Tối ưu hóa quản lý ngữ cảnh và sử dụng bộ nhớ

Bộ nhớ Agent phình to không giới hạn buộc mỗi lần truy xuất phải tìm kiếm qua các kho ngày càng lớn và mỗi lượt (turn) phải xử lý lại lịch sử mà Agent đã thấy. Bộ nhớ phân tầng với các chính sách lưu giữ giữ cho hạ tầng được điều chỉnh theo ngữ cảnh thực sự quan trọng, để các thao tác bộ nhớ luôn nhanh và chi phí bộ nhớ giữ tỷ lệ thuận với mức dùng.

**Kết quả mong muốn:**

- Bạn có bộ nhớ phân tầng với ngữ cảnh phiên hoạt động được tách khỏi dữ liệu lưu trữ, để các tầng nóng và lạnh không cạnh tranh cùng một kho lưu trữ.
- Các chính sách lưu giữ, lưu trữ (archival) và cắt tỉa giữ cho bộ nhớ có giới hạn và tự động chuyển ngữ cảnh cũ dần tới tầng phù hợp.
- Các hệ thống đa Agent chia sẻ ngữ cảnh bền vững qua các namespace thay vì nhân bản nó cho mỗi Agent.
- Các Agent xây dựng ngữ cảnh theo cách tăng dần thay vì xử lý lại toàn bộ lịch sử tương tác trong mỗi lượt.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai bộ nhớ phẳng không phân tầng, nên ngữ cảnh phiên nóng cạnh tranh với dữ liệu lưu trữ cùng một kho và đường truy cập.
- Bỏ qua các chính sách lưu giữ, lưu trữ và cắt tỉa, để bộ nhớ tích lũy vô hạn định và buộc mỗi lần truy xuất phải quét một kho ngày càng lớn hơn.
- Xử lý lại toàn bộ ngữ cảnh lịch sử trong mỗi lượt thay vì chỉ lấy phần lát cắt liên quan, tạo ra các thao tác truy xuất dư thừa mà không cải thiện chất lượng phản hồi.
- Nhân bản ngữ cảnh dùng chung qua kho bộ nhớ của mỗi Agent thay vì đọc từ một namespace dùng chung, tạo ra sự phình lưu trữ tuyến tính theo số lượng Agent.

**Lợi ích khi áp dụng thực hành tốt này:**

- Hạ tầng bộ nhớ mở rộng theo ngữ cảnh thực sự quan trọng, không phải theo lịch sử tích lũy.
- Truy xuất ngữ nghĩa trả về lát cắt ngữ cảnh liên quan trong thời gian hằng số thay vì tăng theo kích thước kho.
- Các hệ thống đa Agent chia sẻ lưu trữ cho ngữ cảnh chung, giảm bộ nhớ nhân bản trên toàn đội hình.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Không phải mọi ngữ cảnh Agent đều hoạt động như nhau. Một lượt gần đây trong một phiên đang diễn ra hành xử rất khác một bản ghi từ ba tháng trước. Cái đầu cần truy cập ở mức mili-giây trong mỗi lượt, còn cái sau cần khả dụng cho việc truy xuất thỉnh thoảng. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cung cấp cơ chế phân tầng tích hợp sẵn tách biệt hai trường hợp này, với bộ nhớ làm việc được tối ưu cho các phiên hoạt động và lưu trữ dài hạn cho ngữ cảnh cũ hơn. Các chính sách lưu giữ chuyển ngữ cảnh giữa các tầng một cách tự động, để tầng nóng giữ nhỏ và tầng lạnh giữ rẻ.

Ngữ cảnh bền vững dùng chung là một phần của kiến trúc nơi nhiều hệ thống đa Agent thất bại. Khi năm Agent mỗi cái duy trì bản sao riêng của cùng một tài liệu tham chiếu, lưu trữ phình nhanh gấp năm lần so với mức nhu cầu tổ chức thực sự đòi hỏi. Cách tổ chức dựa trên namespace của AgentCore Memory cho phép nhiều Agent đọc từ và ghi vào các namespace chung được giới hạn phạm vi bởi các chính sách IAM — một kho, nhiều bên đọc. Đây là lưu trữ dùng chung, không phải bộ nhớ trong-tiến-trình dùng chung, nên tính nhất quán và kiểm soát truy cập giữ được tường minh. Riêng biệt, [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) là nơi phù hợp cho tri thức tổ chức, FAQ và tài liệu tham chiếu mà các Agent truy vấn để làm giàu ngữ cảnh. Nó bổ trợ cho AgentCore Memory thay vì thay thế.

Gửi toàn bộ lịch sử tương tác vào mỗi lệnh gọi Model trông có vẻ đúng nhưng phải trả tiền để xử lý lại thông tin mà Model đã thấy.

Mẫu tốt hơn là tăng dần. Duy trì các phiên có trạng thái (stateful) bảo tồn ngữ cảnh làm việc qua các lượt, tóm tắt các đoạn cũ hơn thành các biểu diễn cô đọng khi chúng già đi khỏi cửa sổ tức thời, và dùng tìm kiếm ngữ nghĩa qua Knowledge Bases với vector embeddings để chỉ truy xuất lát cắt lịch sử liên quan thay vì toàn bộ bản ghi. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) lộ các thao tác bộ nhớ nào là thường xuyên và các tầng nào bị sử dụng thiếu hoặc thừa, để việc cấp phát luôn dựa trên mức dùng thực tế.

### Các bước triển khai

- **Cấu hình bộ nhớ phân tầng với các chính sách vòng đời:** Dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho ngữ cảnh phiên hoạt động với các chính sách lưu giữ tự động chuyển ngữ cảnh cũ dần tới lưu trữ dài hạn.
- **Thiết lập các namespace dùng chung cho ngữ cảnh đa Agent:** Tạo các namespace AgentCore Memory mà nhiều Agent đọc từ và ghi vào, được giới hạn phạm vi bởi các chính sách IAM, để ngữ cảnh bền vững dùng chung được lưu một lần thay vì nhân bản theo từng Agent.
- **Dùng truy xuất ngữ nghĩa cho ngữ cảnh lịch sử:** Cấu hình [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) với vector embeddings để các truy vấn chỉ truy xuất lát cắt ngữ cảnh lịch sử liên quan thay vì toàn bộ bản ghi.
- **Nén ngữ cảnh cũ:** Áp dụng tóm tắt (summarization) bằng các Model nền Amazon Bedrock để cô đọng các đoạn tương tác cũ hơn thành các biểu diễn gọn nhẹ bảo toàn ý nghĩa với chi phí token chỉ bằng một phần nhỏ.
- **Giám sát các mẫu truy cập bộ nhớ và tái cân bằng các tầng:** Theo dõi tỷ lệ hit của tầng, độ trễ truy xuất và kích thước kho qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và điều chỉnh cửa sổ lưu giữ cùng việc cấp phát tầng dựa trên mức dùng quan sát được.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS02-BP02 Thiết lập các chiến lược caching Agent hiệu quả](agentsus02-bp02.md)
- [AGENTSUS02-BP03 Mở rộng các phụ thuộc dữ liệu, mạng và compute một cách phù hợp](agentsus02-bp03.md)
- [SUS02-BP01 Scale workload infrastructure dynamically](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_user_a2.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Memory: Building context-aware agents](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/)
- [Building smarter AI agents: AgentCore long-term memory deep dive](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Các video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)

**Các ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
