# AGENTSUS03-BP01 Duy trì các kỹ năng và năng lực tổ chức

Các tổ chức tự động hóa mà không có chủ đích bảo tồn chuyên môn con người đằng sau việc tự động hóa sẽ mất đi năng lực đào tạo nhân viên mới, xử lý các trường hợp biên (edge case) và phục hồi khi các hệ thống tự động chạm giới hạn của chúng. Giữ một sự phân biệt rõ ràng giữa những gì Agent xử lý tự chủ và những gì ở lại với các chuyên gia con người sẽ duy trì năng lực tổ chức xuyên suốt toàn bộ vòng đời triển khai.

**Kết quả mong muốn:**

- Bạn có một phân loại năng lực (competency taxonomy) tách biệt các tác vụ con-người-sở-hữu, Agent-tăng-cường và tự-động-hóa-hoàn-toàn, với các tiêu chí được ghi chép cho mỗi tầng.
- Định tuyến ở lớp Agent tự động chuyển lên cấp cao (escalate) các quyết định nhiều rủi ro, mơ hồ hoặc trường hợp biên tới các chuyên gia con người.
- Các chương trình luân phiên và các workshop giữ cho các chuyên gia lĩnh vực (subject matter expert) thành thạo với các quy trình mà Agent vốn thực thi.
- Bạn giám sát tỷ lệ chuyển lên cấp cao và phân bố tác vụ của chuyên gia để xác nhận các năng lực trọng yếu vẫn được thực hành tích cực.

**Các phản mẫu thường gặp (anti-patterns):**

- Tự động hóa các quy trình lĩnh vực mà không duy trì runbook được ghi chép hay các bài tập thực thi thủ công định kỳ, giảm năng lực vận hành của tổ chức khi các hệ thống Agent không khả dụng.
- Chạy các Agent mà không có ranh giới rõ ràng giữa hành động tự chủ và giám sát của con người, tạo ra các trường hợp mà Agent đưa ra các quyết định nhiều rủi ro vốn nên được định tuyến tới các chuyên gia.
- Mở rộng áp dụng Agent mà không có kế hoạch nhân lực để bảo tồn các kỹ năng trọng yếu, nên các lợi ích năng suất ngắn hạn làm xói mòn năng lực tổ chức dài hạn.
- Coi việc chuyển lên cấp cao như một ngoại lệ thay vì một kết quả kỳ vọng, nên các đường bàn giao giữa Agent và chuyên gia con người bị kiểm thử thiếu và thất bại khi cần đến nhất.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tổ chức giữ được năng lực vận hành thủ công khi các hệ thống Agent không khả dụng hoặc gặp các tình huống vượt khỏi phạm vi huấn luyện của chúng.
- Chuyên môn trọng yếu vẫn sẵn có cho việc onboarding, các trường hợp biên và các quy trình kinh doanh đang tiến hóa mà tự động hóa chưa theo kịp.
- Việc áp dụng đi đúng nhịp với khả năng duy trì giám sát của tổ chức, thay vì chạy vượt lên trước nó.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Câu hỏi ngưỡng là năng lực nào phải ở lại với con người và năng lực nào có thể chuyển sang Agent hoặc tự động hóa. Một phân loại ba tầng — con-người-sở-hữu, Agent-tăng-cường và tự-động-hóa-hoàn-toàn — cho các nhóm một vốn từ chung cho quyết định đó. Các tiêu chí phân loại quan trọng hơn các nhãn:

- Con-người-sở-hữu nghĩa là các quyết định nơi dung sai lỗi thấp và ngữ cảnh biến thiên cao (phán đoán quy định, chuyển lên cấp cao của khách hàng, và các đánh đổi chiến lược)
- Agent-tăng-cường nghĩa là công việc nơi Agent tăng tốc đầu ra của con người nhưng con người vẫn là người ra quyết định (review mã, soạn thảo tài liệu, và phân tích dữ liệu)
- Tự-động-hóa-hoàn-toàn nghĩa là các tác vụ thường quy nơi độ chính xác của Agent vượt quá chi phí của lỗi (định tuyến, phân loại, và xử lý biểu mẫu chuẩn)

