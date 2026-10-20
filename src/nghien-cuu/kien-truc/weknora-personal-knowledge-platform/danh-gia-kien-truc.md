# Đánh giá Kiến trúc WeKnora & C4 Model

> **Tài liệu triển khai thực tế:** [Kiến trúc Triển khai WeKnora Docker Core](./)  
> **Phạm vi kiểm chứng:** Tencent/WeKnora tại commit [`6f98ff80c3185679cc16f834faf42fc662770e68`](https://github.com/Tencent/WeKnora/tree/6f98ff80c3185679cc16f834faf42fc662770e68), audit ngày 2026-09-16.  
> **Quy ước:** **[Fact]** là điều quan sát được trong repo/tài liệu chính thức; **[Inference]** là suy luận từ các fact; **[Recommendation]** là lựa chọn kiến trúc đề xuất cho máy cá nhân.  
> Các link nguồn bên dưới được ghim vào commit để tránh nội dung `main` thay đổi sau này.

## Tóm tắt điều hành

- **[Fact]** WeKnora tự định vị là framework tri thức mã nguồn mở dùng LLM cho hiểu tài liệu, truy hồi ngữ nghĩa và suy luận tự động; ba bề mặt chính là RAG Quick Q&A, ReAct Agent và Wiki Mode. Repo công bố giấy phép MIT cho mã dự án, kèm nghĩa vụ riêng cho thành phần bên thứ ba. [S1], [S2]
- **[Fact]** Phiên bản được khai báo trong `VERSION`, README và Helm `appVersion` là **0.8.0**; changelog ghi release 0.8.0 ngày **2026-09-03**. Commit được audit ngày 2026-09-15 mới hơn release đó, nên bài này mô tả trạng thái source tại commit, không khẳng định mọi thay đổi sau release đã có binary phát hành. [S1], [S3], [S4]
- **[Fact]** WeKnora có hai họ triển khai local chính: **Lite** một tiến trình với SQLite/FTS5/sqlite-vec và hàng đợi/stream trong bộ nhớ; **Standard Docker Compose** với frontend, Go app, docreader, ParadeDB/PostgreSQL và Redis. Trong Compose, “Core services” là tên nhóm dịch vụ mặc định; `full` là profile chính thức bật thêm nhiều dịch vụ. “Docker Core” không phải edition độc lập. [S5], [S6], [S7]
- **[Inference]** WeKnora không chỉ là viewer Markdown như my-wiki. Nó là lớp ingest/index/retrieval/reasoning/derived knowledge có trạng thái riêng, mô hình dữ liệu riêng và chi phí vận hành riêng.
- **[Recommendation]** Giữ **Markdown + Git trong my-wiki làm authoritative source / nguồn sự thật**. Dùng WeKnora làm **serving/index/agent layer** và Auto-Wiki làm **derived knowledge / tri thức dẫn xuất**. Không cho đồng bộ hai chiều tự do giữa Markdown gốc, chunk đã sửa và Wiki sinh bởi LLM.
- **[Recommendation]** Với một máy cá nhân: thử nhanh bằng Lite; nếu dùng lâu dài, ingest nền, Auto-Wiki, nhiều Agent/MCP hoặc cần phục hồi tác vụ tốt hơn thì chuyển sang Standard Compose core. Không bật `--profile full` mặc định; chỉ bật đúng profile cần thiết.

## 1. WeKnora là gì — và không phải là gì?

### 1.1 Định vị sản phẩm

**[Fact]** README mô tả WeKnora là “open-source, LLM-powered knowledge framework” cho document understanding, semantic retrieval và autonomous reasoning. Sản phẩm gom ba khả năng lõi: RAG Q&A, ReAct Agent và Wiki Mode; ngoài ra có long-term memory, Skills/Sandbox, MCP, RBAC, nhiều nguồn ingest, nhiều model/vector/object-storage provider và local/private deployment. [S1]

**[Inference]** “Personal Knowledge Platform” là cách dùng phù hợp, nhưng không phải cách định vị duy nhất của upstream: upstream thiên về enterprise-grade, multi-workspace và extensibility. Người dùng cá nhân nhận được một phần lớn năng lực enterprise, đồng thời phải chấp nhận nhiều moving parts hơn một static wiki.

**[Fact]** WeKnora hỗ trợ Web UI, REST API, CLI, Chrome extension, mini program và MCP Server. UI cho hỏi đáp, quản trị knowledge base, duyệt Wiki, xem graph, chỉnh chunk/Wiki và lịch sử phiên bản. [S1]

**[Inference]** WeKnora UI có thể thay viewer my-wiki cho tác vụ “tìm–hỏi–tổng hợp”, nhưng không thay hoàn toàn trải nghiệm đọc tài liệu tĩnh, URL ổn định, diff/review và publish bằng Git của VitePress.

### 1.2 Phiên bản, hoạt động repo và giấy phép

**[Fact]** Bản audit dùng remote chính thức `https://github.com/Tencent/WeKnora.git`, commit `6f98ff80c3185679cc16f834faf42fc662770e68`, commit time `2026-09-15T22:54:52+08:00`. Repo có `VERSION=0.8.0`; README badge và Helm appVersion cũng là 0.8.0; changelog có mục 0.8.0 ngày 2026-09-03. [S1], [S3], [S4]

**[Inference]** Có commit mới sau ngày release là bằng chứng repo vẫn hoạt động tại thời điểm audit. Nó không tự chứng minh SLA, độ ổn định production hay lịch support dài hạn.

**[Fact]** `LICENSE` nói mã dự án dùng MIT, ngoại trừ các third-party components được liệt kê và chịu điều khoản riêng; README yêu cầu attribution phù hợp. [S2]

**[Recommendation]** Khi đóng gói lại, giữ `LICENSE` và `THIRD_PARTY_NOTICES.md`; không diễn giải “MIT” thành việc mọi binary dependency đều chỉ chịu MIT.

## 2. Kiến trúc hệ thống

### 2.1 Standard Docker Compose

**[Fact]** Kiến trúc core mặc định gồm:

| Container / tiến trình | Vai trò |
|---|---|
| `frontend` | Vue 3 static app trên NGINX; reverse proxy `/api` đến app |
| `app` | Go backend: REST/SSE, RAG, Agent, worker, IM/embed |
| `docreader` | Python gRPC parser cho PDF/Office/web và nhiều định dạng |
| `postgres` | ParadeDB/PostgreSQL 17, dữ liệu nghiệp vụ + BM25 + pgvector |
| `redis` | Asynq queues, stream recovery, pub/sub, rate/concurrency control |

App và docreader dùng shared volume cho ảnh parse; app có volume file local. Vector DB, graph, object storage, web search và Langfuse là thành phần chọn thêm. [S6], [S7]

**[Fact]** `docker compose up -d` khởi động core services. Profile `full` bật một tập lớn gồm sandbox image, MCP server và các dịch vụ mang nhãn `full`; các profile riêng như `neo4j`, `minio`, `qdrant`, `searxng`, `langfuse` có thể bật độc lập. [S1], [S7], [S8]

**[Inference]** “Full” là convenience bundle, không phải lựa chọn tối ưu mặc định. Nó có thể bật đồng thời những thành phần một cá nhân không cần, tăng RAM, volume, secret, backup surface và rủi ro nâng cấp.

### 2.2 Lite

**[Fact]** Lite dùng `DB_DRIVER=sqlite`, `RETRIEVE_DRIVER=sqlite`, SQLite FTS5 + sqlite-vec, `STREAM_MANAGER_TYPE=memory`, frontend nhúng trong binary và không cần Redis/PostgreSQL. Upstream mô tả Lite là single app, zero external service stack, một workspace, không cần đăng ký; chỉ có Simple parser tích hợp nhưng có thể nối parser ngoài/cloud. [S5], [S6], [S9]

**[Fact]** Lite vẫn có thể cấu hình Docker/Cube/E2B sandbox theo workspace, nhưng không preconfigure backend. Desktop Wails dùng cùng runtime Lite nhưng tài liệu chính thức ghi chưa phát hành installer trong release tại thời điểm audit. [S6]

**[Inference]** “Zero dependencies” nghĩa là zero external infrastructure cho core runtime, không nghĩa là mọi workload đều offline hoặc không cần model. Embedding/chat/rerank vẫn phải đến Ollama hoặc API tương thích; parser nâng cao và một số feature cần dịch vụ khác.

### 2.3 Backend và ranh giới module

**[Fact]** Backend Go dùng dependency injection và các lớp handler/service/repository/infrastructure. Truyền thông chính gồm HTTP/SSE browser→frontend→app, gRPC app→docreader, PostgreSQL wire, Redis RESP, Bolt tới Neo4j, SDK/HTTP tới model/vector/storage, Docker Engine hoặc control plane tới sandbox. [S6]

**[Inference]** C4 Level 2 nên vẽ WeKnora như nhiều container ở Standard, nhưng như một container ứng dụng + SQLite ở Lite. Không nên vẽ Lite và Standard thành cùng một topology rồi chỉ đổi nhãn database.

## 3. Document ingestion và biểu diễn tri thức

### 3.1 Từ file đến chunk và index

**[Fact]** Entry points gồm upload file, import URL, manual content và reparse. Ở Standard, handler ghi record rồi enqueue tác vụ; worker thực hiện parse → image resolution → chunking → lưu chunk → embedding/index. Hậu xử lý có thể tạo caption/OCR, summary, generated questions, graph và Wiki. [S10]

**[Fact]** Parser chuẩn hóa kết quả về Markdown text + image bytes. Chunking chạy phía Go, hỗ trợ parent-child; parent chunk chỉ lưu DB, child chunk được index. Index có thể kết hợp vector và keyword/BM25. Nếu index lỗi, service xóa chunk/index đã ghi để tránh half-state. [S10]

**[Fact]** Tài liệu có state machine `pending → processing → finalizing → completed`, có retry, span progress và housekeeping cho stuck tasks. Tài liệu trở nên searchable sau khi index xong, trước khi mọi enrichment hoàn tất. [S10]

**[Inference]** Trạng thái “đã thấy trong search” không đồng nghĩa “Auto-Wiki/summary/graph đã hoàn tất”. UI/sync job cần phân biệt indexed, enriched và failed, thay vì chỉ coi upload HTTP thành công là hoàn tất.

### 3.2 Ba lớp tri thức

**[Inference]** Có thể hiểu dữ liệu WeKnora thành ba lớp:

1. **Source layer:** file/URL/manual knowledge và metadata.
2. **Retrieval layer:** parsed Markdown, chunks, embeddings, keyword index, generated questions, captions/OCR.
3. **Derived layer:** summaries, graph và Wiki pages.

**[Recommendation]** Với my-wiki, chỉ lớp 1 bắt nguồn từ Git được xem là authoritative. Lớp 2 có thể tái tạo; lớp 3 cần provenance, review và có thể xóa/tái sinh.

### 3.3 Chunk editing là một fork ngữ nghĩa

**[Fact]** WeKnora cho sửa chunk, lưu revision/diff/rollback và tự reindex; Wiki cũng cho chỉnh trực tiếp, version history và rollback. [S1], [S11]

**[Inference]** Khi sửa chunk trong UI, nội dung retrieval có thể khác Markdown trong Git. Đây là một fork ngữ nghĩa dù source file vẫn giữ nguyên.

**[Recommendation]** Trong kiến trúc Git-authoritative, không dùng chunk editor cho thay đổi nội dung lâu dài. Sửa file Markdown gốc, commit, rồi re-ingest. Chỉ dùng chunk edit cho điều tra/ngắn hạn và ghi issue quay về source.

## 4. Retrieval-Augmented Generation (RAG)

**[Fact]** RAG là event-driven plugin pipeline: load history → query understanding/rewrite → parallel chunk/entity/web search → rerank + Wiki boost → fetch web content nếu bật → merge → top-k → optional DuckDB analysis → context assembly → streaming completion. Kết quả và references đi qua SSE/StreamManager; Redis cho phép multi-instance và replay sau đứt kết nối. [S12]

**[Fact]** Retrieval có thể fan-out qua nhiều stores, kết hợp vector + keyword bằng weighted reciprocal-rank fusion. Rerank có fallback, threshold degradation, composite score và MMR diversity. Wiki chunks được boost sau rerank khi KB bật Wiki. [S12]

**[Inference]** Đây là pipeline có nhiều policy, không phải “vector search rồi nhét top-k vào prompt”. Chất lượng phụ thuộc parser, chunking, embedding space, keyword/vector fusion, reranker, thresholds, Wiki boost và prompt/model.

**[Fact]** Hệ thống phát reference list và có citation alias protocol; unknown alias bị loại. [S12]

**[Recommendation]** Đánh giá bằng tập câu hỏi thực tế và kiểm tra citation/source passage, không chỉ đọc câu trả lời trôi chảy. Dùng một bộ regression nhỏ gồm: exact fact, cross-document comparison, stale doc, conflicting docs, Vietnamese terminology và câu không có trong corpus.

## 5. Auto-Wiki: tri thức dẫn xuất, không phải source-of-truth

**[Fact]** Wiki Mode biến knowledge-base documents thành các Markdown pages liên kết. Pipeline Map–Reduce gồm candidate extraction, chunk-level citation, reduce/merge theo slug và finalize bằng SQL/graph algorithms. Page có `SourceRefs` và `ChunkRefs`; có entity/concept/summary/index, còn synthesis/comparison do Agent tạo. [S11]

**[Fact]** Wiki page hỗ trợ manual edit, lịch sử version, line diff và rollback. Revision history có soft limit 50 ưu tiên tỉa pipeline snapshots và hard limit 200 cho mọi nguồn. Wiki không có anonymous public mode; read/write vẫn chịu KB access/RBAC. [S11]

**[Fact]** Agent có công cụ đọc, search, ghi, replace, rename, delete Wiki page và flag issue. Generated page được boost trong RAG. [S11], [S12]

**[Inference]** Auto-Wiki là một materialized, LLM-derived view của corpus. Citation grounding, revisions và manual correction làm nó audit-friendly hơn bản tóm tắt vô nguồn, nhưng không loại bỏ lỗi tổng hợp, merge nhầm entity, stale derived page hoặc bias do Wiki boost.

**[Recommendation]** Gắn nhãn rõ “Generated/Derived”; giữ link về source commit/path; không copy ngược Wiki-generated text vào authoritative Markdown nếu chưa review; khi source đổi, re-ingest và kiểm tra affected pages. Các quyết định quan trọng phải trích source document, không chỉ trích Wiki page.

## 6. Agent, context, memory, Skills và Sandbox

### 6.1 Quick Answer và ReAct Agent

**[Fact]** Custom Agent có `quick-answer` dùng RAG pipeline và `smart-reasoning` dùng ReAct, có thể giới hạn KB, web search, MCP và skill. Scope cấu hình không vượt quyền của principal hiện tại. [S13]

**[Fact]** Agent runtime dựng context gồm system prompt, runtime/user context, memory (nếu bật), skills, model metadata, history và resource scope; có context compaction cho vòng tool dài. [S13]

**[Inference]** Agent là consumer của knowledge platform, không phải cơ chế đảm bảo fact. Nó tăng khả năng thao tác đa bước và cũng tăng attack surface: prompt injection từ document/tool output, side effects và secret exposure.

### 6.2 Long-term memory

**[Fact]** Memory 0.8.0 độc lập với Neo4j conversation memory cũ. Nó lưu profile/preference/fact/task/interest theo workspace và caller identity; inferred items ở trạng thái pending đến khi user xác nhận. Workspace và user đều có opt-in/out; mặc định workspace disabled. Memory có thể ảnh hưởng query understanding và document ranking nhưng không mở rộng KB permission. [S3], [S14]

**[Recommendation]** Bắt đầu bằng `explicit_only`; chỉ bật auto-extract sau khi có thói quen review pending items. Backup/export memory riêng; không coi memory là tài liệu tham chiếu chính thức.

### 6.3 Skills và Sandbox

**[Fact]** Skill là bundle `SKILL.md` + scripts/templates/references. Runtime hỗ trợ Docker, CubeSandbox và E2B; local host-process backend đã bị loại. Docker backend mặc định tắt vì mount `docker.sock` trao quyền điều khiển Docker host cho app. Sandbox có network policy nhưng Docker không có rule chi tiết như Cube/E2B; `/workspace` chỉ là convention, không phải security boundary tự thân. [S3], [S15]

**[Recommendation]** Trên máy cá nhân, để Skills/Sandbox tắt cho đến khi có use case. Nếu bật Docker: dùng image cố định, resource limits, network `none` hoặc allowlist, không mount thư mục my-wiki ở chế độ write, không đặt secret rộng trong workspace env và xem `docker.sock` là quyền root tương đương.

## 7. MCP theo hai hướng

### 7.1 WeKnora consume external MCP

**[Fact]** WeKnora là MCP client cho remote SSE/Streamable HTTP; stdio bị chặn ở client runtime vì command-injection risk. External tools có thể được đăng ký vào Agent, với API key/Bearer/OAuth, per-tool enable/approval và in-conversation OAuth. Tool output được gắn nhãn untrusted; approval mặc định fail-close nếu DB check lỗi. [S16]

**[Recommendation]** Allowlist service/tool; bật approval cho write/delete/network-send; dùng OAuth/API key theo principal; không cho một Agent `all` MCP services nếu chỉ cần vài tool.

### 7.2 WeKnora expose knowledge qua MCP

**[Fact]** `mcp-server/` là Python package độc lập `tencent-weknora-mcp`, gọi REST API bằng `X-API-Key` và expose knowledge/search/chat/agent/wiki tools qua stdio, SSE hoặc HTTP. Network transport yêu cầu auth token; file upload có allowed-directory checks. Tài liệu feature tại commit nói 31 tools, trong khi README summary ở cùng commit còn nói 29 tools—đây là documentation drift; danh sách chi tiết/code nên là căn cứ khi triển khai. [S1], [S16]

**[Inference]** Đây là đường tích hợp tự nhiên cho coding/personal agents: chúng có thể search/read/ask WeKnora mà không cần truy cập trực tiếp PostgreSQL/vector store.

**[Recommendation]** Với external agent, tạo scoped API key read-only/retrieve-only nếu có thể; không expose tenant/KB delete và knowledge write mặc định. Bind network MCP về loopback hoặc private network; không public internet trực tiếp.

## 8. Auth, RBAC và local security

**[Fact]** Standard có JWT/API key/OIDC và workspace RBAC 4 cấp Viewer < Contributor < Admin < Owner, cộng ownership per KB/Agent và audit log. RBAC mặc định enforcement `true`. [S17]

**[Fact]** README khuyến cáo đặt WeKnora trong internal/private network, không expose trực tiếp Internet, có firewall/access control và cập nhật security fixes. [S1]

**[Inference]** “Chạy local” không tự động an toàn: frontend/app port, model endpoints, MCP network transport, Docker daemon, imported URLs và browser/file parsers đều là attack surface.

**[Recommendation]** Single-user vẫn nên: bind loopback; đổi mọi default secret; đặt `WEKNORA_VERSION` cố định thay vì `latest`; backup volume; dùng API key scope tối thiểu; tắt registration/network services không dùng; review imported untrusted documents; không cho sandbox write vào Git source.

## 9. Lite vs Standard Core vs Full

| Tiêu chí | Lite | Standard Compose core | `full` profile |
|---|---|---|---|
| **[Fact] Runtime** | 1 app + embedded UI | frontend + app + docreader + PostgreSQL + Redis | Core + bundle optional services |
| **[Fact] Data/retrieval** | SQLite FTS5 + sqlite-vec | ParadeDB/Postgres BM25 + pgvector | Thêm Qdrant/Neo4j/MinIO/SearXNG… theo compose |
| **[Fact] Queue/stream** | memory/synchronous fallback | Redis/Asynq + worker pools | Như core, thêm observability/services |
| **[Fact] Workspace/parser** | single workspace; Simple built-in | multi-workspace; full parser chain | Như Standard |
| Backup | DB file + local files/config | named volumes + config/secrets | Nhiều volume và dependency hơn |
| Failure recovery | đơn giản nhưng ít durability/concurrency hơn | queue/retry/housekeeping tốt hơn | nhiều failure modes hơn |
| Phù hợp | pilot, offline-ish, ít tài liệu | personal long-lived, agent/MCP/Wiki | lab cần nhiều optional feature cùng lúc |

**[Recommendation] Lộ trình:**

1. **Pilot Lite:** 50–200 tài liệu đại diện; local/remote models; test retrieval/citation; chưa bật Skills.
2. **Chọn checkpoint:** nếu SQLite đủ và thao tác ít, giữ Lite; nếu cần ingest concurrency, parser chain, Auto-Wiki dài hạn, audit/RBAC/API integrations, chuyển Standard core.
3. **Standard core:** pin version; dùng Postgres/Redis/local storage; chỉ thêm `mcp` hoặc `neo4j`/`minio` khi có nhu cầu được đo lường.
4. **Không dùng `full` như synonym của production-ready.** Bật full chỉ khi thật sự cần phần lớn bundle và có budget vận hành/backup.

### Migration

**[Fact]** Standard upgrade được mô tả bằng pin `WEKNORA_VERSION`, `docker compose pull`, `docker compose up -d`; app có automatic database migrations. Repo có migration tree riêng cho PostgreSQL và SQLite. [S1], [S6]

**[Inference]** Tài liệu upstream tại commit không đưa ra một quy trình được bảo đảm để in-place chuyển toàn bộ Lite SQLite sang Standard PostgreSQL. “Chuyển Lite → Core” an toàn nhất nên được coi là export/re-ingest source, không phải copy database.

**[Recommendation]** Vì Git giữ source-of-truth, migration là dựng Standard mới, cấu hình model, chạy manifest sync/re-ingest, so sánh count + regression queries, rồi chuyển endpoint. Export những dữ liệu không tái tạo được (manual Wiki edits, sessions, memory) riêng; không giả định chúng tự migrate.

## 10. WeKnora và my-wiki: thay thế hay kết hợp?

| Nhu cầu | my-wiki/VitePress | WeKnora |
|---|---|---|
| Đọc Markdown có cấu trúc, URL ổn định | Mạnh | Có, nhưng thiên KB/Wiki UI |
| Git history, PR/diff, portability | Native | Không phải workflow chính |
| Full-text/semantic/hybrid search | Hạn chế hơn | Mạnh |
| Q&A có citation | Không phải chức năng lõi | Native |
| Auto-Wiki/graph | Không | Có, derived |
| Agent/MCP | Không phải lõi | Native client + server |
| Static publication | Mạnh | UI cần backend/state |
| Tái tạo từ source | Trực tiếp | Cần ingest/index/model config |

**[Inference]** Hai hệ thống bổ sung nhau tốt hơn thay thế nhau: my-wiki là authoring/publication surface; WeKnora là computational knowledge surface.

**[Recommendation] Source-of-truth contract:**

- Canonical: `D:/4.Code/my-wiki/src/nghien-cuu/**` và các Markdown được chọn, versioned bằng Git.
- Import một chiều: Git/Markdown → WeKnora knowledge entries.
- Manifest lưu `path`, `git_blob_sha` hoặc content hash, `knowledge_base_id`, `knowledge_id`, last sync status.
- Update source thì update/reparse knowledge; delete source cần tombstone/review trước khi delete knowledge.
- Không tự động xuất Auto-Wiki/chunk edits ngược vào my-wiki.
- Nếu một Wiki page đáng giữ, human review rồi viết lại thành canonical Markdown với source citations.

## 11. Kiến trúc đề xuất cho máy cá nhân

Phần này là input trực tiếp cho C4 Level 1–3 ở T003.

### 11.1 System Context — Level 1

**[Recommendation] Hệ thống đích:** “Personal Knowledge System” gồm hai bề mặt phối hợp.

- **Human / Chủ sở hữu:** viết và review Markdown; đọc my-wiki; hỏi/search bằng WeKnora.
- **External AI Agent:** dùng MCP read/search/ask với scoped API key.
- **my-wiki:** authoritative Markdown + Git + VitePress viewer.
- **WeKnora:** ingest/index/RAG/Agent/derived Wiki.
- **Model Provider:** Ollama local hoặc remote OpenAI-compatible API.
- **Optional external MCP services:** tool providers mà WeKnora Agent consume.

Quan hệ chính: Human → my-wiki (author/read); Human → WeKnora UI (search/ask/review derived); sync → WeKnora API; external Agent → WeKnora MCP; WeKnora → model provider; WeKnora Agent → approved MCP services.

### 11.2 Container — Level 2

**[Recommendation] Baseline lâu dài: Standard Compose core**, gồm:

1. `my-wiki Git working tree` — canonical files; không mount write vào WeKnora/sandbox.
2. `VitePress viewer` — render canonical docs.
3. `Sync adapter` — read-only scan Markdown, compute hash, call REST/MCP/manual knowledge API, maintain manifest; chạy theo lệnh hoặc schedule.
4. `WeKnora frontend` — human UI.
5. `WeKnora app` — API, RAG, Agent, worker.
6. `docreader` — parser service.
7. `PostgreSQL/ParadeDB` — metadata, chunks, BM25, pgvector.
8. `Redis` — queues and stream state.
9. `local file volume` — uploaded/original/derived assets.
10. `MCP Server` — optional, loopback/private, scoped WeKnora API key.
11. `Ollama/model API` — embedding/chat/rerank.
12. `backup target` — Git remote + encrypted backup of Postgres/files/config/secrets metadata.

**[Recommendation] Không bật mặc định:** Neo4j, MinIO, Qdrant, SearXNG, Langfuse, Sandbox. Postgres core đã có BM25 + pgvector; local storage đủ cho một máy; từng optional container phải có use case và backup plan.

### 11.3 Component — Level 3 (bên trong integration boundary)

T003 nên zoom vào `Sync adapter + WeKnora knowledge boundary`:

- `Source scanner`: chọn glob, bỏ `.vitepress`, generated assets và private paths.
- `Hasher/manifest`: content hash + Git commit/blob identity.
- `Mapper`: path/frontmatter → KB, title, tags, metadata (`source_path`, `source_commit`, `authoritative=true`).
- `Importer`: create/update/reparse qua API; idempotency dựa trên manifest/hash.
- `Status reconciler`: poll parse status; log count/failure; không coi upload 202 là complete.
- `Deletion gate`: tombstone, human approval trước delete.
- `Evidence linker`: giữ source path/commit trong metadata để citation quay về canonical doc.
- `Derived knowledge boundary`: chunks/index/Wiki/memory tách khỏi canonical store.
- `MCP gateway`: read-oriented tools cho external agents; write tools off/approval.

### 11.4 Trust boundaries cần thể hiện

- **Authoritative boundary:** Git/my-wiki.
- **Derived/AI boundary:** WeKnora chunks, embeddings, Auto-Wiki, memory.
- **Execution boundary:** Skills/Sandbox (nếu bật), không có write access tới Git.
- **External network boundary:** remote models, web search, external MCP.
- **Credential boundary:** WeKnora secrets/API keys/MCP OAuth, không commit vào Git.

### 11.5 Luồng chính

1. Human sửa Markdown → review/commit Git.
2. Sync adapter đọc commit, upsert content + provenance vào WeKnora.
3. WeKnora parse/chunk/index; optional Wiki derives pages.
4. Human hỏi qua UI hoặc Agent hỏi qua MCP.
5. RAG trả answer + source references.
6. Human sửa sai ở Markdown canonical, không sửa lâu dài ở derived layer.
7. Re-sync/reparse; kiểm tra regression và affected Wiki pages.

## Kiến trúc C4 bằng Archify

Archify không có C4 native; ba sơ đồ dưới đây dùng diagram type `architecture`, boundary, typed node và relationship để biểu diễn quy ước C4. JSON nguồn có thể regenerate được lưu cùng project handoff trong `40_RESULTS/archify-c4/`.

### C4 Level 1 — System Context

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/c4-l1-system-context.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

### C4 Level 2 — Container

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/c4-l2-container.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

### C4 Level 3 — Component

Level 3 zoom vào Sync Adapter và knowledge integration boundary; đây là mức component có giá trị vận hành. Không dựng Level 4 vì task không triển khai code Sync Adapter và sơ đồ code sẽ tạo độ chính xác giả.

<iframe src="/nghien-cuu/kien-truc/weknora-personal-knowledge-platform/assets/c4-l3-component.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

## 12. Vận hành, backup và rủi ro

### 12.1 Checklist vận hành

**[Recommendation]**

- Pin release/tag và image versions; đọc breaking changes trước upgrade.
- Backup trước migration; thử restore định kỳ.
- Lưu model IDs, embedding dimensions và KB process config như cấu hình có version.
- Theo dõi failed/stuck ingestion; regression-test sau đổi parser/chunker/embedding/reranker.
- Giữ service trên loopback/private LAN; dùng TLS nếu qua mạng.
- Export memory/manual Wiki edits nếu chúng có giá trị; chúng không hoàn toàn tái tạo từ Git.
- Ghi rõ generated timestamp/source commit trên nội dung được publish từ derived layer.

### 12.2 Risk register

| Rủi ro | Bằng chứng/nguồn | Giảm thiểu đề xuất |
|---|---|---|
| Source drift do sửa chunk/Wiki | UI có revisions và edit [S1], [S11] | Git authoritative, one-way sync |
| Hallucination/stale Wiki | Wiki do LLM map-reduce, được boost [S11], [S12] | label derived, source refs, review |
| Lock-in dữ liệu/index | metadata/chunks/index trong DB + model-specific embeddings | giữ Markdown/Git; re-ingest manifest |
| Embedding migration | multi-KB search yêu cầu compatible embedding space [S12] | version model/dimension; rebuild index |
| Lite durability/concurrency | memory queue, SQLite [S5], [S6] | backup file; chuyển core khi scale |
| Full profile bloat | bật nhiều optional services [S7], [S8] | selective profiles |
| Sandbox host compromise | docker.sock tương đương host control [S3], [S15] | off by default; isolation/limits |
| MCP side effects/injection | external tools + approval/untrusted prefix [S16] | scope, approval, private network |
| Secret/data exfiltration | models/web/MCP là outbound boundary | local models hoặc allowlist; no secrets in docs |
| Documentation drift | README nói 29 tools, feature docs nói 31 | verify code/version when integrating |

## 13. Kết luận

**[Inference]** WeKnora là ứng viên mạnh để thêm semantic retrieval, cited Q&A, ReAct Agent, Auto-Wiki và MCP vào kho tri thức cá nhân. Giá trị lớn nhất không phải “thay trang web đọc Markdown”, mà là biến corpus thành một dịch vụ truy hồi và reasoning cho cả Human + Agent.

**[Recommendation]** Kiến trúc bền vững là **Git/Markdown canonical + WeKnora derived serving layer**. Bắt đầu Lite để xác nhận value; dùng Standard Compose core khi thành hệ thống dùng lâu dài; bật từng optional profile theo nhu cầu. Auto-Wiki, memory và Agent output luôn cần provenance và review.

## Nguồn chính thức

- **[S1]** [`README.md`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/README.md#L50-L85), kiến trúc/features/deployment tại [L115–179](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/README.md#L115-L179), cài đặt/profiles tại [L231–290](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/README.md#L231-L290), security/license tại [L369–387](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/README.md#L369-L387).
- **[S2]** [`LICENSE` L1–19](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/LICENSE#L1-L19).
- **[S3]** [`CHANGELOG.md` v0.8.0 L1–73](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/CHANGELOG.md#L1-L73).
- **[S4]** [`VERSION`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/VERSION), [`helm/Chart.yaml` L1–9](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/helm/Chart.yaml#L1-L9).
- **[S5]** [`docs/LITE.md`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/docs/LITE.md#L1-L15).
- **[S6]** [`website-docs/02-architecture/01-overview.md` L1–43](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/01-overview.md#L1-L43), topology/protocol tại [L73–136](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/01-overview.md#L73-L136).
- **[S7]** [`website-docs/01-getting-started/02-installation.md` L1–105](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/01-getting-started/02-installation.md#L1-L105), Lite tại [L213–258](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/01-getting-started/02-installation.md#L213-L258).
- **[S8]** [`docker-compose.yml`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/docker-compose.yml), đặc biệt core services và các `profiles: full`.
- **[S9]** [`.env.lite.example` L17–39](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/.env.lite.example#L17-L39).
- **[S10]** [`website-docs/02-architecture/03-document-pipeline.md` L1–57](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/03-document-pipeline.md#L1-L57), processing tại [L254–364](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/03-document-pipeline.md#L254-L364), state/recovery tại [L388–458](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/03-document-pipeline.md#L388-L458).
- **[S11]** [`website-docs/03-features/14-wiki.md` L1–40](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/14-wiki.md#L1-L40), model/API tại [L96–190](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/14-wiki.md#L96-L190), generation tại [L192–269](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/14-wiki.md#L192-L269).
- **[S12]** [`website-docs/02-architecture/04-rag-pipeline.md` L1–52](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/04-rag-pipeline.md#L1-L52), retrieval/rerank tại [L187–246](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/04-rag-pipeline.md#L187-L246), citation/fan-out tại [L441–474](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/02-architecture/04-rag-pipeline.md#L441-L474).
- **[S13]** [`website-docs/03-features/07-agent.md`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/07-agent.md#L1-L51).
- **[S14]** [`website-docs/03-features/23-memory.md`](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/23-memory.md#L1-L67).
- **[S15]** [`website-docs/03-features/22-skills-sandbox.md` L1–79](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/22-skills-sandbox.md#L1-L79).
- **[S16]** [`website-docs/03-features/08-mcp.md` L1–42](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/08-mcp.md#L1-L42), client security tại [L119–144](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/08-mcp.md#L119-L144), approval tại [L292–341](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/08-mcp.md#L292-L341), server/tools tại [L355–445](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/website-docs/03-features/08-mcp.md#L355-L445).
- **[S17]** [`docs/RBAC说明.md` L1–59](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/docs/RBAC%E8%AF%B4%E6%98%8E.md#L1-L59), config/audit tại [L107–157](https://github.com/Tencent/WeKnora/blob/6f98ff80c3185679cc16f834faf42fc662770e68/docs/RBAC%E8%AF%B4%E6%98%8E.md#L107-L157).

## Giới hạn kiểm chứng

- Không cài đặt hoặc chạy WeKnora; kiến trúc/runtime được kiểm chứng bằng source và tài liệu chính thức tại commit cố định.
- Không benchmark chất lượng, latency, RAM hoặc corpus lớn.
- Không xác minh UI bằng thao tác browser vì browser provider không khả dụng trong môi trường task.
- Git clone là shallow clone của repo chính thức; metadata release/tag từ GitHub API không được truy vấn. Claim release dựa trên `VERSION`, README, Helm và CHANGELOG trong repo.
- Tài liệu upstream có drift nhỏ (29 so với 31 MCP tools); triển khai thực tế phải kiểm tra version/code đang chạy.
