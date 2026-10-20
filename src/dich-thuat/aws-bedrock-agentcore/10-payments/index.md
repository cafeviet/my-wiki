---
title: "AgentCore payments: Cho phép thanh toán vi giao dịch an toàn cho AI agent"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments.html"
---

# AgentCore payments: Cho phép thanh toán vi giao dịch an toàn cho AI agent

# Amazon Bedrock AgentCore payments: Cho phép thanh toán vi giao dịch an toàn cho AI agent

## AWS Amazon Bedrock AgentCore payments là gì?

Amazon Bedrock AgentCore payments là một dịch vụ được quản lý hoàn toàn, cho phép thanh toán vi giao dịch (microtransaction) trong các AI agent (tác tử AI) để truy cập các API trả phí, MCP server và nội dung. AI agent ngày càng xử lý các tác vụ phức tạp bằng cách gọi API, truy cập MCP server và tương tác với các agent khác. Khi ngày càng nhiều dịch vụ kiếm tiền qua mô hình trả tiền theo mức dùng (pay-per-use), lập trình viên gặp thách thức khi tích hợp thanh toán vào các quy trình có tính agentic. Các giao dịch thường là vi giao dịch (thường dưới 1 đô la hoặc chỉ vài xu lẻ), khiến các phương thức thanh toán truyền thống trở nên tốn kém do phí giao dịch tối thiểu cao. Trong khi đó, các nhà cung cấp nội dung và nhà xuất bản đang đưa ra các paywall (tường phí) cho AI agent muốn truy cập nội dung của họ. AgentCore payments cung cấp một bộ năng lực thân thiện với lập trình viên, giúp bạn phát triển các giải pháp cho phép thanh toán an toàn, tức thì tới các dịch vụ trả phí bằng stablecoin, các giao thức mở như x402 cho vi giao dịch tiết kiệm chi phí, và các guardrail (rào chắn) có thể cấu hình để giúp kiểm soát chi tiêu của agent. Điều này có thể giảm công sức của lập trình viên từ nhiều tháng xuống còn vài ngày.

## Nó giải quyết vấn đề gì cho khách hàng?

Amazon Bedrock AgentCore payments giải quyết những thách thức mà lập trình viên agent gặp phải khi tích hợp năng lực thanh toán vào AI agent của họ. Theo cách truyền thống, lập trình viên phải thiết lập và quản lý các mối quan hệ thanh toán riêng với từng nhà cung cấp dịch vụ bên ngoài mà agent của họ cần truy cập, tạo ra chi phí vận hành và độ phức tạp. Bài toán kinh tế của các giao dịch agent-tới-người-bán đặt ra một thách thức cơ bản: các lệnh gọi API riêng lẻ hoặc yêu cầu nội dung thường có giá trị chỉ vài xu, trong khi các phương thức thanh toán truyền thống như thẻ tín dụng (khả dụng hạn chế do giới hạn địa lý) áp đặt phí giao dịch tối thiểu, khiến các vi giao dịch không khả thi về mặt kinh tế.

Ngoài cấu trúc chi phí, lập trình viên có thể phải tốn nhiều tháng công sức kỹ thuật để tích hợp ví (wallet) bên thứ ba, xây dựng hệ thống điều phối thanh toán, triển khai hỗ trợ cho các giao thức agentic mới nổi, xử lý các trường hợp biên và thiết lập observability (khả năng quan sát) đầu cuối trên các luồng thanh toán. Vì AI agent hoạt động tự động, lập trình viên thường phải xây dựng các khung quản trị và kiểm soát ngân sách từ đầu để ngăn chi tiêu vượt tầm kiểm soát, đồng thời hỗ trợ tuân thủ các quy định thanh toán và duy trì tiêu chuẩn bảo mật, việc này có thể phức tạp. Những yêu cầu này càng phức tạp hơn trong bối cảnh thanh toán. AgentCore payments giải quyết những thách thức này bằng cách cung cấp một dịch vụ được quản lý hoàn toàn, chuyên biệt, cho phép lập trình viên bổ sung năng lực thanh toán cho agent của họ chỉ với vài dòng mã.

## Các trường hợp sử dụng

Amazon Bedrock AgentCore payments hỗ trợ các trường hợp sử dụng mà AI agent cần truy cập động, trả theo mức dùng vào các tài nguyên và dịch vụ cao cấp.

- **Research (nghiên cứu)** — Các agent nghiên cứu có thể hoạt động với ngân sách được phân bổ, thông minh chọn và mua quyền truy cập các nguồn dữ liệu trả phí chuyên biệt theo nhu cầu để cung cấp thông tin chuyên sâu trong giới hạn chi phí.

- **Financial analysis (phân tích tài chính)** — Các nhà phân tích tài chính có thể dùng agent để trả tiền truy cập dữ liệu thị trường thời gian thực nằm sau paywall (chẳng hạn các cơ sở dữ liệu tài chính độc quyền và nền tảng giao dịch) để thực hiện phân tích và hỗ trợ quyết định đầu tư.

- **Browser agents (agent trình duyệt)** — Các agent trên trình duyệt (UI hoặc browser agent) có thể điều hướng và trích xuất nội dung từ các website kiếm tiền hoặc hạn chế truy cập bot, cho phép nghiên cứu tự động, thu thập dữ liệu và hoàn thành tác vụ ở quy mô lớn.

- **Pay-per-intelligence (trả theo trí tuệ)** — Các agent có thể định tuyến động các tác vụ đến mô hình AI tối ưu, chỉ trả tiền cho lượng token thực sự dùng thay vì duy trì đăng ký thuê bao trên nhiều nhà cung cấp mô hình.

