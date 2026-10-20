---
title: "Bắt đầu với AWS Agent Registry"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-get-started.html"
---

# Bắt đầu với AWS Agent Registry

###### Việc di trú (Migration) đã mở

AWS Agent Registry đã ra mắt dưới namespace mới `agent-registry`. Hỗ trợ cho namespace bản xem trước công khai `bedrock-agentcore` sẽ ngừng vào ngày 17 tháng 9 năm 2026. Để biết hướng dẫn di trú, xem [Hướng dẫn di trú registry toàn diện](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-faq.html).

Trong hướng dẫn này, bạn sẽ tạo registry đầu tiên, thêm một record, phê duyệt nó, và tìm kiếm nó.

## Điều kiện tiên quyết

Hoàn thành các bước trong [Điều kiện tiên quyết](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-prerequisites.html).

## Bước 1: Tạo một registry

Tạo một registry với ủy quyền IAM và phê duyệt thủ công.

### Console

#### Tạo một registry với ủy quyền dựa trên IAM

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**.

- Trong mục **Registries**, chọn **Create registry**.

- Trong mục **Registry details**, tại **Name**, nhập tên cho registry của bạn. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 64 ký tự.

- (Tùy chọn) Chọn **Additional details** để mở rộng mục này, sau đó tại **Description**, nhập mô tả giúp nhận diện registry này.

- Trong mục **Discovery Authorization**, tại **Auth type**, chọn **Use IAM Authorization** (ủy quyền vào).

- Trong mục **Record approval**, bật hoặc tắt **Auto-approval**:

    Khi **Auto-approval** được bật, khi bạn gửi một record để phê duyệt, record sẽ chuyển thẳng sang trạng thái **Approved** và hiển thị trong kết quả tìm kiếm ngay sau đó.

- Khi **Auto-approval** tắt, khi bạn gửi một record để phê duyệt, record chuyển sang trạng thái **Pending approval** và cần một curator xem xét và phê duyệt trước khi được công bố.

- (Tùy chọn) Trong mục **Tags**, chọn **Add new tag** để gắn một hoặc nhiều thẻ vào registry. Mỗi thẻ có một khóa và một giá trị tùy chọn.

- Chọn **Create registry**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**.

- Trong mục **Registries**, chọn **Create registry**.

- Trong mục **Registry details**, tại **Name**, nhập tên cho registry của bạn. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 64 ký tự.

- (Tùy chọn) Chọn **Additional details** để mở rộng mục này, sau đó tại **Description**, nhập mô tả giúp nhận diện registry này.

- Trong mục **Search API Authorization**, tại **Auth type**, chọn **Use IAM Authorization** (ủy quyền vào).

- Trong mục **Record approval**, bật hoặc tắt **Auto-approval**:

    Khi **Auto-approval** được bật, khi bạn gửi một record để phê duyệt, record sẽ chuyển thẳng sang trạng thái **Approved** và hiển thị trong kết quả tìm kiếm ngay sau đó.

- Khi **Auto-approval** tắt, khi bạn gửi một record để phê duyệt, record chuyển sang trạng thái **Pending approval** và cần một curator xem xét và phê duyệt trước khi được công bố.

- Chọn **Create registry**.

#### Tạo một registry với ủy quyền dựa trên JWT

Ủy quyền qua nhà cung cấp danh tính sử dụng JSON Web Token (JWT) để kiểm soát quyền truy cập vào các API data-plane có thể khám phá được và MCP endpoint của registry. Bạn có thể dùng Amazon Cognito để thiết lập ủy quyền nhanh chóng, hoặc mang theo nhà cung cấp danh tính của riêng bạn để bật OAuth 2.0.

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**.

- Trong mục **Registries**, chọn **Create registry**.

- Trong mục **Registry details**, tại **Name**, nhập tên cho registry của bạn. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 64 ký tự.

- (Tùy chọn) Chọn **Additional details** để mở rộng mục này, sau đó tại **Description**, nhập mô tả giúp nhận diện registry này.

- Trong mục **Discovery Authorization**, tại **Auth type**, chọn **Use JSON Web Tokens (JWT)** (ủy quyền vào).

- Với **JWT schema configuration**, chọn một trong các tùy chọn sau:

       **Quick create configurations with Cognito (khuyến nghị)** – AWS Agent Registry tạo các cấu hình ủy quyền thay mặt bạn bằng cách dùng Amazon Cognito làm nhà cung cấp danh tính. Không cần cấu hình bổ sung.

