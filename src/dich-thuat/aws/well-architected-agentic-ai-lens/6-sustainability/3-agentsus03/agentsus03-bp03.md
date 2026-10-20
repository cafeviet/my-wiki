# AGENTSUS03-BP03 Duy trì các đặc tả toàn diện cho Agent và hệ thống dạng tác nhân

Các Agent không có đặc tả (specification) trở thành các hệ thống mà chỉ các nhà phát triển ban đầu của chúng hiểu. Tài liệu kỹ lưỡng — mục đích, ranh giới, điểm tích hợp và logic quyết định — giữ cho tri thức tổ chức luôn sẵn có cho toàn nhóm và xác nhận rằng hành vi của Agent có thể truy vết khi các nhóm và quy trình kinh doanh thay đổi.

**Kết quả mong muốn:**

- Mỗi Agent đã triển khai có một đặc tả bao trùm mục đích kinh doanh, ranh giới vận hành, tiêu chí quyết định và các đường chuyển lên cấp cao.
- Các đặc tả được lưu trong các tạo tác được quản lý phiên bản (version-controlled) song song với bản hiện thực Agent.
- Một danh mục Agent tập trung cho phép các thành viên nhóm khám phá, rà soát và tái sử dụng các năng lực của Agent.
- Hành vi ở thời điểm chạy được ghi chép tự động và so sánh với các đặc tả thiết kế để phát hiện sự trôi dạt (drift).
- Quản trị yêu cầu xác thực đặc tả trước khi các Agent đến production.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các Agent mà không có tài liệu kỹ lưỡng về mục đích, ranh giới hay logic ra quyết định, nên tri thức tổ chức chỉ nằm ở các nhà phát triển ban đầu.
- Để tài liệu lỗi thời khi các Agent tiến hóa, tạo ra các đặc tả mô tả hành vi của ngày hôm qua thay vì của hôm nay.
- Coi cấu hình Agent chỉ là mã, mà không nắm bắt các mẫu ra quyết định của chuyên gia và lý do đằng sau logic kinh doanh vốn đã định hình thiết kế.
- Bỏ qua việc xác thực đặc tả trong đường thăng cấp, nên các Agent đến production với tài liệu không khớp với hành vi thực tế của chúng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tri thức tổ chức tồn tại qua các thay đổi nhân sự và tái cấu trúc tổ chức, được bảo tồn trong tài liệu thay vì trong trí nhớ.
- Các nhóm phát triển dựa trên các đặc tả được thông tin bởi quy trình kinh doanh, giảm chi phí thử nghiệm của mỗi Agent mới.
- Logic quyết định và ranh giới vận hành được ghi chép làm cho việc giám sát các quy trình được tự động hóa trở nên khả thi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Một đặc tả tách rời hành vi của Agent khỏi tác giả của nó. Khi nhà phát triển ban đầu rời đi, người bảo trì kế tiếp tiếp quản hệ thống qua đặc tả thay vì qua việc dịch ngược (reverse engineering). Amazon Bedrock AgentCore cho phép các đặc tả khai báo nắm bắt các template prompt, định nghĩa Tools, chính sách guardrail và logic điều phối như các tạo tác được quản lý phiên bản. Tài liệu và cấu hình là cùng một tạo tác thay vì hai bản sao trôi dạt khỏi nhau.

Các công cụ phát triển theo hướng đặc tả (specification-driven) như Kiro mở rộng kỷ luật này vào cách các Agent được viết ngay từ đầu. Khi các đặc tả là điểm khởi đầu thay vì một chuyện phụ, tài liệu được tạo ra như một sản phẩm phụ của quá trình phát triển thay vì một tác vụ hồi cứu. Khoản đầu tư trả trước cho việc viết đặc tả được thu hồi trong quá trình review mã, kiểm thử và tiến hóa liên tục, vì mọi thay đổi tiếp theo đều diễn ra dựa trên một đường cơ sở rõ ràng.

Việc khám phá cần một mái nhà trung tâm, như một danh mục dựa trên các năng lực registry của [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) vốn làm cho các Agent có thể khám phá, quản trị và tái sử dụng trên toàn tổ chức. Mỗi mục nắm bắt mục đích kinh doanh, lịch sử phiên bản, các phụ thuộc và các đặc điểm vận hành, để một nhóm đang cân nhắc có nên xây cái gì mới không có thể kiểm tra cái gì đã tồn tại.

Các đặc tả có thể trôi dạt nếu một tổ chức thiếu các cơ chế xác thực. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) sinh tài liệu ở thời điểm chạy từ các mẫu thực thi thực tế. Khi hành vi ở thời điểm chạy phân kỳ khỏi các đặc tả thiết kế, telemetry cho thấy điều đó trước khi sự phân kỳ trở thành tri thức tổ chức không được ghi chép.

Với các hệ thống đa Agent, hãy ghi chép các giao thức phối hợp và các mẫu ủy quyền một cách tường minh, vì hành vi trồi lên (emergent) của một hệ thống đa Agent hiếm khi hiển nhiên từ đặc tả của bất kỳ Agent riêng lẻ nào. Giám sát ở cấp danh mục — sự tuân thủ đặc tả, độ hiện hành của tài liệu và sự trôi dạt hành vi — giữ cho tài liệu còn dùng được khi số lượng Agent mở rộng.

### Các bước triển khai

- **Thiết lập các chuẩn tài liệu:** Yêu cầu mỗi Agent mang theo các đặc tả sử dụng các tạo tác cấu hình khai báo của AgentCore. Mỗi đặc tả phải bao trùm: Mục đích kinh doanh
- Ranh giới vận hành
- Tiêu chí quyết định
- Các đường chuyển lên cấp cao
- **Áp dụng phát triển theo hướng đặc tả:** Dùng Kiro hoặc các công cụ specification-driven tương tự để tài liệu được tạo ra như một sản phẩm phụ tự nhiên của quá trình phát triển thay vì một tác vụ hồi cứu.
- **Đăng ký các Agent trong một danh mục trung tâm:** Ghi mỗi Agent trong [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) với siêu dữ liệu sau: Mục đích
- Lịch sử phiên bản
- Phụ thuộc
- Các đặc điểm vận hành
- **Sinh tài liệu ở thời điểm chạy:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để tạo tài liệu ở thời điểm chạy có thể so sánh với các đặc tả thiết kế nhằm phát hiện sự trôi dạt.
- **Chặn cửa việc thăng cấp bằng xác thực đặc tả:** Yêu cầu xác thực tài liệu như một phần của pipeline thăng cấp Agent lên production, để các Agent production luôn có các đặc tả hiện hành.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS03-BP01 Duy trì các kỹ năng và năng lực tổ chức](agentsus03-bp01.md)
- [AGENTSUS03-BP04 Loại bỏ các Agent không dùng và ngăn tình trạng bùng nổ Agent (agent sprawl)](agentsus03-bp04.md)
- [OPS11-BP01 Have a process for continuous improvement](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_process_cont_imp.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [The future of managing agents at scale: AWS Agent Registry now in preview](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

**Các ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - End-to-end use cases](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
