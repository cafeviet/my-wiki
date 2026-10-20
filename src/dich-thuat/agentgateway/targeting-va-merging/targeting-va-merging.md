# Targeting và Merging

> **Bản dịch tiếng Việt từ:** [Targeting and merging](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/policies/target-merge/), tài liệu dự án agentgateway (phiên bản Kubernetes 1.6.x).
> **Nguồn gốc:** agentgateway.dev — Agent Connectivity Solved.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên trường (field), tài nguyên và API được giữ nguyên.

## Nhắm mục tiêu cho policy (Policy targeting)

Mỗi phân mục policy chỉ có thể nhắm (**target**) vào một số loại tài nguyên Kubernetes nhất định. Nếu bạn đặt `targetRef` hoặc `targetSelector` tới một loại tài nguyên không hợp lệ cho phân mục đó, Kubernetes API server sẽ từ chối request kèm lỗi xác thực (**validation error**). Việc nhắm sai mục tiêu **không** bị bỏ qua trong im lặng.

Một policy phải nằm trong cùng namespace với các tài nguyên mà nó nhắm tới. Một policy nhắm vào một Service chỉ có hiệu lực sau khi một route hoặc một tài nguyên agentgateway khác tham chiếu Service đó và đưa nó vào cấu hình proxy.

> [!NOTE]
> Một AgentgatewayPolicy đơn lẻ chỉ có thể nhắm vào **một** loại tài nguyên. Ví dụ, bạn không thể nhắm cả Gateway lẫn HTTPRoute trong cùng một policy. Mọi mục trong `targetRefs` hoặc `targetSelectors` phải tham chiếu cùng một `kind`.

### Quy tắc nhắm mục tiêu

Bảng dưới đây cho biết mỗi phân mục policy có thể nhắm vào loại tài nguyên nào.

