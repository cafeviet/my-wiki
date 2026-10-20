# Gateway API

> **Bản dịch tiếng Việt từ:** [Gateway API](https://agentgateway.dev/), tài liệu dự án agentgateway.
> **Nguồn gốc:** agentgateway.dev — Agent Connectivity Solved.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên API/CRD, giao thức, GEP và lệnh được giữ nguyên.

Agentgateway được xây dựng dựa trên [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/). Gateway API là một dự án Kubernetes chính thức, tập trung vào việc quản lý định tuyến lưu lượng (**traffic routing**) ở tầng L4 và L7 trong môi trường Kubernetes. Ngoài phần chức năng lõi (**core**), Gateway API còn cung cấp một bộ các điểm mở rộng (**extension point**) phong phú cho những tình huống sử dụng nâng cao. Agentgateway tận dụng chính các điểm mở rộng này để cung cấp những năng lực vượt ra ngoài phạm vi của Kubernetes API lõi.

## Mức độ tuân thủ (Conformance)

Khác với các bản triển khai (**implementation**) Gateway API khác, agentgateway là **data plane** (mặt phẳng dữ liệu) duy nhất được thiết kế từ đầu dành riêng cho Kubernetes. Nhờ đó, agentgateway cung cấp một trong những mức hỗ trợ toàn diện nhất cho Gateway API.

Bạn có thể xem kết quả kiểm thử tuân thủ (**conformance test**) theo từng phiên bản trong [tài liệu Gateway API](https://gateway-api.sigs.k8s.io/docs/implementations/list/#conformance-levels). Ví dụ, tại thời điểm viết tài liệu này, agentgateway là bản triển khai Gateway API **duy nhất** vượt qua toàn bộ các bài kiểm thử tuân thủ cho Gateway API **v1.3**.

Các tính năng của Gateway API có thể "tốt nghiệp" (**graduate**) từ kênh thử nghiệm (**experimental channel**) lên kênh chuẩn (**standard channel**) một cách độc lập với chu kỳ phát hành của agentgateway. Bảng dưới đây phân biệt mức hỗ trợ của agentgateway với trạng thái kênh ở thượng nguồn (**upstream**). Các tính năng được đánh dấu "standard" vẫn yêu cầu **experimental CRD** khi dùng với các phiên bản Gateway API ra đời trước thời điểm chúng tốt nghiệp.

| Tính năng | GEP | Trạng thái (agentgateway) | Kênh Gateway API |
| --- | --- | --- | --- |
| Xác thực chứng chỉ phía client (**Client Certificate Validation**) cho TLS kết thúc tại Gateway Listener | [GEP-91](https://gateway-api.sigs.k8s.io/geps/gep-91) | ✅ Hỗ trợ | Standard từ 1.5 |
| HTTP Auth | [GEP-1494](https://gateway-api.sigs.k8s.io/geps/gep-1494) | ✅ Hỗ trợ | Experimental |
| Session Persistence (**duy trì phiên**) | [GEP-1619](https://gateway-api.sigs.k8s.io/geps/gep-1619) | ❌ Chưa hỗ trợ | Experimental |
| ListenerSets | [GEP-1713](https://gateway-api.sigs.k8s.io/geps/gep-1713/) | ✅ Hỗ trợ | Standard từ 1.5 |
| HTTPRoute Retries (**thử lại**) | [GEP-1731](https://gateway-api.sigs.k8s.io/geps/gep-1731) | ✅ Hỗ trợ | Experimental |
| Tương tác Gateway API với Multi-Cluster Services | [GEP-1748](https://gateway-api.sigs.k8s.io/geps/gep-1748) | ❌ Chưa hỗ trợ | Experimental |
| CORS Filter | [GEP-1767](https://gateway-api.sigs.k8s.io/geps/gep-1767) | ✅ Hỗ trợ | Standard từ 1.5 |
| TLSRoute — định tuyến TLS passthrough | [GEP-2643](https://gateway-api.sigs.k8s.io/geps/gep-2643) | ✅ Hỗ trợ | Standard từ 1.5 |
| Cấu hình mTLS đầy đủ cho backend (**Complete Backend mutual TLS**) | [GEP-3155](https://gateway-api.sigs.k8s.io/geps/gep-3155) | ❌ Chưa hỗ trợ (có thể dùng qua extension) | Standard từ 1.5 |
| Retry Budgets (**ngân sách thử lại**) | [GEP-3388](https://gateway-api.sigs.k8s.io/geps/gep-3388) | ❌ Chưa hỗ trợ | Experimental |
| Cập nhật TLS cho HTTP/2 Connection Coalescing | [GEP-3567](https://gateway-api.sigs.k8s.io/geps/gep-3567) | ✅ Hỗ trợ | Standard từ 1.5 |

## Các phần mở rộng (Extensions)

Để bổ sung những chức năng còn thiếu trong Gateway API lõi, agentgateway cung cấp một số extension. Một số extension mang lại chức năng hoàn toàn mới — ví dụ như hỗ trợ giao thức MCP — trong khi số khác cung cấp phiên bản phong phú hơn cho các tính năng sẵn có.

Mục này mô tả các extension **chồng lấn** với Gateway API lõi. Để xem danh sách đầy đủ các extension, hãy tham khảo phần còn lại của tài liệu.

Khi một tính năng được triển khai ở cả Gateway API lõi lẫn một extension, bạn được quyền chọn dùng API nào cũng được:

- Nếu bạn coi trọng việc xây dựng trên chuẩn khả chuyển (**portable standard**) và không cần chức năng bổ sung, hãy dùng **Gateway API lõi**.
- Nếu bạn cần chức năng bổ sung, hoặc muốn giữ khả năng mở rộng sang các chức năng khác trong tương lai mà không phải di trú (**migration**), hãy dùng **extension của agentgateway**.

| Tính năng | Gateway API | Extension của Agentgateway | Khác biệt |
| --- | --- | --- | --- |
| Khởi tạo TLS tới backend (**Originating TLS to backends**) | [BackendTLSPolicy](https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/) | `AgentgatewayPolicy` `.backend.tls` | Agentgateway hỗ trợ mTLS, tự động xác thực SNI và SAN, tùy biến ALPN, và khả năng (tùy chọn) tắt xác thực TLS. |
| Thao tác header (**Header manipulation**) | [HTTPRoute header modifier](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/#filters-optional) | `AgentgatewayPolicy` `.traffic.transformation` | Agentgateway hỗ trợ đặt header dựa trên biểu thức CEL, thay vì chỉ giá trị tĩnh. |
| Phân quyền bên ngoài (**External Authorization**) | [HTTPRoute ExternalAuth filter](https://gateway-api.sigs.k8s.io/geps/gep-1494/) | `AgentgatewayPolicy` `.traffic.extAuth` | Agentgateway hỗ trợ cấu hình nâng cao hơn, như tự động chuyển hướng (tới trang đăng nhập) và kiểm soát tốt hơn việc xử lý request/response. |
| HTTP Filters | [Filter inline trong HTTPRoute](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/#filters-optional) | `AgentgatewayPolicy` `.traffic` | Agentgateway cho phép mọi policy được cấu hình hoặc như filter inline trong HTTPRoute, hoặc như policy độc lập gắn vào các đối tượng như Gateway và HTTPRoute, mang lại sự linh hoạt và tái sử dụng tốt hơn. |

## So sánh với các bản triển khai khác

Kubernetes Gateway API có hơn 40 [bản triển khai](https://gateway-api.sigs.k8s.io/docs/implementations/list/) tại thời điểm viết tài liệu này. Nếu bạn đang trong quá trình đánh giá một bản triển khai Gateway API, hãy cân nhắc các yếu tố sau:

**Mức độ tuân thủ (Conformance level)**: Bản triển khai có được cập nhật không? Tài liệu Gateway API [đặt ra ba mức tuân thủ](https://gateway-api.sigs.k8s.io/docs/implementations/list/#conformance-levels), tùy theo mức cam kết của mỗi bản triển khai với Gateway API theo từng phiên bản.

- Ưu tiên những bản triển khai tuân thủ (**conformant**) vượt qua các bài kiểm thử của **hai bản phát hành gần nhất** của Gateway API, chẳng hạn như kgateway cùng với agentgateway.
- Xem lại báo cáo tuân thủ theo từng phiên bản phát hành cụ thể. Nếu một bản triển khai không được liệt kê, có thể nó đã lỗi thời (**stale**). Nhiều bản triển khai đã không được cập nhật trong nhiều năm, khiến chúng không tương thích với API mới nhất.
- Xác nhận bản triển khai đã **phát hành chính thức** (generally available). Một số bản triển khai có thể còn ở giai đoạn beta hoặc alpha, chưa sẵn sàng cho môi trường production.

**Độ phủ tính năng (Feature coverage)**: Bản triển khai có triển khai đúng đặc tả Gateway API cho các tính năng bạn dùng không?

- Đánh giá báo cáo tuân thủ của từng bản triển khai cho phiên bản bạn muốn dùng. Khác với các chương trình tuân thủ khác, tuân thủ Gateway API **không yêu cầu phải vượt qua tất cả (hay bất kỳ) bài kiểm thử nào** — thay vào đó, nó cho phép các bản triển khai bỏ qua (**skip**) một số tính năng.
- Xác nhận các chức năng cơ bản như so khớp HTTP Method (**HTTP Method matching**), request timeout, v.v... được bản triển khai hỗ trợ. Hãy nhớ rằng vì các bản triển khai có thể bỏ qua tính năng, ngay cả một báo cáo tuân thủ "đạt" cũng không đồng nghĩa với việc có đủ chức năng cơ bản.

**Hiệu năng thực tế (Real-world performance)**: Bản triển khai có hoạt động tốt trong các kịch bản thực tế không?

- Lưu ý rằng báo cáo tuân thủ chỉ đánh giá tính đúng đắn của bản triển khai trong một môi trường đơn giản. Chúng không kiểm thử việc bản triển khai có mở rộng (**scale up**) lên hàng nghìn route hay không, có xử lý được cấu hình thay đổi nhanh hay không, hoặc có xử lý thay đổi mượt mà mà không gây gián đoạn (**downtime**) hay không.
- Tham khảo bộ [Gateway API Benchmarks](https://github.com/howardjohn/gateway-api-bench) (không chính thức) như một điểm khởi đầu để đánh giá hành vi của một bản triển khai Gateway API. Agentgateway được nhắc đến trong [Phần 2](https://github.com/howardjohn/gateway-api-bench/blob/main/README-v2.md)!

## Thuật ngữ song ngữ (Glossary)

| Thuật ngữ gốc | Tiếng Việt / Giải thích |
| --- | --- |
| Gateway API | Dự án Kubernetes chính thức quản lý định tuyến lưu lượng L4/L7 |
| Data plane | Mặt phẳng dữ liệu — thành phần trực tiếp xử lý/định tuyến gói tin |
| Conformance | Mức độ tuân thủ đặc tả qua bộ kiểm thử tiêu chuẩn |
| Experimental / Standard channel | Kênh thử nghiệm / kênh chuẩn phát hành tính năng |
| CRD (Custom Resource Definition) | Định nghĩa tài nguyên tùy chỉnh trong Kubernetes |
| GEP (Gateway Enhancement Proposal) | Đề xuất cải tiến Gateway API |
| Extension point | Điểm mở rộng của đặc tả |
| HTTPRoute / TLSRoute | Đối tượng định tuyến HTTP / TLS trong Gateway API |
| Listener | Điểm lắng nghe lưu lượng trên Gateway |
| Policy / Filter | Chính sách / bộ lọc xử lý request-response |
| mTLS (mutual TLS) | TLS hai chiều, xác thực cả hai phía |
| SNI / SAN / ALPN | Các mở rộng của giao thức TLS |
| CEL (Common Expression Language) | Ngôn ngữ biểu thức dùng để đặt header động |
| Upstream | Thượng nguồn — dự án/nguồn gốc tính năng |
| Portable standard | Chuẩn khả chuyển giữa các bản triển khai |
| Generally available (GA) | Đã phát hành chính thức cho production |
