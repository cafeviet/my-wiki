# AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh

Chỉ riêng việc tuân theo chỉ thị không cung cấp thực thi đáng tin cậy. Các kiểm soát nhiều lớp (xác định nơi có thể, xác suất nơi cần thiết) giúp giữ agent bên trong các ranh giới vận hành ngay cả khi prompt mang tính đối kháng và hành vi của mô hình không thể dự đoán.

**Kết quả mong muốn:**

- Bạn định nghĩa trước các ranh giới vận hành và chính sách của agent và thực thi chúng qua các kiểm soát nhiều lớp, với các kiểm soát xác định (IAM, kiểm định lược đồ, các kiểm tra chính sách kỹ thuật) xử lý những gì có thể diễn đạt một cách xác định và các kiểm soát xác suất (bộ lọc nội dung, đánh giá hành vi) xử lý những gì không thể.
- Nhiều lớp kiểm định ở các giai đoạn khác nhau của chuỗi lời gọi của agent có thể giảm khả năng một thất bại kiểm soát đơn lẻ dẫn đến vi phạm ranh giới.
- Bạn ghi log, cảnh báo và định kỳ rà soát các can thiệp của guardrail, các vi phạm chính sách và các kết quả đánh giá hành vi để điều chỉnh các kiểm soát và làm nổi bật các mẫu mới nổi.

**Các phản mẫu thường gặp (anti-patterns):**

- Dựa vào một cấu hình guardrail duy nhất cho mọi ca sử dụng agent, áp dụng cùng các ràng buộc cho các agent thông tin rủi ro thấp và các agent vận hành rủi ro cao.
- Chỉ áp dụng lọc nội dung cho đầu ra của mô hình mà không kiểm định đầu vào trước, để cho nội dung đối kháng tới được mô hình trước khi bất kỳ kiểm tra nào chạy.
- Chỉ định nghĩa các ranh giới vận hành trong các system prompt ngôn ngữ tự nhiên, dựa vào việc tuân theo chỉ thị của mô hình như ràng buộc duy nhất, điều có thể bị vượt qua qua prompt injection hoặc cách khung đối kháng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các kiểm soát kỹ thuật xác định (IAM, kiểm định lược đồ) kết hợp với các kiểm soát nội dung xác suất (Guardrails) ở các giai đoạn riêng biệt giảm sự phụ thuộc chỉ vào việc tuân theo chỉ thị.
- Kiểm định nhiều lớp bắt các vi phạm chính sách ở nhiều giai đoạn, nên một sự vượt qua ở một lớp ít có khả năng dẫn đến một vi phạm ranh giới không được kiểm tra.
- Các can thiệp guardrail và các kết quả đánh giá được ghi log cung cấp cho các cập nhật chính sách khi các mẫu mới nổi lên, giữ các ranh giới cập nhật với các ca sử dụng đang tiến hóa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các ranh giới vận hành chỉ được viết trong system prompt thường không cung cấp thực thi đáng tin cậy. Một prompt có thể bị ghi đè bởi cách khung đối kháng, prompt injection, hoặc chính sự tái diễn giải sáng tạo của mô hình, và không kiểu thất bại nào trong đó tạo ra một tín hiệu kiểm toán trước khi ranh giới đã bị vượt qua. Mẫu thiết kế là phân lớp. Hãy diễn đạt những gì có thể diễn đạt một cách xác định thành các kiểm tra cứng:

- Giới hạn phạm vi IAM
- Kiểm định lược đồ
- Các chính sách Cedar
- Ranh giới quyền hạn

Dùng các kiểm soát xác suất (bộ lọc nội dung, đánh giá hành vi) để bao phủ các rủi ro mang hình dạng nội dung mà tính xác định không thể vươn tới.

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) là lớp xác suất. Hãy cấu hình một guardrail cơ sở với các ràng buộc phổ quát (không sinh nội dung có hại, không tiết lộ system prompt), rồi phủ chồng các cấu hình riêng theo ca sử dụng cho ngữ cảnh vận hành của từng agent. Cường độ bộ lọc nội dung cần được hiệu chỉnh theo độ nhạy của ca sử dụng: cường độ HIGH cho các agent hướng người tiêu dùng xử lý các danh mục như ngôn từ thù ghét, bạo lực và nội dung tình dục, cường độ MEDIUM cho các agent doanh nghiệp nội bộ, và các ngưỡng tùy chỉnh cho các miền chuyên biệt (y tế, pháp lý) với các chuẩn nội dung riêng của chúng. Kiểm duyệt nội dung cần áp dụng cho mọi đường đầu ra, bao gồm các đầu ra dùng trong các luồng công việc agent nội bộ và các thông điệp giữa các agent, không chỉ các phản hồi hướng người dùng. Dùng quản lý phiên bản Guardrails để quản lý thay đổi kèm khôi phục.

