# AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác

Một tác nhân không khả dụng không nên hạ gục cả một luồng công việc. Các chuỗi dự phòng định trước cho phép các bộ điều phối thay thế bằng các phương án khác, bảo toàn tiến độ với chất lượng giảm bớt thay vì một sự đình trệ hoàn toàn.

**Kết quả mong muốn:**

- Bạn có các chuỗi dự phòng cho mỗi tác nhân trọng yếu với các phương án thay thế có thứ tự và các đánh đổi chất lượng được tài liệu hóa.
- Bạn kiểm tra sức khỏe tác nhân một cách chủ động và bỏ qua các tác nhân không khả dụng thay vì chờ timeout.
- Bạn truyền đạt sự suy giảm cho các hệ thống phía dưới qua các sự kiện có cấu trúc để hành vi của chúng có thể thích ứng.

**Các phản mẫu thường gặp (anti-patterns):**

- Thiết kế các luồng công việc đa tác nhân không có đường dự phòng, nên một tác nhân lỗi làm dừng toàn bộ luồng công việc.
- Triển khai các dự phòng âm thầm làm giảm chất lượng mà không báo cho người dùng hoặc các hệ thống phía dưới.
- Bỏ qua kiểm thử dự phòng, chỉ phát hiện ra các khoảng trống trong các sự cố vận hành.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chức năng luồng công việc một phần vẫn duy trì khi một tác nhân riêng lẻ bị lỗi.
- Suy giảm minh bạch tới được người dùng và các hệ thống phía dưới để họ có thể thích ứng.
- Luồng công việc hoàn tất nhanh hơn thông qua các đường dự phòng định trước tự kích hoạt.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các chuỗi dự phòng cho bộ điều phối một nơi để đi tới khi tác nhân ưu tiên gặp sự cố. Mỗi chuỗi là một trình tự có thứ tự. Đầu tiên, một tác nhân thứ cấp với năng lực tương đương. Rồi, một tác nhân đơn giản hóa với năng lực giảm bớt. Tiếp theo, một kết quả cache từ một lần thực thi trước. Cuối cùng, một phản hồi thất bại nhẹ nhàng. Thứ tự quan trọng vì nó nắm bắt sự đánh đổi chất lượng. Vài phương án đầu bảo toàn hầu hết chức năng, và các phương án sau chấp nhận suy giảm lớn hơn để đổi lấy việc giữ luồng công việc tiếp tục di chuyển. Tài liệu hóa tác động chất lượng của mỗi cấp để các bộ điều phối chọn phương án tốt nhất hiện có thay vì phương án khả thi kỹ thuật đầu tiên.

Kiểm tra sức khỏe chủ động giữ độ trễ dự phòng thấp. Không có nó, bộ điều phối chờ tác nhân ưu tiên hết timeout trước khi thử dự phòng, chồng thêm các hình phạt độ trễ cấp tác nhân lên luồng công việc. Kiểm tra các số liệu của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và điểm cuối /ping của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) trước khi gọi. Khi một tác nhân báo sức khỏe suy giảm, bỏ qua nó và chuyển thẳng tới phương án tiếp theo.

Khi một dự phòng kích hoạt, công bố một sự kiện suy giảm có cấu trúc xác định tác nhân bị lỗi, dự phòng được kích hoạt và tác động năng lực. Các hệ thống phía dưới đăng ký và thích ứng bằng cách gắn cờ đầu ra để rà soát thêm, hiển thị thông báo suy giảm cho người dùng, hoặc định tuyến vòng qua luồng công việc bị ảnh hưởng hoàn toàn. Kiểm định các cơ chế dự phòng qua kỹ thuật hỗn loạn (chaos engineering) bằng [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html). Tiêm các lỗi tác nhân trong các môi trường phi vận hành để xác nhận các chuỗi dự phòng kích hoạt đúng và các luồng công việc hoàn tất với các đầu ra suy giảm như kỳ vọng.

### Các bước triển khai

- **Thiết kế các chuỗi dự phòng cho mỗi tác nhân trọng yếu:** Định nghĩa một trình tự có thứ tự các phương án với các đánh đổi chất lượng được tài liệu hóa ở mỗi cấp.
- **Triển khai kiểm tra sức khỏe chủ động trước khi gọi:** Kiểm tra các số liệu của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và điểm cuối /ping của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), và bỏ qua các tác nhân báo sức khỏe suy giảm.
- **Cấu hình các chuyển tiếp dự phòng trong lớp điều phối:** Phân biệt các lỗi thoáng qua (thử lại trước) với các lỗi bền vững (dự phòng ngay).
- **Công bố các sự kiện suy giảm có cấu trúc khi các dự phòng kích hoạt:** Phát các sự kiện để các hệ thống phía dưới tiêu thụ nhằm giúp phần còn lại của môi trường thích ứng.
- **Kiểm định các cơ chế dự phòng qua kỹ thuật hỗn loạn:** Dùng [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) để tiêm các lỗi tác nhân theo lịch đều đặn và xác nhận các chuỗi vẫn hoạt động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL04-BP01 Triển khai mẫu tác nhân trọng tài (arbiter) cho các hệ thống đa tác nhân được phối hợp](agentrel04-bp01.md)
- [AGENTREL04-BP02 Phân loại các tác nhân bằng một phân loại năng lực kỹ lưỡng](agentrel04-bp02.md)
- [AGENTREL04-BP04 Triển khai các control plane bền bỉ cho việc phối hợp tác nhân](agentrel04-bp04.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](../8-agentrel08/agentrel08-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Multi-agent collaboration with Strands](https://aws.amazon.com/blogs/devops/multi-agent-collaboration-with-strands/)
- [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Fault Injection Service](https://aws.amazon.com/fis/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
