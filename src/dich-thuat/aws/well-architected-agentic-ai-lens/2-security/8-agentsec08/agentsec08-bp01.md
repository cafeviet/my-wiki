# AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection

Agent nhận đầu vào từ nhiều bề mặt và chỉ cần một bề mặt chưa được kiểm định là đủ để nội dung đối kháng tới quá trình suy luận của agent. Một kiến trúc kiểm định nhiều lớp bao phủ mọi bề mặt, và đặc biệt bắt được prompt injection gián tiếp nhúng trong nội dung ngoài được truy xuất.

**Kết quả mong muốn:**

- Mọi bề mặt đầu vào có một lớp kiểm định phù hợp với hồ sơ rủi ro của nó, và không có đầu vào nào tới quá trình suy luận của agent mà không đi qua ít nhất một kiểm soát kiểm định.
- Bạn giải quyết cụ thể prompt injection gián tiếp qua nội dung ngoài được truy xuất, đây là bề mặt thường bị bỏ sót nhất khi kiểm định chỉ được áp dụng cho các đầu vào trực tiếp của người dùng.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ áp dụng kiểm định đầu vào cho các đầu vào trực tiếp của người dùng trong khi bỏ qua kiểm định cho dữ liệu được truy xuất từ các nguồn ngoài, để cho các chỉ thị nhúng trong các trang web, tài liệu và phản hồi API vượt qua kiểm định hướng người dùng.
- Kiểm định tại một bề mặt đầu vào nhưng không tại các bề mặt khác (ví dụ, kiểm định các đầu vào người dùng bằng Guardrails nhưng không kiểm định các đầu ra công cụ trước khi chúng đi vào ngữ cảnh của agent), tạo ra các khoảng trống có thể bị nhắm tới.
- Định nghĩa các chủ đề bị cấm bằng các mô tả mơ hồ hoặc quá rộng sinh ra các dương tính giả trên nội dung hợp lệ, làm xói mòn sự tin tưởng và thúc đẩy các nhóm làm yếu hoặc tắt hẳn các guardrail.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiến trúc chiều sâu phòng thủ nơi mỗi bề mặt đầu vào có kiểm định phù hợp với hồ sơ rủi ro của nó giúp bao phủ mọi bề mặt.
- Kiểm định nội dung ngoài trước khi nó đi vào ngữ cảnh của agent đóng khoảng trống bị bỏ sót nhất: prompt injection gián tiếp.
- Các chế độ đánh giá dựa trên độ tin cậy cho phép các tổ chức điều chỉnh độ nghiêm ngặt của kiểm định theo từng danh mục bộ lọc dựa trên khả năng xảy ra và tác động của từng kịch bản rủi ro.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các bề mặt đầu vào của một agent không phải là một thứ. Các thông điệp trực tiếp của người dùng, các đầu ra công cụ, các thông điệp giữa các agent, nội dung ngoài được truy xuất (các trang web, tài liệu, phản hồi API), và các lần đọc bộ nhớ đều là các đường mà dữ liệu tới ngữ cảnh của agent, và mỗi cái cần một kiểm soát kiểm định. Hướng dẫn riêng theo bề mặt nằm trong AGENTSEC01-BP02 (đầu vào bộ nhớ), AGENTSEC02-BP02 (tham số công cụ) và AGENTSEC04-BP01 (guardrail căn chỉnh mục tiêu). Thực hành tốt này là khung kiến trúc và tập trung vào mối quan tâm xuyên suốt mà những cái kia không bao phủ: prompt injection gián tiếp qua việc truy xuất nội dung ngoài.

Truy xuất nội dung ngoài là bề mặt thường bị bỏ sót nhất. Khi một agent dùng RAG, duyệt web hoặc các lời gọi API để thu thập thông tin trong quá trình thực thi tác vụ, nội dung được truy xuất trở thành một phần của ngữ cảnh của agent, và các chỉ thị đối kháng nhúng trong nội dung đó (prompt injection gián tiếp) tác động đến hành vi của agent hiệu quả như một prompt injection trực tiếp. Hãy áp dụng [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) với phát hiện tấn công prompt cho mọi nội dung được truy xuất trước khi nó đi vào ngữ cảnh của agent, và hiện thực kiểm định nguồn nội dung hạn chế agent chỉ truy xuất nội dung từ các domain hoặc nguồn dữ liệu được phê duyệt nơi khả thi.

