# Hermes 

Các bài nghiên cứu, cong cu tich hop len hermes

## Danh mục Nghiên cứu

- [Handoff Đa tác tử (GPT Web - Drive - Kanban)](./gptweb-google-drive-hermes-kanban/) — Kiến trúc bàn giao nhiệm vụ cho nhiều Agent: Google Drive làm transport, Hermes Kanban làm control plane.
- [Vận hành & Giám sát Handoff Tác tử](./van-hanh-giam-sat-hermes-handoff/) — Quan sát tác tử chạy nền: ba bề mặt quan sát, vòng chẩn đoán và bảng phân loại lỗi thực chiến.
- [AI Engineering Coach với Hermes](./ai-engineering-coach-hermes/) — Plugin & Skill hướng dẫn kỹ thuật trên nền Hermes Agent.
- [Architecture-as-Code với Archify](./architecture-as-code-archify/) — Diagram-as-Code Engine, Typed JSON Intermediate Representation, Agent Skill Loop và so sánh công cụ trực quan hóa kiến trúc.
- [Kiến trúc Giải pháp: Hermes Agent tích hợp Langfuse](./hermes-langfuse-integration/) — Observer Hooks, mô hình trace/generation/observation, cấu hình plugin, bẫy ACL trên Windows, chế độ v4 events_only và lộ trình trace gateway 9Router.
- [Hướng dẫn Tích hợp & Vận hành: Mem0 Long-Term Memory cho Hermes Agent](./hermes-mem0-integration/) — Kiến trúc bộ nhớ dài hạn Mem0 Self-Hosted (PostgreSQL pgvector, FastAPI, Dashboard), giải quyết bẫy Windows Docker, tích hợp Agent Tool và Lifecycle Hooks.

## Quy ước cấu trúc

```text
nghien-cuu/agents/
└── ten-bai/
    ├── index.md            # Bài nghiên cứu chính
    ├── assets/             # Sơ đồ HTML / JSON
    └── evidence/           # Dữ liệu nguồn & hồ sơ kiểm chứng
```
