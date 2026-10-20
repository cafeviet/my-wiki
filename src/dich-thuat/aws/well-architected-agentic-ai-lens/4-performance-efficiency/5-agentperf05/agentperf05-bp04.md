# AGENTPERF05-BP04 Triển khai các mẫu ủy quyền và bàn giao tác nhân hiệu quả

Các chuyển tiếp tác-nhân-tới-tác-nhân mượt mà khiến các luồng công việc đa tác nhân cảm thấy như một trải nghiệm gắn kết duy nhất, nơi tác nhân nhận tiếp nối chính xác ở nơi tác nhân ủy quyền dừng lại. Ủy quyền (delegation) và bàn giao (handoff) đều đòi hỏi truyền ngữ cảnh hiệu quả. Tác nhân nhận cần đủ ngữ cảnh để hành động, nhưng truyền quá nhiều lãng phí thời gian và **Token**.

**Kết quả mong muốn:**

- Bạn có các thao tác ủy quyền và bàn giao tác nhân hoàn thành với **latency** tối thiểu, truyền chính xác ngữ cảnh mà tác nhân nhận cần.
- Bạn có các tác nhân nhận bắt đầu xử lý hữu ích ngay lập tức mà không suy-ra-lại ngữ cảnh mà tác nhân ủy quyền đã có.
- Bạn có các cơ chế truyền ngữ cảnh chuẩn hóa cho phép bất kỳ tác nhân nào ủy quyền tới hoặc nhận bàn giao từ bất kỳ tác nhân nào khác.
- Bạn có latency bàn giao được đo và tối ưu như một phần của ngân sách hiệu năng luồng công việc tổng thể.

**Các phản mẫu thường gặp (anti-patterns):**

- Truyền toàn bộ lịch sử hội thoại và mọi ngữ cảnh tích lũy trong mỗi lần ủy quyền, bất kể tác nhân nhận thực sự cần gì, lãng phí thời gian tuần tự hóa và dung lượng context window.
- Đòi hỏi các tác nhân nhận suy-ra-lại ngữ cảnh (truy vấn-lại cơ sở dữ liệu, truy xuất-lại tài liệu) mà tác nhân ủy quyền đã có, trùng lặp công việc và thêm latency.
- Triển khai ủy quyền như các lệnh gọi chặn đồng bộ nơi tác nhân cha chờ rảnh rỗi cho tác nhân con hoàn thành, lãng phí tài nguyên compute của tác nhân cha.

**Lợi ích khi áp dụng thực hành tốt này:**

- Truyền ngữ cảnh có chọn lọc và các kho ngữ cảnh dùng chung giảm latency ủy quyền.
- Các tác nhân nhận tái dùng ngữ cảnh đã được tác nhân ủy quyền thu thập thay vì lặp lại công việc.
- Các mẫu ủy quyền bất đồng bộ cải thiện throughput của tác nhân cha.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Triển khai một kho ngữ cảnh dùng chung dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) hoặc [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) nơi các tác nhân ủy quyền ghi ngữ cảnh và các tác nhân nhận đọc nó, tránh nhu cầu tuần tự hóa và truyền các payload ngữ cảnh lớn qua lớp điều phối. Các lược đồ truyền ngữ cảnh định nghĩa ngữ cảnh tối thiểu cần cho mỗi loại ủy quyền, một tác nhân xác thực dữ liệu cần dữ liệu và các luật xác thực, không phải toàn bộ lịch sử hội thoại. Với các tác nhân xây dựng bằng Strands Agents, mẫu agent-as-tool tích hợp sẵn tự động thừa hưởng ngữ cảnh liên quan từ phiên của tác nhân cha.

