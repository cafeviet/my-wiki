# AGENTCOST04-BP01 Thiết kế lựa chọn công cụ tiết kiệm chi phí để tối thiểu các lần gọi không cần thiết

Thường thì lần gọi công cụ tiết kiệm chi phí nhất là lần mà một agent quyết định không thực hiện vì câu trả lời đã có sẵn trong ngữ cảnh. Suy luận ưu-tiên-ngữ-cảnh, lựa chọn xếp hạng theo chi phí, và phát hiện trùng lặp gắn việc gọi công cụ với giá trị của thông tin được truy xuất.

**Kết quả mong muốn:**

- Bạn có các agent kiểm tra ngữ cảnh và bộ nhớ được quản lý trước khi gọi công cụ.
- Bạn có một rubric lựa chọn xếp hạng theo chi phí trỏ các agent tới các lựa chọn thay thế rẻ hơn trước.
- Bạn gom lô các yêu cầu ở nơi có thể và cache kết quả trong các phiên để tránh các lần gọi trùng lặp.
- Bạn giám sát tần suất gọi theo từng công cụ và tỷ lệ trúng cache như các số liệu riêng biệt.

**Các phản mẫu thường gặp (anti-patterns):**

- Gọi công cụ mà không kiểm tra xem thông tin cần thiết đã tồn tại trong ngữ cảnh hay bộ nhớ được quản lý hay chưa, thêm chi phí mà không cải thiện kết quả.
- Tạo các giao diện công cụ hẹp trả về dữ liệu tối thiểu, buộc các lần gọi theo sau để lắp ráp ngữ cảnh đầy đủ.
- Triển khai logic thử lại mà không có exponential backoff hoặc điểm cắt tự động, gây các cơn bão thử lại nhân chi phí trong lúc suy giảm dịch vụ.
- Vận hành mà không có số liệu gọi công cụ, nên không ai có thể xác định công cụ nào đắt nhất hoặc được gọi thường xuyên nhất.

**Lợi ích khi áp dụng thực hành tốt này:**

- Đánh giá ưu-tiên-ngữ-cảnh giảm các lần gọi công cụ không cần thiết cho các agent có ngữ cảnh phong phú từ các bước suy luận trước đó.
- Các rubric lựa chọn công cụ xếp hạng theo chi phí hướng các agent tới các lựa chọn thay thế rẻ hơn, dành các API bên ngoài đắt tiền cho các trường hợp mà các lựa chọn chi phí thấp hơn không đủ.
- Các giao diện công cụ theo lô và các tập kết quả đầy đủ giảm chi phí trên mỗi lần gọi và nhu cầu về các lần gọi theo sau.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Tính cần thiết của công cụ thuộc về prompt suy luận của agent, chứ không phải một suy nghĩ muộn màng trong giám sát. System prompt nên chỉ thị model đánh giá xem câu trả lời có thể suy ra từ thông tin đã có trong ngữ cảnh, từ lịch sử hội thoại lưu trong [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html), hay từ các kết quả công cụ trước đó trong cùng chu kỳ suy luận hay không, trước khi chọn một công cụ. Ghép điều này với một rubric lựa chọn xếp hạng theo chi phí đặt các lựa chọn thay thế rẻ hơn lên trước: nếu một phép tính cục bộ hoặc một kết quả đã cache tạo ra cùng câu trả lời như một lần gọi API bên ngoài, agent nên đi theo con đường rẻ hơn.

Thiết kế giao diện công cụ quan trọng ngang bằng với các chỉ thị cho agent. Các giao diện hẹp trả về dữ liệu tối thiểu buộc các agent thực hiện các lần gọi theo sau để lắp ráp ngữ cảnh mà chúng cần, làm phồng chi phí công cụ cho mỗi chu kỳ suy luận. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cung cấp khám phá công cụ dựa trên MCP với các tính năng kết hợp (composition) gộp nhiều API vào các endpoint đơn, giảm chi phí gọi. Thiết kế các giao diện công cụ để chấp nhận đầu vào theo lô và trả về các tập kết quả đầy đủ để một lần gọi làm được công việc của nhiều lần.

