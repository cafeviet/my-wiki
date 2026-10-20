# AGENTOPS02-BP03 Triển khai năng lực đánh phiên bản và quay lui hành vi agent

Các nhóm có hành vi được đánh phiên bản và quay lui đã được kiểm thử có thể phục hồi trong vài phút khi một agent hành xử bất thường, trong khi các nhóm không có sẽ mất hàng giờ gỡ lỗi dưới áp lực. Khả năng đảo ngược nhanh chóng cải thiện năng lực của tổ chức trong việc tự tin lặp lại trên một hệ thống agentic.

**Kết quả mong muốn:**

- Mỗi cấu hình hành vi của agent (system prompt, chỉ dẫn suy luận, quyền của Tools, và ranh giới quyết định) được đánh phiên bản với lịch sử thay đổi đầy đủ.
- Bạn có thể quay lui về bất kỳ phiên bản hành vi trước nào trong vòng vài phút khi một thay đổi tạo ra kết quả không mong muốn.
- Các quy trình quay lui được tự động hóa và kiểm thử thường xuyên, không phải ứng biến trong lúc sự cố.
- Các triển khai theo giai đoạn giới hạn phạm vi tác động của các thay đổi hành vi, và kiểm thử A/B hỗ trợ so sánh các biến thể dựa trên dữ liệu trước khi triển khai toàn bộ.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các thay đổi hành vi tới 100% lưu lượng ngay lập tức mà không có triển khai theo giai đoạn, khuếch đại tối đa phạm vi tác động khi một thay đổi tạo ra kết quả không mong muốn.
- Vận hành mà không có một baseline hành vi được xác định, tức cấu hình tốt cuối cùng đã biết, khiến việc quay lui trở thành cuộc tìm kiếm thủ công xem phiên bản trước nào ổn định.
- Xem các thay đổi Prompt là rủi ro thấp vì chúng không liên quan đến thay đổi mã, bỏ qua đánh giá và triển khai theo giai đoạn cho các sửa đổi có thể làm biến đổi căn bản hành vi agent.
- Chạy kiểm thử A/B mà không có kỷ luật thống kê, ra quyết định triển khai từ nhiễu thay vì tín hiệu.

**Lợi ích khi áp dụng thực hành tốt này:**

- Đánh phiên bản và quay lui có hệ thống tạo ra một tấm lưới an toàn cho phép các nhóm lặp lại trên hành vi agent một cách tự tin, biết rằng bất kỳ thay đổi nào cũng có thể được đảo ngược nhanh chóng.
- Các khung kiểm thử A/B và các baseline hành vi cung cấp nền tảng thực nghiệm cho cải tiến liên tục, kiểm định rằng mỗi lần lặp tạo ra lợi ích đo lường được.
- Các triển khai theo giai đoạn giới hạn số người dùng bị ảnh hưởng bởi một hồi quy, cho nhóm thời gian phát hiện và sửa chữa trước khi phơi nhiễm toàn bộ.
- Đánh giá tác động thay đổi gắn các dịch chuyển chỉ số chất lượng với các phiên bản hành vi cụ thể, khiến việc quy kết trở nên trực tiếp thay vì suy luận gián tiếp.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html) xử lý các cấu hình dựa trên Prompt với đánh phiên bản ngữ nghĩa (semantic versioning) tích hợp sẵn, metadata, và tích hợp với đánh giá. Các cấu hình phi Prompt (quyền của Tools, ranh giới quyết định, và ngưỡng leo thang) nên được lưu trong một kho cấu hình có phiên bản với theo dõi thay đổi. Mỗi phiên bản nên mang một số phiên bản ngữ nghĩa, một mô tả thay đổi, một tác giả, và một tham chiếu tới kết quả đánh giá của nó.

Một baseline hành vi là một phiên bản mà nhóm đã chỉ định rõ ràng là tốt đã biết, chứ không chỉ là phiên bản trước đó, vì phiên bản trước có thể đã được đưa ra một giờ trước và chưa từng chứng minh sự ổn định. Quay lui nên khôi phục baseline, không phải thay đổi cuối cùng, trừ khi nhóm đã thăng hạng rõ ràng thay đổi đó lên trạng thái baseline. Không có một baseline được chỉ định, quay lui đòi hỏi phải tìm kiếm qua nhiều phiên bản để tìm một cấu hình ổn định.

