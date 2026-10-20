# AgentPlatfrom

Các bài nghiên cứu chuyên sâu xây dựng Agent Platform cho MB bank

## Danh mục Nghiên cứu

- [Đánh giá Sẵn sàng Công nghệ & AI (MBBank)](./mb-technology-and-ai-readiness/) — Chuyển dịch từ use case manh mún sang chuyển đổi theo Domain, mô hình Hub-and-Spoke (CoE & Delivery Squads), kiểm toán 11 AI use cases thực tế và ma trận 19 thành phần DataOps/MLOps. Kèm [Báo cáo Kiến trúc & Nợ Kỹ thuật CNTT](./mb-technology-and-ai-readiness/danh-gia-kien-truc-cntt).
- [Enterprise Agent Platform](./mb-enterprise-agent-platform-operations/) — Khung nền tảng Enterprise Agent Platform (14 cấu phần, bộ ba Gateway, runtime mở) kết hợp chiến trường thực tế Khối Vận hành & Tín dụng MB (155 văn bản, 106 điều kiện giải ngân, bẫy STP và điều phối 4 Agent chuyên trách).
- [Quản trị Agent Doanh nghiệp Ngân hàng](./mb-enterprise-agent-governance/) — Khung quản trị tập trung và kiến trúc mục tiêu cho tác nhân AI trong ngân hàng: 6 trụ cột, 9 nguyên tắc, giải quyết 5 điểm mù kỹ thuật (OAuth RFC 8693, Saga/Idempotency, Managed MCP, CI/CD Evals, ABAC) và kịch bản ngắt mạch (Circuit Breaker).
- [Kiến trúc Tham chiếu Agent Doanh nghiệp](./agent-reference-architecture/) — Khung kiến trúc tham chiếu hoàn chỉnh cho tác nhân AI: đối chiếu 5 đặc tính cốt lõi với 5 dạng thất bại, tư duy Harness 4 góc phần tư (KNOW, DO, CONTROL, VERIFY & LEARN), phân tầng Gateway L7, ranh giới Zero Trust và lộ trình Stage Gates.
- [POC Agent cho Dev](./agent-poc-dev/) — Phạm vi thu gọn để một dev chạy trên máy cá nhân: Harness, Tool PEP, PDP fail-closed, phê duyệt gắn payload, đối soát khi timeout; 20 test xác định và chạy thật với Ollama.

## Quy ước cấu trúc

```text
nghien-cuu/ngan-hang-so/
└── ten-bai/
    ├── index.md            # Bài nghiên cứu chính
    ├── assets/             # Sơ đồ HTML / JSON
    └── evidence/           # Dữ liệu nguồn & hồ sơ kiểm chứng
```
