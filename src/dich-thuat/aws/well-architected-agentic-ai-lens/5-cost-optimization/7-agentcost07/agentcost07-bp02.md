# AGENTCOST07-BP02 Thiết lập phát hiện bất thường chủ động cho các mẫu chi phí của agent

Các cảnh báo tính hóa đơn chung giúp bạn tìm ra leo thang chi phí nhanh hơn sau khi nó bắt đầu. Phát hiện bất thường đặc thù theo agent bắt các cú tăng đột biến token vòng lặp suy luận, các cơn bão gọi công cụ, và tăng trưởng bộ nhớ nhanh chóng, và việc định tuyến các cảnh báo đó đúng cách nghĩa là bạn có thể cảnh báo nhóm sở hữu agent thay vì nhóm vận hành.

**Kết quả mong muốn:**

- Bạn thiết lập phát hiện bất thường dựa trên ML với các đường cơ sở thống kê và các ngưỡng lệch.
- Bạn có các bộ phát hiện tùy chỉnh cho các chế độ lỗi đặc thù theo agent vượt ra ngoài giám sát hạ tầng chung.
- Bạn ghép mỗi loại bất thường với một runbook điều tra để tăng tốc việc giải quyết.
- Bạn tương quan các bất thường để định tuyến các vấn đề do agent điều khiển tới các nhóm phát triển và các vấn đề hạ tầng tới các nhóm vận hành.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai phát hiện bất thường mà không có đủ dữ liệu cơ sở, tạo ra các dương tính giả quá mức làm suy giảm sự tin tưởng của nhóm.
- Chỉ dựa vào giám sát hạ tầng chung vốn bỏ lỡ các chế độ lỗi đặc thù theo agent đang đẩy các chi phí cao nhất.
- Phát hiện các bất thường mà không có các runbook điều tra, để chi phí leo thang trong khi các nhóm loay hoay tìm ra các quy trình chẩn đoán khi các vấn đề xảy ra.
- Coi mọi cú tăng đột biến chi phí là tương đương trong khi các cú tăng đột biến của agent có các nguyên nhân gốc khác nhau (vòng lặp suy luận, cơn bão công cụ, tăng trưởng bộ nhớ) đòi hỏi các biện pháp khắc phục khác nhau.
- Thu thập các hiểu biết về bất thường mà không đưa chúng ngược trở lại vào các thay đổi thiết kế agent (giới hạn số vòng lặp chặt hơn, các prompt tốt hơn, caching công cụ) vốn giúp ngăn tái diễn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phát hiện chủ động xác định leo thang chi phí từ các chế độ lỗi đặc thù theo agent trong vòng vài phút thay vì vài ngày.
- Các runbook điều tra giảm thời gian trung bình để giải quyết bằng cách thay phân tích ad-hoc bằng việc thực thi chẩn đoán có hướng dẫn.
- Phân tích tương quan định tuyến các cảnh báo tới đúng nhóm (phát triển agent hoặc vận hành), giúp ngăn các độ trễ phân loại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Phát hiện bất thường cần các đường cơ sở thực trước khi hữu ích. Thu thập 2 đến 4 tuần dữ liệu vận hành cơ sở trước khi đặt các ngưỡng, vì các bộ phát hiện được cấu hình trên lịch sử không đủ tạo ra các dương tính giả làm xói mòn sự tin tưởng vào toàn bộ hệ thống. [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) tự động học các đường cơ sở thống kê cho các số liệu chi phí agent và tạo các dải bất thường động thích nghi với tính mùa vụ và các xu hướng. Áp dụng nó cho các số liệu [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bao gồm tiêu thụ token theo từng phiên, tần suất gọi công cụ, tăng trưởng bộ nhớ, và chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ. Dùng 2σ cho cảnh báo và 3σ cho các cảnh báo nghiêm trọng.

Giám sát hạ tầng chung không bắt được các chế độ lỗi tốn nhiều tiền nhất của agent. Các cú tăng đột biến token vòng lặp suy luận, các cơn bão gọi công cụ, và tăng trưởng bộ nhớ là các mẫu đặc thù theo agent, và chúng cần các bộ phát hiện đặc thù theo agent. Các ngưỡng khởi đầu hợp lý bao gồm:

- Các cú tăng đột biến token vòng lặp suy luận ở mức 5 lần trung bình phiên
- Các cơn bão gọi công cụ ở mức 3 lần tốc độ cơ sở
- Tăng trưởng lưu trữ bộ nhớ ở mức 2 lần mỗi giờ
- Leo thang chi phí luồng đa agent ở mức 2 lần trung bình lịch sử

Các ngưỡng này bắt hành vi bệnh lý đủ sớm để giúp ngăn tác động chi phí đáng kể.

Phân tích tương quan giúp làm cho định tuyến trở thành một lựa chọn hợp lý. Một bất thường do agent điều khiển tương quan với các agent ID cụ thể trong các thẻ phân bổ chi phí và hiện lên trong các mẫu tiêu thụ token hoặc gọi của AgentCore Observability. Một bất thường hạ tầng xảy ra độc lập với hành vi agent và hiện lên trong các số liệu dịch vụ chung. Định tuyến các bất thường do agent điều khiển tới các nhóm phát triển (với ngữ cảnh về mẫu suy luận nào kích hoạt cú tăng đột biến) và các bất thường hạ tầng tới các nhóm vận hành (với ngữ cảnh về các tài nguyên bị ràng buộc) giữ các cảnh báo trước những người có thể hành động về chúng. Phân tích span của AgentCore Observability đào sâu thêm. Cú tăng đột biến ở trong token planning, các lần gọi công cụ, hay tăng trưởng bộ nhớ? Điều đó xác định liệu bản sửa là một thay đổi prompt, một cache công cụ, hay một chính sách bộ nhớ chặt hơn.

[AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) cung cấp một lớp dự phòng ở cấp tính hóa đơn. Được cấu hình theo từng thẻ phân bổ chi phí agent, nó bắt các leo thang từ từ không hiển thị trong các số liệu vận hành. Các runbook điều tra cho mỗi loại bất thường (các truy vấn chẩn đoán, các nguyên nhân gốc khả dĩ, và các hành động khắc phục tức thời) sống trong AWS Systems Manager OpsCenter, với các truy vấn CloudWatch Logs Insights cho các vết, AWS X-Ray cho các luồng công việc phân tán, và phân tích span của AgentCore Observability cho các mẫu token.

### Các bước triển khai

- **Thiết lập đường cơ sở, rồi phát hiện:** Thu thập 2 đến 4 tuần dữ liệu cơ sở bằng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), rồi cấu hình [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) trên các chỉ số chi phí then chốt với các ngưỡng cảnh báo 2σ và nghiêm trọng 3σ.
- **Triển khai các bộ phát hiện đặc thù theo agent:** Triển khai các bộ phát hiện dựa trên Lambda cho các cú tăng đột biến token vòng lặp suy luận (5 lần trung bình phiên), các cơn bão gọi công cụ (3 lần tốc độ cơ sở), các bất thường tăng trưởng bộ nhớ (2 lần mỗi giờ), và leo thang chi phí luồng công việc (2 lần trung bình lịch sử), xuất bản các sự kiện bất thường có cấu trúc sang Amazon EventBridge.
- **Thêm độ bao phủ bất thường ở cấp tính hóa đơn:** Cấu hình các monitor [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) theo từng thẻ phân bổ chi phí agent như một lớp dự phòng cho các leo thang từ từ.
- **Tạo các runbook điều tra:** Lưu các runbook cho mỗi loại bất thường trong AWS Systems Manager OpsCenter, với các truy vấn chẩn đoán (Amazon CloudWatch Logs Insights cho các vết, AWS X-Ray cho các luồng công việc phân tán, phân tích span của AgentCore Observability cho các mẫu token) và các hành động khắc phục.
- **Định tuyến các bất thường thông qua phân tích tương quan:** Phân loại các bất thường bằng các thẻ phân bổ chi phí và các chiều AgentCore Observability, định tuyến các bất thường do agent điều khiển tới các nhóm phát triển và các bất thường hạ tầng tới các nhóm vận hành.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)
- [AGENTCOST07-BP01 Triển khai kiểm soát chi phí tự động với các điểm cắt thông minh](agentcost07-bp01.md)
- [AGENTCOST07-BP03 Tạo các vòng lặp phản hồi tối ưu có hệ thống để cải thiện liên tục](agentcost07-bp03.md)

**Tài liệu liên quan:**

- [Amazon CloudWatch Anomaly Detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)
- [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Observability tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Dịch vụ liên quan:**

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
