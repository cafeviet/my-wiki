# AGENTSEC07-BP02 Chỉ báo độ tin cậy rõ ràng và các cảnh báo thao túng

Những người rà soát được quản lý khối lượng công việc vẫn đưa ra các quyết định kém khi họ thiếu ngữ cảnh để đánh giá những gì agent đang khuyến nghị. Làm nổi bật độ tin cậy của agent, các cờ thao túng và các so sánh lịch sử cho phép người rà soát hiệu chỉnh mức soi xét theo rủi ro thực tế của mỗi quyết định.

**Kết quả mong muốn:**

- Những người rà soát của con người thấy các điểm độ tin cậy của agent, các chỉ báo bất định, và các cờ cảnh báo thao túng cùng với mỗi quyết định, cho phép họ hiệu chỉnh mức soi xét phù hợp.
- Ngữ cảnh lịch sử và các quyết định tương tự trong quá khứ được làm nổi bật để người rà soát có thể nhận diện khi một agent đang khuyến nghị một hành động lệch khỏi các mẫu đã thiết lập.

**Các phản mẫu thường gặp (anti-patterns):**

- Trình bày các quyết định của agent mà không có điểm độ tin cậy hay các chỉ báo bất định, để người rà soát không thể phân biệt các khuyến nghị độ tin cậy cao với các đầu ra suy đoán.
- Không làm nổi bật ngữ cảnh lịch sử hay các quyết định tương tự trong quá khứ, nên mọi khuyến nghị trông đều hợp lý như nhau mà không có một đường cơ sở về "điều gì thường xảy ra ở đây".
- Hiển thị các điểm độ tin cậy mà không giải thích ý nghĩa hay các giới hạn của chúng, dẫn đến người rà soát quá tin các đầu ra độ tin cậy cao mà không có sự hoài nghi phù hợp.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các điểm độ tin cậy và ngữ cảnh lịch sử giúp người rà soát hiệu chỉnh mức soi xét theo rủi ro thực tế của mỗi quyết định.
- Các cờ sai lệch thu hút sự chú ý của người rà soát tới các quyết định cần nó nhất khi một khuyến nghị của agent khác với các mẫu lịch sử.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Hãy bắt đầu với những gì người rà soát đang được yêu cầu quyết định. Hai mẫu là phổ biến và đòi hỏi các tín hiệu khác nhau. Trong **mẫu đánh giá viên (evaluator pattern)**, agent khuyến nghị một hành động và người rà soát quyết định liệu khuyến nghị có đúng hay không. Tín hiệu hữu ích là độ tin cậy của agent vào chính đầu ra của nó (một điểm thấp gợi ý khuyến nghị có thể sai). Trong **mẫu cổng (gate pattern)**, agent muốn thực hiện một hành động rủi ro cao và người rà soát là một cổng chính sách quyết định liệu hành động có nên được cho phép hay không. Chính độ tin cậy của agent kém hữu ích hơn vì agent sẽ không đề xuất hành động nếu nó nghĩ hành động đó sai. Với các cuộc rà soát mẫu cổng, tín hiệu hữu ích đến từ các hệ thống độc lập với agent: phát hiện bất thường, các kiểm tra chính sách, và các cờ cảnh báo thao túng từ đường ống kiểm định đầu vào.

Với các cuộc rà soát mẫu đánh giá viên, hãy cấu hình [bám ngữ cảnh của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html) để sinh một điểm bám ngữ cảnh kiểm tra liệu phản hồi có được hậu thuẫn bởi tài liệu nguồn mà agent được cung cấp hay không. Hãy làm nổi bật điểm đó cùng với các thông báo rà soát kèm các giải thích bằng ngôn ngữ đơn giản (ví dụ, "phản hồi của agent không được hậu thuẫn tốt bởi tài liệu nguồn, và khuyến nghị kiểm chứng độc lập") để người rà soát biết điểm đó nghĩa là gì thay vì đoán. Với các cuộc rà soát mẫu cổng, hãy rút từ các kiểm tra độc lập với agent: phát hiện bất thường (AGENTSEC07-BP04) đánh giá liệu hành động có lệch khỏi hành vi đường cơ sở, và các cờ cảnh báo thao túng do đường ống kiểm định đầu vào nêu ra (AGENTSEC04-BP01 và AGENTSEC08-BP01) báo hiệu khi bản thân yêu cầu trông có vẻ đối kháng. [Automated reasoning của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-policy.html) cung cấp một kiểm tra xác định bổ trợ kiểm chứng các đầu ra của agent so với một chính sách được viết chính thức (ví dụ, "người dùng trong region X không thể thực hiện thao tác Y"). Nó hữu ích nhất như ngữ cảnh trên màn hình của người rà soát ("cái này đã qua kiểm tra chính sách X vào lúc Y") thay vì như tín hiệu quyết định chính, vì các hành động qua được automated reasoning thường không cần cổng con người trừ khi bản thân chính sách được biết là có lỗ hổng hoặc hành động đủ khó đảo ngược để đáng có một phê duyệt dư của con người. Hãy làm nổi bật mỗi tín hiệu với cùng cách diễn đạt bằng ngôn ngữ đơn giản để người rà soát biết mỗi con số hoặc cờ nghĩa là gì.

