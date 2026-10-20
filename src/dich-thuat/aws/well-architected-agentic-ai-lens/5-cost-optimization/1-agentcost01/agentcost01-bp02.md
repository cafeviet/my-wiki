# AGENTCOST01-BP02 Tối ưu chi phí cộng tác đa agent thông qua các mẫu bàn giao hiệu quả

Trong các hệ thống đa agent, chi phí ẩn lớn nhất là ngữ cảnh dư thừa đi kèm với mỗi lần bàn giao (handoff). Các thông điệp bàn giao có cấu trúc và bộ nhớ dùng chung giữ cho chi phí phối hợp tỷ lệ với độ phức tạp của tác vụ chứ không theo độ dài hội thoại.

**Kết quả mong muốn:**

- Bạn có các thông điệp bàn giao chỉ mang theo đặc tả tác vụ, các sự kiện liên quan và các ràng buộc, chứ không phải toàn bộ bản ghi hội thoại.
- Bạn có các agent cộng tác chia sẻ ngữ cảnh chung qua một tầng bộ nhớ (memory) được quản lý thay vì truyền lại nó ở mỗi lần bàn giao.
- Bạn theo dõi chi phí phối hợp theo từng lần bàn giao và theo từng luồng công việc như các số liệu riêng biệt.

**Các phản mẫu thường gặp (anti-patterns):**

- Truyền toàn bộ lịch sử hội thoại ở mỗi lần bàn giao, khiến chi phí token đầu vào mở rộng theo độ dài hội thoại bất kể mức độ liên quan với agent nhận.
- Xây dựng các cấp bậc supervisor sâu nơi việc lồng nhiều tầng thêm các lần gọi model điều phối tại mỗi tầng, khiến chi phí phối hợp vượt quá giá trị thực thi.
- Bỏ qua bộ nhớ dùng chung cho các agent cộng tác, truyền lại các sự kiện chung trong cửa sổ ngữ cảnh của mỗi agent và gây tăng chi phí tuyến tính theo số lượng agent.
- Chạy các luồng đa agent mà không theo dõi chi phí bàn giao, làm giảm khả năng nhận diện các luồng công việc nơi chi phí phối hợp đã trở nên không tương xứng với công việc thực thi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chi phí phối hợp giữ tỷ lệ với độ phức tạp của tác vụ chứ không theo độ dài hội thoại hay số lượng agent.
- Bộ nhớ dùng chung loại bỏ việc truyền ngữ cảnh dư thừa, giảm chi phí token cho mỗi lần bàn giao.
- Khả năng nhìn thấy chi phí theo từng lần bàn giao cho phép tinh chỉnh các mẫu tương tác đa agent dựa trên dữ liệu.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Thứ đắt nhất mà một agent có thể gửi đi là ngữ cảnh mà bên nhận đã có (hoặc không cần). Mỗi lần bàn giao sao chép toàn bộ hội thoại qua ranh giới lại phải trả tiền một lần nữa cho thông tin không hề thay đổi. Hãy coi các thông điệp bàn giao như các bản tóm tắt có cấu trúc chứa đặc tả tác vụ, các sự kiện liên quan và các ràng buộc mà worker phải tôn trọng. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho phép các mẫu ghi-một-lần, đọc-nhiều-lần trong đó một agent lưu một sự kiện dưới một session ID và actor ID, và mọi agent cộng tác đọc nó mà không nhúng lại vào prompt của riêng mình. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) bổ sung kỷ luật tương ứng ở phía công cụ, dùng Semantic Tool Selection tương thích **MCP** để chỉ trình ra các công cụ liên quan tới ý định hiện tại thay vì toàn bộ danh mục.

Chưng cất ngữ cảnh (context distillation) nghĩa là một lần gọi model nhỏ hoặc một hàm Lambda có thể nén ngữ cảnh đến vào lượng thông tin tối thiểu đủ dùng cho tác vụ của agent kế tiếp trước khi lần bàn giao vượt qua ranh giới. Chi phí của lần gọi chưng cất thường thấp hơn chi phí của việc truyền lặp đi lặp lại ngữ cảnh chưa cắt gọt qua các luồng công việc sâu hơn.

