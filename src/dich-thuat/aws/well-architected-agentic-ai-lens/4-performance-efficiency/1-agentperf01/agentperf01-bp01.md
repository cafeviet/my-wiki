# AGENTPERF01-BP01 Định nghĩa tiêu chí thành công bám sát hiệu năng cho các khối công việc tác nhân

Các khối công việc tác nhân khó đo lường hơn ứng dụng truyền thống vì một yêu cầu duy nhất của người dùng tỏa ra thành nhiều lệnh gọi suy luận (inference), lệnh gọi **Tools**, và truy xuất bộ nhớ, mỗi cái có đặc trưng riêng về **latency**, chất lượng, và chi phí. Nếu không có mục tiêu hiệu năng tường minh, các nhóm tối ưu dựa trên một mốc tham chiếu luôn dịch chuyển và không thể biết khi nào một tác nhân đã sẵn sàng cho production.

**Kết quả mong muốn:**

- Bạn có tài liệu về tiêu chí thành công hiệu năng cho mọi khối công việc tác nhân, với các mục tiêu cụ thể, đo lường được, được rà soát khi yêu cầu kinh doanh tiến hóa.
- Các nhóm của bạn đánh giá khách quan xem một tác nhân có đáp ứng kỳ vọng hiệu năng trước khi triển khai và liên tục xác nhận hiệu năng trong production.
- Bạn tích hợp tiêu chí hiệu năng vào các pipeline CI/CD dưới dạng cổng chất lượng (quality gates), giúp ngăn các hồi quy lọt vào production.

**Các phản mẫu thường gặp (anti-patterns):**

- Định nghĩa tiêu chí thành công chỉ quanh các chỉ số hạ tầng như mức dùng CPU hay tiêu thụ bộ nhớ, mà không đo các chiều riêng của tác nhân như reasoning latency, hiệu quả token, hay chất lượng hoàn thành tác vụ.
- Áp một mục tiêu latency duy nhất cho cả tác nhân streaming lẫn không-streaming, hoặc cho cả khối công việc tương tác lẫn batch, trong khi time-to-first-token và hoàn thành đầu-cuối lại là các KPI chính cho các lớp tác nhân khác nhau.
- Thiết lập mục tiêu hiệu năng sau khi triển khai thay vì trong lúc thiết kế, tạo ra các kiến trúc không thể đáp ứng yêu cầu nếu không làm lại đáng kể.

**Lợi ích khi áp dụng thực hành tốt này:**

- Tiêu chí thành công tường minh thiết lập các mục tiêu cụ thể để telemetry có thể được đánh giá dựa vào đó, khiến công việc hiệu năng hạ nguồn trở nên đo lường được thay vì suy đoán.
- Tiêu chí bám sát hiệu năng hướng các nhóm tối ưu pipeline suy luận cho những chỉ số quan trọng, thay vì theo đuổi những tối ưu chung chung không cải thiện kết quả kinh doanh.
- Các cổng chất lượng gắn với mục tiêu đo lường được biến tiêu chí thành công thành hiện vật có thể cưỡng chế, chặn hồi quy trước khi vào production thay vì phát hiện sau khi việc đã rồi.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Tiêu chí thành công cho một khối công việc tác nhân phải đủ cụ thể để đánh giá một bản build và đủ chi tiết để dẫn dắt các quyết định kiến trúc. Một tiêu chí bám sát hiệu năng phải nêu tên tín hiệu, ngưỡng, phân vị hoặc mục tiêu đạt được, cửa sổ đánh giá, và kết quả kinh doanh mà nó bảo vệ. Không có sự cụ thể đó, các nhóm không thể quyết định nên đổi Model, thêm caching, tách một luồng công việc, hay từ chối một bản phát hành, vì không có mốc tham chiếu để phán xét thay đổi.

Các khối công việc tác nhân có bề mặt KPI rộng hơn ứng dụng truyền thống vì một yêu cầu duy nhất của người dùng bung ra thành nhiều lệnh gọi suy luận, truy vấn truy xuất, lệnh gọi Tools, và với hệ đa tác nhân là các lượt bàn giao liên tác nhân, mỗi cái có latency, chế độ lỗi, và chi phí riêng. Một tập tiêu chí thành công đầy đủ trải rộng bốn chiều:

- Latency (time-to-first-token cho tác nhân streaming, thời gian hoàn thành đầu-cuối cho tác nhân hướng-tác-vụ, và ngân sách theo từng pha trên toàn pipeline suy luận)
- Throughput (số phiên đồng thời, số yêu cầu mỗi giây duy trì được, và độ sâu hàng đợi dưới tải)
- Chất lượng (tỷ lệ hoàn thành tác vụ, độ chính xác lựa chọn Tools và tham số, tính căn cứ (grounding) của suy luận, và độ trung thực (faithfulness) của phản hồi)
- Hiệu quả (số token mỗi tác vụ, chi phí mỗi lần hoàn thành, và tỷ lệ trúng cache).

Các [framework đánh giá tác nhân phân lớp](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/) phân rã chất lượng sâu hơn thành các tín hiệu cấp-thành-phần mà giám sát chỉ-dựa-vào-hạ-tầng không thể thấy, như việc dùng Tools, truy xuất bộ nhớ, độ bám chủ đề đa lượt, độ chính xác suy luận, trách nhiệm, và an toàn.

KPI latency chính khác nhau theo lớp tác nhân. Với các tác nhân streaming, hội thoại, người dùng cảm nhận độ nhạy bén qua time-to-first-token và inter-token latency, nên đó là các KPI kiểm soát việc phát hành. Với các tác nhân hướng-tác-vụ trả về một kết quả có cấu trúc duy nhất, thời gian hoàn thành tác vụ là chính và time-to-first-token phần lớn không liên quan. Với các luồng công việc batch hoặc bất đồng bộ, throughput và chi-phí-mỗi-tác-vụ chi phối, và latency p99 nghiêm ngặt ít quan trọng hơn việc hoàn-thành-trong-SLA có thể dự đoán. Một mục tiêu latency duy nhất cho các lớp này hoặc cấp dư cho một số tác nhân hoặc đặt mục tiêu không thể đạt cho các tác nhân khác. [Hướng dẫn Hiệu quả hiệu năng của AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_establish_key_performance_indicators.html) khẳng định rằng hành vi phần đuôi quan trọng hơn giá trị trung bình; p90 và p99 neo giữ các mục tiêu latency vì trung bình che giấu các phản hồi chậm gây trải nghiệm tệ mà người dùng cảm nhận.

Một mục tiêu đo lường được có cấu trúc nhiều hơn một con số. Một mục tiêu mức dịch vụ (SLO) kết hợp một chỉ báo mức dịch vụ (SLI, tức chỉ số), một ngưỡng, một mục tiêu đạt được (tỷ lệ thời gian hoặc yêu cầu phải đạt ngưỡng), một khoảng thời gian (lịch hay cửa sổ trượt), và một ngân sách lỗi (mức thiếu hụt cho phép).

[Các mục tiêu mức dịch vụ của Amazon CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html) hình thức hóa cấu trúc này và bổ sung cảnh báo tốc-độ-tiêu (burn-rate) kích hoạt khi ngân sách bị tiêu nhanh hơn dự kiến, điều quan trọng với các khối công việc tác nhân có phân phối latency dịch chuyển tinh vi khi prompt, Tools, hay Model trôi dạt. SLO nên được phân rã thành ngân sách latency theo pha, suy luận, truy xuất, gọi Tools, điều phối liên tác nhân, để khi một ngân sách bị vượt, việc quy về đúng pha vi phạm đã mã hóa sẵn trong tiêu chí thay vì điều tra sau đó.

Tiêu chí thành công không tĩnh. Hành vi tác nhân được định hình bởi prompt, bộ nhớ, Tools, và các Model đứng sau, tất cả đều trôi dạt, nên tiêu chí đúng lúc ra mắt sẽ bào mòn khi hệ thống tiến hóa. Tích hợp mục tiêu vào CI/CD dưới dạng cổng chất lượng, ngân sách latency được đối chiếu với kết quả kiểm thử tải, tỷ lệ hoàn-thành-tác-vụ đối chiếu với tập đánh giá được tuyển chọn, chi-phí-mỗi-tác-vụ đối chiếu với một trần, biến chúng từ tài liệu thành hiện vật có thể cưỡng chế chặn hồi quy ngay tại ranh giới.

