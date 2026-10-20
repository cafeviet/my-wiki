# AGENTCOST04-BP02 Tối ưu chi phí phục vụ công cụ thông qua serverless và chia sẻ tài nguyên

Hạ tầng công cụ chạy liên tục để phục vụ lưu lượng agent khó lường mang chi phí rảnh cao nhất trong một ngăn xếp agent. Phục vụ công cụ **serverless** với hạ tầng dùng chung xuyên các agent căn chỉnh chi tiêu với số lần gọi thực tế và loại bỏ chi phí cố định của các phiên bản chuyên dụng cho từng agent.

**Kết quả mong muốn:**

- Bạn có hạ tầng phục vụ công cụ scale động theo mức sử dụng của agent và chỉ tính phí cho các lần gọi thực tế.
- Bạn chia sẻ các dịch vụ công cụ không trạng thái (stateless) xuyên các agent trong khi duy trì cách ly bảo mật.
- Bạn dùng mạng riêng và serialization gọn để giảm chi phí truyền dữ liệu trên các lần gọi công cụ tần suất cao.
- Bạn theo dõi quy gán chi phí theo từng agent để tối ưu có mục tiêu.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các máy chủ bền vững để phục vụ công cụ vốn phát sinh phí trong các giờ hoặc ngày khi không có agent nào gọi công cụ.
- Tạo các phiên bản máy chủ công cụ chuyên dụng cho từng agent thay vì các dịch vụ không trạng thái dùng chung, tạo ra hàng chục máy chủ ít được tận dụng.
- Định tuyến các lần gọi công cụ qua NAT Gateway khi các agent và công cụ nằm trong cùng một VPC, phát sinh phí xử lý dữ liệu trên mỗi GB không cần thiết.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phục vụ công cụ serverless scale về không khi các agent không hoạt động, giảm chi phí rảnh thông qua giá theo mức tiêu thụ.
- Hạ tầng công cụ dùng chung trải chi phí hosting cố định trên tất cả các agent trong khi duy trì cách ly bảo mật.
- Các VPC endpoint và serialization gọn giảm chi phí truyền dữ liệu cho các lần gọi công cụ tần suất cao.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Lưu lượng công cụ của agent vốn có tính bùng nổ. Một đội agent hoạt động trong giờ làm việc, rảnh qua đêm, và rất không đều xuyên các loại agent. Hạ tầng công cụ được cấp phát trước phải trả tiền cho hình dạng đó bằng cách giữ tính toán ấm qua các giờ rảnh, có thể là một chi phí ẩn đáng kể trong các ngăn xếp agent. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) cung cấp phục vụ công cụ serverless, được quản lý hoàn toàn, chuyển đổi các API và các dịch vụ hiện có thành các công cụ tương thích MCP mà không cần quản lý hạ tầng. AgentCore Gateway xử lý xác thực, scale tự động, và gộp nhiều API vào các endpoint hợp nhất.

Vì các công cụ được trình ra qua AgentCore Gateway có sẵn cho tất cả các agent được ủy quyền, một endpoint có thể phục vụ toàn bộ đội thay vì một endpoint cho mỗi agent. [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cung cấp kiểm soát truy cập chi tiết giữ cho việc chia sẻ an toàn.

Với các công cụ cần thực thi kéo dài, [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) hỗ trợ các workload tới 8 giờ với giá theo mức tiêu thụ được tính theo từng giây. Giá theo mức tiêu thụ là mặc định đúng cho các mẫu gọi công cụ khó lường vì nó chỉ tính phí trong lúc xử lý tích cực.

Cold start là một chế độ lỗi đáng để lập kế hoạch trước. Một công cụ nguội kéo dài chu kỳ suy luận của agent và có thể kích hoạt các lần thử lại, có thể đẩy chi phí token theo từng phiên lên trên các đường nguội. Giám sát tần suất cold start trong Amazon CloudWatch và đánh giá Lambda SnapStart hoặc làm ấm theo lịch khi cold start là đáng kể.

Mạng và serialization là nền tảng của việc lập kế hoạch cho các chế độ lỗi này. Các VPC endpoint cho các đường dữ liệu riêng tránh phí xử lý NAT Gateway cho các lần gọi công cụ tần suất cao giữa các agent và công cụ trong cùng một VPC. JSON gọn (hoặc các định dạng nhị phân ở nơi được hỗ trợ) giảm kích thước payload trên các lần gọi tần suất cao lặp lại. Gắn thẻ mọi lần gọi với agent ID và workflow ID cho phép [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) và AWS Cost Explorer làm lộ các agent và công cụ nào đẩy chi tiêu cao nhất.

### Các bước triển khai

- **Trình ra các công cụ qua Gateway serverless:** Triển khai các công cụ agent qua khả năng MCP server của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để có hạ tầng serverless với scale tự động và truy cập dùng chung xuyên các agent.
- **Áp dụng kiểm soát truy cập chi tiết:** Cấu hình các chính sách Cedar của [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) cho truy cập công cụ theo từng agent, giữ cách ly bảo mật trong khi chia sẻ hạ tầng.
- **Quy gán chi phí theo từng agent:** Dùng các thẻ dữ liệu đo lường của [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với agent ID và workflow ID, và tạo các báo cáo AWS Cost Explorer định kỳ theo agent và loại công cụ.
- **Giám sát các mẫu gọi và cold start:** Làm lộ các mẫu gọi công cụ qua AgentCore Observability, và đặt cảnh báo Amazon CloudWatch cho các mẫu vượt quá các giới hạn kỳ vọng, bao gồm tần suất cold start.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST04-BP01 Thiết kế lựa chọn công cụ tiết kiệm chi phí để tối thiểu các lần gọi không cần thiết](agentcost04-bp01.md)
- [AGENTCOST04-BP03 Triển khai caching thông minh và xử lý thất bại cho kết quả công cụ](agentcost04-bp03.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Gateway](https://www.youtube.com/watch?v=atWXM5lziY8)
- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Gateway tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore - Lab 3: Gateway, Identity & Policy](https://catalog.workshops.aws/agentcore-getting-started/en-US/50-add-tool-gateway)
- [Diving Deep into Bedrock AgentCore - Gateway](https://catalog.workshops.aws/agentcore-deep-dive/en-US/30-agentcore-gateway)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
