# AGENTSUS03-BP04 Loại bỏ các Agent không dùng và ngăn tình trạng bùng nổ Agent (agent sprawl)

Mỗi Agent còn được triển khai sau khi đã hết hữu ích đều tiêu thụ hạ tầng, mở rộng bề mặt tấn công (attack surface) và thêm gánh nặng vận hành mà không bao giờ xuất hiện như một khoản mục chi phí tường minh. Quản lý danh mục chủ động giúp ngăn sự tích lũy âm thầm của chi phí và độ phức tạp đi kèm với việc áp dụng mở rộng quy mô.

**Kết quả mong muốn:**

- Mỗi Agent đã triển khai có một chủ sở hữu được ghi chép, một mục đích kinh doanh rõ ràng và mức sử dụng đo được.
- Các Agent không còn mang lại giá trị được chuyển qua một vòng đời loại bỏ (decommissioning) có cấu trúc và được cho nghỉ hưu.
- Các nhóm tìm trong registry Agent các năng lực hiện có trước khi khởi động việc phát triển Agent mới.
- Sức khỏe danh mục — tổng số Agent, phần trăm có sử dụng tích cực, phần trăm có tài liệu hiện hành — hiển thị ở cấp tổ chức.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các Agent mà không gán quyền sở hữu hay theo dõi mức sử dụng, nên không ai có thể biết Agent nào còn mang lại giá trị.
- Cho phép các Agent bị bỏ rơi tồn tại vô hạn định vì không tồn tại quy trình loại bỏ, tích lũy chi phí hạ tầng và mở rộng bề mặt tấn công.
- Xây các Agent mới cho các năng lực vốn đã tồn tại trong các Agent đã triển khai ở nơi khác trong tổ chức, tạo ra các bản hiện thực dư thừa.
- Dựa vào tri thức phi chính thức về việc Agent nào còn hữu ích thay vì theo dõi mức sử dụng tự động, nên quyết định loại bỏ phụ thuộc vào bất kỳ ai tình cờ nhớ ra Agent nào đang được triển khai.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các quyết định ở cấp danh mục về mức tiêu thụ tài nguyên gắn với giá trị kinh doanh thực sự mang lại, thay vì với các mẫu triển khai trong quá khứ.
- Việc loại bỏ thu hồi tài nguyên hạ tầng và giảm diện tích bề mặt vận hành.
- Khả năng khám phá các năng lực hiện có giảm các bản hiện thực dư thừa và củng cố các mẫu kiến trúc tái sử dụng được.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) cung cấp danh mục có thẩm quyền về các Agent đã triển khai, với mỗi mục nắm bắt mục đích kinh doanh, chủ sở hữu được chỉ định, ngày triển khai, các phụ thuộc và các chỉ số sử dụng. Tìm kiếm năng lực theo ngữ nghĩa (semantic capability search) cho phép các nhóm khám phá các Agent hiện có trước khi xây các Agent mới, đây là mặt phòng ngừa của việc tránh bùng nổ Agent. Ghép registry với các chỉ số [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html) theo dõi tần suất gọi và dấu thời gian lần gọi gần nhất (last-invocation timestamp) cho mỗi Agent. Khi đó các Agent không hoạt động sẽ tự động nổi lên để chủ sở hữu rà soát thay vì bị phát hiện trong các đợt kiểm toán.

Việc loại bỏ trở thành thường lệ khi nó có một vòng đời được xác định. Các giai đoạn hoạt động, đang rà soát, ngừng dùng (deprecated) và đã loại bỏ cho các chủ sở hữu các chuyển tiếp rõ ràng và cho tổ chức khả năng thấy nhất quán được Agent nào đang trên đường nghỉ hưu. Khi một Agent bị gắn cờ vì sử dụng thấp, câu hỏi đầu tiên của chủ sở hữu là liệu nó có phục vụ một mục đích theo mùa hoặc ít-gặp-nhưng-trọng-yếu hay không. Các Agent mùa thuế, các Agent báo cáo hàng quý, và các Agent phục hồi thảm họa trông nhàn rỗi phần lớn thời gian nhưng lại thiết yếu khi chúng được gọi. Một đợt rà soát có cấu trúc tạo ra sự phân biệt đó trước khi việc ngừng dùng xảy ra.

Trong đợt hợp lý hóa danh mục hàng quý, các nhóm đánh giá toàn bộ kho Agent đối chiếu với các ưu tiên kinh doanh hiện tại, nhận diện các năng lực chồng lấn, và hợp nhất các bản hiện thực dư thừa thành các mẫu dùng chung (theo [AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được](../1-agentsus01/agentsus01-bp02.md)). Họ cho nghỉ hưu các Agent mà ngữ cảnh kinh doanh của chúng đã thay đổi. Các chỉ số sức khỏe danh mục được theo dõi qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) — tổng số Agent, phần trăm có sử dụng tích cực, và phần trăm có tài liệu hiện hành — làm cho các kết quả bền vững hiển thị ở cấp tổ chức.

### Các bước triển khai

- **Đăng ký mọi Agent đã triển khai kèm siêu dữ liệu quyền sở hữu:** Ghi mỗi Agent trong [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) với các thông tin sau: Mục đích kinh doanh
- Chủ sở hữu được chỉ định
- Ngày triển khai
- Phụ thuộc
- **Theo dõi các chỉ số gọi và gắn cờ các Agent không hoạt động:** Đo đạc các Agent bằng các chỉ số [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html) nắm bắt tần suất gọi và dấu thời gian lần gọi gần nhất, và gắn cờ các Agent vượt qua một ngưỡng không hoạt động xác định để chủ sở hữu rà soát.
- **Định nghĩa một vòng đời loại bỏ:** Thiết lập các giai đoạn sau với tiêu chí chuyển tiếp và trách nhiệm của chủ sở hữu ở mỗi giai đoạn: Hoạt động
- Đang rà soát
- Ngừng dùng (Deprecated)
- Đã loại bỏ (Decommissioned)
- **Yêu cầu tìm kiếm trong registry trước khi phát triển Agent mới:** Thêm một bước kiểm tra tiền-phát-triển vào quy trình tiếp nhận (intake) để các nhóm khám phá và đánh giá các năng lực hiện có trước khi khởi động công việc mới.
- **Chạy các đợt rà soát danh mục hàng quý:** Đánh giá toàn bộ kho Agent đối chiếu với các ưu tiên kinh doanh hiện tại, hợp nhất các năng lực chồng lấn thành các mẫu dùng chung, và cho nghỉ hưu các Agent mà ngữ cảnh kinh doanh của chúng đã thay đổi.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS01-BP02 Triển khai các mẫu quy trình tái sử dụng được](../1-agentsus01/agentsus01-bp02.md)
- [AGENTSUS03-BP03 Duy trì các đặc tả toàn diện cho Agent và hệ thống dạng tác nhân](agentsus03-bp03.md)
- [AGENTSUS02-BP04 Đo lường và tối ưu hóa dấu chân môi trường của các khối công việc Agent](../2-agentsus02/agentsus02-bp04.md)
- [SUS03-BP02 Remove or refactor workload components with low or no use](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a3.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [The future of managing agents at scale: AWS Agent Registry now in preview](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon CloudWatch metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)

**Các video liên quan:**

- [AgentCore Registry: Discover, Govern, and Reuse AI Agents at Scale](https://www.youtube.com/watch?v=rIcOJrE-fTk)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