Việc phân loại được rà soát khi năng lực Agent cải thiện và khi các ưu tiên tổ chức dịch chuyển.

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với Policies và code interceptor có thể gọi các quy trình có-con-người-trong-vòng-lặp (human-in-the-loop) dựa trên các ngưỡng độ phức tạp, điểm tin cậy (confidence score) hoặc đánh giá mức rủi ro. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) thực thi các ranh giới quyết định để các trường hợp nhiều rủi ro tự động chuyển lên cấp cao thay vì phụ thuộc vào việc Agent tự báo cáo độ tin cậy thấp. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy đầu ra Agent đối chiếu với các đường cơ sở do chuyên gia tạo, đây là cách bạn phát hiện sự trôi dạt (drift) trong các danh mục mà Agent từng được tin cậy nhưng giờ đang suy giảm.

Việc tự động hóa loại bỏ một tác vụ khỏi quy trình của chuyên gia cũng loại bỏ luôn sự thực hành vốn giữ cho chuyên môn sắc bén. Các chương trình luân phiên phân công các chuyên gia xử lý một phần các trường hợp một cách thủ công trên cơ sở định kỳ. Với các năng lực trọng yếu về mặt kinh doanh, một mức tối thiểu xác định (một phần trăm các trường hợp mỗi quý, một ca hàng tuần, hoặc một workshop hàng tháng) giữ cho sự thực hành luôn tích cực. Ghi chép runbook cho các quy trình mà Agent giờ thực thi để đường thủ công vẫn khả thi khi đường tự động không khả dụng. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) theo dõi tỷ lệ chuyển lên cấp cao và phân bố tác vụ, cho thấy liệu các chuyên gia có được giữ trong vòng lặp đủ thường xuyên để duy trì sự sắc bén hay không.

### Các bước triển khai

- **Định nghĩa một phân loại năng lực:** Phân loại các kỹ năng tổ chức thành các tầng con-người-sở-hữu, Agent-tăng-cường và tự-động-hóa-hoàn-toàn với các tiêu chí được ghi chép và một nhịp rà soát.
- **Cấu hình việc chuyển lên cấp cao tự động:** Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) Policies và [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) để định tuyến các quyết định nhiều rủi ro, mơ hồ hoặc độ tin cậy thấp tới các chuyên gia con người.
- **Thiết lập các chương trình luân phiên:** Phân công các chuyên gia lĩnh vực xử lý một phần trăm các trường hợp xác định một cách thủ công mỗi quý cho các năng lực trọng yếu với khả năng phục hồi của doanh nghiệp, và duy trì runbook cho việc thực thi thủ công.
- **Xác thực đầu ra Agent đối chiếu với các đường cơ sở của chuyên gia:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đối chiếu với các đường cơ sở do chuyên gia lĩnh vực tạo để phát hiện sự trôi dạt trong các danh mục đã được tin cậy giao cho tự động hóa.
- **Giám sát việc chuyển lên cấp cao và phân bố tác vụ:** Theo dõi tỷ lệ chuyển lên cấp cao và phân bố tác vụ của chuyên gia qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để xác nhận các năng lực trọng yếu vẫn được thực hành tích cực.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS03-BP02 Xây dựng các Agent phản chiếu các kỹ năng và năng lực tổ chức của bạn](agentsus03-bp02.md)
- [AGENTSUS03-BP03 Duy trì các đặc tả toàn diện cho Agent và hệ thống dạng tác nhân](agentsus03-bp03.md)
- [MLPERF06-BP01 Include human-in-the-loop monitoring](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/mlperf-06.html)

**Các tài liệu liên quan:**

- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Human-in-the-loop (HITL) - Amazon Nova Act](https://docs.aws.amazon.com/nova/latest/userguide/nova-act-hitl.html)
- [Build reliable AI agents with Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)

**Các ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
