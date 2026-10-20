# Cron dọn dẹp máy định kỳ

> **Mục tiêu:** một cron job (lịch chạy định kỳ) trên Hermes Agent, dùng mô hình **1 Agent Lead điều phối nhiều Worker song song** để dọn dẹp máy — Docker, log 9Router, và build artifact của my-wiki — mỗi tuần một lần, tự giao báo cáo về chat. Bài này minh hoạ cách dựng workflow lead→worker chạy nền trên Hermes, bổ sung cho [kiến trúc handoff](../gptweb-google-drive-hermes-kanban/) và [vận hành & giám sát](../van-hanh-giam-sat-hermes-handoff/).

## 1. Tóm tắt

Thay vì gõ tay nhiều lệnh dọn dẹp mỗi tuần, ta gói chúng vào **một skill lead** (`machine-cleanup`) và gắn skill đó vào **một cron job** của Hermes. Khi tới lịch, job tự chạy: Agent Lead fan out ba Worker song song (`delegate_task`), thu thập báo cáo rồi gộp thành một bản tổng với số byte thực sự thu hồi.

| Thuộc tính | Giá trị |
|---|---|
| Tên job | `machine-cleanup-weekly` |
| Job ID | `ac1ddbf2b0db` |
| Lịch chạy (Schedule) | `every monday 9am` (Thứ Hai 9h sáng, UTC+07:00) |
| Lặp lại | ∞ |
| Skill gắn kèm | `machine-cleanup` |
| Giao kết quả (Deliver) | `origin` — chat đã tạo job |
| Trạng thái lần chạy gần nhất | ✅ completed |

## 2. Vì sao dùng cron + delegate_task, không dùng Kanban

Hermes có hai mô hình điều phối (orchestration). Chọn đúng theo bài toán:

| | `delegate_task` (sub-agent) | Kanban (work queue) |
|---|---|---|
| Bản chất | Lead spawn worker trong cùng session, chạy song song | Board SQLite bền, dispatcher tự spawn profile theo task |
| Thời lượng | Vài phút, mất khi process thoát | Bền, sống qua restart |
| Phù hợp | Dọn dẹp định kỳ, task ngắn fan-out | Pipeline nhiều bước, nhiều máy, cần trạng thái lâu dài |

Dọn dẹp định kỳ là task ngắn, không cần trạng thái bền qua nhiều phiên → **cron + `delegate_task`** là lựa chọn nhẹ nhất. Kanban dành cho workflow như [AI Research Handoff](../gptweb-google-drive-hermes-kanban/).

## 3. Mô hình Lead → 3 Worker

Khi cron tick (Thứ Hai 9h), Agent Lead (nạp skill `machine-cleanup`) fan out ba Worker song song, mỗi Worker làm một nhiệm vụ độc lập với lệnh thật và luật an toàn riêng, rồi Lead gộp báo cáo.

```
cron tick (Thứ Hai 9h)
      │
      ▼
┌─────────────────────┐
│   AGENT LEAD        │  skill: machine-cleanup
│  (cleanup lead)     │  fan out song song
└──────────┬──────────┘
           │ delegate_task(tasks=[...])
   ┌───────┼───────────────┬─────────────────────┐
   ▼       ▼               ▼                     ▼
┌────────────┐  ┌────────────────┐  ┌──────────────────────┐
│ Worker 1   │  │ Worker 2       │  │ Worker 3             │
│ Docker     │  │ 9router logs   │  │ my-wiki artifacts    │
│ (SAFE tier)│  │ (>30 ngày)     │  │ (VitePress cache)    │
└─────┬──────┘  └───────┬────────┘  └──────────┬───────────┘
      └─────────────────┼──────────────────────┘
                        ▼
             ┌─────────────────────┐
             │  LEAD gộp báo cáo   │  → giao về chat (origin)
             └─────────────────────┘
```

## 4. Chi tiết ba Worker

### Worker 1 — Docker (SAFE tier)
Thu hồi dung lượng Docker ở mức an toàn:

```bash
docker container prune -f     # container đã dừng
docker image prune -f         # image dangling (KHÔNG dùng -a)
docker builder prune -f       # build cache
docker network prune -f       # network không dùng
```

