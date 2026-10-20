# Nghiên cứu

Các bài nghiên cứu được phân loại theo chủ đề chuyên sâu. Mỗi bài nằm trong một thư mục riêng gồm bản tài liệu Markdown, thư mục `assets/` chứa sơ đồ tương tác và `evidence/` chứa bằng chứng dữ liệu kiểm chứng.

## Chủ đề Nghiên cứu

- [Agent Platform](./ngan-hang-so/) — Build agent platform cho MBbank
- [Top Github project](./kien-truc/) — Các top project tren github đang thử nghiệm
- [Tác tử AI (Agents)](./agents/) — Nguyên lý kiến trúc tác tử AI (12-Factor Agents), harness engineering, quy trình bàn giao đa tác tử (GPT Web - Drive - Kanban) và giám sát vận hành.
- [Hermes](./hermes/) — Hệ sinh thái tác tử Hermes Agent: Tích hợp Mem0 Long-Term Memory, Langfuse Observability, điều phối đa tác tử và công cụ kiến trúc.
- [JD-AI](./jd-ai/) — Phân tích các bản mô tả công việc liên quan đến kỹ sư AI, năng lực kỹ thuật và yêu cầu vận hành.

## Quy ước cấu trúc

```text
nghien-cuu/
└── chu-de/
    └── ten-bai/
        ├── index.md            # Bài chính (hoặc tách thành nhiều file .md)
        ├── assets/             # Sơ đồ HTML / JSON
        └── evidence/           # Bằng chứng kiểm chứng & dữ liệu nguồn
```

> [!NOTE]
> Các thư mục con trong `nghien-cuu/` đại diện cho các nhóm chủ đề lớn — sidebar VitePress sẽ tự động quét và phân nhóm thành các danh mục có thể thu gọn.
