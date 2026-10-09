# agentgateway

Các bài dịch từ tài liệu dự án [agentgateway](https://agentgateway.dev/) — cổng kết nối (gateway) mã nguồn mở cho lưu lượng HTTP, gRPC, MCP, A2A và LLM.

- [Agentgateway: kiến trúc Kubernetes và mô hình C4](./agentgateway-kubernetes-c4/agentgateway-kubernetes-c4.md) — Năm hình theo thứ tự tổng quan, C1, C2, C3 controller và Deployment.
- [Kiến trúc agentgateway trên Kubernetes](./kien-truc-agentgateway-tren-kubernetes/kien-truc-agentgateway-tren-kubernetes.md)
- [Gateway API](./gateway-api/gateway-api.md) — Mức độ tuân thủ (conformance) Kubernetes Gateway API, các extension riêng (BackendTLSPolicy, header CEL, extAuth, HTTP filter) và tiêu chí so sánh các bản triển khai.

### Policies

- [Tổng quan Policy](./tong-quan-policy/tong-quan-policy.md) — Custom resource AgentgatewayPolicy và ba phân mục `frontend` / `traffic` / `backend`.
- [Thứ tự xử lý Policy](./thu-tu-xu-ly-policy/thu-tu-xu-ly-policy.md) — Bốn giai đoạn Frontend → PreRouting → PostRouting → Backend và thứ tự thực thi cố định của các traffic filter.
- [Targeting và Merging](./targeting-va-merging/targeting-va-merging.md) — Quy tắc nhắm mục tiêu theo loại tài nguyên, merge cấp trường, thứ tự ưu tiên và `inheritance`.
- [Conditional Policy](./conditional-policy/conditional-policy.md) — Chạy các biến thể policy khác nhau trên cùng một route theo biểu thức CEL (first-match-wins).
