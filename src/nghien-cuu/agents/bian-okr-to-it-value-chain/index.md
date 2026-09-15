# Chuỗi giá trị từ OKR nghiệp vụ đến IT và vòng đo lường KR (BIAN)

> **Chuẩn tham chiếu:** BIAN Service Landscape V14 · **Phạm vi:** từ Objective/Key Result nghiệp vụ → thay đổi nghiệp vụ → tác động kiến trúc → nhu cầu CNTT → triển khai → kết quả nghiệp vụ → đo lường KR.
>
> **Nguyên tắc xuyên suốt:** OKR/KR **không phải** IT Requirement. Cầu nối chuẩn là `KR → Business Initiative / Business Change → Impact Assessment → IT Demand`.

---

## 1. Executive Summary

Trang này mô tả một **mô hình tham chiếu ổn định** để kiến trúc doanh nghiệp tiếp nhận yêu cầu nghiệp vụ bắt nguồn từ OKR đã đăng ký, phân rã thành thay đổi nghiệp vụ và tác động kiến trúc, chuyển tác động đủ điều kiện thành nhu cầu CNTT, triển khai CNTT, rồi **đo lường xem KR ban đầu có đạt được hay không**.

Mô hình gồm **ba nhóm logic** (project-level grouping — **không phải** tên BIAN Service Domain) ánh xạ tới năm BIAN Service Domain chính thức:

| Nhóm logic (project-level grouping) | BIAN Service Domain chính thức | Câu hỏi chủ sở hữu |
|---|---|---|
| **Business Direction & Execution** — Định hướng & thực thi nghiệp vụ | Business Unit Direction · Business Unit Management | Vì sao thay đổi? Kết quả mong muốn là gì? Có đạt không? |
| **Enterprise Architecture** — Kiến trúc doanh nghiệp | Enterprise Architecture | Cái gì phải thay đổi? Thành phần nào bị tác động? Có cần CNTT không? |
| **IT Demand & Delivery** — Nhu cầu & triển khai CNTT | IT Systems Direction · System Development | Có nên đầu tư? Ưu tiên khi nào? Triển khai thế nào? |

**Điểm cốt lõi:** vòng đời **không kết thúc ở Release**. Nó phải quay về:

```
Release → Business Adoption / Usage → Business Outcome → Measure KR → Business Unit Management / Direction
```

---

## 2. Chuỗi giá trị đầu-cuối (End-to-End Value Chain)

<iframe src="/nghien-cuu/agents/bian-okr-to-it-value-chain/assets/01-end-to-end-value-chain.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

Chuỗi giá trị chạy qua bốn lane: nghiệp vụ (Why/What) → kiến trúc (Impact/State) → CNTT (How) → **đo lường & đóng vòng (Business Outcome)**.

- **Objective + KR** (BU Direction) → **Business Change** (Initiative + Owner) → **Corrective Action** khi KR lệch mục tiêu.
- **Impact Assessment** (Capability/Process/Data) → **Target State** (Gap + IT Impact).
- **IT Demand** (assess + prioritize) → **IT Initiative** (portfolio + roadmap) → **Release** (build → test → ship).
- **Business Outcome** (Adoption · Actual vs Target) → **Measure KR** (đóng vòng nghiệp vụ) — thuộc **Business Unit Management / Direction**.
- Nhánh `KR không đạt` quay về Corrective Action, không sửa âm thầm phạm vi.

---

## 3. Nhóm 1 — Business Direction & Execution (Định hướng & thực thi nghiệp vụ)

**BIAN Service Domains:** Business Unit Direction — *Định hướng đơn vị*; Business Unit Management — *Quản trị đơn vị*.

**Luồng giá trị cốt lõi:**

```
Strategy → Objective → Key Result (KR) → Business Initiative → Business Change
```

**Vòng đóng kết quả:**

```
Business Outcome → Measure KR → Actual vs Target → Corrective Action
```

**Phạm vi cốt lõi:** Strategy / Objective / KR / Business Target · Business Initiative / Business Change · Business Plan / Activity / Deliverable · Business Owner / Business Priority · Business Outcome / KR Measurement · Performance Monitoring / Corrective Action.

**Câu hỏi then chốt:**

| Câu hỏi | Tiếng Anh |
|---|---|
| Vì sao cần thay đổi? | Why are we changing? |
| Kết quả nghiệp vụ mong muốn là gì? | What business outcome do we expect? |
| Kết quả có đạt mục tiêu không? | Did we achieve the expected outcome? |

> **Lưu ý mô hình:** `Business Initiative` và `Business Change` là **khái niệm project/domain-model**, không phải tên BIAN Service Domain chính thức.

---

## 4. Nhóm 2 — Enterprise Architecture (Kiến trúc doanh nghiệp)

**BIAN Service Domain:** Enterprise Architecture.

**Luồng giá trị cốt lõi:**

```
Business Initiative / Business Change
  → Impact Assessment
  → Business Capability / Process / Data / Application / Technology / Security Impact
  → Current State / Target State
  → Gap Analysis
  → IT Impact
```

