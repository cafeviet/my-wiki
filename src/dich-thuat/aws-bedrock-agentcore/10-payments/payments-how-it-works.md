---
title: "Cách hoạt động"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-how-it-works.html"
---

# Cách hoạt động

# Cách AgentCore payments hoạt động

Amazon Bedrock AgentCore payments cung cấp kết nối thanh toán, quản lý ví, giới hạn thanh toán, xử lý thanh toán và observability (khả năng quan sát) thanh toán. Sử dụng các thành phần và quy trình được mô tả trên trang này, bạn có thể cấu hình các nhà cung cấp thanh toán, kết nối với hạ tầng ví bên ngoài, và cho phép các agent (tác tử AI) của bạn tự chủ chi trả cho các API, MCP server và nội dung web bằng giao thức x402 hoặc Machine Payments Protocol (MPP).

## PaymentManager

Một PaymentManager là tài nguyên cấp cao nhất điều phối các thao tác thanh toán cho tài khoản AWS của bạn. Nó đại diện cho ranh giới cấu hình về cách các agent của bạn xác thực và tương tác với các nhà cung cấp thanh toán bên ngoài. Khi bạn tạo một PaymentManager, bạn chỉ định một loại authorizer và một IAM role, và dịch vụ sẽ provision một workload identity tương ứng trong AgentCore Identity (danh tính). Ví dụ, một nhà phát triển đang xây dựng một agent nghiên cứu truy cập các nguồn dữ liệu cao cấp sẽ tạo một PaymentManager duy nhất và gắn một hoặc nhiều PaymentConnector vào đó.

Mỗi PaymentManager:

- Có một định danh và ARN duy nhất

- Dùng ủy quyền `AWS_IAM` hoặc `CUSTOM_JWT` cho các thao tác data plane

- Quản lý một hoặc nhiều PaymentConnector dưới dạng tài nguyên con

Các trạng thái vòng đời của PaymentManager bao gồm:

- `CREATING` — Trạng thái ban đầu trong quá trình provision

- `READY` — Đang hoạt động và chấp nhận các cấu hình connector

- `UPDATING` — Một thay đổi cấu hình đang được áp dụng

- `CREATE_FAILED` — Provision thất bại

- `UPDATE_FAILED` — Thao tác cập nhật thất bại

Bạn tạo một PaymentManager bằng thao tác [CreatePaymentManager](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-create-manager.html). Để xem danh sách đầy đủ các thao tác PaymentManager, xem [Tài liệu tham chiếu API Payments](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreatePaymentManager.html).

## PaymentConnector

Một PaymentConnector tích hợp PaymentManager của bạn với một nhà cung cấp thanh toán bên ngoài như Coinbase hoặc Stripe (Privy). Mỗi connector tham chiếu một credential provider được lưu trong AgentCore Identity, sử dụng kết nối và lưu trữ bảo mật có sẵn cho các API key và secret của bạn.

AgentCore payments hỗ trợ các loại connector sau:

- [CoinbaseCDP](https://docs.cdp.coinbase.com/embedded-wallets/welcome) — Kết nối với Coinbase Developer Platform cho các thao tác ví crypto.

- [StripePrivy](https://docs.privy.io/basics/get-started/organization) — Kết nối với Stripe với hạ tầng ví Privy.

Các đặc điểm chính của connector:

- Mỗi PaymentConnector thuộc về đúng một PaymentManager

- Credential được lưu trong AWS Secrets Manager thông qua AgentCore Identity và được tham chiếu bằng ARN

- Các connector chia sẻ các trạng thái vòng đời cơ bản với PaymentManager (`CREATING`, `READY`, `UPDATING`, `CREATE_FAILED`, `UPDATE_FAILED`, `DELETE_FAILED`). Các connector Coinbase Quick create còn có thể báo thêm các trạng thái (`PENDING_AUTHENTICATION`, `PROVISIONING`, `AUTHENTICATION_EXPIRED`, `AUTHENTICATION_FAILED`) — xem mục tiếp theo.

Bạn tạo một connector bằng thao tác [CreatePaymentConnector](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-create-manager.html#payments-create-manager-create). Để xem danh sách đầy đủ các thao tác connector, xem [Tài liệu tham chiếu API Payments](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreatePaymentConnector.html).

### Quick create và Provision thủ công (Manual)

Bạn provision credential của một connector theo một trong hai cách. Chế độ bạn có thể dùng phụ thuộc vào nhà cung cấp thanh toán.

**Quick create (khuyến nghị)** — Quick create chỉ khả dụng cho các connector Coinbase. Bạn ủy quyền kết nối thông qua Coinbase bằng một lần đồng ý OAuth, và dịch vụ sau đó provision và lưu credential provider của Coinbase cho bạn. Bạn tạo connector với `provisionMode` đặt thành `QUICK_CREATE` và một danh sách credential rỗng. Connector chuyển sang `PENDING_AUTHENTICATION` và trả về một `authorizationUrl`. Sau khi bạn ủy quyền tại URL đó, dịch vụ provision credential và connector trở thành `READY`. `authorizationUrl` có hiệu lực khoảng 10 phút. Nếu nó hết hạn trước khi bạn ủy quyền, connector chuyển sang `AUTHENTICATION_EXPIRED` và bạn phải tạo lại nó.

**Manual** — Với provision thủ công, bạn mang API credential của nhà cung cấp của riêng bạn. Credential được lưu dưới dạng một PaymentCredentialProvider, và connector tham chiếu provider đó bằng ARN. Stripe (Privy) chỉ hỗ trợ provision thủ công.

Trong quá trình Quick create, một connector có thể báo các trạng thái bổ sung sau:

- `PENDING_AUTHENTICATION` — Đang chờ bạn ủy quyền tại `authorizationUrl`.

- `PROVISIONING` — Dịch vụ đang provision và lưu credential provider sau khi bạn ủy quyền.

- `AUTHENTICATION_EXPIRED` — `authorizationUrl` đã hết hạn trước khi bạn ủy quyền. Tạo lại connector để lấy một URL mới.

- `AUTHENTICATION_FAILED` — Ủy quyền không hoàn tất thành công.

Để có hướng dẫn từng bước, xem [phần bắt đầu nhanh](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-getting-started.html) hoặc [Tạo một Payment Manager và Connector](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-create-manager.html).

## Quản lý credential

AgentCore payments tích hợp với [AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/) để quản lý bảo mật các credential của nhà cung cấp thanh toán bên ngoài. Khi bạn tạo một PaymentConnector, dịch vụ tham chiếu một PaymentCredentialProvider trong AgentCore Identity. PaymentCredentialProvider lưu các credential đặc thù của nhà cung cấp (chẳng hạn Coinbase CDP API key và wallet secret, hoặc Privy app credential và authorization key) trong AWS Secrets Manager. Tại runtime, dịch vụ Payments truy xuất các authentication token qua API data plane `GetResourcePaymentToken` của Identity.

## Payment session và instrument

Payment session đại diện cho các ngữ cảnh thanh toán riêng lẻ giữa một agent và một người dùng cuối. Mỗi session có các giới hạn thanh toán có thể cấu hình (`maxSpendAmount`, `currency`) và một thời điểm hết hạn, cung cấp kiểm soát chi tiêu cho từng tương tác. Khi session hết hạn hoặc đạt giới hạn thanh toán, các yêu cầu thanh toán tiếp theo trong session đó sẽ bị từ chối.

Payment instrument đại diện cho credential thanh toán của người dùng cuối, chẳng hạn một địa chỉ ví crypto. Mỗi instrument gắn với một mạng blockchain cụ thể và có trạng thái `INITIATED`, `ACTIVE`, `FAILED` hoặc `DELETED`.

Tại runtime, agent tạo một session và instrument, sau đó gọi `ProcessPayment` khi agent gặp một tài nguyên trả phí. Dịch vụ điều phối toàn bộ vòng đời thanh toán (kiểm tra giới hạn thanh toán, kết nối bảo mật tới ví, và ký giao dịch trên cả x402 v1 và v2 cũng như Machine Payments Protocol (MPP)) thông qua PaymentConnector đã cấu hình.

Để biết thêm về các thao tác data plane, xem [Xử lý thanh toán](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-process-payment.html). Để xem đầy đủ các schema API, xem [CreatePaymentSession](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_CreatePaymentSession.html), [CreatePaymentInstrument](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_CreatePaymentInstrument.html), và [ProcessPayment](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_ProcessPayment.html) trong Tài liệu tham chiếu API.

## Xác thực và bảo mật

AgentCore payments triển khai xác thực và ủy quyền ở nhiều lớp. Để biết thêm chi tiết, tham khảo [IAM role và permission](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments-iam-roles.html).

## Nạp tiền vào ví (instrument)

Một payment instrument, sau khi được tạo, khởi đầu với 0 USDC. Agent không có quyền giao dịch qua instrument trừ khi khách hàng cấp quyền một cách tường minh. Các bước sau mô tả cách nạp tiền vào ví:

### Coinbase

- **Khởi chạy frontend được cung cấp bởi Coinbase** — Triển khai wallet hub của Coinbase trong dịch vụ của bạn. [Coinbase AgentCore template trên GitHub](https://github.com/coinbase/cdp-agentcore-template) cung cấp một frontend mẫu cho các Nhà phát triển Agent tích hợp AWS AgentCore SDK với Coinbase để cho phép người dùng đăng nhập, kết nối agent và onramp tiền. Ngoài ra, trong body phản hồi của API `CreatePaymentInstrument`, hãy lấy redirect URL từ `paymentInstrumentDetails.redirectUrl` để truy cập trực tiếp Coinbase WalletHub.

- **Nạp tiền vào ví** — Sau khi người dùng đăng nhập vào wallet hub, họ có thể nạp tiền vào ví bằng chuyển khoản crypto-to-crypto hoặc qua các phương thức thanh toán truyền thống như thẻ tín dụng (khả dụng hạn chế do giới hạn địa lý), thẻ ghi nợ, Apple Pay, Google Pay hoặc ACH

- **Cấp quyền cho agent** — Trong cùng wallet hub đó, người dùng có thể cấp hoặc thu hồi quyền cho agent, cho phép hoặc từ chối agent thao tác trên ví crypto mới tạo của người dùng.

### Stripe (Privy)

- **Khởi chạy frontend được cung cấp bởi Privy** — Triển khai wallet hub của Privy trong dịch vụ của bạn. [Privy AgentCore SDK trên GitHub](https://github.com/privy-io/aws-agentcore-sdk) cung cấp một frontend mẫu cho các Nhà phát triển Agent tích hợp AWS AgentCore SDK với Privy để cho phép người dùng đăng nhập, kết nối agent và onramp tiền.

- **Nạp tiền vào ví** — Sau khi người dùng đăng nhập vào wallet hub, họ có thể nạp tiền vào ví bằng chuyển khoản crypto-to-crypto hoặc qua các phương thức thanh toán truyền thống như thẻ tín dụng (khả dụng hạn chế do giới hạn địa lý), thẻ ghi nợ, Apple Pay, Google Pay hoặc ACH

- **Cấp quyền cho agent** — Trong cùng wallet hub đó, người dùng có thể cấp quyền cho agent, cho phép agent thao tác trên ví crypto mới tạo của người dùng.

## Kết nối tới các API trả phí, MCP server và nội dung

[AgentCore Gateway](/dich-thuat/aws-bedrock-agentcore/08-gateway/) (cổng) cho phép bạn kết nối tới các MCP server trả phí và endpoint API, đảm bảo agent của bạn truy cập chúng một cách bảo mật. Bạn cũng có thể dùng tích hợp có sẵn của [Coinbase x402 Bazaar](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-integrations.html#gateway-target-integrations-supported-apis-coinbase-bazaar) thông qua AgentCore Gateway để khám phá hàng nghìn MCP tool trả phí có sẵn.

[AgentCore Browser](/dich-thuat/aws-bedrock-agentcore/12-browser/) cho phép các agent tự chủ truy cập các website có tường phí (paywall) hỗ trợ x402, một cách bảo mật thông qua sự kết hợp giữa AgentCore Browser và payments.

## Luồng thanh toán

Các bước sau mô tả luồng runtime khi một agent truy cập một tài nguyên trả phí bằng giao thức x402.

- **Gọi tool** — Agent gọi một tool hoặc endpoint trả phí (ví dụ, `GET /premium-data`) qua AgentCore Gateway hoặc bằng cách gọi trực tiếp.

- **Yêu cầu thanh toán** — Merchant phản hồi bằng HTTP `402 Payment Required`, kèm một payload thanh toán chỉ định số tiền, người nhận, tài sản và mạng.

- **Kiểm tra giới hạn thanh toán** — AgentCore payments kiểm tra mức chi tiêu của session đang hoạt động so với các giới hạn đã cấu hình. Nếu giao dịch vượt quá giới hạn, request bị từ chối.

- **Ký thanh toán** — AgentCore payments truy xuất credential ví từ AgentCore Identity, dựng payment proof, và ký giao dịch thông qua đối tác bên ngoài đã cấu hình.

- **Thử lại kèm thanh toán** — Agent thử lại request gốc với payload thanh toán đã ký trong header `X-PAYMENT`.

- **Xác minh và quyết toán** — Merchant xác minh payment proof và quyết toán giao dịch on-chain. Khi xác minh thành công, merchant trả về nội dung được yêu cầu.

- **Cập nhật trạng thái** — AgentCore payments commit giao dịch và cập nhật sổ chi tiêu của session. Nếu bất kỳ bước nào thất bại, phần đặt trước cho giới hạn thanh toán được giải phóng và giao dịch được ghi nhận là `FAILED`.

Khi agent dùng Machine Payments Protocol (MPP) thay vì x402, luồng vẫn tương tự ngoại trừ các header thử thách (challenge) và credential. Với MPP, merchant trả payment challenge trong header `WWW-Authenticate: Payment` thay vì một payload x402. Agent sau đó thử lại request gốc với credential đã ký trong header `Authorization` thay vì header `X-PAYMENT`.

## Observability

[AgentCore Observability](/dich-thuat/aws-bedrock-agentcore/13-observability/) cung cấp khả năng hiển thị trên toàn bộ vòng đời thanh toán, mang lại log chi tiết, dashboard thời gian thực, và các số liệu có thể hành động cho phép nhà phát triển giám sát tỷ lệ giao dịch thành công, theo dõi các mẫu chi tiêu, chẩn đoán lỗi và tối ưu hiệu năng thanh toán.
