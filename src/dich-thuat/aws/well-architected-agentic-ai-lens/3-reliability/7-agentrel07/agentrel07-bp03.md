# AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và tạo điều kiện phục hồi

Tương quan log qua các dịch vụ bằng tay là chậm, và trong một sự cố thì chậm còn tệ hơn đắt. Truy vết phân tán qua mọi thành phần với các chú thích đặc thù cho tác nhân cho người vận hành toàn bộ đường yêu cầu trong một góc nhìn và biến các lần khởi động lại diện rộng thành các hành động phục hồi có mục tiêu.

**Kết quả mong muốn:**

- Bạn có truy vết phân tán qua mọi thành phần tác nhân với các chú thích đặc thù cho tác nhân.
- Bạn lan truyền bối cảnh vết qua các ranh giới giao tiếp đồng bộ và bất đồng bộ.
- Bạn tương quan các vết, số liệu và log trong một góc nhìn hợp nhất phơi bày các nguyên nhân gốc nhanh chóng.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ truy vết ở ranh giới ứng dụng mà không lan truyền bối cảnh qua các lời gọi dịch vụ nội bộ.
- Bỏ qua việc tương quan các vết với log và số liệu, làm giảm khả năng phân tích hợp nhất trong các sự cố.
- Bỏ qua các chú thích đặc thù cho tác nhân giúp lọc theo ID tác nhân, loại tác vụ hoặc mô hình sử dụng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các nguyên nhân gốc nổi lên nhanh chóng vì luồng yêu cầu quan sát được đầu-tới-cuối.
- Thời gian trung bình để phục hồi (MTTR) giảm vì dữ liệu vết dẫn dắt các hành động có mục tiêu thay vì các lần khởi động lại diện rộng.
- Các nút thắt cổ chai về độ trễ trở nên hiện hữu, cho phép tối ưu hiệu năng một cách chủ động.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bắt toàn bộ đường thực thi của mỗi lần gọi tác nhân thông qua telemetry tương thích OpenTelemetry. Bật nó qua mọi thành phần tác nhân, không chỉ ranh giới ngoài, để vết thực sự trải dài yêu cầu đầu-tới-cuối. Không có độ phủ ở cấp thành phần, các vết có các khoảng trống nơi công việc vô hình diễn ra, và đó chính xác là nơi việc gỡ lỗi chậm lại trong một sự cố.

Các chú thích là điều làm cho các vết tìm kiếm được ở quy mô của các hệ thống thực. Các thẻ đặc thù cho tác nhân, ID tác nhân, loại tác vụ, ID mô hình, ID luồng công việc, cho phép bạn lọc các vết xuống một tác nhân cụ thể hoặc kịch bản lỗi thay vì grep qua một luồng không phân biệt. Trang bị công cụ cho các vết ở cấp khung của Strands Agents để bắt các bước suy luận, các lời gọi công cụ và kết quả của chúng trong một góc nhìn vết hợp nhất, vì các quyết định nội bộ của tác nhân là nơi hầu hết các tín hiệu thú vị cư ngụ.

Lan truyền bối cảnh là chi tiết quyết định liệu các đường bất đồng bộ có quan sát được hay không. Đối với giao tiếp dựa trên hàng đợi, lan truyền các header vết qua các thuộc tính thông điệp để các vết tiếp tục qua các ranh giới hàng đợi. Không có lan truyền, vết kết thúc ở bên sản xuất và một vết mới bắt đầu ở bên tiêu thụ, và sự kiện rằng chúng liên quan với nhau bị mất. Tạo cảnh báo dựa trên vết qua Amazon CloudWatch tương quan các vết, số liệu và log trong một góc nhìn hợp nhất, để một bất thường vết, một tăng vọt số liệu và một lỗi log xuất hiện cùng nhau thay vì riêng lẻ.

### Các bước triển khai

- **Bật AgentCore Observability với truy vết OpenTelemetry:** Bật [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) qua mọi thành phần tác nhân.
- **Thêm các chú thích đặc thù cho tác nhân:** Gắn thẻ các vết với ID tác nhân, loại tác vụ và ID mô hình để có thể lọc trong các sự cố.
- **Lan truyền bối cảnh vết qua các ranh giới:** Bao gồm các đường đồng bộ và bất đồng bộ, với các thuộc tính thông điệp cho giao tiếp dựa trên hàng đợi.
- **Trang bị công cụ cho các vết ở cấp khung của Strands Agents:** Bắt các bước suy luận và các lời gọi công cụ trong góc nhìn vết hợp nhất.
- **Tạo các bảng điều khiển CloudWatch tương quan các vết, số liệu và log:** Xây dựng một góc nhìn hợp nhất để phản ứng sự cố dựa trên tín hiệu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL07-BP01 Thiết kế luồng công việc theo giai đoạn với phục hồi tăng dần](agentrel07-bp01.md)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi của tác nhân](agentrel07-bp02.md)
- [AGENTREL08-BP02 Triển khai truy vết tác nhân cho telemetry xuyên suốt quá trình xử lý của tác nhân](../8-agentrel08/agentrel08-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Strands Agents Traces](https://strandsagents.com/docs/user-guide/observability-evaluation/traces/)

**Video liên quan:**

- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)
- [AWS re:Invent 2024 - Observability for Reliable Agentic AI with Strands & OpenTelemetry (NTA406)](https://www.youtube.com/watch?v=qJxF4XfMLhk)
- [AWS re:Invent 2024 - Build observable AI agents with Strands, AgentCore, and Datadog (AIM233)](https://www.youtube.com/watch?v=mOAd8grR1BU)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore - Observability](https://catalog.workshops.aws/agentcore-deep-dive/en-US/70-agentcore-observability)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
