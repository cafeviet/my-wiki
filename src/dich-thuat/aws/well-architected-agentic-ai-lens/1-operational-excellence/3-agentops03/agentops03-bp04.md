# AGENTOPS03-BP04 Triển khai quản lý và quản trị danh mục agent ở cấp tổ chức theo quy mô

Một số ít agent do một nhóm xây dựng là một dự án. Hàng chục agent do nhiều nhóm xây dựng là một danh mục (portfolio), và các danh mục cần các cơ chế vận hành khác nhau. Không có tầm nhìn liên tổ chức, các nhóm xây dựng các agent trùng lặp, phá vỡ các tích hợp của nhau, và mất dấu những agent nào vẫn còn xứng đáng tồn tại.

**Kết quả mong muốn:**

- Một catalog tập trung mang lại cho tổ chức một góc nhìn hiện tại về mọi agent, chủ sở hữu, năng lực, phụ thuộc, trạng thái vòng đời, hồ sơ chi phí, và giá trị kinh doanh.
- Các nhóm khám phá các agent hiện có trước khi xây dựng agent mới, để nỗ lực dồn vào các khoảng trống năng lực thay vì các bản trùng lặp.
- Các phụ thuộc liên nhóm được theo dõi và quản lý thông qua các quy trình ngừng dùng được phối hợp.
- Các buổi rà soát danh mục theo quý bộc lộ các agent ít được dùng để hợp nhất hoặc ngừng vận hành, giữ cho danh mục phù hợp với các ưu tiên kinh doanh.

**Các phản mẫu thường gặp (anti-patterns):**

- Cho phép các nhóm xây dựng agent độc lập mà không kiểm tra các năng lực hiện có, tạo ra các agent trùng lặp làm nhân đôi chi phí phát triển, chi phí hạ tầng, và gánh nặng vận hành.
- Chỉ duy trì các agent registry trong từng nhóm riêng lẻ, khiến không ai có góc nhìn liên tổ chức cần thiết để nhận diện sự trùng lặp hay đánh giá sức khỏe hệ thống tổng thể.
- Ngừng dùng hoặc sửa đổi các agent mà không thông báo cho các nhóm phụ thuộc, gây ra các lỗi lan truyền khi các orchestrator hoặc các agent ủy thác gọi các agent đã thay đổi.
- Xem việc tạo agent như một hoạt động không cần lý do biện minh, khiến danh mục tăng trưởng nhanh hơn khả năng của tổ chức trong việc vận hành, giám sát, và bảo trì nó.
- Không đo lường giá trị kinh doanh tương đối với chi phí vận hành, làm giảm rủi ro của các quyết định dựa trên dữ liệu về việc agent nào xứng đáng được tiếp tục đầu tư.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản trị danh mục mở rộng các thực hành vận hành từ các agent riêng lẻ tới các môi trường doanh nghiệp, để chi phí quản trị tăng dưới tuyến tính (sub-linearly) theo số lượng agent.
- Một catalog tập trung với quyền sở hữu, theo dõi phụ thuộc, và trạng thái vòng đời cung cấp hồ sơ có thể kiểm toán cần thiết cho tuân thủ và trách nhiệm tổ chức.
- Tìm kiếm năng lực trước khi xây dựng giảm phát triển trùng lặp, giải phóng nỗ lực kỹ thuật cho các khoảng trống năng lực.
- Các buổi rà soát theo quý giúp ngăn sự phình to bằng cách bộc lộ các ứng viên cho hợp nhất và ngừng vận hành trước khi danh mục trở nên không thể quản lý.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Quản trị danh mục mở rộng registry ở cấp nhóm thành một catalog tổ chức trải rộng qua các ranh giới nhóm (để biết thêm chi tiết, xem [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](agentops03-bp01.md)). Các trường được bổ sung ở tầng này là những trường hỗ trợ các quyết định liên nhóm:

- Nhóm sở hữu
- Lĩnh vực kinh doanh (business domain)
- Các phụ thuộc thượng nguồn (các agent hoặc hệ thống gọi agent này)
- Các phụ thuộc hạ nguồn (các agent, Tools, hoặc dịch vụ mà agent này gọi)
- Chi phí mỗi tháng (suy ra từ CloudWatch và Cost Explorer)
- Các chỉ dấu giá trị kinh doanh (khối lượng hoàn thành tác vụ, các chỉ số kết quả kinh doanh).

[AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) cung cấp catalog tập trung với các luồng phê duyệt tích hợp, metadata linh hoạt, và tìm kiếm lai (semantic và keyword) để các truy vấn liên tổ chức chạy hiệu quả. Hãy làm giàu các bản ghi registry với metadata phụ thuộc, quy kết chi phí, và các chỉ dấu giá trị kinh doanh để catalog hỗ trợ các quyết định ở cấp danh mục vượt ra ngoài việc khám phá đơn thuần.

Cổng rà soát trước khi tạo giúp ngăn các bản dựng trùng lặp. Các nhóm tìm kiếm các agent cụ thể theo mục đích sẽ không tìm thấy một agent qua việc khớp từ khóa với tên agent. [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) cung cấp tìm kiếm lai tích hợp kết hợp hiểu biết ngữ nghĩa với khớp từ khóa, để các truy vấn năng lực bằng ngôn ngữ tự nhiên bộc lộ các agent hiện có với năng lực chồng lấn. Khi có chồng lấn, nhóm yêu cầu tài liệu hóa lý do tại sao agent hiện có không đủ trước khi tiếp tục.