- **Use existing Identity provider configurations** – Mang theo nhà cung cấp danh tính của riêng bạn để bật OAuth 2.0. Nếu chọn tùy chọn này, hoàn thành các bước sau:

          Tại **Discovery URL**, nhập discovery URL từ nhà cung cấp danh tính của bạn. AWS Agent Registry dùng URL này để tự động lấy các thiết lập đăng nhập, token, và xác minh cho nhà cung cấp của bạn. Bạn có thể tìm URL này trong bảng điều khiển hoặc tài liệu của nhà cung cấp danh tính (ví dụ, `https://cognito-identity.amazonaws.com/.well-known/openid-configuration`).
          Lưu ý: Discovery URL không thể thay đổi sau khi registry đã được tạo.

- (Tùy chọn) Dưới **JWT authorization configuration**, chọn **Allowed audiences** để cung cấp danh sách các audience được phép mà AWS Agent Registry xác thực dựa trên claim `aud` trong JWT token. Một claim audience (`aud`) trong OAuth 2.0 chỉ định resource server (API) nào mà token dành cho. Điều này đảm bảo token là người nhận đúng trước khi xử lý yêu cầu, ngăn việc token bị tái sử dụng tại một API khác mà nó không được cấp cho.

- (Tùy chọn) Chọn **Allowed clients** để cung cấp danh sách các định danh client được phép mà AWS Agent Registry xác thực dựa trên claim `client_id` trong JWT token. Một `client_id` là một định danh công khai, duy nhất cho một ứng dụng đang yêu cầu access token để truy cập các API data-plane có thể khám phá được hoặc MCP endpoint của registry. Nếu bật tùy chọn này, nhập một hoặc nhiều client ID vào trường **Clients**, rồi chọn **Add client** để thêm các client khác.

- (Tùy chọn) Chọn **Allowed scopes** để cung cấp danh sách các quyền được phép, được định nghĩa dưới dạng scope. Nếu được cấu hình, ít nhất một giá trị scope trong token đến phải khớp với một trong các giá trị đã cấu hình. Scope đóng vai trò như quyền để giới hạn những gì một ứng dụng có thể làm.

- (Tùy chọn) Chọn **Custom claims** để cung cấp một tập quy tắc khớp các claim cụ thể trong token đến với các giá trị định trước. Với mỗi quy tắc, chỉ định tên claim, loại giá trị (**STRING** hoặc **STRING_ARRAY**), và giá trị khớp yêu cầu.

- Trong mục **Record approval**, bật hoặc tắt **Auto-approval**:

    Khi **Auto-approval** được bật, khi bạn gửi một record để phê duyệt, record sẽ chuyển thẳng sang trạng thái **Approved** và hiển thị ngay lập tức trong kết quả tìm kiếm.

- Khi **Auto-approval** tắt, khi bạn gửi một record để phê duyệt, record chuyển sang trạng thái **Pending approval** và cần một registry admin xem xét và phê duyệt trước khi được công bố.

- (Tùy chọn) Trong mục **Tags**, chọn **Add new tag** để gắn một hoặc nhiều thẻ vào registry. Mỗi thẻ có một khóa và một giá trị tùy chọn.

- Chọn **Create registry**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**.

- Trong mục **Registries**, chọn **Create registry**.

- Trong mục **Registry details**, tại **Name**, nhập tên cho registry của bạn. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 64 ký tự.

- (Tùy chọn) Chọn **Additional details** để mở rộng mục này, sau đó tại **Description**, nhập mô tả giúp nhận diện registry này.

- Trong mục **Search API Authorization**, tại **Auth type**, chọn **Use JSON Web Tokens (JWT)** (ủy quyền vào).

- Với **JWT schema configuration**, chọn một trong các tùy chọn sau:

       **Quick create configurations with Cognito (khuyến nghị)** – AWS Agent Registry tạo các cấu hình ủy quyền thay mặt bạn bằng cách dùng Amazon Cognito làm nhà cung cấp danh tính. Không cần cấu hình bổ sung.

- **Use existing Identity provider configurations** – Mang theo nhà cung cấp danh tính của riêng bạn để bật OAuth 2.0. Nếu chọn tùy chọn này, hoàn thành các bước sau:

          Tại **Discovery URL**, nhập discovery URL từ nhà cung cấp danh tính của bạn. AWS Agent Registry dùng URL này để tự động lấy các thiết lập đăng nhập, token, và xác minh cho nhà cung cấp của bạn. Bạn có thể tìm URL này trong bảng điều khiển hoặc tài liệu của nhà cung cấp danh tính (ví dụ, `https://cognito-identity.amazonaws.com/.well-known/openid-configuration`).
          Lưu ý: Discovery URL không thể thay đổi sau khi registry đã được tạo.