Bản thân việc quay lui nên được tự động hóa và diễn tập. Hãy thiết kế quay lui như một luồng công việc tự động được kích hoạt bởi hoặc phê duyệt thủ công hoặc vi phạm ngưỡng chất lượng tự động từ các cảnh báo [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/). Thời gian mục tiêu để khôi phục nên dưới năm phút cho các thay đổi hành vi. Bất cứ điều gì lâu hơn nghĩa là luồng công việc có quá nhiều bước thủ công hoặc quá nhiều phụ thuộc chưa được chuẩn bị sẵn. Hãy diễn tập việc quay lui theo quý để quy trình luôn cập nhật với runtime. Ví dụ, một quay lui được viết sáu tháng trước và chưa từng chạy là một quay lui có thể không hoạt động.

Triển khai theo giai đoạn giới hạn phạm vi tác động trước khi việc quay lui trở nên cần thiết. Định tuyến có trọng số dựa trên endpoint của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) khiến điều này trở nên đơn giản. Hãy khởi động một phiên bản hành vi mới ở 5–10% lưu lượng, giám sát các chỉ số chất lượng, và chỉ thăng hạng khi tín hiệu sạch. Kiểm thử A/B sử dụng cùng cỗ máy cho mục đích khác, chia lưu lượng giữa các biến thể để đo biến thể nào hoạt động tốt hơn. Các bổ sung then chốt là các chỉ số theo từng biến thể trong CloudWatch và kiểm định ý nghĩa thống kê trước các quyết định triển khai. Hãy tài liệu hóa các tiêu chí đánh giá và kết quả bên cạnh hồ sơ phiên bản hành vi để việc so sánh có thể tái lập.

Hãy thực hiện các đánh giá tác động, trong đó bạn tương quan các mốc thời gian triển khai phiên bản với các thay đổi trong chỉ số chất lượng để quy các dịch chuyển chỉ số về các cập nhật hành vi cụ thể. Khi một chỉ số dịch chuyển, nhóm nên nhanh chóng xác định phiên bản nào đã gây ra vấn đề thay vì phải đối chiếu các dashboard khác nhau để tìm phiên bản có vấn đề.

### Các bước triển khai

- **Bật đánh phiên bản ngữ nghĩa cho Prompt:** Cấu hình [Amazon Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html) với các trường metadata cho mô tả thay đổi, tác giả, và kết quả đánh giá trên mỗi phiên bản.
- **Đánh phiên bản các cấu hình phi Prompt:** Lưu quyền của Tools, ranh giới quyết định, và ngưỡng leo thang trong một kho cấu hình có phiên bản với theo dõi thay đổi và thông báo.
- **Chỉ định các baseline hành vi:** Gắn thẻ (tag) và tài liệu hóa cấu hình tốt cuối cùng đã biết cho mỗi agent làm mục tiêu quay lui, tách biệt với phiên bản gần nhất.
- **Tự động hóa quay lui:** Xây dựng các luồng công việc khôi phục baseline trong vòng năm phút, được kích hoạt bởi phê duyệt thủ công hoặc vi phạm ngưỡng chất lượng tự động từ các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html).
- **Cấu hình triển khai theo giai đoạn:** Dùng định tuyến có trọng số dựa trên endpoint của [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) khởi đầu ở 5–10% lưu lượng cho các phiên bản hành vi mới, với các cổng thăng hạng tự động.
- **Thiết lập hạ tầng kiểm thử A/B:** Nắm bắt các chỉ số theo từng biến thể trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) với theo dõi ý nghĩa thống kê trước các quyết định triển khai.
- **Tương quan triển khai với các dịch chuyển chỉ số:** Ghi lại các mốc thời gian triển khai bên cạnh các xu hướng chỉ số chất lượng để các thay đổi có thể được quy về các phiên bản cụ thể.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](agentops02-bp01.md)
- [AGENTOPS02-BP02 Triển khai phát hiện và khắc phục trôi lệch cấu hình](agentops02-bp02.md)
- [AGENTOPS03-BP02 Triển khai các pipeline CI/CD phù hợp với việc triển khai hệ thống agentic (AgentOps)](../3-agentops03/agentops03-bp02.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)
- [Triển khai AI agent trên Amazon Bedrock AgentCore bằng GitHub Actions](https://aws.amazon.com/blogs/machine-learning/deploy-ai-agents-on-amazon-bedrock-agentcore-using-github-actions/)

**Video liên quan:**

- [AWS re:Invent 2024 - Architecting scalable and secure agentic AI with AgentCore (AIM431)](https://www.youtube.com/watch?v=wqmeZOT6mmc)
- [AWS re:Invent 2024 - Amazon Bedrock Agents and AgentCore Design Patterns (TNC322)](https://www.youtube.com/watch?v=GYlPFmrATjU)

**Ví dụ liên quan:**

- [GitHub: Sample Agentic Platform on AWS](https://github.com/aws-samples/sample-agentic-platform)
- [GitHub: Amazon Bedrock Samples, GenAI Quick-Start PoCs](https://github.com/aws-samples/genai-quickstart-pocs)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