Ngữ cảnh lịch sử làm cho các bất thường hiển thị. Hãy lưu các quyết định và các điểm độ tin cậy của chúng trong Amazon DynamoDB để truy xuất nhanh trong quá trình rà soát. Khi một quyết định mới xuất hiện, hãy truy vấn DynamoDB tìm các quyết định tương tự trong quá khứ (cùng loại thao tác, cùng agent, các tham số tương tự) và làm nổi bật chúng cùng với yêu cầu hiện tại. Hãy gắn cờ quyết định hiện tại nếu điểm độ tin cậy của nó lệch đáng kể so với trung bình lịch sử cho loại thao tác đó.

[Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) thêm tín hiệu xu-hướng-chất-lượng. Các trình đánh giá dựng sẵn bao phủ độ đúng đắn (đầu ra có khớp các câu trả lời mong đợi trên một tập kiểm thử hay không), tính hữu ích, độ chính xác lựa chọn công cụ (agent có chọn đúng công cụ cho tác vụ hay không), và độ an toàn. Hãy thêm các trình đánh giá tùy chỉnh cho các tiêu chí theo miền cụ thể: tuân thủ chính sách, tuân thủ định dạng (đầu ra có khớp lược đồ mà các hệ thống phía sau mong đợi hay không), và đạt mục tiêu (agent có thực sự hoàn thành những gì người dùng yêu cầu hay không). Hãy ưu tiên các trình đánh giá đo những thứ mà người rà soát không thể dễ dàng tự kiểm chứng trong thời gian họ có trong một cuộc rà soát. Nếu người rà soát có thể kiểm tra nó trong mười giây, đó không phải là mục đích của trình đánh giá. Một agent mà các điểm đánh giá đang có xu hướng đi xuống là một tín hiệu mà người rà soát cần thấy cùng với quyết định cụ thể trước mặt họ.

Các dashboard Amazon Quick trực quan hóa các mẫu quyết định và các bất thường theo thời gian. Các dashboard này giúp người rà soát và các đội bảo mật nhận diện các xu hướng mang tính hệ thống — ví dụ một agent cụ thể liên tục sinh các đầu ra độ tin cậy thấp cho một loại thao tác cụ thể — điều mà các cuộc rà soát quyết định riêng lẻ bỏ sót.

### Các bước triển khai

- **Cấu hình bám ngữ cảnh và automated reasoning:** Sinh các điểm độ tin cậy cho các đầu ra của agent qua bám ngữ cảnh và automated reasoning của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html), và bao gồm các giải thích bằng ngôn ngữ đơn giản cùng với các điểm số trong các thông báo rà soát.
- **Lưu các quyết định lịch sử để tra cứu tương tự:** Lưu bền vững các quyết định và các điểm độ tin cậy trong Amazon DynamoDB và hiện thực một truy vấn tương tự làm nổi bật các quyết định trong quá khứ cho cùng loại thao tác cùng với mỗi yêu cầu rà soát mới.
- **Gắn cờ các sai lệch khỏi các mẫu lịch sử:** Khi một điểm độ tin cậy lệch đáng kể so với trung bình lịch sử cho loại thao tác đó, hãy làm nổi bật nó cho người rà soát.
- **Làm nổi bật các xu hướng của AgentCore Evaluations:** Tích hợp các điểm chất lượng của [Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) vào ngữ cảnh rà soát để người rà soát có thể thấy liệu chất lượng agent tổng thể ổn định hay đang suy giảm.
- **Xây dựng các dashboard cho các xu hướng hệ thống:** Tạo các dashboard Amazon Quick trực quan hóa các mẫu quyết định, các phân bố điểm độ tin cậy và các xu hướng bất thường theo thời gian cho đội bảo mật rà soát.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh](../4-agentsec04/agentsec04-bp01.md)
- [AGENTSEC07-BP01 Triển khai quản lý tải nhận thức](agentsec07-bp01.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](agentsec07-bp04.md)

**Tài liệu liên quan:**

- [Tài liệu Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
- [Tài liệu Amazon Quick](https://docs.aws.amazon.com/quicksuite/latest/user/welcome.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon Quick](https://aws.amazon.com/quicksuite/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