- (Tùy chọn) Dưới **JWT authorization configuration**, chọn **Allowed audiences** để cung cấp danh sách các audience được phép mà AWS Agent Registry xác thực dựa trên claim `aud` trong JWT token. Một claim audience (`aud`) trong OAuth 2.0 chỉ định resource server (API) nào mà token dành cho. Điều này đảm bảo token là người nhận đúng trước khi xử lý yêu cầu, ngăn việc token bị tái sử dụng tại một API khác mà nó không được cấp cho.

- (Tùy chọn) Chọn **Allowed clients** để cung cấp danh sách các định danh client được phép mà AWS Agent Registry xác thực dựa trên claim `client_id` trong JWT token. Một `client_id` là một định danh công khai, duy nhất cho một ứng dụng đang yêu cầu access token để truy cập search API của registry. Nếu bật tùy chọn này, nhập một hoặc nhiều client ID vào trường **Clients**, rồi chọn **Add client** để thêm các client khác.

- (Tùy chọn) Chọn **Allowed scopes** để cung cấp danh sách các quyền được phép, được định nghĩa dưới dạng scope. Nếu được cấu hình, ít nhất một giá trị scope trong token đến phải khớp với một trong các giá trị đã cấu hình. Scope đóng vai trò như quyền để giới hạn những gì một ứng dụng có thể làm.

- (Tùy chọn) Chọn **Custom claims** để cung cấp một tập quy tắc khớp các claim cụ thể trong token đến với các giá trị định trước. Với mỗi quy tắc, chỉ định tên claim, loại giá trị (**STRING** hoặc **STRING_ARRAY**), và giá trị khớp yêu cầu.

- Trong mục **Record approval**, bật hoặc tắt **Auto-approval**:

    Khi **Auto-approval** được bật, khi bạn gửi một record để phê duyệt, record sẽ chuyển thẳng sang trạng thái **Approved** và hiển thị ngay lập tức trong kết quả tìm kiếm.

- Khi **Auto-approval** tắt, khi bạn gửi một record để phê duyệt, record chuyển sang trạng thái **Pending approval** và cần một registry admin xem xét và phê duyệt trước khi được công bố.

- Chọn **Create registry**.

###### Lưu ý

* Cần ít nhất một trường **JWT authorization configuration**: allowed audiences, allowed clients, allowed scopes, hoặc custom claims. Nếu bạn cấu hình nhiều hơn một, AWS Agent Registry xác minh tất cả. * Discovery URL không thể thay đổi sau khi registry đã được tạo. * Loại ủy quyền (IAM hoặc JWT) không thể thay đổi sau khi registry đã được tạo. * Một registry chỉ hỗ trợ một dạng loại ủy quyền vào tại một thời điểm — IAM SigV4 hoặc JWT Bearer Token. Bạn không thể dùng cả hai đồng thời. Tìm kiếm qua IAM chỉ được hỗ trợ với registry dựa trên IAM; và tìm kiếm qua OAuth chỉ được hỗ trợ với registry dựa trên OAuth.

Sau khi tạo registry, console điều hướng tới trang chi tiết registry. Trạng thái registry ban đầu là **Creating**. AWS Agent Registry gán cho registry một ARN, mà bạn có thể tìm thấy trong mục **Registry details**. Trạng thái registry chuyển thành **Ready** sau khi việc cấp phát (provisioning) hoàn tất. Bạn có thể thêm record vào registry khi trạng thái của nó là **Ready**.

### AWS CLI

```bash
aws agent-registry-control create-registry \
  --name "MyFirstRegistry" \
  --description "My first Agent Registry" \
  --region us-east-1
```

```bash
aws bedrock-agentcore-control create-registry \
  --name "MyFirstRegistry" \
  --description "My first Agent Registry" \
  --region us-east-1
```

Trạng thái registry bắt đầu là CREATING và chuyển sang READY khi việc cấp phát hoàn tất.

### AWS SDK

