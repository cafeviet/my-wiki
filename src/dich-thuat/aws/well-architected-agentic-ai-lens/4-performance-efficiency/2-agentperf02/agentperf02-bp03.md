# AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency

Phần lớn tổng thời gian **latency** của một yêu cầu tác nhân được dùng để chờ suy luận Model, truy xuất, gọi **Tools**, và tra cứu bộ nhớ chứ không phải công việc CPU bên trong tiến trình tác nhân. Thực thi các thao tác độc lập đồng thời, tái dùng các kết nối và runtime ấm, và khử trùng lặp các tra cứu lặp lại trong một yêu cầu cắt giảm tổng latency mà không đổi Model hay prompt.

**Kết quả mong muốn:**

- Bạn có các thao tác độc lập trong một yêu cầu tác nhân thực thi đồng thời; thực thi tuần tự chỉ dành cho các thao tác có phụ thuộc dữ liệu thật sự.
- Bạn có các kết nối tới dịch vụ hạ nguồn, endpoint Model, API Tools, kho bộ nhớ, chỉ mục vector, được gộp (pooled) và tái dùng qua các yêu cầu thay vì thiết lập lại mỗi lần gọi.
- Bạn có các khởi động lạnh (cold start) của runtime được loại khỏi đường tới hạn hoặc bị giới hạn thông qua dung lượng cấp phát trước, làm-ấm-trước (pre-warming), hoặc các môi trường thực thi bền.
- Bạn có các tra cứu lặp lại trong một yêu cầu được giải quyết từ một cache phạm vi-yêu-cầu, để công việc trùng lặp không bị trả phí hai lần trong một lần gọi.

**Các phản mẫu thường gặp (anti-patterns):**

- Thực thi các thao tác độc lập tuần tự khi chúng không chia sẻ phụ thuộc dữ liệu, khiến tổng latency là tổng của các thời lượng thao tác thay vì thao tác chậm nhất.
- Thiết lập kết nối mới tới endpoint Model, API Tools, hoặc kho dữ liệu trên mỗi lần gọi, trả chi phí thiết lập kết nối và bắt-tay TLS trên đường tới hạn.
- Chạy mã tác nhân trên compute trả phạt khởi-động-lạnh trên đường tới hạn mà không có dung lượng cấp phát trước, làm-ấm-trước, hoặc một runtime bền để hấp thụ nó.
- Thực thi lại cùng một tra cứu nhiều lần trong một yêu cầu duy nhất, ví dụ lấy cùng một đoạn cơ sở tri thức hoặc hồ sơ người dùng qua các bước suy luận liên tiếp, mà không có cache phạm vi-yêu-cầu để khử trùng lặp công việc.
- Đưa vào song song hóa mà không tôn trọng giới hạn tốc độ hạ nguồn hoặc dung lượng connection pool, nên các lệnh gọi đồng thời bị throttle hoặc xếp hàng và phần thắng latency dự kiến trở thành latency thêm cộng lỗi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chồng lấp các thao tác độc lập khiến đường tới hạn bám theo thao tác chậm nhất thay vì tổng của mọi thao tác.
- Phân bổ đều chi phí thiết lập kết nối và khởi tạo runtime qua các yêu cầu tránh trả các chi phí đó trên mỗi lần gọi.
- Các lệnh gọi song song tôn trọng dung lượng hạ nguồn tránh throttling và bão-thử-lại mà song song hóa ngây thơ kích hoạt.
- Chồng lấp các chờ đợi I/O-bound, truy xuất và gọi Tools, với công việc compute-bound như suy luận và phân tích cú pháp giữ tác nhân hữu ích trong lúc chờ.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phần lớn tổng thời gian latency của một yêu cầu tác nhân được dùng để chờ, suy luận Model, truy xuất, gọi Tools, và tra cứu bộ nhớ, chứ không phải công việc CPU bên trong tiến trình tác nhân. Cấu trúc của cách các chờ đợi đó được kết hợp chi phối tổng latency hơn tốc độ của bất kỳ một phụ thuộc hạ nguồn nào. Bốn quyết định cấu trúc thường ảnh hưởng latency:

- Chạy các thao tác độc lập đồng thời thay vì tuần tự
- Tái dùng các kết nối và runtime ấm qua các lần gọi
- Loại các khởi động lạnh khỏi đường tới hạn
- Khử trùng lặp các tra cứu lặp lại trong một yêu cầu.

Mỗi quyết định độc lập với lựa chọn Model và prompt, nên các phần lợi cộng dồn với các tối ưu vòng-lặp-suy-luận và lựa-chọn-Model được đề cập ở nơi khác trong trụ cột này.

Đồng thời (concurrency) có tác động lớn nhất khi tác nhân tỏa ra qua các nguồn dữ liệu hoặc lệnh gọi Tools độc lập. Phân tích phụ thuộc nhận diện các thao tác không chia sẻ phụ thuộc dữ liệu (ví dụ một tra cứu cá nhân hóa và một truy vấn cơ sở tri thức phát ra từ cùng một bước suy luận, và thực thi chúng song song để latency của bước bằng thao tác chậm nhất thay vì tổng).

