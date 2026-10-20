# Tích hợp Tools và tối ưu framework

Các tác nhân mở rộng năng lực của chúng bằng cách gọi các **Tools** bên ngoài (API, cơ sở dữ liệu, công cụ tìm kiếm, trình thông dịch mã, và các dịch vụ khác) và vận hành trong các framework cung cấp giàn giáo cho hành vi tác nhân. Hiệu năng của các tích hợp Tools ảnh hưởng trực tiếp tới độ nhạy bén của tác nhân vì các lệnh gọi Tools xảy ra trong vòng lặp suy luận của tác nhân, thêm **latency** vào mỗi vòng lặp đòi hỏi các năng lực bên ngoài. Lựa chọn và cấu hình framework tương tự ảnh hưởng hiệu năng qua tác động của chúng tới hiệu quả vòng-lặp-tác-nhân, quản lý bộ nhớ, và chi phí điều phối. Tối ưu lớp này đòi hỏi chọn các framework giảm thiểu chi phí, thiết kế các chiến lược tích hợp Tools giảm latency gọi, triển khai các cơ chế khám phá và lựa chọn Tools hiệu quả, và dùng các meta-tool hợp thành nhiều năng lực thành các thao tác hiệu quả duy nhất.

| AGENTPERF06: Bạn tối ưu các tích hợp Tools và sử dụng framework cho hiệu năng tác nhân như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các lệnh gọi Tools thêm latency tối thiểu vào vòng lặp suy luận của tác nhân, và trải nghiệm lựa chọn nhất quán qua các tác nhân bất kể một Tool được triển khai ở đâu.
- Các tác nhân thấy một danh mục được lọc gồm 5 đến 10 Tools liên quan cho mỗi ngữ cảnh tác vụ thay vì toàn danh mục, giữ độ chính xác lựa chọn Tools cao khi danh mục tăng.
- Các lệnh gọi Tools độc lập chạy song song, và các kết quả tái dùng được cache ở phạm vi khớp ngữ nghĩa của dữ liệu (yêu cầu, phiên, hoặc toàn cục).
- Các mẫu gọi Tools (gộp kết nối, timeout được định-cỡ theo hành vi thực, backoff và jitter trên các lần thử lại, các cắt-mạch tự động) giữ chi phí hạ tầng khỏi đường tới hạn.
- Các meta-tool đóng gói các chuỗi đa-bước có thể dự đoán thành các thao tác phía-máy-chủ duy nhất, gộp các vòng lặp suy luận cho công việc thường quy trong khi các Tools riêng lẻ vẫn sẵn có cho các trường hợp mới lạ.
- Latency theo-Tool, tỷ lệ lỗi, trạng thái cắt-mạch, và hiệu quả cache được đo, để các hồi quy cấp-Tool có thể quy trách nhiệm trước khi chúng chi phối latency tác vụ.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với tích hợp Tools và tối ưu framework.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các Tools được tích hợp trực tiếp bởi mỗi nhóm tác nhân, không có giao thức dùng chung và không kỷ luật danh mục. Toàn bộ danh sách Tools được trình cho Model trên mọi vòng lặp suy luận, các lệnh gọi Tools chạy tuần tự, và các kết quả được tính-lại trên mọi lần gọi. Kết nối được thiết lập lại mỗi lệnh gọi, timeout mặc định về các giá trị SDK quá hào phóng, và các lần thử lại chạy không có backoff. Không có telemetry theo-Tool, nên các hồi quy chỉ hiện lên như chậm người-dùng-thấy. |
| 2 | Manh nha (Emerging) | [Model Context Protocol (MCP)](https://modelcontextprotocol.io) được áp dụng làm giao thức tích hợp và [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) phơi bày các Tools qua một giao diện nhất quán. Khám phá Tools ngữ nghĩa được dùng cho các danh mục lớn để Model thấy một tập được lọc thay vì mọi Tool. Gộp kết nối cơ bản có sẵn cho các endpoint tùy chỉnh, và các timeout theo-Tool được đặt từ latency p95 đo được. Các lần thử lại dùng backoff và jitter, và các chỉ số latency theo-Tool cùng tỷ lệ lỗi được công bố qua [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html). |
| 3 | Đã định nghĩa (Defined) | Thực thi Tools song song được bật cho các lệnh gọi độc lập. Các API Tools được thiết kế cho tiêu thụ tác nhân với lược đồ gọn, phân trang, và phản hồi một phần. Các kết quả được cache ở nhiều phạm vi (yêu cầu, phiên, toàn cục) dùng các cache trong-tiến-trình và [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html) nơi phù hợp. Các API batch thay các vòng lặp đơn-mục cho công việc đa-mục, và các Tools dựa-trên-[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) khởi tạo client bên ngoài handler để bảo toàn connection pool qua các lần gọi. |
| 4 | Chủ động (Proactive) | Các cắt-mạch tự động định tuyến vòng qua các Tools suy giảm, dự phòng về các kết quả được cache hoặc lỗi có kiểm soát thay vì làm cạn ngân sách suy luận. Các chuỗi Tools lặp lại thường xuyên được nhận diện từ telemetry và hợp nhất thành các meta-tool triển khai trên AWS Lambda và phơi bày qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html). Hiệu năng meta-tool được so sánh với chuỗi Tools-riêng-lẻ tương đương, và các bảng điều khiển theo-Tool cảnh báo trên các hồi quy latency, tỷ lệ lỗi, tỷ lệ timeout, và trạng thái cắt-mạch. |
| 5 | Tối ưu (Optimized) | Các chiến lược tích hợp, gọi, và meta-tool được tinh chỉnh liên tục đối chiếu dữ liệu vận hành. Các meta-tool được nghỉ hưu khi chúng ngừng vượt đường cơ sở Tools-riêng-lẻ, TTL cache được tinh chỉnh theo từng Tool, và các danh mục Tools tiến hóa theo các mẫu dùng. Tổ chức công bố các mẫu Tools thân-thiện-tác-nhân tái dùng (lược đồ gọn, wrapper cắt-mạch, mẫu meta-tool) và chia sẻ các benchmark qua các nhóm, giữ đóng góp cấp-Tool vào latency đầu-cuối ở cận dưới được định nghĩa bởi thời gian xử lý vốn có của mỗi Tool. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm trình mọi Tool sẵn có cho Model trên mọi vòng lặp suy luận, tiêu dung lượng context window và làm suy giảm độ chính xác lựa chọn một khi danh mục tăng vượt 10 đến 15 Tools.
- Các lệnh gọi Tools độc lập chạy tuần tự thay vì song song, nên latency cấp-Tool cộng dồn tuyến tính theo số lệnh gọi thay vì bám theo giá trị cực đại.
- Caching kết quả Tools bị bỏ qua, nên các tác nhân gọi-lại cùng một Tool với các tham số giống hệt vài lần trong một tác vụ duy nhất.
- Kết nối được thiết lập lại trên mọi lần gọi, thêm latency bắt-tay TLS vào mọi lệnh gọi Tool vốn có thể tái dùng một kết nối bền.
- Timeout được mặc định hoặc đặt quá hào phóng, để một lệnh gọi Tool bệnh lý duy nhất tiêu toàn bộ ngân sách latency tác vụ, và các lần thử lại chạy không có backoff hoặc một ngân sách tổng.
- Các chuỗi Tools đa-bước có thể dự đoán được thực-thi-lại như các lệnh gọi Tools riêng lẻ trên mọi lần xảy ra thay vì được hợp nhất thành các meta-tool, lãng phí các vòng lặp suy luận và token vào công việc thường quy.

###### Các thực hành tốt

- [AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu](agentperf06-bp01.md)
- [AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả](agentperf06-bp02.md)
- [AGENTPERF06-BP03 Tối ưu sử dụng meta-tool và chuỗi hóa Tools](agentperf06-bp03.md)
