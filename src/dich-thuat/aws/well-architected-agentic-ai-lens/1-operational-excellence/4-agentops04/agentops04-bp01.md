# AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools

Các agent không thể khám phá Tools rốt cuộc sẽ dùng các tích hợp hardcode, tài liệu không nhất quán, và một khoản "thuế bảo trì" tăng theo mỗi năng lực mới. Một registry tập trung khiến catalog Tools trở nên truy vấn được, có phiên bản, và có thể quản trị.

**Kết quả mong muốn:**

- Một registry Tools tập trung cung cấp một nguồn có thẩm quyền duy nhất cho các năng lực Tools, các phiên bản hiện tại, và trạng thái vận hành.
- Tài liệu Tools được chuẩn hóa và đầy đủ để các agent có thể chọn và gọi Tools mà không phải đoán mò.
- Đánh phiên bản Tools và theo dõi tương thích giúp ngăn các agent gọi các phiên bản đã ngừng dùng hoặc không tương thích.
- Các quy trình ngừng dùng Tools gỡ bỏ các Tools đã kết thúc vòng đời một cách gọn gàng mà không làm gián đoạn các agent phụ thuộc.

**Các phản mẫu thường gặp (anti-patterns):**

- Cho phép mỗi nhóm quản lý các định nghĩa Tools độc lập mà không có một registry dùng chung, tạo ra các Tools trùng lặp, tài liệu không nhất quán, và các agent không thể khám phá các Tools do các nhóm khác xây dựng.
- Đăng ký Tools mà không có chuẩn tài liệu, để các agent đoán mò định dạng tham số và mã lỗi qua thử-và-sai.
- Ngừng dùng Tools mà không thông báo cho các agent phụ thuộc, gây ra các lỗi tại runtime khi các agent cố gọi các Tools không còn tồn tại.
- Để registry trôi lệch khỏi thực tế, khiến trạng thái sức khỏe trong registry mâu thuẫn với tình trạng sẵn sàng thực tế của Tools.

**Lợi ích khi áp dụng thực hành tốt này:**

- Một nguồn chân lý duy nhất cho các năng lực và trạng thái Tools nghĩa là mọi agent khám phá và sử dụng Tools nhất quán, và các cập nhật lan truyền tin cậy.
- Tầm nhìn tập trung vào catalog Tools cho phép các nhóm theo dõi tình trạng sẵn sàng, phân bố phiên bản, và các quan hệ phụ thuộc qua danh mục agent.
- Các chuẩn tài liệu giảm lỗi khi gọi bằng cách cung cấp cho các agent thông tin đầy đủ, có cấu trúc về mỗi Tools.
- Các luồng ngừng dùng cho các agent phụ thuộc thời gian để di chuyển trước khi các Tools bị gỡ bỏ, giúp ngăn gián đoạn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Hãy bắt đầu với những gì [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cung cấp trước khi xây dựng tùy chỉnh. AgentCore Gateway bao gồm khám phá Tools theo ngữ nghĩa và các năng lực MCP server, xử lý việc lập catalog, đánh phiên bản, và khám phá mà không cần hạ tầng tùy chỉnh. Đối với nhiều nhóm, điều này bao phủ yêu cầu về registry một cách trọn vẹn. Hãy đánh giá AgentCore Gateway so với luồng khám phá bạn cần, bao gồm tìm kiếm năng lực, theo dõi phiên bản, và metadata phụ thuộc, trước khi đầu tư vào hạ tầng song song.

Một khoảng trống đối với hầu hết các tổ chức là các chuẩn tài liệu, chứ không phải cơ chế registry. Một mục Tools có thể bị gọi sai nếu không có một tuyên bố mục đích, các lược đồ tham số, mã lỗi, giới hạn tốc độ, và các yêu cầu xác thực. Hãy áp đặt tính đầy đủ như một cổng trong quy trình đưa vào (onboarding) thay vì như một gợi ý sau khi đăng ký. Chi phí từ chối một Tools không có tài liệu trong lúc đăng ký thấp hơn chi phí gỡ lỗi việc dùng sai sau khi triển khai.

Đánh phiên bản ngữ nghĩa với các bảo đảm tương thích giúp các agent và Tools tiến hóa ở các tốc độ khác nhau. Một phiên bản Tools mới không nên âm thầm làm hỏng các agent được viết dựa trên phiên bản trước, và một agent mới không nên bị chặn bởi các Tools chưa phơi bày phiên bản mà nó cần. Hãy duy trì nhiều phiên bản đang hoạt động trong các giai đoạn chuyển tiếp, và triển khai các luồng ngừng dùng thông báo cho các agent phụ thuộc trước khi chúng bị ngừng dùng. Các health check cập nhật trạng thái vận hành của Tools để registry được cập nhật với dữ liệu thực tế.

### Các bước triển khai

- **Đánh giá [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) như registry chính:** Dùng khám phá Tools theo ngữ nghĩa và các năng lực MCP server của nó, và chỉ bổ sung hạ tầng tùy chỉnh ở nơi thiếu một năng lực cụ thể.
- **Định nghĩa các chuẩn tài liệu Tools:** Yêu cầu mục đích, các lược đồ tham số, mã lỗi, giới hạn tốc độ, và các yêu cầu xác thực. Áp đặt tính đầy đủ như một cổng trong quy trình đưa Tools vào.
- **Triển khai đánh phiên bản ngữ nghĩa:** Dùng các bảo đảm tương thích và duy trì nhiều phiên bản đang hoạt động trong các giai đoạn chuyển tiếp để các agent và Tools có thể tiến hóa độc lập.
- **Cấu hình các health check và luồng ngừng dùng:** Cập nhật trạng thái vận hành tự động và thông báo cho các agent phụ thuộc trước các ngày kết thúc vòng đời.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS04-BP02 Thiết lập các giao thức tích hợp Tools chuẩn hóa (MCP, A2A)](agentops04-bp02.md)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](agentops04-bp03.md)
- [AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent](../1-agentops01/agentops01-bp01.md)
- [AGENTSEC02-BP03 Duy trì registry Tools được phê duyệt với các đánh giá bảo mật](../../2-security/2-agentsec02/agentsec02-bp03.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Các framework, nền tảng, giao thức và công cụ agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)
- [AI agent trong doanh nghiệp: Thực hành tốt với Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)
- [Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)

**Video liên quan:**

- [AWS re:Invent 2024 - Scale agent tools with AgentCore Gateway (AIM3313)](https://www.youtube.com/watch?v=DlIHB8i6uyE)
- [AWS re:Invent 2024 - Build agentic workflows with third-party agents and tools (AIM3311)](https://www.youtube.com/watch?v=kfgt1uJE-E4)
- [AWS re:Invent 2024 - Modernize containers for AI agents using AgentCore Gateway (CNS422)](https://www.youtube.com/watch?v=6autfsn1fy8)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
