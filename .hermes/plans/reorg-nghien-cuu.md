# Plan: Gom nhóm lại mục `nghien-cuu/` dựa trên nội dung

Trạng thái: ĐỀ XUẤT — chưa thực thi. Chờ bạn chọn phương án.

## 1. Hiện trạng (48 file .md, 4 nhóm)

| Nhóm | Số bài (folder) | Chủ đề thực tế |
|---|---|---|
| `agents/` | 7 cụm | Hỗn hợp: lý thuyết agent (12-factor), Hermes plugin/handoff, **1 bài BIAN (trùng)**, **2 bài eval Langfuse** |
| `kien-truc/` | 7 cụm | Kiến trúc hệ thống/DN: Archify, WeKnora, **BIAN (trùng)**, **3 bài Langfuse/eval** |
| `ngan-hang-so/` | 5 cụm | Ngân hàng số, Agent governance, MBBank readiness |
| `jd-ai/` | 1 bài | JD kỹ sư AI (CBA) |

## 2. Vấn đề phát hiện qua đọc nội dung

### 2.1. BIAN bị trùng (duplicate thật)
- `agents/bian-okr-to-it-value-chain/index.md` và `kien-truc/bian-okr-to-it-value-chain/index.md`
- **Nội dung giống hệt** (diff chỉ khác dòng title + 3 đường dẫn iframe do khác thư mục). Assets 2 bên trùng tên.
- Không file nào khác link tới cả hai → xóa 1 bản an toàn.
- Bài này thuần kiến trúc doanh nghiệp (BIAN Service Landscape, EA, IT Demand). **Thuộc `kien-truc/`**, không thuộc `agents/`.
- **Đề xuất: giữ bản `kien-truc/`, xóa bản `agents/`** (cả md + public assets).

### 2.2. Cụm Langfuse/eval nằm rải 2 nhóm
5 bài cùng chủ đề quan sát + đánh giá agent (Langfuse / DeepEval / eval stack):
- `agents/langgraph-eval-stack-langfuse-deepeval-agentcore/` — eval stack LangGraph (tổng thuật)
- `agents/tracing-scoring-rag-langfuse-deepeval/` — trace + score RAG (tổng thuật)
- `kien-truc/edd-langfuse-deepeval/` — EDD + 2 bài con (CI/CD, integration patterns)
- `kien-truc/langfuse-self-hosted/` — vận hành Langfuse self-host
- `kien-truc/hermes-langfuse-integration/` — Hermes + Langfuse (bài mới)

Rải ở 2 nhóm làm khó tra cứu. 3 bài trong `kien-truc/` đã thành cụm sẵn; 2 bài trong `agents/` lạc chỗ.

### 2.3. `agents/` đang là "catch-all" lẫn 3 chủ đề
Lý thuyết agent (12-factor) + sản phẩm Hermes thực chiến (coach, handoff, giám sát) + eval + BIAN. Cần tách bạch.

### 2.4. `jd-ai/` chỉ 1 bài
Nhóm 1-bài hơi mỏng, nhưng chủ đề (tuyển dụng/năng lực) khác hẳn 3 nhóm kia → giữ riêng hợp lý.

---

## 3. Hai phương án gom nhóm

### PHƯƠNG ÁN A — Giữ 4 nhóm, chỉ dọn trùng + chuyển bài lạc (ít xáo trộn) ⭐ khuyến nghị

Trục gom = **chủ đề**, giữ nguyên 4 nhóm, chỉ sửa chỗ sai:

1. **Xóa trùng BIAN**: bỏ `agents/bian-okr-to-it-value-chain/` (giữ bản `kien-truc/`).
2. **Dồn eval về `kien-truc/`**: chuyển 2 bài eval từ `agents/` sang `kien-truc/`:
   - `agents/langgraph-eval-stack-...` → `kien-truc/langgraph-eval-stack-...`
   - `agents/tracing-scoring-rag-...` → `kien-truc/tracing-scoring-rag-...`
3. `agents/` còn lại = **thuần agent**: 12-factor, ai-engineering-coach-hermes, gptweb-drive-kanban handoff, van-hanh-giam-sat-handoff.
4. Cập nhật `index.md` của `agents/` và `kien-truc/` cho khớp.

