# AGENTPERF05-BP02 Triển khai các mô hình cộng tác đa tác nhân được tối ưu

Các hệ đa tác nhân thường mang lại kết quả mạnh nhất khi mỗi mẫu cộng tác được khớp với tác vụ nó được thiết kế cho (ví dụ supervisor-worker cho phân rã có cấu trúc, bầy/swarm cho khám phá sáng tạo, và pipeline cho xử lý tuần tự). Trước khi chọn bất kỳ mẫu đa tác nhân nào, hãy quyết định liệu một năng lực nên là một sub-agent hay một **Tool** mà một tác nhân đơn lẻ gọi. Một lệnh gọi Tool hoàn thành trong vài mili-giây, trong khi một ủy quyền sub-agent là một vòng lặp suy luận LLM đầy đủ tốn thời gian và **Token**.

**Kết quả mong muốn:**

- Bạn có các luồng công việc đa tác nhân dùng các mô hình cộng tác khớp với đặc trưng tác vụ của chúng.
- Bạn có mỗi năng lực được triển khai ở mức trừu tượng đúng, Tool cho các thao tác xác định đơn-bước, sub-agent cho các tác vụ đòi hỏi suy luận độc lập.
- Bạn có chi phí phối hợp được giảm thiểu qua lựa chọn mẫu phù hợp và triển khai.

**Các phản mẫu thường gặp (anti-patterns):**

- Ủy quyền cho một sub-agent cho các năng lực xác định, không-trạng-thái, và đơn-bước, gọi API, tra cứu cơ sở dữ liệu, hoặc chuyển đổi định dạng, trả toàn bộ chi phí của một vòng lặp suy luận LLM cho công việc mà một lệnh gọi Tool sẽ xử lý trong vài mili-giây.
- Dùng một mô hình supervisor-worker cho mọi luồng công việc đa tác nhân, tạo ra một điểm nghẽn ở supervisor phải xử lý mọi kết quả trung gian và ra mọi quyết định ủy quyền.
- Triển khai các mẫu bầy mà không có tiêu chí hội tụ tường minh hoặc ngân sách tài nguyên, để các tác nhân tiếp tục khám phá vô hạn mà không hội tụ về một kết quả chung.

**Lợi ích khi áp dụng thực hành tốt này:**

- Khớp mô hình cộng tác với cấu trúc tác vụ giảm thiểu chi phí phối hợp.
- Lựa chọn mô hình phù hợp cho các tác vụ có thể phân rã tối đa hóa song song hóa.
- Các timeout và cơ chế dự phòng giữ cộng tác kiên cường khi các tác nhân riêng lẻ thất bại hoặc chậm lại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Dùng một sub-agent khi năng lực đòi hỏi suy luận riêng của nó (suy luận LLM cho các đầu vào mơ hồ hoặc các phán đoán), phạm vi ngữ cảnh hoặc bộ nhớ riêng của nó, điều phối Tool nhiều-bước nơi việc sắp xếp thứ tự đòi hỏi suy luận, một Model hoặc prompt khác, hoặc cô lập lỗi độc lập.

Dùng một Tool khi năng lực là xác định, không-trạng-thái, đơn-bước, và nhanh (dưới 2-3 giây).

Với các trường hợp ranh giới, bắt đầu với một Tool và chỉ thăng cấp thành một sub-agent khi các mẫu gọi-lại thường xuyên cho thấy năng lực cần vòng lặp suy luận riêng của nó.

Một khi kiến trúc đa tác nhân được biện minh, chọn mô hình cộng tác dựa trên đặc trưng tác vụ. Dùng supervisor-worker khi tác vụ có phân rã rõ ràng và cần kiểm soát chất lượng tập trung. Mẫu agent-as-tool của Strands Agents và cộng tác đa tác nhân của Amazon Bedrock Agents cung cấp điều phối supervisor-worker với truyền ngữ cảnh tự động và tổng hợp kết quả.

Dùng pipeline khi tác vụ có một luồng tuần tự tự nhiên, cân bằng các thời lượng giai đoạn và dùng điều phối đồ thị của framework của bạn để nối các tác nhân tuần tự.

Dùng ngang-hàng (peer-to-peer) hoặc blackboard khi nhiều tác nhân cần đóng góp các giải pháp một phần một cách bất đồng bộ, triển khai một không gian làm việc dùng chung dùng AgentCore Memory hoặc DynamoDB với các thông báo hướng-sự-kiện.