Các framework tác nhân phơi bày điều này trực tiếp. Strands Agents thực thi các lệnh gọi Tools độc lập phát ra trong một bước suy luận một cách đồng thời, và các trình điều phối dựa-trên-đồ-thị như LangGraph tỏa ra qua các cạnh độc lập. Ràng buộc là dung lượng hạ nguồn, nơi các lệnh gọi Model đồng thời và gọi Tools phải tôn trọng [hạn ngạch dịch vụ Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) (số-yêu-cầu-mỗi-phút và số-token-mỗi-phút) cùng giới hạn tốc độ API Tools, nếu không song song hóa chuyển thành throttling và bão-thử-lại làm mất phần thắng latency.

Tái dùng kết nối và loại khởi-động-lạnh xử lý các chi phí thiết lập mỗi-lần-gọi cộng dồn với đồng thời. Các kết nối HTTP tới endpoint Model và API Tools nên bền qua các lần gọi thông qua connection pool của SDK hoặc HTTP-client thay vì mở và đóng mỗi yêu cầu. Mỗi kết nối mới trả chi phí bắt-tay-TLS và thiết-lập-kết-nối trên đường tới hạn mà một kết nối được gộp tránh hoàn toàn, và chi phí đó tích lũy qua fan-out và qua các lần gọi.

Kết nối cơ sở dữ liệu tuân theo cùng nguyên tắc. [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html) gộp kết nối tới Aurora và RDS để các tác nhân serverless không cạn giới hạn kết nối cơ sở dữ liệu hoặc trả latency thiết-lập-kết-nối mỗi lần gọi. Tại runtime, [các phiên Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html) tái dùng một microVM chuyên dụng qua các lần gọi cùng chia sẻ một định danh phiên, việc này loại khởi-động-lạnh trong khi một phiên đang hoạt động và bảo toàn trạng thái trong-bộ-nhớ qua các bước suy luận.

Với các tác nhân host trên AWS Lambda, [đồng thời cấp phát trước của Lambda](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) khởi tạo trước các môi trường thực thi và [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) khôi phục từ một snapshot được cache trên các runtime được hỗ trợ, giảm latency lần-gọi-đầu xuống dưới một giây với cái giá là dung lượng liên tục hoặc phí mỗi-lần-khôi-phục.

Caching phạm vi-yêu-cầu xử lý công việc dư thừa xảy ra bên trong một lần gọi duy nhất thay vì qua các lần gọi. Một vòng lặp suy luận gọi cùng một Tool hai lần, truy xuất cùng một đoạn qua các bước liên tiếp, hoặc lấy lại cùng một hồ sơ người dùng ở trình lập kế hoạch và trình thực thi lãng phí ngân sách latency vào I/O lặp lại. Một cache khóa theo định danh yêu cầu hoặc phiên khử trùng lặp các tra cứu này cho phần còn lại của yêu cầu mà không có sự phức tạp về tính nhất quán của một cache liên-yêu-cầu.

Phạm vi được thu hẹp có chủ đích, các cache bền và liên-yêu-cầu như prompt caching của Amazon Bedrock và các semantic cache là các tối ưu cấp-cao-hơn được đề cập trong các thực hành tốt tập trung vào ngữ cảnh và bộ nhớ. Tuy nhiên, khử trùng lặp phạm vi-yêu-cầu thường là tối ưu caching rủi-ro-thấp-nhất sẵn có, vì cache bị hủy vào cuối lần gọi và không thể phục vụ dữ liệu cũ cho một yêu cầu tiếp theo.

### Các bước triển khai

