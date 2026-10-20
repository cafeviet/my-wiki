---
title: "AgentCore harness"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html"
---

# AgentCore harness

Mỗi agent (tác tử AI) đều có một lớp orchestration (điều phối): một vòng lặp gọi model, chọn tool (công cụ), truyền kết quả trở lại, quản lý ngữ cảnh và xử lý lỗi. Chạy nó trong production đòi hỏi hạ tầng thực sự bên dưới: compute, một sandbox, các kết nối tool bảo mật, filesystem, memory (bộ nhớ), identity (danh tính) và observability (khả năng quan sát). Cùng nhau, chúng tạo thành **agent harness**, hệ thống cho phép một agent thực sự chạy được.

Dựng một cái cục bộ thì nhanh. Production mới là nơi khối lượng công việc bùng nổ, và ngay khoảnh khắc nó phải phục vụ nhiều hơn một người dùng, cả một lớp mới xuất hiện: đồng thời, cô lập, danh tính, trạng thái, mở rộng. Cho đến nay, mỗi nhóm đều phải tự làm phần việc đó.

Harness (khung điều phối) được quản lý trong AgentCore biến công việc đó thành cấu hình. Bạn khai báo agent của bạn làm gì (model, tool, skill, chỉ dẫn); AgentCore lo phần **môi trường, compute, memory, identity, mạng và observability** biến cấu hình thành một agent đang chạy. Thử một model khác hoặc thêm một tool mới là một thay đổi cấu hình, không phải một lần viết lại code.

Mỗi session harness đều có trạng thái theo mặc định và chạy trong một **microVM cô lập cho mỗi session** (được hỗ trợ bởi AgentCore runtime (môi trường chạy)). Agent có **filesystem và shell** riêng, nên nó có thể viết code, thực thi code, và có thể lưu bền **các bộ nhớ ngắn hạn và dài hạn (short-term và long-term memories)** cùng các tệp qua các session, kể cả khi session microVM bên dưới đã hết hạn và được thay bằng một session mới. Các agent có thể dùng **bất kỳ model nào** do Amazon Bedrock, OpenAI, Google Gemini cung cấp, hoặc bất kỳ nhà cung cấp tương thích LiteLLM nào, và có thể **đổi nhà cung cấp giữa chừng session** mà không mất ngữ cảnh, nên bạn có thể lập kế hoạch với một model và thực thi với model khác, hoặc hoán đổi nhà cung cấp để kiểm thử tương quan giá/hiệu năng mà không phải dựng lại cuộc hội thoại. Các agent có thể kết nối tới tool qua **[AgentCore gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), [MCP server](https://modelcontextprotocol.io/), hoặc dùng [browser](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html) hay [code interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html) tích hợp sẵn**. Bạn có thể gắn **các AWS skill từ Git, S3, hoặc catalog AWS skills đã được tuyển chọn** chỉ bằng một công tắc, để agent tiếp nhận chuyên môn theo lĩnh vực khi cần thay vì tự ứng biến. Khi bạn cần một môi trường tùy chỉnh với các dependency riêng, bạn có thể **mang container của riêng bạn.** Bạn cũng có thể **mount S3 Files hoặc EFS** để chia sẻ dữ liệu qua các session và harness với đầy đủ độ bền và lịch sử của S3. **Mọi hành động đều được trace tự động** qua AgentCore observability, với một góc nhìn hợp nhất phơi bày những gì agent đã làm trên mọi khả năng ở một nơi, nên bạn không còn phải nhảy qua lại giữa các log group để ráp lại xem chuyện gì đã xảy ra.

Bạn có thể lặp trên lưu lượng thực với AgentCore evaluations và optimization để **chấm điểm hành vi, nhận các khuyến nghị về prompt và mô tả tool, và chạy A/B test với báo cáo ý nghĩa thống kê** theo từng session. Sau đó, triển khai các thay đổi an toàn với **các phiên bản bất biến và các endpoint có tên**, và roll back tức thì bằng cách trỏ một endpoint về một phiên bản trước đó. Bạn có thể thả một harness vào một pipeline lớn hơn qua trạng thái AgentCore InvokeHarness trong AWS Step Functions, hoặc export sang code Strands (Claude Agent SDK sắp ra mắt) và chạy nó trên AgentCore runtime khi cấu hình là chưa đủ. Mọi thứ bạn cần để xây dựng, chạy và vận hành các agent production, mà không phải quản lý hạ tầng. Harness được cung cấp sức mạnh bởi [Strands Agents](https://strandsagents.com/), framework agent mã nguồn mở từ AWS.

Không có khoản phí harness riêng. Bạn chỉ trả cho các khả năng AgentCore bên dưới mà bạn dùng. Để biết chi tiết, xem [trang định giá AgentCore](https://aws.amazon.com/bedrock/agentcore/pricing/).

**AgentCore harness khả dụng ở dạng GA trên tất cả các region được hiển thị [tại đây](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html).**

- [Bắt đầu](/dich-thuat/aws-bedrock-agentcore/04-harness/harness-get-started)

- [Model và chỉ dẫn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-models.html)

- [Tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-tools.html)

- [Lifecycle hooks](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-lifecycle-hooks.html)

- [Skills](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-skills.html)

- [Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-memory.html)

- [Môi trường và filesystem](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-environment.html)

- [Interactive shells (terminals)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-command-shell.html)

- [Observability và kiểm soát chi phí](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-operations.html)

- [Quản lý phiên bản và endpoint của AgentCore harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-versioning.html)

- [Export harness sang code](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-export.html)

- [Bảo mật và kiểm soát truy cập](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-security.html)

- [AgentCore harness so với Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html)