| Phân mục policy | Target hợp lệ | sectionName | Ghi chú |
| --- | --- | --- | --- |
| `frontend` | Gateway | Tùy theo trường. Xem [Giới hạn phân mục frontend](#frontend-restrictions). | Áp dụng cho mọi listener trên Gateway được nhắm. Một `targetRef`/`targetSelector` cũng có thể đặt `port` để thu hẹp policy về một cổng listener duy nhất trên Gateway. |
| `traffic` | Gateway, HTTPRoute, GRPCRoute, ListenerSet | Tùy chọn | Khi nhắm Gateway, `sectionName` chọn một listener cụ thể. Khi nhắm HTTPRoute hoặc GRPCRoute, `sectionName` chọn một route rule cụ thể. |
| `backend` | Gateway, HTTPRoute, GRPCRoute, ListenerSet, Service, AgentgatewayBackend | Tùy chọn | Khi nhắm Service, `sectionName` chọn một port cụ thể. Khi nhắm AgentgatewayBackend, `sectionName` chọn một sub-backend cụ thể. |

### Giới hạn phân mục frontend {#frontend-restrictions}

Dùng trường `port` để thu hẹp policy `frontend` về một cổng listener duy nhất trên Gateway. Việc một policy `frontend` có được phép đặt thêm `sectionName` để thu hẹp về một listener có tên cụ thể hay không phụ thuộc vào các trường mà policy đó đặt.

| Trường | `sectionName` |
| --- | --- |
| `accessLog`, `metrics`, `tracing` | Được phép. Chọn một listener duy nhất. |
| `connect`, `http`, `networkAuthorization`, `proxyProtocol`, `tcp`, `tls` | Không được phép. |

Nếu một policy đặt bất kỳ trường "không được phép" nào, Kubernetes API server sẽ từ chối `sectionName` trên policy đó.

### Giới hạn phân mục backend

Một số trường con của `backend` có thêm giới hạn về nhắm mục tiêu.

| Trường | Giới hạn |
| --- | --- |
| `backend.ai` | Không thể nhắm Service. Dùng AgentgatewayBackend thay thế. |
| `backend.mcp` | Không thể nhắm Service. Dùng AgentgatewayBackend thay thế. |

### Giới hạn theo giai đoạn traffic

Phân mục `traffic` hỗ trợ trường tùy chọn `phase` để kiểm soát thời điểm policy chạy. Khi đặt phase là `PreRouting`, policy chạy trước khi chọn route. Vì thời điểm này, các policy `PreRouting` chỉ có thể nhắm vào một Gateway hoặc ListenerSet.

Để biết thêm, xem [Thứ tự xử lý policy](../thu-tu-xu-ly-policy/thu-tu-xu-ly-policy.md#prerouting).

## Hợp nhất policy (Policy merging)

Khi nhiều policy nhắm cùng một tài nguyên, agentgateway hợp nhất các phân mục policy ở **cấp trường** (shallow merge). Mỗi trường được coi là một đơn vị nguyên tử (**atomic unit**). Nếu hai policy đặt cùng một trường, policy cụ thể hơn (**more specific**) sẽ được ưu tiên.

Phép merge cấp trường này áp dụng cho tất cả các trường, kể cả các trường con lồng nhau. Mỗi trường con lồng nhau được coi là một đơn vị nguyên tử. Ví dụ, `backend.ai.promptGuard` và `backend.ai.routes` là hai trường nguyên tử riêng biệt. Nếu Policy A đặt `backend.ai.promptGuard` và Policy B đặt `backend.ai.routes`, cả hai đều có trong kết quả merge. Tuy nhiên, nếu cả hai policy cùng đặt một trường con lồng nhau như `backend.ai.promptGuard`, chỉ toàn bộ giá trị của trường con đó từ policy ưu tiên cao hơn được dùng — không có phép merge đệ quy bên trong các trường lồng nhau.

### Policy AI và authorization inline trên backend

Một AgentgatewayBackend có thể đặt policy AI inline tại `spec.ai.groups[].providers[].policies.ai`. Một AgentgatewayPolicy có thể đặt policy AI tại `spec.backend.ai` và gắn vào cùng backend đó. Hai policy merge theo từng trường, giống như mọi cặp policy khác. Với một trường mà cả hai cùng đặt, giá trị inline thắng, vì policy inline trên đối tượng backend cụ thể hơn policy được gắn vào. Xem thứ tự đầy đủ ở [Thứ tự ưu tiên khi merge](#merging-precedence).

Các trường sau của `ai` merge riêng rẽ với nhau: `defaults`, `finalTransformations`, `modelAliases`, `overrides`, `prompt`, `promptCaching`, `promptGuard`, `routes`, và `transformations`.

Một AgentgatewayBackend cũng có thể đặt backend authorization inline. Dùng `spec.policies.authorization` để đặt authorization cho toàn bộ backend. Dùng `spec.ai.groups[].providers[].policies.authorization` để đặt authorization cho một AI provider. Một AgentgatewayPolicy có thể đặt backend authorization tại `spec.backend.authorization`, tách biệt với trường `spec.traffic.authorization` chạy cùng các policy traffic.

Một AgentgatewayPolicy được gắn nhắm vào `sectionName` của một provider bên trong một AI provider group cũng có thể nhắm thêm một AgentgatewayBackend riêng trong cùng danh sách `targetRefs`, để cả hai chia sẻ cùng cài đặt `auth`, `tls` và `tunnel`. Xem ví dụ ở [Share connection settings](https://agentgateway.dev/docs/kubernetes/latest/documentation/llm/shared-connection-settings/).

> [!IMPORTANT]
> Ở phiên bản 1.4 trở về trước, một block `ai` inline **thay thế toàn bộ** một block `ai` được gắn. Nếu backend đặt dù chỉ một trường của `ai`, mọi trường của policy được gắn đều bị bỏ. Sau khi nâng cấp lên 1.5, một trường mà chỉ AgentgatewayPolicy đặt sẽ có hiệu lực tại nơi trước đây nó bị bỏ qua — điều này có thể vô tình bật một prompt guard, một default, hoặc một transformation vốn trước đó không có tác dụng. Hãy rà soát từng AgentgatewayBackend có block `ai` inline đi kèm một policy được gắn, và loại bỏ khỏi AgentgatewayPolicy bất kỳ trường nào bạn không muốn backend kế thừa.

### Thứ tự ưu tiên khi merge {#merging-precedence}

Các conditional policy được chọn trước dựa trên điều kiện của chúng. Chỉ các policy đã được chọn mới tham gia vào việc đánh giá thứ tự ưu tiên khi merge.

Mỗi phân mục policy tuân theo một thứ tự ưu tiên khác nhau dựa trên độ cụ thể (**specificity**) của target. Target càng cụ thể thì ưu tiên càng cao. Trong bảng dưới, dấu `<` cho biết policy nào ghi đè policy nào. Ví dụ, `A < B` nghĩa là policy gắn tại `B` ghi đè một trường trùng khớp do policy gắn tại `A` đặt.

| Phân mục | Thứ tự ưu tiên (thấp đến cao) |
| --- | --- |
| `frontend` | Gateway < Port < Listener |
| `traffic` | Gateway < Listener < Route < Route rule |
| `backend` | Gateway < Listener < Route (targetRef) < Route rule (targetRef) < Backend (targetRef) < Backend (inline trên đối tượng backend) < Route backend ref (inline trên route) |

Với policy `frontend`, bạn chỉ có thể áp dụng policy ở cấp Listener khi trường của policy `frontend` đó hỗ trợ đặt `sectionName`. Xem các trường hỗ trợ `sectionName` tại [Giới hạn phân mục frontend](#frontend-restrictions).

Với `backend`, thứ tự ưu tiên hoạt động tương tự nhưng có nhiều cấp hơn. Ví dụ, nếu một policy cấp Gateway đặt `backend.tcp` và `backend.tls`, còn một policy cấp Backend đặt `backend.tls`, thì policy hiệu dụng dùng `tcp` từ policy Gateway và `tls` từ policy Backend.

### Độ cụ thể bằng nhau (Equal specificity)

Nếu nhiều policy có cùng độ cụ thể cùng đặt một trường, policy **cũ nhất** thắng, dựa trên `metadata.creationTimestamp` của nó trong Kubernetes. Nếu timestamp bằng nhau, agentgateway dùng thứ tự từ điển (lexicographic) của khóa policy để phá hòa. Việc lựa chọn này ổn định qua các lần controller khởi động lại.

Agentgateway dùng toàn bộ giá trị của policy thắng cho trường xung đột. Nó **không** gộp các rule hay các mục trong danh sách từ các policy khác, kể cả khi chúng chạy trong cùng giai đoạn traffic. Ví dụ, nếu hai policy cùng đặt `traffic.headerModifiers.response` tại cùng một điểm gắn và cùng giai đoạn, chỉ các chỉnh sửa header response của policy cũ hơn mới áp dụng. Các trường không xung đột vẫn đóng góp vào policy hiệu dụng.

Mọi policy bị ảnh hưởng vẫn có thể báo trạng thái `Accepted` và `Attached` là `True`, không có điều kiện nào cho biết một trường đã bị bỏ.

Một tình huống hòa chỉ xảy ra khi hai policy chia sẻ cùng độ cụ thể và cùng một trường. Bạn có thể gắn nhiều policy vào cùng một target miễn là mỗi policy đặt một trường khác nhau, hoặc gắn ở một cấp độ cụ thể khác nhau. Ví dụ, một policy `frontend` đặt `tls` ở cấp Gateway và một policy khác đặt `accessLog` qua `sectionName` của listener thì không hòa, vì chúng đặt các trường khác nhau. Một policy `frontend` đặt `tls` ở cấp Gateway và một policy khác đặt `tls` qua `port` cũng không hòa, vì `port` cụ thể hơn và thắng cho trường đó.

Hòa dễ xảy ra nhất với `frontend`, vì policy `frontend` có tối đa ba cấp độ cụ thể: Gateway, một `port` tùy chọn, và một `sectionName` listener tùy chọn cho các trường mà `sectionName` được phép. Hai policy cùng chỉ nhắm vào Gateway thì không có cách nào phân biệt độ cụ thể.

Để tránh hòa, hãy đặt một trường hay phân mục nhất định trong chỉ một policy cho mỗi target.

## Ghi đè chiến lược merge cho policy traffic

`AgentgatewayPolicy.spec.strategy.inheritance` thay đổi cách các policy `traffic` merge. Nó chỉ hợp lệ trên policy có đặt `traffic`. Kubernetes API server từ chối policy đặt block `inheritance` cùng với block `frontend` hoặc `backend`. Việc merge policy frontend và backend luôn tuân theo thứ tự ưu tiên `frontend` và `backend` trong bảng [Thứ tự ưu tiên khi merge](#merging-precedence) và không bao giờ dùng `inheritance`.

Các giá trị `inheritance` được hỗ trợ cho policy `traffic`:

| Giá trị | Hành vi |
| --- | --- |
| `Default` | Giá trị mặc định. Các trường từ điểm gắn cụ thể hơn (như route và route rule) có thể ghi đè các trường từ điểm gắn ít cụ thể hơn (như gateway và listener). Dùng giá trị này để đặt một `traffic` mặc định tại Gateway mà các route cụ thể có thể ghi đè. |
| `Override` | Chặn các policy `traffic` tại điểm gắn cụ thể hơn đóng góp vào policy hiệu dụng. Dùng khi một policy ít cụ thể hơn (như ở cấp Gateway) phải giữ vai trò authoritative cho mọi thứ bên dưới nó. Chính policy ít cụ thể hơn mới là policy ghi đè, chứ không phải policy bị ghi đè: một policy `traffic` cấp Gateway với `inheritance: Override` khóa các trường của nó, để các policy gắn ở điểm cụ thể hơn (như route hay route rule) không thể thay thế chúng. |
