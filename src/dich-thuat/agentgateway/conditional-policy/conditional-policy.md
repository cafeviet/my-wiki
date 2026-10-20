# Conditional Policy

> **Bản dịch tiếng Việt từ:** [Conditional policies](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/policies/conditional-policies/), tài liệu dự án agentgateway (phiên bản Kubernetes 1.6.x).
> **Nguồn gốc:** agentgateway.dev — Agent Connectivity Solved.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên trường (field), biểu thức CEL và mã YAML được giữ nguyên.

## Policy có điều kiện (Conditional policies)

Thông thường một policy áp dụng cùng một cấu hình cho mọi request trên route mà nó gắn vào. Thực thi có điều kiện (**conditional execution**) cho phép bạn lồng một danh sách các biến thể policy (**variant**) dưới một trường `conditional`. Mỗi biến thể có một biểu thức CEL quyết định xem nó có áp dụng hay không. Với mỗi request, agentgateway đánh giá các mục theo thứ tự và chạy biến thể **đầu tiên** có biểu thức trả về `true`.

Một tình huống dùng phổ biến là chọn giữa hai máy chủ external authorization dựa trên request. Ví dụ, bạn có thể gửi các đường dẫn admin tới một máy chủ authorization nghiêm ngặt hơn và định tuyến mọi thứ còn lại tới một máy chủ tiêu chuẩn.

Các policy sau hỗ trợ thực thi có điều kiện:

- External authorization (`extAuth`)
- External processing (`extProc`)
- Rate limiting (`rateLimit`)
- Transformation (`transformation`)
- Direct response (`directResponse`)

Để biết cách viết các biểu thức CEL dùng trong mỗi trường `condition`, xem [tài liệu tham khảo CEL expressions](https://agentgateway.dev/docs/kubernetes/latest/reference/cel/).

### Cách thực thi có điều kiện hoạt động

- **Khớp đầu tiên thắng (First match wins).** Agentgateway đánh giá từng mục `conditional` theo thứ tự bạn liệt kê và chạy biến thể đầu tiên có `condition` trả về `true`. Các mục sau đó không được đánh giá.
- **Fallback tùy chọn.** Một mục không có `condition` là fallback vô điều kiện. Nó phải là mục **cuối cùng** trong danh sách, và bạn chỉ được có nhiều nhất một fallback. Nếu không có điều kiện nào khớp và không có fallback, policy không chạy cho request đó.
- **Loại trừ lẫn nhau với dạng inline.** Với một policy nhất định, hãy đặt **hoặc** các trường cấp cao nhất **hoặc** danh sách `conditional`, không đặt cả hai.
- **Giới hạn.** Một danh sách `conditional` có từ 1 đến 16 mục.

### Ví dụ

Xem các ví dụ sau để hiểu cách conditional policy hoạt động. Thực thi có điều kiện hoạt động giống nhau cho mọi policy được hỗ trợ. Mỗi ví dụ dưới đây minh họa một cấu hình cho một loại policy.

#### Nhiều máy chủ ext auth

Định tuyến tới một trong hai máy chủ external authorization dựa trên đường dẫn request. Các request tới đường dẫn bắt đầu bằng `/admin` đi tới máy chủ authorization nghiêm ngặt hơn. Mục fallback xử lý mọi request còn lại.

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: conditional-extauth
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: my-route
  traffic:
    extAuth:
      conditional:
      # Đường dẫn admin đi tới máy chủ authorization nghiêm ngặt hơn.
      - condition: request.path.startsWith("/admin")
        policy:
          backendRef:
            name: auth-strict
            port: 9000
          grpc: {}
          failureMode: FailClosed
      # Fallback cho mọi request khác. Không có condition, phải đứng cuối.
      - policy:
          backendRef:
            name: auth-standard
            port: 9000
          grpc: {}
          failureMode: FailClosed
```

#### Các mức rate limit khác nhau

Áp dụng rate limit nghiêm ngặt hơn cho request ghi (write) và mức lỏng hơn cho mọi lưu lượng khác.

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: conditional-ratelimit
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: my-route
  traffic:
    rateLimit:
      conditional:
      - condition: request.method == "POST" || request.method == "PUT" || request.method == "DELETE"
        policy:
          local:
          - requests: 10
            unit: Minutes
      - policy:
          local:
          - requests: 100
            unit: Minutes
```

#### Biến đổi lưu lượng nội bộ

Thêm một header tracing khi request có header `x-internal: true`. Vì không có mục fallback, agentgateway bỏ qua transformation với mọi request khác.

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: conditional-transform
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: my-route
  traffic:
    transformation:
      conditional:
      - condition: request.headers["x-internal"] == "true"
        policy:
          request:
            add:
            - name: x-trace-source
              value: '"internal"'
```

#### Lọc chat LLM bằng extproc

Gửi các request trên đường dẫn bắt đầu bằng `/v1/chat` qua một external processor. Mọi request khác bỏ qua processor này.

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: conditional-extproc
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: my-route
  traffic:
    extProc:
      conditional:
      - condition: request.path.startsWith("/v1/chat")
        policy:
          backendRef:
            name: content-filter
            port: 9100
```

#### Chặn nhanh các đường dẫn deprecated bằng direct response

Trả về response `410 Gone` cho mọi đường dẫn bắt đầu bằng `/v0/`. Mọi request khác đi tiếp tới backend.

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: conditional-direct-response
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: my-route
  traffic:
    directResponse:
      conditional:
      - condition: request.path.startsWith("/v0/")
        policy:
          status: 410
          body: "This API version is no longer available. Use /v1/."
```