Dùng bầy (swarm) khi tác vụ hưởng lợi từ khám phá song song và hành vi nảy sinh, triển khai phát hiện hội tụ và ngân sách token theo-bầy để giúp ngăn tiêu tài nguyên vô giới hạn.

Với logic ủy quyền xác định hoặc các luồng công việc chạy-dài bền, [AWS Step Functions](https://aws.amazon.com/step-functions/) vẫn là một lựa chọn thay thế mạnh cho việc điều phối các lệnh gọi tác nhân.

Với mọi mô hình cộng tác, triển khai các cơ chế timeout và dự phòng giúp ngăn một tác nhân chậm hoặc thất bại duy nhất chặn toàn bộ luồng công việc. Triển khai các hệ đa tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cho mở rộng và observability được quản lý, hoặc trên Amazon EKS hay Amazon ECS cho các triển khai dựa-trên-container tùy chỉnh. Giám sát các chỉ số chi phí cộng tác gồm latency phối hợp, tỷ lệ công-việc-dư-thừa, và throughput mỗi mô hình.

### Các bước triển khai

- **Đánh giá liệu mỗi năng lực nên là một Tool hay một sub-agent:** Mặc định thành Tools và chỉ thăng cấp thành sub-agent khi các mẫu gọi-lại cho thấy nhu cầu suy luận độc lập.
- **Phân loại các luồng công việc đa tác nhân theo đặc trưng tác vụ:** Đánh giá khả năng phân rã, cấu trúc phụ thuộc, yêu cầu latency, và liệu tác vụ có hưởng lợi từ khám phá song song.
- **Chọn mô hình cộng tác:** Dùng supervisor-worker cho phân rã rõ ràng, pipeline cho luồng tuần tự, ngang-hàng cho các không gian vấn đề dùng chung, và bầy cho khám phá song song.
- **Triển khai dùng các mẫu đa tác nhân nguyên bản của framework của bạn:** Dùng agent-as-tool của Strands, cộng tác đa tác nhân của Amazon Bedrock, hoặc một tương đương, và dùng [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho ngữ cảnh dùng chung qua các tác nhân.
- **Triển khai các cơ chế timeout và dự phòng cho mọi mô hình cộng tác:** Đặt timeout theo-tác-nhân và định nghĩa hành vi dự phòng để một tác nhân chậm hoặc thất bại không thể chặn toàn bộ luồng công việc.
- **Giám sát các chỉ số chi phí cộng tác và tối ưu lựa chọn mô hình theo thời gian:** Theo dõi latency phối hợp, tỷ lệ công-việc-dư-thừa, và throughput mỗi mô hình, và đánh giá lại lựa chọn cộng tác khi lưu lượng dịch chuyển.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](agentperf05-bp01.md)
- [AGENTPERF05-BP04 Triển khai các mẫu ủy quyền và bàn giao tác nhân hiệu quả](agentperf05-bp04.md)
- [AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả](../4-agentperf04/agentperf04-bp02.md)

**Tài liệu liên quan:**

- [Blog: Các mẫu cộng tác đa tác nhân với Strands Agents và Amazon Nova](https://aws.amazon.com/blogs/machine-learning/multi-agent-collaboration-patterns-with-strands-agents-and-amazon-nova/)
- [Blog: Cộng tác đa tác nhân với Strands](https://aws.amazon.com/blogs/devops/multi-agent-collaboration-with-strands/)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS, Cộng tác đa tác nhân](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/multi-agent-collaboration.html)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS, Các tác nhân điều phối luồng công việc](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-orchestration-agents.html)
- [Dùng cộng tác đa tác nhân với Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html)

**Video liên quan:**

- [Các mẫu thiết kế Amazon Bedrock Agents và AgentCore (TNC322)](https://www.youtube.com/watch?v=GYlPFmrATjU)

**Ví dụ liên quan:**

- [GitHub: Workshop cộng tác đa tác nhân Bedrock](https://github.com/aws-samples/bedrock-multi-agents-collaboration-workshop)
- [GitHub: Cộng tác đa tác nhân với Strands](https://github.com/aws-samples/sample-multi-agent-collaboration-with-strands)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock Agents](https://aws.amazon.com/bedrock/agents/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
