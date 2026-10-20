# AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định

Các quyết định của agent chỉ có thể kiểm toán được nếu suy luận đằng sau chúng được ghi lại, được bảo tồn nguyên vẹn, và có thể tiếp cận được ở tốc độ mà các cuộc điều tra thực sự diễn ra. Lưu trữ tạo phẩm có bằng chứng chống can thiệp, quy kết về trigger gốc, và một chỉ mục có thể truy vấn biến khối lượng log thô thành năng lực điều tra pháp chứng.

**Kết quả mong muốn:**

- Bạn ghi lại mọi quyết định, hành động và bước suy luận của agent vào kho lưu trữ có bằng chứng chống can thiệp, có thể truy vấn, tạo ra một bản ghi hành vi agent đầy đủ và có thể kiểm chứng.
- Mỗi hành động được ghi log bao gồm quy kết về nguồn khởi tạo (một phiên người dùng con người, một sự kiện ngược dòng, một lịch, hay một agent khác), nên các hành động được ghi log thường có thể truy ngược tới thứ đã kích hoạt chúng.
- Bạn có thể tái dựng toàn bộ quá trình ra quyết định cho bất kỳ hành động nào của agent từ các tạo phẩm được lưu, độc lập với lời tường thuật của chính agent về suy luận của nó.
- Kiểm chứng bằng mật mã xác minh tính toàn vẹn của log, vai trò IAM vận hành của agent không thể chỉnh sửa hay xóa lịch sử quyết định của chính nó, và dữ liệu nhạy cảm (PII, bí mật, các trường được quản chế) được che hoặc lược bỏ trước khi log được ghi vào kho lưu trữ dài hạn.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ ghi log các đầu ra cuối cùng của agent mà không có suy luận trung gian, các lần gọi công cụ, hay các điểm quyết định, khiến việc tái dựng sự cố trở nên bất khả.
- Lưu log và tạo phẩm quyết định trong kho lưu trữ có thể thay đổi mà không có bảo vệ ghi-một-lần (write-once), nên log có thể bị xóa hoặc chỉnh sửa về sau.
- Lưu tạo phẩm quyết định trong cùng tài khoản và với cùng quyền hạn như các tài nguyên vận hành của agent, để cho một agent bị ảnh hưởng chỉnh sửa hoặc xóa lịch sử của chính nó.
- Lưu giữ các tạo phẩm mà không có một chỉ mục có thể truy vấn, nên việc quét các đối tượng S3 thô trở nên không thực tế trong các cuộc điều tra nhạy về thời gian.

**Lợi ích khi áp dụng thực hành tốt này:**

- Việc ghi log chi tiết các chuỗi suy luận, các lần gọi công cụ và các bước trung gian, được lưu độc lập với các tài nguyên vận hành của agent, hỗ trợ việc tái dựng hành vi của agent trong các cuộc điều tra.
- Amazon S3 Object Lock và kiểm chứng tệp log AWS CloudTrail cung cấp chứng minh bằng mật mã về tính toàn vẹn của log phục vụ mục đích tuân thủ và pháp chứng.
- Các kho tạo phẩm có thể truy vấn hỗ trợ phân tích hành vi hồi cứu làm nổi bật các mẫu bị các cảnh báo thời gian thực bỏ sót.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Việc ghi log cho agent có ba yêu cầu cứng mà việc ghi log ứng dụng thông thường không có:

- Tính đầy đủ (chuỗi suy luận, không chỉ các đầu ra)
- Tính bất biến (agent mà bạn đang điều tra hành vi của nó không thể là thực thể kiểm soát log của chính nó)
- Khả năng truy vấn ở tốc độ điều tra (các lần quét S3 không đủ nhanh khi từng phút quan trọng)

Mỗi yêu cầu đó định hình một phần khác nhau của kiến trúc.

