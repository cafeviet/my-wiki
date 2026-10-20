# AGENTPERF06-BP03 Tối ưu sử dụng meta-tool và chuỗi hóa Tools

Các **meta-tool** cho các tác nhân hoàn thành trong một bước suy luận điều mà lẽ ra phải mất năm bước. Với các tác vụ đòi hỏi một chuỗi lệnh gọi **Tools** có thể dự đoán, một meta-tool kết hợp toàn bộ chuỗi thành một thao tác phía-máy-chủ duy nhất và trả về kết quả cuối trong một vòng lặp suy luận thay vì nhiều, cắt cả **latency** lẫn chi phí **Token** bằng cách loại các bước suy luận trung gian.

**Kết quả mong muốn:**

- Bạn có các chuỗi Tools đa-bước phổ biến được đóng gói dưới dạng các meta-tool thực thi toàn bộ chuỗi trong một vòng lặp suy luận tác nhân duy nhất.
- Bạn có các tác nhân dùng meta-tool cho các thao tác thường quy và các Tools riêng lẻ cho các tác vụ mới lạ hoặc không thể dự đoán.
- Bạn có hiệu năng meta-tool được giám sát để xác nhận rằng thao tác hợp thành nhanh hơn chuỗi các lệnh gọi Tools riêng lẻ tương đương.

**Các phản mẫu thường gặp (anti-patterns):**

- Đòi hỏi tác nhân thực hiện các lệnh gọi Tool riêng lẻ cho mọi bước của một chuỗi có thể dự đoán (ví dụ tìm kiếm, truy xuất, phân tích, và định dạng), tiêu nhiều vòng lặp suy luận cho điều lẽ ra có thể là một lần gọi meta-tool duy nhất.
- Tạo các meta-tool quá phức tạp cố xử lý quá nhiều biến thể, trở nên khó bảo trì và chậm hơn các Tools riêng lẻ cho các trường hợp biên.
- Bỏ qua meta-tool cho các chuỗi Tools lặp lại thường xuyên, buộc các tác nhân khám-phá-lại và thực-thi-lại cùng chuỗi Tools trên mọi lần xảy ra.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các meta-tool gộp các chuỗi đa-bước thành các lần gọi duy nhất giảm các lệnh gọi suy luận LLM.
- Loại các vòng lặp suy luận trung gian giảm latency và chi phí token.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Thấp

## Hướng dẫn triển khai

Phân tích telemetry tác nhân để nhận diện các chuỗi lệnh gọi Tool lặp lại thường xuyên, các mẫu nơi các tác nhân nhất quán gọi cùng các Tools theo cùng thứ tự với luồng dữ liệu có thể dự đoán giữa chúng. Triển khai các chuỗi này dưới dạng các meta-tool dùng các hàm [AWS Lambda](https://aws.amazon.com/lambda/) thực thi toàn bộ chuỗi phía-máy-chủ và trả về kết quả cuối.

Ví dụ, một meta-tool "research" có thể kết hợp tìm kiếm cơ sở tri thức, truy xuất tài liệu, và trích xuất độ liên quan thành một lần gọi duy nhất.

Phơi bày các meta-tool qua MCP qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cạnh các Tools riêng lẻ, để các tác nhân có thể chọn giữa meta-tool cho các thao tác thường quy và các Tools riêng lẻ cho các tác vụ mới lạ đòi hỏi suy luận từng-bước.

Thiết kế các meta-tool với các hợp đồng đầu vào và đầu ra rõ ràng và xử lý lỗi cung cấp phản hồi có ý nghĩa khi bất kỳ bước nào trong chuỗi thất bại. Cập nhật prompt tác nhân để bao gồm các mô tả meta-tool hướng dẫn tác nhân ưu tiên chúng cho các thao tác thường quy.

Giám sát hiệu năng meta-tool để xác nhận rằng thao tác hợp thành nhanh hơn chuỗi Tools riêng lẻ tương đương, và phân rã latency meta-tool thành các chỉ số theo-bước để tối ưu được hướng vào bước chậm nhất.

### Các bước triển khai

- **Phân tích telemetry tác nhân để nhận diện các chuỗi lệnh gọi Tool lặp lại thường xuyên:** Tìm các chuỗi xảy ra ba lần trở lên với luồng dữ liệu có thể dự đoán giữa các bước.
- **Thiết kế các meta-tool cho các chuỗi phổ biến nhất với các hợp đồng đầu vào/đầu ra rõ ràng và xử lý lỗi:** Định nghĩa các hợp đồng tường minh và xử lý lỗi theo-bước để các lỗi meta-tool có thể quy trách nhiệm.
- **Triển khai các meta-tool dưới dạng các hàm Lambda thực thi toàn bộ chuỗi phía-máy-chủ:** Dùng [AWS Lambda](https://aws.amazon.com/lambda/) để chạy chuỗi phía-máy-chủ để tác nhân thấy một lệnh gọi thay vì nhiều.
- **Phơi bày các meta-tool qua MCP và AgentCore Gateway cạnh các Tools riêng lẻ:** Đăng ký các meta-tool với [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cạnh các Tools riêng lẻ để tác nhân có thể chọn dựa trên tác vụ.
- **Giám sát hiệu năng meta-tool và so sánh với các chuỗi Tools riêng lẻ tương đương:** Theo dõi latency meta-tool và phân tách theo-bước và so sánh với đường Tools-riêng-lẻ để xác nhận meta-tool thực sự nhanh hơn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu](agentperf06-bp01.md)
- [AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả](agentperf06-bp02.md)
- [AGENTPERF05-BP03 Tối ưu thực thi pipeline AI đa-giai-đoạn](../5-agentperf05/agentperf05-bp03.md)

**Tài liệu liên quan:**

- [Blog: Từ linh hoạt tới framework: Xây dựng các máy chủ MCP với điều phối Tool có kiểm soát](https://aws.amazon.com/blogs/devops/flexibility-to-framework-building-mcp-servers-with-controlled-tool-orchestration/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Các framework, giao thức, và Tools AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)

**Video liên quan:**

- [AgentCore Deep Dive: Browser Tool & Code Interpreter](https://www.youtube.com/watch?v=z3lAJ-Nf_lk)
- [Excel-lent Agents: Code Interpreter của AgentCore](https://www.youtube.com/watch?v=THUX2ycix3Y)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
