# AWS Well-Architected Agentic AI Lens

> **Bản dịch tiếng Việt từ:** [AWS Well-Architected Agentic AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html), Amazon Web Services.  
> **Ngày xuất bản nguồn:** 10/06/2026.  
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; các mã best-practice (AGENTOPS01, AGENTSEC04-BP02…) và tên sản phẩm được giữ nguyên.


Ngày xuất bản: **June 10, 2026** ([Lịch sử sửa đổi tài liệu](9-phu-luc/document-revisions.md))

Các tổ chức triển khai **AI tác nhân (agentic AI)** đang chuyển từ câu hỏi "chúng ta có xây được một Agent không?" sang "chúng ta có thể vận hành các Agent một cách tin cậy, bảo mật và hiệu quả về chi phí ở quy mô lớn không?". AWS Well-Architected Agentic AI Lens trả lời câu hỏi này bằng cách mở rộng AWS Well-Architected Framework với các thực hành tốt nhất dành riêng cho việc thiết kế, triển khai và vận hành các hệ thống agentic AI trên AWS, cung cấp hướng dẫn kiến trúc từ các Agent nguyên mẫu cho đến các hệ thống Agent cấp sản xuất.

Lens này bao quát toàn bộ phổ kiến trúc agentic AI, từ hạ tầng nền tảng hỗ trợ tính toán và bộ nhớ của Agent, đến các mẫu điều phối (orchestration) phối hợp các luồng công việc đa Agent, cho tới các thực hành vận hành giúp Agent duy trì độ tin cậy, bảo mật và hiệu quả chi phí trong môi trường sản xuất. Dù Agent phục vụ người dùng cuối qua giao diện hội thoại, tự động hóa các quy trình nội bộ, hay vận hành trên hạ tầng sản xuất song hành cùng các kỹ sư con người, các nguyên tắc kiến trúc trong Lens này đều áp dụng cho toàn bộ các trường hợp sử dụng agentic.

## Điều làm nên sự khác biệt của Lens này

Các hệ thống agentic AI đưa ra những chiều kiến trúc mà các hướng dẫn hiện có về đám mây và AI tạo sinh chưa giải quyết:

- **Agent suy luận, không chỉ phản hồi:** Một yêu cầu duy nhất của người dùng có thể kích hoạt nhiều lần suy luận LLM, gọi công cụ (**Tools**), truy xuất bộ nhớ, và giao tiếp giữa các Agent, mỗi lần đều làm tăng độ trễ, chi phí và bề mặt lỗi. Tối ưu hóa theo mô hình yêu cầu-phản hồi truyền thống không giải quyết được các vòng lặp suy luận lặp đi lặp lại.
- **Agent hành động tự chủ:** Agent gọi công cụ, sửa đổi dữ liệu và tương tác với các hệ thống bên ngoài mà không cần chỉ thị rõ ràng của con người ở từng bước. Tính tự chủ này đòi hỏi các biện pháp kiểm soát bảo mật, ranh giới quyền hạn và các mẫu giám sát của con người được thiết kế riêng cho các hoạt động tự chủ.
- **Hành vi của Agent mang tính ngẫu nhiên:** Các quyết định do LLM điều khiển vốn không xác định (non-deterministic), cùng một đầu vào có thể tạo ra các đầu ra khác nhau qua các lần gọi. Các chiến lược về độ tin cậy phải tính đến điều này thông qua giám sát hành vi, khung đánh giá, và suy giảm nhẹ nhàng (graceful degradation) thay vì chỉ dựa vào kiểm thử xác định.
- **Agent cộng tác:** Các hệ thống đa Agent tạo ra chi phí phối hợp, độ phức tạp trong bàn giao (handoff), và các dạng lỗi phân tán. Các mẫu điều phối, giao thức giao tiếp và cơ chế giải quyết xung đột trở thành những mối quan tâm kiến trúc hàng đầu.
- **Agent ghi nhớ:** Bộ nhớ bền vững xuyên suốt các phiên cho phép cá nhân hóa và học hỏi, nhưng lại đưa ra những thách thức về tính toàn vẹn dữ liệu, quyền riêng tư và quản lý chi phí mà các ứng dụng phi trạng thái (stateless) không gặp phải.

