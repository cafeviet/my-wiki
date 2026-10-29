---
title: Kiến trúc & Lộ trình Enterprise Agent Platform
---

# Kiến trúc & Lộ trình Enterprise Agent Platform

**Tài liệu kiến trúc tham chiếu và lộ trình triển khai Nền tảng Tác nhân Doanh nghiệp (Enterprise Agent Platform)**

**Trạng thái:** Tài liệu tổng hợp ban đầu (working draft)
**Phạm vi:** Kiến trúc tham chiếu (Reference Architecture), use case Trung tâm Vận hành (TTVH), triển khai Agentgateway và kế hoạch thực thi Production.
**Liên quan:** Chuyên đề bổ trợ cho [Báo cáo Quản trị Tác nhân AI trong Doanh nghiệp Ngân hàng](./). Các sơ đồ dưới đây là hình tham chiếu để đối chiếu thiết kế; **không phải chứng nhận đã triển khai hoặc phê duyệt Production**.

---

## 1. Tổng quan — Kiến trúc tham chiếu (Reference Architecture)

![Kiến trúc tham chiếu Enterprise Agent Platform](/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/assets/eap-overview.svg)

**Mục đích:** Cung cấp góc nhìn tổng thể về các thành phần và ranh giới của nền tảng Agent doanh nghiệp. Đây là hình tham chiếu để đối chiếu thiết kế triển khai chi tiết, không mặc định mọi thành phần đều đã được triển khai.

**Cần làm rõ khi chốt HLD (High-Level Design):** ranh giới tin cậy (trust boundaries), luồng dữ liệu (data flows), danh tính và phân quyền (identity and authorization), phân tách control plane / data plane, kiểm toán (audit) và yêu cầu phi chức năng (Non-Functional Requirements — NFR).

## 2. Use Case trọng tâm — AI Operation Agent (TTVH)

![Use case TTVH — AI Operation Agent](/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/assets/eap-usecase-ttvh.png)

**Mục tiêu thể hiện trong sơ đồ:** Agent tiếp nhận cảnh báo/sự cố, hỗ trợ phân tích nguyên nhân gốc (Root Cause Analysis — RCA), khoanh vùng và đề xuất hướng xử lý trong mục tiêu dưới 15 phút; tương tác qua Microsoft Teams/Email.

**Nhóm tích hợp được thể hiện:** nguồn cảnh báo (MB Monitor, Email, Teams), nguồn dữ liệu vận hành và tri thức (CMDB, AMT, OEM, Prometheus, Grafana, ELK, K8s, cùng các hệ thống cần kết nối), tầng công cụ MCP (Model Context Protocol), mô hình AI và người dùng vận hành.

**Lưu ý:** Mục tiêu dưới 15 phút là mục tiêu nghiệp vụ trên sơ đồ, chưa phải SLA được chứng minh. Cần đo riêng thời gian phát hiện, thu thập ngữ cảnh, suy luận và trả kết quả; định nghĩa tiêu chí RCA chính xác và trường hợp phải chuyển người xử lý.

## 3. Agentgateway Deployment — Kiến trúc triển khai

![Agentgateway deployment trên OpenShift](/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/assets/eap-agentgateway-deployment.png)

**Phạm vi hình:** Mô tả triển khai trên OpenShift Container Platform (OCP), với F5/LB, OpenShift Router, các namespace dịch vụ, Agentgateway, các thành phần quản lý/định danh, model serving, rate limiting, MCP servers và hạ tầng dùng chung.

**Điểm cần xác nhận trước Production:** tuyến mạng và TLS end-to-end, phân quyền giữa các workload, HA (High Availability) và khôi phục, bảo vệ secret, quản lý phiên bản và cấu hình, logging/tracing, giới hạn lưu lượng, phương án rollback và quyền gọi công cụ MCP.

**Giới hạn:** Hình này mô tả một lát cắt triển khai kỹ thuật; không nên coi là sơ đồ đầy đủ về quản trị vòng đời Agent, phê duyệt hành động và toàn bộ hệ thống nghiệp vụ.

## 4. Kế hoạch thực thi — Implementation Roadmap

![Kế hoạch triển khai Enterprise Agent Platform](/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/assets/eap-implementation-roadmap.png)

Kế hoạch được chia thành bốn phase theo hình minh họa:

| Phase | Tên tiếng Anh | Mục tiêu |
|---|---|---|
| A | Controlled Production Connectivity | Kết nối Production có kiểm soát; xây dựng nền tảng và kiểm tra tích hợp ban đầu |
| B | Managed Agent Runtime & Governance | Quản lý runtime, vòng đời, chính sách, giám sát và quản trị Agent |
| C | Governed Production Actions | Chuẩn hóa hành động, tích hợp phê duyệt và thực thi an toàn |
| X | Production Assurance | Kiểm chứng mức độ sẵn sàng vận hành và bảo mật |

**Các mốc trong hình:** A01–A09, B01–B07, C01–C05, X01–X02. Tên và phạm vi từng công việc được trình bày trong ảnh; bảng WBS (Work Breakdown Structure) chi tiết, phụ thuộc, owner và tiêu chí nghiệm thu (acceptance criteria) cần quản lý trong tài liệu riêng để tránh suy diễn từ infographic.

**Lưu ý về thứ tự:** Các phase được thể hiện theo luồng A → B → C → X nhằm dễ truyền đạt. Trên thực tế, kiểm soát an ninh và chuẩn bị vận hành của X phải được thực hiện xuyên suốt, không chỉ bắt đầu sau phase C.

## 5. Đề xuất hoàn thiện (Recommendations)

1. **Hồ sơ quyết định kiến trúc (Architecture Decision Records — ADR):** Ghi nhận lý do lựa chọn Agentgateway, cơ chế định danh, mô hình triển khai và các phương án bị loại.
2. **Mô hình bảo mật và tin cậy (Security & Trust Model):** Đặc tả quyền Agent → Tool → Production, chính sách least privilege, phê duyệt và audit trail.
3. **Điều kiện nghiệm thu Production (Production Gates):** Xác định tiêu chí đo được cho từng phase: connectivity, HA, security, observability, rollback, operational readiness.
4. **Đánh giá use case (Use-case Evaluation):** Xây bộ dữ liệu sự cố điển hình và kiểm thử độ chính xác RCA, thời gian phản hồi, hallucination, khả năng từ chối hành động rủi ro.
5. **Phân tách trách nhiệm (Separation of Responsibilities):** Làm rõ owner của Platform, Agent team, Ops, Security, IAM và hệ thống nguồn.

---

## Quy ước sử dụng

- Các hình được lưu tại `public/.../assets/` với đường dẫn tuyệt đối để tương thích với VitePress và kho Git.
- Nội dung diễn giải ngoài hình là đề xuất biên tập, cần được kiểm chứng với HLD/WBS và thiết kế triển khai thực tế.
- Không nên sử dụng infographic như bằng chứng nghiệm thu kỹ thuật.

---

> **Nguồn:** Tài liệu nội bộ `enterprise-agent-platform` (working draft). Bốn hình minh họa (overview, use case TTVH, Agentgateway deployment, implementation roadmap) được trích nguyên bản từ bộ tài liệu gốc. Đây là chuyên đề tham chiếu đi kèm [Báo cáo Quản trị Tác nhân AI trong Doanh nghiệp Ngân hàng](./).