```python
import boto3

client = boto3.client('agent-registry-control')

response = client.create_registry(
    name='my-agent-registry',
    description='My first Agent Registry'
)
print(response['registryArn'])
```

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.create_registry(
    name='my-agent-registry',
    description='My first Agent Registry'
)
print(response['registryArn'])
```

## Bước 2: Thêm một registry record

Tạo một record cho một MCP server trong registry của bạn.

### Console

Một registry record đại diện cho một agent, tool (công cụ), skill, hoặc tài nguyên tùy chỉnh.

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên của registry nơi bạn muốn thêm một record.

- Trong mục **Registry records**, chọn **Create record**.

- Chọn một loại nguồn:

     **Synchronize from endpoint** — Cung cấp một endpoint URL và thông tin xác thực tùy chọn để lấy metadata từ một MCP server hoặc Agent (A2A) endpoint. Xem [Đồng bộ record từ các nguồn bên ngoài](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html) để biết chi tiết.

- **Manual** — Cấu hình thủ công các chi tiết record và cấu hình giao thức. Tiếp tục với các bước bên dưới.

- Trong mục **Record details**, tại **Name**, nhập một tên duy nhất cho record. Tên phải là duy nhất trong registry — tổ hợp của `Name` và `Record version` phải duy nhất. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 255 ký tự.

- (Tùy chọn) Tại **Display name**, nhập một nhãn dễ đọc cho record. Nhãn này xuất hiện trong bảng registry records và trong kết quả tìm kiếm bên cạnh tên kỹ thuật của record.

- (Tùy chọn) Tại **Description**, nhập một mô tả cho record. Mô tả có thể từ 1 đến 4.096 ký tự.

- Tại **Record version**, nhập một định danh phiên bản cho record (ví dụ, `1.0.0` hoặc `v2.1`).

- Trong mục **Record type and descriptor**:

     Dưới **Type**, chọn loại ngữ nghĩa của record. Loại này quyết định các khóa descriptor chính nào là hợp lệ.

       **MCP** – Giao thức được thiết kế cho giao tiếp giữa AI tool và agent. Xử lý quản lý ngữ cảnh và các định dạng thông điệp có cấu trúc.

- **Agent** – Giao thức được thiết kế cho các tương tác agent-to-agent bảo mật. Cho phép các luồng công việc phân tán và trao đổi thông tin.

- **Skills** – Đăng ký các agent skill với tài liệu markdown và một định nghĩa có cấu trúc tùy chọn.

- **Custom** – Triển khai giao thức tùy chỉnh cho các mẫu giao tiếp chuyên biệt. Định nghĩa đặc tả giao diện và yêu cầu tích hợp của riêng bạn.

- Dưới **Descriptor**, chọn hình dạng dữ liệu descriptor của record. Các tùy chọn có sẵn phụ thuộc vào **Type** bạn đã chọn:

       **MCP** → **MCP server** hoặc **Custom**

- **Agent** → **A2A Agent Card**, **MCP server**, hoặc **Custom**

- **Skills** → **Agent skills definition** hoặc **Custom**

- **Custom** → **Custom**

- Một trình soạn thảo dành riêng cho descriptor xuất hiện dựa trên lựa chọn **Descriptor** của bạn:

     **MCP server** – Chọn một phiên bản schema từ dropdown **Schema version** (ví dụ, `2025-12-11`), và nhập server.json từ [Model Context Protocol registry](https://registry.modelcontextprotocol.io/) trên website Model Context Protocol vào trình soạn thảo **Your MCP server definition**. Định nghĩa phải tuân thủ schema MCP server chính thức cho phiên bản đã chọn. Để xem schema chính thức làm tham chiếu, bật **Show official schema**. (Tùy chọn) Chọn **Add tool definition** để thêm các tool có sẵn trên server này kèm tham số đầu vào, đầu ra, và ví dụ sử dụng của chúng. Chọn một phiên bản schema (ví dụ, `2025-11-25`) và nhập định nghĩa tool của bạn vào trình soạn thảo **Your Tool definition**.

- **A2A Agent Card** – Phiên bản schema là `0.3`. Nhập định nghĩa agent card của bạn vào trình soạn thảo. Để xem schema chính thức làm tham chiếu, bật **Show official schema**.

- **Agent skills definition** – Tại **Skill documentation**, nhập markdown mô tả skill này. (Tùy chọn) Chọn **Include skill definition** để thêm một định nghĩa có cấu trúc. Chọn một phiên bản schema và nhập định nghĩa dưới dạng một đối tượng JSON.

- **Custom** – Nhập định nghĩa tùy chỉnh của bạn dưới dạng một đối tượng JSON.

- (Tùy chọn) Trong mục **Tags**, chọn **Add new tag** để gắn một hoặc nhiều thẻ vào record. Mỗi thẻ có một khóa và một giá trị tùy chọn.

- Chọn **Create record**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên của registry nơi bạn muốn thêm một record.

- Trong mục **Registry records**, chọn **Create record**.

- Chọn một loại nguồn:

     **Synchronize from endpoint** — Cung cấp một endpoint URL và thông tin xác thực tùy chọn để lấy metadata từ một MCP server hoặc Agent (A2A) endpoint. Xem [Đồng bộ record từ các nguồn bên ngoài](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html) để biết chi tiết.

- **Manual** — Cấu hình thủ công các chi tiết record và cấu hình giao thức. Tiếp tục với các bước bên dưới.

- Trong mục **Record details**, tại **Name**, nhập một tên cho record. Tên phải bắt đầu bằng ký tự chữ-số. Các ký tự hợp lệ là a–z, A–Z, 0–9, `_` (gạch dưới), `-` (gạch nối), `.` (dấu chấm), và `/` (gạch chéo). Tên có thể dài tối đa 255 ký tự.

- (Tùy chọn) Tại **Description**, nhập một mô tả cho record. Mô tả có thể từ 1 đến 4.096 ký tự.

- Tại **Record version**, nhập một định danh phiên bản cho record (ví dụ, `1.0.0` hoặc `v2.1`).

- Trong mục **Record type**, chọn loại khớp với tài nguyên của bạn:

     **MCP** – Giao thức được thiết kế cho giao tiếp giữa AI tool và agent. Xử lý quản lý ngữ cảnh và các định dạng thông điệp có cấu trúc. Nếu bạn chọn loại này, hoàn thành các bước sau:

       Trong mục **MCP server definition**, chọn một phiên bản schema từ dropdown **Schema version** (ví dụ, `2025-12-11`), rồi nhập server.json từ [Model Context Protocol registry](https://registry.modelcontextprotocol.io/) trên website Model Context Protocol vào trình soạn thảo **Your MCP server definition**. Định nghĩa phải tuân thủ schema MCP server chính thức cho phiên bản đã chọn. Để xem schema chính thức làm tham chiếu, bật **Show official schema**.

- (Tùy chọn) Chọn **Add tool definition** để thêm các tool cụ thể có sẵn trên server này kèm tham số đầu vào, đầu ra, và ví dụ sử dụng của chúng nhằm tăng khả năng khám phá. Nếu bạn chọn tùy chọn này, chọn một phiên bản schema từ dropdown **Schema version** (ví dụ, `2025-11-25`), rồi nhập định nghĩa tool của bạn vào trình soạn thảo **Your Tool definition**. Để xem tool schema chính thức làm tham chiếu, bật **Show official schema**.

- **Agent** – Giao thức được thiết kế cho các tương tác agent-to-agent bảo mật. Cho phép các luồng công việc phân tán và trao đổi thông tin. Nếu bạn chọn loại này, phiên bản schema là `0.3`. Nhập định nghĩa agent card của bạn vào trình soạn thảo. Để xem schema chính thức làm tham chiếu, bật **Show official schema**.

- **Agent Skills** – Đăng ký các agent skill với tài liệu markdown và một định nghĩa có cấu trúc tùy chọn. Nếu bạn chọn loại này, hoàn thành các bước sau:

       Tại **Skill documentation**, nhập tài liệu markdown mô tả skill này.

- (Tùy chọn) Chọn **Include skill definition** để thêm một định nghĩa có cấu trúc. Nếu bạn chọn tùy chọn này, chọn một phiên bản schema từ dropdown **Schema version**, rồi nhập định nghĩa skill dưới dạng một đối tượng JSON vào trình soạn thảo.

- **Custom** – Triển khai giao thức tùy chỉnh cho các mẫu giao tiếp chuyên biệt. Định nghĩa đặc tả giao diện và yêu cầu tích hợp của riêng bạn. Nếu bạn chọn loại này, nhập định nghĩa tùy chỉnh của bạn dưới dạng một đối tượng JSON vào trình soạn thảo.

- Chọn **Create record**.

###### Lưu ý

Để thêm vào registry một server hoặc agent không tuân theo các schema giao thức chuẩn MCP hoặc A2A, hãy dùng loại record Custom.

Sau khi bạn chọn Create record, AWS Agent Registry bắt đầu cấp phát record. Trạng thái record ban đầu là Creating. Khi việc cấp phát hoàn tất, trạng thái chuyển thành Draft. Để làm record khả dụng cho người khác khám phá, hãy gửi nó để phê duyệt. Để biết thêm thông tin, xem [Bước 3: Gửi record để phê duyệt](#registry-get-started-step3).

### AWS CLI

```bash
aws agent-registry-control create-registry-record \
  --registry-id <registryId> \
  --name "weather-server" \
  --display-name "WeatherServer" \
  --record-type MCP \
  --descriptors '{"mcpServer": {"data": "{\"name\": \"weather/mcp-server\", \"description\": \"Weather data service\", \"version\": \"1.0.0\"}", "dataSchemaVersion": "2025-12-11"}}' \
  --record-version "1.0" \
  --region us-east-1
