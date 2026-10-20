# AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng

Một danh mục agent không có kỷ luật vòng đời sẽ trở thành một nghĩa địa các dịch vụ không được tài liệu hóa với những chủ sở hữu bị lãng quên. Các giai đoạn vòng đời rõ ràng, quyền sở hữu SME được nêu tên, và ngừng vận hành gọn gàng giữ cho danh mục dễ quản lý khi nó tăng từ một số ít agent lên hàng chục hoặc hàng trăm.

**Kết quả mong muốn:**

- Mỗi agent có một trạng thái vòng đời được tài liệu hóa (phát triển, thí điểm, sản xuất, ngừng dùng (deprecated), và đã ngừng vận hành (decommissioned)) với các tiêu chí chuyển tiếp được xác định.
- Việc đưa vào (onboarding) tuân theo một quy trình cấp phát (provisioning) chuẩn hóa, cấu hình các tài nguyên, quyền, và giám sát cần thiết trước khi một agent xử lý lưu lượng sản xuất.
- Việc ngừng vận hành gỡ bỏ gọn gàng các agent đã nghỉ, không để lại tài nguyên mồ côi, quyền lơ lửng, hay phụ thuộc không được tài liệu hóa.
- Mỗi agent có một chủ sở hữu SME được nêu tên, chịu trách nhiệm về hành vi, hiệu năng, và việc nghỉ cuối cùng của nó.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai agent vào sản xuất mà không có trạng thái vòng đời được xác định hay chủ sở hữu được chỉ định, khiến không ai chịu trách nhiệm khi hành vi cần được chú ý.
- Vận hành mà không có quy trình ngừng vận hành, để các agent đã nghỉ vẫn chạy với quyền đang hoạt động và tiêu thụ tài nguyên lâu sau khi chúng đã được thay thế.
- Bỏ qua giai đoạn thí điểm và đẩy agent từ phát triển thẳng vào sản xuất đầy đủ, bỏ lỡ cơ hội kiểm định hành vi dưới lưu lượng thực với giám sát tăng cường.
- Xem agent registry như một tài liệu một lần mà không ai cập nhật một khi agent đã hoạt động.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các quy trình vòng đời chuẩn hóa tạo ra sự cấp phát, vận hành, và nghỉ nhất quán, giảm độ phức tạp vận hành khi danh mục tăng trưởng.
- Các trạng thái vòng đời và tiêu chí chuyển tiếp được tài liệu hóa tạo ra một hồ sơ có thể kiểm toán về lịch sử của mỗi agent phục vụ tuân thủ và quản trị.
- Các chủ sở hữu được nêu tên đẩy nhanh ứng phó sự cố. Khi một agent hành xử sai, nhóm biết cần liên hệ ai mà không phải tìm kiếm.
- Ngừng vận hành gọn gàng giúp ngăn sự tích tụ chậm của các tài nguyên bị bỏ hoang, vốn trở thành một vấn đề chi phí và bảo mật theo thời gian.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Năm giai đoạn bao phủ cung vận hành của gần như bất kỳ agent nào:

- Phát triển (đang phát triển tích cực, không phục vụ lưu lượng sản xuất)
- Thí điểm (sử dụng sản xuất giới hạn với giám sát tăng cường và kiểm định chi phí)
- Sản xuất (triển khai đầy đủ với các quy trình vận hành chuẩn)
- Ngừng dùng (deprecated) (đã lên lịch ngừng vận hành, không tích hợp mới)
- Đã ngừng vận hành (decommissioned) (đã gỡ khỏi dịch vụ, tài nguyên được dọn dẹp)

Mỗi lần chuyển tiếp nên mang các tiêu chí rõ ràng, các phê duyệt bắt buộc, các cổng kiểm định, và yêu cầu tài liệu, để các thay đổi giai đoạn là quyết định thay vì trôi lệch.

Thí điểm kiểm định tính khả thi về kinh tế và xác định các vấn đề trước khi triển khai đầy đủ, giảm chi phí giải quyết vấn đề. Đối với các nhóm dùng phát triển hướng đặc tả (spec-driven development) với các công cụ như Kiro, luồng công việc spec tạo ra tài liệu cần thiết cho quản trị vòng đời như một sản phẩm phụ. Đây là một tác dụng phụ hữu ích đáng dùng thay vì xây dựng lại.