Điều này áp dụng cho cả các agent dựa trên mã (Strands Agents, LangGraph) và các agent không cần mã được xây qua [Amazon Quick Suite](https://aws.amazon.com/quicksuite/). Một cổng CI/CD nhẹ kiểm tra registry và gắn cờ các bản trùng lặp tiềm năng là đủ cho hầu hết các tổ chức, trong khi các quy trình phê duyệt nặng nề khuyến khích việc lách qua.

Hãy triển khai theo dõi phụ thuộc liên nhóm như một thực hành được quản lý. Các agent khai báo các phụ thuộc thượng nguồn và hạ nguồn của chúng tại thời điểm đăng ký và cập nhật khai báo khi phụ thuộc thay đổi. [Amazon EventBridge](https://aws.amazon.com/eventbridge/) công bố các sự kiện khi các agent bị ngừng dùng, sửa đổi, hoặc ngừng vận hành để các nhóm hạ nguồn nhận được thông báo trước. Các agent được phơi bày qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) hưởng lợi từ metadata đăng ký Tools của Gateway, vốn tự động theo dõi agent nào tiêu thụ Tools nào và giảm gánh nặng khai báo thủ công. Một đồ thị phụ thuộc trong [Amazon Neptune](https://aws.amazon.com/neptune/) cho phép phân tích tác động để xác định một thay đổi ở một agent sẽ ảnh hưởng tới các agent khác như thế nào.

Các buổi rà soát danh mục theo quý giúp ngăn trôi lệch dần. Buổi rà soát đánh giá bốn chiều:

- Mức sử dụng (agent nào đang được dùng tích cực và agent nào nhàn rỗi)
- Hiệu quả chi phí (agent nào mang lại giá trị kinh doanh tương xứng với chi phí)
- Sự trùng lặp (agent nào chồng lấn với các agent khác)
- Sức khỏe (agent nào cho thấy tỷ lệ lỗi cao, hiệu năng suy giảm, hoặc cấu hình lỗi thời)

Catalog là nguồn dữ liệu chính, được làm giàu bằng các chỉ số [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/), quy kết [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/), và đồ thị phụ thuộc. Các buổi rà soát tạo ra các khuyến nghị cụ thể. Chúng bao gồm các agent cần hợp nhất, ngừng dùng, hoặc đầu tư, và các rủi ro phụ thuộc liên nhóm cần giải quyết.

### Các bước triển khai

- **Mở rộng agent registry thành một catalog tổ chức:** Dùng [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) để lập catalog các agent với metadata về nhóm sở hữu, lĩnh vực kinh doanh, các phụ thuộc thượng nguồn và hạ nguồn, chi phí mỗi tháng, và các chỉ dấu giá trị kinh doanh.
- **Bật tìm kiếm năng lực theo ngữ nghĩa:** Dùng tìm kiếm lai tích hợp của Agent Registry để các truy vấn ngôn ngữ tự nhiên bộc lộ các năng lực chồng lấn trước khi bắt đầu phát triển mới.
- **Đặt cổng cho việc tạo agent mới trên tìm kiếm registry:** Thêm một kiểm tra CI/CD trước khi tạo, yêu cầu lý do biện minh khi tồn tại các agent chồng lấn.
- **Theo dõi các phụ thuộc liên nhóm:** Dùng [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) để thông báo cho các nhóm hạ nguồn khi các agent thượng nguồn bị ngừng dùng, sửa đổi, hoặc ngừng vận hành.
- **Xây dựng một đồ thị phụ thuộc:** Dùng [Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) để trả lời các câu hỏi phân tích tác động trước khi sửa đổi agent.
- **Chạy các buổi rà soát danh mục theo quý:** Đánh giá mức sử dụng, hiệu quả chi phí, sự trùng lặp, và sức khỏe, tạo ra các khuyến nghị cụ thể cho hợp nhất, ngừng dùng, và đầu tư.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](agentops03-bp01.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](agentops03-bp02.md)
- [AGENTOPS04-BP01 Triển khai quản lý sổ đăng ký và catalog Tools](../4-agentops04/agentops04-bp01.md)
- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent](../5-agentops05/agentops05-bp04.md)
- [AGENTCOST06-BP01 Triển khai khám phá và registry nhẹ cho cộng tác tiết kiệm chi phí](../../5-cost-optimization/6-agentcost06/agentcost06-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Chuẩn bị doanh nghiệp cho agentic AI ở quy mô lớn](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/preparing-business.html)
- [AI agent trong doanh nghiệp: Thực hành tốt với Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)

**Video liên quan:**

- [AWS re:Invent 2024 - Agents in the enterprise: Best practices with AgentCore (AIM3310)](https://www.youtube.com/watch?v=w5XJxCpUADY)
- [AWS 2025 - AgentCore Registry: Discover, Govern, and Reuse AI Agents at Scale](https://www.youtube.com/watch?v=rIcOJrE-fTk)
- [AWS re:Invent 2024 - Cox Automotive's Blueprint for Agentic AI on AgentCore (IND3329)](https://www.youtube.com/watch?v=ICA8-d_Nt9Q)

**Dịch vụ liên quan:**

- [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [Amazon Neptune](https://aws.amazon.com/neptune/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
