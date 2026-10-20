# Tối ưu chi phí phục vụ công cụ cho agent

Các agent đánh giá tính cần thiết của công cụ (tool) trước khi gọi và cache kết quả cho các mẫu lặp lại giữ cho chi phí công cụ dự đoán được ngay cả khi các năng lực tự chủ mở rộng. Việc sử dụng công cụ của agent có thể tạo ra các cú tăng đột biến chi phí khó lường thông qua các lần gọi API quá mức, các cơn bão thử lại (retry storm) khi gọi thất bại, và hạ tầng luôn-bật mở rộng kém theo nhu cầu.

| AGENTCOST04: Làm thế nào để tối ưu chi phí gọi công cụ của agent? |
| --- |
|  |

## Mục tiêu năng lực

- Các công cụ chỉ được gọi khi cần, với các agent được thiết kế để tham vấn ngữ cảnh, bộ nhớ được quản lý và các kết quả công cụ trước đó trước khi phát ra các lần gọi mới.
- Việc lựa chọn công cụ ưu tiên các lựa chọn thay thế rẻ hơn thông qua các rubric xếp hạng theo chi phí, và các giao diện công cụ chấp nhận đầu vào theo lô để giảm chi phí trên mỗi lần gọi.
- Hạ tầng phục vụ công cụ dựa trên mức tiêu thụ và scale về không khi rảnh, với các dịch vụ dùng chung trải chi phí cố định trên nhiều agent thay vì nhân bản nó cho từng agent.
- Kết quả công cụ được cache thông qua một chiến lược nhiều lớp. Các cache phạm vi phiên phục vụ tái sử dụng trong phiên và các cache phân tán phục vụ tái sử dụng xuyên phiên, bao gồm các khớp ngữ nghĩa của các lần gọi tương đương về chức năng.
- Các thất bại được kiềm chế thông qua các điểm cắt tự động và các công cụ fallback được thiết kế để giữ chức năng agent mà không có chi phí thử lại không giới hạn.
- Các số liệu và chi phí gọi theo từng agent, từng công cụ hiển thị ở cấp phiên và chu kỳ suy luận, cho phép tối ưu có mục tiêu.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc tối ưu chi phí phục vụ công cụ cho agent nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Hạ tầng phục vụ công cụ chạy liên tục bất kể hoạt động của agent. Các công cụ được gọi mà không kiểm tra xem thông tin cần thiết đã tồn tại trong ngữ cảnh hay bộ nhớ hay chưa, và các lần thử lại về cơ bản là không giới hạn. Không có quy gán chi phí theo từng công cụ hay từng agent, và không có chiến lược caching. Các thất bại lan thành các cơn bão thử lại vì thiếu các điểm cắt. |
| 2 | Nhen nhóm (Emerging) | Phục vụ công cụ chuyển sang hạ tầng được quản lý, dựa trên mức tiêu thụ như [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) và [AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html). Caching phạm vi phiên cơ bản và exponential backoff với trần được triển khai. Các agent nhận một rubric lựa chọn công cụ xếp hạng theo chi phí trong system prompt của mình, và dữ liệu đo lường lần gọi được thu thập qua [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Quy gán chi phí tồn tại ở cấp dịch vụ nhưng hiện chưa ở cấp agent hay chu kỳ suy luận. |
| 3 | Xác định (Defined) | Các giao diện công cụ được thiết kế cho đầu vào theo lô và các tập kết quả đầy đủ. Caching phạm vi phiên được bổ sung bởi caching phân tán, xuyên phiên trên [Amazon OpenSearch Service Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html). Các điểm cắt tự động được thực thi qua [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thay vì logic ứng dụng, và các công cụ fallback giữ chức năng agent trong lúc suy giảm. Quy gán chi phí theo từng agent và từng công cụ được báo cáo qua các thẻ [AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html), và độ chính xác lựa chọn công cụ được đánh giá định kỳ với [AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html). |
| 4 | Chủ động (Proactive) | Semantic caching nhận diện các lần gọi công cụ tương đương về chức năng thông qua độ tương đồng embedding, và các giá trị time to live (TTL) của cache được hiệu chỉnh theo từng công cụ dựa trên độ biến động dữ liệu. Xác thực đầu vào trong các hàm action group [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) giúp ngăn các lần gọi lãng phí từ các lời gọi sai định dạng. Các điểm cắt và ngân sách thử lại được mã hóa trong các chính sách [Cedar](https://docs.cedarpolicy.com/) được thực thi tại ranh giới Gateway. Các dashboard thời gian thực theo dõi tỷ lệ trúng cache, các chuyển tiếp trạng thái điểm cắt, và chi phí thử lại như một tỷ lệ của tổng chi phí công cụ. |
| 5 | Tối ưu (Optimized) | Phục vụ công cụ tự tối ưu. TTL cache, ngưỡng điểm cắt và rubric lựa chọn công cụ tự điều chỉnh dựa trên tỷ lệ trúng, mẫu thất bại và kết quả chi phí quan sát được. Vô hiệu hóa cache hướng-sự-kiện xóa dữ liệu lỗi thời ngay lập tức khi các hệ thống nguồn thay đổi, hỗ trợ caching tích cực mà không lỗi thời. Các mẫu lựa chọn công cụ và thử lại được đánh giá liên tục theo các kết quả kinh doanh, và các phát hiện tối ưu được đưa ngược trở lại vào các system prompt, chính sách và hạ tầng một cách tự động. |

## Các vấn đề thường gặp cần chú ý

- Các agent gọi công cụ mà không kiểm tra ngữ cảnh hay bộ nhớ được quản lý trước, tạo ra các lần gọi trùng lặp qua các lần lặp suy luận và đẩy chi phí theo từng phiên lên.
- Các giao diện công cụ hẹp trả về dữ liệu tối thiểu, buộc các agent xâu chuỗi các lần gọi theo sau để lắp ráp ngữ cảnh đầy đủ và nhân chi phí trên mỗi lần gọi.
- Các máy chủ công cụ bền vững chạy liên tục cho các workload agent khó lường, phát sinh phí trong các cửa sổ rảnh dài khi không có agent nào gọi chúng.
- Logic thử lại không có điểm cắt tự động biến sự suy giảm dịch vụ tạm thời thành các cơn bão thử lại khuếch đại chi phí mà không giải quyết được thất bại nền tảng.
- Các chiến lược caching chỉ dựa vào tra cứu khớp chính xác và bỏ lỡ các lần gọi tương đương về chức năng mà agent diễn đạt khác nhau qua các phiên hoặc lần lặp suy luận.
- Dữ liệu đo lường lần gọi công cụ dừng ở cấp dịch vụ, làm giảm khả năng quy gán theo từng agent hay từng chu kỳ suy luận và để công sức tối ưu thiếu mục tiêu.

###### Các thực hành tốt

- [AGENTCOST04-BP01 Thiết kế lựa chọn công cụ tiết kiệm chi phí để tối thiểu các lần gọi không cần thiết](agentcost04-bp01.md)
- [AGENTCOST04-BP02 Tối ưu chi phí phục vụ công cụ thông qua serverless và chia sẻ tài nguyên](agentcost04-bp02.md)
- [AGENTCOST04-BP03 Triển khai caching thông minh và xử lý thất bại cho kết quả công cụ](agentcost04-bp03.md)
