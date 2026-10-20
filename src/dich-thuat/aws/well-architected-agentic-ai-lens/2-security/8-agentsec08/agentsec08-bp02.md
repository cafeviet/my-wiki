# AGENTSEC08-BP02 Lọc đầu ra cho thông tin nhạy cảm

Lọc các phản hồi hướng người dùng để ngỏ các đường dữ liệu nội bộ (các thông điệp giữa các agent, các lượt ghi bộ nhớ, các log kiểm toán) như các kênh mở để PII và thông tin xác thực thoát ra. Quét mọi đường đầu ra bằng một chính sách phân loại dữ liệu giữ nội dung nhạy cảm bên trong phạm vi xử lý được ủy quyền của agent.

**Kết quả mong muốn:**

- Bạn quét các đầu ra của agent tìm PII, thông tin xác thực và dữ liệu nhạy cảm khác trước khi trả về cho người dùng hoặc các hệ thống phía sau, với nội dung được che hoặc chặn dựa trên các chính sách phân loại dữ liệu.
- Các đầu ra của agent chứa thông tin xác thực, khóa riêng hoặc PII được quản chế bị chặn hoặc che trước khi chúng tới người dùng cuối hoặc các hệ thống bên ngoài.
- Bạn ghi log các quyết định lọc đầu ra phục vụ kiểm toán tuân thủ.

**Các phản mẫu thường gặp (anti-patterns):**

- Dựa vào mô hình để tự kiểm duyệt thông tin nhạy cảm, trong khi các mô hình thực sự có sinh các đầu ra chứa PII hoặc thông tin xác thực (đặc biệt khi thông tin đó nằm trong ngữ cảnh của agent từ các đầu ra công cụ hoặc các tài liệu được truy xuất).
- Chỉ áp dụng lọc đầu ra cho các phản hồi hướng người dùng trong khi bỏ qua lọc cho các đầu ra được truyền tới các agent khác hoặc được lưu trong bộ nhớ, tạo ra các đường rò rỉ dữ liệu qua các giao tiếp nội bộ.
- Dùng các quy tắc che quá rộng che nội dung hợp lệ cùng với dữ liệu nhạy cảm, làm suy giảm chất lượng đầu ra đến mức người dùng tìm cách lách bộ lọc.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thực thi phân loại dữ liệu tại ranh giới agent giúp giữ thông tin nhạy cảm trong phạm vi xử lý dữ liệu được ủy quyền của agent bất kể mô hình sinh ra gì.
- Các quyết định lọc được ghi log hỗ trợ tuân thủ các quy định bảo vệ dữ liệu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Mọi đường đầu ra là một đường trích xuất (exfiltration) tiềm tàng. Các phản hồi hướng người dùng là đường hiển nhiên, nhưng một agent cũng ghi vào bộ nhớ, truyền nội dung tới các agent khác, và phát ra các log. Chỉ lọc đường hướng người dùng để lại các đường khác như các kênh mở cho dữ liệu nhạy cảm, và các đầu vào đối kháng được thiết kế để trích xuất dữ liệu không nhất thiết nhắm vào kênh hướng người dùng. Yêu cầu về mặt kiến trúc là mọi bề mặt đầu ra đi qua cùng một bộ lọc, không chỉ những bề mặt người dùng thấy.

Các bộ lọc thông tin nhạy cảm của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-info.html) bao phủ các loại dữ liệu liên quan đến hầu hết các ca sử dụng:

- Các danh mục PII (tên, địa chỉ, số điện thoại, địa chỉ email, SSN, và số tài khoản tài chính)
- Thông tin xác thực (API key, mật khẩu, và khóa riêng)
- Các loại thực thể tùy chỉnh riêng của tổ chức bạn

Hãy cấu hình hành động bộ lọc là MASK (che) cho hầu hết các loại dữ liệu nhạy cảm để bảo tồn tính hữu dụng của đầu ra trong khi bảo vệ nội dung nhạy cảm, và BLOCK (chặn) cho các danh mục nhạy cảm nhất như thông tin xác thực và khóa riêng nơi việc che là không đủ.

