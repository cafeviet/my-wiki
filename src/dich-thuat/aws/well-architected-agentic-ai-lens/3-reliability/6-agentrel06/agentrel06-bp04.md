# AGENTREL06-BP04 Triển khai các mẫu thực thi tác vụ idempotent

Thử lại (retry) là cơ chế phục hồi phổ biến nhất, và không có **idempotency** nó có thể tạo ra các tác dụng phụ trùng lặp. Các idempotency key tất định và ghi có điều kiện cho phép các thao tác được thử lại một cách an toàn mà không tạo ra các tác dụng phụ trùng lặp.

**Kết quả mong muốn:**

- Bạn sinh các idempotency key tất định từ đầu vào của thao tác, nhờ đó các lần thử lại của cùng một thao tác logic luôn tạo ra cùng một khóa.
- Bạn kiểm tra một kết quả hiện có trước khi thực thi bất kỳ thao tác có tác dụng phụ nào và trả về kết quả cache nếu thao tác đã thành công.
- Bạn lan truyền các idempotency key qua các luồng công việc nhiều bước và tới các hệ thống bên ngoài hỗ trợ idempotency tích hợp sẵn.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các lần thử lại mà không có bảo đảm idempotency, tạo ra các tác dụng phụ trùng lặp khi các thao tác được thử lại sau khi hoàn tất một phần.
- Dùng các định danh phi tất định cho các idempotency key, nên các lần thử lại của cùng một thao tác sinh các khóa khác nhau và phá vỡ bảo đảm.
- Không lan truyền các idempotency key qua các luồng công việc nhiều bước, cho phép các tác dụng trùng lặp ở các bước không nhận được khóa gốc.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phục hồi dựa trên thử lại từ các lỗi thoáng qua trở nên an toàn mà không có các tác dụng phụ trùng lặp.
- Xử lý lỗi đơn giản hơn vì các lần thực thi đầu tiên và thử lại trông giống hệt nhau.
- Các luồng công việc nhiều bước phục hồi đáng tin cậy vì các idempotency key chảy qua mọi bước.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Sinh idempotency key là nơi hầu hết các đội mắc lỗi. Các khóa phi tất định (dấu thời gian và UUID sinh ra tại thời điểm thử lại) phá vỡ cơ chế vì lần thử lại tính ra một khóa khác với lần thử ban đầu. Các khóa tất định được suy ra từ đầu vào của thao tác thì hoạt động. Băm (hash) ID luồng công việc, loại tác vụ và thân yêu cầu, và cùng một thao tác logic luôn tạo ra cùng một khóa. Đây là chi tiết quan trọng nhất phải làm đúng vì mọi thứ khác phụ thuộc vào nó.

Một khi khóa ổn định, bước kiểm tra tiền thực thi trở nên đơn giản. Trước khi thực thi một thao tác có tác dụng phụ, truy vấn kho idempotency để tìm một kết quả hiện có được đánh khóa trên cùng định danh. Nếu bạn tìm thấy một kết quả và nó đã thành công, trả về kết quả cache mà không thực thi lại. Nếu không, chạy thao tác và ghi lại kết quả. [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) với ghi có điều kiện làm cho điều này an toàn trong điều kiện đồng thời. Hai lần thử lại song song không thể cùng tạo một bản ghi, và hết hạn dựa trên TTL giữ cho kho không phình vô hạn trong khi vẫn duy trì bảo đảm trong cửa sổ thử lại kỳ vọng.

Lan truyền mở rộng bảo đảm qua các luồng công việc. Khi một bộ điều phối ủy thác một tác vụ con, hãy bao gồm khóa của luồng công việc cha hoặc một dẫn xuất tất định của nó để các tác nhân phía dưới duy trì idempotency qua mọi bước. Đối với các thao tác tương tác với các hệ thống bên ngoài hỗ trợ cơ chế idempotency tích hợp sẵn, chuyển khóa của tác nhân tới hệ thống bên ngoài. Giám sát sức khỏe kho idempotency qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), theo dõi tỷ lệ trúng cache (cache hit rate). Các lần thử lại trả về kết quả cache là tín hiệu cho thấy cơ chế đang hoạt động như dự định.

### Các bước triển khai

- **Thiết kế các idempotency key tất định:** Suy ra các khóa từ đầu vào của thao tác thông qua băm nhất quán để các lần thử lại sinh cùng khóa như lần thử ban đầu.
- **Triển khai kiểm tra idempotency như một bước tiền thực thi:** Dùng [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) với ghi có điều kiện và hết hạn dựa trên TTL để lưu các bản ghi idempotency một cách an toàn.
- **Lan truyền các idempotency key qua các luồng công việc nhiều bước:** Duy trì idempotency qua mọi bước bằng cách chuyển khóa của luồng công việc cha hoặc một dẫn xuất tất định tới các bước phía dưới.
- **Chuyển các khóa tới các hệ thống bên ngoài có idempotency tích hợp sẵn:** Ngăn xử lý trùng lặp ở cấp hệ thống bên ngoài bằng cách chuyển tiếp khóa của tác nhân.
- **Giám sát tỷ lệ trúng cache:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để theo dõi các lần thử lại trả về kết quả cache, xác nhận cơ chế đang hoạt động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL06-BP01 Phát triển các tích hợp dựa trên tác nhân với các hệ thống hiện có hoặc kế thừa](agentrel06-bp01.md)
- [AGENTREL06-BP03 Kiểm thử hiệu năng hệ thống suy giảm một cách đều đặn](agentrel06-bp03.md)
- [AGENTREL06-BP05 Triển khai bật/tắt năng lực động](agentrel06-bp05.md)

**Tài liệu liên quan:**

- [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)

**Dịch vụ liên quan:**

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
