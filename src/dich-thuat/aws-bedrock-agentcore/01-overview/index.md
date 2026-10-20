---
title: "Tổng quan"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---

# Tổng quan

## Amazon Bedrock AgentCore là gì?

Amazon Bedrock AgentCore là một nền tảng agentic để xây dựng, triển khai và vận hành các agent (tác tử AI) có hiệu quả cao một cách bảo mật ở quy mô lớn, sử dụng bất kỳ framework và mô hình nền tảng (foundation model) nào. Với AgentCore, bạn có thể cho phép agent thực hiện hành động trên các tool (công cụ) và dữ liệu với đúng quyền hạn và cơ chế quản trị, chạy agent một cách bảo mật ở quy mô lớn, đồng thời giám sát hiệu năng và chất lượng của agent trong môi trường production — tất cả mà không cần quản lý hạ tầng. Các dịch vụ AgentCore hoạt động cùng nhau hoặc độc lập với bất kỳ framework mã nguồn mở nào như CrewAI, LangGraph, LlamaIndex và Strands Agents, cũng như với bất kỳ mô hình nền tảng nào, nên bạn không phải đánh đổi giữa sự linh hoạt của mã nguồn mở với tính bảo mật và độ tin cậy cấp doanh nghiệp.

## Các dịch vụ cốt lõi trong Amazon Bedrock AgentCore

Amazon Bedrock AgentCore bao gồm các dịch vụ và khả năng dạng module sau đây, mà bạn có thể dùng cùng nhau hoặc độc lập:

| Dịch vụ | Mô tả | Tích hợp |
| --- | --- | --- |
| [Harness](/dich-thuat/aws-bedrock-agentcore/04-harness/) | Một agent loop (vòng lặp agent) được quản lý, cho phép bạn định nghĩa và gọi các agent AI chỉ với một lời gọi API. Chỉ định model, system prompt và tool ngay tại chỗ. Harness (khung điều phối) lo phần orchestration, thực thi tool, quản lý bộ nhớ và tạo phản hồi. Mỗi session chạy trong một microVM cô lập với quyền truy cập filesystem và shell, hỗ trợ các trường hợp dùng như sinh code, phân tích dữ liệu và deep research. Bạn có thể mang container image riêng cho các môi trường tùy chỉnh với dependency bổ sung. | AgentCore Harness hoạt động với Amazon Bedrock, OpenAI, Google Gemini và bất kỳ nhà cung cấp model tương thích OpenAI nào. Tích hợp với AgentCore Memory, Gateway, Browser, Code Interpreter và Observability. Hỗ trợ remote MCP server, hàm inline và môi trường container tùy chỉnh. |
| [Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/) | Một môi trường runtime (môi trường chạy) serverless, bảo mật, được xây dựng chuyên biệt để triển khai và mở rộng các agent AI cũng như tool động. Runtime cung cấp cold start nhanh cho tương tác thời gian thực, hỗ trợ runtime kéo dài cho các agent bất đồng bộ, cô lập session thực sự, danh tính (identity) tích hợp sẵn và hỗ trợ các khối lượng công việc agentic đa phương thức và đa agent. | AgentCore Runtime hoạt động với các framework tùy chỉnh và bất kỳ framework mã nguồn mở nào, bao gồm CrewAI, LangGraph, LlamaIndex, Google ADK, OpenAI Agents SDK và Strands Agents, bất kỳ mô hình nền tảng nào trong hoặc ngoài Amazon Bedrock bao gồm OpenAI, Gemini của Google, Claude của Anthropic, Amazon Nova, Meta Llama và các model Mistral, cùng các giao thức phổ biến như MCP và A2A. |
| [Memory](/dich-thuat/aws-bedrock-agentcore/07-memory/) | Một cách để xây dựng các agent nhận biết ngữ cảnh với toàn quyền kiểm soát những gì agent ghi nhớ và học hỏi. Hỗ trợ cả short-term memory (bộ nhớ ngắn hạn) cho hội thoại nhiều lượt và long-term memory (bộ nhớ dài hạn) tồn tại qua các session, với khả năng không chỉ chia sẻ kho memory (bộ nhớ) giữa các agent mà còn học hỏi từ kinh nghiệm. | AgentCore Memory hoạt động với LangGraph, LangChain, Strands, LlamaIndex |
| [Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/) | Một cách bảo mật để chuyển đổi các API, hàm Lambda và dịch vụ hiện có của bạn thành các tool tương thích Model Context Protocol (MCP), đồng thời kết nối với các MCP server có sẵn, giúp chúng khả dụng cho các agent AI qua các endpoint của Gateway (cổng) chỉ với vài dòng code. | Bất kỳ API, MCP tool, Lambda nào, và các tích hợp phổ biến bao gồm Salesforce, Zoom, JIRA, Slack, v.v. |
| [Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/) | Một dịch vụ quản lý danh tính, truy cập và xác thực agent bảo mật, có khả năng mở rộng, tương thích với các nhà cung cấp danh tính hiện có, loại bỏ nhu cầu di chuyển người dùng hoặc xây dựng lại luồng xác thực. | Bất kỳ IdP và nhà cung cấp credential nào như Amazon Cognito, Okta, Microsoft Azure Entra ID, Auth0, v.v. |
| [Code Interpreter](/dich-thuat/aws-bedrock-agentcore/11-code-interpreter/) | Một môi trường sandbox cô lập để agent thực thi code, nâng cao độ chính xác và mở rộng khả năng giải quyết các tác vụ phức tạp đầu-cuối. | Nhiều ngôn ngữ bao gồm Python, JavaScript và TypeScript |
| [Browser](/dich-thuat/aws-bedrock-agentcore/12-browser/) | Một môi trường runtime trình duyệt trên đám mây nhanh và bảo mật, cho phép các agent AI tương tác với ứng dụng web, điền form, điều hướng website và trích xuất thông tin trong một môi trường được quản lý hoàn toàn. | Bất kỳ mô hình nền tảng nào hoặc các framework tự động hóa trình duyệt phổ biến bao gồm Playwright và BrowserUse |
| [Observability](/dich-thuat/aws-bedrock-agentcore/13-observability/) | Một góc nhìn hợp nhất để trace, gỡ lỗi và giám sát hiệu năng agent trong production. Nó cung cấp các trực quan hóa chi tiết cho từng bước trong quy trình làm việc của agent, cho phép bạn kiểm tra đường thực thi của agent, kiểm toán các output trung gian, và gỡ lỗi các điểm nghẽn hiệu năng cũng như lỗi. | Bất kỳ ngăn xếp giám sát và observability (khả năng quan sát) nào tích hợp với dữ liệu telemetry được phát ra theo định dạng chuẩn tương thích OpenTelemetry (OTEL) |
| [Payments](/dich-thuat/aws-bedrock-agentcore/10-payments/) | Một dịch vụ được quản lý hoàn toàn cho phép các thanh toán microtransaction để agent AI truy cập các API trả phí, MCP server và nội dung, sử dụng giao thức x402 và Machine Payments Protocol (MPP). Payments cung cấp tích hợp ví, giới hạn chi tiêu có thể cấu hình, và observability đầu-cuối cho các hoạt động thanh toán của agent. | AgentCore payments hỗ trợ các nhà cung cấp ví Coinbase CDP và Stripe (Privy), AgentCore Gateway, Strands Agents, bất kỳ endpoint tương thích x402 hoặc MPP nào, AgentCore Identity và AgentCore Observability được hỗ trợ bởi Amazon CloudWatch để giám sát hợp nhất. |
| [Evaluations](/dich-thuat/aws-bedrock-agentcore/16-evaluations/) | Một dịch vụ đánh giá được xây dựng chuyên biệt cho việc đánh giá agent tự động, nhất quán và dựa trên dữ liệu. AgentCore Evaluations đo lường mức độ tốt của agent và tool trong việc thực thi tác vụ, xử lý các trường hợp biên và duy trì độ tin cậy của output trên nhiều loại đầu vào và ngữ cảnh khác nhau. Evaluations cung cấp các tín hiệu chất lượng có thể đo lường, giúp các nhóm tối ưu hiệu năng bằng những hiểu biết có cấu trúc, và đảm bảo agent của bạn đáp ứng các tiêu chuẩn về chức năng và hành vi trước và sau khi triển khai. | AgentCore Evaluations hỗ trợ đánh giá trên các session, trace và span được tạo ra từ framework Strands Agent hoặc LangGraph, và được instrument bằng OpenTelemetry hoặc OpenInference. Tất cả kết quả được tích hợp vào AgentCore Observability được hỗ trợ bởi Amazon CloudWatch để giám sát hợp nhất. |
| [Optimization](/dich-thuat/aws-bedrock-agentcore/17-optimization/) | Một dịch vụ cải tiến liên tục sử dụng các khuyến nghị do AI tạo ra, các gói cấu hình có phiên bản và A/B testing để cải thiện hiệu năng agent thông qua những thay đổi cấu hình dựa trên dữ liệu. Thay vì tối ưu thủ công dựa trên phỏng đoán, bạn hướng dịch vụ vào các trace của agent để sinh ra cải tiến và xác thực chúng bằng các thí nghiệm có kiểm soát. | AgentCore optimization xây dựng trên AgentCore Evaluations và hoạt động với các agent được instrument bằng OpenTelemetry qua AgentCore Observability. Hỗ trợ tối ưu system prompt và mô tả tool với việc phân chia lưu lượng qua AgentCore Gateway để A/B testing. |
| [Policy](/dich-thuat/aws-bedrock-agentcore/15-policy-in/) | Một khả năng cung cấp kiểm soát tất định để đảm bảo các agent hoạt động trong các ranh giới và quy tắc nghiệp vụ đã định mà không làm chậm chúng. Dễ dàng soạn thảo các quy tắc chi tiết bằng ngôn ngữ tự nhiên hoặc [Cedar](https://www.cedarpolicy.com/en) (ngôn ngữ policy mã nguồn mở của AWS). | Tích hợp với AgentCore Gateway, để chặn mọi lời gọi tool trước khi thực thi. Bạn có thể định nghĩa những tool nào agent có thể truy cập, chúng có thể thực hiện hành động gì, và trong điều kiện nào. |
| [Registry](/dich-thuat/aws-bedrock-agentcore/18-aws-agent-registry/) | Một catalog tập trung để khám phá và quản lý các agent, MCP server, tool, skill và tài nguyên tùy chỉnh trên toàn tổ chức của bạn. Registry cung cấp một quy trình được quản trị để xuất bản, xem xét và phê duyệt tài nguyên, với tìm kiếm lai (hybrid) kết hợp ngữ nghĩa và từ khóa để các agent và nhà phát triển có thể tìm đúng tool. | AgentCore Registry hoạt động với bất kỳ MCP Server, Agent, Skill hay Custom Resource nào, được triển khai trên AWS, on-prem hoặc trên bất kỳ môi trường đám mây nào khác. |

## Bạn có thể xây dựng gì với Amazon Bedrock AgentCore?

Với Amazon Bedrock AgentCore, các nhà phát triển có thể đưa các agent AI vào production nhanh hơn với quy mô, độ tin cậy và tính bảo mật thiết yếu cho việc triển khai trong thực tế. Một số trường hợp dùng phổ biến mà bạn nên cân nhắc tận dụng AgentCore là:

- **Agents**

    Xây dựng các ứng dụng AI tự chủ có khả năng suy luận, dùng tool và duy trì ngữ cảnh. Triển khai các agent cho hỗ trợ khách hàng, tự động hóa quy trình làm việc, phân tích dữ liệu hoặc hỗ trợ lập trình. Agent của bạn chạy serverless với các session cô lập, memory bền vững và observability tích hợp sẵn.

- **Tools và Model Context Protocol (MCP) Servers**

    Biến các API, cơ sở dữ liệu hoặc dịch vụ hiện có thành các tool mà bất kỳ agent tương thích MCP nào cũng có thể dùng. Triển khai một gateway bọc quanh các hàm Lambda hoặc OpenAPI spec của bạn, giúp backend của bạn truy cập được ngay lập tức cho các agent mà không cần viết lại code.

- **Agent Platforms**

    Cung cấp cho các nhà phát triển nội bộ hoặc khách hàng của bạn một con đường sẵn sàng để xây dựng và triển khai agent bằng các tool đã được phê duyệt, các kho memory dùng chung và quyền truy cập được quản trị vào các dịch vụ doanh nghiệp. Tập trung hóa observability, xác thực và tuân thủ trong khi cho phép các nhóm ra mắt các tính năng do agent hỗ trợ nhanh hơn.

## Định giá cho Amazon Bedrock AgentCore

AgentCore cung cấp mô hình định giá linh hoạt, dựa trên mức tiêu thụ, không có cam kết trả trước hoặc phí tối thiểu. Để biết thêm thông tin, xem [Định giá AgentCore](https://aws.amazon.com/bedrock/agentcore/pricing/). AgentCore có thể dùng và lưu trữ nội dung của bạn để cải thiện trải nghiệm dịch vụ hoặc hiệu năng cho bạn. Những cải tiến đó là để phục vụ việc sử dụng AgentCore của chính bạn chứ không phải cho các khách hàng khác.

## Bước tiếp theo

Nếu bạn là người dùng lần đầu của Amazon Bedrock AgentCore, chúng tôi khuyên bạn bắt đầu bằng cách đọc các mục sau:

- [Bắt đầu với AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html)

- [Tìm hiểu các giao diện sẵn có để sử dụng Amazon Bedrock AgentCore](/dich-thuat/aws-bedrock-agentcore/05-understand-the-available-interfaces-for-/)
