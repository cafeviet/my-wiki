# Vận hành & Giám sát Handoff Tác tử

> **Mục tiêu:** một giải pháp giám sát (observability) cho hệ handoff nhiều Agent chạy nền — biết task đang ở đâu, worker đang làm gì, và khi lỗi thì chẩn đoán tận gốc thay vì retry mù. Bài này bổ sung cho [kiến trúc handoff](../gptweb-google-drive-hermes-kanban/): ở đó là *thiết kế*, ở đây là *vận hành*.

## 1. Tóm tắt giải pháp

Hệ handoff chạy hoàn toàn nền: importer poll mỗi phút, Hermes Gateway tự claim và spawn worker, worker gọi model qua 9Router. Không có UI trung tâm, nên bài toán giám sát là **gom ba lớp quan sát rời rạc thành một quy trình chẩn đoán**:

- **Pipeline Google Drive** — task đang nằm ở `01_INBOX`, `02_ACTIVE` hay `03_DONE`.
- **Hermes Kanban board** — trạng thái task, các run, event và lý do block.
- **Log** — `importer.jsonl` (lỗi Drive→Kanban) và transcript worker (lỗi model/API/spawn).

Nguyên tắc cốt lõi rút ra từ vận hành thực tế: **board chỉ cho biết task *có* lỗi; log worker mới cho biết *vì sao*.** Event trên board chỉ ghi `crashed / pid not alive` — nguyên nhân thật (404, 503, WinError 4551) nằm trong `kanban log <task>`.

<iframe src="/nghien-cuu/agents/van-hanh-giam-sat-hermes-handoff/assets/01-topology.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

## 2. Ba bề mặt quan sát

Mỗi lớp trả lời một câu hỏi khác nhau; muốn giám sát đúng phải biết hỏi đúng chỗ.

| Bề mặt | Trả lời câu hỏi | Cách xem |
|---|---|---|
| Pipeline Drive | Task đến chưa? Xong chưa? | Nhìn `01_INBOX` / `02_ACTIVE` / `03_DONE` |
| Kanban board | Task ở trạng thái nào? Retry mấy lần? | `kanban list` / `show` / `stats` |
| Log importer | Việc import/reconcile có lỗi không? | `tail -f logs/importer.jsonl` |
| Log worker | Agent làm gì? Vì sao chết? | `kanban log <task>` |
| DevWebUI | Tiến trình nền còn sống không? | `http://127.0.0.1:4000` |

> Lưu ý môi trường: trên máy triển khai, lệnh `hermes` (shim `.exe`) bị Smart App Control chặn (mục 5). Mọi lệnh CLI trong bài dùng dạng module tương đương: `python -m hermes_cli.main kanban ...`.

### Lệnh quan sát board

```powershell
# Danh sách task + trạng thái
python -m hermes_cli.main kanban --board ai-research-handoff list

# Thống kê board
python -m hermes_cli.main kanban --board ai-research-handoff stats

# Theo dõi realtime
python -m hermes_cli.main kanban --board ai-research-handoff watch

# Chi tiết 1 task: events, runs, lý do block
python -m hermes_cli.main kanban --board ai-research-handoff show <task_id>

# QUAN TRỌNG: transcript worker — nguồn sự thật khi debug
python -m hermes_cli.main kanban --board ai-research-handoff log <task_id>
```

## 3. Vòng chẩn đoán khi agent lỗi

Khi một task bị `blocked` hoặc `crashed`, quy trình chẩn đoán đi từ *quan sát* → *phân loại* → *xử lý gốc* → *chạy lại*. Điểm mấu chốt: `unblock` chỉ nên chạy **sau khi** đã sửa nguyên nhân gốc, vì `unblock` tự reset bộ đếm `consecutive_failures` về 0 — nếu unblock khi chưa sửa, dispatcher sẽ claim lại rồi crash y hệt và block ngay.

<iframe src="/nghien-cuu/agents/van-hanh-giam-sat-hermes-handoff/assets/02-loop.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

Các bước cụ thể:

1. `kanban list` — thấy task `blocked`.
2. `kanban show <task>` — đọc `Events` và `Runs`, xác định outcome (`spawn_failed`, `crashed`, `gave_up`).
3. `kanban log <task>` — đọc transcript worker, tìm lỗi thật (HTTP code, WinError, message model).
4. Phân loại lỗi (mục 4) và sửa gốc.
5. `kanban unblock <task> --reason "..."` — đưa task về `ready` để dispatcher chạy lại.

Nếu task **không vào board**, lỗi nằm ở tầng import: xem `logs/importer.jsonl`.

## 4. Bảng phân loại lỗi thực chiến

Bốn lớp lỗi gặp trong vận hành, mỗi lớp có dấu hiệu và cách sửa riêng. Đây là phần giá trị nhất của việc giám sát: nhận diện đúng lớp lỗi để sửa gốc thay vì retry.

| Dấu hiệu | Lớp | Nguyên nhân gốc | Sửa |
|---|---|---|---|
| `HTTP 503: response_format type is unavailable` | Model API | DeepSeek từ chối `json_schema` | 9Router hạ cấp `json_schema → json_object` cho DeepSeek |
| `HTTP 404: No active credentials for provider: codex` | Cấu hình profile | Model dùng prefix `cx/` (codex, không có credential) | Đổi sang model có credential, ví dụ `kr/gpt-5.6-sol` |
| `WinError 4551: Application Control policy blocked` | Hệ điều hành | Smart App Control chặn `hermes.exe` chưa ký | Gọi Hermes qua module form `python -m hermes_cli.main` |
| `workspace must be scratch, worktree, or dir:...` | Envelope | Field `workspace` sai định dạng | Importer resolve tên repo → `dir:<absolute-path>` trong allowlist |

