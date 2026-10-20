# Vòng đời agent và các quy trình triển khai

Quản lý vòng đời agent vượt ra ngoài triển khai phần mềm truyền thống để bao gồm sự tiến hóa hành vi, cập nhật năng lực, và quản trị vận hành. Các agent đòi hỏi quản lý liên tục khi chúng thích ứng với yêu cầu kinh doanh đang thay đổi, tích hợp các Tools mới, và mở rộng quy mô qua các môi trường khác nhau.

| AGENTOPS03: Bạn quản lý vòng đời agent và các quy trình triển khai như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Mỗi agent có một chủ sở hữu được tài liệu hóa, một trạng thái vòng đời, và một tập tiêu chí chuyển tiếp, từ phát triển ban đầu đến ngừng vận hành gọn gàng.
- Các thay đổi agent đến được sản xuất qua các pipeline triển khai tự động với các cổng chất lượng đặc thù agent, triển khai theo giai đoạn, và quay lui tự động khi có hồi quy.
- Dung lượng agent điều chỉnh theo nhu cầu workload trong các ranh giới theo từng môi trường, và các triển khai được giữ đúng kích cỡ (right-sized) qua các buổi rà soát dung lượng định kỳ.
- Danh mục agent hiển thị trong một catalog duy nhất với các phụ thuộc liên nhóm được theo dõi, để các nhóm khám phá các năng lực hiện có trước khi xây dựng agent mới.
- Việc hợp lý hóa ở cấp danh mục (ngừng vận hành, hợp nhất, tiếp tục đầu tư) được dẫn dắt bởi bằng chứng về mức sử dụng, chi phí, và giá trị kinh doanh thay vì sở thích ở cấp nhóm.

## Các mức độ trưởng thành

Các mức độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với vòng đời agent và các quy trình triển khai như một tổng thể.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Vòng đời agent mang tính phi chính thức. Các nhóm tạo agent theo yêu cầu, thường đưa thẳng vào sản xuất, không có giai đoạn được tài liệu hóa, không có registry, và không có chủ sở hữu được chỉ định. Các triển khai là thủ công. Không có CI/CD đặc thù agent hay đánh giá hành vi. Việc scaling là tĩnh hoặc theo từng workload và chỉ xem lại khi có gì đó hỏng. Không tồn tại tầm nhìn ở cấp danh mục xuyên các nhóm. |
| 2 | Manh nha (Emerging) | Một vòng đời với các giai đoạn được xác định tồn tại trên giấy và hầu hết các nhóm tuân theo nó. Các agent được theo dõi trong một registry ở cấp nhóm. CI/CD cơ bản chạy unit test, và các triển khai dùng các mẫu hạ tầng như mã. Ranh giới scaling theo từng môi trường được đặt thủ công. Các nhóm có thể liệt kê các agent họ sở hữu, nhưng không có catalog liên nhóm hay góc nhìn về phụ thuộc. |
| 3 | Được định nghĩa (Defined) | Các giai đoạn vòng đời được chuẩn hóa xuyên tổ chức với các cổng kiểm định tại mỗi lần chuyển tiếp. Các pipeline AgentOps bao gồm đánh giá đặc thù agent qua [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) và triển khai theo giai đoạn qua đánh phiên bản [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html). Auto-scaling được điều khiển bởi các chỉ số đặc thù agent thay vì CPU hay bộ nhớ thô. Một catalog agent dùng chung đang manh nha, và các buổi rà soát danh mục theo quý đầu tiên được tổ chức. |
| 4 | Chủ động (Proactive) | Các chuyển tiếp vòng đời được tự động hóa hoàn toàn, bao gồm công tắc chấm dứt khẩn cấp (emergency termination switch) và các runbook ngừng vận hành. Các cổng hành vi CI/CD chặn phát hành khi độ chính xác tác vụ hoặc ngưỡng ảo giác (hallucination) suy giảm, với quay lui tự động từ các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html). Các chính sách scaling, được lưu tập trung, điều chỉnh khi các agent di chuyển giữa các giai đoạn vòng đời. [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) với tìm kiếm năng lực theo ngữ nghĩa và thông báo phụ thuộc [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) là đường mặc định cho việc tạo agent mới. |
| 5 | Tối ưu (Optimized) | Quản lý vòng đời, triển khai, scaling, và danh mục được hệ thống hóa bằng chính sách và liên tục được tinh chỉnh từ dữ liệu vận hành. Một đồ thị phụ thuộc (dependency graph) hậu thuẫn phân tích tác động trước bất kỳ thay đổi agent nào. Việc hợp lý hóa danh mục (hợp nhất, ngừng vận hành, tái đầu tư) chạy như một nhịp vận hành đều đặn với đo lường giá trị kinh doanh. Chi phí quản trị mở rộng dưới tuyến tính (sub-linearly) theo số lượng agent, và tổ chức đóng góp các mẫu của mình trở lại ngành. |

## Các vấn đề thường gặp cần lưu ý

- Các agent tích tụ trong sản xuất mà không có chủ sở hữu hay trạng thái vòng đời được tài liệu hóa, khiến việc ngừng vận hành và ứng phó sự cố bị đình trệ vì không ai biết ai chịu trách nhiệm cho mỗi agent.
- Các triển khai agent dựa vào CI/CD phần mềm truyền thống mà không có đánh giá hành vi đặc thù agent, để các hồi quy Prompt hoặc Tools đến được người dùng mà unit test không bao giờ bắt được.
- Việc scaling được cấu hình giống hệt nhau qua các môi trường, hoặc lãng phí chi phí ở phát triển hoặc làm suy giảm độ trễ sản xuất trong các đợt tăng vọt lưu lượng.
- Các nhóm xây dựng các agent trùng lặp song song vì tổ chức thiếu một catalog dùng chung và đường khám phá, làm phình chi phí và gánh nặng vận hành mà không thêm năng lực.
- Các phụ thuộc agent liên nhóm không được tài liệu hóa, khiến việc dừng hoặc sửa đổi một agent thượng nguồn gây ra các lỗi lan truyền trong các agent hạ nguồn vốn âm thầm tiêu thụ nó.

###### Các thực hành tốt

- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](agentops03-bp01.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](agentops03-bp02.md)
- [AGENTOPS03-BP03 Triển khai các chính sách scaling đặc thù agent và lập kế hoạch dung lượng](agentops03-bp03.md)
- [AGENTOPS03-BP04 Triển khai quản lý và quản trị danh mục agent ở cấp tổ chức theo quy mô](agentops03-bp04.md)