- **On-demand storage (lưu trữ theo nhu cầu)** — Các agent có thể cấp phát tài nguyên lưu trữ tạm thời theo nhu cầu với mức giá trả theo mức dùng chi tiết, giúp giảm nhu cầu phân bổ dung lượng trước và giảm lãng phí.

Những năng lực này cho phép các quy trình tự động vốn trước đây không khả thi do rào cản thanh toán, đồng thời giúp lập trình viên kiểm soát chi phí và phân bổ tài nguyên tốt hơn.

## Các tính năng chính

Amazon Bedrock AgentCore payments cung cấp các năng lực sau để đơn giản hóa và bảo mật các thao tác thanh toán cho AI agent.

- **Orchestrating Payments (điều phối thanh toán)** — Với AgentCore payments, bạn có thể điều phối thanh toán bằng các chuẩn mở HTTP-native, bao gồm giao thức x402 và Machine Payments Protocol (MPP). Cả hai giao thức đều dùng mã trạng thái HTTP 402 Payment Required cho thanh toán lập trình. AgentCore payments quản lý toàn bộ vòng đời ở phía agent, từ nhận yêu cầu thanh toán của người bán, qua việc ký giao dịch bằng nhà cung cấp ví (wallet provider) đã cấu hình, đến việc trả về bằng chứng thanh toán mà agent gửi lại cho người bán. Nó xử lý các luồng nhiều bước và các ngoại lệ một cách tự động, cho phép các vi giao dịch agent-tới-người-bán thời gian thực vốn quá tốn kém với các phương thức thanh toán truyền thống (vốn áp phí tối thiểu).

- **Payment limits (giới hạn thanh toán)** — Các giới hạn thanh toán tích hợp giúp lập trình viên thiết lập kiểm soát ngân sách chi tiết ở cả cấp người dùng và cấp agent. Mỗi PaymentSession có một giới hạn ngân sách có thể cấu hình (maxSpendAmount, currency) và thời gian hết hạn. Khi phiên hết hạn hoặc đạt giới hạn ngân sách, các yêu cầu thanh toán tiếp theo bị từ chối. Nếu việc ký thanh toán thất bại sau khi đã trừ ngân sách, ngân sách không bị trừ cho khoản thanh toán thất bại đó.

- **Third-party wallet integration (tích hợp ví bên thứ ba)** — Dịch vụ cung cấp tích hợp ví an toàn với hai nhà cung cấp: CoinbaseCDP và Stripe(Privy) cho các thao tác ví stablecoin nhúng. Các thông tin nhạy cảm như API key và bí mật ví được lưu trữ qua AgentCore Identity (danh tính). AgentCore giúp lập trình viên giới hạn agent nào có thể truy cập tài nguyên ví.

- **Endpoint discoverability (khả năng khám phá endpoint)** — AgentCore payments cung cấp một Coinbase x402 Bazaar MCP server sẵn dùng, phơi bày hơn 10.000 endpoint x402 trả theo mức dùng thông qua AgentCore Gateway (cổng). Lập trình viên có thể duyệt và tìm kiếm các dịch vụ hỗ trợ x402 và thêm chúng làm target trong một Gateway qua console hoặc CLI.

- **Observability (khả năng quan sát)** — Observability đầu cuối thông qua Amazon CloudWatch mang lại tầm nhìn trên toàn bộ vòng đời thanh toán. Khách hàng có thể truy cập vended log (log ứng dụng được tự động phát tới CloudWatch log group của bạn) và vended span (bản ghi trace xem được trong AWS X-Ray) cho mỗi lệnh gọi data plane API, giúp lập trình viên giám sát tỷ lệ thành công của giao dịch, theo dõi các mẫu chi tiêu và chẩn đoán lỗi.

## Truy cập AgentCore payments

Bạn có thể tương tác với AWS AgentCore payments bằng cách gọi trực tiếp các API công khai của dịch vụ payments thông qua AWS CLI, AWS SDK, AgentCore SDK và AgentCore CLI. Để scaffold (dựng khung) các tài nguyên thanh toán và thêm một process payment tool vào agent, hãy dùng AgentCore Payments skill trong AWS agent toolkit. Tại thời điểm chạy (runtime), bạn có thể tích hợp xử lý thanh toán với các framework agent SDK được hỗ trợ như Strands Agents và LangGraph.

## Các dịch vụ liên quan

- **[AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/)** - Lưu trữ và liên kết (federate) an toàn các thông tin thanh toán để giúp triển khai nguyên tắc quyền tối thiểu (least permissions) khi truy cập. Các Coinbase API key và Stripe/Privy Wallet credential của bạn sẽ được lưu trữ an toàn tại đây dưới dạng PaymentCredentialProvider.

- **[AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/)** - Kết nối tới các MCP server trả phí, đảm bảo agent của bạn có quyền truy cập an toàn tới chúng qua AgentCore Gateway. Bạn cũng có thể tận dụng tích hợp sẵn có của Coinbase x402 Bazaar qua AgentCore Gateway để khám phá hàng ngàn MCP tool trả phí hiện có.

- **[AgentCore Browser](/dich-thuat/aws-bedrock-agentcore/12-browser/)** - AgentCore Browser, cùng với AgentCore payments, giúp bạn truy cập tự động và an toàn các website có paywall hỗ trợ x402.

- **[AgentCore Observability](/dich-thuat/aws-bedrock-agentcore/13-observability/)** - Giúp bạn truy vết, gỡ lỗi và giám sát hiệu năng của AI agent trong môi trường production. AgentCore payments cung cấp các metric và trace để bạn quan sát cho AI agent của mình.
