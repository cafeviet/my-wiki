# AGENTREL08-BP04 Theo dõi các số liệu sử dụng bộ nhớ của tác nhân

Sự cạn kiệt bộ nhớ tạo ra các tác nhân trông có vẻ khỏe mạnh nhưng thiếu ngữ cảnh để suy luận tốt. Theo dõi mức sử dụng qua các tầng ngắn hạn, dài hạn và trong ngữ cảnh phơi bày áp lực trước khi các lỗi âm thầm bắt đầu.

**Kết quả mong muốn:**

- Bạn theo dõi số lượng token theo từng thành phần ngữ cảnh và phát ra các tỷ lệ phần trăm sử dụng cửa sổ ngữ cảnh.
- Bạn có các cảnh báo khi mức sử dụng cửa sổ ngữ cảnh vượt 80%, kích hoạt các luồng tóm tắt hoặc tỉa (pruning).
- Bạn phát hiện các xu hướng tăng trưởng bộ nhớ qua metric math để các rò rỉ dần dần nổi lên trước khi chúng gây ra lỗi.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ giám sát các số liệu bộ nhớ ở cấp hạ tầng mà không theo dõi các mẫu đặc thù cho tác nhân như mức sử dụng cửa sổ ngữ cảnh và sự tăng trưởng trạng thái phiên.
- Vận hành mà không có các đường cơ sở cho mức tiêu thụ bộ nhớ bình thường, khiến sự tăng trưởng bất thường không phát hiện được.
- Bỏ qua mức sử dụng bộ nhớ trong ngữ cảnh, chỉ báo trực tiếp nhất về sự suy giảm liên quan đến ngữ cảnh.

**Lợi ích khi áp dụng thực hành tốt này:**

- Áp lực bộ nhớ được phát hiện sớm qua giám sát liên tục trước khi sự cạn kiệt gây ra lỗi.
- Các quyết định suy giảm có căn cứ từ việc tầng bộ nhớ nào thực sự đang chịu áp lực.
- Các lỗi liên quan đến bộ nhớ âm thầm được ngăn ngừa vì mức sử dụng trong ngữ cảnh được giám sát một cách chủ động.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Bộ nhớ trong ngữ cảnh là nơi các lỗi âm thầm bắt đầu. Khi cửa sổ ngữ cảnh lấp đầy với ngữ cảnh được truy xuất, lịch sử hội thoại và kết quả công cụ, mô hình có ít chỗ hơn cho thông tin mới và năng lực suy luận hữu hiệu của nó sụt xuống. Theo dõi mức sử dụng theo từng thành phần (system prompt, ngữ cảnh được truy xuất, lịch sử hội thoại, kết quả công cụ) qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cho bạn biết thành phần nào đang tạo ra áp lực. Các cảnh báo khi mức sử dụng vượt 80% cửa sổ ngữ cảnh của mô hình kích hoạt các luồng tóm tắt hoặc tỉa trước khi giới hạn trở thành một bức tường cứng. Để đo token chính xác với các mô hình Anthropic trên Amazon Bedrock, dùng [đếm token của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/count-tokens.html). Đối với các nhà cung cấp khác, ước lượng xấp xỉ là đủ tốt cho mục đích đường cơ sở.

Các kho bộ nhớ bên ngoài là nơi khác mà áp lực biểu hiện. Giám sát độ trễ truy cập và tỷ lệ lỗi của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) qua AgentCore Observability, và theo dõi các số liệu ở cấp hạ tầng qua Amazon CloudWatch. Độ trễ tăng lên trên truy cập bộ nhớ thường là tín hiệu đầu tiên cho thấy kho đang chịu áp lực, khá lâu trước khi nó thực sự lỗi.

Phân tích xu hướng tăng trưởng bắt các rò rỉ mà các số liệu ở cấp hạ tầng bỏ lỡ. Dùng [Amazon CloudWatch Metric Math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html) để tính các tốc độ tăng trưởng trên các cửa sổ cấu hình được và cảnh báo khi tốc độ vượt đường cơ sở. Sự tăng trưởng tăng dần đều đặn hiếm khi kích hoạt một cảnh báo ngưỡng nhưng thường chỉ ra một rò rỉ mà cuối cùng sẽ làm cạn kiệt bộ nhớ. Xây dựng các phản hồi quản lý bộ nhớ tự động cho mỗi tầng. Áp dụng tóm tắt ngữ cảnh cho áp lực trong ngữ cảnh, tỉa phiên cho áp lực bộ nhớ ngắn hạn, và hợp nhất bộ nhớ cho áp lực bộ nhớ dài hạn.

### Các bước triển khai

- **Theo dõi mức sử dụng bộ nhớ trong ngữ cảnh theo từng thành phần:** Đo số lượng token cho system prompt, ngữ cảnh được truy xuất, lịch sử hội thoại và kết quả công cụ. Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để thu thập.
- **Cấu hình các cảnh báo tại 80% mức sử dụng cửa sổ ngữ cảnh:** Kích hoạt các luồng tóm tắt hoặc tỉa trước khi giới hạn trở thành một bức tường cứng.
- **Giám sát độ trễ truy cập và tỷ lệ lỗi của AgentCore Memory:** Bắt áp lực kho bên ngoài sớm qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).
- **Triển khai phân tích xu hướng tăng trưởng bộ nhớ:** Dùng [Amazon CloudWatch Metric Math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html) để phát hiện các rò rỉ dần dần không kích hoạt các cảnh báo ngưỡng.
- **Xây dựng các phản hồi quản lý bộ nhớ tự động:** Triển khai các phản hồi tóm tắt, tỉa và hợp nhất theo từng tầng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP04 Triển khai suy giảm nhẹ nhàng cho các thao tác bộ nhớ và trạng thái](../3-agentrel03/agentrel03-bp04.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](agentrel08-bp01.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](agentrel08-bp02.md)
- [AGENTREL08-BP03 Kiến trúc hệ thống tác nhân với cô lập tài nguyên và giảm thiểu tranh chấp](agentrel08-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock token counting](https://docs.aws.amazon.com/bedrock/latest/userguide/count-tokens.html)
- [Amazon CloudWatch Metric Math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