Kết quả:
- `agents/` (5 cụm): 12-factor + coach + handoff design + handoff ops
- `kien-truc/` (8 cụm): Archify, WeKnora, BIAN, + **cụm Langfuse/eval 5 bài**
- `ngan-hang-so/`, `jd-ai/`: nguyên trạng

Ưu: ít di chuyển, link nội bộ gần như không đổi (không bài nào link chéo 2 bài đang đụng). Nhược: `kien-truc/` hơi to.

### PHƯƠNG ÁN B — Tách nhóm Langfuse/eval thành domain thứ 5 (gom mạnh)

Tạo nhóm mới `observability-eval/` (hoặc `danh-gia-quan-sat/`) gom cả 5 bài Langfuse/eval:
```
nghien-cuu/
├── agents/              # thuần lý thuyết + sản phẩm agent
├── kien-truc/           # Archify, WeKnora, BIAN
├── observability-eval/  # 5 bài Langfuse/DeepEval/eval (MỚI)
├── ngan-hang-so/
└── jd-ai/
```
- Xóa trùng BIAN như PA A.
- Chuyển 5 bài eval (2 từ agents + 3 từ kien-truc) vào nhóm mới.
- Tạo `observability-eval/index.md`.

Ưu: chủ đề eval/observability rất mạch lạc, dễ tra. Nhược: di chuyển nhiều hơn, phải sửa iframe path của tất cả bài có sơ đồ (edd, langfuse-self-hosted, hermes-langfuse-integration) + mirror `public/`, nhiều điểm dễ gãy hơn.

---

## 4. Quy trình thực thi (áp dụng cho A hoặc B)

Theo skill `translation-library-organization`:

1. **Backup trạng thái git** trước khi move (`git status` sạch các thay đổi liên quan).
2. **Xóa trùng BIAN**: `rm -rf` bản `agents/bian-okr-to-it-value-chain/` (md) + `public/nghien-cuu/agents/bian-okr-to-it-value-chain/` (assets). Xác nhận bản `kien-truc/` còn nguyên + iframe OK.
3. **Di chuyển bài** (md + public assets cùng lúc):
   - `mv` nếu tracked (git ghi rename); fallback `cp -r && rm -rf` nếu Windows báo Permission denied.
   - Mirror `src/public/nghien-cuu/<cũ>/` → `<mới>/`.
4. **Sửa đường dẫn iframe tuyệt đối** trong md đã move: `/nghien-cuu/<cũ>/...` → `/nghien-cuu/<mới>/...` (regex scripted).
5. **Cập nhật index.md** nhóm nguồn + nhóm đích (+ tạo index nhóm mới nếu PA B). Giữ title `# Heading 1` ngắn gọn (gọn mắt), mô tả dài để blockquote.
6. **Sửa link nội bộ** nếu có bài trỏ tới đường cũ (hiện grep = 0, nhưng kiểm lại sau move).
7. **Verify**:
   - `npm run build` → 0 dead link.
   - Diff iframe src trong `dist/` so với file html thực tế (OK/MISS từng cái).
   - `git status` → moves là rename, không đụng file lạ.

## 5. Rủi ro & lưu ý
- VitePress resolve URL thư mục chỉ qua `index.md` — bài 1-page giữ tên `index.md`, không đổi.
- Sidebar auto-sinh (`vitepress-sidebar`) → đổi folder là sidebar tự cập nhật, không cần sửa config.mts.
- Build xanh KHÔNG chứng minh iframe/ảnh còn sống — phải diff `dist/` (ghi trong skill).
- 12-factor có `bo-12-factor/` nhiều page không dùng `index.md` ở folder đó — KHÔNG đụng tới trong lần reorg này.

## 6. Quyết định cần bạn chốt
1. Chọn **Phương án A** (dọn nhẹ, giữ 4 nhóm) hay **B** (tách domain eval thứ 5)?
2. BIAN: đồng ý **giữ bản `kien-truc/`, xóa bản `agents/`**? (title bản kien-truc gọn hơn: "BIAN: Chuỗi Giá trị từ OKR đến CNTT")
3. Nếu B: tên nhóm mới — `observability-eval/` hay tiếng Việt `danh-gia-quan-sat/`?
