# AGENTOPS07-BP03 Bổ sung quản trị thay đổi để đáp ứng các cải tiến kỹ thuật và các yêu cầu kinh doanh

Một quy trình quản trị thay đổi được xây dựng chỉ cho các thay đổi kỹ thuật sẽ không tính đến cách các agent thực sự tiến hóa. Các điều chỉnh Prompt, việc thêm Tools, và các nâng cấp Model đều mang các hàm ý kinh doanh mà rà soát thuần kỹ thuật không bắt được. Một quy trình lôi kéo cả các bên liên quan kỹ thuật và kinh doanh, tỷ lệ thuận với phạm vi thay đổi, giữ cho các agent phù hợp với các mục tiêu mà chúng tồn tại để phục vụ.

**Kết quả mong muốn:**

- Mỗi thay đổi agent, cải tiến kỹ thuật hay yêu cầu kinh doanh, tuân theo một quy trình quản trị thay đổi được tài liệu hóa.
- Các bên liên quan kỹ thuật và kinh doanh được lôi kéo phù hợp dựa trên phạm vi và tác động của thay đổi.
- Lý do biện minh kinh doanh cho mỗi thay đổi được tài liệu hóa và có thể truy vết, để sự tiến hóa agent có mục đích.
- Các agent tiến hóa đồng bộ với các thay đổi tổ chức thay vì trôi lệch khỏi sự phù hợp.

**Các phản mẫu thường gặp (anti-patterns):**

- Quản lý các thay đổi agent thông qua các quy trình quản trị thay đổi thuần kỹ thuật mà không có sự tham gia của các bên liên quan kinh doanh, cho phép các agent trôi lệch khỏi các mục tiêu kinh doanh.
- Đối xử mọi thay đổi agent như các thay đổi kỹ thuật mà không đánh giá tác động kinh doanh, bỏ lỡ các thay đổi ảnh hưởng tới các quy trình kinh doanh, trải nghiệm khách hàng, hoặc các yêu cầu tuân thủ.
- Triển khai các quy trình quản trị thay đổi nặng nề đến mức các nhóm lách qua chúng cho các thay đổi khẩn cấp, tạo ra một quy trình ngầm phi chính thức thiếu quản trị và khả năng truy vết.
- Không đồng bộ các thay đổi agent với các thay đổi tổ chức rộng hơn (như các cập nhật quy trình, các thay đổi chính sách, và các cập nhật pháp lý), khiến các agent vận hành dựa trên các quy tắc kinh doanh lỗi thời.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản trị thay đổi được tài liệu hóa với lý do biện minh kinh doanh tạo ra một hồ sơ có thể kiểm toán về sự tiến hóa agent có mục đích, được quản trị.
- Quản trị thay đổi nắm bắt lý do biện minh kinh doanh và đánh giá tác động, tạo ra một vòng lặp phản hồi cung cấp thông tin cho việc ưu tiên hóa trong tương lai.
- Phân loại hai chiều (phạm vi kỹ thuật, tác động kinh doanh) giúp đúng các bên liên quan tham gia với đúng các thay đổi thay vì mọi người rà soát mọi thứ.
- Đồng bộ với các thay đổi tổ chức giúp ngăn các agent vận hành dưới các quy tắc kinh doanh lỗi thời.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Phân loại các thay đổi theo hai chiều, phạm vi kỹ thuật và tác động kinh doanh, giúp giữ cho các quy trình của bạn tỷ lệ thuận.

Phạm vi kỹ thuật nắm bắt loại thay đổi là gì, như cập nhật Prompt, thay đổi Tools, thay đổi Model, hoặc thay đổi kiến trúc. Tác động kinh doanh nắm bắt điều nó ảnh hưởng, như không có, điều chỉnh nhỏ, thay đổi quy trình đáng kể, hoặc ảnh hưởng tuân thủ. Sự kết hợp xác định các luồng phê duyệt bắt buộc, độ sâu tài liệu, và mức độ nghiêm ngặt của kiểm thử. Một điều chỉnh câu chữ Prompt không có tác động kinh doanh đi qua quy trình nhanh chóng, trong khi một tích hợp Tools mới có hàm ý tuân thủ kích hoạt rà soát đầy đủ.

Các buổi rà soát sự phù hợp kinh doanh giúp bạn bắt được trôi lệch cấu hình chậm. Các năng lực agent từng hiệu quả khi quy trình kinh doanh là X có thể không hiệu quả khi quy trình kinh doanh là Y, và nếu không ai định kỳ kiểm định sự phù hợp, trôi lệch tích tụ mà không được chú ý. Một buổi rà soát định kỳ, ví dụ theo quý, kiểm định liệu các năng lực agent có còn phù hợp với các quy trình kinh doanh, chính sách, và yêu cầu pháp lý hiện tại hay không. Hãy thiết lập một cơ chế rà soát trong đó một ánh xạ agent-tới-quy-trình-kinh-doanh được duy trì trong catalog danh mục, với các thông báo được định tuyến tới các chủ sở hữu agent phụ thuộc khi các quy trình kinh doanh được cập nhật.

Theo dõi khối lượng thay đổi, thời gian chu kỳ phê duyệt, và các chỉ số phù hợp giữ cho chính quy trình luôn được quan sát để cải tiến liên tục. Các quy trình mất quá lâu hoặc bắt được quá ít vấn đề nên được rà soát và cập nhật khi cần. Giám sát các chỉ số kiểm định việc phân bậc hiện tại.

### Các bước triển khai

- **Định nghĩa một ma trận phân loại thay đổi:** Ánh xạ phạm vi kỹ thuật và tác động kinh doanh tới các phê duyệt và tài liệu bắt buộc.
- **Triển khai các luồng yêu cầu thay đổi:** Dùng các mẫu có cấu trúc nắm bắt cả lý do biện minh kỹ thuật và kinh doanh.
- **Thiết lập các buổi rà soát sự phù hợp kinh doanh định kỳ:** Kiểm định rằng các năng lực agent khớp với các quy trình kinh doanh, chính sách, và yêu cầu pháp lý hiện tại.
- **Duy trì các ánh xạ agent-tới-quy-trình-kinh-doanh:** Cấu hình các thông báo khi các quy trình được cập nhật để các agent phụ thuộc có thể được rà soát.
- **Theo dõi các chỉ số quản trị thay đổi:** Giám sát khối lượng thay đổi, thời gian chu kỳ phê duyệt, và các thước đo phù hợp để giữ cho quy trình tỷ lệ thuận.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS07-BP01 Triển khai các cơ chế ứng phó và phục hồi tự động](agentops07-bp01.xml)
- [AGENTOPS07-BP02 Thiết lập các hệ thống quản lý tri thức vận hành](agentops07-bp02.xml)
- [AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh](../agentops06/agentops06-bp03.xml)
- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](../agentops03/agentops03-bp01.xml)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)
- [Operationalizing agentic AI, Part 1: A stakeholder's guide](https://aws.amazon.com/blogs/machine-learning/operationalizing-agentic-ai-part-1-a-stakeholders-guide/)
- [Advancing AI agent governance with Boomi and AWS: A unified approach to observability and compliance](https://aws.amazon.com/blogs/machine-learning/advancing-ai-agent-governance-with-boomi-and-aws-a-unified-approach-to-observability-and-compliance)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