```

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <registryId> \
  --name "WeatherServer" \
  --descriptor-type MCP \
  --descriptors '{"mcp": {"server": {"inlineContent": "{\"name\": \"weather/mcp-server\", \"description\": \"Weather data service\", \"version\": \"1.0.0\"}"}}}' \
  --record-version "1.0" \
  --region us-east-1
```

Record được tạo ở trạng thái CREATING và chuyển sang DRAFT khi việc xử lý hoàn tất. Để xem thêm ví dụ AWS CLI cho việc tạo record của các loại khác, tham khảo mục [Tạo và quản lý record](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-create-manage-records.html).

### AWS SDK

```python
import boto3
import json

client = boto3.client('agent-registry-control')

server_content = json.dumps({
    "name": "io.example/weather-server",
    "description": "A weather MCP server",
    "version": "1.0.0"
})

tools_content = json.dumps({
    "tools": [{
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "inputSchema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }]
})

response = client.create_registry_record(
    registryId='<registryId>',
    name='my-mcp-server',
    displayName='My MCP Server',
    recordType='MCP',
    descriptors={
        'mcpServer': {
            'data': server_content,
            'dataSchemaVersion': '2025-12-11',
            'additionalData': {
                'tools': {
                    'data': tools_content,
                    'dataSchemaVersion': '2024-11-05'
                }
            }
        }
    },
    recordVersion='1.0'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Status: {response['status']}")  # CREATING
```

