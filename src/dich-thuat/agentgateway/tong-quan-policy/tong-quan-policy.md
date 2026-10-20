# Tổng quan Policy

> **Bản dịch tiếng Việt từ:** [Overview](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/policies/overview/), tài liệu dự án agentgateway (phiên bản Kubernetes 1.6.x).
> **Nguồn gốc:** agentgateway.dev — Agent Connectivity Solved.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên API/CRD, trường (field) và lệnh được giữ nguyên.

Custom resource **AgentgatewayPolicy** cho phép bạn áp dụng các policy về quản lý lưu lượng (**traffic management**), bảo mật (**security**), khả năng quan sát (**observability**) và kết nối backend lên các tài nguyên agentgateway của mình.

## Các phân mục của policy (Policy sections)

Mỗi AgentgatewayPolicy có ba phân mục cấp cao trong trường `spec`, mỗi phân mục kiểm soát một giai đoạn khác nhau của quá trình xử lý request. Bạn có thể đưa một hoặc nhiều phân mục này vào cùng một policy.

| Phân mục | Mô tả | Các trường khả dụng |
| --- | --- | --- |
| `frontend` | Kiểm soát cách gateway chấp nhận kết nối đến. Áp dụng ở cấp gateway, **trước** khi ra quyết định định tuyến. | `tcp`, `tls`, `http`, `networkAuthorization`, `accessLog`, `tracing` |
| `traffic` | Kiểm soát cách agentgateway xử lý lưu lượng. Áp dụng ở cấp listener, route hoặc route rule. Các trường được liệt kê theo thứ tự thực thi. | `cors`, `jwtAuthentication`, `basicAuthentication`, `apiKeyAuthentication`, `extAuth`, `authorization`, `rateLimit`, `extProc`, `transformation`, `csrf`, `headerModifiers`, `hostRewrite`, `directResponse`, `buffer`, `timeouts`, `retry` |
| `backend` | Kiểm soát cách agentgateway kết nối tới các backend đích. Áp dụng ở cấp backend, service, route hoặc gateway. | `tcp`, `tls`, `http`, `tunnel`, `transformation`, `auth`, `authorization`, `extAuth`, `health`, `ai`, `mcp` |

### Các trường của policy backend

Một policy `traffic` xử lý request khi nó đi qua một Gateway listener hoặc route. Một policy `backend` áp dụng cho đích (**destination**) mà agentgateway chọn cho request đó, và mỗi trường cấu hình một khía cạnh của kết nối tới đích đó.

Hãy gộp các trường vào cùng một policy khi chúng dùng chung một đối tượng mục tiêu (**target**) và vòng đời (**lifecycle**). Để biết mỗi trường có thể gắn vào tài nguyên nào, và cách hai policy cùng đặt một trường sẽ hợp nhất (**merge**) ra sao, xem [Targeting và merging](../targeting-va-merging/targeting-va-merging.md).

| Trường | Mục đích | Hướng dẫn |
| --- | --- | --- |
| `backend.tcp` | Đặt timeout kết nối và các probe TCP keepalive. | [Backend timeouts](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/timeouts/backend/), [HTTP connection settings](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/connection/#backend) |
| `backend.http` | Chọn phiên bản HTTP phía upstream và đặt thời hạn (deadline) cho response của backend. | [Backend timeouts](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/timeouts/backend/), [HTTP connection settings](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/connection/#backend) |
| `backend.tls` | Khởi tạo TLS hoặc mutual TLS (mTLS) và cấu hình xác thực chứng chỉ. | [Backend TLS](https://agentgateway.dev/docs/kubernetes/latest/documentation/security/backendtls/) |
| `backend.tunnel` | Tiếp cận đích thông qua một HTTP CONNECT proxy. | [Policy API reference](https://agentgateway.dev/docs/kubernetes/latest/reference/api/) |
| `backend.auth` | Thêm credential, hoặc trao đổi/ký/chuyển tiếp token cho đích. | [Backend authentication](https://agentgateway.dev/docs/kubernetes/latest/documentation/security/backend-authn/) |
| `backend.authorization` | Phân quyền (authorize) request sau khi agentgateway đã chọn backend đích. | [Authorization](https://agentgateway.dev/docs/kubernetes/latest/documentation/security/authorization/) |
| `backend.extAuth` | Chạy phân quyền bên ngoài (external authorization) sau khi agentgateway chọn đích. | [Bring your own external authorization service](https://agentgateway.dev/docs/kubernetes/latest/documentation/security/extauth/byo-ext-auth-service/) |
| `backend.transformation` | Biến đổi (transform) request gửi tới đích và response trả về từ nó. | [Transformations](https://agentgateway.dev/docs/kubernetes/latest/documentation/traffic-management/transformations/) |
| `backend.health` | Phát hiện endpoint không khỏe mạnh, loại bỏ chúng, và khôi phục sau khi phục hồi. | [Backend health](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/backend-health/) |
| `backend.ai` | Cấu hình prompt guard, routing, transformation và các hành vi đặc thù cho AI. | [LLM features](https://agentgateway.dev/docs/kubernetes/latest/documentation/llm/) |
| `backend.mcp` | Cấu hình authorization, authentication và guardrail cho Model Context Protocol (MCP). | [MCP features](https://agentgateway.dev/docs/kubernetes/latest/documentation/mcp/) |

## Hướng dẫn ví dụ

Tham khảo các mục sau để xem ví dụ về policy.

- [Security](https://agentgateway.dev/docs/kubernetes/latest/documentation/security/)
- [Traffic management](https://agentgateway.dev/docs/kubernetes/latest/documentation/traffic-management/)
- [Resiliency](https://agentgateway.dev/docs/kubernetes/latest/documentation/resiliency/)
