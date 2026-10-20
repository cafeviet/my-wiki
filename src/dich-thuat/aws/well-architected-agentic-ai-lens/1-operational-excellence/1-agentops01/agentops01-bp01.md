# AGENTOPS01-BP01 Thiết lập vai trò, trách nhiệm và tiêu chí thành công được định nghĩa rõ ràng cho agent

Một agent không có vai trò được tài liệu hóa sẽ khó đánh giá và cải thiện. Hãy trao cho mỗi agent một mục đích, phạm vi, mức độ tự chủ, và tiêu chí thành công rõ ràng để biến hành vi mơ hồ thành thứ mà các nhóm có thể quan sát, đo lường, và quy trách nhiệm.

**Kết quả mong muốn:**

- Mỗi agent có một bản mô tả công việc được tài liệu hóa, xác định vai trò, các kết quả kinh doanh mà nó sở hữu, ranh giới tự chủ, và tiêu chí thành công đo lường được.
- Các nhóm có thể đánh giá khách quan liệu một agent có hoạt động như dự định hay không, và các bên liên quan hiểu được giá trị mà mỗi agent mang lại.
- Quy trình xử lý lỗi và leo thang được xác định trước khi triển khai, để các yêu cầu ngoài phạm vi và các trường hợp biên (edge cases) được xử lý một cách có thể dự đoán.
- Tiêu chí thành công ánh xạ tới các kết quả kinh doanh (tỷ lệ giải quyết tác vụ, mức độ hài lòng của khách hàng) bên cạnh các chỉ số kỹ thuật.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai agent mà không có ranh giới phạm vi được tài liệu hóa, tạo ra hành vi khó lường khi agent gặp các yêu cầu ngoài mục đích dự định của nó.
- Định nghĩa tiêu chí thành công chỉ bằng các chỉ số kỹ thuật (độ trễ, thời gian hoạt động) mà không ánh xạ tới kết quả kinh doanh, khiến không thể đánh giá agent có mang lại giá trị hay không.
- Xem định nghĩa vai trò agent như tài liệu một lần thay vì tài liệu sống tiến hóa theo yêu cầu kinh doanh.
- Bỏ qua việc xác định các bên liên quan phụ thuộc vào agent, khiến không có chủ sở hữu rõ ràng khi cần điều chỉnh hành vi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Ý định và phạm vi được tài liệu hóa trở thành nền tảng cho các kiểm soát ở phía sau. Guardrails, ngưỡng giám sát, và đường leo thang đều bắt nguồn từ mục đích đã tuyên bố của agent.
- Tiêu chí thành công đo lường được cho phép đánh giá dựa trên dữ liệu, mang lại cho nhóm bằng chứng thực nghiệm để tinh chỉnh lặp lại và ra quyết định đầu tư.
- Các yêu cầu ngoài phạm vi và trường hợp biên được xử lý một cách nhã nhặn vì các đường lỗi đã được xác định trước khi agent được đưa vào vận hành.
- Các bên liên quan và người vận hành chia sẻ hiểu biết chung về việc agent phải làm gì và ai chịu trách nhiệm về hành vi của nó.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Một định nghĩa vai trò dạng văn bản là kiểm soát đơn giản nhất mà một agent có thể có, và cũng là thứ thường bị bỏ qua nhất. Thiếu nó, Guardrails được điều chỉnh theo hành vi giả định, ngưỡng giám sát được đặt theo workload giả định, và tác nhân kích hoạt leo thang được kích hoạt theo lỗi giả định. Tài liệu này nên nêu tên mục đích chính của agent, quy trình kinh doanh mà nó hỗ trợ, các bên liên quan phụ thuộc vào nó, và các kết quả mà nó chịu trách nhiệm. Hãy giữ tài liệu luôn cập nhật khi yêu cầu tiến hóa.

Một agent chỉ quan sát và báo cáo là một cam kết vận hành khác với một agent tự chủ hành động, và việc gộp lẫn hai vai trò này có thể trở thành một điểm giám sát bị bỏ sót. Tiến trình trưởng thành từ người quan sát (observer) đến trợ lý (assistant) đến tự chủ (autonomous) đến điều phối viên (orchestrator) đến người đổi mới (innovator) mang lại cho các bên liên quan một vốn từ chung để bàn về mức độ tự chủ của một agent và mức độ rà soát của con người mà nó vẫn cần. Đặt kỳ vọng ở đúng nấc thang trong tiến trình đó, và các kiểm soát ở phía sau sẽ theo sau.

Tiêu chí thành công thất bại khi chúng đo những gì rẻ để đo thay vì những chỉ số quan trọng về mặt vận hành. Ví dụ, một agent hỗ trợ khách hàng có mục tiêu độ trễ mà không có tỷ lệ giải quyết đang tối ưu cho sai đối tượng. Khung SMART (specific, measurable, achievable, relevant, time-bound) có ích, nhưng phép kiểm sắc bén hơn là kiểm tra xem một chỉ số có cải thiện song hành với kết quả kinh doanh mà nó đo hay không. Các chỉ số kết quả kinh doanh (tỷ lệ giải quyết tác vụ, tỷ lệ leo thang, mức độ hài lòng của khách hàng) nên được kiểm tra bên cạnh các chỉ số kỹ thuật và có trọng số ngang nhau.

