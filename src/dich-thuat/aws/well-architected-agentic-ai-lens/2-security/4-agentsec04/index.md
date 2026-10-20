# Căn chỉnh mục tiêu của agent và phòng chống thao túng

Agent có thể bị điều hướng để theo đuổi các mục tiêu ngoài ý muốn hoặc thể hiện các hành vi ngoài phạm vi đã định của nó. Nếu không có cơ chế căn chỉnh mục tiêu (goal alignment), agent có thể thực hiện các hành động xung đột với chính sách của tổ chức hoặc ý định của người dùng. Việc triển khai các rào chắn (Guardrails), các kiểm soát kiểm định nhiều lớp và các phê duyệt human-in-the-loop giúp kiểm chứng rằng agent hoạt động trong các ranh giới dự định.

| AGENTSEC04: Bạn hỗ trợ căn chỉnh mục tiêu của agent và phòng chống thao túng như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các ranh giới vận hành và chính sách cho mỗi agent được định nghĩa trước và thực thi qua các kiểm soát nhiều lớp thay vì chỉ dựa vào các chỉ thị trong prompt.
- Thực thi xác định (giới hạn phạm vi IAM, kiểm định lược đồ đầu vào và các bộ máy chính sách) và các kiểm soát nội dung theo xác suất (lọc đầu vào và đầu ra, đánh giá hành vi) hoạt động ở các giai đoạn riêng biệt của chuỗi lời gọi, nên một thất bại ở một lớp hiếm khi dẫn đến vi phạm ranh giới.
- Phân loại rủi ro là xác định, với các thao tác rủi ro cao được định tuyến tới rà soát của con người trước khi thực thi và các thao tác rủi ro thấp thường lệ tiến hành tự chủ.
- Người rà soát nhận đủ ngữ cảnh quyết định, các chính sách timeout và các đường leo thang để đưa ra các phê duyệt có hiểu biết mà không làm đình trệ luồng công việc hay mặc định phê duyệt máy móc (rubber-stamping).
- Các can thiệp của guardrail, các quyết định phê duyệt và các kết quả đánh giá được ghi log, cảnh báo và rà soát theo một nhịp đã định để giữ các chính sách cập nhật với các mẫu mới nổi.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc căn chỉnh mục tiêu của agent và phòng chống thao túng như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Các ranh giới vận hành chỉ tồn tại dưới dạng các chỉ thị ngôn ngữ tự nhiên trong system prompt. Không có guardrail nội dung, kiểm định đầu vào hay các kiểm soát human-in-the-loop nào tại chỗ. Căn chỉnh phụ thuộc vào việc mô hình tuân theo chỉ thị, và một đầu vào đối kháng đơn lẻ có thể điều hướng lại agent mà không có chiều sâu phòng thủ. |
| 2 | Manh nha (Emerging) | [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) được cấu hình với các [bộ lọc nội dung (content filters)](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filter.html) cơ bản bao gồm đầu vào và đầu ra. Một tầng phê duyệt duy nhất tồn tại cho một tập con các hành động hệ trọng, được hiện thực qua các cơ chế dựng sẵn như [xác nhận người dùng của Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html) hoặc định tuyến qua các kênh tạm bợ như email hay chat. Các can thiệp guardrail được ghi vào log nhưng được rà soát không đều. |
| 3 | Được định nghĩa (Defined) | Các cấu hình guardrail phân tầng căn chỉnh cường độ bộ lọc với ca sử dụng của từng agent, và [các chủ đề bị cấm và bộ lọc từ (denied topics and word filters)](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters-overview.html) được hiệu chỉnh theo từng hồ sơ rủi ro. Phân loại rủi ro xác định định tuyến các phê duyệt qua một cơ chế luồng công việc có cấu trúc như [các luồng công việc callback của AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) hoặc [trả về quyền kiểm soát (return of control)](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html), với các timeout và đường leo thang đã định. [Các cảnh báo Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html) kích hoạt khi có các đợt tăng đột biến can thiệp, và việc quản lý phiên bản guardrail hỗ trợ khôi phục (rollback) các thay đổi chính sách. |
| 4 | Chủ động (Proactive) | Kiểm định chạy ở mọi giai đoạn của chuỗi lời gọi: đầu vào, suy luận, đầu ra và gọi công cụ. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy theo một nhịp đã định với các cảnh báo về độ đúng đắn, độ chính xác lựa chọn công cụ và trôi dạt điểm an toàn. Các cấp phép tin cậy bền vững được giới hạn phạm vi hẹp theo lệnh và hình dạng tham số, phân tầng theo rủi ro, và được làm cho có thể kiểm toán và thu hồi. Ngữ cảnh quyết định đầy đủ được ghi vào kho lưu trữ bền vững trước các thông báo phê duyệt, và các bản ghi phê duyệt được liên kết với dấu vết kiểm toán tập trung. |
| 5 | Tối ưu (Optimized) | Các kiểm soát căn chỉnh được hiệu chỉnh từ dữ liệu can thiệp và đánh giá, và phân loại rủi ro thích ứng với các tín hiệu động như tần suất thao tác, giờ trong ngày và vị trí nguồn. Đồng thuận nhiều người rà soát (multi-reviewer consensus) khả dụng cho các thao tác rủi ro cao nhất, bao gồm các luồng công việc bất đồng bộ chạy trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html). Các cập nhật chính sách chảy qua các cấu hình có quản lý phiên bản với lịch sử thay đổi có thể chứng minh, và vòng phản hồi từ các can thiệp được ghi log trở lại chính sách được tự động hóa thay vì thủ công. |

## Các vấn đề thường gặp cần lưu ý

- Căn chỉnh được coi như một bài tập kỹ thuật prompt (prompt-engineering) thay vì một vấn đề thực thi nhiều lớp, nên một đầu vào đối kháng đơn lẻ tác động đến mô hình có thể làm sụp đổ nhiều ranh giới cùng lúc.
- Lọc nội dung chỉ được áp dụng cho đầu ra của mô hình, để ngỏ đường suy luận cho prompt injection và tiêu tốn năng lực trên các đầu vào đối kháng lẽ ra có thể bị từ chối ngay từ đầu.
- Một hồ sơ guardrail duy nhất được áp dụng cho mọi agent, điều này hoặc ràng buộc quá mức các agent thông tin rủi ro thấp hoặc để các agent vận hành rủi ro cao bị ràng buộc dưới mức.
- Các luồng công việc phê duyệt hoặc định tuyến mọi hành động qua rà soát của con người (tạo ra sự mệt mỏi của người rà soát và phê duyệt máy móc) hoặc bỏ qua rà soát cho các thao tác đáng được rà soát, cho cả hai cực tệ nhất.
- Phân loại rủi ro được ủy thác cho một LLM tiếp xúc với cùng nội dung không đáng tin như yêu cầu mà nó đang đánh giá, điều này có thể bị tác động để đánh dấu yêu cầu đó là rủi ro thấp.

###### Các thực hành tốt

- [AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh](agentsec04-bp01.md)
- [AGENTSEC04-BP02 Human-in-the-loop cho các quyết định quan trọng](agentsec04-bp02.md)