Hãy bắt đầu với lớp gọi mô hình. Bật ghi log lần gọi mô hình Amazon Bedrock để thu mọi yêu cầu và phản hồi suy luận (prompt đầu vào, đầu ra mô hình, số lượng token, các chỉ số độ trễ) với việc chuyển tới Amazon CloudWatch Logs cho giám sát vận hành và Amazon S3 cho lưu giữ dài hạn. Vì các prompt của agent và các đầu ra của mô hình thường chứa PII, bí mật hoặc dữ liệu được quản chế, hãy áp dụng bảo vệ dữ liệu trước khi nội dung đáp xuống kho lưu trữ dài hạn. [Các chính sách bảo vệ dữ liệu Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html) tự động phát hiện và che các loại nhạy cảm (thông tin xác thực, định danh cá nhân, dữ liệu tài chính) trong các sự kiện log. Các bộ lọc thông tin nhạy cảm của [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) ẩn danh hoặc lược bỏ PII trong các prompt đầu vào và các phản hồi mô hình tại thời điểm suy luận, nhưng đó khác với những gì log thu lại. Hãy kiểm chứng hành vi che trên từng đích đang dùng (Amazon Bedrock Model Invocation Logs, AgentCore Observability, CloudWatch Logs, kho tạo phẩm S3) và thêm việc che tại thời điểm ghi trong mã của agent bất cứ nơi nào nguồn không tự che.

Các tạo phẩm quyết định đòi hỏi một ranh giới tin cậy riêng. Hãy tạo một bucket S3 riêng trong một tài khoản AWS tách biệt với versioning được bật, và dùng các bucket policy cho phép ghi từ tài khoản agent nhưng từ chối các thao tác delete và overwrite. Điều đó cho bạn một kho tạo phẩm chỉ-thêm mà vai trò IAM vận hành của agent không thể can thiệp. Một lược đồ khóa nhất quán (ID agent, ID phiên, dấu thời gian, loại quyết định) làm cho việc truy xuất có thể dự đoán trong các cuộc điều tra. Hãy ghi lại bên khởi tạo trên mọi quyết định. Một agent có thể được gọi bởi:

- Một phiên người dùng con người
- Một sự kiện Amazon EventBridge
- Một thông điệp Amazon SQS
- Một cảnh báo Amazon CloudWatch
- Một quy tắc theo lịch
- Một agent khác

Hãy ghi log các định danh mô tả trigger (phiên IAM hoặc người dùng Amazon Cognito cho các yêu cầu của con người, nguồn sự kiện và ID sự kiện cho các sự kiện, ARN cảnh báo cho các cảnh báo, các ID agent gọi và phiên cho các lời gọi giữa các agent) dưới dạng các trường có cấu trúc để các truy vấn điều tra có thể lọc theo nguồn trigger.

Để có bằng chứng chống can thiệp trên chính bucket, hãy mặc định về các bucket policy từ chối delete và overwrite, MFA delete trên bucket, và versioning. Nơi các yêu cầu tuân thủ đòi hỏi các đảm bảo mạnh hơn, hãy cân nhắc bật Amazon S3 Object Lock ở chế độ governance, cho phép người dùng có các quyền IAM cụ thể ghi đè các thiết lập lưu giữ khi cần. Chế độ compliance giúp ngăn bất kỳ người dùng nào (kể cả tài khoản root) xóa hoặc rút ngắn các kỳ lưu giữ trong suốt thời gian khóa. Một khi được cấu hình, chế độ này không thể đảo ngược, và một sai cấu hình về kỳ hoặc phạm vi lưu giữ có thể khiến khách hàng không thể xóa dữ liệu mà họ cần xóa (ví dụ, để đáp ứng các yêu cầu quyền-được-lãng-quên). Chỉ dùng chế độ compliance khi có một yêu cầu quy định cụ thể cho nó, và kiểm chứng cấu hình lưu giữ với dữ liệu thử đại diện trước khi áp dụng rộng rãi.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html) ghi lại các chuỗi suy luận, các lần gọi công cụ và các tạo phẩm quyết định của agent một cách tự động cho các agent chạy trên AgentCore Runtime. Phân cấp phiên, trace và span ghi lại các bước suy luận, các lời gọi công cụ với đầu vào và đầu ra, và các thao tác bộ nhớ. AgentCore xuất dữ liệu span cho các tài nguyên bộ nhớ theo mặc định và công bố các chỉ số ở cấp phiên có thể xem trên trang generative AI observability của Amazon CloudWatch. Với các tạo phẩm cần lưu giữ vượt ra ngoài cửa sổ khả năng quan sát mặc định hoặc cần các kiểm soát tuân thủ cụ thể, hãy ghi ngữ cảnh quyết định đầy đủ tới kho tạo phẩm S3 riêng tại mỗi điểm quyết định đáng kể. AWS Distro for OpenTelemetry (ADOT) mở rộng độ bao phủ với các chỉ số, log và span tùy chỉnh trong mã của agent.

[Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) bổ trợ cho việc ghi log bằng cách liên tục chấm điểm hành vi của agent về độ đúng đắn, tính hữu ích, độ chính xác lựa chọn công cụ và độ an toàn. Kết quả được công bố tới Amazon CloudWatch cùng với dữ liệu khả năng quan sát để có một khung nhìn thống nhất, và các cảnh báo Amazon CloudWatch về điểm đánh giá phát hiện trôi dạt hành vi ngoài các ngưỡng chấp nhận được.

Bằng chứng chống can thiệp ở cấp dấu vết kiểm toán dùng AWS CloudTrail với kiểm chứng tệp log trên mọi tài khoản và region nơi agent hoạt động. Kiểm chứng tệp log tạo ra các hash SHA-256 và chữ ký RSA trong một tệp digest xác minh rằng các tệp log chưa bị chỉnh sửa, xóa hay giả mạo sau khi chuyển. Một bucket S3 riêng với các kiểm soát truy cập xuyên tài khoản giúp ngăn vai trò IAM của chính agent chỉnh sửa hoặc xóa log.

Amazon Athena với AWS Glue Data Catalog làm cho kho tạo phẩm quyết định có thể truy vấn: một AWS Glue crawler quét bucket tạo phẩm S3 và tạo các bảng trong Data Catalog dựa trên lược đồ tạo phẩm, và Athena chạy các truy vấn SQL trực tiếp trên S3 mà không cần nạp dữ liệu vào một cơ sở dữ liệu riêng. Các truy vấn điều tra như "tìm mọi quyết định được thực hiện bởi agent X có liên quan tới công cụ Y giữa các ngày A và B" trở nên rẻ để chạy. Hãy ghi tài liệu các truy vấn điều tra tiêu chuẩn cho các kịch bản bảo mật phổ biến để các điều tra viên có thể làm việc ngay lập tức trong một sự cố. Mẫu này (log tới Amazon S3, được ghi mục lục bởi AWS Glue, truy vấn bằng Amazon Athena) là một cách tiếp cận phân tích log pháp chứng đã được thiết lập, được khuyến nghị trong AWS Well-Architected Security Pillar.

Một chính sách vòng đời (lifecycle policy) giữ chi phí lưu trữ tỷ lệ với các mẫu truy cập. Log nóng cư trú trong Amazon CloudWatch Logs cho giám sát vận hành (30 đến 90 ngày), chuyển tiếp sang Amazon S3 Standard cho lưu giữ trung hạn (1 đến 2 năm), và lưu trữ vào Amazon Glacier cho lưu giữ tuân thủ dài hạn (7+ năm). Hãy gắn thẻ các đối tượng bằng metadata phân loại dữ liệu và chính sách lưu giữ để các chuyển tiếp vòng đời được tự động hóa.

### Các bước triển khai

