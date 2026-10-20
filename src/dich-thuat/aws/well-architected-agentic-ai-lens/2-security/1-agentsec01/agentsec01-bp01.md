# AGENTSEC01-BP01 Triển khai kiểm soát cô lập và toàn vẹn bộ nhớ

Bộ nhớ agent dùng chung là con đường ngắn nhất để một phiên bị ảnh hưởng làm nhiễm bẩn mọi phiên khác. Việc phân vùng bộ nhớ theo các ranh giới quan trọng đối với khối công việc, và xác minh những gì được trả ra, giúp giới hạn phạm vi của việc đầu độc bộ nhớ chỉ trong phân vùng bị chạm tới.

**Kết quả mong muốn:**

- Bạn phân vùng bộ nhớ agent theo các trục cô lập phù hợp với khối công việc (phiên, người dùng, tenant, agent hoặc nhóm), không có nhiễm chéo giữa các ngữ cảnh.
- Bạn phát hiện việc chỉnh sửa trái phép các bộ nhớ đã lưu thông qua các phép kiểm tra tính toàn vẹn và duy trì lịch sử thay đổi trạng thái có bằng chứng chống can thiệp (tamper-evident).
- Bạn giới hạn phạm vi truy cập bộ nhớ theo từng agent thông qua các chính sách IAM đặc quyền tối thiểu (least privilege), để mỗi agent chỉ có thể đọc hoặc ghi những namespace mà nó được ủy quyền.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng chung bộ nhớ giữa các agent hoặc phiên theo mặc định, khiến một phiên bị ảnh hưởng có thể đọc hoặc ghi đè ngữ cảnh của phiên khác và việc đầu độc lan ngang.
- Lưu bộ nhớ agent ở dạng văn bản thô không mã hóa tại chỗ, làm lộ ngữ cảnh suy luận, kết quả công cụ trung gian và dữ liệu người dùng nếu kho lưu trữ nền bị truy cập qua một chính sách IAM sai cấu hình hoặc lỗ hổng phơi bày kho lưu trữ.
- Bỏ qua các phép kiểm tra toàn vẹn khi đọc bộ nhớ, để cho các bộ nhớ bị hỏng hoặc bị tiêm nhiễm âm thầm ảnh hưởng đến quyết định và tích lũy qua các phiên.
- Cấp cho mọi agent quyền đọc/ghi rộng trên toàn bộ kho bộ nhớ, tạo ra một mô hình tin cậy phẳng nơi bất kỳ agent bị ảnh hưởng nào cũng chạm tới các luồng công việc không liên quan.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phân vùng bộ nhớ theo từng phiên và từng agent giới hạn phạm vi của bất kỳ agent đơn lẻ nào bị ảnh hưởng.
- Xác minh tính toàn vẹn bằng mật mã trên các lượt đọc bộ nhớ bắt được các ý đồ đầu độc trước khi dữ liệu bị ảnh hưởng tác động đến quyết định.
- Truy cập bộ nhớ được giới hạn phạm vi bằng IAM giới hạn mỗi agent chỉ ở các phân vùng nó cần, giảm khả năng di chuyển ngang.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Đầu độc bộ nhớ là một vấn đề di chuyển ngang (lateral-movement). Nếu mọi agent đều đọc từ cùng một hồ chứa, một lượt ghi bị ảnh hưởng sẽ trở thành đầu vào của mọi agent, và cái giá của một lần tiêm nhiễm thành công là tính đúng đắn của toàn bộ hệ thống. Thay đổi về mặt thiết kế là coi bộ nhớ như một kho dữ liệu có nhận thức về tenant ngay từ đầu. Hãy phân vùng nó theo các ranh giới thực sự quan trọng đối với khối công việc:

- Phiên (Session)
- Người dùng (User)
- Tenant
- Agent
- Nhóm (Group)

Hãy biến truy cập xuyên phân vùng thành ngoại lệ mà bạn phải cấp một cách tường minh, chứ không phải mặc định mà bạn phải ngăn chặn một cách tường minh.

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) thể hiện việc phân vùng này thông qua một hệ thống namespace phân cấp được xây dựng trên các định danh actorId và sessionId, với các placeholder động như {actorId} và {sessionId} được phân giải tại thời điểm gọi. Một mẫu namespace như /support-agent/{actorId}/preferences cho mỗi người dùng một phân vùng được giới hạn phạm vi tự động mà không cần mã hóa cứng định danh. Phiên đang gọi quyết định namespace mà agent đọc từ đó hoặc ghi vào, và chính sách IAM trên vai trò (role) của agent giới hạn các tiền tố namespace mà nó có thể chạm tới, nên ngay cả một namespace được agent dựng sai vẫn bị lớp ủy quyền từ chối.

Namespace dùng chung không phải là phản mẫu khi chúng có chủ đích. Một cơ sở tri thức sản phẩm chung được mọi support agent đọc, một ngữ cảnh làm việc giới hạn theo nhóm, hay một bộ nhớ điều phối nơi các agent hợp tác trao đổi kết quả trung gian đều là các phân vùng dùng chung hợp lệ. Hãy mô hình hóa chúng thành các namespace có tên (ví dụ, /support-agent/shared/product-knowledge hoặc /team-{teamId}/shared/working-context) và giới hạn phạm vi chính sách IAM của mỗi vai trò agent tới đúng các namespace dùng chung mà agent đó được ủy quyền chạm tới. Kiểu lỗi cần giúp ngăn chặn là dùng chung theo mặc định, chứ không phải việc dùng chung đã được thiết kế và ủy quyền.

