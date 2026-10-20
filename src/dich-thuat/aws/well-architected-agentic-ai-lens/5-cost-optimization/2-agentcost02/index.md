# Tối ưu chi phí gọi model và token

Các nhóm định cỡ đúng việc lựa chọn model theo độ phức tạp của tác vụ và tối ưu lượng tiêu thụ token cho mỗi lần gọi có thể cải thiện mức giảm chi phí mà không hy sinh chất lượng quyết định của agent. Chi phí foundation model có thể chi phối ngân sách AI agentic, khi các agent có thể gọi các model đắt tiền cho các tác vụ đơn giản hoặc tiêu thụ token quá mức thông qua suy luận dài dòng.

| AGENTCOST02: Làm thế nào để tối ưu chi phí gọi model và tiêu thụ token của agent? |
| --- |
|  |

## Mục tiêu năng lực

- Việc lựa chọn model khớp với độ phức tạp của tác vụ, với phân loại và định dạng thường quy được xử lý bởi các model tiết kiệm chi phí và các model cao cấp được dành cho suy luận thực sự cần chúng.
- Các prompt, mô tả công cụ và ràng buộc đầu ra được giữ ở kích thước tối thiểu cần thiết để duy trì chất lượng quyết định qua các pha planning, execution và reflection.
- Suy luận lặp lại và ngữ cảnh ổn định được phục vụ từ **cache** thay vì tạo lại, nên các yêu cầu tương đương không phải trả toàn bộ chi phí suy luận hai lần.
- Các tác vụ khối lượng lớn, lặp lại chạy trên các model chuyên biệt hoặc tùy chỉnh mà chi phí huấn luyện một lần khấu hao vào khoản tiết kiệm bền vững trên mỗi lần gọi.
- Chi phí trên mỗi phản hồi đúng, lượng tiêu thụ token, tỷ lệ trúng cache và tỷ lệ leo thang cascade được theo dõi theo từng tầng model và được đưa ngược trở lại vào các quyết định định tuyến, caching và tùy chỉnh.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc tối ưu chi phí gọi model và token nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các nhóm gọi một foundation model mặc định duy nhất cho mọi tác vụ agent bất kể độ phức tạp, và các prompt, danh sách công cụ và đầu ra phình to mà không được xem xét. Không có prompt caching, semantic caching hay tùy chỉnh model nào được áp dụng. Các cú sốc chi phí bị quy cho tăng trưởng lưu lượng thay vì được điều tra. |
| 2 | Nhen nhóm (Emerging) | Một chính sách định tuyến model được ghi chép ánh xạ các loại tác vụ tới các tầng model cụ thể, và các môi trường được căn chỉnh với [tầng giá on-demand của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html) phù hợp (Flex, Standard, Priority). Nén prompt, ràng buộc độ dài đầu ra tường minh, và [prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) cho các system prompt ổn định được áp dụng cho các agent khối lượng cao nhất. Lượng tiêu thụ token được xem xét định kỳ theo các dashboard chi phí tổng hợp. |
| 3 | Xác định (Defined) | Một bộ tiền phân loại định tuyến mọi lần gọi tới một tầng model dựa trên độ phức tạp tác vụ, và model cascading với leo thang dựa trên độ tin cậy là mẫu mặc định cho suy luận không tầm thường. Semantic caching và tái sử dụng plan template chạy song song với prompt caching, với TTL được phân biệt theo độ tươi của tác vụ. Lượng tiêu thụ token, tỷ lệ trúng cache và tỷ lệ leo thang cascade được theo dõi theo từng pha suy luận bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và [Bedrock batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html) được dùng cho công việc không nhạy về thời gian. |
| 4 | Chủ động (Proactive) | Định tuyến, caching và guardrail được tự động hóa. Các chính sách [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) thực thi giới hạn tầng model, các chính sách cache là hướng-sự-kiện, và các chuỗi fallback xử lý timeout mà không thử lại ở cùng tầng. Các loại tác vụ khối lượng lớn chạy trên các model đã chưng cất hoặc fine-tune tiết kiệm tham số trong production, được xác thực qua A/B testing với [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) và phục vụ qua [Custom Model Import](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html) trên [AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html). Chi phí trên mỗi phản hồi đúng là một số liệu cấp dịch vụ được theo dõi và định hướng các quyết định làm mới hàng quý. |
| 5 | Tối ưu (Optimized) | Các danh mục model được tối ưu liên tục. Các bộ phân loại độ phức tạp, ngưỡng cascade, ngưỡng tương đồng của cache và nhịp làm mới tùy chỉnh đều được tinh chỉnh từ dữ liệu đo lường production. Các model tùy chỉnh được làm mới trên một pipeline liên tục với trích xuất dữ liệu huấn luyện, đánh giá và cổng thăng cấp tự động. Tổ chức thúc đẩy cải thiện chi phí-trên-kết-quả qua từng quý trong khi duy trì hoặc nâng các đường cơ sở chất lượng quyết định, và đóng góp các mẫu và benchmark trở lại cho cộng đồng thực hành rộng hơn. |

## Các vấn đề thường gặp cần chú ý

- Mọi lần gọi agent mặc định dùng model đa năng có năng lực cao nhất, dẫn đến chi phí suy luận cao hơn cho phân loại và định dạng thường quy vốn có thể dùng các lựa chọn thay thế tiết kiệm chi phí.
- Các system prompt và danh mục công cụ tích lũy mà không được xem xét, nên khoản thuế token đầu vào cố định phải trả ở mọi lần gọi âm thầm tăng qua các tháng ngay cả khi lưu lượng không đổi.
- Caching được coi là một lần bật duy nhất thay vì một kỷ luật liên tục, nên các chính sách vô hiệu hóa lỗi thời, ngưỡng tương đồng yếu, hoặc các tiền tố có thể cache bị trôi làm xói mòn tỷ lệ trúng và khoản tiết kiệm mà không ai nhận thấy.
- Việc tùy chỉnh model được theo đuổi trên các workload khối lượng thấp hoặc phù phiếm thay vì trên các tác vụ khối lượng lớn, lặp lại nơi chi phí huấn luyện có thể khấu hao, khiến khoản đầu tư mãi mãi lỗ.
- Tín hiệu chi phí chỉ được theo dõi ở mức tổng hợp, nên các nhóm không thể thấy tầng, pha suy luận hay lớp cache nào đang đẩy chi tiêu và không thể ưu tiên công việc tối ưu dựa trên bằng chứng.

###### Các thực hành tốt

- [AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng](agentcost02-bp01.md)
- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](agentcost02-bp02.md)
- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](agentcost02-bp03.md)
- [AGENTCOST02-BP04 Triển khai tùy chỉnh model để giảm chi phí dài hạn](agentcost02-bp04.md)