Một agent registry là một tài liệu bền vững giúp quy trình này mạch lạc. Nó nên theo dõi ID agent, trạng thái vòng đời, chủ sở hữu, phụ thuộc, năng lực, và metadata vận hành. Không có registry, trạng thái vòng đời chỉ tồn tại trong đầu người ta, khiến việc theo dõi và quản lý nhất quán xuyên tổ chức trở nên khó khăn. Registry trở thành đầu vào cho các buổi rà soát danh mục, phân tích phụ thuộc khi ngừng vận hành, và ứng phó khẩn cấp.

Các chuyển tiếp vòng đời khẩn cấp xứng đáng có các quy trình riêng. Các cơ chế công tắc chấm dứt khẩn cấp (emergency termination switch) tự động cho phép thu hồi ngay quyền của một agent và dừng các hoạt động, cho phép ứng phó nhanh với các vấn đề vận hành. Runbook ngừng vận hành làm công việc tương tự cho trường hợp có kế hoạch. Nó gỡ tài nguyên, thu hồi quyền, cập nhật registry, và thông báo cho các hệ thống phụ thuộc như các bước tự động thay vì các mục checklist. Đối với các agent được xây qua các nền tảng không cần mã như [Amazon Quick Suite](https://aws.amazon.com/quicksuite/), cùng các quy tắc vòng đời được áp dụng. Registry theo dõi chúng, các buổi rà soát danh mục xem xét chúng, và ngừng vận hành dọn dẹp chúng.

### Các bước triển khai

- **Tài liệu hóa năm giai đoạn vòng đời:** Quy định các tiêu chí chuyển tiếp, các vai trò phê duyệt bắt buộc, và các cổng kiểm định cho mỗi giai đoạn.
- **Xây dựng agent registry:** Theo dõi ID agent, trạng thái vòng đời, chủ sở hữu, phụ thuộc, năng lực, và metadata vận hành trong một kho bền vững.
- **Tự động hóa các chuyển tiếp trạng thái vòng đời:** Kiểm định các tiêu chí, kích hoạt các hành động đặc thù giai đoạn, và ghi lại các chuyển tiếp với quy kết, các triển khai, các thay đổi quyền, thiết lập giám sát, và các bước ngừng vận hành.
- **Tạo các mẫu cấp phát chuẩn hóa:** Cấu hình các tài nguyên, quyền, và giám sát cần thiết một cách tự động để các agent mới vào sản xuất với một baseline nhất quán.
- **Triển khai công tắc chấm dứt khẩn cấp và các runbook ngừng vận hành:** Bao gồm phân tích phụ thuộc trước khi chạy để việc ngừng vận hành không làm hỏng các bên tiêu thụ thượng nguồn.
- **Thiết lập các buổi rà soát danh mục theo quý:** Xác định các agent cần ngừng dùng hoặc ngừng vận hành, bao gồm cả các agent được xây với các nền tảng không cần mã như [Amazon Quick](https://aws.amazon.com/quicksuite/).

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent](../1-agentops01/agentops01-bp01.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](agentops03-bp02.md)
- [AGENTOPS03-BP03 Triển khai các chính sách scaling đặc thù agent và lập kế hoạch dung lượng](agentops03-bp03.md)
- [AGENTOPS02-BP02 Triển khai phát hiện và khắc phục trôi lệch cấu hình](../2-agentops02/agentops02-bp02.md)
- [AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tài liệu hiệu quả](../../5-cost-optimization/6-agentcost06/agentcost06-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Focus area 5: Manage the lifecycle](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/focus-areas-lifecycle.html)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)
- [Chuẩn bị doanh nghiệp cho agentic AI ở quy mô lớn](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/preparing-business.html)
- [Kiro Specs](https://kiro.dev/docs/specs/)
- [Operationalizing Agentic AI Part 1: A Stakeholder's Guide](https://aws.amazon.com/blogs/machine-learning/operationalizing-agentic-ai-part-1-a-stakeholders-guide/)

**Video liên quan:**

- [AWS re:Invent 2024 - Agents in the enterprise: Best practices with AgentCore (AIM3310)](https://www.youtube.com/watch?v=w5XJxCpUADY)
- [AWS re:Invent 2024 - Cox Automotive's Blueprint for Agentic AI on AgentCore (IND3329)](https://www.youtube.com/watch?v=ICA8-d_Nt9Q)
- [AWS re:Invent 2024 - Bridging from POC to production: Intro to AgentCore (AIM2204)](https://www.youtube.com/watch?v=oDjESsByBmM)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore](https://catalog.workshops.aws/agentcore-getting-started/en-US)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