Với các mẫu bàn giao trong các tác nhân hội thoại, tóm tắt ngữ cảnh nén cuộc hội thoại thành một tóm tắt bàn giao súc tích được điều chỉnh theo vai trò của tác nhân nhận, thay vì truyền lịch sử hội thoại thô. Với các mẫu ủy quyền có thể dự đoán, ví dụ một tác nhân phân loại (triage) nhất quán ủy quyền tới một trong vài tác nhân chuyên biệt, làm-ấm-trước qua đồng thời cấp phát trước của [AWS Lambda](https://aws.amazon.com/lambda/) hoặc các pool phiên ấm trên AgentCore Runtime loại latency khởi-động-lạnh khỏi phía nhận. Ủy quyền bất đồng bộ cho tác nhân cha tiếp tục xử lý các tác vụ khác trong khi tác nhân con làm việc, dùng callback hoặc thông báo [Amazon EventBridge](https://aws.amazon.com/eventbridge/) để nhận kết quả.

[Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) chuẩn hóa các giao diện ủy quyền, cho phép bất kỳ tác nhân nào ủy quyền tới bất kỳ tác nhân nào khác qua một API nhất quán xử lý truyền ngữ cảnh, xác thực, và phân phối kết quả. Latency bàn giao thuộc về các bảng điều khiển hiệu năng tác nhân như một chỉ số riêng biệt, được đo từ lúc khởi tạo ủy quyền tới hành động hữu ích đầu tiên của tác nhân nhận.

### Các bước triển khai

- **Nhận diện các mẫu ủy quyền và bàn giao trong các luồng công việc đa tác nhân hiện có và đo latency chuyển tiếp hiện tại:** Lập bản đồ các điểm ủy quyền và bàn giao và đo latency chuyển tiếp hiện tại để các mục tiêu tối ưu được đặt trên nền dữ liệu.
- **Triển khai các kho ngữ cảnh dùng chung dùng AgentCore Memory hoặc DynamoDB cho truyền ngữ cảnh giữa các tác nhân:** Dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) hoặc [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) để các tác nhân ủy quyền ghi ngữ cảnh một lần và các tác nhân nhận đọc nó mà không tuần tự hóa các payload lớn.
- **Định nghĩa các lược đồ ngữ cảnh tối thiểu cho mỗi loại ủy quyền, chỉ định chính xác những gì tác nhân nhận cần:** Giữ payload ủy quyền nhỏ và mục-đích-cụ-thể để các bên nhận chỉ nhận ngữ cảnh cần cho vai trò của chúng.
- **Triển khai tóm tắt ngữ cảnh cho các bàn giao hội thoại nén lịch sử thành các tóm tắt phù-hợp-vai-trò:** Tóm tắt lịch sử hội thoại thô thành một tóm tắt bàn giao được điều chỉnh theo vai trò của tác nhân nhận thay vì chuyển tiếp toàn bộ bản ghi.
- **Cấu hình làm-ấm-trước cho các mẫu ủy quyền có thể dự đoán dùng đồng thời cấp phát trước hoặc các pool phiên ấm:** Với các đích ủy quyền lặp lại, dùng đồng thời cấp phát trước của [AWS Lambda](https://aws.amazon.com/lambda/) hoặc các pool phiên ấm trên AgentCore Runtime để loại latency khởi-động-lạnh.
- **Chuyển các ủy quyền đồng bộ thành các mẫu bất đồng bộ với phân phối kết quả dựa-trên-callback:** Cho tác nhân cha tiếp tục công việc khác trong khi tác nhân con chạy, nhận kết quả qua callback hoặc thông báo EventBridge.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](agentperf05-bp01.md)
- [AGENTPERF05-BP02 Triển khai các mô hình cộng tác đa tác nhân được tối ưu](agentperf05-bp02.md)
- [AGENTPERF04-BP01 Tối ưu các mẫu xử lý thông điệp bất đồng bộ](../4-agentperf04/agentperf04-bp01.md)

**Tài liệu liên quan:**

- [Blog: Các mẫu cộng tác đa tác nhân với Strands Agents và Amazon Nova](https://aws.amazon.com/blogs/machine-learning/multi-agent-collaboration-patterns-with-strands-agents-and-amazon-nova/)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS, Cộng tác đa tác nhân](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/multi-agent-collaboration.html)
- [Vận hành hóa AI dạng tác nhân trên AWS, Thiết kế cho khả năng ghép và cộng tác](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)

**Video liên quan:**

- [AgentCore Memory: Bộ nhớ giai thoại & Các mẫu](https://www.youtube.com/watch?v=1EEIGsKIjGA)

**Ví dụ liên quan:**

- [GitHub: Hướng dẫn điều phối đa tác nhân dùng Bedrock AgentCore](https://github.com/aws-solutions-library-samples/guidance-for-multi-agent-orchestration-using-bedrock-agentcore-on-aws)
- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Memory](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