Luật an toàn: không prune volume, không đụng container/image đang chạy, không chạy `docker system prune -a --volumes`. Docker không khả dụng → SKIP.

### Worker 2 — Log 9Router
Xoá file log/usage cũ hơn 30 ngày trong `~/.9router`:

```bash
find ~/.9router -maxdepth 1 -type f \
  \( -name 'log.txt' -o -name 'log*.txt' -o -name 'usage.json' \) \
  -mtime +30 -print -delete
```

Không đụng SQLite DB, auth, hay config — chỉ `log*.txt` và `usage.json`. Thư mục không tồn tại → SKIP.

### Worker 3 — Build artifact my-wiki
Xoá cache/dist VitePress (tái tạo được) dưới `D:/4.Code/my-wiki`:

```bash
# cache + dist của VitePress, cache của node_modules
src/.vitepress/cache   .vitepress/cache
src/.vitepress/dist    .vitepress/dist
node_modules/.cache
```

Không xoá source (`.md`, `assets/`, `public/`) hay `node_modules` chính. Tái tạo bằng `npm run docs:build`.

## 5. Luật an toàn chung

- Đo dung lượng **trước/sau**, báo cáo byte thực từ output lệnh — không ước lượng.
- Không xoá gì ngoài các target đã liệt kê.
- Target không tồn tại = **SKIP**, không phải lỗi.
- Không đụng container/image/volume đang dùng.

## 6. Tạo job và vòng kiểm chứng

Lệnh tạo job (gắn skill lead, giao kết quả về chat):

```bash
hermes cron create "every monday 9am" \
  "Run the machine cleanup lead playbook: fan out the three cleanup workers, collect reports, emit one consolidated summary with real reclaimed bytes." \
  --name machine-cleanup-weekly \
  --skill machine-cleanup \
  --deliver origin
```

Chạy thử ngay (không chờ lịch) để xác nhận lead + 3 worker hoạt động thật:

```bash
hermes cron run <job_id>
```

Kết quả chạy thử: lead fan out 3 task, tất cả `✓` (Docker ~294s, 9router logs ~74s, my-wiki ~196s), job `completed`.

## 7. Mẫu báo cáo tổng

```
Machine cleanup — <date>
- Docker: reclaimed <X> (containers/images/cache)   | or SKIPPED: <why>
- 9router logs: <N files, Y> deleted                 | or SKIPPED: not present
- my-wiki: reclaimed <Z> (cache/dist)                | or SKIPPED: <why>
Total reclaimed: <sum>
```

## 8. Lệnh quản lý

```bash
hermes cron list                  # xem job + lần chạy gần nhất
hermes cron runs <job_id>         # lịch sử các lần chạy
hermes cron run <job_id>          # chạy thử ngay
hermes cron pause <job_id>        # tạm dừng
hermes cron resume <job_id>       # bật lại
hermes cron edit <job_id>         # đổi lịch / skill / deliver
hermes cron remove <job_id>       # xoá job
```

## 9. Bài học vận hành

- **Chạy thử trước khi tin.** Lần chạy đầu thất bại với `No module named 'pydantic_core._pydantic_core'` — venv Python của Hermes hỏng, không phải lỗi job hay skill. Cron spawn một process con mới, nên nếu venv hỏng thì job luôn fail dù lệnh dọn dẹp hoàn toàn đúng.
- **Gốc rễ thường nằm ngoài job.** Nguyên nhân venv hỏng là một thư mục plugin ở profile khác (`profiles/reviewer/plugins/langfuse`) bị khoá quyền NTFS → chặn `hermes pm install`. Lấy lại quyền thư mục (`takeown` + `icacls /reset`) rồi chạy lại `pm install` (venv ✅) thì cron chạy thành công.
- **Cảnh báo "install out of sync" ở mọi lệnh `hermes`** là tín hiệu sớm của venv/plugin hỏng — xử lý ngay thay vì bỏ qua.
- **Mở rộng theo công thức:** viết một skill lead mô tả các worker + luật an toàn, rồi `hermes cron create ... --skill <tên>`. Cùng mẫu này dùng được cho backup định kỳ, health-check service, v.v.