Kiểm định trước khi thực thi (pre-execution validation) quan trọng vì hai lý do. Áp dụng Guardrails cho các đầu vào của người dùng trước khi chúng tới mô hình sẽ chặn nội dung đối kháng trước khi nó tác động đến suy luận, và nó từ chối các đầu vào xấu trước khi chúng tiêu tốn năng lực suy luận. Khi một agent gọi một mô hình Amazon Bedrock có gắn một guardrail, kiểm tra chạy tự động trên đầu vào và đầu ra. API ApplyGuardrail chạy cùng chính sách một cách độc lập khi đường tự động không áp dụng — các agent gọi các mô hình không phải Amazon Bedrock (các API bên thứ ba, các mô hình tự host), các đường ống cần lọc nội dung trước khi quyết định có gọi một mô hình hay không (ví dụ, kiểm tra nội dung được truy xuất trước khi nó đi vào prompt), hoặc các điểm kiểm soát kiểm định bổ sung ngoài lần gọi mô hình.

Giám sát đóng vòng phản hồi. [Các chỉ số CloudWatch của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html) bao gồm InvocationsIntervened, được phân tách theo Operation (ApplyGuardrail) và GuardrailContentSource (Input / Output) để các can thiệp phía đầu vào và phía đầu ra hiển thị riêng biệt. Các cảnh báo Amazon CloudWatch về tỷ lệ can thiệp định tuyến qua Amazon SNS tới đội bảo mật. Để có chi tiết (cái gì bị chặn, chính sách nào kích hoạt, phần nào của nội dung bị ảnh hưởng), hãy bật ghi log lần gọi mô hình Amazon Bedrock, ghi lại đầy đủ dấu vết guardrail cho mỗi lời gọi. Hãy phân tích các mẫu can thiệp theo thời gian để tìm các kỹ thuật mới nổi đòi hỏi cập nhật chính sách và để bắt các danh mục bộ lọc sinh quá nhiều dương tính giả hoặc âm tính giả.

[Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đánh giá độ đúng đắn của việc đạt mục tiêu và theo dõi liệu các agent có đang đạt các mục tiêu dự định của chúng hay đang trôi dạt vào các mục tiêu bị lệch căn chỉnh. Các trình đánh giá dựng sẵn bao phủ độ đúng đắn, tính hữu ích, độ chính xác lựa chọn công cụ và độ an toàn. Các trình đánh giá dựa trên mô hình tùy chỉnh mở rộng độ bao phủ tới các yêu cầu căn chỉnh riêng của tổ chức. Hãy chạy các đánh giá theo một nhịp định kỳ và sau bất kỳ thay đổi đáng kể nào đối với các prompt, công cụ hay cấu hình guardrail của agent. Kết quả được công bố tới Amazon CloudWatch cùng với các insight của AgentCore Observability để có một khung nhìn thống nhất, và các cảnh báo CloudWatch về điểm đánh giá bắt được trôi dạt hành vi ngoài các ngưỡng chấp nhận được.

### Các bước triển khai

- **Ánh xạ các ràng buộc đạo đức tới các danh mục guardrail:** Định nghĩa các ràng buộc đạo đức của tổ chức và các ranh giới vận hành theo từng ca sử dụng agent và ánh xạ chúng tới các danh mục chính sách guardrail với sự phân biệt phù hợp theo rủi ro.
- **Xây dựng các cấu hình guardrail phân tầng:** Tạo các cấu hình [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) cơ sở và riêng theo ca sử dụng, áp dụng chúng cho mọi lần triển khai, và dùng quản lý phiên bản để có khả năng khôi phục.
- **Kiểm định đầu vào trước khi suy luận:** Gọi API ApplyGuardrail trên các đầu vào trước khi chúng tới mô hình, kiểm tra so với các chủ đề bị cấm, bộ lọc từ và các mẫu thông tin nhạy cảm.
- **Cảnh báo về các chỉ số can thiệp:** Cấu hình các cảnh báo Amazon CloudWatch trên các chỉ số Guardrails (đặc biệt là InvocationsIntervened), định tuyến cảnh báo qua Amazon SNS, và bật ghi log lần gọi mô hình Amazon Bedrock để có các bản ghi can thiệp chi tiết.
- **Triển khai AgentCore Evaluations với cảnh báo trôi dạt:** Triển khai [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) với các trình đánh giá dựng sẵn và tùy chỉnh, và cấu hình các cảnh báo Amazon CloudWatch trên điểm đánh giá để phát hiện trôi dạt hành vi.
- **Rà soát log can thiệp hàng tháng:** Thiết lập một cuộc rà soát hàng tháng các log can thiệp guardrail để nhận diện các mẫu mới nổi và cập nhật các chính sách tương ứng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](agentsec04-bp02.md)
- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](../8-agentsec08/agentsec08-bp01.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock Guardrails content filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filter.html)
- [Build responsible AI applications with Amazon Bedrock Guardrails](https://aws.amazon.com/blogs/machine-learning/build-responsible-ai-applications-with-amazon-bedrock-guardrails/)
- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
- [AI agents in enterprises: Best practices with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon SNS](https://aws.amazon.com/sns/)
