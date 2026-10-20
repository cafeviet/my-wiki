---
title: "Khái niệm và thuật ngữ"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-concepts.html"
---
# Khái niệm và thuật ngữ

###### Đã mở di trú (Migration Now Open)

AWS Agent Registry đã ra mắt dưới namespace mới `agent-registry`. Hỗ trợ cho namespace `bedrock-agentcore` ở giai đoạn public preview sẽ ngừng vào ngày 17 tháng 9 năm 2026. Về hướng dẫn di trú, xem [Comprehensive registry migration guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-faq.html).

## Registry

Một registry là một catalog tập trung mà bạn tạo trong tài khoản AWS của mình để tổ chức và quản lý các tài nguyên. Mỗi registry có một tên, một mô tả, một cấu hình ủy quyền kiểm soát cách các consumer truy cập các discoverable data-plane API cùng MCP endpoint, và một cấu hình phê duyệt xác định liệu các record có cần rà soát thủ công trước khi trở nên có thể khám phá hay không.

Cách bạn tổ chức các registry tùy thuộc vào nhu cầu của bạn — ví dụ, các registry chuyên biệt cho các loại tài nguyên khác nhau (một agent registry, một MCP server registry, một skill registry), các registry cho các giai đoạn phát triển khác nhau (production, QA, development), các registry độc lập cho các nhóm hoặc đơn vị kinh doanh khác nhau, hoặc một registry duy nhất cho toàn bộ tổ chức của bạn.

## Registry record

Một registry record đại diện cho metadata của một tài nguyên riêng lẻ được xuất bản vào một registry. Mỗi record ghi lại các metadata chính mô tả tài nguyên bên dưới — cung cấp thông tin về nó là gì, làm gì, và có thể tìm thấy như thế nào. Các record có một `name`, một `displayName` dễ đọc với con người (tùy chọn), một mô tả tùy chọn, một `recordVersion`, một `recordType` (`AGENT`, `MCP`, `SKILL`, hoặc `CUSTOM`), và các descriptor đặc thù theo loại tài nguyên mang nội dung thực tế. Tổ hợp `name` và `recordVersion` phải là duy nhất trong registry (dùng làm khóa khử trùng lặp), nên cùng một `name` có thể được tái sử dụng qua các phiên bản khác nhau của cùng một tài nguyên.

## Resource types