Hãy cân nhắc cách bạn triển khai phát hiện trùng lặp. Các agent thường gọi cùng một công cụ với các tham số giống hệt nhau qua các lần lặp suy luận, đặc biệt khi quay lại một nhánh. Triển khai một cache kết quả công cụ phạm vi phiên trong các hàm action group Lambda hoặc các MCP server của AgentCore Gateway để agent không gọi lại cùng công cụ với cùng tham số. Lưu kết quả trong bộ nhớ ngắn hạn của AgentCore Memory để prompt suy luận của agent có thể làm lộ các kết quả trước trước khi quyết định thực hiện một lần gọi khác.

Để thực thi và đo lường, [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) áp dụng các chính sách Cedar dừng thử lại khi tỷ lệ thất bại cho thấy sự suy giảm dai dẳng và giới hạn số lần gọi công cụ cho mỗi chu kỳ suy luận. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) làm lộ các mẫu lựa chọn công cụ, Amazon CloudWatch theo dõi tần suất gọi và tỷ lệ trúng khử trùng lặp, và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chấm điểm độ chính xác lựa chọn công cụ để các mẫu gọi quá mức hiện lên như dữ liệu chất lượng, không chỉ dữ liệu chi phí.

### Các bước triển khai

- **Nhúng đánh giá tính cần thiết của công cụ vào các system prompt:** Chỉ đạo model kiểm tra ngữ cảnh và [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) trước khi gọi công cụ, và đưa vào một rubric lựa chọn xếp hạng theo chi phí đặt các lựa chọn thay thế rẻ hơn lên trước.
- **Thiết kế lại các giao diện công cụ cho gom lô:** Trình ra các công cụ qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với đầu vào theo lô và các tập kết quả đầy đủ để một lần gọi mang payload trước đây cần nhiều lần.
- **Cache kết quả công cụ trong các phiên:** Triển khai các cache phạm vi phiên trong các hàm action group Lambda hoặc các MCP server của Gateway để khử trùng lặp các lần gọi công cụ giống hệt nhau, lưu kết quả trong AgentCore Memory để agent có thể làm lộ chúng trước lần gọi kế tiếp.
- **Áp dụng các điểm cắt tự động qua policy:** Cấu hình các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) giới hạn số lần gọi công cụ cho mỗi chu kỳ suy luận và dừng thử lại khi thất bại dai dẳng.
- **Giám sát các mẫu lựa chọn công cụ:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để làm lộ các mẫu lựa chọn công cụ và tạo các số liệu Amazon CloudWatch cho tần suất gọi công cụ và tỷ lệ trúng khử trùng lặp.
- **Chấm điểm độ chính xác lựa chọn công cụ:** Dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) để định kỳ chấm điểm độ chính xác lựa chọn công cụ, gắn cờ các mẫu nơi các agent chọn công cụ đắt tiền trong khi các lựa chọn thay thế rẻ hơn đã đủ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](../2-agentcost02/agentcost02-bp02.md)
- [AGENTCOST04-BP02 Tối ưu chi phí phục vụ công cụ thông qua serverless và chia sẻ tài nguyên](agentcost04-bp02.md)
- [AGENTCOST04-BP03 Triển khai caching thông minh và xử lý thất bại cho kết quả công cụ](agentcost04-bp03.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [AWS re:Invent 2024 - Scale agent tools with AgentCore Gateway (AIM3313)](https://www.youtube.com/watch?v=DlIHB8i6uyE)
- [Integrating MCP Tools with Strands Agents](https://www.youtube.com/watch?v=bHSbjCZZFjE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Gateway tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore - Gateway](https://catalog.workshops.aws/agentcore-deep-dive/en-US/30-agentcore-gateway)

**Công cụ liên quan:**

- [Strands Agents MCP Tools](https://strandsagents.com/docs/user-guide/concepts/tools/mcp-tools/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
