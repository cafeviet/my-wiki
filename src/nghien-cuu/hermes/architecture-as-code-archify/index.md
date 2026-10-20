# Architecture-as-Code với Archify

> **Phiên bản tổng hợp** — Hợp nhất toàn bộ nội dung trao đổi về Archify, cơ chế Agent Skill, CLI, khả năng mở rộng Server/API/MCP, tích hợp với Landscape/Architecture Repository, và so sánh với Mermaid, PlantUML, LikeC4.

---

## 1. Executive Summary

Archify không chỉ là công cụ "vẽ sơ đồ" — đây là một **Diagram-as-Code Engine** với các lớp:

- **Typed JSON IR** – Biểu diễn trung gian JSON có kiểu
- **Schema Validation** – Kiểm tra schema
- **Layout & Routing Validation** – Kiểm tra bố cục và đường nối
- **Deterministic Renderer** – Bộ kết xuất xác định
- **Interactive Artifact** – Giao phẩm tương tác
- Tích hợp tự nhiên với **AI Agent / Coding Agent**

**Nguyên tắc cốt lõi:**

> **LLM không trực tiếp vẽ SVG. AI thiết kế nội dung và cấu trúc diagram; code của Archify kiểm tra và render diagram.**

### Luồng cốt lõi

<iframe src="/nghien-cuu/kien-truc/architecture-as-code-archify/assets/diagram-01-core-pipeline.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

Mô hình khuyến nghị trong doanh nghiệp:

```
Landscape / Architecture Repository
             ↓
       Canonical Model
             ↓
       View Definition
             ↓
     Archify JSON IR
             ↓
          Archify
             ↓
   Architecture Artifact
```

LLM được dùng cho: Understand · Select · Explain · Analyze · Recommend · Generate ad-hoc view

Code được dùng cho: Query · Transform · Validate · Layout · Route · Render · Publish

---

## 2. Bối cảnh và mục tiêu

Trong quản trị kiến trúc doanh nghiệp, các đối tượng như System, Container, Component, Microservice, API, Database, Kafka Topic, Owner, Domain, Deployment, Dependency, Integration cần được quản lý như một **Architecture Model** thay vì chỉ tồn tại dưới dạng sơ đồ tĩnh.

Các yêu cầu chính:

1. Có **Canonical Source of Truth** (Nguồn sự thật chuẩn)
2. Sinh được nhiều diagram từ cùng một model
3. Hỗ trợ **Architecture-as-Code**
4. Hỗ trợ AI Agent nhưng không để AI trở thành nguồn sự thật
5. Diagram phải có khả năng validate
6. Đưa trực tiếp giao phẩm lên Landscape Portal
7. Hỗ trợ CI/CD, versioning, delta, governance
8. Triển khai được cả local CLI và central service

---

## 3. Archify là gì?

Archify là hệ thống render diagram dựa trên **Typed JSON IR**.

Các loại diagram: `architecture` · `workflow` · `sequence` · `dataflow` · `lifecycle`

Output: Self-contained HTML · SVG · PNG · Interactive architecture artifact

**Vai trò phù hợp:**

```
Architecture Presentation Engine
+
Diagram-as-Code Engine
+
Validation Harness
```

> Archify **không** phải Architecture Repository.

---

## 4. Cơ chế hoạt động

### LLM làm gì?

LLM chịu trách nhiệm ở lớp **Semantic Reasoning**:

- Đọc yêu cầu và codebase
- Xác định component và relationship
- Chọn abstraction level, node hiển thị, luồng chính, boundary, hierarchy
- Tạo Typed JSON IR
- Nhận lỗi validator và sửa candidate

### Code làm gì?

Archify code chịu trách nhiệm: JSON Schema validation · resolve node coordinates · grid placement · node dimensions · edge anchors · route calculation · port spreading · collision detection · label placement · route clearance · SVG generation · HTML packaging · deterministic export

> **AI quyết định WHAT; code quyết định phần lớn HOW TO RENDER.**

### Pattern Harness Engineering

```
Probabilistic Reasoning
        ↓
Structured IR
        ↓
Verification
        ↓
Deterministic Execution
```

---

## 5. Typed JSON IR – Ví dụ