**MCP servers** — Các Model Context Protocol (MCP) server cung cấp các tool mà các Agent (tác tử AI) có thể khám phá và gọi. Một record MCP server chứa một định nghĩa server mô tả cấu hình của server và các định nghĩa tool cho tất cả các tool mà server cung cấp, bao gồm các tham số input và định dạng output của chúng. AWS Agent Registry kiểm chứng các record MCP server theo [MCP protocol schema](https://modelcontextprotocol.io/docs/getting-started/intro) để đảm bảo tính đúng đắn.

**Agents** — Các Agent là các chương trình tự trị có thể suy luận, lập kế hoạch, và thực hiện hành động để hoàn thành nhiệm vụ. Một record agent chứa một agent card mô tả các năng lực, kỹ năng, và giao diện giao tiếp của Agent theo đặc tả giao thức A2A [(Agent-to-Agent)](https://a2a-protocol.org/latest/). AWS Agent Registry kiểm chứng các record agent theo A2A protocol schema để đảm bảo tính đúng đắn.

**Skills** — Các skill là các năng lực có thể tái sử dụng, có thể được chia sẻ giữa các Agent. Một record skill chứa metadata descriptor cơ bản như Name, Description, thông tin truy cập tùy chọn như Package hoặc chi tiết Repository, và tài liệu markdown tùy chọn mô tả skill làm gì và cách dùng.

**Custom resources** — Đối với các tài nguyên không phù hợp với các loại chuẩn ở trên, bạn có thể định nghĩa schema metadata của riêng mình bằng bất kỳ cấu trúc JSON hợp lệ nào.

## Credential provider

Khi bạn cấu hình một registry record để đồng bộ metadata từ một nguồn ngoài (outbound authorization), AWS Agent Registry cần thông tin xác thực để truy cập nguồn đó. Một credential provider lưu trữ các chi tiết ủy quyền — hoặc thông tin xác thực OAuth hoặc một IAM role — mà AWS Agent Registry dùng để gọi endpoint của tài nguyên ngoài trong quá trình đồng bộ. Bạn tham chiếu một credential provider bằng ARN của nó khi cấu hình đồng bộ trên một record. Để biết thêm thông tin, xem [Manage credential providers](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-outbound-credential-provider.html).

Ủy quyền registry có hai loại:

- **Inbound authorization**: Dùng cấu hình này để kiểm soát cách các consumer của bạn tìm kiếm, duyệt, và gọi các discoverable data-plane API cùng MCP endpoint của registry (qua AWS CLI, AWS SDK, hoặc một MCP-compatible client). Registry hỗ trợ inbound authorization dựa trên IAM và dựa trên JWT. Bạn chỉ định inbound authorization như một phần của quy trình tạo một registry.

- **Outbound authorization**: Khi bạn cấu hình một record để đồng bộ với một MCP hoặc A2A endpoint từ xa, registry cần thông tin xác thực outbound để gọi tài nguyên từ xa tại endpoint đã chỉ định và truy xuất metadata. Bạn cung cấp các thông tin xác thực này như một phần của việc thiết lập job đồng bộ cho một registry record cụ thể.

## Tags

Bạn có thể gắn tag vào các registry và các registry record cho việc phân bổ chi phí, kiểm soát truy cập, và theo dõi mang tính tổ chức. Mỗi tag là một cặp key-value, và cả key lẫn value đều là chuỗi do bạn định nghĩa. Tag không ảnh hưởng đến hành vi runtime của một registry hay một record — chúng tồn tại như metadata mà bạn và tổ chức của bạn có thể dùng để phân loại tài nguyên trong một tài khoản AWS.

## Key Personas

Các persona sử dụng Registry có thể khác nhau giữa các tổ chức. Tuy nhiên, chúng tôi đã thấy các persona chung sau đây tương tác với Registry, thường gặp ở nhiều tổ chức.

Với tư cách administrator, bạn sở hữu hạ tầng registry. Bạn tạo và cấu hình các registry trong tài khoản AWS, quyết định cách tổ chức từng registry (theo nhóm, môi trường, hoặc loại tài nguyên), và chọn phương thức ủy quyền (IAM hoặc JWT) xác định cách các consumer truy cập registry. Bạn thiết lập quy trình phê duyệt — quyết định liệu các record có cần rà soát thủ công hay được tự động phê duyệt — và cấu hình các tích hợp Amazon EventBridge để kết nối registry với các hệ thống thông báo và rà soát hiện có của tổ chức. Bạn quản lý các quyền IAM để kiểm soát những publisher, curator, và consumer nào có thể truy cập từng registry. Với tư cách admin, bạn cũng có toàn quyền tạo, cập nhật, và xóa các record, và có thể phê duyệt, từ chối, hoặc gỡ khỏi sử dụng (deprecate) các record khi cần.

Với tư cách publisher, bạn là một người xây dựng trong tổ chức đã tạo ra một tài nguyên — một MCP server, một agent, một skill, hoặc một tool khác — và muốn làm cho nó có thể được người khác khám phá. Bạn tạo các registry record mô tả các tài nguyên của mình, cung cấp metadata, các định nghĩa, và thông tin phiên bản giúp người khác tìm và hiểu tài nguyên làm gì. Bạn lặp lại chỉnh sửa các record ở trạng thái Draft, tinh chỉnh mô tả và schema cho đến khi record sẵn sàng, rồi gửi để phê duyệt. Nếu một record bị từ chối, bạn xem lại phản hồi của curator, thực hiện các thay đổi cần thiết, và gửi lại. Bạn cũng có thể cấu hình đồng bộ dựa trên URL để các record của bạn luôn đồng bộ với các MCP server đang chạy mà không cần cập nhật thủ công.

Với tư cách curator, bạn là người gác cổng chất lượng của registry, và thường cũng có thể là administrator của registry. Bạn rà soát các record mà publisher đã gửi để phê duyệt, đánh giá từng record theo các tiêu chuẩn của tổ chức về bảo mật, tuân thủ, độ đầy đủ metadata, và bất kỳ tiêu chí nào khác mà tổ chức bạn định nghĩa. Bạn phê duyệt các record đạt các tiêu chuẩn này — làm chúng hiển thị qua các discoverable data-plane API (search, list, batch-get) và qua MCP endpoint — và từ chối các record không đạt, cung cấp phản hồi rõ ràng về những gì cần sửa. Khi một tài nguyên ngừng sử dụng, có vấn đề đã biết, hoặc bị thay thế bởi một phiên bản mới hơn, bạn deprecate record để gỡ nó khỏi việc khám phá. Với tư cách curator, bạn giúp giữ registry là một catalog đáng tin cậy, chất lượng cao mà những người xây dựng khắp tổ chức có thể dựa vào.

Với tư cách consumer, bạn là một con người hoặc một Agent cần tìm và dùng các tài nguyên. Bạn có thể khám phá các record đã phê duyệt theo ba cách:

- **Search** với các truy vấn ngôn ngữ tự nhiên hoặc tra cứu theo từ khóa để tìm các record khớp một chủ đề, năng lực, hoặc trường hợp sử dụng (`SearchDiscoverableRegistryRecords`).

- **Browse** catalog các record đã phê duyệt với một danh sách phân trang, tùy chọn lọc theo loại record, và truy xuất chi tiết cho một hoặc nhiều record cùng lúc (`ListDiscoverableRegistryRecords` và `GetDiscoverableRegistryRecord` / `BatchGetDiscoverableRegistryRecord`).

- **Connect** tới MCP endpoint của registry từ bất kỳ MCP-compatible client nào để khám phá các tool khả dụng bằng chương trình (`InvokeRegistryMcp`).

  Với tư cách consumer, bạn chỉ thấy các record đã phê duyệt, nên bạn có thể tin rằng mọi thứ bạn tìm thấy trong registry đã được rà soát và đạt các tiêu chuẩn chất lượng của tổ chức. Bạn có thể ủy quyền qua thông tin xác thực IAM hoặc JWT token từ một identity provider của doanh nghiệp, tùy theo cách registry được cấu hình.