Nguyên tắc: một lỗi crash lặp lại **hai lần cùng kiểu** là tín hiệu dừng retry và tìm nguyên nhân gốc, không phải tăng `max-retries`.

## 5. Bài học môi trường: Smart App Control chặn shim

Đây là lớp lỗi ít gặp nhất nhưng khó chẩn đoán nhất, vì nó không phải bug phần mềm mà là chính sách bảo mật của Windows.

**Triệu chứng:** worker `spawn_failed` với `[WinError 4551] An Application Control policy has blocked this file`, hoặc gõ `hermes` trong terminal báo `Permission denied`.

**Nguyên nhân:** Windows Smart App Control (SAC) ở chế độ Enforce từ chối chạy **mọi** file `.exe` chưa ký. Các console-script shim trong venv (`hermes.exe`, `hermes-agent.exe`) đều chưa ký nên bị chặn. Ngược lại, `python.exe` đã được ký hợp lệ nên SAC cho chạy.

**Điểm quan trọng về whitelist:** SAC **không** hỗ trợ whitelist từng file — đây là thiết kế cố ý của Microsoft, khác Windows Defender (có Exclusions) hay WDAC (soạn được policy cho phép). SAC chỉ dựa trên cloud-reputation và chữ ký số. Tắt SAC là thao tác một chiều: bật lại phải cài lại Windows.

**Giải pháp đúng — dùng module form:** vì `python.exe` được phép chạy, mọi lời gọi Hermes đi qua interpreter thay vì shim sẽ né được SAC:

```powershell
# Bị chặn (shim chưa ký):
hermes kanban list

# Chạy được (interpreter đã ký):
python -m hermes_cli.main kanban list
```

Kanban dispatcher của Hermes cũng spawn worker qua shim, nên cần patch để nó fallback sang module form khi phát hiện SAC Enforce + exe chưa ký. Đây là điểm cần kiểm tra lại sau mỗi lần update Hermes, vì patch nằm trong cây cài đặt.

## 6. Vòng đời task và tín hiệu quan sát

Task Kanban đi qua các trạng thái sau; mỗi trạng thái có một tín hiệu quan sát tương ứng:

| Trạng thái | Ý nghĩa | Tín hiệu giám sát |
|---|---|---|
| `ready` | Chờ dispatcher claim | Có mặt trong `kanban list` |
| `running` | Worker đang chạy | Heartbeat trong `kanban log` |
| `review` | Chờ duyệt kết quả | Trạng thái review trên board |
| `done` | Hoàn thành | File `.result.json` xuất sang `03_DONE` |
| `blocked` | Chờ input / approval (R3) hoặc bị circuit breaker | Lý do trong `Events` của `show` |
| `crashed` | Worker chết giữa chừng | `pid not alive` trong `Runs` |
| `gave up` | Hết `max-retries`, circuit breaker | `gave_up` event |

Hai vòng khôi phục: `crashed` còn retry budget thì tự quay lại `running`; `blocked` / `gave up` cần thao tác `unblock` thủ công (sau khi đã sửa gốc) để đưa về `ready`.

## 7. Kiểm soát tiến trình nền qua DevWebUI

Importer chạy nền hai kênh song song, đều dùng interpreter đã ký (`pythonw` / module form) để không hiện cửa sổ console:

- **Windows Task Scheduler** — job `AIResearchHandoffKanbanImporter`, chạy `--once` mỗi phút, ẩn (`pythonw`), quyền `Limited`.
- **DevWebUI** — process `handoff-importer` chạy `watch.cmd` (`--watch --interval 60`), có nút start/stop và log trong giao diện web ở `http://127.0.0.1:4000`.

Hai kênh trùng nhau nhưng an toàn nhờ `idempotency_key` (`project_id:task_id:v<schema_version>`) — không tạo task đôi.

> Bài học popup: DevWebUI spawn process với `windowsHide: true`, nhưng nếu `watch.cmd` gọi `python.exe` (có console) thì cửa sổ vẫn nháy mỗi cycle. Đổi sang `pythonw.exe` (không cấp console) là dứt điểm. Tương tự, các lệnh con `hermes kanban` mà importer spawn cần `CREATE_NO_WINDOW` để không flash một cửa sổ mỗi task.

## 8. Checklist giám sát nhanh

Khi cần nắm tình trạng hệ thống trong 30 giây:

```powershell
# 1. Board còn task treo không?
python -m hermes_cli.main kanban --board ai-research-handoff list

# 2. Importer có lỗi gì gần đây?
Get-Content D:\4.Code\google-driver\handoff-kanban\logs\importer.jsonl -Tail 5

# 3. Task đang chạy có heartbeat không?
python -m hermes_cli.main kanban --board ai-research-handoff show <task_id>

# 4. Tiến trình nền còn sống? (importer, gateway, 9router)
#    Mở http://127.0.0.1:4000 hoặc kiểm tra process
```

## 9. Kết luận

> **Board nói task có lỗi; log worker nói vì sao; sửa gốc rồi mới unblock.**

Giám sát một hệ agent chạy nền không phải là dựng một dashboard, mà là biết ba lớp quan sát trả lời câu hỏi gì và đọc chúng theo đúng thứ tự. Bốn lớp lỗi thực chiến — model API, cấu hình profile, chính sách hệ điều hành, và envelope — đều có dấu hiệu riêng; nhận diện đúng lớp là điều kiện để sửa gốc thay vì retry mù cho đến khi circuit breaker chặn task lại.