## AI tác nhân có trách nhiệm

Các Agent thực hiện hành động trong thế giới thực mang trọng trách lớn hơn các hệ thống chỉ tạo văn bản. Lens này lồng ghép các nguyên tắc **AI có trách nhiệm (responsible AI)** xuyên suốt các thực hành tốt nhất thay vì coi chúng là một mối quan tâm riêng biệt:

- **Tự chủ có giới hạn (bounded autonomy):** Mỗi Agent vận hành trong các ranh giới phạm vi được xác định rõ ràng, với các **Guardrails** ràng buộc hành vi bất kể đầu vào nhận được (xem [AGENTSEC04](2-security/4-agentsec04/index.md)).
- **Minh bạch và khả năng giải thích:** Các quyết định của Agent được ghi log, truy vết và có thể kiểm toán, cho phép các nhóm tái dựng chính xác điều đã diễn ra trong bất kỳ lần thực thi nào (xem [AGENTOPS05](1-operational-excellence/5-agentops05/index.md)).
- **Giám sát của con người:** Các mô hình giám sát phân tầng khớp mức độ rà soát của con người với rủi ro và khả năng đảo ngược của từng hành động Agent, bảo toàn phán đoán của con người ở nơi quan trọng nhất (xem [AGENTREL02-BP05](3-reliability/2-agentrel02/agentrel02-bp05.md)).
- **Căn chỉnh mục tiêu (goal alignment):** Các khung đánh giá liên tục thẩm định liệu Agent có đạt được các mục tiêu dự kiến hay theo đuổi những mục tiêu lệch hướng (xem [AGENTOPS06](1-operational-excellence/6-agentops06/index.md)).
- **Tính bền vững tổ chức:** Việc áp dụng Agent giúp bảo toàn chuyên môn quan trọng của con người và tri thức thể chế thay vì tạo ra sự phụ thuộc vào những hệ thống mà chỉ nhà phát triển ban đầu mới hiểu (xem [AGENTSUS03](6-sustainability/3-agentsus03/index.md)).

## Bối cảnh công nghệ agentic AI trên AWS

Lens này được xây dựng xoay quanh các dịch vụ AWS và các framework mã nguồn mở tạo nền tảng cho agentic AI cấp sản xuất:

- **Amazon Bedrock** cung cấp quyền truy cập vào các mô hình nền tảng (foundation model) từ nhiều nhà cung cấp, bao gồm Anthropic, OpenAI, Meta, Amazon, Mistral, NVIDIA và những nhà cung cấp khác, kèm theo các khả năng tích hợp sẵn cho Guardrails, cơ sở tri thức (knowledge base), quản lý Prompt và đánh giá mô hình.
- **Amazon Bedrock AgentCore** cung cấp hạ tầng chuyên dụng để triển khai và vận hành Agent ở quy mô lớn. AgentCore trung lập với framework và trung lập với mô hình. Nó được thiết kế để hỗ trợ các framework agentic như Strands Agents, LangGraph, CrewAI, hoặc framework của riêng bạn, cùng với các nhà cung cấp mô hình lớn. Các khả năng của nó bao gồm Runtime cho việc lưu trữ Agent kiểu serverless, Gateway cho tích hợp công cụ tương thích MCP, Memory cho quản lý trạng thái Agent, Identity cho xác thực Agent, Observability cho truy vết phân tán, Evaluations cho đánh giá chất lượng, và Policy cho kiểm soát truy cập dựa trên Cedar.
- **Strands Agents** là một framework mã nguồn mở, hướng mô hình (model-driven) để xây dựng Agent với hỗ trợ gốc cho công cụ MCP, giao thức A2A, và các mẫu đa Agent (Graph, Swarm và Workflow). Strands hỗ trợ nhiều nhà cung cấp mô hình bao gồm Amazon Bedrock, Anthropic, OpenAI, Ollama và những nhà cung cấp khác.
- **MCP và A2A** là các giao thức mở cho giao tiếp Agent-tới-công cụ và Agent-tới-Agent, cho phép khả năng tương tác (interoperability) giữa các framework, nền tảng và hệ sinh thái Agent rộng lớn hơn.
- **Kiro** là một IDE agentic giúp tăng tốc phát triển Agent thông qua các luồng công việc hướng đặc tả (spec-driven), các tệp định hướng (steering files) cho tiêu chuẩn của nhóm, và các hook cho kiểm tra chất lượng tự động.