**Phạm vi cốt lõi:** Business Capability Impact · Process Impact · Information/Data Impact · Application Impact · Technology Impact · Security Impact · Dependency Analysis · Current / Target Architecture · Gap Analysis · Architecture Principles / Constraints / Recommendation · IT Impact Identification.

**Câu hỏi then chốt:**

| Câu hỏi | Tiếng Anh |
|---|---|
| Cái gì phải thay đổi? | What needs to change? |
| Những thành phần nào bị tác động? | What is impacted? |
| Có cần thay đổi CNTT hay không? | Is IT change required? |

Kiến trúc là **một tầng độc lập** — không gộp vào nghiệp vụ, không gộp vào CNTT. Đây là nơi duy nhất sinh ra `IT Impact` một cách có kỷ luật.

---

## 5. Nhóm 3 — IT Demand & Delivery (Nhu cầu & triển khai CNTT)

**BIAN Service Domains:** IT Systems Direction — *Định hướng hệ thống CNTT*; System Development — *Phát triển hệ thống*.

**Luồng giá trị cốt lõi:**

```
IT Impact → IT Demand → Assessment → Priority → Capacity / Cost / Investment
  → IT Portfolio / Roadmap → IT Initiative → Requirement → Build → Test → Release
```

**Phạm vi — IT Systems Direction:** IT Demand Management / Assessment · IT Prioritization · IT Portfolio / Roadmap Planning · IT Capacity / Investment / Budget Planning · Business–IT Alignment · IT Commitment.

**Phạm vi — System Development:** IT Requirement Management · Development Planning · Solution Implementation · Software Development / Integration / Testing · Defect Resolution · Release Preparation / Technical Delivery.

**Câu hỏi then chốt:**

| Câu hỏi | Tiếng Anh |
|---|---|
| CNTT có nên đầu tư cho thay đổi này không? | Should IT invest in this change? |
| Khi nào và với mức ưu tiên nào? | When and with what priority? |
| CNTT sẽ triển khai thay đổi đã cam kết như thế nào? | How will IT implement the committed change? |

---

## 6. Sở hữu & ranh giới trách nhiệm (Domain Ownership & Boundary)

<iframe src="/nghien-cuu/agents/bian-okr-to-it-value-chain/assets/02-domain-ownership-boundary.html" width="100%" height="700" style="border:none;border-radius:0.75rem;"></iframe>

| Nhóm logic | Trong phạm vi — sở hữu | Ngoài phạm vi | Điểm bàn giao |
|---|---|---|---|
| Business Direction & Execution | Strategy · Objective · KR · Business Initiative · Business Change · Business Outcome · Measure KR · Corrective Action | Thiết kế giải pháp kỹ thuật | `Business Change → Impact Assessment` |
| Enterprise Architecture | Impact Assessment · Capability/Process/Data/App/Tech/Security Impact · Current/Target State · Gap Analysis · IT Impact | Cam kết ngân sách, triển khai mã nguồn | `IT Impact → IT Demand` |
| IT Demand & Delivery | IT Demand · Priority · Portfolio/Roadmap · Commitment · Requirement · Build · Test · Release | Đo lường kết quả nghiệp vụ, sở hữu KR | `Release → Business Outcome` |

**Tóm tắt trách nhiệm:**

| Vai trò | Sở hữu | Tiếng Anh |
|---|---|---|
| Nghiệp vụ | Kết quả | Business owns Outcome |
| Kiến trúc | Đánh giá tác động & trạng thái mục tiêu | Architecture owns Impact & Target State |
| CNTT | Cam kết & triển khai | IT owns Commitment & Delivery |
| Nghiệp vụ | Đóng vòng bằng đo lường KR | Business closes the loop by measuring KR |

> **Cảnh báo ngữ nghĩa:** "Business Initiative", "Business Change", "IT Demand" và tên ba nhóm logic là **khái niệm project/domain-model**, trừ khi nguồn BIAN chính thức định nghĩa đối tượng tương đương. Không trình bày chúng như tên BIAN Service Domain chính thức.

---

## 7. Mô hình đối tượng truy vết (Traceability Object Model)

<iframe src="/nghien-cuu/agents/bian-okr-to-it-value-chain/assets/03-traceability-object-model.html" width="100%" height="720" style="border:none;border-radius:0.75rem;"></iframe>

```
Objective → KR → Business Initiative → Business Change
  → Impact Assessment → Gap Analysis → IT Demand
  → IT Initiative → Release → Business Outcome → Measure KR
  → (đóng vòng) Objective
```

**Ba cổng kiểm soát:**

1. `Business Change → Impact Assessment` — cổng vào kiến trúc.
2. `Gap Analysis → IT Demand` — cổng vào CNTT.
3. `Measure KR → Objective` — cổng đóng vòng (closed loop).

Bảng truy vết đối tượng → domain sở hữu:

| Đối tượng | Nhóm sở hữu | Domain BIAN | Câu hỏi |
|---|---|---|---|
| Objective · KR | Business Direction & Execution | Business Unit Direction | Vì sao? Kết quả mong muốn? |
| Business Initiative · Business Change | Business Direction & Execution | Business Unit Direction / Management | Cái gì thay đổi? |
| Impact Assessment · Gap Analysis | Enterprise Architecture | Enterprise Architecture | Tác động gì? Trạng thái mục tiêu? |
| IT Demand · IT Initiative | IT Demand & Delivery | IT Systems Direction | Có nên đầu tư? Ưu tiên? |
| Release | IT Demand & Delivery | System Development | Triển khai thế nào? |
| Business Outcome · Measure KR | Business Direction & Execution | Business Unit Management / Direction | Có đạt mục tiêu không? |

---

## 8. Kết quả triển khai vs kết quả nghiệp vụ

Nếu CNTT hoàn thành (Release) nhưng KR **không** đạt, phải ghi nhận **hai loại thành công tách biệt**:

| Loại | Ý nghĩa | Ai sở hữu |
|---|---|---|
| Delivery success | Đúng hạn, đúng phạm vi kỹ thuật, đã phát hành | IT Demand & Delivery |
| Business outcome success | Kết quả nghiệp vụ thực tế đạt mục tiêu đề ra | Business Direction & Execution |

Khi KR không đạt: ghi nhận Corrective Action, hoặc điều chỉnh/tạo Business Initiative mới — **không** gộp hai loại thành công này làm một.

---

## 9. Kiểm chứng BIAN V14

Các xác nhận sau được kiểm chứng trực tiếp từ dữ liệu chính thức của BIAN Service Landscape V14 (nguồn `https://bian.org/servicelandscape-14-0-0/`), xem evidence kèm theo.

| # | Xác nhận | Nguồn |
|---|---|---|
| 1 | **Business Unit Direction** tồn tại | `object_15.html?object=36980`, `data/all_objects_data_15.js` |
| 2 | **Business Unit Management** tồn tại | Cùng file dữ liệu V14 |
| 3 | **Enterprise Architecture** tồn tại | `object_14.html?object=29101` |
| 4 | **IT Systems Direction** tồn tại | `object_16.html?object=44281` |
| 5 | **System Development** thuộc nhóm **Solution Development** | `object_31.html?object=48386` (hierarchy) |
| 6 | Direct functional pattern V14 | `object_45.html?object=95219` |
| 7 | Quan hệ hierarchy `Solution Development ⊃ System Development` | `all_objects_relations.js` |

**Phân định rõ:**

- **Fact** — tên và quan hệ hierarchy của năm Service Domain nêu trên, theo dữ liệu BIAN V14 chính thức.
- **Inference** — việc gom chúng thành ba nhóm logic và luồng giá trị đầu-cuối là mô hình kiến trúc của chúng ta, **không** phải định nghĩa của BIAN.
- **Recommendation** — dùng `KR → Business Initiative / Business Change → Impact Assessment → IT Demand` làm cầu nối chuẩn; không đưa KR trực tiếp vào IT Requirement.

---

## 10. Nguồn tham chiếu chính thức

| Tài liệu | Liên kết |
|---|---|
| BIAN Service Landscape V14 | https://bian.org/deliverables/service-landscape/ |
| Business Unit Management V14 | https://bian.org/servicelandscape-14-0-0/object_15.html?object=36980 |
| Enterprise Architecture V14 | https://bian.org/servicelandscape-14-0-0/object_14.html?object=29101 |
| IT Systems Direction V14 | https://bian.org/servicelandscape-14-0-0/object_16.html?object=44281 |
| Direct functional pattern V14 | https://bian.org/servicelandscape-14-0-0/object_45.html?object=95219 |
| Solution Development grouping V14 | https://bian.org/servicelandscape-14-0-0/object_31.html?object=48386 |

---

## 11. Ghi chú kỹ thuật về sơ đồ

Ba sơ đồ trong trang được tác giả bằng **Archify** (Typed JSON IR), validate qua `archify validate workflow <file> --quality showcase` trước khi render. Nguồn chỉnh sửa được lưu trong thư mục `assets/` cạnh bài viết:

| Sơ đồ | Nguồn Archify | Giao phẩm HTML |
|---|---|---|
| a. End-to-End Value Chain | `assets/01-end-to-end-value-chain.workflow.json` | `public/.../assets/01-end-to-end-value-chain.html` |
| b. Domain Ownership & Boundary | `assets/02-domain-ownership-boundary.workflow.json` | `public/.../assets/02-domain-ownership-boundary.html` |
| c. Traceability Object Model | `assets/03-traceability-object-model.workflow.json` | `public/.../assets/03-traceability-object-model.html` |

---

*Nguồn: Xác minh BIAN Service Landscape V14 (fetched 2026-09-15) + mô hình kiến trúc nội bộ. Evidence: `evidence/bian-v14-verification.txt`.*
