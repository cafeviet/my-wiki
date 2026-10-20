# Handoff Đa tác tử (GPT Web - Drive - Kanban)

> **Mục tiêu:** biến kết quả nghiên cứu và task do GPT Web tạo thành công việc có thể được local Agent nhận, thực thi, theo dõi và bàn giao lại; bắt đầu với Hermes, sau đó mở rộng qua Codex và Antigravity mà không thay đổi contract đầu vào.

## 1. Tóm tắt giải pháp

Kiến trúc được chọn tách rõ ba nguồn sự thật:

- **Google Drive** là lớp vận chuyển (transport) cho task bất biến, research input và artifacts.
- **Hermes Kanban** là nguồn trạng thái thực thi: queue, dependency, atomic claim, retry, heartbeat, review và lịch sử run.
- **Target Git repository** là nguồn sự thật cho code, test, diff và bằng chứng kỹ thuật.

Không dùng Google Drive như transactional task database. GPT Web không sửa `CLAIMED`, `RUNNING` hoặc retry state trong Markdown; các trạng thái đó thuộc Hermes Kanban.

<iframe src="/nghien-cuu/agents/gptweb-google-drive-hermes-kanban/assets/kien-truc-gptweb-drive-kanban.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

## 1b. Kiến trúc theo mô hình C4

Để mô tả hệ thống một cách chặt chẽ, ta dùng mô hình **C4**: đi từ **System Context** (Level 1) — hệ thống nằm giữa những actor và hệ thống bên ngoài nào — rồi zoom vào **Container** (Level 2) — các khối triển khai được (application, data store, executor) và ranh giới giữa chúng. Hai tầng này đủ để nắm ranh giới control plane và điểm mở rộng mà không sa vào chi tiết component từng file.

### C4 Level 1 — System Context

Ở tầng này, AI Research Handoff là một hệ thống duy nhất đứng giữa người dùng GPT Web (tạo task) và các nguồn sự thật bên ngoài: Google Drive làm transport, Git repository giữ code/evidence, và các model provider truy cập qua 9Router. Sơ đồ làm rõ ai gửi task vào và kết quả đi ra đâu.

<iframe src="/nghien-cuu/agents/gptweb-google-drive-hermes-kanban/assets/c4-context.html" width="100%" height="600" style="border:none;border-radius:0.75rem;"></iframe>

### C4 Level 2 — Container

Tầng Container tách rõ ba nhóm ranh giới: **trong hệ thống nhưng ngoài Hermes** (Handoff Importer / Reconciler chạy như tiến trình Python độc lập, Google Drive transport), **trong Hermes** (Hermes Kanban SQLite giữ execution state, Hermes Gateway dispatch và spawn worker theo profile), và **ngoài Hermes** (9Router gateway model, target Git repository, cùng các executor tương lai Codex/Antigravity nối qua Executor Adapter). Ranh giới này cho thấy Hermes Kanban là control plane duy nhất, còn mọi executor chỉ là engine thực thi.

<iframe src="/nghien-cuu/agents/gptweb-google-drive-hermes-kanban/assets/c4-container.html" width="100%" height="640" style="border:none;border-radius:0.75rem;"></iframe>

### Các use case quan trọng

1. **Tiếp nhận task từ GPT Web qua Drive** — Handoff Importer đọc `01_INBOX`, validate fail-closed theo schema và bảo đảm idempotency (`idempotency_key`) để không import trùng.
2. **Dispatch và thực thi bởi Hermes worker** — Hermes Gateway atomic claim card, spawn worker theo profile, duy trì heartbeat, áp retry và circuit breaker khi worker fail hoặc stale.
3. **Reconcile kết quả về Drive `03_DONE`** — khi Kanban báo `done`, task envelope, receipt và result được xuất trở lại Drive để GPT Web và người dùng thấy kết quả.
4. **Human approval gate cho task R3** — task rủi ro cao (`R3`) được tạo ở trạng thái `blocked` với `requires_user_approval`, chỉ chạy sau khi có người duyệt.
5. **Mở rộng executor sang Codex/Antigravity** — thêm executor mới qua cùng Executor Adapter contract `enqueue(validated_task, source_path)`, không tạo thêm task database thứ hai.

