# Điều phối luồng công việc và cộng tác đa tác nhân

Các trường hợp dùng tác nhân có tác động lớn nhất (nghiên cứu phức tạp, dịch vụ khách hàng đa-lĩnh-vực, và tự động hóa quy trình) đòi hỏi nhiều tác nhân làm việc cùng nhau, và điều phối được thiết kế tốt là cái khiến tổng thể lớn hơn tổng các phần. Các hệ thống AI dạng tác nhân phức tạp thường liên quan đến nhiều tác nhân cộng tác để giải quyết các tác vụ vượt khả năng của bất kỳ tác nhân đơn lẻ nào. Điều phối luồng công việc phối hợp các tương tác đa tác nhân này qua các mẫu như phân cấp supervisor-worker, cộng tác ngang-hàng (peer-to-peer), và phân rã tác vụ dựa-trên-pipeline. Hiệu năng của các hệ đa tác nhân phụ thuộc vào việc phân phối công việc hiệu quả đến đâu, cách các tác nhân được chọn và gọi, cách các kết quả trung gian được truyền giữa các tác nhân, và cách thực thi song song được dùng để giảm **latency**.

| AGENTPERF05: Bạn tối ưu điều phối luồng công việc và cộng tác đa tác nhân cho hiệu năng như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các luồng công việc đa tác nhân chạy với chi phí điều phối tối thiểu, để latency đầu-cuối tiệm cận đường tới hạn của các thao tác phụ thuộc thay vì tổng của mọi bước.
- Các mẫu điều phối được khớp với hình dạng tác vụ, với các đồ thị động cho các luồng do-suy-luận-điều-khiển, Step Functions cho các khung xương xác định, và các lớp lai cho các luồng công việc kết hợp cả hai.
- Các tác-vụ-con độc lập chạy song song và các kết quả trung gian lớn được truyền bằng tham chiếu, giữ lớp điều phối nhỏ và đường tới hạn ngắn.
- Các mô hình cộng tác được khớp với đặc trưng tác vụ (supervisor-worker, pipeline, ngang-hàng, bầy/swarm), và các năng lực mặc định thành **Tools** thay vì sub-agent trừ khi chúng cần suy luận độc lập.
- Các pipeline đa-giai-đoạn dùng streaming và micro-batching để chồng lấp xử lý giai đoạn, với compute được-định-cỡ-đúng theo giai đoạn và tracing đầu-cuối khiến các điểm nghẽn có thể quy trách nhiệm.
- Các thao tác ủy quyền và bàn giao chỉ truyền ngữ cảnh mà tác nhân nhận cần, thông qua các kho ngữ cảnh dùng chung và các giao diện chuẩn hóa, và latency bàn giao là một chỉ số hạng nhất.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với điều phối luồng công việc và cộng tác đa tác nhân.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các luồng công việc đa tác nhân chạy tuần tự mà không có điều phối tường minh. Các nhóm nối các lệnh gọi tác nhân trong mã ứng dụng, truyền payload đầy đủ và lịch sử hội thoại giữa các bước, và dùng sub-agent cho công việc mà một Tool có thể làm trong vài mili-giây. Không có phát hiện chu trình, không timeout, và không telemetry theo-bước, nên các chuỗi ủy quyền mất-kiểm-soát và các nhánh chậm chỉ hiện lên như các lỗi người-dùng-thấy. |
| 2 | Manh nha (Emerging) | Các luồng công việc được phân loại là động, xác định, hoặc lai, và mỗi cái được đặt trên một trình điều phối phù hợp. [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) được áp dụng cho các luồng xác định, và điều phối framework nguyên bản được dùng cho các đồ thị động. Song song hóa cơ bản được bật cho các tác-vụ-con độc lập, và các kho dùng chung trên [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) hoặc [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) thay các payload nội tuyến cho các kết quả lớn. Timeout và đường dự phòng tồn tại cho các luồng công việc quan trọng nhất. |
| 3 | Đã định nghĩa (Defined) | Các luồng công việc đồ thị động chạy với phát hiện chu trình, giới hạn độ sâu cực đại, và số lượng fan-out có ràng buộc. Các mô hình cộng tác được chọn theo từng luồng công việc (supervisor-worker, pipeline, ngang-hàng, bầy) dùng các nguyên hàm framework nguyên bản như agent-as-tool của [Strands Agents](https://strandsagents.com/) và [cộng tác đa tác nhân của Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html). Các pipeline đa-giai-đoạn dùng streaming qua [API suy luận streaming của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/api-methods-run-inference.html) và micro-batching, với compute được-định-cỡ-đúng theo giai đoạn. Các kho ngữ cảnh dùng chung trên [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) mang ngữ cảnh ủy quyền thay vì truyền nội tuyến. |
| 4 | Chủ động (Proactive) | Các timeout theo-bước, theo-nhánh, và cấp-luồng-công-việc được suy ra từ SLO tác vụ, và các nhánh chậm kết thúc với kết quả một phần tốt nhất thay vì chặn. Tracing phân tán đầu-cuối qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) hoặc [AWS X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html) khiến đường tới hạn có thể quy trách nhiệm, và cân bằng lại giai đoạn là một thực hành thường quy. Ủy quyền xảy ra qua các giao diện chuẩn hóa trên [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), ủy quyền bất đồng bộ với callback [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) được dùng nơi tác nhân cha có công việc song song, và các bên nhận có thể dự đoán được làm-ấm-trước dùng [đồng thời cấp phát trước của AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) hoặc các pool phiên ấm. |
| 5 | Tối ưu (Optimized) | Các mẫu điều phối, mô hình cộng tác, và lược đồ ngữ cảnh được tinh chỉnh liên tục đối chiếu dữ liệu đo được. Các chỉ số latency bàn giao, hiệu quả song song, kích thước payload trạng thái, và chi phí cộng tác nằm trên các bảng điều khiển dùng chung dẫn dắt việc lặp lại thiết kế. Các luồng công việc mới bắt đầu từ các mẫu tái dùng, và tổ chức đóng góp các triển khai tham chiếu cho điều phối đồ thị động, các khung xương Step Functions lai, và các giao diện ủy quyền chuẩn hóa trở lại cộng đồng nội bộ. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm mặc định về sub-agent cho các năng lực mà một lệnh gọi Tool có thể xử lý trong vài mili-giây, trả toàn bộ chi phí vòng-lặp-suy-luận cho công việc xác định, đơn-bước.
- Các luồng công việc chạy các bước tuần tự ngay cả khi đồ thị phụ thuộc cho phép thực thi song song, đẩy latency đầu-cuối thành tổng các thời lượng bước thay vì đường tới hạn.
- Các điều phối đồ thị động chạy không có phát hiện chu trình, giới hạn độ sâu, hoặc fan-out có ràng buộc, nên vòng lặp suy luận thỉnh thoảng tạo ra các chuỗi ủy quyền vô giới hạn hoặc các nhánh đồng thời quá mức.
- Các trình điều phối mang các payload lớn nội tuyến giữa các bước thay vì truyền tham chiếu, phình kích thước trạng thái và buộc context window của trình điều phối giữ dữ liệu thô nó không cần.
- Các pipeline đa-giai-đoạn dùng cấu hình compute giống hệt cho mọi giai đoạn, cấp dư cho các giai đoạn nhẹ và bỏ đói các giai đoạn nặng-compute, và bỏ qua streaming hoặc micro-batching vốn có thể chồng lấp xử lý giai đoạn.
- Ủy quyền truyền toàn bộ lịch sử hội thoại trên mỗi lần bàn giao, các tác nhân nhận suy ra lại ngữ cảnh mà tác nhân cha đã có, và latency bàn giao không được đo nên chi phí âm thầm tăng.

###### Các thực hành tốt

- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](agentperf05-bp01.md)
- [AGENTPERF05-BP02 Triển khai các mô hình cộng tác đa tác nhân được tối ưu](agentperf05-bp02.md)
- [AGENTPERF05-BP03 Tối ưu thực thi pipeline AI đa-giai-đoạn](agentperf05-bp03.md)
- [AGENTPERF05-BP04 Triển khai các mẫu ủy quyền và bàn giao tác nhân hiệu quả](agentperf05-bp04.md)
