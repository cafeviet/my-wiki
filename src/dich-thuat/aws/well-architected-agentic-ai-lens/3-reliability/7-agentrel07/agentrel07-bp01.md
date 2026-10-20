# AGENTREL07-BP01 Thiết kế luồng công việc theo giai đoạn với phục hồi tăng dần

Các luồng công việc đơn khối mất tất cả khi một lỗi đơn lẻ xảy ra. Ranh giới giai đoạn tường minh với đầu ra được lưu bền kiềm chế các lỗi ở giai đoạn bị ảnh hưởng và cho phép việc phục hồi bắt đầu từ điểm kiểm tra hoàn tất gần nhất thay vì từ đầu.

**Kết quả mong muốn:**

- Bạn có các luồng công việc được phân rã thành các giai đoạn rời rạc tại các điểm kiểm tra tự nhiên nơi công việc đã hoàn tất có giá trị độc lập.
- Bạn lưu bền các đầu ra giai đoạn một cách bền vững để việc phục hồi tiếp tục từ giai đoạn hoàn tất gần nhất.
- Bạn kiểm định các đầu ra giai đoạn trước khi tiến tới để các lỗi không lan truyền âm thầm qua các giai đoạn sau.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các luồng công việc như các tiến trình đơn khối không có ranh giới giai đoạn, nên bất kỳ lỗi nào cũng buộc khởi động lại hoàn toàn.
- Định nghĩa các giai đoạn ở mức chi tiết quá thô, làm mất một lượng lớn công việc bên trong một giai đoạn khi nó lỗi.
- Bỏ qua kiểm định đầu ra giai đoạn, cho phép các lỗi lan truyền qua các giai đoạn sau.

**Lợi ích khi áp dụng thực hành tốt này:**

- Mất công việc giữ ở mức tối thiểu vì việc phục hồi tiếp tục từ giai đoạn hoàn tất gần nhất.
- Phục hồi nhanh hơn vì tránh được việc tính toán lại thừa các giai đoạn đã hoàn tất.
- Ranh giới giai đoạn kiềm chế các lỗi, cải thiện việc cô lập lỗi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) lưu bền trạng thái thực thi tại mỗi chuyển tiếp trạng thái và cho phép phục hồi từ bước hoàn tất gần nhất thay vì khởi động lại toàn bộ. Cơ chế thử lại với exponential backoff tích hợp sẵn xử lý các lỗi thoáng qua bên trong một bước, và khả năng redrive khởi động lại luồng công việc từ điểm lỗi mà không thực thi lại các bước đã hoàn tất. Sự kết hợp này, lưu bền cộng thử lại có chọn lọc cộng redrive, là điều mang lại sức mạnh cho phục hồi tăng dần. [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cung cấp bề mặt thực thi cho từng bước tác nhân bên trong luồng công việc.

Đặt các ranh giới giai đoạn ở nơi công việc đã hoàn tất có giá trị độc lập. Một tài liệu đã phân tích cú pháp, một truy vấn đã kiểm định, và một ngữ cảnh đã truy xuất và tóm tắt đều là các ranh giới tự nhiên. Nếu một giai đoạn tạo ra một hiện vật nửa vời vô dụng khi đứng một mình, thì ranh giới đang ở sai chỗ.

Bảo vệ chất lượng bám theo thiết kế giai đoạn. Kiểm định đầu ra giai đoạn giữa các giai đoạn, kiểm tra sự tuân thủ lược đồ và các ngưỡng chất lượng trước khi tiến tới, giữ cho các lỗi không lan truyền. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) có thể kiểm tra rằng các đầu ra luồng công việc được phục hồi khớp với các đường cơ sở chất lượng trước-khi-lỗi, để phục hồi tăng dần không âm thầm làm giảm chất lượng. Các timeout ở cấp giai đoạn ngăn các giai đoạn bị kẹt chặn tiến độ vô thời hạn. Các số liệu ở cấp giai đoạn qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), bao gồm tỷ lệ thành công, thời gian thực thi và tần suất timeout, nhận diện các giai đoạn cần tối ưu.

### Các bước triển khai

- **Phân rã các luồng công việc thành các giai đoạn rời rạc:** Đặt các ranh giới tại các điểm kiểm tra tự nhiên nơi công việc đã hoàn tất có giá trị độc lập.
- **Triển khai với Step Functions cho trạng thái bền vững:** Dùng [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) với thử lại và exponential backoff tích hợp sẵn cho mỗi bước.
- **Cấu hình redrive để phục hồi từ điểm lỗi:** Khởi động lại các luồng công việc lỗi mà không thực thi lại các bước đã hoàn tất.
- **Triển khai kiểm định đầu ra giai đoạn:** Kiểm tra sự tuân thủ lược đồ và các ngưỡng chất lượng giữa các giai đoạn để các lỗi không lan truyền.
- **Cấu hình các timeout ở cấp giai đoạn với các đường phục hồi:** Xử lý các giai đoạn lỗi sau khi cạn kiệt các lần thử lại.
- **Giám sát các số liệu ở cấp giai đoạn:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để tìm các giai đoạn cần tối ưu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL03-BP03 Triển khai quản lý trạng thái toàn diện và phục hồi dựa trên điểm kiểm tra](../3-agentrel03/agentrel03-bp03.md)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi của tác nhân](agentrel07-bp02.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và tạo điều kiện phục hồi](agentrel07-bp03.md)

**Tài liệu liên quan:**

- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Planning for failure: How to make generative AI workloads more resilient](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)

**Video liên quan:**

- [AWS 2025 - AgentCore now GA: From Prototype to Production](https://www.youtube.com/watch?v=WyGK8UcAxKo)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