## 2. Vì sao bỏ Dispatcher PowerShell cũ?

Prototype ban đầu quét task `READY`, sửa trực tiếp file trên Drive rồi gọi Hermes. Review thực tế cho thấy cách đó không phù hợp:

1. CLI được gọi bằng `hermes ask --file`, nhưng Hermes hiện tại không có subcommand `ask`.
2. Google Drive không có transaction hoặc compare-and-swap giữa nhiều writer.
3. Lock file tự tạo không đảm bảo atomic trên nhiều máy.
4. Task từ Drive được ghép thẳng thành prompt, nhưng không có schema, allowlist hay risk gate cơ học.
5. Scheduler dự kiến chạy quyền cao làm tăng blast radius.
6. Không có heartbeat, timeout, retry, stale-claim recovery hoặc validation sau khi Agent hoàn thành.

Hermes Kanban đã cung cấp phần lớn các capability này ở đúng lớp orchestration, nên tự xây lại chúng trong PowerShell tạo duplicate control plane.

## 3. Luồng end-to-end

```text
GPT Web
  → tạo task envelope JSON bất biến
  → Google Drive / 01_INBOX
  → Handoff Importer validate
  → Hermes Kanban tạo card bằng idempotency_key
  → Hermes Gateway atomically claim và spawn profile
  → Worker thực thi trong scratch / dir / worktree
  → Worker complete, review hoặc block
  → Result Exporter đưa receipt + artifacts về Drive
```

### Trạng thái được sở hữu ở đâu?

| Trạng thái | Chủ sở hữu |
|---|---|
| Task envelope do GPT tạo | Google Drive `01_INBOX` |
| Đã import | Receipt trong `02_ACTIVE` |
| Ready/running/blocked/review/done | Hermes Kanban SQLite |
| Code, test, commit, diff | Target Git repository |
| Giao phẩm cuối | Google Drive `03_DONE` hoặc project output |

## 4. Task envelope v1

Task dùng JSON để tránh lỗi Markdown escape và cho phép validate fail-closed:

```json
{
  "schema_version": 1,
  "project_id": "RESEARCH-001",
  "task_id": "T001",
  "title": "Nghiên cứu một chủ đề",
  "body": "Tạo bài nghiên cứu có dẫn nguồn và bằng chứng.",
  "executor": "hermes",
  "assignee_profile": "researcher",
  "workspace": "scratch",
  "priority": 50,
  "risk_level": "R1",
  "requires_user_approval": false,
  "max_runtime": "30m",
  "max_retries": 2
}
```

### Invariant bắt buộc

- `project_id`, `task_id`, `assignee_profile` chỉ dùng ký tự an toàn; không chấp nhận path traversal.
- `idempotency_key = project_id:task_id:v<schema_version>` chống import trùng.
- Workspace `dir:` bắt buộc có allowlist cục bộ và phải nằm trong allowlist đó.
- `assignee_profile` phải thuộc allowlist `default/researcher/coder/reviewer`; tên profile lạ bị từ chối.
- Task `R3` bắt buộc `requires_user_approval: true` và được tạo ở trạng thái `blocked`.
- Executor chưa có adapter sẽ bị từ chối; không fallback im lặng sang runtime khác.
- File task là bất biến sau khi vào `01_INBOX`.

## 5. Hermes Kanban làm gì?

Hermes Kanban là durable work queue cho nhiều profile, không phải một Agent đơn lẻ. Nó chịu trách nhiệm:

- lưu task trong SQLite;
- atomic claim để hai worker không cùng nhận một task;
- dependency giữa parent/child tasks;
- chọn profile, model/provider và workspace;
- spawn worker thông qua Hermes Gateway;
- heartbeat và reclaim stale worker;
- giới hạn runtime, retry và failure circuit breaker;
- comments, event stream, logs và lịch sử các run;
- workflow `ready → running → review/done`, hoặc `blocked` khi cần input.

Trên máy triển khai, board `ai-research-handoff` được tạo riêng để task không va chạm board khác.

## 6. Các Hermes profile ban đầu

| Profile | Vai trò |
|---|---|
| `researcher` | Nghiên cứu, dẫn nguồn, phân biệt Fact / Inference / Recommendation |
| `coder` | Thực thi code trong workspace phù hợp và chạy test |
| `reviewer` | Review độc lập acceptance criteria, security và evidence |
| `default` | Kiểm thử tích hợp và fallback có chủ đích trong giai đoạn đầu |

Hermes Gateway giữ dispatcher loop; profile không cần có Gateway riêng để được spawn làm worker.

### Model / provider cho worker

Toàn bộ traffic của môi trường này đi qua **9Router** local (`http://127.0.0.1:20127/v1`), không gọi thẳng API nhà cung cấp. Vì vậy phải dùng đúng model-id mà 9Router expose, không phải tên model gốc.

- Sai: đặt `deepseek/deepseek-v3.2` + provider `deepseek` → 9Router định tuyến nhầm sang upstream không có credential (`404 openrouter`).
- Đúng: dùng model-id của 9Router qua provider `custom`.

```powershell
# xem model DeepSeek 9Router đang expose
curl -s http://127.0.0.1:20127/v1/models | findstr deepseek

# đặt cho một profile (ví dụ default)
hermes --profile default config set model.default ds/deepseek-chat
hermes --profile default config set model.provider custom
```

| Nhu cầu | Model 9Router |
|---|---|
| Chat mặc định | `ds/deepseek-chat` |
| Reasoning | `ds/deepseek-reasoner` hoặc `kr/deepseek-3.2-thinking` |
| Bản mạnh hơn | `ds/deepseek-v4-pro` |

Bài học: khi có gateway ở giữa, nguồn sự thật về model-id là `GET /v1/models` của gateway, không phải catalog nhà cung cấp.

## 7. Handoff Importer đã triển khai

Implementation nằm ngoài Drive tại:

```text
D:\4.Code\google-driver\handoff-kanban
```

Lý do: code điều phối không nên được Google Drive tự động đồng bộ và thay đổi từ xa.

Cấu trúc:

```text
handoff-kanban/
├── handoff_kanban/
│   ├── task_schema.py         # validate fail-closed + idempotency_key
│   ├── importer.py            # 01_INBOX → Kanban, ghi receipt vào 02_ACTIVE
│   ├── reconciler.py          # Kanban done → xuất result/receipt/envelope sang 03_DONE
│   ├── cli.py                 # điểm vào, hỗ trợ --log-file cho chạy ẩn
│   └── adapters/
│       ├── __init__.py        # ExecutorAdapter contract
│       └── hermes.py          # adapter Hermes Kanban
├── examples/TASK_ENVELOPE.example.json
├── tests/                     # 17 unit test
├── docs/
│   ├── gptweb-drive-kanban.architecture.json
│   └── EXECUTOR_ADAPTER_CONTRACT.md
├── register-importer-task.ps1     # đăng ký scheduler ẩn (pythonw)
└── unregister-importer-task.ps1
```

Cách chạy một import cycle:

```powershell
cd D:\4.Code\google-driver\handoff-kanban
python -m handoff_kanban.cli `
  --handoff-root "D:\4.Code\google-driver\google_drive\AI Research Handoff" `
  --board ai-research-handoff `
  --allowed-root "D:\4.Code" `
  --once
```

Sau khi import thành công:

- task chuyển từ `01_INBOX` sang `02_ACTIVE`;
- receipt ghi Kanban task ID;
- Kanban card có assignee, workspace, timeout, retry và idempotency key;
- mỗi cycle cũng reconcile: khi Kanban báo `done`, task envelope + receipt + result được xuất sang `03_DONE`.