Mỗi tầng supervisor-worker thêm ít nhất một lần suy luận để ủy quyền và một lần để tổng hợp. Các cấp bậc sâu hơn ba tầng làm chi phí đó tăng nhanh, và hầu hết các cấp bậc sâu có thể được làm phẳng bằng cách thay các supervisor trung gian bằng giao tiếp trực tiếp worker-với-worker qua giao thức Agent-to-Agent của AgentCore Runtime. Số liệu chẩn đoán là tỷ lệ token điều phối-trên-thực thi. Các supervisor không nên tiêu thụ quá 20% tổng token của luồng công việc, để lại 80% cho các worker làm việc thực thi. Một tỷ lệ trôi lên trên 20% có nghĩa là sự phối hợp đã trở nên không tương xứng với công việc.

Khả năng nhìn thấy là điều kiện tiên quyết cho các mẫu này. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp tracing phân tán để chi phí giao tiếp agent-với-agent xuất hiện như một hạng mục riêng thay vì bị ẩn bên trong chi phí luồng công việc tổng hợp. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy theo thời gian thực trên các vết gọi công cụ trực tiếp và như các bộ kiểm thử offline trong pipeline CI/CD, nên các lần gọi dư thừa hoặc không cần thiết được phát hiện sớm.

### Các bước triển khai

- **Thiết kế các thông điệp bàn giao có cấu trúc:** Thay toàn bộ lịch sử hội thoại bằng một đối tượng tóm tắt chứa đặc tả tác vụ, các sự kiện liên quan và các ràng buộc mà agent nhận phải tôn trọng. Đánh phiên bản lược đồ thông điệp để bên nhận có thể từ chối các lần bàn giao sai định dạng.
- **Chèn chưng cất ngữ cảnh tại các ranh giới:** Thêm một lần gọi model nhỏ hoặc hàm Lambda trích xuất ngữ cảnh tối thiểu đủ dùng trước mỗi lần bàn giao, để token đầu vào tại các điểm chuyển tiếp phản ánh nhu cầu tác vụ hiện tại thay vì lịch sử tích lũy.
- **Cấu hình bộ nhớ dùng chung với quy tắc sở hữu:** Cấp phát [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) truy cập được bởi mọi agent cộng tác, và ghi lại agent nào sở hữu quyền ghi vào mỗi namespace để trạng thái dùng chung có nguồn gốc rõ ràng.
- **Làm phẳng các cấp bậc sâu:** Kiểm tra các luồng đa agent tìm độ sâu supervisor-worker lớn hơn ba tầng, và thay các supervisor trung gian bằng giao tiếp trực tiếp worker-với-worker qua giao thức Agent-to-Agent của AgentCore Runtime ở nơi có thể làm cho định tuyến trở nên tường minh.
- **Trình ra các agent chuyên biệt qua Gateway:** Xuất bản các agent như công cụ qua khả năng MCP server của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), và bật Semantic Tool Selection để các agent cộng tác chỉ thấy các công cụ liên quan tới yêu cầu hiện tại.
- **Đánh giá hiệu quả gọi công cụ trong CI và trong production:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) trên các vết gọi công cụ trực tiếp để gắn cờ việc sử dụng kém hiệu quả lúc chạy, và trên các bộ kiểm thử offline trong pipeline CI/CD để bắt các hồi quy trước khi triển khai.
- **Theo dõi tỷ lệ điều phối-trên-thực thi:** Gắn thẻ mọi lần gọi với workflow-id và agent-role, xây dựng các dashboard CloudWatch hiển thị tỷ lệ token supervisor-trên-worker cho mỗi luồng công việc, và cấu hình cảnh báo AWS Budgets khi chi phí điều phối vượt quá 20% tổng chi phí token của luồng công việc.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](agentcost01-bp01.md)
- [AGENTCOST01-BP03 Triển khai các mẫu tiết kiệm chi phí như hybrid supervisor để phối hợp đa agent](agentcost01-bp03.md)
- [AGENTCOST01-BP04 Thiết kế các cấp bậc agent và mẫu ủy quyền giảm chi phí phối hợp](agentcost01-bp04.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](../5-agentcost05/agentcost05-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Agentic AI patterns and workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)
- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Multi-agent tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime/03-advanced-concepts)
- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Evaluations tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