```json
{
  "schema_version": 1,
  "diagram_type": "architecture",
  "meta": { "title": "Payment Architecture", "quality_profile": "showcase" },
  "layout": { "mode": "grid", "cols": 4 },
  "components": [
    { "id": "mobile",   "type": "frontend", "label": "MB App",          "row": 0, "col": 0 },
    { "id": "gateway",  "type": "backend",  "label": "API Gateway",     "row": 0, "col": 1 },
    { "id": "payment",  "type": "backend",  "label": "Payment Service", "row": 0, "col": 2 },
    { "id": "database", "type": "database", "label": "Payment DB",      "row": 1, "col": 2 }
  ],
  "connections": [
    { "from": "mobile",  "to": "gateway",  "label": "HTTPS" },
    { "from": "gateway", "to": "payment",  "label": "REST"  },
    { "from": "payment", "to": "database", "label": "SQL"   }
  ]
}
```

> Archify JSON là **Presentation IR** — không phải Canonical Architecture Model.

---

## 6. Validation Harness

Archify kiểm tra: schema error · overlapping component · route xuyên qua component · edge crossing · ambiguous corridor · boundary issue · label overlap · label-to-route clearance · route rhythm.

Agent repair loop:

```
LLM → candidate.json → Validator
                           ├── PASS → Renderer → HTML
                           └── FAIL → diagnostics → LLM sửa JSON → (lặp lại)
```

---

## 7. Kiến trúc mục tiêu với Landscape

<iframe src="/nghien-cuu/kien-truc/architecture-as-code-archify/assets/diagram-02-target-architecture.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

**Landscape là nguồn sự thật.** Archify là presentation engine nhận dữ liệu từ Landscape, không lưu trữ model.

| Thành phần | Vai trò |
|---|---|
| Landscape DB | Canonical Architecture Model |
| View Definition | Chỉ định "cần diagram gì" |
| Archify JSON IR | Presentation IR — generated artifact |
| Archify Engine | Validate + Render |
| Architecture Portal | Hiển thị artifact cho stakeholder |

---

## 8. Agent Skill Loop

<iframe src="/nghien-cuu/kien-truc/architecture-as-code-archify/assets/diagram-03-agent-loop.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

### Hai harness vận hành

**Agent Harness** (AI Layer):
1. LLM nhận yêu cầu / đọc codebase
2. Tạo candidate Typed JSON IR
3. Gọi `archify validate` — nhận diagnostics
4. Sửa JSON nếu FAIL, lặp lại

**Execution Harness** (Engine Layer):
1. Nhận JSON đã pass validate
2. Layout Engine tính grid, coords, edges
3. Renderer sinh SVG + HTML
4. Xuất self-contained artifact

### Skill vs Tool

| | Skill | Tool (MCP) |
|---|---|---|
| Cơ chế | Agent đọc SKILL.md, tự tạo JSON, gọi CLI | Agent gọi tool_call → Server xử lý |
| Phù hợp | POC, local, coding agent | Enterprise, multi-agent, central service |
| Tri thức | Procedural knowledge | Callable API contract |

### CLI Reference

```bash
git clone https://github.com/tt-a1i/archify.git
cd archify/archify && npm ci
node bin/archify.mjs doctor
node bin/archify.mjs validate architecture input.json --quality showcase --json
node bin/archify.mjs deliver architecture input.json output.html --quality showcase --json
```

---

## 9. Hai lane vận hành

### Standard Views (không cần LLM)

```
Landscape → View Definition → View Generator → Archify JSON → Archify → HTML
```

Ví dụ: Enterprise View · Domain View · System Overview · Runtime View · Integration View · Deployment View · Security View · Data Flow

### Ad-hoc Views (có LLM)

```
User Question → LLM Agent → View Definition / Typed JSON IR → Archify → Artifact
```

> Không nên bắt LLM nằm giữa **mọi** luồng — standard views nên chạy deterministic.

---

## 10. Tích hợp với Architecture Portal

**Khuyến nghị Write-time Rendering:**

```
JSON changed → Render → Store Artifact
User Click   → Open Artifact
```

Trigger: Khi save Landscape · File Watcher · CI/CD (Git Commit → Pipeline → Validate → Render → Publish)

---

## 11. Mở rộng thành Server/API/MCP

