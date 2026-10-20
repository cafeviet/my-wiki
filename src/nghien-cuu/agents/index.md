# Tác tử AI (Agents)

Các bài nghiên cứu về nguyên lý kiến trúc tác tử AI, harness engineering và hạ tầng điều phối vận hành đa tác tử.

## Danh mục Nghiên cứu

- [12-Factor Agents: Phân tích Kiến trúc](./12-factor-agents/phan-tich-kien-truc) — Nguyên lý xây dựng tác tử AI tin cậy để đưa vào sản xuất. Gồm [Bản phân tích kiến trúc](./12-factor-agents/phan-tich-kien-truc) và [Toàn văn bản dịch 13 bài](./12-factor-agents/bo-12-factor/).
- [Handoff Đa tác tử (GPT Web - Drive - Kanban)](../hermes/gptweb-google-drive-hermes-kanban/) — Kiến trúc bàn giao nhiệm vụ cho nhiều Agent: Google Drive làm transport, Hermes Kanban làm control plane.
- [Vận hành & Giám sát Handoff Tác tử](../hermes/van-hanh-giam-sat-hermes-handoff/) — Quan sát tác tử chạy nền: ba bề mặt quan sát, vòng chẩn đoán và bảng phân loại lỗi thực chiến.
- [AI Engineering Coach với Hermes](../hermes/ai-engineering-coach-hermes/) — Plugin & Skill hướng dẫn kỹ thuật trên nền Hermes Agent.

## Quy ước cấu trúc

```text
nghien-cuu/agents/
└── ten-bai/
    ├── index.md            # Bài nghiên cứu chính
    ├── assets/             # Sơ đồ HTML / JSON
    └── evidence/           # Dữ liệu nguồn & hồ sơ kiểm chứng
```
