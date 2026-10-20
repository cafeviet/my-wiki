# Tối ưu pipeline xử lý cốt lõi và suy luận

Một pipeline suy luận được tối ưu tốt là cái khiến các tác nhân cảm thấy nhanh, nhạy bén, và đáng dùng. Nó là khác biệt giữa một tác nhân mà người dùng dựa vào và một tác nhân họ bỏ rơi. Pipeline suy luận (bao trùm nhận thức, suy luận, lập kế hoạch, ra quyết định, và thực thi hành động) là đường-tới-hạn-về-hiệu-năng của mọi hệ thống AI dạng tác nhân. Mỗi vòng lặp của vòng lặp tác nhân liên quan đến một lệnh gọi suy luận LLM, vốn thường là thao tác tốn-latency và tốn-tài-nguyên nhất trong ngăn xếp. Tối ưu xử lý cốt lõi đòi hỏi thiết kế các pipeline suy luận hiệu quả nhằm giảm thiểu các vòng lặp không cần thiết, chọn Model phù hợp độ phức tạp tác vụ, giảm latency đường thực thi qua các quyết định kiến trúc, và tối ưu phân phối streaming để giảm thiểu latency cảm nhận cho các tương tác hướng-người-dùng. Thiết kế pipeline kém tạo ra các tác nhân chậm, tốn kém, và không nhạy bén, bất kể hạ tầng nền tảng được cấp phát tốt đến đâu.

Về mô hình actor như một mẫu thực thi nền tảng, xem [AGENTREL01-BP03](../../3-reliability/1-agentrel01/agentrel01-bp03.md).

