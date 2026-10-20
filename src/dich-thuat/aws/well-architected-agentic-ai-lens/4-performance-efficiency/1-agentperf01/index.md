# Lập kế hoạch và đo lường hiệu năng chiến lược

Các hệ thống AI dạng tác nhân đưa vào những chiều đo hiệu năng mới vượt ra ngoài các chỉ số hạ tầng truyền thống, bao gồm **latency suy luận (reasoning latency)**, **throughput token**, hiệu quả gọi **Tools**, **thời gian tới token đầu tiên (time-to-first-token)**, và tổng thời gian hoàn thành tác vụ. Lập kế hoạch hiệu năng chiến lược đòi hỏi định nghĩa các tiêu chí thành công có thể đo lường với ngân sách latency theo từng pha, triển khai **đo lường viễn trắc (telemetry)** kỹ lưỡng trên toàn pipeline suy luận, phân tích (profiling) latency tổng thể một cách hệ thống để nhận diện điểm nghẽn, và thiết lập các thực hành kiểm thử hiệu năng nhằm xác nhận độ nhạy bén của tác nhân dưới tải. Nếu không lập kế hoạch hiệu năng có chủ đích, tổ chức có nguy cơ triển khai những tác nhân trông có vẻ hoạt động được nhưng lại không đáp ứng được kỳ vọng về latency, throughput, hay chất lượng khi mở rộng quy mô.

Về các mô hình trưởng thành của tác nhân và quản trị vòng đời, xem [AGENTOPS03-BP01](../../1-operational-excellence/3-agentops03/agentops03-bp01.md). Về các vòng phản hồi chỉ số kinh doanh, xem [AGENTOPS02-BP04](../../1-operational-excellence/2-agentops02/agentops02-bp04.md). Về các framework đánh giá tác nhân, xem [AGENTOPS06-BP02](../../1-operational-excellence/6-agentops06/agentops06-bp02.md).

