# AGENTSUS03-BP02 Xây dựng các Agent phản chiếu các kỹ năng và năng lực tổ chức của bạn

Các Agent được xây để mã hóa các quy trình đã kiểm chứng sẽ mang lại giá trị tức thời. Các Agent được xây để tự động hóa các quy trình mà chính tổ chức chưa thành thạo thường lãng phí tài nguyên để học điều lẽ ra đã có thể được ghi chép trước. Tập trung tự động hóa vào công việc được hiểu rõ là ranh giới giữa việc áp dụng Agent hoàn vốn nhanh và việc áp dụng tiêu tốn tài nguyên vào phương pháp chưa được kiểm chứng.

**Kết quả mong muốn:**

- Bạn chọn các quy trình để tự động hóa nơi các bước, tiêu chí quyết định và chỉ số thành công được ghi chép và được thực thi nhất quán bởi các chuyên gia con người.
- Các Agent phản chiếu các cây quyết định, các điểm kiểm tra xác thực và các đường chuyển lên cấp cao mà các chuyên gia đã dùng.
- Tri thức tổ chức được nắm bắt trong các knowledge base làm nền tảng cho các quyết định của Agent, thay vì chỉ dựa vào dữ liệu huấn luyện của Model nền.
- Các tiêu chí sẵn sàng (readiness criteria) — độ trưởng thành tài liệu tối thiểu — chặn cửa (gate) các dự án phát triển Agent trước khi tài nguyên được cam kết.

**Các phản mẫu thường gặp (anti-patterns):**

- Xây các Agent để tự động hóa các quy trình chưa quen thuộc hoặc hiểu chưa thấu nơi các bước, tiêu chí quyết định và chỉ số thành công chưa được ghi chép, nên việc tự động hóa trở thành một thí nghiệm thay vì một lợi ích năng suất.
- Bỏ qua bước mã hóa các thực hành của chuyên gia trước khi viết logic Agent, bỏ lỡ cơ hội nhân bản các cách tiếp cận đã kiểm chứng.
- Sinh mã Agent mà không hiểu nó, tạo ra các bản hiện thực mà nhóm không thể duy trì hoặc tiến hóa và tích lũy nợ kỹ thuật.
- Tự động hóa các quy trình biến thiên rộng trong cách thực thi giữa các chuyên gia, nên Agent chọn một biến thể và phát hiện ở thời điểm chạy rằng lựa chọn đó không khớp với ngữ cảnh kinh doanh.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tự động hóa Agent bắt đầu từ thực hành đã kiểm chứng, nên tự động hóa chạy đúng ngay khi triển khai thay vì bị gỡ lỗi trong production.
- Chuyên môn con người vẫn là nguồn chân lý (source of truth) và được khuếch đại thay vì thay thế, bảo tồn năng lực thích ứng.
- Tài nguyên phát triển chảy tới các quy trình nơi ROI có thể biện minh được, thay vì bị chi cho tự động hóa mang tính suy đoán.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Tiêu chí cho một ứng viên tự động hóa tốt rất đơn giản. Quy trình được hiểu rõ, các bước được ghi chép, các tiêu chí quyết định là tường minh, và nhiều chuyên gia thực thi nó theo cùng một cách. Các quy trình không đạt bài kiểm tra đó không nên là những thứ đầu tiên mà tổ chức tự động hóa. Agent sẽ nhân bản bất kỳ biến thể nào mà tài liệu nắm bắt được, và nếu tài liệu nắm bắt sai biến thể, mỗi lần gọi Agent lại củng cố sai lầm. Chính bài tập ghi chép là lợi tức đầu tiên trên khoản đầu tư. Ghi lại những gì chuyên gia làm khuyến khích sự nhất quán ngay cả trước khi bất kỳ Agent nào được xây.