```python
import boto3
import json

client = boto3.client('bedrock-agentcore-control')

server_content = json.dumps({
    "name": "io.example/weather-server",
    "description": "A weather MCP server",
    "version": "1.0.0"
})

tools_content = json.dumps({
    "tools": [{
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "inputSchema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }]
})

response = client.create_registry_record(
    registryId='<registryId>',
    name='my-mcp-server',
    descriptorType='MCP',
    descriptors={
        'mcp': {
            'server': {
                'schemaVersion': '2025-12-11',
                'inlineContent': server_content
            },
            'tools': {
                'protocolVersion': '2024-11-05',
                'inlineContent': tools_content
            }
        }
    },
    recordVersion='1.0'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Status: {response['status']}")  # CREATING
```

## Bước 3: Gửi record để phê duyệt

### Console

Việc gửi một record để phê duyệt sẽ khởi động quy trình xem xét làm record khả dụng để khám phá. Bạn có thể gửi một record từ bảng registry records hoặc từ trang chi tiết record.

**Để gửi một record để phê duyệt từ bảng registry records**

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn record bạn muốn gửi.

- Chọn **Update status**, rồi chọn **Submit for approval**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn record bạn muốn gửi.

- Chọn **Update status**, rồi chọn **Submit for approval**.

**Để gửi một record để phê duyệt từ trang chi tiết record**

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn tên của record bạn muốn gửi.

- Chọn **Update status**, rồi chọn **Submit for approval**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn tên của record bạn muốn gửi.

- Chọn **Update status**, rồi chọn **Submit for approval**.

Sau khi bạn gửi một record để phê duyệt, trạng thái record thay đổi dựa trên thiết lập phê duyệt của registry:

- Nếu registry bật **Auto-approval**, trạng thái record chuyển thẳng sang **Approved** và hiển thị trong kết quả tìm kiếm ngay sau đó.

- Nếu registry tắt **Auto-approval**, trạng thái record chuyển sang **Pending approval** và cần một registry admin xem xét và phê duyệt trước khi được công bố.

### AWS CLI

```bash
aws agent-registry-control submit-registry-record-for-approval \
  --registry-id <registryId> \
  --record-id <recordId> \
  --region us-east-1
```

```bash
aws bedrock-agentcore-control submit-registry-record-for-approval \
  --registry-id <registryId> \
  --record-id <recordId> \
  --region us-east-1
```

Record chuyển sang PENDING_APPROVAL (hoặc thẳng sang APPROVED nếu auto-approval được bật).

### AWS SDK

