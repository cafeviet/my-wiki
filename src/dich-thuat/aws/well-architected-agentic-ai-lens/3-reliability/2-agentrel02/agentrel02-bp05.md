# AGENTREL02-BP05 Thiết lập giám sát của con người theo tầng và các luồng phê duyệt

Giám sát đồng nhất hoặc làm chậm mọi hành động thường quy đến mức bò, hoặc để một quyết định hệ trọng lọt qua mà không được kiểm tra. Phân tầng việc rà soát để khớp với rủi ro và khả năng đảo ngược của mỗi hành động cân bằng giữa thông lượng và quản trị phù hợp.

**Kết quả mong muốn:**

- Bạn có các hành động của tác nhân được phân loại thành các tầng (tự chủ, thông báo, phê duyệt) dựa trên tác động và khả năng đảo ngược.
- Bạn có một lớp rà soát tự động ở lượt đầu lọc các hành động vi phạm chính sách trước khi người rà soát nhìn thấy chúng.
- Bạn ghi log mọi quyết định giám sát với danh tính người rà soát, lý do và dấu thời gian phục vụ báo cáo tuân thủ và quản trị.

**Các phản mẫu thường gặp (anti-patterns):**

- Áp dụng giám sát đồng nhất bất kể rủi ro, tạo ra nghẽn cổ chai cho các tác vụ thường quy hoặc để các hành động hệ trọng lọt qua mà không được kiểm tra.
- Bỏ qua các tiêu chí leo thang rõ ràng, nên một số hành động rủi ro cao tiến hành tự chủ trong khi một số hành động rủi ro thấp lại xếp hàng chờ rà soát.
- Chạy các luồng phê duyệt không có timeout hay dự phòng, khiến tác nhân đình trệ vô thời hạn khi người rà soát không sẵn sàng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quản trị phù hợp cho các hành động hệ trọng mà không gây nghẽn cổ chai cho công việc thường quy.
- Giảm rủi ro từ tính ngẫu nhiên của LLM vì các quyết định không thể đảo ngược hoặc rủi ro cao được con người rà soát.
- Một vết kiểm toán phục vụ tuân thủ thông qua ghi log có cấu trúc các quyết định giám sát.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phân loại rủi ro là lựa chọn thiết kế đầu tiên. Phân loại các hành động của tác nhân thành ba tầng. Hành động tự chủ là rủi ro thấp và đảo ngược được. Hành động thông báo là rủi ro trung bình và tiến hành với việc người vận hành được biết. Hành động phê duyệt là rủi ro cao hoặc không đảo ngược được và cần con người phê duyệt tường minh. Mã hóa việc phân loại thành các chính sách Cedar qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), để việc thực thi tầng diễn ra tại ranh giới gateway trước khi tác nhân có thể thực thi. Thực thi dựa trên chính sách áp dụng việc phân loại lúc chạy thay vì chỉ dựa vào tài liệu tham khảo.

Rà soát lượt đầu tự động giảm tải cho người rà soát. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) chặn các đầu ra của tác nhân trước khi chúng tới người rà soát, lọc nội dung vi phạm các chính sách định trước. Những gì tới hàng đợi của con người nên là các trường hợp thực sự mơ hồ, còn các vi phạm chính sách được lọc tự động.

Các luồng phê duyệt cần cấu trúc, không chỉ một sự tạm dừng. Một yêu cầu rà soát có cấu trúc nên bao gồm mô tả hành động, lập luận của tác nhân, đánh giá tác động và lịch sử thực thi để người rà soát có thể quyết định nhanh. Cấu hình các timeout leo thang tới người rà soát thứ cấp hoặc lùi về các mặc định an toàn khi người rà soát chính không sẵn sàng, để hệ thống xử lý việc người rà soát vắng mặt mà không bị chặn vô thời hạn. Ghi log mọi quyết định với danh tính người rà soát, lý do và dấu thời gian, và giám sát độ sâu hàng đợi phê duyệt qua Amazon CloudWatch để phát hiện khi các bản rà soát đang tích tụ. Các công cụ phát triển như [Kiro](https://kiro.dev/autonomous-agent/) triển khai mẫu tự chủ tăng tiến (progressive autonomy) này một cách trực tiếp. Chế độ giám sát rà soát mỗi hành động trước khi nó được áp dụng, trong khi chế độ autopilot cấp quyền tự chủ đầy đủ cho các luồng công việc đáng tin cậy. Hai chế độ này phản chiếu mô hình giám sát theo tầng ở lớp phát triển.

### Các bước triển khai

- **Định nghĩa một khung phân loại rủi ro:** Phân loại các hành động của tác nhân thành các tầng tự chủ, thông báo và phê duyệt dựa trên tác động và khả năng đảo ngược, và mã hóa việc phân loại thành các chính sách Cedar qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html).
- **Cấu hình Amazon Bedrock Guardrails làm lớp lượt đầu tự động:** Dùng [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) để lọc các hành động vi phạm chính sách trước khi leo thang tới con người.
- **Xây dựng các luồng phê duyệt có cấu trúc:** Tạm dừng thực thi và định tuyến các yêu cầu rà soát tới người rà soát. Mỗi yêu cầu nên bao gồm mô tả hành động, lập luận của tác nhân, đánh giá tác động và lịch sử thực thi.
- **Cấu hình các timeout và đường leo thang:** Xử lý việc người rà soát vắng mặt mà không bị chặn vô thời hạn, với leo thang tới người rà soát thứ cấp hoặc lùi về mặc định an toàn.
- **Ghi log mọi quyết định giám sát:** Bắt danh tính người rà soát, lý do và dấu thời gian để vết kiểm toán hỗ trợ báo cáo tuân thủ và quản trị.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](agentrel02-bp03.md)
- [AGENTREL02-BP04 Phát triển các giao thức chỉ dẫn rõ ràng cho tác nhân](agentrel02-bp04.md)
- [AGENTSEC04-BP02 Human-in-the-loop for critical decisions](../../2-security/4-agentsec04/agentsec04-bp02.md)
- [AGENTSUS03-BP01 Maintain organizational skills and competencies](../../6-sustainability/3-agentsus03/agentsus03-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Human-in-the-loop (HITL) - Amazon Nova Act](https://docs.aws.amazon.com/nova-act/latest/userguide/hitl.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Evaluating AI agents: Real-world lessons from building agentic systems at Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)

**Công cụ liên quan:**

- [Kiro Autonomous Agent](https://kiro.dev/autonomous-agent/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