Tính toàn vẹn là nửa còn lại của mô hình. AgentCore Memory giữ một dấu vết kiểm toán chỉ-thêm (append-only) nơi quá trình hợp nhất đánh dấu các bản ghi lỗi thời là INVALID thay vì xóa chúng, nên toàn bộ chuỗi thay đổi có thể khôi phục để phân tích điều tra. Điều đó giúp bảo vệ lịch sử, nhưng nó không phát hiện được liệu một bản ghi cụ thể có bị chỉnh sửa âm thầm bên ngoài luồng hợp nhất bình thường hay không. Chữ ký HMAC của AWS KMS xếp thêm lớp phát hiện can thiệp trên từng bản ghi: ký khi ghi, tính lại và so sánh khi đọc, và coi một sự không khớp là bằng chứng cho thấy bản ghi đã bị thay đổi. Kết hợp điều đó với các khóa AWS KMS do khách hàng quản lý trên chính tài nguyên bộ nhớ (thông qua tham số encryptionKeyArn) cho ngữ cảnh suy luận nhạy cảm, và các chiến lược bộ nhớ dựng sẵn sẽ lọc thông tin định danh cá nhân (PII) khỏi các bản ghi dài hạn theo mặc định.

Giám sát hoàn thiện kiểm soát này. Hãy định tuyến các sự kiện truy cập bộ nhớ tới Amazon CloudWatch Logs, cảnh báo về các ý đồ truy xuất xuyên namespace và các lượt ghi tần suất cao từ một agent đơn lẻ, và chạy các bài tập red-team mô phỏng đầu độc bộ nhớ để kiểm chứng rằng các kiểm soát cô lập đứng vững dưới áp lực.

### Các bước triển khai

- **Tạo tài nguyên bộ nhớ với mã hóa do khách hàng quản lý:** Cấp phát một tài nguyên [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html), chỉ định encryptionKeyArn với một khóa AWS KMS do khách hàng quản lý cho các khối công việc nhạy cảm, và đặt eventExpiryDuration khớp với yêu cầu lưu giữ dữ liệu của bạn.
- **Thiết kế lược đồ namespace phân cấp:** Dùng các placeholder động ({actorId}, {sessionId}) để tự động phân vùng bộ nhớ theo từng người dùng và từng phiên, ví dụ /support-agent/{actorId}/preferences cho dữ liệu giới hạn theo người dùng và /support-agent/shared/product-knowledge cho ngữ cảnh dùng chung có chủ đích.
- **Cấu hình chiến lược bộ nhớ ở đúng cấp độ cô lập:** Áp dụng các chiến lược ngữ nghĩa (semantic), tùy chọn người dùng (user preferences), tóm tắt (summary) hoặc tùy chỉnh (custom) với namespace được giới hạn phạm vi ở phân vùng bạn muốn, và dùng các ghi đè chiến lược tùy chỉnh khi cần các prompt trích xuất và hợp nhất theo miền cụ thể.
- **Giới hạn phạm vi vai trò IAM chỉ tới các namespace được ủy quyền:** Cấp cho mỗi agent một vai trò IAM riêng với các chính sách dựa trên tài nguyên chỉ cho phép các tiền tố namespace nó cần, từ chối tất cả namespace khác theo mặc định.
- **Thực thi truy xuất giới hạn theo namespace trong mã của agent:** Gọi retrieve_memory_records và list_events chỉ trong các namespace được ủy quyền của agent, để dữ liệu xuyên tenant bị chặn ở cả lớp ứng dụng lẫn lớp ủy quyền.
- **Xếp lớp xác minh toàn vẹn HMAC trên các bản ghi nhạy cảm:** Với các khối công việc cần phát hiện can thiệp vượt ra ngoài dấu vết kiểm toán dựng sẵn, hãy lưu một HMAC do KMS tạo cùng với mỗi mục bộ nhớ và xác minh nó khi đọc trước khi nội dung tác động đến quyết định của agent.
- **Cảnh báo về các bất thường trong truy cập bộ nhớ:** Cấu hình các cảnh báo Amazon CloudWatch cho các ý đồ truy xuất xuyên namespace, các lượt ghi tần suất cao từ một agent đơn lẻ, và các đợt tăng đột biến trong thất bại trích xuất bộ nhớ, rồi định tuyến cảnh báo qua Amazon EventBridge để ứng phó sự cố tự động.
- **Kiểm toán các chiến lược và chạy bài tập red-team:** Định kỳ xem xét các mẫu trích xuất và hợp nhất bằng list_memories và retrieve_memory_records để kiểm chứng rằng các chiến lược đang thu thập đúng thông tin và việc lọc PII đang hoạt động, và mô phỏng các kịch bản đầu độc bộ nhớ để kiểm chứng các kiểm soát cô lập đứng vững.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC01-BP02 Kiểm định và làm sạch đầu vào bộ nhớ](agentsec01-bp02.md)
- [AGENTSEC01-BP03 Giám sát sự lan truyền ảo giác](agentsec01-bp03.md)
- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](../3-agentsec03/agentsec03-bp03.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Memory: Building context-aware agents](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/)
- [Building smarter AI agents: AgentCore long-term memory deep dive](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Key Management Service](https://aws.amazon.com/kms/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
