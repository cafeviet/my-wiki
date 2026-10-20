# AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu

Yếu tố đóng góp chi phối vào **latency** tác nhân thay đổi theo loại tác vụ: một yêu cầu hỏi-đáp đơn giản có thể bị giới hạn bởi suy luận (inference-bound), một yêu cầu nặng-truy-xuất có thể bị giới hạn bởi truy xuất (retrieval-bound), và một luồng công việc đa tác nhân có thể bị giới hạn bởi điều phối (coordination-bound). Không phân rã tổng latency thành các đóng góp theo từng pha, các nhóm tối ưu các điểm nghẽn được phỏng đoán thay vì các điểm nghẽn đo được, và công sức kỹ thuật rơi vào công việc không làm dịch chuyển hiệu năng cho người dùng.

**Kết quả mong muốn:**

- Bạn có một profile latency cho mọi khối công việc tác nhân, phân rã latency thành các đóng góp theo từng pha, với pha chi phối được nhận diện và nhắm tới để tối ưu.
- Các nhóm của bạn chẩn đoán vấn đề hiệu năng bằng cách xem xét sự phân tách theo pha thay vì phỏng đoán thành phần nào chậm.
- Bạn có các cảnh báo hồi quy theo pha, kích hoạt khi có độ trôi cấp-pha trước khi mục tiêu mức dịch vụ đầu-cuối bị vượt.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ đo tổng latency mà không phân rã thành các pha, khiến không thể biết sự chậm chạp do suy luận, truy xuất, gọi Tools, hay chi phí điều phối gây ra.
- Tối ưu latency suy luận (lựa chọn Model, nén prompt) trong khi điểm nghẽn thực sự là latency truy xuất hoặc gọi Tools, lãng phí công sức kỹ thuật vào một pha đóng góp một phần nhỏ tổng thời gian.
- Profiling dưới điều kiện kiểm thử tổng hợp mà không xác nhận đối chiếu các mẫu lưu lượng production, bỏ sót các điểm nghẽn chỉ xuất hiện dưới tải đồng thời.

**Lợi ích khi áp dụng thực hành tốt này:**

- Khả năng thấy cấp-pha hướng công sức kỹ thuật vào điểm nghẽn thực sự thay vì các điểm nghẽn được phỏng đoán.
- Giám sát xu hướng theo pha chỉ chính xác pha nào đã suy giảm, khiến các hồi quy latency được chẩn đoán nhanh hơn.
- Các profile pha trước-và-sau xác nhận rằng một tối ưu thực sự thu nhỏ pha đã nhắm mà không làm hồi quy các pha khác.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Profiling một tác nhân là thao tác tổng hợp telemetry dựa-trên-span mà pipeline suy luận đã phát ra thành các đóng góp theo từng pha, rồi hỏi pha nào chi phối ngân sách. Việc phân rã là một phép nhóm trên dữ liệu trace hiện có, với điều kiện mọi span ánh xạ sạch tới một pha trong một phân loại chung. Khi ánh xạ đó mơ hồ, một span duy nhất bao cả truy xuất lẫn định dạng đầu ra, hoặc một vòng lặp suy luận ẩn giấu một lệnh gọi Tools nội tuyến, profile trở nên không đáng tin và các quyết định tối ưu trôi dạt. Việc chuẩn bị nằm ở định nghĩa các pha một lần, căn chỉnh các loại span theo chúng, và làm ánh xạ hiển thị với mọi nhóm đóng góp cho tác nhân.

Pha chi phối thay đổi theo khối công việc và dịch chuyển theo thời gian. Ví dụ:

- Một tác nhân hỏi-đáp hội thoại thường bị giới hạn bởi suy luận (inference-bound)
- Một tác nhân nặng-truy-xuất đọc trên nhiều cơ sở tri thức có thể bị giới hạn bởi truy xuất (retrieval-bound)
- Một luồng công việc đa tác nhân bàn giao ngữ cảnh tuần tự giữa supervisor và worker thường bị giới hạn bởi điều phối (coordination-bound)
- Một tác nhân gọi các API bên ngoài có thể bị giới hạn bởi Tools (tool-bound) khi một dịch vụ hạ nguồn suy giảm

Tối ưu sai pha không tạo ra cải thiện đo được nào cho người dùng. Ví dụ, tăng tốc suy luận 30% là vô hình khi suy luận chiếm 10% ngân sách và truy xuất chiếm 60%. Quy trách nhiệm cấp-pha giúp ngăn việc nhắm sai đó, và nó vẫn cần thiết ngay cả sau khi một khối công việc đã được tinh chỉnh vì pha chi phối lúc ra mắt hiếm khi giữ vị trí chi phối sau khi prompt, Tools, và Model tiến hóa.

