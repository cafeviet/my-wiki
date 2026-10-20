# AGENTCOST03-BP03 Triển khai lưu bền trạng thái và quản lý vòng đời tối ưu chi phí

Trạng thái agent tăng nhanh khi mỗi bước suy luận kích hoạt một checkpoint, và nó tồn tại mãi mãi khi không có chính sách vòng đời loại bỏ nó. Lưu trạng thái tại các điểm quyết định có ý nghĩa, phân tầng theo mẫu truy cập, và tự động hóa lưu trữ giữ được khả năng phục hồi mà không phải trả tiền cho một tồn đọng ngày càng lớn của các phiên lỗi thời.

**Kết quả mong muốn:**

- Bạn checkpoint tại các điểm quyết định có ý nghĩa thay vì sau mỗi bước suy luận.
- Bạn có trạng thái phiên được phân tầng theo mẫu truy cập, với lưu trữ hiệu năng cao dành cho công việc hoạt động.
- Bạn có các chính sách vòng đời tự động lưu trữ hoặc xóa ngữ cảnh lỗi thời.
- Bạn theo dõi chi phí lưu trữ theo từng agent và phiên, với cảnh báo cho tăng trưởng bất ngờ.

**Các phản mẫu thường gặp (anti-patterns):**

- Checkpoint sau mỗi bước suy luận với các ghi đồng bộ trong khi checkpoint bất đồng bộ tại các điểm quyết định có ý nghĩa đã đủ.
- Giữ toàn bộ trạng thái phiên trên lưu trữ hiệu năng cao bất kể mức độ hoạt động, trả chi phí không cần thiết cho các phiên không hoạt động hoặc đã lưu trữ.
- Cho phép bộ nhớ agent tích lũy vô hạn mà không lưu trữ hoặc xóa, tạo ra tăng trưởng lưu trữ không giới hạn.
- Lưu trạng thái agent không nén trong khi nén có thể giảm chi phí lưu trữ theo tỷ lệ.
- Triển khai lưu bền trạng thái mà không giám sát chi phí, che giấu các mẫu chi phí cao và các cơ hội tối ưu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản lý vòng đời tự động giúp ngăn tăng trưởng lưu trữ không giới hạn mà không cần can thiệp thủ công qua hàng nghìn phiên.
- Bộ nhớ được quản lý tách việc học bền vững khỏi trạng thái phù du, giữ kiến thức cải thiện hiệu năng agent trong khi dọn dẹp các tạo tác tạm thời.
- Cấu hình timeout phiên cân bằng khả năng đáp ứng với chi phí bằng cách kiểm soát vòng đời tính toán.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cung cấp một hệ thống tệp bền vững tự động xử lý lưu trữ theo tầng và vòng đời. Hệ thống tệp sống sót qua các chu kỳ dừng và tiếp tục phiên tới 14 ngày không hoạt động trước khi tự động xóa, và hai tham số vòng đời định hình chi phí là idleRuntimeSessionTimeout (mặc định 15 phút) và maxLifetime (tới 8 giờ). Mặc định 15 phút phù hợp cho các workload tương tác, trong khi các timeout dài hơn giảm các chuyển tiếp trạng thái phiên cho các workload theo lô. Lưu trữ phiên tự động đồng bộ các ghi hệ thống tệp tới lưu trữ bền vững xuyên suốt vòng đời phiên, với dữ liệu được xả ra trong lúc tắt máy có trật tự khi các phiên dừng.

Hãy đưa ra một lựa chọn thiết kế có chủ đích về việc checkpoint. Với các use case cần các checkpoint tường minh tại các điểm quyết định do ứng dụng định nghĩa, hãy triển khai logic checkpoint tùy chỉnh ghi các ảnh chụp trạng thái vào hệ thống tệp bền vững. Khoảng cách checkpoint là một sự đánh đổi giữa độ chi tiết phục hồi và mức tiêu thụ lưu trữ: các checkpoint thường xuyên hơn cho phép phục hồi chi tiết hơn nhưng tăng chi phí lưu trữ. Một số framework agent cung cấp các khả năng checkpoint tích hợp sẵn dùng cùng hệ thống tệp, tránh việc phát minh lại mẫu.

Hãy cân nhắc cách bạn thực hiện việc học bền vững. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) lưu bền các hiểu biết xuyên các phiên (bộ nhớ ngắn hạn cho các tương tác gần đây, bộ nhớ dài hạn cho việc học đã hợp nhất), điều này khác với trạng thái hệ thống tệp theo từng phiên. Với việc lưu giữ tuân thủ vượt quá cửa sổ hệ thống tệp Runtime 14 ngày, hãy xuất dữ liệu phiên đã hoàn thành sang [Amazon S3](https://aws.amazon.com/s3/) với Intelligent-Tiering được bật, và cấu hình các quy tắc vòng đời cho lưu trữ dài hạn tiết kiệm chi phí. Giám sát mức tiêu thụ theo từng loại agent bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với các chiều tùy chỉnh, và đặt cảnh báo Amazon CloudWatch khi tăng trưởng vượt quá các giới hạn kỳ vọng.

### Các bước triển khai

- **Triển khai trên AgentCore Runtime với các tham số vòng đời đã tinh chỉnh:** Dùng [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) để quản lý vòng đời phiên tự động, cấu hình idleRuntimeSessionTimeout và maxLifetime dựa trên các mẫu workload.
- **Tích hợp bộ nhớ được quản lý cho việc học bền vững:** Cấu hình bộ nhớ ngắn hạn của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho ngữ cảnh gần đây và bộ nhớ dài hạn cho các hiểu biết bền vững, giữ việc học bền vững tách khỏi trạng thái hệ thống tệp phù du.
- **Lưu trữ các phiên yêu cầu tuân thủ sang S3:** Xuất các lịch sử phiên đã hoàn thành sang [Amazon S3 Intelligent-Tiering](https://aws.amazon.com/s3/storage-classes/intelligent-tiering/) và đặt các quy tắc vòng đời cho việc lưu giữ dài hạn tiết kiệm chi phí.
- **Giám sát lưu trữ theo từng loại agent:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với các chiều tùy chỉnh để theo dõi chi phí lưu trữ theo từng loại agent, và đặt cảnh báo Amazon CloudWatch cho tăng trưởng lưu trữ bất ngờ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST03-BP01 Thiết kế các hệ thống truy xuất tiết kiệm chi phí với bộ nhớ theo tầng](agentcost03-bp01.md)
- [AGENTCOST03-BP02 Tối ưu chi phí thông qua nén và cắt tỉa cửa sổ ngữ cảnh một cách thông minh](agentcost03-bp02.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime Sessions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon S3 Intelligent-Tiering](https://aws.amazon.com/s3/storage-classes/intelligent-tiering/)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime advanced concepts](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime/03-advanced-concepts)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