**V1 – HTTP Wrapper:** `POST /api/v1/diagrams/validate` · `render` · `compare`

**V2 – Tách Archify Core:** CLI · REST API · MCP dùng chung schema/validator/renderer

- **MCP** khi consumer chủ yếu là AI Agent
- **REST** khi consumer là Portal, CI/CD, backend

---

## 12. So sánh công cụ

<iframe src="/nghien-cuu/kien-truc/architecture-as-code-archify/assets/diagram-05-tool-comparison.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

| Khía cạnh | Archify | Mermaid | PlantUML | LikeC4 |
|---|---|---|---|---|
| Bản chất | Structured IR + Validator + Renderer | Text DSL + Renderer | Text DSL + Renderer | Architecture Model + Views |
| Input | JSON IR | Text DSL | Text DSL | `.c4` / `.likec4` |
| LLM-first | Rất mạnh | Có thể | Có thể | Có thể |
| Visual validation | Mạnh | Hạn chế | Hạn chế | Model/view level |
| Architecture model | Hạn chế hơn LikeC4 | Yếu | Yếu–trung bình | Rất mạnh |
| LLM repair loop | Thiết kế sẵn | Tự xây | Tự xây | Tự xây |

**Kết hợp thực tế:** Landscape DB → Mermaid (Docs) + LikeC4 (Architecture Views) + Archify (Interactive Artifact)

---

## 13. Architecture Layers

- **Layer 1** – Architecture Model (Landscape mạnh)
- **Layer 2** – View / Presentation IR (LikeC4 + Archify mạnh)
- **Layer 3** – Renderer (Archify mạnh)

---

## 14. Architecture Governance

```
Landscape DB    = Source of Truth
LikeC4          = Generated Model/View Projection
Archify JSON    = Generated Presentation IR
```

**Architecture Delta:** V1 → V2 → Graph Diff → Added/Removed/Changed → Delta Artifact

Use case: PR review · Architecture Review Board · AS-IS/TO-BE · Release governance

---

## 15. Repository Structure đề xuất

```
architecture/
├── model/      # source
├── views/      # source
├── generated/  # không sửa tay (archify/ + html/)
├── rules/
└── ci/
```

---

## 16. Lộ trình triển khai

<iframe src="/nghien-cuu/kien-truc/architecture-as-code-archify/assets/diagram-04-deployment-phases.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

| Phase | Tên | Mục tiêu chính |
|---|---|---|
| 1 | Local Agent + Skill | Hiểu cơ chế, test JSON IR và validation |
| 2 | Landscape → Archify | Standard views, portal integration, render-on-change |
| 3 | Architecture-as-Code | Version, diff, governance gate, architecture delta |
| 4 | AI Architecture Agent | Ad-hoc views, explain/analyze/recommend |
| 5 | Central Archify Service / MCP | Centralized version, security, audit, no version drift |

---

## 17. Rủi ro và kiểm soát

| Rủi ro | Kiểm soát |
|---|---|
| Duplicate Source of Truth | `generated/archify/` chỉ là generated artifact |
| LLM Hallucination | Lấy data từ Architecture Repository; validator/policy layer |
| Diagram Correct ≠ Architecture Correct | Thêm architecture rules, governance evaluator |
| Large Graph | Drill-down: Enterprise → Domain → System → Container |
| Version Drift | Central Archify Service / MCP ở scale enterprise |

---

## 18. Open Decisions

1. Canonical Model trong Landscape DB hay Git?
2. View Definition dùng YAML/JSON hay lưu DB?
3. Archify JSON lưu lâu dài hay generate transient?
4. Render khi save, khi commit hay theo batch?
5. Standard View nào bắt buộc cho mỗi System?
6. Có cần LikeC4 làm semantic projection layer?
7. Central Archify REST API hay MCP?
8. Architecture Delta chỉ dùng review hay block CI/CD?

---

## 19. Kết luận

> **Model giữ sự thật, LLM tạo reasoning, IR tạo contract, validator tạo trust, renderer tạo giao phẩm.**

Pattern này phát triển Architecture-as-Code thành một **AI-assisted Architecture Governance Platform**.

---

*Nguồn: Tổng hợp từ tài liệu trao đổi nội bộ về Archify solution — September 2026*
