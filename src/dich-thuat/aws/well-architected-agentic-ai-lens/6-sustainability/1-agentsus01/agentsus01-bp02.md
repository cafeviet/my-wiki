# AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được

Khi mỗi nhóm xây lại quy trình truy xuất, xác thực và biến đổi dữ liệu từ đầu, mỗi lần xây lại tốn thời gian phát triển và phải trả cho chu kỳ tối ưu hóa riêng của nó. Một thư viện các mẫu có tham số hóa chuyển chi phí đó thành một khoản đầu tư một lần và giúp các dự án tiếp theo ghép nối từ các khối dựng đã được kiểm thử thay vì bắt đầu lại từ đầu.

**Kết quả mong muốn:**

- Bạn có một danh mục các mẫu quy trình có tham số hóa cho các tác vụ Agent lặp lại (truy xuất, xác thực, biến đổi và ra quyết định) mà các nhóm có thể khám phá và khởi tạo.
- Các nhóm ghép nối các hệ thống Agent mới từ các mẫu hiện có trước khi viết bản hiện thực mới.
- Mỗi mẫu có một giao diện được ghi chép, lịch sử phiên bản và hồ sơ tài nguyên đã khai báo, và một mẫu đơn lẻ phục vụ nhiều bên gọi qua một lớp Tools dùng chung.
- Bạn giám sát tần suất gọi mẫu và tỷ lệ thất bại để các tối ưu hóa cho một mẫu lan tỏa đến mọi bên gọi.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây các quy trình dùng một lần cho mỗi dự án mới mà không tính đến tái sử dụng, nhân bản công sức qua các nhóm và tích lũy nợ kỹ thuật khi các năng lực tương tự bị hiện thực lại với các biến thể nhỏ.
- Mã hóa cứng (hardcode) logic quy trình và các điểm quyết định vào từng bản hiện thực riêng lẻ thay vì tham số hóa chúng, khiến việc tái sử dụng các mẫu đã kiểm chứng trở nên bất khả thi.
- Phát triển các thành phần tái sử dụng được mà không có danh mục trung tâm hay tài liệu, nên các nhóm xây lại các quy trình vốn đã tồn tại ở nơi khác trong tổ chức.
- Coi các quy trình như mã dùng-rồi-bỏ thay vì các tài sản được duy trì, bỏ qua khâu kiểm thử, ghi chép và quản lý phiên bản vốn giữ cho các mẫu còn dùng được sau lần triển khai đầu tiên.

**Lợi ích khi áp dụng thực hành tốt này:**

- Mỗi dự án Agent mới bắt đầu từ các khối dựng đã kiểm chứng, đã kiểm thử thay vì xây lại từ đầu, giảm các chu kỳ phát triển và kiểm thử dư thừa vốn chiếm phần lớn giai đoạn đầu áp dụng.
- Hành vi giữ nhất quán qua các nhóm vì mọi bên gọi một mẫu đều nhận cùng một bản hiện thực đã được xác thực.
- Một tối ưu hóa đơn lẻ cho một mẫu dùng chung cải thiện mọi bên gọi cùng lúc, phân bổ công việc tinh chỉnh trong tương lai ra toàn đội hình.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một mẫu chỉ trở nên tái sử dụng được khi các tham số, đầu vào, đầu ra và chế độ thất bại của nó là tường minh. Các quy trình lặp lại trong hệ thống Agent — một chuỗi truy xuất với việc chọn nguồn, một pipeline xác thực với kiểm tra lược đồ (schema), và một giai đoạn biến đổi với chuyển đổi định dạng — trông giống nhau qua các dự án vì hình dạng công việc là như nhau. Phần biến thiên rất hẹp: là nguồn nào, lược đồ nào và định dạng nào. Đưa các tham số đó thành một phần của giao diện, thay vì mã hóa cứng chúng vào từng bản hiện thực, cho phép một bản hiện thực phục vụ nhiều bên gọi.