Hãy đưa định nghĩa vai trò vào vận hành bằng cách nối nó vào các kiểm soát tại runtime. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) biến các giới hạn chủ đề, bộ lọc nội dung, và chủ đề bị chặn đã được tài liệu hóa thành sự áp đặt tại thời điểm gọi (invocation). Đối với các đường không cần mã (no-code) như [Amazon Quick Suite](https://aws.amazon.com/quicksuite/), cùng kỷ luật định nghĩa vai trò được áp dụng thông qua cấu hình danh tính, chỉ dẫn, và tri thức. Hãy công bố định nghĩa vai trò agent lên [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) để cả người vận hành và các agent khác có thể khám phá năng lực, hiểu phạm vi, và định tuyến công việc một cách phù hợp.

Xử lý lỗi xác định agent làm gì khi gặp yêu cầu ngoài phạm vi, khi Tools không khả dụng, hoặc khi nó không thể tạo ra phản hồi tự tin. Các đường suy giảm nhã nhặn (graceful degradation), leo thang dựa trên độ tin cậy, và ghi log có cấu trúc cho các yêu cầu ngoài phạm vi giúp các trường hợp biên không biến thành sự cố. Hãy rà soát bản mô tả công việc theo quý hoặc mỗi khi yêu cầu kinh doanh thay đổi.

### Các bước triển khai

- **Tạo mẫu bản mô tả công việc agent:** Bao gồm tên và định danh, mục đích chính, danh sách các bên liên quan, mức độ tự chủ trên mô hình trưởng thành, tiêu chí thành công với mục tiêu đo lường được, các chủ đề ngoài phạm vi, và quy trình leo thang.
- **Hoàn thành bản mô tả công việc cho mỗi agent:** Cùng lúc mời cả các bên liên quan kỹ thuật và kinh doanh để kiểm định sự phù hợp giữa phạm vi và tiêu chí thành công, và ghi nhận sự phê duyệt từ cả hai.
- **Định nghĩa tiêu chí thành công đo lường được:** Kết hợp các chỉ số kết quả kinh doanh (tỷ lệ hoàn thành tác vụ, tỷ lệ leo thang, mức độ hài lòng của người dùng) với các chỉ số kỹ thuật, và áp dụng khung SMART cho từng chỉ số.
- **Áp đặt phạm vi tại runtime bằng [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html):** Cấu hình các giới hạn chủ đề, bộ lọc nội dung, và chủ đề bị chặn phản ánh các ranh giới đã tài liệu hóa của agent.
- **Công bố định nghĩa agent lên [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html):** Đăng ký năng lực, phạm vi, và metadata của mỗi agent để người vận hành và các agent khác có thể khám phá và định tuyến công việc phù hợp.
- **Định nghĩa xử lý lỗi và leo thang:** Tài liệu hóa các đường suy giảm nhã nhặn, tác nhân leo thang tới con người dựa trên độ tin cậy, và yêu cầu ghi log có cấu trúc cho các yêu cầu ngoài phạm vi.
- **Thiết lập nhịp rà soát theo quý:** Cập nhật bản mô tả công việc khi yêu cầu kinh doanh thay đổi, và xem chúng như tài liệu vận hành sống thuộc sở hữu của một cá nhân được nêu tên.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS01-BP02 Thiết kế quy trình bàn giao đa agent với leo thang có con người trong vòng lặp](agentops01-bp02.md)
- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](../2-agentops02/agentops02-bp01.md)
- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](../3-agentops03/agentops03-bp01.md)
- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công phù hợp với hiệu năng cho workload agent](../../4-performance-efficiency/1-agentperf01/agentperf01-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Các mẫu và luồng công việc agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [AI agent trong doanh nghiệp: Thực hành tốt với Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)
- [Kiro Specs](https://kiro.dev/docs/specs/)

**Video liên quan:**

- [AWS re:Invent 2024 - Agentic AI Meets responsible AI: Strategy and best practices (AIM422)](https://www.youtube.com/watch?v=OGvXA1dAh1U)
- [AWS re:Invent 2024 - Agents in the enterprise: Best practices with AgentCore (AIM3310)](https://www.youtube.com/watch?v=w5XJxCpUADY)
- [AWS 2025 - Beginner-Friendly Amazon Bedrock AgentCore & Strands Agents Tutorial](https://www.youtube.com/watch?v=j2wYT6jqXZY)
- [AWS re:Invent 2024 - Agentic AI and the journey to gen AI value realization (AIM242)](https://www.youtube.com/watch?v=p_QuUrB3ONg)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock Samples, GenAI Quick-Start PoCs](https://github.com/aws-samples/genai-quickstart-pocs)
- [GitHub: Sample Agentic Platform on AWS](https://github.com/aws-samples/sample-agentic-platform)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore](https://catalog.workshops.aws/agentcore-getting-started/en-US)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
