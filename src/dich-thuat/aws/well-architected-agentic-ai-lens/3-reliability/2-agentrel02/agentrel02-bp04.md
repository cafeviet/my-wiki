# AGENTREL02-BP04 Phát triển các giao thức chỉ dẫn rõ ràng cho tác nhân

Các prompt tùy tiện được từng lời gọi mô hình diễn giải hơi khác nhau tạo ra hành vi khó lường, và vấn đề nhân lên trong các luồng công việc đa tác nhân. Các mẫu chỉ dẫn được chuẩn hóa, prompt có phiên bản và các lược đồ bàn giao (handoff) tường minh giảm sự mơ hồ và làm cho các thoái lui truy vết được về một phiên bản cụ thể.

**Kết quả mong muốn:**

- Bạn có một mẫu system prompt chuẩn tắc mà mọi tác nhân tuân theo, bao quát vai trò, năng lực, ràng buộc, định dạng đầu ra và hành vi leo thang.
- Bạn đánh phiên bản các mẫu prompt tập trung và ghi log phiên bản được dùng ở mỗi lần gọi.
- Bạn có các lược đồ bàn giao tường minh cho ủy thác đa tác nhân để các tác nhân nhận nhận được chỉ dẫn không mơ hồ.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy prompt tùy tiện không có định dạng chuẩn hóa, tạo ra diễn giải không nhất quán về mục tiêu giữa các tác nhân.
- Bỏ qua các quy trình bàn giao tường minh cho điều phối đa tác nhân, để các tác nhân phía dưới tự đoán vai trò của chúng.
- Bỏ qua đánh phiên bản prompt, nên việc hoàn tác một thay đổi có vấn đề đòi hỏi khảo cổ thay vì lật một cờ cấu hình.

**Lợi ích khi áp dụng thực hành tốt này:**

- Hành vi có thể dự đoán thông qua các định dạng chỉ dẫn chuẩn hóa làm giảm sự mơ hồ.
- Điều phối đa tác nhân đáng tin cậy thông qua các quy trình bàn giao tường minh và bảo toàn ngữ cảnh.
- Gỡ lỗi và tinh chỉnh nhanh hơn thông qua các mẫu nhất quán mà bạn có thể kiểm thử một cách hệ thống.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Định nghĩa một cấu trúc mà mọi system prompt tuân theo. Cấu trúc này nên bao quát định nghĩa vai trò, mô tả năng lực, đặc tả ràng buộc, yêu cầu định dạng đầu ra và hành vi leo thang. Biến mẫu này thành điểm khởi đầu cho bất kỳ tác nhân mới nào. Khi mọi tác nhân thừa hưởng cùng một cấu trúc, người rà soát có thể kiểm tra các phần quan trọng chỉ trong nháy mắt và các thoái lui dễ nhìn thấy hơn vì các khác biệt (diff) nhỏ.

Lưu trữ mẫu là nơi việc đánh phiên bản diễn ra. Lưu prompt trong một kho cấu hình có phiên bản để các thay đổi không đòi hỏi triển khai lại. Gán định danh phiên bản cho mọi mẫu và ghi log phiên bản được dùng trong mỗi lần gọi qua [ghi log gọi mô hình Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html). Khi một thoái lui xuất hiện, ID phiên bản trên vết lỗi cho bạn biết chính xác mẫu nào chịu trách nhiệm.

Bàn giao cần lược đồ riêng của nó. Đối với điều phối đa tác nhân, một thông điệp bàn giao tường minh nên mang theo định danh tác vụ, loại tác vụ, thân thông điệp, bối cảnh thực thi, hạn chót và cơ chế gọi lại (callback). Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để quản lý khám phá và gọi với các hợp đồng giao diện được định nghĩa tốt. Kiểm định các phiên bản prompt mới ngoại tuyến bằng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để so sánh hành vi tác nhân trước khi di trú, và chạy các bài kiểm thử hợp đồng trong CI/CD bao gồm các trường hợp đối kháng được thiết kế để phơi bày lỗ hổng tiêm prompt (prompt injection).

### Các bước triển khai

- **Định nghĩa một mẫu system prompt chuẩn tắc:** Thiết lập một cấu trúc chung cho vai trò, năng lực, ràng buộc, định dạng đầu ra và hành vi leo thang mà mọi tác nhân thừa hưởng.
- **Lưu các mẫu prompt trong một kho cấu hình có phiên bản:** Tập trung quản lý để các cập nhật prompt không đòi hỏi triển khai lại.
- **Thiết kế các lược đồ thông điệp bàn giao tường minh:** Định nghĩa một định dạng thông điệp bàn giao chuẩn tắc cho ủy thác đa tác nhân với định danh tác vụ, thân thông điệp và cơ chế gọi lại.
- **Dùng AgentCore Evaluations để so sánh các phiên bản prompt:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trên các phiên bản ứng viên trước khi di trú lưu lượng vận hành.
- **Chạy các bài kiểm thử hợp đồng tự động trong CI/CD:** Bao gồm phát hiện tiêm prompt đối kháng để các thoái lui giao thức không được xuất xưởng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL02-BP01 Thiết kế các tác nhân cho các tác vụ cụ thể và nguyên tử](agentrel02-bp01.md)
- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](agentrel02-bp03.md)
- [AGENTREL02-BP05 Thiết lập giám sát của con người theo tầng và các luồng phê duyệt](agentrel02-bp05.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Build reliable AI agents with Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