Hãy áp dụng bộ lọc như middleware trong đường ống đầu ra của agent, để mọi đích đầu ra — các phản hồi hướng người dùng, các thông điệp giữa các agent, các lượt ghi vào [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html) qua API create_event, và các log kiểm toán — đều chảy qua nó. Các chiến lược bộ nhớ dài hạn dựng sẵn của AgentCore Memory đã lọc PII khỏi các bản ghi dài hạn được trích xuất theo mặc định, nhưng bộ nhớ ngắn hạn (các sự kiện thô) giữ nội dung gốc, nên các yêu cầu tuân thủ cấm PII trong bất kỳ dạng lưu trữ nào đòi hỏi áp dụng các bộ lọc thông tin nhạy cảm Guardrails trước khi ghi các sự kiện vào bộ nhớ ngắn hạn nữa.

Với các loại dữ liệu nhạy cảm riêng của tổ chức không được bao phủ bởi các danh mục dựng sẵn, các bộ nhận diện thực thể tùy chỉnh của Amazon Comprehend mở rộng độ bao phủ. Hãy huấn luyện các bộ nhận diện trên các ví dụ về các loại dữ liệu nhạy cảm của bạn và tích hợp chúng vào đường ống lọc đầu ra qua các hàm AWS Lambda gọi API Amazon Comprehend trước khi trả về các đầu ra.

Ghi log mọi quyết định lọc (loại dữ liệu nhạy cảm được phát hiện, hành động được thực hiện (che hoặc chặn), đích đầu ra) tạo ra báo cáo phòng chống thất thoát dữ liệu (data loss prevention) và bắt các mẫu nơi agent đang sinh một cách hệ thống các đầu ra chứa dữ liệu nhạy cảm (một tín hiệu của prompt injection hoặc trích xuất dữ liệu). Các cảnh báo Amazon CloudWatch về các tỷ lệ phát hiện tăng cao biến tín hiệu đó thành một cảnh báo đang diễn ra.

### Các bước triển khai

- **Cấu hình các bộ lọc thông tin nhạy cảm:** Thiết lập [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-info.html) với các bộ lọc cho mọi danh mục PII và thông tin xác thực liên quan, chọn MASK hoặc BLOCK theo từng danh mục dựa trên chính sách phân loại dữ liệu.
- **Lọc mọi đường đầu ra:** Áp dụng lọc đầu ra như một lớp middleware cho các phản hồi hướng người dùng, các thông điệp giữa các agent, các lượt ghi bộ nhớ và các log kiểm toán.
- **Lọc trước các lượt ghi bộ nhớ ngắn hạn khi cần:** Với các yêu cầu tuân thủ cấm PII trong bất kỳ dạng lưu trữ nào, áp dụng lọc Guardrails trước khi ghi các sự kiện vào kho ngắn hạn của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html).
- **Mở rộng bằng các thực thể tùy chỉnh của Amazon Comprehend:** Huấn luyện các bộ nhận diện thực thể tùy chỉnh của Amazon Comprehend cho các loại dữ liệu nhạy cảm riêng của tổ chức và tích hợp chúng vào đường ống lọc.
- **Ghi log và cảnh báo về các phát hiện:** Ghi log mọi quyết định lọc đầu ra với metadata về loại dữ liệu, hành động và đích, và cấu hình các cảnh báo Amazon CloudWatch cho các tỷ lệ phát hiện dữ liệu nhạy cảm tăng cao.
- **Rà soát các cấu hình định kỳ:** Điều chỉnh lọc đầu ra để khớp với các chính sách phân loại dữ liệu đang tiến hóa và các loại dữ liệu được quản chế mới.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](agentsec08-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Guardrails sensitive information filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-info.html)
- [Thực hành tốt Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)
- [Tài liệu Amazon Comprehend](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Comprehend](https://aws.amazon.com/comprehend/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
