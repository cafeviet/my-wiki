# AGENTCOST07-BP01 Triển khai kiểm soát chi phí tự động với các điểm cắt thông minh

Các agent tự chủ gọi công cụ và tích lũy bộ nhớ mà không có trần là một rủi ro chi phí chính của các hệ thống agentic. Các giới hạn ngân sách phân cấp, các điểm cắt tự động trên các phiên chạy hoang, và throttling phân cấp giúp giữ chi phí của bạn bị giới hạn mà không buộc agent dừng làm việc ngay dấu hiệu áp lực đầu tiên.

**Kết quả mong muốn:**

- Bạn thực thi các giới hạn ngân sách theo chu kỳ, theo tác vụ, và theo ngày như các kiểm tra tiền-gọi, chứ không phải các cảnh báo sau khi sự việc đã xảy ra.
- Bạn có các điểm cắt tự động dừng các vòng lặp suy luận tại các ngưỡng số vòng lặp hoặc chi phí.
- Bạn có throttling phân cấp làm chậm các lần gọi khi ngân sách tiến gần các giới hạn thay vì buộc tắt máy nhị phân.
- Bạn yêu cầu phê duyệt cho các mở rộng năng lực làm tăng đáng kể các hồ sơ chi phí.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các agent mà không có giới hạn ngân sách, gây các khoản vượt chi bất ngờ trong quá trình vận hành production.
- Cho phép các agent rơi vào các vòng lặp suy luận không giới hạn tiêu thụ token mỗi chu kỳ mà không tiến triển hướng tới hoàn thành.
- Cho phép các lần gọi công cụ và tăng trưởng bộ nhớ không giới hạn: các agent tự chủ gọi công cụ và tích lũy bộ nhớ, và không có trần, chi phí tăng không giới hạn. Đây là một rủi ro chi phí chính của các agent tự chủ.
- Coi các kiểm soát chi phí và quyền tự chủ của agent là loại trừ lẫn nhau, hoặc hạn chế các agent quá mức hoặc cấp quyền chi tiêu không giới hạn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các giới hạn ngân sách phân cấp (như theo chu kỳ, theo tác vụ, và theo ngày) tạo nhiều rào cản phòng thủ chống lại các khoản vượt chi.
- Các điểm cắt tự động dừng các vòng lặp suy luận tại các ngưỡng đã cấu hình, xử lý một trong các chế độ lỗi đắt nhất trong các hệ thống tự chủ.
- Throttling phân cấp được thiết kế để bảo tồn chức năng agent ở thông lượng giảm thay vì buộc tắt máy đột ngột.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Triển khai các kiểm soát chi phí bên ngoài vòng lặp điều khiển của agent để thực thi đáng tin cậy. [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) áp dụng các chính sách Cedar tại ranh giới [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), giúp ngăn các agent lách qua các giới hạn ngân sách thông qua thao túng prompt. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) bổ sung điều này bằng cách thực thi các hạn chế dựa trên chủ đề giúp ngăn các chuỗi suy luận lạc đề, vốn giảm lãng phí token từ khám phá ngoài chủ đề.

Các ngân sách phân cấp cho bạn nhiều rào cản phòng thủ:

- Các giới hạn theo chu kỳ bắt các vòng lặp chạy hoang riêng lẻ
- Các giới hạn theo tác vụ bắt công việc tổng hợp trong một yêu cầu người dùng đơn lẻ
- Các giới hạn theo ngày bắt việc sử dụng cao liên tục

Các điểm cắt tự động theo dõi cả số vòng lặp và chi phí token tích lũy theo từng phiên, dừng các vòng lặp suy luận khi các ngưỡng bị vượt. Các trần gọi công cụ theo từng phiên quan trọng như một kiểm soát riêng vì mỗi lần gọi công cụ phát sinh cả chi phí API bên ngoài và chi phí token của việc xử lý dữ liệu trả về. Việc dùng công cụ không giới hạn có thể rút cạn ngân sách token từ hướng khác. Các guardrail tăng trưởng bộ nhớ giới hạn tốc độ tăng trưởng cửa sổ ngữ cảnh vì mỗi token trong ngữ cảnh đều được trả ở mọi lần gọi sau đó, biến việc tích lũy không giới hạn thành một động lực chi phí dồn tích.

