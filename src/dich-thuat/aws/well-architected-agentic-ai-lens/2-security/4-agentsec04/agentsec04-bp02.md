# AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng

Định tuyến mọi hành động của agent qua rà soát của con người tạo ra các phê duyệt máy móc (rubber-stamp). Không định tuyến hành động nào tạo ra tính tự chủ không giới hạn. Phê duyệt phân tầng theo rủi ro chỉ tạm dừng agent cho các quyết định mà phán đoán của con người thực sự thay đổi kết quả, với đủ ngữ cảnh để những quyết định đó có ý nghĩa.

**Kết quả mong muốn:**

- Bạn tạm dừng các thao tác agent rủi ro cao để con người rà soát trước khi thực thi, và người rà soát nhận đủ ngữ cảnh để đưa ra các quyết định có hiểu biết trong một cửa sổ thời gian đã định.
- Các đường leo thang xử lý các trường hợp mà người rà soát chính không sẵn có.
- Bạn ghi log các quyết định phê duyệt của con người với dấu thời gian và danh tính người rà soát, tạo ra một bản ghi có thể kiểm toán về sự giám sát của con người phục vụ mục đích tuân thủ.

**Các phản mẫu thường gặp (anti-patterns):**

- Định tuyến mọi hành động của agent qua rà soát của con người bất kể mức rủi ro, tạo ra sự mệt mỏi của người rà soát và các phê duyệt máy móc.
- Cung cấp cho người rà soát ngữ cảnh không đủ (chỉ hành động được đề xuất, không có chuỗi suy luận, nguồn dữ liệu hay các hậu quả tiềm tàng), biến rà soát thành một thủ tục hình thức.
- Hiện thực các luồng công việc phê duyệt mà không có các chính sách timeout hay các đường leo thang, nên việc thực thi của agent đình trệ vô thời hạn khi người rà soát không sẵn có.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các luồng công việc phê duyệt phân tầng theo rủi ro tập trung sự chú ý của người rà soát vào các quyết định mà phán đoán của con người quan trọng nhất.
- Các quyết định phê duyệt được ghi log với danh tính người rà soát và dấu thời gian tạo ra một bản ghi có thể kiểm toán đáp ứng các yêu cầu tuân thủ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Một khung phân loại rủi ro là thứ cho phép sự chú ý của con người đi tới nơi nó tạo ra giá trị. Hãy kết hợp các thuộc tính tĩnh của thao tác (loại hành động nào, đối với tài nguyên nào) với các tín hiệu động về yêu cầu (tần suất, giờ trong ngày, vị trí nguồn, các bất thường gần đây). Bản thân việc phân loại rủi ro không thể dựa vào một LLM tiếp xúc với cùng nội dung không đáng tin như yêu cầu đang được đánh giá, vì nội dung đối kháng có thể tác động lên bộ phân loại để đánh dấu yêu cầu là rủi ro thấp. Hãy dùng logic xác định (các bộ máy chính sách, các bộ phân loại dựa trên quy tắc) như tín hiệu có thẩm quyền, với việc phân loại có LLM hỗ trợ như một đầu vào tùy chọn mà một lớp xác định kiểm tra lại. Như một đường cơ sở: các thao tác chỉ-đọc tiến hành tự chủ, các lượt ghi rủi ro thấp yêu cầu phê duyệt một người rà soát, và các thao tác rủi ro cao hơn (giao dịch tài chính, xóa dữ liệu, giao tiếp bên ngoài) yêu cầu phê duyệt nghiêm ngặt hơn, có thể là một người rà soát, nhiều người rà soát, hoặc ngoài băng tùy theo chính sách rủi ro của bạn. Để tham khảo các cách tiếp cận khung rủi ro đã được thiết lập nhằm điều chỉnh cho phù hợp, xem [AWS Agentic AI Security Scoping Matrix](https://aws.amazon.com/ai/security/agentic-ai-scoping-matrix/) và [hướng dẫn xây dựng AI agent trong các môi trường GxP này](https://aws.amazon.com/blogs/machine-learning/a-guide-to-building-ai-agents-in-gxp-environments/).

Các cấp phép tin cậy bền vững (persistent trust grants), nơi một người rà soát phê duyệt một mẫu thao tác cụ thể một lần và các thao tác tương lai khớp với mẫu tiến hành mà không cần phê duyệt lại, là một van xả hữu ích cho các thao tác thực sự thường lệ, nhưng chúng dịch chuyển nơi phán đoán của con người được áp dụng từ khoảnh khắc-tới-khoảnh khắc sang thời điểm-cấp-phép. Nếu bạn hiện thực tin cậy bền vững, hãy giới hạn mỗi cấp phép vào một lệnh, hình dạng tham số hoặc tài nguyên cụ thể. Phân tầng các cấp phép theo rủi ro để các thao tác rủi ro cao hơn không đủ điều kiện cho tin cậy bền vững hoặc yêu cầu xác nhận lại theo một nhịp đã định, và làm cho bản thân các cấp phép có thể kiểm toán và thu hồi. Các cấp phép tin cậy dạng ký tự đại diện (wildcard) (phê duyệt mọi thao tác tương lai của một loại nhất định mà không giới hạn phạm vi tham số) thực chất loại bỏ sự giám sát của con người khỏi cả một lớp thao tác và không nên được phát hành.

Một khi bộ phân loại nói rằng cần phê duyệt của con người, hãy định tuyến yêu cầu tới cơ chế phê duyệt phù hợp với môi trường thực thi của agent. Ba mẫu bao phủ hầu hết các lần triển khai. Với các agent nhúng trong các khối công việc do step function điều khiển, mẫu callback .waitForTaskToken của [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) đưa vào một bước phê duyệt. Luồng công việc phát ra một task token và tạm dừng, token được chuyển tới một ứng dụng phê duyệt qua một kênh phù hợp với tập người rà soát (Amazon SNS tới một hàng đợi mà ứng dụng phê duyệt tiêu thụ, Amazon SES tới hộp thư của người rà soát, hoặc một điểm cuối webhook trên ứng dụng phê duyệt), ứng dụng trình bày quyết định cho người rà soát, và ứng dụng gọi SendTaskSuccess hoặc SendTaskFailure với task token nhân danh người rà soát. Người rà soát thường không gọi trực tiếp các API Step Functions. Ứng dụng phê duyệt giữ các thông tin xác thực, và người rà soát tương tác với ứng dụng. Xem [hướng dẫn phê duyệt của con người trong Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html) để có một ví dụ hoàn chỉnh.

Với các agent xây dựng trên [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html), hai mẫu dựng sẵn xử lý xác nhận human-in-the-loop mà không cần điều phối luồng công việc bên ngoài. [Xác nhận người dùng (user confirmation)](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html) tạm dừng agent trước khi thực thi một hàm cụ thể và trả về tên hàm và các giá trị tham số cho ứng dụng gọi để trình bày yes/no cho người dùng. [Trả về quyền kiểm soát (return of control, ROC)](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html) đi xa hơn bằng cách trả về chính lời gọi hàm để ứng dụng quyết định làm gì (trình bày cho người dùng, chạy kiểm định, chỉnh sửa tham số, hoặc từ chối). ROC được cấu hình ở cấp action group và bao phủ mọi hành động trong nhóm đó. Cả hai mẫu đều giả định ứng dụng là thành phần hiện thực trải nghiệm phê duyệt của con người. Những mẫu này phù hợp hơn cho các ca sử dụng tương tác nơi người dùng cuối của ứng dụng cũng là người phê duyệt, trong khi các mẫu callback Step Functions phù hợp với các luồng công việc bất đồng bộ có các vai trò người rà soát riêng.

Với các agent cần xử lý phê duyệt chạy dài, [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html) hỗ trợ cả xử lý đồng bộ và bất đồng bộ qua một API thống nhất, cho phép một agent bắt đầu một tác vụ có thể mất vài phút hoặc vài giờ, xác nhận yêu cầu ngay lập tức, tiếp tục các luồng công việc phê duyệt ở nền, và để người dùng quay lại kiểm tra kết quả sau. SDK cung cấp quản lý vòng đời tác vụ tường minh qua các API add_async_task và complete_async_task, theo dõi trạng thái xử lý và báo cáo tình trạng của agent qua điểm cuối /ping. Một agent báo cáo HealthyBusy khi các tác vụ phê duyệt nền đang tiến hành và Healthy khi rảnh. Điều này đặc biệt hữu ích cho các luồng công việc đồng thuận nhiều người rà soát nơi việc thu thập phê duyệt kéo dài các khoảng thời gian dài. Các thao tác chặn (blocking) như chờ phản hồi của người rà soát cần chạy trong các luồng riêng hoặc dùng các phương thức async để tránh chặn điểm cuối kiểm tra tình trạng, điều sẽ khiến phiên runtime chấm dứt sau 15 phút ping không phản hồi.

Người rà soát cần đủ ngữ cảnh để đưa ra các quyết định có hiểu biết mà không phải lội qua các log thô. Các quyết định liên quan đến suy luận của agent thường tạo ra một khối lượng lớn nội dung trung gian (prompt, đầu ra công cụ, tài liệu được truy xuất, phản hồi mô hình) quá nhiều để chuyển trong một payload thông báo và có thể được truy cập bởi những người rà soát không đăng nhập vào ứng dụng của agent. Hãy lưu ngữ cảnh quyết định đầy đủ trong kho lưu trữ bền vững như Amazon S3 trước khi gửi thông báo phê duyệt, bao gồm chuỗi suy luận của agent, hành động được đề xuất, các nguồn dữ liệu liên quan và các hậu quả tiềm tàng. Hãy làm ngữ cảnh khả dụng qua cùng giao diện được xác thực mà người rà soát dùng để phê duyệt hoặc từ chối. Khi người rà soát không có quyền truy cập UI của hệ thống phê duyệt (ví dụ, phê duyệt qua email), các presigned S3 URL với thời gian hết hạn ngắn cung cấp truy cập tạm thời tới tài liệu ngữ cảnh. Hãy cấu trúc ngữ cảnh để làm nổi bật các yếu tố quyết định then chốt.

Các chính sách timeout và các đường leo thang là riêng cho từng cơ chế phê duyệt. Trong Step Functions, TimeoutSeconds hoặc HeartbeatSeconds trên trạng thái task đang chờ token phê duyệt kích hoạt một chuyển tiếp timeout, và các mệnh đề Catch định tuyến các lần thực thi bị timeout tới một trạng thái leo thang (thông báo cho các người rà soát thứ cấp, leo thang lên cấp quản lý, hoặc mặc định về một dự phòng an toàn, thường là chặn thao tác). Xem [xử lý lỗi Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html) để biết chi tiết thuộc tính. Với các luồng xác nhận người dùng và ROC của Amazon Bedrock Agents, các timeout và leo thang được xử lý bởi ứng dụng gọi. Với các tác vụ async của AgentCore Runtime, các timeout Step Functions nền tảng áp dụng vì tác vụ async thường chờ một callback Step Functions hoặc một tín hiệu bên ngoài tương đương.

Các quyết định phê duyệt cần được ghi log phục vụ tuân thủ và kiểm toán. Hãy ghi lại danh tính người rà soát, các dấu thời gian thông báo và phản hồi, thao tác đang được rà soát, quyết định, và bất kỳ sự kiện leo thang nào. Step Functions phát ra lịch sử thực thi tới Amazon CloudWatch Logs khi ghi log được bật ở cấp luồng công việc (xem [ghi log Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/monitoring-logging.html)). Hãy bổ sung điều này bằng các log ở cấp ứng dụng từ ứng dụng phê duyệt để danh tính người rà soát và lý do quyết định được ghi lại cùng với các lời gọi SendTaskSuccess/SendTaskFailure. Với các agent dựa trên AgentCore, phân cấp phiên và trace của AgentCore Observability ghi lại các sự kiện phía agent và ghép với các log của ứng dụng phê duyệt để có một bản ghi đầy đủ. Hãy lưu giữ log nhất quán với các yêu cầu tuân thủ của bạn và AGENTSEC05-BP01.

### Các bước triển khai

- **Định nghĩa một bộ phân loại rủi ro xác định:** Ánh xạ các loại thao tác của agent tới các yêu cầu tầng phê duyệt (tự chủ, một người rà soát, nhiều người rà soát), kết hợp phân loại tĩnh với các tín hiệu động tại thời điểm yêu cầu, và hiện thực bộ phân loại như logic xác định thay vì một LLM.
- **Khớp cơ chế phê duyệt với môi trường thực thi:** Dùng các callback của [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) cho các agent do step function điều khiển, xác nhận người dùng hoặc trả về quyền kiểm soát của [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) cho các agent trên Amazon Bedrock Agents, và các tác vụ async của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html) cho các agent cần xử lý phê duyệt chạy dài, và hiện thực mẫu tương ứng cho mỗi tầng đòi hỏi phê duyệt của con người.
- **Giới hạn mọi cấp phép tin cậy bền vững:** Giới hạn phạm vi mỗi cấp phép một cách hẹp (lệnh, hình dạng tham số hoặc tài nguyên cụ thể), phân tầng các cấp phép theo rủi ro, và làm cho chúng có thể kiểm toán và thu hồi.
- **Lưu ngữ cảnh quyết định bền vững:** Ghi ngữ cảnh quyết định đầy đủ tới Amazon S3 trước khi gửi các thông báo phê duyệt, và làm ngữ cảnh khả dụng qua giao diện phê duyệt được xác thực hoặc qua các presigned URL ngắn hạn khi điều đó không khả thi.
- **Cấu hình các timeout với các dự phòng an toàn:** Hiện thực các chính sách timeout và đường leo thang cho từng cơ chế phê duyệt, với các hành động dự phòng an toàn (thường là chặn thao tác) khi không có người rà soát phản hồi trong cửa sổ đã định.
- **Ghi log mọi phê duyệt:** Ghi lại danh tính người rà soát, các dấu thời gian, thao tác đang được rà soát, quyết định và các sự kiện leo thang, căn chỉnh với các yêu cầu lưu giữ và tuân thủ của AGENTSEC05-BP01.
- **Rà soát các chỉ số luồng công việc định kỳ:** Tìm các mẫu gợi ý sự mệt mỏi của người rà soát hoặc các kém hiệu quả trong quy trình và điều chỉnh các ngưỡng tầng rủi ro tương ứng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh](agentsec04-bp01.md)
- [AGENTSEC07-BP01 Triển khai quản lý tải nhận thức](../7-agentsec07/agentsec07-bp01.md)
- [AGENTSEC07-BP03 Nhiều người rà soát cho các thao tác quan trọng](../7-agentsec07/agentsec07-bp03.md)

**Tài liệu liên quan:**

- [AWS Step Functions callback patterns](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html)
- [Human approval in Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html)
- [Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [Step Functions logging](https://docs.aws.amazon.com/step-functions/latest/dg/monitoring-logging.html)
- [Implement human-in-the-loop confirmation with Amazon Bedrock Agents](https://aws.amazon.com/blogs/machine-learning/implement-human-in-the-loop-confirmation-with-amazon-bedrock-agents/)
- [Amazon Bedrock Agents user confirmation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html)
- [Amazon Bedrock Agents return of control](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html)
- [Amazon Bedrock AgentCore Runtime asynchronous processing](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html)
- [AWS Agentic AI Security Scoping Matrix](https://aws.amazon.com/ai/security/agentic-ai-scoping-matrix/)
- [A guide to building AI agents in GxP environments](https://aws.amazon.com/blogs/machine-learning/a-guide-to-building-ai-agents-in-gxp-environments/)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon SNS](https://aws.amazon.com/sns/)
- [Amazon SES](https://aws.amazon.com/ses/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