| AGENTPERF01: Bạn lập kế hoạch chiến lược cho hiệu năng tác nhân và thiết lập các thực hành đo lường như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các tiêu chí thành công về hiệu năng được định nghĩa dưới dạng các mục tiêu mức dịch vụ (service level objectives) có thể đo lường cho từng khối công việc tác nhân, bao trùm latency (bao gồm time-to-first-token và hoàn thành đầu-cuối), throughput, chất lượng, và các chiều hiệu quả mà việc suy luận, dùng Tools, và điều phối đa tác nhân riêng của tác nhân đưa vào.
- Ngân sách latency đầu-cuối được phân rã thành các phân bổ theo từng pha trên toàn truy xuất ngữ cảnh, suy luận, gọi Tools, và điều phối liên tác nhân, để độ trôi (drift) được quy về đúng pha gây ra nó thay vì phải chẩn đoán trong lúc xảy ra sự cố.
- Telemetry phân tán ghi lại mọi lần thực thi tác nhân dưới dạng phân cấp session, trace, và span khớp với các quy ước ngữ nghĩa AI tạo sinh của OpenTelemetry, để các thao tác trong pipeline suy luận có thể quan sát và tương quan riêng lẻ.
- Lưu lượng sản xuất (production) được phân tích theo một nhịp định sẵn để phân rã latency đầu-cuối thành các đóng góp theo từng pha, với công sức tối ưu được xếp hạng theo đóng góp nhân với biến thiên có thể xử lý được (addressable variance) thay vì chỉ theo đóng góp.
- Các tiêu chí thành công, telemetry, và cảnh báo cấp-pha nạp vào các cổng chất lượng (quality gates) CI/CD và cảnh báo hồi quy, để trạng thái hiệu năng luôn khớp với hành vi production khi prompt, Tools, và Model trôi dạt.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với việc lập kế hoạch và đo lường hiệu năng chiến lược.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các mục tiêu hiệu năng mang tính khát vọng hơn là đo lường được, không có KPI theo từng khối công việc và chỉ có các chỉ số hạ tầng. Telemetry giới hạn ở nhật ký runtime và các chỉ số thời lượng của [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html), và latency đầu-cuối là tín hiệu duy nhất được giám sát. Các hồi quy hiệu năng được phát hiện qua báo cáo của người dùng chứ không qua khả năng quan sát (observability), và tiêu chí chỉ được xem lại sau khi có sự cố. |
| 2 | Manh nha (Emerging) | Mục tiêu latency và throughput được ghi tài liệu cho các khối công việc chủ lực, và các trace cơ bản chảy qua [AWS X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html) hoặc CloudWatch. Các chỉ số riêng của tác nhân (hoàn thành tác vụ, số token mỗi tác vụ) được phát ra nhưng hiện chưa gắn với cảnh báo hay SLO. Việc phân rã theo pha là một lần chứ chưa mã hóa vào tiêu chí, và profiling diễn ra bị động sau sự cố đầu tiên. |
| 3 | Đã định nghĩa (Defined) | Mỗi khối công việc production có các mục tiêu mức dịch vụ có cấu trúc với chỉ báo mức dịch vụ (SLI), ngưỡng, mục tiêu đạt được, và khoảng thời gian được quản lý qua [Amazon CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html). Telemetry tương thích OpenTelemetry qua [AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/introduction) nạp vào bề mặt observability AI tạo sinh của CloudWatch, và ngân sách latency theo pha được phân bổ từ mục tiêu đầu-cuối. Profiling chạy trên lưu lượng production và các chỉ số phân vị theo pha được công bố. |
| 4 | Chủ động (Proactive) | [Phát hiện bất thường CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) cấp-pha và cảnh báo tốc-độ-tiêu (burn-rate) kích hoạt khi có độ trôi trước khi SLO đầu-cuối bị vượt, với các cảnh báo tổng hợp tương quan tín hiệu để giảm nhiễu. SLO được kiểm soát trong CI/CD qua kiểm thử tải và đánh giá tự động, và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) xác nhận chất lượng như một phần của pipeline. Các profile theo pha được làm mới theo nhịp định sẵn và các mục tiêu tối ưu được xếp hạng theo đóng góp và biến thiên có thể xử lý được. |
| 5 | Tối ưu (Optimized) | Các tiêu chí thành công, ngân sách theo pha, và ngưỡng được hiệu chỉnh liên tục từ telemetry production thay vì qua các chu kỳ rà soát thủ công. Các cổng chất lượng dựa trên tập đánh giá và trần chi-phí-mỗi-tác-vụ đi cùng mọi bản phát hành, và profiling nạp vào lộ trình kiến trúc. Tổ chức đóng góp lại các mẫu đo lường hiệu năng và profile chi-phí-suy-luận cho cộng đồng thực hành của mình và tinh chỉnh mục tiêu từ dữ liệu chứ không từ giả định tại thời điểm ra mắt. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm định nghĩa tiêu chí thành công theo thuật ngữ hạ tầng và bỏ sót các chiều riêng của tác nhân như reasoning latency, hiệu quả token, độ chính xác Tools, và time-to-first-token, nên tiêu chí không thể phát hiện các hồi quy thực sự ảnh hưởng tới người dùng.
- Mục tiêu latency đơn được áp cho cả tác nhân streaming lẫn không-streaming, hoặc cho cả khối công việc tương tác lẫn batch, điều này hoặc cấp phát dư cho một số tác nhân hoặc đặt mục tiêu không thể đạt được cho các tác nhân khác.
- Telemetry được thêm vào sau khi ra mắt và để lại lỗ hổng trong tính liên tục của trace qua các ranh giới tác nhân, các lệnh gọi Tools, và các thao tác bất đồng bộ, khiến việc điều tra hiệu năng sụp thành phỏng đoán.
- Latency đầu-cuối được đo mà không phân rã theo pha, nên công sức tối ưu rơi vào các pha đóng góp ít cho phần đuôi (tail) thay vì vào pha thực sự giới hạn hiệu năng người dùng thấy.
- Tiêu chí thành công, telemetry, và profiling bị coi là hiện vật tại thời điểm ra mắt chứ không phải hiện vật được xem lại theo nhịp, khiến độ trôi của tác nhân âm thầm bào mòn KPI cho đến khi người dùng nhận ra.

###### Các thực hành tốt

- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công bám sát hiệu năng cho các khối công việc tác nhân](agentperf01-bp01.md)
- [AGENTPERF01-BP02 Triển khai telemetry hiệu năng toàn diện](agentperf01-bp02.md)
- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](agentperf01-bp03.md)