Guardrails cung cấp một cơ chế kiểm định thống nhất có thể được áp dụng qua nhiều bề mặt đầu vào thông qua API ApplyGuardrail. Hãy cấu hình một guardrail với phát hiện tấn công prompt, các chủ đề bị cấm và các bộ lọc từ một lần, và áp dụng nó tại mỗi ranh giới đầu vào. Điều đó cho bạn thực thi chính sách nhất quán qua các bề mặt với điều chỉnh riêng theo bề mặt thông qua quản lý phiên bản guardrail.

Hai chế độ đánh giá quan trọng: chế độ chặn (block mode) trả về một quyết định nhị phân cho phép hoặc từ chối, và chế độ phát hiện (detect mode) trả về các điểm độ tin cậy cho từng danh mục bộ lọc mà không chặn yêu cầu. Hãy dùng chế độ chặn cho phát hiện tấn công prompt, nơi ngay cả các khớp độ tin cậy thấp cũng đáng can thiệp cho mức nghiêm trọng của tác động tiềm tàng. Với các bộ lọc an toàn nội dung trên các ứng dụng nội bộ hoặc rủi ro thấp hơn, chế độ phát hiện cho phép ứng dụng đưa ra các quyết định tương xứng với rủi ro dựa trên các điểm độ tin cậy được trả về. Hãy chấm điểm mỗi kịch bản rủi ro theo khả năng xảy ra và tác động để xác định các ngưỡng độ tin cậy phù hợp theo từng danh mục bộ lọc thay vì áp dụng các ngưỡng đồng nhất.

Các chủ đề bị cấm dùng đánh giá dựa trên LLM, mang tính xác suất để xác định liệu nội dung có khớp một định nghĩa chủ đề, và chất lượng định nghĩa thúc đẩy độ chính xác. Hãy dùng đầy đủ giới hạn 1.000 ký tự cho mỗi định nghĩa chủ đề bị cấm với các mô tả cụ thể và không mơ hồ, và điền cả năm trường prompt mẫu (mỗi trường tối đa 200 ký tự) với các ví dụ đại diện minh họa ranh giới giữa nội dung bị hạn chế và được cho phép. Các định nghĩa mơ hồ hoặc rộng làm tăng các tỷ lệ dương tính giả, điều làm xói mòn sự tin tưởng của người dùng và gây áp lực buộc các nhóm làm yếu hoặc tắt các guardrail.

Khi dùng API ApplyGuardrail trực tiếp (thay vì qua API Converse hoặc Amazon Bedrock Agents), các kết quả đánh giá guardrail không tự động được công bố tới Amazon CloudWatch. Bạn chịu trách nhiệm về đường ống dữ liệu đo lường thu các kết quả đánh giá, các điểm độ tin cậy và nội dung bị chặn. Hãy đặt tham số outputScope thành full trên các lời gọi API ApplyGuardrail để nhận dữ liệu đánh giá đầy đủ bao gồm các điểm độ tin cậy theo từng bộ lọc, điều thiết yếu để điều chỉnh các ngưỡng và cung cấp cho Guardrails Optimizer. Hãy ghi log cả nội dung yêu cầu lẫn phản hồi đánh giá cho các mục bị chặn, dữ liệu này cần thiết cho việc tinh chỉnh cấu hình liên tục và phân tích dương tính giả.

Amazon Bedrock Guardrails Optimizer là một hiện thực tham chiếu trên AWS Samples tự động hóa việc tinh chỉnh cấu hình guardrail. Nó dùng một Strands Agent để lặp đi lặp lại điều chỉnh các định nghĩa chủ đề bị cấm, các prompt mẫu và các ngưỡng bộ lọc dựa trên dữ liệu kiểm thử đã chú thích. Trái với tinh chỉnh mô hình (fine-tuning), đây là tối ưu cấu hình chính sách. Agent phân tích các ca kiểm thử thất bại, viết lại cấu hình guardrail, đánh giá lại so với tập dữ liệu kiểm thử, và lặp lại cho đến khi đạt độ chính xác mục tiêu. Hãy chuẩn bị một tập dữ liệu đại diện được chú thích với các kết quả mong đợi (cho phép hoặc từ chối cho từng danh mục bộ lọc), chạy Optimizer trong quá trình thiết lập guardrail ban đầu, và lên lịch chạy lại định kỳ (hàng tháng hoặc hàng quý) dùng các mẫu từ lưu lượng sản xuất để thích ứng với các mẫu nội dung đang tiến hóa và giảm các tỷ lệ dương tính giả theo thời gian.

