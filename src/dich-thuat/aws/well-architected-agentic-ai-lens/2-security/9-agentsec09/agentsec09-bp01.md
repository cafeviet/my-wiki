# AGENTSEC09-BP01 Tích hợp quét lỗ hổng có AI hỗ trợ trên toàn vòng đời phát triển

Các bộ quét khớp mẫu (pattern-matching) tìm các lỗi phổ biến nhưng bỏ sót các lỗ hổng phụ thuộc ngữ cảnh trong điều phối agent, các tương tác công cụ và các chuỗi ủy quyền. Quét có AI hỗ trợ suy luận về mã và các tài liệu thiết kế theo cách một nhà nghiên cứu bảo mật con người làm bắt được các vấn đề này tại giai đoạn mà việc khắc phục rẻ nhất.

**Kết quả mong muốn:**

- Quét lỗ hổng được nhúng ở mọi giai đoạn của vòng đời phát triển AI tác tử, bao phủ các tài liệu thiết kế, các pull request và các ứng dụng đã triển khai.
- Bạn rà soát các tài liệu thiết kế tìm các rủi ro bảo mật trước khi mã được viết, phân tích các pull request tìm các lỗ hổng phổ biến và riêng của agent trong quá trình phát triển, và liên tục quét các ứng dụng đã triển khai tìm các đe dọa mới nổi.
- Các phát hiện mang các đánh giá mức độ nghiêm trọng, các điểm độ tin cậy và hướng dẫn khắc phục thực tế để các nhóm có thể ưu tiên và sửa các vấn đề một cách hiệu quả.

**Các phản mẫu thường gặp (anti-patterns):**

- Dựa vào phân tích tĩnh dựa trên quy tắc khớp các mẫu lỗ hổng đã biết, bỏ sót các vấn đề phụ thuộc ngữ cảnh trong logic điều phối agent, xử lý tham số công cụ không an toàn, hoặc kiểm soát truy cập bị hỏng trong các chuỗi ủy thác đa agent.
- Chỉ thực hiện quét bảo mật tại thời điểm triển khai thay vì qua các giai đoạn thiết kế và phát triển, để cho các lỗ hổng tích lũy và làm cho việc khắc phục phát hiện muộn trở nên tốn kém.
- Coi mã do AI sinh giống như mã do con người viết cho rà soát bảo mật, bỏ qua các mẫu lỗ hổng đặc thù mà các trợ lý lập trình AI đưa vào (các lời gọi API ảo giác, các cấu hình mặc định không an toàn, và việc dùng thư viện lỗi thời).

**Lợi ích khi áp dụng thực hành tốt này:**

- Các rà soát bảo mật giai đoạn thiết kế nhận diện các rủi ro kiến trúc trước khi mã được viết, giảm chi phí khắc phục và các trì hoãn phát triển.
- Quét có AI hỗ trợ suy luận về ngữ cảnh ứng dụng và hành vi agent bắt được các lỗ hổng phức tạp mà các công cụ khớp mẫu bỏ sót.
- Quét tự động được tích hợp vào các đường ống CI/CD mở rộng chuyên môn bảo mật qua các nhóm phát triển mà không tạo ra các nút thắt cổ chai.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Khớp mẫu so với các chữ ký đã biết là không đủ cho các hệ thống tác tử. Một chữ ký SQL injection không bắt được một chuỗi ủy quyền đa agent bị hỏng, và một quy tắc thiếu-kiểm-định-đầu-vào không bắt được một tham số công cụ bị thao túng qua một prompt injection. Việc quét vươn tới các vấn đề đó phải suy luận về cách các thành phần tương tác, truy vết các luồng dữ liệu qua lớp điều phối, và hiểu agent thực sự được dự định làm gì. Đó là năng lực mà quét có AI hỗ trợ bổ sung, và tại sao nó hiệu quả trên các lỗ hổng riêng của agent.