## 7b. Chạy ngầm mỗi phút không popup

Importer/reconciler chạy tự động qua Windows Task Scheduler. Vấn đề với launcher `.bat`: Windows luôn cấp console cho batch script nên cửa sổ nháy mỗi phút. Giải pháp là chạy **`pythonw.exe`** trực tiếp — biến thể không cấp phát console, nên không có cửa sổ nào xuất hiện.

```powershell
cd D:\4.Code\google-driver\handoff-kanban

# đăng ký / cập nhật job (mặc định mỗi 1 phút, quyền Limited)
.\register-importer-task.ps1
.\register-importer-task.ps1 -IntervalMinutes 5   # đổi tần suất

# gỡ job
.\unregister-importer-task.ps1
```

Vì `pythonw` không có stdout, CLI nhận `--log-file` và ghi **một dòng JSON mỗi lần chạy** để vẫn kiểm tra được:

```json
{"ts": "2026-09-14T03:36:19+00:00", "ok": true, "imported": [], "reconciled": []}
```

Log nằm ở `handoff-kanban/logs/importer.jsonl`. Nhánh lỗi cũng được ghi (`"ok": false`, kèm `error`) và trả exit code khác 0 cho scheduler.

> Task chạy dưới user hiện tại với `RunLevel=Limited` (không elevated), `ExecutionTimeLimit` 5 phút, `MultipleInstances=IgnoreNew` để hai cycle không chồng nhau.

## 8. Mở rộng sang Codex

Codex là một **executor nằm ngoài Hermes**: nó nối vào hệ thống qua đúng Executor Adapter contract `enqueue(validated_task, source_path)`, không trở thành control plane. Hermes Kanban vẫn là control plane duy nhất giữ execution state, retry và review; Codex chỉ là engine thực thi được chọn theo task.

Codex CLI đã có trên máy, nhưng không nên để importer gọi Codex trực tiếp. Ta giữ một interface adapter thống nhất:

```text
enqueue(validated_task, source_path) → external_receipt
```

Hai lựa chọn cho Phase 2:

1. **Hermes làm orchestrator, Codex làm executor:** Kanban task được giao cho một Hermes profile chuyên gọi Codex trong target worktree. Kanban vẫn giữ state, retry và review.
2. **Codex adapter độc lập:** importer tạo execution record riêng rồi runner quản lý subprocess Codex, timeout, sandbox, logs và completion receipt.

Khuyến nghị bắt đầu với lựa chọn 1 vì chỉ có một control plane. Codex là worker engine, không trở thành task database thứ hai.

## 9. Mở rộng sang Antigravity

Antigravity cũng là một **executor nằm ngoài Hermes**, dự kiến nối qua cùng Executor Adapter contract `enqueue(validated_task, source_path)` như Codex. Dù thêm executor này, Hermes Kanban vẫn là control plane duy nhất; Antigravity chỉ là engine thực thi, không phải task database thứ hai.

Tên “Antigravity” chưa đủ để xác định API/CLI contract chính thức trong môi trường hiện tại; máy cũng chưa có executable `antigravity`. Vì vậy implementation hiện chỉ chừa executor contract, không giả định lệnh hoặc quyền.

Để thêm adapter cần xác định:

- sản phẩm/runtime chính xác;
- cơ chế nhận task: CLI, API, MCP hay queue;
- authentication;
- workspace và sandbox;
- cách phát heartbeat, cancel và timeout;
- result schema và evidence boundary.

Sau khi contract được xác nhận, adapter mới implement cùng test contract như Hermes.

## 10. Risk model

| Mức | Ví dụ | Hành vi |
|---|---|---|
| `R0` | đọc/tóm tắt local | enqueue tự động |
| `R1` | research, tạo tài liệu trong output cho phép | enqueue tự động, bounded runtime |
| `R2` | sửa code trong Git worktree | dùng `coder`, review bắt buộc |
| `R3` | credential, production, destructive/system change | tạo `blocked`, chờ user approval |