Tính profile ở cấp phân phối, không phải giá trị trung bình. Trung bình che giấu phần đuôi, và latency đuôi là cái người dùng trải nghiệm khi một tác nhân cảm thấy chậm. Tính p50, p90, và p99 cho mỗi pha riêng biệt, và cho tổng latency. Pha chi phối ở trung vị thường không phải pha chi phối ở p99, vì phần đuôi chậm thường tập trung ở một hoặc hai pha, suy luận trong lúc Model bị throttling, truy xuất trong lúc dựng lại chỉ mục hoặc cache lạnh, gọi Tools trong lúc dịch vụ hạ nguồn gặp sự cố. Một profile chỉ báo cáo trung bình theo pha có thể chỉ nhóm vào sai mục tiêu, vì pha gây hại người dùng ở phần đuôi thường nhỏ hơn pha chi phối trung bình.

Chạy profiling đối chiếu các mẫu lưu lượng production để có kết quả đáng tin. Kiểm thử tải tổng hợp có thể luyện đường yêu cầu, nhưng chúng hiếm khi tái tạo các phân phối prompt, các hành vi lựa-chọn-Tools, và các mẫu đồng thời mà người dùng thực tạo ra. Điều này nghĩa là các điểm nghẽn chỉ xuất hiện dưới tranh chấp vẫn vô hình, như bỏ đói thread-pool trong lúc fan-out, các đợt trượt-cache sau khi warmup hết hạn, hoặc xếp hàng trong các endpoint suy luận dùng chung.

Với [Amazon CloudWatch Transaction Search](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html) nạp 100% span tới log group aws/spans, bạn có thể tái dựng một profile production từ lưu lượng thực bằng các truy vấn [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) trên các thời lượng span mà không cần dựng hạ tầng profiling chuyên biệt. Tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) tạo dữ liệu span tương thích một cách tự động khi bật AgentCore Observability, và tác nhân trên Amazon ECS, Amazon EKS, AWS Lambda, hay hạ tầng tự vận hành tạo nó qua bộ thu [AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/introduction), nên cả hai nhóm cùng chia sẻ một bề mặt duy nhất.

Xếp hạng mục tiêu tối ưu theo đóng góp nhân với biến thiên có thể xử lý được (addressable variance), không theo đóng góp một mình. Một pha đóng góp 40% ngân sách nhưng đã gần sàn lý thuyết của nó thì có ít dư địa hơn một pha đóng góp 25% nhưng có biến thiên cao do lựa chọn triển khai, truy xuất tuần tự có thể song song hóa, hoặc các lệnh gọi Tools có thể cache.

Profiling cũng giúp phát hiện hồi quy theo pha. Một khi có phân phối đường cơ sở cho mỗi pha, cảnh báo [phát hiện bất thường Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) kích hoạt khi một pha trôi ra ngoài dải kỳ vọng trước khi thay đổi hiện lên trong SLO, để các hồi quy được quy về đúng pha vi phạm ngay tại thời điểm cảnh báo thay vì trong lúc hồi cứu sự cố.

### Các bước triển khai