## Về Lens này

Lens này được tổ chức xoay quanh sáu trụ cột (pillar) của AWS Well-Architected Framework, mỗi trụ cột được điều chỉnh để giải quyết những đặc điểm riêng của các hệ thống agentic AI:

- **Operational excellence (Xuất sắc trong vận hành):** Vận hành và cải tiến các hệ thống Agent tự chủ thông qua các thực hành vận hành có hệ thống, bao gồm quản lý vòng đời Prompt, giám sát hành vi và quản trị có con người trong vòng lặp (human-in-the-loop).
- **Security (Bảo mật):** Bảo vệ danh tính Agent, quyền truy cập công cụ và các luồng dữ liệu, đồng thời chống lại tấn công tiêm nhiễm Prompt (prompt injection), leo thang đặc quyền và thao túng các hoạt động tự chủ.
- **Reliability (Độ tin cậy):** Xây dựng các hệ thống Agent thực thi tác vụ một cách dự đoán được, tự động phục hồi sau lỗi và duy trì chức năng một phần trong các điều kiện bất lợi.
- **Performance efficiency (Hiệu quả hiệu năng):** Tối ưu hóa các đường ống nhận thức (cognitive pipeline), lựa chọn mô hình, truy cập bộ nhớ và phối hợp đa Agent để mang lại hiệu năng Agent phản hồi nhanh và có thể mở rộng.
- **Cost optimization (Tối ưu chi phí):** Thiết kế Agent với chi phí là yếu tố cân nhắc hàng đầu, điều chỉnh đúng kích thước các khả năng của mô hình và bộ nhớ, và triển khai khả năng hiển thị chi phí đầy đủ.
- **Sustainability (Tính bền vững):** Xây dựng các hệ thống Agent với kiến trúc mô-đun, tái sử dụng nhằm tối đa hóa hiệu quả tài nguyên và duy trì các mẫu áp dụng bền vững.

## Cách sử dụng Lens này

Lens này được thiết kế để sử dụng cùng với [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html). Mỗi trụ cột trong Lens này chứa các vùng trọng tâm (focus area) với các câu hỏi định hướng, thực hành tốt nhất, hướng dẫn triển khai và ví dụ mã dành riêng cho các workload agentic AI.

Hãy sử dụng Lens này khi:

- Thiết kế một hệ thống agentic AI mới hoặc bổ sung năng lực agentic cho một ứng dụng hiện có
- Rà soát một triển khai agentic AI hiện có để tìm các cải tiến kiến trúc
- Đánh giá hồ sơ độ tin cậy, bảo mật hoặc chi phí của một luồng công việc dựa trên Agent
- Thiết lập các tiêu chuẩn tổ chức cho phát triển và vận hành agentic AI

## Lộ trình của Lens

Không phải nhóm nào cũng cần mọi thực hành tốt nhất. Hãy dùng các lộ trình đọc sau dựa trên vị trí của bạn trong hành trình agentic AI:

**Xây dựng Agent đầu tiên của bạn**

Bắt đầu với các thực hành nền tảng thiết lập phạm vi Agent, ranh giới bảo mật và hành vi có thể dự đoán được:

- [AGENTOPS01: Xác định vai trò của Agent, tiêu chí thành công và quy trình bàn giao](1-operational-excellence/1-agentops01/index.md)
- [AGENTREL02: Thiết kế cho các tác vụ nguyên tử, quyền hạn tối thiểu và giao thức chỉ thị rõ ràng](3-reliability/2-agentrel02/index.md)
- [AGENTSEC03: Thiết lập danh tính Agent, truy cập theo đặc quyền tối thiểu và xác thực mạnh](2-security/3-agentsec03/index.md)
- [AGENTSEC08: Xác thực đầu vào và lọc đầu ra trước khi lên sản xuất](2-security/8-agentsec08/index.md)

**Chuyển sang môi trường sản xuất**

Bổ sung khả năng quan sát (observability), đánh giá, kiểm soát chi phí và tối ưu hóa đường ống nhận thức:

- [AGENTOPS05: Triển khai truy vết, phát hiện bất thường và bảng điều khiển vận hành](1-operational-excellence/5-agentops05/index.md)
- [AGENTOPS06: Thiết lập khung kiểm thử và đánh giá với LLM-làm-giám-khảo (LLM-as-judge)](1-operational-excellence/6-agentops06/index.md)
- [AGENTPERF02: Tối ưu hóa các đường ống nhận thức, lựa chọn mô hình và đường thực thi](4-performance-efficiency/2-agentperf02/index.md)
- [AGENTCOST01: Kiểm soát chi phí vòng lặp suy luận và chi phí phối hợp đa Agent](5-cost-optimization/1-agentcost01/index.md)
- [AGENTCOST02: Điều chỉnh đúng kích thước lựa chọn mô hình và tối ưu hóa tiêu thụ Token](5-cost-optimization/2-agentcost02/index.md)

**Mở rộng lên các hệ thống đa Agent**

Giải quyết độ tin cậy điều phối, bảo mật phối hợp và hiệu năng luồng công việc:

- [AGENTREL04: Triển khai các mẫu trọng tài (arbiter), phân loại năng lực và cơ chế dự phòng](3-reliability/4-agentrel04/index.md)
- [AGENTPERF05: Tối ưu hóa các mẫu điều phối và mô hình cộng tác đa Agent](4-performance-efficiency/5-agentperf05/index.md)
- [AGENTSEC06: Bảo vệ giao tiếp giữa các Agent, ranh giới tin cậy và phối hợp](2-security/6-agentsec06/index.md)
- [AGENTCOST05: Triển khai quy kết chi phí trên các luồng công việc đa Agent](5-cost-optimization/5-agentcost05/index.md)

**Củng cố một triển khai hiện có**

Tăng cường các biện pháp kiểm soát bảo mật, khả năng chống chịu và giám sát của con người:

- [AGENTSEC04: Triển khai Guardrails và con người trong vòng lặp cho các quyết định trọng yếu](2-security/4-agentsec04/index.md)
- [AGENTSEC07: Bảo vệ hoạt động giám sát của con người và phát hiện Agent lừa đảo (rogue agent)](2-security/7-agentsec07/index.md)
- [AGENTREL06: Tích hợp tin cậy với các hệ thống cũ (legacy) bằng cơ chế dự phòng và tính bất biến (idempotency)](3-reliability/6-agentrel06/index.md)

## Tính khả dụng của Lens

Các custom lens mở rộng hướng dẫn thực hành tốt nhất được cung cấp bởi AWS Well-Architected Tool. AWS WA Tool cho phép bạn tạo [custom lens](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html) của riêng mình, hoặc sử dụng các lens do người khác tạo và chia sẻ với bạn.

Để bắt đầu rà soát workload agentic AI của bạn, hãy tải về và nhập [Agentic AI Lens](https://github.com/aws-samples/sample-well-architected-custom-lens/blob/main/agentic-ai-lens/agentic-ai-lens.json) vào AWS WA Tool từ [kho GitHub custom lens AWS Well-Architected](https://github.com/aws-samples/sample-well-architected-custom-lens) công khai.
