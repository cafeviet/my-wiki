# AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân

Telemetry ở ranh giới yêu cầu không thể phân biệt biến động bình thường với sự suy giảm thực. Telemetry ở cấp giai đoạn qua toàn bộ vòng đời xử lý cho người vận hành tín hiệu họ cần để kích hoạt suy giảm nhẹ nhàng vào đúng thời điểm thay vì quá sớm hoặc quá muộn.

**Kết quả mong muốn:**

- Bạn có telemetry ở cấp giai đoạn qua truy xuất ngữ cảnh, suy luận mô hình, thực thi công cụ và sinh phản hồi.
- Bạn bắt dữ liệu đặc thù LLM, số lượng token, độ trễ suy luận, lý do kết thúc (finish reason), trên mọi lần gọi mô hình.
- Bạn có các bảng điều khiển CloudWatch với các widget ở cấp giai đoạn và các cảnh báo tổng hợp dẫn dắt việc kích hoạt suy giảm tự động.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai telemetry chỉ ở ranh giới yêu cầu mà không trang bị công cụ cho từng giai đoạn xử lý.
- Bỏ qua telemetry đặc thù LLM, số lượng token, độ trễ suy luận, chất lượng đầu ra. Đó là điều thiết yếu để phát hiện sự suy giảm liên quan đến mô hình.
- Coi telemetry như một mối quan tâm sau-triển-khai thay vì thiết kế nó vào kiến trúc ngay từ đầu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phát hiện suy giảm chính xác vì telemetry bao phủ mọi giai đoạn xử lý.
- Các quyết định suy giảm có căn cứ từ việc giai đoạn nào thực sự đang chịu áp lực.
- Phản ứng sự cố nhanh hơn thông qua các bảng điều khiển dựng sẵn phơi bày các tín hiệu ngay lập tức.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bắt telemetry đặc thù cho tác nhân thông qua trang bị công cụ tương thích OpenTelemetry. Điều này bao gồm các vết gọi công cụ, chi tiết tương tác với mô hình và các mẫu truy cập bộ nhớ. Trang bị công cụ ở cấp giai đoạn là điều phân biệt cái này với ghi log yêu cầu chung chung. Một số liệu độ trễ đơn lẻ ở ranh giới yêu cầu không thể cho bạn biết sự chậm chạp đến từ truy xuất, suy luận, thực thi công cụ hay phân tích cú pháp phản hồi.

Telemetry đặc thù LLM xứng đáng được nhấn mạnh riêng. Bật [ghi log gọi mô hình Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) để bắt dữ liệu yêu cầu và phản hồi đầy đủ cho mọi lần gọi LLM, bao gồm số lượng token, độ trễ và lý do kết thúc. Một sự tăng vọt số lượng token đầu ra hoặc một dịch chuyển trong phân bố lý-do-kết-thúc thường đi trước một thoái lui chất lượng hiện hữu vài giờ. Không có các log, các tín hiệu sớm đó là vô hình.

Tập số liệu cần cấu trúc. Đối với mỗi giai đoạn xử lý, định nghĩa một tập chuẩn. Truy xuất ngữ cảnh theo dõi độ trễ và số lượng kết quả. Suy luận mô hình theo dõi độ trễ, số lượng token và ID mô hình. Thực thi công cụ theo dõi số lần gọi, độ trễ và tỷ lệ lỗi. Sinh phản hồi theo dõi tỷ lệ vượt qua kiểm định đầu ra. Xây dựng các bảng điều khiển Amazon CloudWatch với các widget ở cấp giai đoạn và một tóm tắt sức khỏe tổng hợp để người vận hành có thể thấy toàn bộ vòng đời trong nháy mắt. [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) trên các số liệu chính thiết lập các đường cơ sở tự động, loại bỏ nhu cầu tinh chỉnh ngưỡng thủ công. Các cảnh báo tổng hợp qua nhiều giai đoạn phát hiện các mẫu suy giảm trải qua các ranh giới và kích hoạt việc kích hoạt suy giảm tự động khi tín hiệu sức khỏe tổng hợp tụt xuống.

### Các bước triển khai

- **Bật AgentCore Observability với telemetry ở cấp giai đoạn:** Trang bị công cụ cho truy xuất ngữ cảnh, suy luận, thực thi công cụ và sinh phản hồi. Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập.
- **Bật ghi log gọi mô hình Amazon Bedrock:** Bắt số lượng token, độ trễ và lý do kết thúc cho mọi lần gọi LLM qua [ghi log gọi mô hình Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html).
- **Xây dựng các bảng điều khiển CloudWatch với các widget ở cấp giai đoạn:** Bao gồm một tóm tắt sức khỏe tổng hợp để người vận hành thấy toàn bộ vòng đời trong nháy mắt.
- **Cấu hình CloudWatch Anomaly Detection trên các số liệu chính:** Dùng [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) để mô hình hóa đường cơ sở tự động.
- **Tạo các cảnh báo tổng hợp:** Kết hợp các tín hiệu đa giai đoạn để kích hoạt việc kích hoạt suy giảm tự động.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và tạo điều kiện phục hồi](../7-agentrel07/agentrel07-bp03.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](agentrel08-bp01.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](agentrel08-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Amazon Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
