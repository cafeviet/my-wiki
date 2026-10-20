---
title: "Các khái niệm cốt lõi của AgentCore payments"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-concepts.html"
---

# Các khái niệm cốt lõi

# Các khái niệm cốt lõi của AgentCore payments

## Các persona chính

Các persona tương tác với AgentCore payments có thể khác nhau giữa các tổ chức. Sau đây là các persona chung thường gặp ở nhiều tổ chức.

- **Agent developer (lập trình viên agent)**: Các lập trình viên agent xây dựng các agent (tác tử AI) thực thi các microtransaction để truy cập các API trả phí, MCP server, và nội dung web. Họ xử lý các tác vụ quản trị như cấu hình spending guardrail, giám sát hoạt động thanh toán, và quản lý chính sách credential của ví. Họ thực hiện việc thiết lập control plane một lần (tạo PaymentManager và PaymentConnector) và tích hợp mã agent của họ với AgentCore payments SDK hoặc các data plane API để cho phép thực thi thanh toán tự chủ.

- **End user (người dùng cuối)**: Người dùng cuối tương tác với agent để đạt được một mục tiêu cụ thể. Họ có thể nạp số dư của agent thông qua các stablecoin dựa trên crypto hoặc các phương thức thanh toán truyền thống như thẻ tín dụng (khả dụng hạn chế do giới hạn địa lý), thẻ ghi nợ, Apple Pay, Google Pay, hoặc ACH để agent có thể thực thi giao dịch thay mặt họ, với quyền chi tiêu, giới hạn chi tiêu có thể cấu hình, và sự minh bạch đầy đủ về cách sử dụng khoản tiền của họ.

- **Merchant (nhà cung cấp)**: Merchant là các nhà cung cấp API, nhà cung cấp nội dung, và nhà vận hành dịch vụ, những người kiếm tiền từ sản phẩm của họ qua các mô hình trả tiền theo lượt dùng (pay-per-use). Họ đặt giá, chấp nhận thanh toán x402, và cung cấp nội dung hoặc dịch vụ được yêu cầu khi thanh toán được xác nhận.

## Các khái niệm chính

Sơ đồ sau cho thấy cách PaymentManager, PaymentConnector, payment session, và payment instrument liên hệ với nhau trong AgentCore payments.

### PaymentManager

Một PaymentManager là tài nguyên cấp cao nhất mà bạn tạo trong AWS account của mình để điều phối các thao tác thanh toán cho các agent AI. Mỗi PaymentManager có một tên, một cấu hình authorizer kiểm soát cách agent xác thực với data plane (`AWS_IAM` hoặc `CUSTOM_JWT`), và một IAM role mà dịch vụ assume tại runtime. Khi bạn tạo một PaymentManager, AgentCore payments cấp phát một workload identity tương ứng trong AgentCore Identity (danh tính). Mỗi PaymentManager có một định danh và ARN duy nhất, và quản lý một hoặc nhiều PaymentConnector dưới dạng tài nguyên con.

Cách bạn tổ chức các PaymentManager tùy thuộc vào nhu cầu của bạn. Ví dụ, các PaymentManager riêng cho các ứng dụng agent khác nhau, các môi trường khác nhau (production, staging, development), hoặc các nhóm khác nhau trong tổ chức của bạn.

### PaymentConnector

Một PaymentConnector tích hợp PaymentManager của bạn với một nhà cung cấp thanh toán bên ngoài. Mỗi connector tham chiếu đến một credential provider được lưu trong AgentCore Identity, đảm bảo rằng các credential nhạy cảm như API key và wallet secret không bao giờ được truyền trực tiếp đến Payments API. Các credential được lưu trong AWS Secrets Manager thông qua AgentCore Identity và được tham chiếu bằng ARN. Một PaymentConnector thuộc về đúng một PaymentManager, và một PaymentManager có thể có nhiều connector (ví dụ, một cho Coinbase và một cho Stripe).
AgentCore payments hỗ trợ các loại connector sau:

- **[CoinbaseCDP](https://docs.cdp.coinbase.com/wallets/non-custodial-wallets/overview)** — Kết nối tới Coinbase Developer Platform cho các thao tác ví crypto.

- **[StripePrivy](https://docs.privy.io/wallets/overview/embedded)** — Kết nối tới Stripe với hạ tầng ví Privy.

### PaymentSession

Một PaymentSession là một ngữ cảnh thanh toán có phạm vi (scoped) theo dõi chi tiêu cho một tương tác agent duy nhất. Mỗi session có một thời hạn hết hạn có thể cấu hình và tùy chọn kèm theo giới hạn chi tiêu (`maxSpendAmount`, `currency`) nhằm thực thi các giới hạn thanh toán. Khi session hết hạn hoặc đạt giới hạn thanh toán, các yêu cầu thanh toán tiếp theo trong session đó bị từ chối. Nếu một lần ký thanh toán (payment signing) thất bại sau khi đã trừ tiền, khoản tiền sẽ tự động được hoàn lại (rolled back).

### PaymentInstrument

Một PaymentInstrument đại diện cho một ví crypto nhúng (embedded crypto wallet) mà agent dùng để thanh toán cho các merchant thay mặt người dùng. Mỗi instrument gắn với một mạng blockchain cụ thể và có một trong các trạng thái sau: `INITIATED`, `ACTIVE`, `FAILED`, hoặc `DELETED`. Vì cùng một địa chỉ ví không thể được dùng trên nhiều chain, các lập trình viên duy trì các instrument riêng cho từng mạng được hỗ trợ (ví dụ, Ethereum và Solana). Loại instrument duy nhất được hỗ trợ là `EMBEDDED_CRYPTO_WALLET`.

### PaymentCredentialProvider

Một PaymentCredentialProvider là một credential provider chuyên biệt trong AgentCore Identity được thiết kế cho các giao thức thanh toán tiền mã hóa. Nó lưu trữ an toàn các credential đặc thù nhà cung cấp (chẳng hạn Coinbase CDP API key và wallet secret, hoặc thông tin app Privy và authorization key) trong AWS Secrets Manager. Tại runtime, dịch vụ Payments truy xuất các authentication token thông qua data plane API `GetResourcePaymentToken` của AgentCore Identity. Mỗi PaymentConnector duy trì ánh xạ 1:1 với một PaymentCredentialProvider.

### Giao thức x402

Giao thức x402 là một chuẩn thanh toán mở, HTTP-native, tái sử dụng mã trạng thái HTTP 402 cho các thanh toán trực tiếp, có thể lập trình. Khi một agent yêu cầu một tài nguyên trả phí, merchant phản hồi bằng HTTP `402 Payment Required` kèm theo một payment payload xác định số tiền, người nhận, tài sản (asset), và mạng (network). Agent ký thanh toán và thử lại yêu cầu với proof đã ký trong header `X-PAYMENT`. Merchant xác minh thanh toán và cung cấp nội dung.

### Machine Payments Protocol (MPP)

Machine Payments Protocol (MPP) là một chuẩn mở, HTTP-native cho các thanh toán có thể lập trình. Nó sử dụng luồng HTTP authentication challenge tiêu chuẩn. Khi một agent yêu cầu một tài nguyên trả phí, merchant phản hồi bằng HTTP `402 Payment Required` và một challenge `WWW-Authenticate: Payment` xác định các phương thức thanh toán, số tiền, người nhận, và các token được chấp nhận. Agent chuyển tiếp challenge tới AgentCore payments, dịch vụ này ký thanh toán và trả về một credential sẵn sàng gửi. Agent thử lại yêu cầu với credential trong header `Authorization`, và merchant xác minh thanh toán rồi cung cấp nội dung.

### Microtransaction

Một microtransaction là một khoản thanh toán giá trị nhỏ (thường tính bằng cent) cho một lần gọi API, gọi tool (công cụ), hoặc truy cập nội dung riêng lẻ. Các hệ thống thanh toán truyền thống có chi phí giao dịch tối thiểu, khiến chúng kém hiệu quả cho các khoản thanh toán dưới $0.01. AgentCore payments dùng tiền mã hóa và stablecoin để cho phép các khoản micropayment tiết kiệm chi phí.
