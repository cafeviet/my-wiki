# AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi

Log chung chung bỏ lỡ điều quan trọng nhất đối với tác nhân: các điểm quyết định, các lời gọi công cụ và các tương tác với LLM. Telemetry có cấu trúc cùng các đường cơ sở hành vi phơi bày bất thường sớm và cho người vận hành vết kiểm toán họ cần để tái dựng lý do vì sao một tác nhân đã làm điều nó đã làm.

**Kết quả mong muốn:**

- Bạn bắt các điểm quyết định, lời gọi công cụ và tương tác với LLM cho mỗi lần gọi tác nhân.
- Bạn có các đường cơ sở hành vi theo từng tác nhân và các cảnh báo tự động kích hoạt khi số liệu trôi khỏi khoảng kỳ vọng.
- Bạn phát hiện độ trôi hành vi thông qua kiểm định định kỳ, không chỉ qua các lỗi hạ tầng.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy ghi log chung chung không bắt các điểm quyết định đặc thù cho tác nhân, khiến các đội không thể hiểu vì sao một tác nhân tạo ra kết quả bất ngờ.
- Vận hành mà không có đường cơ sở hành vi, nên không có cơ sở để quyết định khi nào hành vi của tác nhân thực sự đã sai lệch.
- Chỉ dựa vào rà soát log thủ công, làm chậm việc phát hiện các vấn đề độ tin cậy cho tới khi người dùng phàn nàn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phát hiện bất thường tự động bắt các vấn đề độ tin cậy trước khi chúng lan truyền.
- Sự minh bạch thực thi đầy đủ qua ghi log điểm quyết định đẩy nhanh phân tích nguyên nhân gốc.
- Các vết kiểm toán có cấu trúc tái dựng quá trình ra quyết định của tác nhân phục vụ tuân thủ và gỡ lỗi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Giám sát hành vi bắt đầu bằng việc bắt đường thực thi, không phải phản hồi cuối cùng. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp telemetry tương thích OpenTelemetry bao phủ toàn bộ đường của mỗi lần gọi tác nhân, từ yêu cầu ban đầu qua suy luận LLM, lời gọi công cụ, truy cập bộ nhớ, đến sinh phản hồi. Gắn thẻ (tag) các vết (trace) với siêu dữ liệu đặc thù cho tác nhân như ID tác nhân, loại tác vụ, mô hình sử dụng và các lời gọi công cụ đã thực hiện, để việc lọc và phân tích nhắm đúng tác nhân hoặc kịch bản lỗi quan tâm.

Telemetry thô là cần thiết nhưng chưa đủ. Bật [ghi log gọi mô hình Amazon Bedrock (model invocation logging)](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) để bắt mọi yêu cầu và phản hồi của LLM, bao gồm prompt, tham số mô hình, số lượng token và độ trễ. Không có chiều sâu đó, việc tái dựng "vì sao tác nhân chọn công cụ này" chỉ còn là đoán mò từ số liệu tổng hợp.

Thu thập các số liệu đặc thù cho tác nhân trong một khoảng thời gian đại diện, bao gồm tần suất gọi công cụ, phân bố số lượng token đầu ra, tỷ lệ hoàn thành tác vụ và tỷ lệ lỗi theo loại. Áp dụng [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) để hệ thống học khoảng kỳ vọng thay vì dựa vào các ngưỡng cố định. Cấu hình cảnh báo trên các dải phát hiện bất thường. Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để đánh giá định kỳ hành vi của tác nhân theo các chuẩn chất lượng, để độ trôi hành vi không biểu hiện thành lỗi hạ tầng vẫn được bắt.

### Các bước triển khai

- **Bật AgentCore Observability trên mọi lần gọi:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với truy vết OpenTelemetry và gắn thẻ các vết với siêu dữ liệu đặc thù cho tác nhân.
- **Bắt dữ liệu yêu cầu/phản hồi LLM đầy đủ:** Bật [ghi log gọi mô hình Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) để phân tích bất thường và kiểm toán.
- **Thiết lập các đường cơ sở hành vi:** Thu thập các số liệu đặc thù cho tác nhân đại diện và áp dụng [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) để các ngưỡng được học thay vì tinh chỉnh thủ công.
- **Cấu hình cảnh báo trên các dải phát hiện bất thường:** Kích hoạt các luồng điều tra khi số liệu trôi khỏi khoảng kỳ vọng.
- **Chạy AgentCore Evaluations theo nhịp định kỳ:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để phát hiện độ trôi hành vi theo các chuẩn chất lượng, không chỉ các tín hiệu hạ tầng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL02-BP01 Thiết kế các tác nhân cho các tác vụ cụ thể và nguyên tử](agentrel02-bp01.md)
- [AGENTREL02-BP02 Giới hạn quyền hạn của tác nhân ở mức truy cập tối thiểu cần thiết](agentrel02-bp02.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](../8-agentrel08/agentrel08-bp02.md)
- [AGENTCOST07-BP02 Establish proactive anomaly detection for agent cost patterns](../../5-cost-optimization/7-agentcost07/agentcost07-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Amazon Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