| AGENTPERF02: Bạn tối ưu xử lý cốt lõi và pipeline suy luận của tác nhân như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các pipeline suy luận bị giới hạn bởi trần số vòng lặp và kết thúc sớm dựa-trên-độ-tin-cậy để tác vụ đơn giản giải quyết trong một hoặc hai vòng lặp trong khi tác vụ phức tạp nhận được số vòng lặp cần thiết.
- Mỗi lớp tác vụ được định tuyến tới Model nhỏ nhất đáp ứng mức chất lượng của nó, với dự phòng theo tầng (cascading fallback) tới một Model có năng lực cao hơn khi Model được gán tạo ra đầu ra độ-tin-cậy-thấp.
- Các thao tác độc lập thực thi đồng thời, kết nối và runtime luôn ấm qua các lần gọi, và các tra cứu lặp lại trong một yêu cầu được khử trùng lặp qua các cache phạm vi-yêu-cầu.
- Các tác nhân hướng-người-dùng stream token với time-to-first-token dưới một giây, công việc tiền-suy-luận được nén để bảo toàn ngân sách TTFT, và các lệnh gọi Tools giữa luồng hiển thị tiến trình cho người dùng thay vì những khoảng dừng không giải thích.
- Các chiến lược thử lại (retry) và đường suy giảm nhẹ nhàng bị giới hạn bởi ngân sách latency tường minh để việc phục hồi lỗi ở trong mục tiêu mức dịch vụ đầu-cuối thay vì âm thầm bào mòn nó.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với việc tối ưu pipeline xử lý cốt lõi và suy luận.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các tác nhân chạy không có giới hạn vòng lặp hay kết thúc dựa-trên-độ-tin-cậy, và một Model lớn duy nhất phục vụ mọi tác vụ bất kể độ phức tạp. Các thao tác độc lập chạy tuần tự, kết nối được thiết lập lại mỗi lần gọi, và các tác nhân hướng-người-dùng chờ phản hồi hoàn chỉnh trước khi bất kỳ đầu ra nào tới người dùng. Lỗi lan truyền mà không có ngân sách thử lại tường minh. |
| 2 | Manh nha (Emerging) | Trần vòng lặp và giới hạn thử lại cơ bản có sẵn cho các tác nhân chủ lực, và phân loại tác vụ được ghi tài liệu nhưng chưa định tuyến nhất quán. Streaming được bật cho một số tương tác hướng-người-dùng nhưng đường tiền-suy-luận chưa được tối ưu cho time-to-first-token. Lựa chọn Model xảy ra tại thời điểm thiết kế thay vì được đánh giá đối chiếu phân phối tác vụ của khối công việc. |
| 3 | Đã định nghĩa (Defined) | Các lớp tác vụ được ánh xạ tới các tầng Model được đánh giá trên chính phân phối của khối công việc qua [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html), với dự phòng theo tầng được cấu hình cho đầu ra độ-tin-cậy-thấp. Các thao tác độc lập thực thi đồng thời bên trong các nguyên hàm framework như [Strands Agents](https://strandsagents.com/), và các API streaming của [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) phân phối đầu ra từng-token-một. Các chiến lược thử lại bị giới hạn bởi ngân sách latency và token tường minh. |
| 4 | Chủ động (Proactive) | Các phép gán Model và luật định tuyến được đưa ra ngoài dưới dạng cấu hình runtime trong [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) và được thăng cấp qua các đợt triển khai tiệm tiến (progressive rollout) được kiểm soát bởi cảnh báo CloudWatch. Gộp kết nối (connection pooling) qua [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html) và runtime ấm qua [phiên Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html) hoặc [đồng thời cấp phát trước của AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) loại bỏ khởi động lạnh (cold start) khỏi đường tới hạn. Các lệnh gọi Tools trong lúc streaming hiển thị các sự kiện tiến trình có cấu trúc cho client. |
| 5 | Tối ưu (Optimized) | Hình dạng pipeline, trần, định tuyến Model, và luật dự phòng được hiệu chỉnh liên tục từ telemetry production, và [suy luận tối-ưu-latency của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html) được đánh giá cho mỗi Model đủ điều kiện. Các khối công việc thoại và thời-gian-thực chạy trên [streaming hai chiều của Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-bidirectional-streaming.html) qua [Amazon Nova Sonic](https://docs.aws.amazon.com/nova/latest/userguide/speech.html). Số vòng lặp suy luận, TTFT, và tỷ lệ leo-thang-dự-phòng nằm cạnh latency và chi phí trên mọi bảng điều khiển, và tổ chức đóng góp lại các mẫu pipeline cho cộng đồng thực hành của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các tác nhân suy luận mà không có trần vòng lặp hay tín hiệu kết thúc sớm, tạo ra các vòng lặp mất kiểm soát tiêu tốn token và thời gian mà không cải thiện chất lượng đầu ra.
- Một Model lớn duy nhất phục vụ mọi tác vụ bất kể độ phức tạp, trả phí bảo hiểm về latency và chi phí của một Model hạng nặng cho công việc mà một Model nhỏ hơn giải quyết cũng tốt.
- Các thao tác độc lập thực thi tuần tự và kết nối được thiết lập lại mỗi lần gọi, nên latency đầu-cuối trở thành tổng của mọi thời lượng thao tác cộng chi phí thiết lập lặp lại.
- Các tác nhân hướng-người-dùng chờ phản hồi hoàn chỉnh trước khi bất kỳ đầu ra nào tới người dùng, nên latency cảm nhận bằng tổng thời gian xử lý thay vì time-to-first-token ngắn hơn mà streaming sẽ mang lại.
- Các lệnh gọi Tools giữa luồng làm dừng đầu ra mà không có tiến trình người-dùng-thấy, tạo ra các khựng cảm nhận nơi người dùng thấy đầu ra một phần rồi im lặng trong vài giây.

###### Các thực hành tốt

- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](agentperf02-bp01.md)
- [AGENTPERF02-BP02 Triển khai chiến lược lựa chọn Model phù hợp tác vụ](agentperf02-bp02.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](agentperf02-bp03.md)
- [AGENTPERF02-BP04 Tối ưu phản hồi streaming và time-to-first-token cho các tương tác tác nhân](agentperf02-bp04.md)