- **Profile đường tới hạn để nhận diện các thao tác có thể song song hóa:** Truy vết một mẫu đại diện các yêu cầu production bằng telemetry hiệu năng đã có để phân rã mỗi lần gọi thành các thời lượng và phụ thuộc theo thao tác. Nhận diện các thao tác không chia sẻ phụ thuộc dữ liệu, các lệnh gọi Tools riêng, truy xuất độc lập, tra cứu cá nhân hóa cạnh truy vấn tri thức, và đánh dấu các đoạn tuần tự nơi đồng thời sẽ dồn latency đồng-hồ-treo-tường về thao tác chậm nhất. Xem lại bản kiểm kê khi prompt và Tools thay đổi, vì đồ thị phụ thuộc dịch chuyển theo chúng.
- **Thực thi các thao tác độc lập đồng thời trong giới hạn dung lượng hạ nguồn:** Cấu hình framework tác nhân để tỏa ra các lệnh gọi Tools và truy xuất độc lập trong cùng một bước suy luận, Strands Agents, LangGraph, và các framework tương tự phơi bày điều này như một nguyên hàm nguyên bản. Giới hạn đồng thời theo dung lượng của dịch vụ hạ nguồn, [hạn ngạch dịch vụ Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html), giới hạn tốc độ API Tools, và trần kết nối cơ sở dữ liệu, để một bước tỏa ra 10 lệnh gọi đồng thời không kích hoạt throttling tốn nhiều latency hơn phần tiết kiệm.
- **Tái dùng các kết nối tới endpoint Model và API bên ngoài qua các lần gọi:** Cấu hình connection pool của HTTP client để các phiên TLS tới Amazon Bedrock và API Tools bền qua các lần gọi thay vì thiết lập lại mỗi yêu cầu. Trên các runtime bảo toàn bộ nhớ qua các lần gọi, [các môi trường thực thi AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html), các dịch vụ dựa-trên-container, và các dịch vụ chạy-dài, khởi tạo client một lần cho mỗi môi trường thực thi thay vì mỗi lần gọi để connection pool của nó tồn tại qua các lệnh gọi. Một lần gọi ấm nên trả zero latency thiết-lập-kết-nối trên các lệnh gọi hạ nguồn.
- **Gộp các kết nối cơ sở dữ liệu qua một connection pool được quản lý:** Với các tác nhân đọc từ hoặc ghi vào dữ liệu quan hệ, đặt [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html) trước các cơ sở dữ liệu Aurora và RDS để các lần gọi serverless chia sẻ một pool kết nối có giới hạn thay vì mở một kết nối mới mỗi lần. Không có bộ gộp, các lần gọi tác nhân đồng thời cạn trần kết nối của cơ sở dữ liệu và trả latency thiết lập mỗi-lần-gọi trên đường tới hạn, cả hai chế độ lỗi đều tệ hơn khi song song hóa tăng.
- **Loại các khởi động lạnh khỏi runtime thực thi tác nhân:** Chọn một runtime giữ môi trường thực thi của tác nhân ấm trên đường tới hạn. [Các phiên Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html) tái dùng một microVM chuyên dụng qua các lần gọi cùng chia sẻ một định danh phiên, bảo toàn trạng thái trong-bộ-nhớ và tránh khởi-động-lạnh mỗi-lần-gọi trong khi phiên đang hoạt động. Với các tác nhân host trên Lambda, [đồng thời cấp phát trước của Lambda](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) khởi tạo trước các môi trường thực thi và [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) khôi phục từ một snapshot được cache trên các runtime được hỗ trợ. Các dịch vụ container luôn-bật như Amazon ECS hoặc Amazon EKS tránh khởi-động-lạnh hoàn toàn với cái giá là dung lượng liên tục. Chọn dựa trên hình dạng lưu lượng thay vì sở thích runtime.
- **Khử trùng lặp các tra cứu lặp lại trong một yêu cầu bằng một cache phạm vi-yêu-cầu:** Thêm một cache trong-bộ-nhớ có phạm vi theo vòng đời của yêu cầu hoặc phiên ghi nhớ (memoize) các tra cứu idempotent, phản hồi Tools, đoạn được truy xuất, đọc hồ-sơ-người-dùng, khóa theo đầu vào. Một vòng lặp suy luận gọi cùng một Tool hai lần hoặc truy xuất cùng một đoạn qua các bước liên tiếp giải quyết lệnh gọi thứ hai từ cache, phục hồi latency đó mà không có sự phức tạp về tính nhất quán của một cache liên-lần-gọi. Cache bị hủy vào cuối yêu cầu, nên nó không thể phục vụ dữ liệu cũ cho một lần gọi tiếp theo.
- **Đo lại đường tới hạn sau mỗi thay đổi cấu trúc và khi lưu lượng tăng:** Sau khi áp dụng các thay đổi đồng thời, gộp, khởi-động-lạnh, hoặc caching, profile lại đường tới hạn dưới tải production đại diện để xác nhận tối ưu giữ vững và không đưa vào các chế độ lỗi mới như throttling hoặc bão hòa connection pool. Lặp lại phép đo khi lưu lượng tăng, vì song song hóa được giới hạn đúng lúc ra mắt thường vượt hạn ngạch ở quy mô cao hơn và profile latency âm thầm hồi quy trước khi một SLO bị vượt.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](../1-agentperf01/agentperf01-bp03.md)
- [AGENTPERF02-BP02 Triển khai chiến lược lựa chọn Model phù hợp tác vụ](agentperf02-bp02.md)
- [AGENTPERF02-BP04 Tối ưu phản hồi streaming và time-to-first-token cho các tương tác tác nhân](agentperf02-bp04.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](../3-agentperf03/agentperf03-bp04.md)

**Tài liệu liên quan:**

- [Hạn ngạch dịch vụ Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)
- [Các phiên Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html)
- [Suy luận tối-ưu-latency của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html)
- [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [Các môi trường thực thi AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)
- [Đồng thời cấp phát trước của AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html)
- [AWS Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
- [Xây dựng kiến trúc serverless cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/introduction.html)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon RDS Proxy](https://aws.amazon.com/rds/proxy/)
