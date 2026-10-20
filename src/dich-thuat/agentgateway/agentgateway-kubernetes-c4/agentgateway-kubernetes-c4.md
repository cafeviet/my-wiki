---
title: "Agentgateway: kiến trúc Kubernetes và mô hình C4"
description: "Năm sơ đồ tổng quan, bối cảnh, đơn vị thực thi, thành phần và triển khai."
---

# Agentgateway: kiến trúc Kubernetes và mô hình C4

Nguồn: [Architecture — Agentgateway](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/architecture/). Ngày tổng hợp: 09/10/2026.

Tài liệu gom năm hình đã xây dựng trong cuộc trao đổi. Đây là bản mô hình hóa tiếng Việt theo nguồn, không phải bản dịch toàn văn. Các hình là diễn giải kiến trúc; sơ đồ triển khai dùng tình huống minh họa hai Gateway.

## 1. Kiến trúc tổng quan — Architecture overview

Mặt phẳng điều khiển (Control plane) phân phối cấu hình; mặt phẳng dữ liệu (Data plane) xử lý lưu lượng. Màu xanh dương biểu thị cấu hình (Configuration), xanh lá biểu thị lưu lượng (Traffic), tím biểu thị triển khai (Provisioning).

![Kiến trúc Agentgateway trên Kubernetes](/dich-thuat/agentgateway/agentgateway-kubernetes-c4/assets/00-architecture.png)

## 2. C1: Bối cảnh hệ thống — System Context

Góc nhìn các hệ thống và người tương tác với Agentgateway. Kubernetes API nằm ngoài ranh giới phần mềm Agentgateway; điều này không có nghĩa nó nằm ngoài cụm Kubernetes.

![C1 — Bối cảnh hệ thống](/dich-thuat/agentgateway/agentgateway-kubernetes-c4/assets/01-c4-context.png)

## 3. C2: Đơn vị thực thi — Container

Góc nhìn trách nhiệm của bộ điều khiển (Controller) và proxy. Đơn vị thực thi (Container) trong C4 là khái niệm kiến trúc, không đồng nghĩa với Docker container.

![C2 — Đơn vị thực thi](/dich-thuat/agentgateway/agentgateway-kubernetes-c4/assets/02-c4-container.png)

## 4. C3: Thành phần — Component

Góc nhìn bên trong bộ điều khiển (Controller): krt collections, máy chủ xDS (xDS server), bộ triển khai (Deployer). Proxy là đơn vị thực thi hỗ trợ bên ngoài ranh giới controller. Sơ đồ phản ánh trách nhiệm logic, không khẳng định ánh xạ đến lớp mã nguồn.

![C3 — Thành phần controller](/dich-thuat/agentgateway/agentgateway-kubernetes-c4/assets/03-c4-component.png)

## 5. Góc nhìn triển khai — Deployment

Minh họa hai Gateway. Đây là ví dụ tô-pô (Topology), không phải cấu hình triển khai đã kiểm chứng tại my-wiki hoặc hệ thống của người dùng.

![Triển khai Agentgateway trên Kubernetes](/dich-thuat/agentgateway/agentgateway-kubernetes-c4/assets/04-c4-deployment.png)

## 6. Cách đọc và giới hạn — Reading guide and limitations

- C1 → C2 → C3 tăng dần mức chi tiết về phần mềm.
- Triển khai (Deployment) là góc nhìn bổ sung. Cấp C4 thứ tư là mã nguồn (Code), chưa được xây dựng trong tài liệu này.
- Nét đứt ở bộ C4 biểu thị ranh giới (Boundary), không phải kết nối mạng.
- Các hình chưa mô tả đầy đủ dự phòng (High availability), quan sát vận hành (Observability) hay ranh giới tin cậy (Trust boundary).

## 7. Tài liệu tham khảo — References

- [Agentgateway Architecture](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/architecture/)
- [Agentgateway Overview](https://agentgateway.dev/docs/kubernetes/latest/documentation/about/overview/)
- [C4 Container diagram](https://c4model.com/diagrams/container)
- [C4 Component diagram](https://c4model.com/diagrams/component)
- [C4 Deployment diagram](https://c4model.com/diagrams/deployment)