Throttling là một kiểm soát tự động hữu ích khác. Các usage plan của Amazon API Gateway hoặc rate limiting tùy chỉnh dựa trên Lambda giảm thông lượng tối đa khi các ngân sách hàng ngày tiến gần các giới hạn, làm chậm tiêu thụ token mà không buộc các điểm cắt cứng. Throttling và các điểm cắt vận hành ở các quy mô khác nhau. Throttling xử lý việc sử dụng cao liên tục, trong khi các điểm cắt xử lý các phiên chạy hoang riêng lẻ. Một ngăn xếp kiểm soát được thiết kế tốt dùng cả hai, để lưu lượng cao bình thường được làm chậm thay vì bị dừng, và các phiên bệnh lý bị dừng thay vì bị làm chậm.

Giám sát các kiểm soát này bằng cách dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), vốn cấp cho các dashboard Amazon CloudWatch về mức sử dụng ngân sách, các lần kích hoạt điểm cắt, và các sự kiện throttling. Với các thay đổi cấu hình có tác động chi phí (thêm các công cụ đắt tiền, nâng cấp các model, hoặc mở rộng các năng lực tự chủ), hãy tích hợp các cổng xem xét chi phí vào pipeline CI/CD để các tác động chi phí đáng kể nhận được xem xét trước khi triển khai.

### Các bước triển khai

- **Thực thi các giới hạn ngân sách qua các chính sách Cedar:** Cấu hình [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với các chính sách Cedar thực thi các giới hạn ngân sách theo chu kỳ, theo tác vụ, và theo ngày tại ranh giới Gateway, bao gồm các trần gọi công cụ theo từng phiên và các guardrail tăng trưởng bộ nhớ kích hoạt tóm tắt khi ngữ cảnh tiến gần các giới hạn model.
- **Triển khai các điểm cắt tự động và các guardrail chủ đề:** Theo dõi số vòng lặp và chi phí tích lũy theo từng phiên với các điểm cắt tự động, và dùng [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) cho các hạn chế dựa trên chủ đề đối với suy luận lạc đề.
- **Thêm throttling phân cấp:** Triển khai throttling tiến triển làm chậm các lần gọi khi ngân sách tiến gần các giới hạn, giữ các thao tác agent ở thông lượng giảm thay vì buộc tắt máy nhị phân.
- **Trực quan hóa và cảnh báo trên các số liệu quản trị:** Tạo các dashboard Amazon CloudWatch hiển thị mức sử dụng ngân sách, các lần kích hoạt điểm cắt, và các sự kiện throttling bằng các số liệu [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)
- [AGENTCOST07-BP02 Thiết lập phát hiện bất thường chủ động cho các mẫu chi phí của agent](agentcost07-bp02.md)
- [AGENTCOST07-BP03 Tạo các vòng lặp phản hồi tối ưu có hệ thống để cải thiện liên tục](agentcost07-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [Amazon Bedrock capacity, limits, and cost optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)
- [Guidance for Cost Analysis and Optimization with Amazon Bedrock Agents](https://aws.amazon.com/solutions/guidance/cost-analysis-and-optimization-with-amazon-bedrock-agents/)

**Video liên quan:**

- [AWS re:Invent 2024 - Balance cost, performance & reliability for AI at enterprise scale (AIM3304)](https://www.youtube.com/watch?v=Lwvv8Q33eeE)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Policy tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/08-AgentCore-policy)

**Workshop liên quan:**

- [Diving Deep into Bedrock AgentCore - Policy](https://catalog.workshops.aws/agentcore-deep-dive/en-US/90-agentcore-policy)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)
