# Vì sao lại là 12-factor agents?

> **Nguồn gốc:** [humanlayer/12-factor-agents — README](https://github.com/humanlayer/12-factor-agents/blob/main/README.md) (commit `d20c728`)

> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Xét cho cùng, cách tiếp cận này **không hoạt động tốt như chúng ta mong muốn**.

`[Dịch]` Khi xây dựng HumanLayer, tôi đã nói chuyện với ít nhất 100 nhà xây dựng SaaS (phần lớn là founder kỹ thuật) đang muốn làm sản phẩm hiện tại của họ "agentic" hơn. Hành trình thường diễn ra đại khái như sau:

1. Quyết định rằng bạn muốn xây một agent
2. Thiết kế sản phẩm, thiết kế trải nghiệm người dùng (UX), xác định vấn đề cần giải quyết
3. Muốn đi nhanh, nên lấy `$FRAMEWORK` và *bắt tay vào xây*
4. Đạt được mức chất lượng 70–80%
5. Nhận ra rằng 80% không đủ tốt cho hầu hết tính năng phục vụ khách hàng
6. Nhận ra rằng để vượt qua 80% thì phải dịch ngược (reverse-engineer) framework, prompt, luồng chạy, v.v.
7. Bắt đầu lại từ đầu

> [!NOTE]
> **Vài lời miễn trừ ngẫu hứng** (từ nguyên bản)
>
> **MIỄN TRỪ 1**: Tôi không chắc chỗ nào là đúng nhất để nói điều này, nhưng chỗ này có vẻ tốt như bất kỳ chỗ nào: **điều này HOÀN TOÀN KHÔNG nhằm chỉ trích những framework ngoài kia, hay những người rất thông minh đang làm việc trên chúng**. Chúng tạo ra những điều phi thường và đã tăng tốc hệ sinh thái AI. Tôi hy vọng một kết quả của bài viết này là những người xây framework có thể học từ hành trình của tôi và của người khác, để làm ra những framework tốt hơn nữa. Đặc biệt là cho những người muốn đi nhanh nhưng cần kiểm soát sâu.
>
> **MIỄN TRỪ 2**: Tôi sẽ không nói về MCP. Tôi chắc bạn tự thấy được nó khớp vào đâu.
>
> **MIỄN TRỪ 3**: Tôi chủ yếu dùng TypeScript, vì [vài lý do](https://www.linkedin.com/posts/dexterihorthy_llms-typescript-aiagents-activity-7290858296679313408-Lh9e), nhưng toàn bộ những thứ này đều hoạt động được với Python hay bất kỳ ngôn ngữ nào bạn thích.

## Design Pattern cho những ứng dụng LLM tuyệt vời

`[Dịch]` Sau khi đào bới hàng trăm thư viện AI và làm việc với hàng chục founder, trực giác của tôi là thế này:

1. Có một số thứ cốt lõi khiến agent trở nên tuyệt vời
2. Dấn hết vào một framework và xây thứ về cơ bản là viết lại từ đầu (greenfield rewrite) có thể **phản tác dụng**
3. Có những nguyên lý cốt lõi khiến agent tuyệt vời, và bạn sẽ có được phần lớn/tất cả chúng nếu bạn kéo một framework vào
4. **NHƯNG**, cách nhanh nhất mà tôi thấy để nhà xây dựng có phần mềm AI chất lượng cao tới tay khách hàng là **lấy những khái niệm nhỏ, module hóa từ việc xây agent, và đưa chúng vào sản phẩm đang có của họ**
5. Những khái niệm module hóa này từ agent có thể được định nghĩa và áp dụng bởi hầu hết kỹ sư phần mềm giỏi, kể cả khi họ không có nền tảng AI

> #### Cách nhanh nhất mà tôi thấy để nhà xây dựng đưa phần mềm AI tốt tới tay khách hàng là lấy những khái niệm nhỏ, module hóa từ việc xây agent và đưa chúng vào sản phẩm đang có của họ.

Sơ đồ dưới đây đối chiếu **vòng lặp naive** (giao hết quyền quyết định cho model) với **vòng lặp do bạn sở hữu** (app giữ quyền điều khiển):

<iframe src="/nghien-cuu/agents/12-factor-agents/assets/02-naive-vs-so-huu.html" width="100%" height="620" style="border:none;border-radius:0.75rem;"></iframe>

---


---

**Điều hướng:** [← Chúng ta đã tới đây thế nào: Lược sử phần mềm](./lich-su-phan-mem.md) · [Mục lục](./) · [Factor 1: Natural Language to Tool Calls →](./factor-01-ngon-ngu-tu-nhien-thanh-tool-call.md)