Một khi tài liệu tồn tại, Agent là một bản dịch của nó. Bạn cấu hình các Agent Amazon Bedrock AgentCore để tuân theo cùng các cây quyết định, các điểm kiểm tra xác thực và các đường chuyển lên cấp cao như các chuyên gia con người. Điều này cho tự động hóa cùng hành vi ở thời điểm chạy như quy trình thủ công. [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) giữ chuyên môn đã ghi chép như một nguồn RAG, làm nền tảng cho các quyết định của Agent dựa trên tri thức tổ chức thay vì để chúng cho dữ liệu huấn luyện của Model nền. [Amazon Bedrock AgentCore tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/tools.html) phản chiếu các hệ thống bên ngoài mà chuyên gia dùng (cùng các API, cùng các nguồn dữ liệu và cùng các dịch vụ xác thực), để góc nhìn của Agent về tác vụ khớp với của chuyên gia.

Định tuyến tạo ra sự phân biệt giữa công việc được tự động hóa và công việc con-người-sở-hữu. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) có thể hướng các tác vụ thường quy tới tự động hóa hoàn toàn trong khi chuyển lên cấp cao các công việc phức tạp hoặc mơ hồ tới các chuyên gia con người, hiện thực phân loại ba tầng được mô tả trong [AGENTSUS03-BP01 Duy trì các kỹ năng và năng lực tổ chức](agentsus03-bp01.md) ở thời điểm chạy. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đánh giá liệu đầu ra Agent có khớp với các đường cơ sở do chuyên gia tạo hay không, và [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) lộ các mẫu nơi hành vi Agent đã trôi dạt khỏi thực hành đã ghi chép. Chặn cửa các dự án phát triển Agent bằng các tiêu chí sẵn sàng — đầu vào, đầu ra, tiêu chí quyết định và chỉ số thành công cần được xác định trước khi phát triển bắt đầu, để kỷ luật ghi chép trở thành một điều kiện tiên quyết thay vì một chuyện phụ.

Các công cụ phát triển theo hướng đặc tả (specification-driven) như Kiro áp dụng cùng kỷ luật cho phía hiện thực. Mã Agent được viết từ một đặc tả thì dễ duy trì hơn, dễ review hơn, và ít khả năng nướng vào các giả định mà sau này không ai truy vết được. Sự đánh đổi là công sức trả trước cho đặc tả, vốn thường được thu hồi trong quá trình review, gỡ lỗi và tiến hóa.

### Các bước triển khai

- **Ghi chép các quy trình trước khi tự động hóa chúng:** Nắm bắt các thông tin sau từ các chuyên gia lĩnh vực trước khi phê duyệt việc phát triển Agent: Logic quyết định
- Xử lý ngoại lệ
- Tiêu chí thành công
- Tiêu chí sẵn sàng (đầu vào, đầu ra, tiêu chí quyết định và chỉ số)
- **Lưu tri thức tổ chức dưới dạng các nguồn RAG:** Nạp chuyên môn đã ghi chép vào [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) để các quyết định của Agent lấy nền tảng từ tri thức của tổ chức thay vì các mặc định của Model nền.
- **Phản chiếu quyền truy cập hệ thống của chuyên gia:** Cấu hình [Amazon Bedrock AgentCore tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/tools.html) để cấp cho các Agent cùng các hệ thống bên ngoài và nguồn dữ liệu mà các chuyên gia con người dùng.
- **Định tuyến công việc thường quy so với phức tạp:** Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để gửi các tác vụ thường quy tới tự động hóa hoàn toàn và chuyển lên cấp cao các công việc phức tạp hoặc mơ hồ tới các chuyên gia con người.
- **Xác thực hành vi đối chiếu với các đường cơ sở của chuyên gia:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đối chiếu với các đường cơ sở do chuyên gia tạo và giám sát sự trôi dạt qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS03-BP01 Duy trì các kỹ năng và năng lực tổ chức](agentsus03-bp01.md)
- [AGENTSUS03-BP03 Duy trì các đặc tả toàn diện cho Agent và hệ thống dạng tác nhân](agentsus03-bp03.md)
- [OPS08-BP01 Use runbooks to perform procedures](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock AgentCore tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/tools.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [AI agents in enterprises: Best practices with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