[Vận hành hóa AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html) khung hóa kỷ luật vòng đời này như bắt buộc chứ không tùy chọn, vì đo lường liên tục là cơ chế duy nhất giữ cho tiêu chí bám sát các kết quả kinh doanh mà chúng được thiết kế để bảo vệ.

### Các bước triển khai

- **Nắm bắt kết quả kinh doanh và kỳ vọng người dùng cùng các bên liên quan:** Làm việc với các chủ sở hữu sản phẩm, kinh doanh, và trải nghiệm người dùng để ghi tài liệu các kết quả mà tác nhân phải tạo ra, các kịch bản nó vận hành, và kỳ vọng của người dùng về độ nhạy bén, chất lượng, và chi phí. Dùng đầu vào này để khung hóa mọi mục tiêu hạ nguồn sao cho KPI latency, throughput, chất lượng, và hiệu quả truy ngược về một nhu cầu kinh doanh hay người dùng đã nêu. [Hướng dẫn quy trình Hiệu quả hiệu năng của AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_establish_key_performance_indicators.html) coi việc thống nhất với các bên liên quan này là bước đầu tiên trong việc thiết lập KPI đáng tin.
- **Phân loại mỗi khối công việc tác nhân theo mẫu tương tác:** Xác định tác nhân là streaming hay không-streaming, tương tác hay batch, đồng bộ hay bất đồng bộ, và đơn-tác-nhân hay đa-tác-nhân. Việc phân loại quy định KPI latency nào là chính, time-to-first-token cho tác nhân hội thoại streaming, hoàn thành đầu-cuối cho tác nhân hướng-tác-vụ, throughput và chi-phí-mỗi-tác-vụ cho luồng batch, và liệu các chỉ số điều phối đa tác nhân như latency bàn giao và độ thành công cộng tác có thuộc tập tiêu chí hay không.
- **Định nghĩa phân loại KPI trải rộng latency, throughput, chất lượng, và hiệu quả:** Với mỗi khối công việc, liệt kê các tín hiệu cụ thể cần đo theo bốn chiều, gồm cả tín hiệu riêng của tác nhân mà chỉ số hạ tầng không bao được. Cấu trúc tín hiệu chất lượng theo lớp, chất lượng phản hồi cuối, hoàn thành tác vụ, độ chính xác dùng Tools, độ liên quan của bộ nhớ và truy xuất, tính căn cứ của suy luận, và trách nhiệm cùng an toàn, theo [framework đánh giá tác nhân do các nhóm của Amazon mô tả](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/). Bao gồm tín hiệu hiệu quả như số token mỗi tác vụ, chi phí mỗi lần hoàn thành, và tỷ lệ trúng cache để kết nối hiệu năng với kinh tế đơn vị.
- **Đặt mục tiêu định lượng với ngưỡng, phân vị, và mục tiêu đạt được:** Gắn một mục tiêu số cho mọi KPI, chỉ định phân vị (p50, p90, p99) cho tín hiệu latency và throughput và mục tiêu đạt được (ví dụ 99,5% yêu cầu) cho tín hiệu chất lượng và tính sẵn sàng. Neo giữ mục tiêu latency vào p90 và p99 thay vì trung bình, vì hành vi phần đuôi định đoạt hiệu năng người dùng cảm nhận; [trụ cột Hiệu quả hiệu năng của AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html) cảnh báo rằng trung bình che giấu các phản hồi chậm quan trọng nhất.
- **Phân bổ ngân sách latency theo pha bên trong ngân sách đầu-cuối:** Phân rã mục tiêu latency đầu-cuối thành ngân sách theo pha, truy xuất ngữ cảnh, suy luận LLM, gọi Tools, điều phối liên tác nhân, sinh đầu ra, để mỗi pha có trần riêng cộng lại thành mục tiêu tổng. Ngân sách theo pha khiến việc vượt trần được quy trách nhiệm ngay tại thời điểm định nghĩa tiêu chí và cho các nhóm kỹ thuật mục tiêu tối ưu rõ ràng khi một pha trôi dạt. Xác nhận việc phân rã đối chiếu với trace đo được để ngân sách phản ánh hành vi thực chứ không phải giả định.
- **Hình thức hóa mục tiêu thành SLO với ngân sách lỗi và cảnh báo tốc-độ-tiêu:** Với mỗi KPI hướng-khách-hàng, mã hóa mục tiêu thành một SLO với SLI, ngưỡng, mục tiêu đạt được, khoảng thời gian, và chu kỳ dùng [các mục tiêu mức dịch vụ của Amazon CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html). Cấu hình cảnh báo tốc-độ-tiêu để dịch vụ báo hiệu khi ngân sách lỗi bị tiêu nhanh hơn dự kiến, cho người vận hành thời gian phản ứng trước khi SLO bị vượt. Nhóm các SLI liên quan thành SLO tổng hợp khi một kết quả hướng-người-dùng phụ thuộc vào nhiều thao tác cùng đạt mục tiêu riêng.
- **Vận hành hóa KPI chất lượng và chi phí qua giám sát nhận-biết-GenAI:** Công bố tiêu thụ token, phân vị latency mỗi lần gọi, quy chi phí, và chỉ số chất lượng cấp-tác-nhân qua [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html), vốn hiển thị các tín hiệu này một cách nguyên bản cho các lệnh gọi Model của Amazon Bedrock và chấp nhận trace có cấu trúc từ tác nhân chạy trên bất kỳ runtime nào qua [AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/introduction). Phát ra các tín hiệu chất lượng riêng của tác nhân, tỷ lệ hoàn thành tác vụ, độ chính xác lựa chọn Tools, tính căn cứ của suy luận, dưới dạng chỉ số tùy chỉnh để chúng có thể được đặt ngưỡng, cảnh báo, và gắn với SLO như cách tín hiệu hạ tầng được xử lý.
- **Tích hợp mục tiêu thành cổng chất lượng trong pipeline triển khai:** Chuyển mỗi tiêu chí thành công thành một kiểm tra tự động trong CI/CD để các bản phát hành vượt mục tiêu latency, chất lượng, hay chi phí bị chặn trước khi tới người dùng. Chạy kiểm thử tải đối chiếu mục tiêu latency và throughput cùng các tập đánh giá được tuyển chọn đối chiếu mục tiêu chất lượng như một phần của pipeline, theo khung quản-lý-vòng-đời trong [Vận hành hóa AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html). Các cổng biến tiêu chí đã viết thành hiện vật có thể cưỡng chế giúp ngăn hồi quy thay vì phát hiện trong production.
- **Xem lại mục tiêu theo nhịp định sẵn khi khối công việc tiến hóa:** Lên lịch rà soát định kỳ mỗi tiêu chí thành công đối chiếu telemetry production, thay đổi kỳ vọng người dùng, và các dịch chuyển ở Model, prompt, hoặc Tools nền tảng. Siết những mục tiêu bị vượt một cách nhất quán, nới những mục tiêu đang chặn các cải tiến chính đáng, và loại bỏ tín hiệu không còn ánh xạ tới kết quả kinh doanh; hành vi tác nhân trôi dạt, và tiêu chí đúng lúc ra mắt cần được kiểm chứng lại đối chiếu thực tế hiện tại.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP02 Triển khai telemetry hiệu năng toàn diện](agentperf01-bp02.md)
- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](agentperf01-bp03.md)
- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc tác nhân](../../1-operational-excellence/5-agentops05/agentops05-bp04.md)
- [AGENTOPS06-BP02 Đánh giá và theo dõi hiệu năng tác nhân liên tục](../../1-operational-excellence/6-agentops06/agentops06-bp02.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy chi-phí-suy-luận cấp-tác-nhân](../../5-cost-optimization/5-agentcost05/agentcost05-bp01.md)

**Tài liệu liên quan:**

- [AWS Well-Architected Framework: Trụ cột Hiệu quả hiệu năng](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html)
- [Amazon CloudWatch Application Signals: Mục tiêu mức dịch vụ (SLOs)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html)
- [Khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html)
- [Vận hành hóa AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Blog: Đánh giá tác nhân AI: Bài học thực tế từ việc xây dựng hệ thống dạng tác nhân tại Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)

**Video liên quan:**

- [AWS re:Invent 2024 - Nâng tầm khả năng quan sát ứng dụng và AI tạo sinh (COP326)](https://www.youtube.com/watch?v=vxzq8GthOLs)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon CloudWatch Application Signals](https://aws.amazon.com/cloudwatch/features/application-monitoring/)
- [AWS Distro for OpenTelemetry (ADOT)](https://aws.amazon.com/otel/)