Natural-language prompt không phải security boundary. Validation, allowlist, workspace isolation và approval state phải được code thực thi.

## 11. Bằng chứng triển khai ban đầu

- Hermes Kanban board: `ai-research-handoff`.
- Hermes profiles: `researcher`, `coder`, `reviewer`; cả ba đã được chuyển sang `cx/gpt-5.6-sol` qua provider `custom` và health-check thành công.
- Unit tests importer/schema/adapter/reconciler/cli: **17/17 pass**.
- Hardening sau review độc lập: importer validate envelope trước rồi mới tin receipt (chỉ khi `idempotency_key` khớp) — chặn receipt giả/lệch; `dir:` workspace bắt buộc allowlist; `assignee_profile` phải thuộc allowlist.
- Archify JSON IR: validate `showcase` **9/9 checks**, không error/warning.
- E2E import: task Drive `E2E-HERMES:T001:v1` được tạo thành Kanban card `t_3eedacc4`.
- E2E dispatch thật: Kanban claim, spawn worker và heartbeat. Run đầu fail do token Kiro cũ; card được circuit breaker block đúng thiết kế. Sau khi pin model đang hoạt động, run thứ hai hoàn thành và lưu worker session ID.
- E2E reconcile: result, receipt và task envelope được xuất sang `03_DONE`; kết quả ghi rõ `PASS` và không có side effect.
- E2E profile chuyên biệt: task `E2E-RESEARCHER:T001` được scheduler import, Gateway tự claim/spawn profile `researcher`, worker heartbeat + complete, rồi scheduler xuất đủ task/receipt/result vào `03_DONE`.
- Scheduler Unicode regression: phát hiện console CP1252 lỗi khi log tiếng Việt; đã thêm test và chuyển output CLI sang ASCII-safe JSON escape.

## 12. Phạm vi chưa hoàn thành

- Importer/reconciler chạy mỗi phút bằng Windows Task Scheduler dưới quyền `Limited`, **ẩn hoàn toàn qua `pythonw.exe`** (không popup), log ra `logs/importer.jsonl`; chưa có dashboard riêng ngoài Kanban/log.
- Codex chưa được nối như executor.
- Antigravity chưa có contract đã xác minh.
- Chưa triển khai task signature/source allowlist ngoài path/schema validation.
- Hermes Doctor cảnh báo Python SQLite của Hermes có WAL-reset bug; board mới dùng rollback journal, nhưng vẫn nên cập nhật Hermes trước khi mở rộng production.

> Hermes chủ động chặn Kanban mutation trong `delegate_task` child context. Importer phải chạy từ tiến trình/scheduler bình thường, không chạy như subagent con.

## 13. Lộ trình

### Phase 1 — Hermes worker

- Drive task envelope → importer → Kanban.
- Profiles researcher/coder/reviewer.
- E2E task an toàn và result verification.

### Phase 2 — Production hardening

- Importer scheduler dưới user thường.
- Receipt reconciliation và exporter.
- Task signature/source allowlist.
- R2 review graph và target repository registration.

### Phase 3 — Codex executor

- Hermes orchestrator → Codex worker adapter.
- Git worktree, timeout, log capture, review task.

### Phase 4 — Antigravity executor

- Chốt runtime contract.
- Implement adapter và contract tests.
- Giữ Kanban là control plane duy nhất.

## 14. Kết luận

> **GPT Web tạo ý định; Google Drive vận chuyển; Importer kiểm tra; Hermes Kanban điều phối; Agent thực thi; repository và evidence chứng minh kết quả.**

Thiết kế adapter cho phép đổi Agent runtime mà không phá task envelope. Điểm quan trọng là giữ duy nhất một control plane: Hermes Kanban quản lý execution state; Codex và Antigravity chỉ là các executor được chọn theo task.