Hãy triển khai quét trên toàn vòng đời. Ở giai đoạn thiết kế, dùng các công cụ phân tích các tài liệu kiến trúc, các đặc tả sản phẩm và các thiết kế kỹ thuật tìm các rủi ro bảo mật trước khi mã được viết. Trong quá trình phát triển, tích hợp quét vào các luồng công việc rà soát mã để phân tích các pull request tìm cả các lỗ hổng phổ biến (SQL injection, thiếu kiểm định đầu vào) lẫn các vấn đề riêng của agent (các lần gọi công cụ không an toàn, giới hạn phạm vi quyền hạn không đủ). Tại triển khai, chạy các lần quét theo yêu cầu so với các ứng dụng đang chạy để kiểm chứng rằng các kiểm soát bảo mật đứng vững dưới các điều kiện thực tế.

[AWS Security Agent](https://aws.amazon.com/security-agent/) cung cấp độ bao phủ vòng đời này như một năng lực duy nhất. Các đội bảo mật định nghĩa các yêu cầu bảo mật của tổ chức một lần trong AWS Management Console (các thư viện ủy quyền được phê duyệt, các chuẩn ghi log, các chính sách truy cập dữ liệu), và AWS Security Agent thực thi chúng xuyên suốt quá trình phát triển, đánh giá các tài liệu thiết kế và mã so với các chuẩn và cung cấp hướng dẫn cụ thể khi nó phát hiện các vi phạm. Với các rà soát bảo mật mã, hãy cấu hình AWS Security Agent giám sát các repository và phân tích các pull request để việc đánh giá mở rộng qua các codebase trong khi giữ sự giám sát trên các vấn đề quan trọng.

Mã do AI sinh cần sự soi xét thêm. Các trợ lý lập trình AI đưa vào các mẫu lỗ hổng khác với mã do con người viết điển hình (các lời gọi API ảo giác, các cấu hình mặc định không an toàn, việc dùng phụ thuộc lỗi thời), và các công cụ quét cần gắn cờ những cái này một cách tường minh. Các công cụ như Claude Code Security dùng kiểm chứng nhiều giai đoạn nơi các phát hiện được kiểm tra lại để chứng minh hoặc bác bỏ các kết quả và lọc ra các dương tính giả trước khi chúng tới các nhà phân tích, điều giảm nhiễu và cho phép các nhóm tập trung vào các vấn đề đã được kiểm chứng.

### Các bước triển khai

- **Mã hóa các yêu cầu bảo mật một cách tập trung:** Định nghĩa các yêu cầu bảo mật của tổ chức (các thư viện được phê duyệt, các chuẩn ghi log, các chính sách truy cập dữ liệu) và cấu hình chúng trong [AWS Security Agent](https://aws.amazon.com/security-agent/) để thực thi tự động qua các nhóm phát triển.
- **Chạy các rà soát giai đoạn thiết kế:** Cấu hình AWS Security Agent phân tích các tài liệu kiến trúc và các đặc tả kỹ thuật trước khi phát triển bắt đầu.
- **Bật rà soát mã ở cấp PR:** Kết nối AWS Security Agent tới các repository mã của bạn để bao phủ cả mã do con người viết lẫn mã do AI sinh trên mỗi pull request.
- **Cấu hình kiểm chứng nhiều giai đoạn:** Thiết lập quét có AI hỗ trợ với kiểm chứng nhiều giai đoạn để giảm các dương tính giả và gán các đánh giá mức độ nghiêm trọng cho các phát hiện đã được kiểm chứng.
- **Phân loại và theo dõi đến khi giải quyết:** Định tuyến các lỗ hổng đã được kiểm chứng tới nhóm phù hợp kèm hướng dẫn khắc phục, và theo dõi các phát hiện đến khi giải quyết.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC07-BP05 Đánh giá bảo mật định kỳ và red teaming](../7-agentsec07/agentsec07-bp05.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](../8-agentsec08/agentsec08-bp01.md)
- [AGENTSEC09-BP02 Tiến hành kiểm thử xâm nhập có nhận thức ngữ cảnh với mô phỏng tấn công đa agent](agentsec09-bp02.md)

**Tài liệu liên quan:**

- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [Security Considerations for AWS Security Agent and AI assisted penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)
- [Claude Code Security, Making frontier cybersecurity capabilities available to defenders](https://www.anthropic.com/news/claude-code-security)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon CodeGuru Security](https://aws.amazon.com/codeguru/)