- **Định nghĩa phân loại pha cho khối công việc:** Liệt kê các pha cấu thành việc thực thi đầu-cuối, xử lý đầu vào, truy xuất ngữ cảnh và bộ nhớ, suy luận LLM, gọi Tools, sinh hoặc stream đầu ra, và điều phối liên tác nhân, và ánh xạ mọi loại span mà tác nhân phát ra tới đúng một pha, căn chỉnh thuộc tính span theo [các quy ước ngữ nghĩa AI tạo sinh của OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Ghi tài liệu phân loại để mọi nhóm đóng góp span nhóm chúng theo cùng cách, và thêm các pha riêng của khối công việc như đánh giá guardrail hay hậu-xử-lý đầu-ra-có-cấu-trúc khi chúng nằm ngoài tập chung.
- **Tổng hợp span thành các chỉ số thời lượng theo pha:** Suy ra thời lượng theo pha từ log group span bằng các truy vấn [CloudWatch Transaction Search](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html) và [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) cộng thời lượng span nhóm theo pha và trace, rồi phát kết quả dưới dạng [chỉ số tùy chỉnh CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) với một kích thước pha. Công bố profile dưới dạng chỉ số, thay vì chỉ như các truy vấn log tùy biến, cho phép cùng tín hiệu chảy vào bảng điều khiển, cảnh báo, và phát hiện bất thường bên cạnh các chỉ số runtime nguyên bản.
- **Tính profile cấp-phân-vị cho mọi pha:** Tính p50, p90, và p99 cho mỗi pha và cho latency đầu-cuối trên một cửa sổ trượt khớp với khoảng thời gian của mục tiêu mức dịch vụ, và hiển thị các phân vị cạnh nhau. Pha chi phối ở trung vị thường không phải pha chi phối ở p99, và profiling chỉ theo trung bình che giấu phần đuôi nơi sự chậm mà người dùng cảm nhận tập trung.
- **Trực quan hóa đóng góp của mỗi pha vào latency đầu-cuối:** Xây dựng một góc nhìn đóng-góp-theo-pha dạng chồng (stacked) trên một [bảng điều khiển CloudWatch tùy chỉnh](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create_dashboard.html) dùng các chỉ số theo pha phát ở bước trước, và dùng [biến bảng điều khiển](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_dashboard_variables.html) để xoay cùng góc nhìn qua tập kích thước chuẩn, agent ID, workflow, môi trường, loại tác vụ, model ID, để phân tích pha-chi-phối chạy theo từng lát cắt thay vì đối chiếu trung bình của cả đội máy vốn có thể che khuất các điểm nghẽn riêng của tenant hay luồng công việc. Ghép góc nhìn tùy chỉnh với các góc nhìn [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html) dựng sẵn cho việc đào sâu session, trace, và span khi một yêu cầu chậm cụ thể cần điều tra.
- **Profiling dưới lưu lượng production thay vì chỉ kiểm thử tổng hợp:** Chạy profile đối chiếu dữ liệu trace production thực để các hiệu ứng đồng thời, biến thiên hỗn-hợp-prompt, và tranh chấp hạ nguồn xuất hiện trong phân phối. Dùng tải tổng hợp từ các công cụ như giải pháp [Distributed Load Testing on AWS](https://docs.aws.amazon.com/solutions/latest/distributed-load-testing-on-aws/solution-overview.html) để kiểm-tra-căng các giả thuyết cụ thể, ví dụ để xác nhận rằng một thay đổi truy-xuất-song-song được đề xuất loại bỏ đuôi p99 quan sát được, và neo góc nhìn đóng-góp-theo-pha vào lưu lượng production để quyết định phản ánh cách người dùng thực sự luyện tác nhân.
- **Xếp hạng mục tiêu tối ưu theo đóng góp và biến thiên có thể xử lý được:** Với mỗi pha, ước lượng đóng góp vào ngân sách đầu-cuối và phần đóng góp đó có thể xử lý được bằng công sức kỹ thuật. Ưu tiên các pha mà cả hai đều cao, đóng góp lớn với dư địa để thu nhỏ, hơn các pha lớn nhưng đã gần sàn lý thuyết, để thời gian kỹ thuật dịch chuyển latency người dùng thấy chứ không phải một chỉ số không ảnh hưởng phần đuôi.
- **Đặt đường cơ sở theo pha và cảnh báo khi có độ trôi:** Thiết lập một phân phối đường cơ sở ở trạng thái ổn định cho mỗi pha, rồi áp [phát hiện bất thường CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) lên các chỉ số phân vị theo pha để các lệch chuẩn kích hoạt với pha vi phạm đã được quy trách nhiệm sẵn. Ghép cảnh báo cấp-pha với mục tiêu mức dịch vụ đầu-cuối để một pha trôi bên trong ngân sách theo pha của nó vẫn kích hoạt điều tra trước khi ngân sách đầu-cuối bị vượt.
- **Đo trước và sau mọi lần tối ưu:** Nắm bắt profile cho mỗi pha trước khi một tối ưu được triển khai và so sánh với cùng profile dưới lưu lượng production sau khi thay đổi được đưa vào. Xác nhận pha đã nhắm thực sự thu nhỏ, kiểm tra không pha nào khác hồi quy để hấp thụ ngân sách, và lưu giữ so sánh trong bản ghi thay đổi để các hồi quy tương lai có thể được chẩn đoán đối chiếu một profile được-biết-là-tốt.
- **Xem lại profile khi khối công việc tiến hóa:** Hành vi tác nhân trôi dạt khi prompt, Tools, bộ nhớ, và Model thay đổi, và pha chi phối lúc ra mắt hiếm khi giữ vị trí chi phối sau sáu tháng. Làm mới profile theo pha sau mỗi thay đổi prompt hay Model đáng kể và ít nhất hàng quý, rồi xếp hạng lại mục tiêu tối ưu đối chiếu profile hiện tại để công sức kỹ thuật tiếp tục rơi vào pha thực sự giới hạn hiệu năng người dùng thấy.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công bám sát hiệu năng cho các khối công việc tác nhân](agentperf01-bp01.md)
- [AGENTPERF01-BP02 Triển khai telemetry hiệu năng toàn diện](agentperf01-bp02.md)
- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](../2-agentperf02/agentperf02-bp01.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](../2-agentperf02/agentperf02-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Blog: Xây dựng tác nhân AI đáng tin cậy với Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html)
- [Observability và giám sát, Xây dựng kiến trúc serverless cho AI dạng tác nhân](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/observability-and-monitoring.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Nâng tầm khả năng quan sát ứng dụng và AI tạo sinh (COP326)](https://www.youtube.com/watch?v=vxzq8GthOLs)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Observability](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