### Các bước triển khai

- **Ánh xạ các bề mặt đầu vào và gán các kiểm soát:** Nhận diện mọi bề mặt đầu vào cho từng agent và kiểm soát kiểm định bao phủ từng bề mặt, gắn cờ bất kỳ bề mặt nào hiện chưa được kiểm định.
- **Kiểm định nội dung ngoài được truy xuất:** Cấu hình [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) với phát hiện tấn công prompt và áp dụng nó cho nội dung ngoài (kết quả RAG, nội dung web, phản hồi API) trước khi nó đi vào ngữ cảnh của agent.
- **Chọn chế độ đánh giá theo rủi ro:** Dùng chế độ chặn cho các bộ lọc phát hiện tấn công prompt và cân nhắc chế độ phát hiện cho các bộ lọc an toàn nội dung trên các ứng dụng rủi ro thấp hơn, hiện thực logic ở cấp ứng dụng để đưa ra các quyết định tương xứng với rủi ro dựa trên các điểm độ tin cậy được trả về.
- **Viết các chủ đề bị cấm chính xác:** Dùng đầy đủ giới hạn 1.000 ký tự cho mỗi định nghĩa chủ đề bị cấm và điền cả năm trường prompt mẫu với các ví dụ đại diện minh họa ranh giới giữa nội dung bị hạn chế và được cho phép.
- **Thu dữ liệu đo lường ApplyGuardrail:** Đặt outputScope thành full trên mọi lời gọi API ApplyGuardrail và hiện thực một đường ống dữ liệu đo lường để thu các kết quả đánh giá, các điểm độ tin cậy và nội dung bị chặn trong Amazon CloudWatch.
- **Chạy Guardrails Optimizer:** Chạy Amazon Bedrock Guardrails Optimizer với một tập dữ liệu kiểm thử đã chú thích trong quá trình thiết lập ban đầu, rồi lên lịch tái tối ưu định kỳ (hàng tháng hoặc hàng quý) dùng các mẫu từ lưu lượng sản xuất.
- **Hạn chế các nguồn nội dung nơi khả thi:** Hiện thực kiểm định nguồn nội dung hạn chế các agent chỉ truy xuất nội dung từ các domain hoặc nguồn dữ liệu được phê duyệt.
- **Kiểm chứng các kiểm soát riêng theo bề mặt tồn tại:** Xác nhận rằng các kiểm soát được mô tả trong AGENTSEC01-BP02 (đầu vào bộ nhớ), AGENTSEC02-BP02 (tham số công cụ) và AGENTSEC04-BP01 (guardrail căn chỉnh mục tiêu) được hiện thực cho từng agent áp dụng.
- **Ghi log và rà soát các đầu vào bị chặn:** Ghi log mọi đầu vào bị chặn qua các bề mặt và rà soát các mẫu định kỳ để nhận diện các kỹ thuật mới và các bề mặt có thể cần bao phủ thêm.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC01-BP02 Kiểm định và làm sạch đầu vào bộ nhớ](../1-agentsec01/agentsec01-bp02.md)
- [AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ](../2-agentsec02/agentsec02-bp02.md)
- [AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh](../4-agentsec04/agentsec04-bp01.md)
- [AGENTSEC08-BP02 Lọc đầu ra cho thông tin nhạy cảm](agentsec08-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Guardrails prompt attack detection](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html)
- [Amazon Bedrock Guardrails denied topics](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html)
- [Amazon Bedrock Guardrails ApplyGuardrail API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html)
- [Build responsible AI applications with Amazon Bedrock Guardrails](https://aws.amazon.com/blogs/machine-learning/build-responsible-ai-applications-with-amazon-bedrock-guardrails/)
- [Best practices with Amazon Bedrock Guardrails filter configuration](https://aws.amazon.com/blogs/machine-learning/build-safe-generative-ai-applications-like-a-pro-best-practices-with-amazon-bedrock-guardrails/)
- [Thực hành tốt Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)

**Ví dụ liên quan:**

- [Amazon Bedrock Guardrails Evaluation and Optimization Framework](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/responsible_ai/bedrock-guardrails-optimizer)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