```python
import boto3

client = boto3.client('agent-registry-control')

response = client.submit_registry_record_for_approval(
    registryId='<registryId>',
    recordId='<recordId>'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Record ID: {response['recordId']}")
print(f"Status: {response['status']}")  # PENDING_APPROVAL or APPROVED
print(f"Updated At: {response['updatedAt']}")
```

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.submit_registry_record_for_approval(
    registryId='<registryId>',
    recordId='<recordId>'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Record ID: {response['recordId']}")
print(f"Status: {response['status']}")  # PENDING_APPROVAL or APPROVED
print(f"Updated At: {response['updatedAt']}")
```

## Bước 4: Phê duyệt record

### Console

**Để phê duyệt một record từ bảng registry records**

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn record bạn muốn phê duyệt.

- Chọn **Update status**, rồi chọn **Approve**.

- Trong hộp thoại xác nhận, nhập lý do cho việc thay đổi trạng thái.

- Chọn **Confirm**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn record bạn muốn phê duyệt.

- Chọn **Update status**, rồi chọn **Approve**.

- Trong hộp thoại xác nhận, nhập lý do cho việc thay đổi trạng thái.

- Chọn **Confirm**.

**Để phê duyệt một record từ trang chi tiết record**

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn tên của record bạn muốn phê duyệt.

- Trong trang chi tiết record, chọn **Update status**, rồi chọn **Approve**.

- Trong hộp thoại xác nhận, nhập lý do cho việc thay đổi trạng thái.

- Chọn **Confirm**.

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Trong mục **Registry records**, chọn tên của record bạn muốn phê duyệt.

- Trong trang chi tiết record, chọn **Update status**, rồi chọn **Approve**.

- Trong hộp thoại xác nhận, nhập lý do cho việc thay đổi trạng thái.

- Chọn **Confirm**.

### AWS CLI

```bash
aws agent-registry-control update-registry-record-status \
  --registry-id <registryId> \
  --record-id <recordId> \
  --status APPROVED \
  --status-reason "Reviewed and approved" \
  --region us-east-1
```

```bash
aws bedrock-agentcore-control update-registry-record-status \
  --registry-id <registryId> \
  --record-id <recordId> \
  --status APPROVED \
  --status-reason "Reviewed and approved" \
  --region us-east-1
```

### AWS SDK

```python
import boto3

client = boto3.client('agent-registry-control')

response = client.update_registry_record_status(
    registryId='<registryId>',
    recordId='<recordId>',
    status='APPROVED',
    statusReason='Meets all requirements'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Status: {response['status']}")  # APPROVED
print(f"Reason: {response['statusReason']}")
```

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.update_registry_record_status(
    registryId='<registryId>',
    recordId='<recordId>',
    status='APPROVED',
    statusReason='Meets all requirements'
)
print(f"Record ARN: {response['recordArn']}")
print(f"Status: {response['status']}")  # APPROVED
print(f"Reason: {response['statusReason']}")
```

## Bước 5: Khám phá các record đã được phê duyệt

Record directory là trang console để duyệt và tìm kiếm các record đã được phê duyệt trong một registry. Khi bạn chọn một registry trên trang Record directory, console tự động liệt kê các record đã được phê duyệt của nó. Từ đó bạn có thể phân trang qua danh sách, hoặc dùng ô tìm kiếm để chạy một truy vấn ngôn ngữ tự nhiên. Về mặt lập trình, dùng `ListDiscoverableRegistryRecords` để duyệt, `SearchDiscoverableRegistryRecords` để tìm kiếm, và `BatchGetDiscoverableRegistryRecord` để lấy đầy đủ chi tiết cho nhiều record trong một lần gọi.

### Console

###### Lưu ý

Khám phá dựa trên console chỉ khả dụng cho các registry dùng **Use IAM** làm loại ủy quyền. Nếu registry của bạn dùng JSON Web Token (JWT), hãy gọi trực tiếp các API data-plane có thể khám phá được bằng một HTTP client như curl hoặc Postman với một JWT Bearer Token hợp lệ trong header của yêu cầu. AWS CLI và AWS SDK dùng chữ ký IAM SigV4 và không thể dùng với các registry được ủy quyền bằng JWT. Để biết thêm chi tiết, xem [Tìm kiếm record trong registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-search-records.html).

**Để duyệt hoặc tìm kiếm các record đã được phê duyệt**

- Mở [AWS Agent Registry console](https://console.aws.amazon.com/agent-registry/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Record directory**.

- Dưới **Registry**, chọn registry mà bạn muốn khám phá các record đã được phê duyệt của nó. Trang tự động liệt kê tất cả các record đã được phê duyệt trong registry đó.

- (Tùy chọn) Chuyển đổi giữa chế độ xem **Card** và **Table** ở góc trên bên phải của trang.

- (Tùy chọn) Trong **Search approved records**, nhập một truy vấn ngôn ngữ tự nhiên hoặc một tên để thu hẹp kết quả, rồi chọn **Search**.

- Chọn một card hoặc một hàng để mở đầy đủ chi tiết của record.

Record directory chỉ hiển thị các record ở trạng thái **Approved**. Các record ở trạng thái Draft, Pending approval, Rejected, hoặc Deprecated sẽ không xuất hiện.

**Để tìm kiếm các registry record**

- Mở trang AWS Agent Registry trong [Bedrock-AgentCore console](https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1#).

- Trong bảng điều hướng, chọn **Registry**, rồi chọn tên registry.

- Chọn tab **Search records**.

- Trong trường **Search approved records**, nhập truy vấn tìm kiếm của bạn.

- (Tùy chọn) Để lọc kết quả theo một thuộc tính cụ thể, chọn trường tìm kiếm để mở rộng menu **Properties**, rồi chọn một bộ lọc: **Name**, **Descriptor type**, hoặc **Version**.

- Chọn **Search**.

Tìm kiếm chỉ trả về các record ở trạng thái **Approved**. Các record ở các trạng thái khác như Draft, Pending approval, Rejected, hoặc Deprecated sẽ không xuất hiện trong kết quả tìm kiếm.

### AWS CLI

**Duyệt các record đã được phê duyệt** — liệt kê các record đã được phê duyệt trong một registry:

```bash
aws agent-registry list-discoverable-registry-records \
  --registry-id "<registry-id>" \
  --region us-east-1
```

**Tìm kiếm các record đã được phê duyệt** — chạy tìm kiếm lai (hybrid) semantic + keyword:

```bash
aws agent-registry search-discoverable-registry-records \
  --search-query "weather" \
  --registry-ids "<registry-id>" \
  --region us-east-1
```

```bash
aws bedrock-agentcore search-registry-records \
  --search-query "weather" \
  --registry-ids "<registry-id>" \
  --region us-east-1
```

**Lấy đầy đủ chi tiết cho nhiều record cùng lúc**:

```bash
aws agent-registry batch-get-discoverable-registry-record \
  --entries '[{"registryId": "<registry-id>", "recordIds": ["<recordId-1>", "<recordId-2>"]}]' \
  --region us-east-1
```

###### Lưu ý

`ListDiscoverableRegistryRecords` và `BatchGetDiscoverableRegistryRecord` chỉ khả dụng trong namespace `agent-registry`. Chúng không khả dụng trong namespace `bedrock-agentcore`.

### AWS SDK

**Duyệt các record đã được phê duyệt**:

```python
import boto3

client = boto3.client('agent-registry')

list_response = client.list_discoverable_registry_records(
    registryId='<registry-id>',
    maxResults=20
)
for record in list_response['registryRecords']:
    print(f"{record['displayName']} ({record['name']}) - {record['recordType']}")
```

**Tìm kiếm các record đã được phê duyệt**:

```python
import boto3

client = boto3.client('agent-registry')

response = client.search_discoverable_registry_records(
    registryIds=['arn:aws:agent-registry:us-east-1:<account>:registry/<registryId>'],
    searchQuery='weather forecast tool',
    maxResults=10
)
for record in response['registryRecords']:
    print(f"Record: {record['displayName']} ({record['recordId']})")
    print(f"  Name: {record['name']}")
    print(f"  Type: {record['recordType']}")
    print(f"  Status: {record['status']}")
    print(f"  Version: {record['recordVersion']}")
```

```python
import boto3

client = boto3.client('bedrock-agentcore')

response = client.search_registry_records(
    registryIds=['arn:aws:bedrock-agentcore:us-east-1:<account>:registry/<registryId>'],
    searchQuery='weather forecast tool',
    maxResults=10
)
for record in response['registryRecords']:
    print(f"Record: {record['name']} ({record['recordId']})")
    print(f"  Type: {record['descriptorType']}")
    print(f"  Status: {record['status']}")
    print(f"  Version: {record['version']}")
```

**Lấy đầy đủ chi tiết cho nhiều record cùng lúc**:

```python
batch_response = client.batch_get_discoverable_registry_record(
    entries=[{'registryId': '<registry-id>', 'recordIds': ['<recordId-1>', '<recordId-2>']}]
)
for record in batch_response['registryRecords']:
    print(f"{record['displayName']} ({record['name']}) - {record['recordType']}")
for err in batch_response['errors']:
    print(f"Error for {err['recordId']}: {err['errorCode']}")
```

## Những gì bạn đã xây dựng

- Một **registry** với ủy quyền IAM và phê duyệt thủ công

- Một **registry record** mô tả một MCP server

- Một **record đã được phê duyệt** có thể duyệt và tìm kiếm thông qua Record directory

## Các bước tiếp theo

- Xây dựng các trải nghiệm khám phá dạng catalog trên nền `ListDiscoverableRegistryRecords` và `BatchGetDiscoverableRegistryRecord`

- Thiết lập thông báo Amazon EventBridge để tự động hóa luồng công việc phê duyệt của bạn

- Thêm nhiều record hơn cho các agent, server, skill, và tài nguyên tùy chỉnh của bạn