- **Bật ghi log lần gọi mô hình Amazon Bedrock:** Bật ghi log lần gọi mô hình Amazon Bedrock và chuyển tới cả Amazon CloudWatch Logs lẫn Amazon S3.
- **Che dữ liệu nhạy cảm trước khi nó đáp xuống kho lưu trữ dài hạn:** Cấu hình các chính sách bảo vệ dữ liệu Amazon CloudWatch Logs, kiểm chứng hành vi che trên mọi đích ghi log đang dùng, và thêm việc che tại thời điểm ghi trong mã của agent nơi đích không tự che.
- **Tạo một bucket tạo phẩm riêng, chỉ-thêm trong một tài khoản Log Archive:** Tạo một bucket Amazon S3 trong một tài khoản Log Archive tách biệt, căn chỉnh với [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html), với versioning được bật và các kiểm soát truy cập xuyên tài khoản cho phép agent ghi nhưng từ chối các thao tác delete và overwrite.
- **Chọn một mô hình bảo vệ lưu giữ:** Mặc định về bảo vệ dựa trên bucket policy (từ chối delete, từ chối overwrite, MFA delete, versioning). Đánh giá Amazon S3 Object Lock ở chế độ governance nơi tuân thủ đòi hỏi các đảm bảo mạnh hơn, và dành chế độ compliance cho các trường hợp có yêu cầu quy định cụ thể cho nó sau khi kiểm chứng phạm vi và thời lượng lưu giữ với dữ liệu thử đại diện.
- **Thu các trace đầy đủ qua AgentCore Observability:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html) để thu các trace thực thi agent đầy đủ, và với các tạo phẩm cần lưu giữ lâu hơn hoặc cần các kiểm soát tuân thủ, hãy ghi ngữ cảnh quyết định đầy đủ tới kho tạo phẩm S3 riêng tại mỗi điểm quyết định đáng kể.
- **Ghi lại các thuộc tính bên khởi tạo trên mọi tạo phẩm:** Thu phiên con người, nguồn sự kiện và ID sự kiện, ARN cảnh báo, ARN quy tắc lịch, ID agent gọi và các định danh tương tự dưới dạng các trường có cấu trúc trên các tạo phẩm quyết định và các mục log.
- **Áp dụng một lược đồ khóa tạo phẩm nhất quán:** Dùng `agentId`, `sessionId`, `timestamp` và `decisionType` làm lược đồ khóa để truy xuất hiệu quả trong các cuộc điều tra.
- **Triển khai AgentCore Evaluations với các cảnh báo trôi dạt:** Triển khai [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) với các trình đánh giá dựng sẵn và tùy chỉnh, công bố kết quả tới Amazon CloudWatch, và cấu hình các cảnh báo trên điểm đánh giá để phát hiện trôi dạt hành vi.
- **Bật kiểm chứng tệp log CloudTrail:** Bật AWS CloudTrail với kiểm chứng tệp log trên mọi tài khoản và region, lưu log trong một bucket S3 riêng với các kiểm soát truy cập xuyên tài khoản.
- **Làm cho các tạo phẩm có thể truy vấn bằng Athena và AWS Glue:** Thiết lập một AWS Glue crawler để quét bucket tạo phẩm S3 và tạo các bảng trong Data Catalog, dùng Amazon Athena để truy vấn các tạo phẩm trực tiếp trên S3, và ghi tài liệu các truy vấn điều tra tiêu chuẩn cho các kịch bản bảo mật phổ biến.
- **Hiện thực lưu giữ phân tầng với tự động hóa:** Định nghĩa các tầng lưu giữ (CloudWatch Logs cho giám sát vận hành, S3 Standard cho trung hạn, Amazon Glacier cho tuân thủ dài hạn) với các chuyển tiếp vòng đời tự động và gắn thẻ phân loại dữ liệu.
- **Mã hóa mọi kho lưu trữ log và tạo phẩm:** Dùng các khóa AWS KMS do khách hàng quản lý với xoay vòng khóa được bật trên mọi đích ghi log.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người](../3-agentsec03/agentsec03-bp02.md)
- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](../4-agentsec04/agentsec04-bp02.md)
- [AGENTSEC05-BP02 Triển khai truy vết phân tán cho các tương tác của agent](agentsec05-bp02.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và hỗ trợ phục hồi](../../3-reliability/7-agentrel07/agentrel07-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [AgentCore Observability: Sessions, traces, and spans](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
- [AWS CloudTrail log file validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)
- [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [Amazon CloudWatch Logs data protection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html)
- [Tài liệu Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [Querying AWS service logs with Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-aws-service-logs.html)
- [Create a customizable cross-company log lake for compliance (AWS Big Data Blog)](https://aws.amazon.com/blogs/big-data/create-a-customizable-cross-company-log-lake-part-ii-build-and-add-amazon-bedrock/)
- [AWS Well-Architected Security Pillar SEC04-BP01: Configure service and application logging](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_app_service_logging.html)
- [Considerations for addressing the core dimensions of responsible AI for Amazon Bedrock applications](https://aws.amazon.com/blogs/machine-learning/considerations-for-addressing-the-core-dimensions-of-responsible-ai-for-amazon-bedrock-applications/)
- [Security reference architecture for generative AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/gen-ai-sra.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon Athena](https://aws.amazon.com/athena/)
- [AWS Glue](https://aws.amazon.com/glue/)
- [AWS Key Management Service](https://aws.amazon.com/kms/)