Việc khám phá phải hoạt động ở hai thời điểm khác nhau. Ở thời điểm thiết kế, một nhóm đang cân nhắc có nên xây cái gì mới không cần biết cái gì đã tồn tại. Đó là bài toán kho tài liệu. Ở thời điểm chạy, một Agent điều phối cần phân giải một năng lực thành một endpoint cụ thể. Đó là bài toán registry. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) lộ các mẫu dưới dạng Tools MCP với giao diện được định nghĩa rõ ràng, nên việc khám phá ở thời điểm chạy đã được tích hợp sẵn. Danh mục ở thời điểm thiết kế (một trang wiki, một service catalog, hoặc một README) phải được duy trì song song với registry để các nhóm có thể duyệt qua năng lực, hạn chế và yêu cầu tài nguyên trước khi viết mã.

Kiểm soát truy cập và quản lý phiên bản giữ cho các mẫu dùng chung không bị mỗi nhóm âm thầm fork riêng. Áp [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) và các chính sách Gateway để việc sử dụng mẫu có một dấu chân đã biết. Giữ các phiên bản mẫu tường minh để bên tiêu dùng áp dụng một phiên bản mới một cách chủ ý. Triển khai các bản hiện thực nền tảng trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) để mỗi mẫu có cùng nền tảng vận hành như nhau.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) lộ tần suất gọi, thời lượng thực thi và tỷ lệ thất bại cho mỗi mẫu trong Amazon CloudWatch, nên các chủ sở hữu có thể biết mẫu nào được dùng nhiều (và do đó đáng đầu tư) và mẫu nào đang nằm không dùng (và có lẽ là trừu tượng hóa sai hoặc không thể khám phá được).

### Các bước triển khai

- **Nhận diện và trích xuất các mẫu lặp lại:** Rà soát các quy trình Agent hiện có để tìm các chuỗi lặp lại và tách mỗi chuỗi thành một template có tham số hóa với giao diện được ghi chép. Các chuỗi phổ biến gồm: Truy xuất
- Xác thực
- Biến đổi
- Quyết định
- **Triển khai các mẫu dưới dạng thành phần tái sử dụng được:** Hiện thực mỗi mẫu trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) và công bố qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) dưới dạng một Tool MCP để các Agent điều phối có thể khám phá và gọi nó ở thời điểm chạy.
- **Duy trì một danh mục ở thời điểm thiết kế:** Giữ một kho tài liệu song song với registry Gateway nơi các nhóm có thể duyệt qua những thông tin sau trước khi viết mã mới: Mục đích của mẫu
- Tham số
- Hồ sơ tài nguyên
- Ví dụ sử dụng
- **Quản trị truy cập và phiên bản mẫu:** Áp [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) và các chính sách Gateway để kiểm soát ai được gọi mỗi mẫu, và công bố các phiên bản mới song song với phiên bản cũ để bên tiêu dùng di trú một cách chủ ý.
- **Giám sát mức sử dụng và đưa cải tiến quay lại:** Theo dõi các thông tin sau cho mỗi mẫu qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html): Tần suất gọi
- Thời lượng
- Tỷ lệ thất bại

Dùng telemetry để tìm các mẫu được dùng nhiều đáng đầu tư và các mẫu trì trệ đáng loại bỏ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh](agentsus01-bp01.md)
- [AGENTSUS01-BP03 Tối ưu hóa việc sử dụng tài nguyên thông qua dịch vụ dùng chung](agentsus01-bp03.md)
- [SUS03-BP01 Optimize software and architecture for asynchronous and scheduled jobs](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a2.html)
- [OPS11-BP03 Iterate to improve](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_iterate_to_improve.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [AWS Step Functions - State machine templates](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-templates.html)
- [Strands Agents](https://strandsagents.com/)
- [Guidance for Multi-Agent Orchestration on AWS](https://aws.amazon.com/solutions/guidance/multi-agent-orchestration-on-aws/)

**Các video liên quan:**

- [AWS 2025 - Building AI Agents with Serverless, Strands, and MCP (NTA405)](https://www.youtube.com/watch?v=LwubRSoJcIM)

**Các ví dụ liên quan:**

- [GitHub: aws-samples/aws-stepfunctions-examples](https://github.com/aws-samples/aws-stepfunctions-examples)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
