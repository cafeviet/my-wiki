# AGENTOPS05-BP05 Tạo các dashboard đặc thù luồng công việc cho sức khỏe vận hành

Các dashboard hạ tầng chung có thể che giấu các chỉ số quan trọng đối với các luồng công việc agentic. Một dashboard được thiết kế quanh đường tới hạn (critical path) của một luồng công việc cụ thể, các độ trễ ở cấp bước, và các chế độ lỗi đặc trưng cung cấp chi tiết mà người vận hành cần để nhanh chóng thấy các vấn đề và hiểu nguyên nhân gốc.

**Kết quả mong muốn:**

- Mỗi luồng công việc agent quan trọng có một dashboard chuyên dụng với tầm nhìn thời gian thực vào sức khỏe luồng công việc.
- Người vận hành xác định các vấn đề và nhanh chóng hiểu nguyên nhân gốc.
- Các dashboard được tùy biến theo các đặc tính cụ thể của mỗi luồng công việc, không phải các mẫu chung.
- Các nhóm vận hành sử dụng các dashboard này như công cụ chính cho giám sát luồng công việc và ứng phó sự cố.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng các dashboard hạ tầng chung cho mọi luồng công việc agent, bỏ lỡ các chỉ số đặc thù luồng công việc như tỷ lệ bàn giao thành công, số vòng lặp suy luận, và các nút thắt cổ chai ở cấp bước.
- Xây dựng các dashboard mà không liên kết tới các runbook vận hành, buộc người vận hành tìm kiếm cách khắc phục trong lúc sự cố thay vì điều hướng trực tiếp.
- Tạo các dashboard một lần và không bao giờ cập nhật khi các luồng công việc tiến hóa, nên các chỉ số cho các bước không còn tồn tại vẫn hiển thị trong khi các bước mới không được giám sát.
- Xây dựng các dashboard đòi hỏi ngữ cảnh sâu để diễn giải, nên chỉ tác giả gốc mới hiểu được chúng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các dashboard đặc thù luồng công việc bộc lộ các chỉ số và mẫu liên quan nhất tới các đặc tính vận hành và chế độ lỗi của mỗi luồng công việc.
- Các dashboard được tùy biến điều chỉnh độ sâu giám sát theo mức độ quan trọng của mỗi luồng công việc, cung cấp chi tiết cho các luồng công việc quan trọng và tổng quan cho các luồng ít quan trọng hơn.
- Các liên kết runbook được nhúng nén thời gian từ phát hiện đến khắc phục.
- Các chú thích sự kiện triển khai tương quan các thay đổi chỉ số với các thay đổi cấu hình, mang lại cho người vận hành sự quy kết mà không cần đối chiếu chéo các công cụ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một bố cục phổ biến, như bản tóm tắt sức khỏe ở cấp cao (khỏe mạnh, suy giảm, và tới hạn), các chỉ số then chốt dưới dạng biểu đồ chuỗi thời gian (time-series), và các sự kiện và cảnh báo gần đây, nghĩa là người vận hành học mẫu này một lần và áp dụng nó cho mọi dashboard luồng công việc. Mỗi luồng công việc sau đó thêm nội dung cụ thể của nó, như các bước đường tới hạn, thời gian hoàn thành của chúng, tỷ lệ thành công của chúng, và độ sâu hàng đợi của chúng.

Việc xác định đường tới hạn ngay trong dashboard. [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) Contributor Insights xác định các tác nhân hàng đầu gây lỗi và độ trễ một cách thực nghiệm thay vì bằng phỏng đoán, vốn thường chính xác hơn những gì nhóm giả định.

Trực quan hóa trạng thái luồng công việc, sự phân bố các yêu cầu đang xử lý (in-flight) qua các bước, là một góc nhìn bộc lộ các điểm tích tụ. Một bước giữ nhiều yêu cầu hơn kỳ vọng hoặc đang chạy chậm hoặc là cổng trước một lỗi hạ nguồn. Dù thế nào, người vận hành thấy vấn đề mà không phải tái dựng nó từ các chỉ số độ trễ và lỗi riêng rẽ. Các chú thích sự kiện triển khai sau đó gắn các thay đổi chỉ số trở lại các thay đổi cấu hình, nén cuộc điều tra nguyên nhân gốc.

Hãy nhúng các liên kết runbook để giảm thời gian phát hiện và khắc phục các vấn đề. Một người vận hành nhìn vào một dashboard đang suy giảm nên cách một cú nhấp chuột so với runbook cho chế độ lỗi đó. Hãy thiết lập một nhịp rà soát, thường là theo quý, để các dashboard giữ phù hợp với các thay đổi luồng công việc thay vì trôi lệch thành các biểu diễn lỗi thời.

### Các bước triển khai

- **Xác định các luồng công việc xứng đáng có dashboard chuyên dụng:** Dựa danh sách trên tác động kinh doanh và lịch sử sự cố.
- **Thiết kế một bố cục dashboard nhất quán:** Áp dụng cùng mẫu tóm tắt sức khỏe, các chỉ số then chốt, và các sự kiện gần đây cho mọi dashboard luồng công việc.
- **Trực quan hóa đường tới hạn:** Hiển thị độ trễ và tỷ lệ thành công ở cấp bước cho các bước mà các nút thắt cổ chai thường hình thành, dùng [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html) Contributor Insights để xác định các tác nhân hàng đầu một cách thực nghiệm.
- **Chú thích các sự kiện triển khai:** Tương quan các thay đổi chỉ số với các lần triển khai cấu hình để sự quy kết hiển thị trên dashboard.
- **Nhúng các liên kết runbook và rà soát theo quý:** Liên kết mỗi dashboard tới runbook cho các kịch bản lỗi phổ biến, và cập nhật các dashboard khi các luồng công việc thay đổi.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent](agentops05-bp04.md)
- [AGENTOPS05-BP01 Thiết lập truy vết và telemetry đầu-cuối cho hoạt động agent](agentops05-bp01.md)
- [AGENTOPS05-BP02 Giám sát các mẫu hành vi agent và phát hiện bất thường](agentops05-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Observing agentic AI workloads using Amazon CloudWatch](https://aws.amazon.com/blogs/mt/observing-agentic-ai-workloads-using-amazon-cloudwatch/)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
