# AGENTOPS07-BP02 Thiết lập các hệ thống quản lý tri thức vận hành

Các nhóm nắm bắt những gì họ học được từ các sự cố sẽ xây dựng trí nhớ thể chế (institutional memory) tồn tại qua các thay đổi nhân sự. Các nhóm không làm điều đó sẽ mất đi insight ngay khi người có nó rời đi, và trả cho cùng một bài học lần thứ hai.

**Kết quả mong muốn:**

- Tri thức vận hành về hành vi agent, các chế độ lỗi, và các quy trình giải quyết được nắm bắt có hệ thống và có thể truy cập bởi mọi thành viên nhóm.
- Các buổi rà soát sau sự cố (post-incident reviews) nhất quán tạo ra các insight thực tế được tích hợp vào các runbook và các quy trình vận hành.
- Tri thức thể chế tồn tại qua các thay đổi nhân sự, cho phép các thành viên nhóm mới trở nên hiệu quả nhanh chóng.
- Tri thức về các can thiệp thành công được nắm bắt bên cạnh các chế độ lỗi, để những gì hiệu quả được ghi nhớ tin cậy như những gì thất bại.

**Các phản mẫu thường gặp (anti-patterns):**

- Dựa vào tri thức nằm ở từng thành viên nhóm thay vì tri thức vận hành được tài liệu hóa, tạo ra các điểm lỗi đơn (single points of failure) khi con người rời đi.
- Tiến hành các buổi rà soát sau sự cố tạo ra các báo cáo nhưng không dẫn tới các thay đổi thực tế trong các runbook hoặc quy trình.
- Lưu tri thức vận hành trong các kho đặc thù nhóm không thể truy cập bởi các nhóm khác, làm giảm rủi ro chia sẻ và tạo ra nỗ lực trùng lặp.
- Xem quản lý tri thức như một bài tập tài liệu thay vì một thực hành vận hành chủ động, tạo ra các tài liệu được tạo một lần và không bao giờ được cập nhật.
- Không nắm bắt tri thức về các can thiệp thành công bên cạnh các chế độ lỗi, bỏ lỡ cơ hội ghi lại những gì hiệu quả và tại sao.

**Lợi ích khi áp dụng thực hành tốt này:**

- Một hệ thống quản lý tri thức có hệ thống nắm bắt kinh nghiệm vận hành của cá nhân thành học tập của tổ chức, khiến toàn nhóm hiệu quả hơn theo thời gian.
- Tri thức vận hành được tài liệu hóa cho phép các phản ứng nhất quán với các kịch bản phổ biến, giảm sự biến thiên trong cách các thành viên nhóm xử lý các tình huống tương tự.
- Tìm kiếm ngữ nghĩa bộc lộ tri thức liên quan ngay cả khi người dùng không biết tên hay danh mục tài liệu chính xác.
- Các buổi kiểm toán theo quý giữ cho cơ sở tri thức cập nhật khi các hệ thống và quy trình tiến hóa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một kho tri thức tập trung là điểm khởi đầu, nhưng trải nghiệm tìm kiếm mới quyết định liệu có ai dùng nó hay không. [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) cung cấp tìm kiếm ngữ nghĩa trên tài liệu vận hành, để các truy vấn ngôn ngữ tự nhiên trả về các mục liên quan ngay cả khi người dùng không biết tiêu đề chính xác. Hãy cấu trúc cơ sở tri thức với các danh mục cho các mẫu hành vi agent, các chế độ lỗi phổ biến và cách giải quyết, các quy trình vận hành, và các bài học sau sự cố. Sinh có tăng cường truy xuất (retrieval-augmented generation) của Amazon Bedrock biến cơ sở tri thức thành thứ có thể truy vấn bằng ngôn ngữ tự nhiên thay vì khớp từ khóa.

Các buổi rà soát sau sự cố có cấu trúc nắm bắt dòng thời gian, nguyên nhân gốc, các bước giải quyết, và các biện pháp phòng ngừa sẽ biến mỗi sự cố đáng kể thành tri thức bền vững. Hãy gắn các đầu ra rà soát trực tiếp với các mục cơ sở tri thức để một chế độ lỗi mới được tài liệu hóa ngay trong tuần nó được chẩn đoán.

Các buổi kiểm toán theo quý kiểm định độ chính xác và tính đầy đủ. Các hành vi agent thay đổi, các dịch vụ tiến hóa, và các quy trình từng hiệu quả năm ngoái có thể không còn áp dụng. Không có kiểm định định kỳ, cơ sở tri thức chậm rãi trở nên kém đáng tin cậy. Hãy cân nhắc xây dựng một trợ lý vận hành nội bộ dùng [Amazon Bedrock Agents](https://aws.amazon.com/bedrock/agents/) mà các thành viên nhóm có thể truy vấn để nhận hướng dẫn về các kịch bản phổ biến. Điều này đặc biệt có giá trị cho việc đưa vào (onboarding) và cho ứng phó sự cố khi hướng dẫn kịp thời quan trọng hơn việc khám phá tài liệu.

### Các bước triển khai

- **Triển khai một kho tri thức tập trung:** Dùng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) cho tìm kiếm ngữ nghĩa trên tài liệu vận hành.
- **Định nghĩa các danh mục và mẫu:** Bao phủ các mẫu hành vi, các chế độ lỗi, các quy trình, và các bài học sau sự cố với cấu trúc nhất quán.
- **Thiết lập một quy trình rà soát sau sự cố:** Dùng các mẫu có cấu trúc cấp trực tiếp vào cơ sở tri thức để tri thức nắm bắt trong lúc rà soát trở thành tri thức bền vững.
- **Triển khai các luồng đóng góp:** Làm cho việc thêm và cập nhật các mục trở nên đơn giản đối với các thành viên nhóm mà không có gánh nặng quy trình nặng nề.
- **Kiểm toán theo quý:** Rà soát độ chính xác, tính đầy đủ, và độ liên quan, và loại bỏ các mục lỗi thời.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS07-BP03 Bổ sung quản trị thay đổi để đáp ứng các cải tiến kỹ thuật và các yêu cầu kinh doanh](agentops07-bp03.xml)
- [AGENTOPS05-BP03 Triển khai ghi log có cấu trúc và các vết kiểm toán toàn diện](../agentops05/agentops05-bp03.xml)
- [AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục](../agentops02/agentops02-bp04.xml)
- [AGENTCOST07-BP03 Tạo các vòng lặp phản hồi tối ưu có hệ thống cho cải tiến liên tục](../../cost-optimization-pillar/agentcost07/agentcost07-bp03.xml)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)
- [Preparing your business for agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/preparing-business.html)
- [Introducing Amazon Bedrock AgentCore: Securely deploy and operate AI agents at any scale](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon S3](https://aws.amazon.com/s3/)
