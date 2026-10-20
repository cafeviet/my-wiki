---
title: "Các khái niệm cốt lõi"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html"
---
# Các khái niệm cốt lõi

Trước khi dùng Policy trong Amazon Bedrock AgentCore, điều quan trọng là hiểu các khái niệm và thành phần chính phối hợp với nhau để cung cấp quản trị dựa trên policy cho các Agent (tác tử AI) của bạn.

###### Chủ đề

- [Gateway](#concept-gateway)

- [Gateway Target](#concept-gateway-target)

- [Principal types](#concept-principal-types)

- [Cedar](#concept-cedar)

- [Cedar Policy](#concept-cedar-policy)

- [Dogwood](#concept-dogwood)

- [Temporal policies](#concept-temporal-policy)

- [Guardrails](#concept-guardrails)

- [Policy session](#concept-policy-session)

- [Policy engine](#concept-policy-engine)

- [Cedar Schema](#concept-cedar-schema)

- [Cedar validation](#concept-cedar-validation)

- [Cedar analysis](#concept-cedar-analysis)

- [Policy authoring service](#concept-policy-authoring-service)

## Gateway

Một Amazon Bedrock AgentCore Gateway (cổng) cung cấp một endpoint để kết nối tới các MCP server và chuyển đổi các API cùng Lambda thành các tool tương thích MCP, tạo một điểm truy cập duy nhất để một Agent tương tác với các tool của nó. Một Gateway có thể có nhiều target, mỗi target đại diện cho một tool hoặc một tập tool khác nhau.

## Gateway Target

Một target định nghĩa các API hoặc hàm Lambda mà một Gateway sẽ cung cấp dưới dạng tool cho một Agent. Các target có thể là các hàm Lambda, các đặc tả OpenAPI, các model Smithy, hoặc các định nghĩa tool khác.

## Principal types

Các policy Cedar dùng principal để đại diện cho thực thể đưa ra một yêu cầu ủy quyền. Policy trong AgentCore hỗ trợ hai loại principal tùy theo cách AgentCore Gateway của bạn được cấu hình xác thực:

- **AgentCore::OAuthUser** - Đại diện cho những người dùng đã xác thực OAuth. Khi một AgentCore Gateway dùng ủy quyền OAuth, principal được tạo từ claim `sub` của JWT token. Các OAuth principal hỗ trợ tag chứa các JWT claim như username, scope, role, v.v.

- **AgentCore::IamEntity** - Đại diện cho những caller đã xác thực IAM. Khi một AgentCore Gateway dùng ủy quyền AWS_IAM, principal được tạo từ danh tính IAM của caller. Các IAM principal có thuộc tính `id` chứa IAM ARN (định dạng: `arn:aws:sts:::assumed-role/` đối với các assumed role), cho phép khớp `principal ==` ổn định. Xem [Policy conditions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-conditions.html) để biết chi tiết.

## Cedar

[Cedar](https://docs.cedarpolicy.com) là một ngôn ngữ policy mã nguồn mở do AWS phát triển để viết và thực thi các policy ủy quyền. Các policy Cedar dễ đọc với con người, có thể phân tích, và có thể được kiểm chứng theo một schema. Policy trong AgentCore dùng Cedar để cung cấp kiểm soát truy cập chính xác, có thể kiểm chứng cho các gateway tool.

## Cedar Policy

Một Cedar policy là một câu lệnh khai báo cho phép hoặc cấm truy cập các gateway tool. Mỗi policy chỉ định ai (principal) có thể thực hiện hành động gì (lời gọi tool) trên tài nguyên nào (gateway) dưới những điều kiện nào. Các policy được đánh giá cho mọi yêu cầu gọi tool.

## Dogwood

[Dogwood](https://dogwood-policy.github.io/dogwood/index.html) là một ngôn ngữ policy mã nguồn mở trên website Dogwood Policy, tương thích với Cedar: mọi policy Cedar hợp lệ cũng là một policy Dogwood hợp lệ, nên các policy Cedar hiện có của bạn hoạt động không cần thay đổi. Ngoài các điều kiện point-in-time bạn đã có thể biểu đạt, Dogwood còn hỗ trợ các điều kiện *temporal* nhận biết session và các *information provider*, chẳng hạn Guardrails, cung cấp các tín hiệu được tính toán cho một policy. Các policy Dogwood được đánh giá theo một policy session nhóm các yêu cầu liên quan.

## Temporal policies

Hầu hết các policy Cedar là stateless: mỗi yêu cầu được đánh giá riêng lẻ. Một *temporal policy* thêm các điều kiện phụ thuộc vào những gì đã xảy ra trước đó trong cùng session, chẳng hạn yêu cầu một phê duyệt trước, giới hạn tần suất một hành động chạy, hoặc giữ tổng cộng dồn dưới một ngưỡng. Các temporal policy được viết bằng Dogwood, vốn tương thích với Cedar, và được đánh giá theo một policy session nhóm các yêu cầu liên quan. Để biết thêm thông tin, xem [Temporal policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-temporal.html).

## Guardrails

Guardrails là các information provider mà một policy Dogwood có thể tham vấn nội tuyến (inline). Tại thời điểm đánh giá, một guardrail tính một tín hiệu content-safety cho yêu cầu — chẳng hạn điểm content-filter, prompt-attack, hoặc sensitive-information — và policy cho phép hoặc cấm hành động dựa trên kết quả đó. Để biết thêm thông tin, xem [Guardrails in policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-guardrails-in-policies.html).

## Policy session

Một policy session là một chuỗi các lời gọi Gateway liên quan được nhóm dưới một session ID, mà bạn cung cấp trên các yêu cầu trong header `x-amzn-bedrock-agentcore-policy-session-id`. Các temporal policy đánh giá theo một policy session: một điều kiện temporal chỉ xét các sự kiện đã ghi cho cùng session với yêu cầu đang được ủy quyền. Để biết thêm thông tin, xem [Policy sessions and identity propagation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-session-based-temporal.html).

## Policy engine

Policy engine là thành phần cốt lõi của Policy trong AgentCore, dùng để lưu trữ và đánh giá các policy Cedar. Khi bạn tạo các policy, chúng áp dụng cho mọi gateway được liên kết với engine, miễn là scope của policy khớp với yêu cầu. Với mỗi lời gọi tool, policy engine đánh giá tất cả các policy áp dụng được theo yêu cầu để xác định cho phép hay từ chối truy cập. Engine tự động thực thi ngữ nghĩa default-deny và forbid-wins.

## Cedar Schema

Một Cedar schema định nghĩa cấu trúc của các entity, action, và context để kiểm chứng policy. Policy engine tự động sinh ra một schema từ các định nghĩa tool của gateway, ánh xạ mỗi tool thành một action và định nghĩa các tham số input mong đợi. Schema đảm bảo các policy được kiểm chứng tại thời điểm tạo, bắt lỗi trước khi triển khai.

## Cedar validation

Cedar validation kiểm tra rằng các policy đúng cú pháp và tuân thủ schema. Khi bạn liên kết các policy với một gateway, policy engine kiểm chứng chúng theo schema được tự sinh để đảm bảo chúng tham chiếu các action hợp lệ, dùng đúng kiểu dữ liệu, và chỉ truy cập các trường context đã định nghĩa. Việc kiểm chứng bắt lỗi trước khi các policy được triển khai, ngăn các lỗi ủy quyền tại runtime.

## Cedar analysis

Cedar analysis dùng automated reasoning để xem xét các policy và phát hiện các vấn đề tiềm ẩn. Policy trong AgentCore dùng automated reasoning để nhận diện các policy luôn cho phép (không có điều kiện nào hạn chế truy cập) hoặc luôn từ chối (các forbid policy không có ngoại lệ), giúp đảm bảo các policy hiện thực đúng kiểm soát truy cập dự kiến thay vì quá dễ dãi hoặc hạn chế không cần thiết.

## Policy authoring service

Policy authoring service tự động chuyển các yêu cầu ủy quyền bằng ngôn ngữ tự nhiên thành các policy Cedar. Khi bạn gửi một policy bằng ngôn ngữ tự nhiên, dịch vụ sinh ra mã Cedar đúng cú pháp, kiểm chứng nó theo gateway schema, và chạy automated analysis để phát hiện các vấn đề tiềm ẩn. Điều này đảm bảo mọi policy được sinh ra đều hợp lệ và giúp nhận diện các quy tắc quá dễ dãi hoặc hạn chế trước khi triển khai.
