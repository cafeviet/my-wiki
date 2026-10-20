# Giám sát, quản lý và phục hồi tác nhân

Các hệ thống tác nhân phân rã luồng công việc thành các giai đoạn phục hồi được, phân loại lỗi để thử lại có mục tiêu, và triển khai truy vết phân tán (distributed tracing) đầu-tới-cuối sẽ phục hồi mượt mà từ các lỗi xảy ra khắp nhiều thành phần của chúng.

| AGENTREL07: Các hệ thống tác nhân chịu lỗi phục hồi như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Các luồng công việc của tác nhân được phân rã thành các giai đoạn với đầu ra được lưu bền và kiểm định tường minh giữa chúng, nhờ đó các lỗi được kiềm chế ở giai đoạn bị ảnh hưởng thay vì lan qua toàn bộ luồng công việc.
- Các lỗi được phân loại trước khi thực hiện bất kỳ hành động phục hồi nào, nhờ đó thử lại áp dụng cho các lỗi thoáng qua, dự phòng áp dụng cho các lỗi bền vững, và chỉ các lỗi thực sự không thể phục hồi mới tới sự chú ý của con người.
- Các lần thử lại dùng exponential backoff kèm jitter và một ngân sách thử lại (retry budget), nhờ đó các lỗi thượng nguồn diện rộng không tạo ra các cơn bão thử lại (retry storm) vô hạn.
- Các phản hồi tự chữa lành xử lý các mẫu lỗi phổ biến một cách trực tiếp (tinh chỉnh prompt, thay thế công cụ, tái dựng ngữ cảnh) trước khi leo thang tới các dự phòng.
- Truy vết phân tán đầu-tới-cuối bao phủ mọi lần gọi tác nhân, với các chú thích đặc thù cho tác nhân và các bước suy luận ở cấp khung được bắt trong cùng một góc nhìn vết.
- Các vết, số liệu và log được tương quan trong các bảng điều khiển hợp nhất, nhờ đó người vận hành chẩn đoán sự cố từ bằng chứng thay vì phải xoay qua lại giữa các công cụ.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với giám sát, quản lý và phục hồi tác nhân như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Các luồng công việc của tác nhân chạy như các tiến trình đơn khối, nên bất kỳ lỗi nào cũng gây ra khởi động lại hoàn toàn và mất công việc. Các lần thử lại được áp dụng đồng nhất, bao gồm cả với các lỗi không thể thử lại, và không có exponential backoff hay jitter. Truy vết bị giới hạn ở ranh giới ứng dụng, và những người xử lý sự cố tái dựng đường thực thi từ log. Các hành động phục hồi là thủ công. |
| 2 | Manh nha (Emerging) | Một vài luồng công việc chạy lâu được chia thành các giai đoạn, và các lần thử lại dùng exponential backoff cho một tập giới hạn các lỗi được biết là thoáng qua. Các cảnh báo [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) thông báo cho người vận hành khi tỷ lệ lỗi tăng cao. Truy vết được thêm cho các đường trọng yếu nhưng không lan qua các ranh giới hàng đợi. Việc phân loại lỗi tồn tại trong mã một lần thay vì một thư viện dùng chung. |
| 3 | Xác lập (Defined) | Các luồng công việc được điều phối trong [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) với lưu bền trạng thái tại mỗi chuyển tiếp và [redrive](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html) được bật cho phục hồi tăng dần. Việc phân loại lỗi được chuẩn hóa trong một thư viện dùng chung, và các lần thử lại dùng exponential backoff với full jitter. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bắt các vết đầu-tới-cuối qua các thành phần tác nhân, và [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) thực thi các ngân sách thử lại. Việc kiểm định ở cấp giai đoạn giúp ngăn các lỗi lan truyền qua các giai đoạn sau. |
| 4 | Chủ động (Proactive) | Các phản hồi tự chữa lành xử lý các mẫu lỗi phổ biến một cách trực tiếp (tinh chỉnh prompt, thay thế công cụ, tái dựng ngữ cảnh) trước khi các dự phòng vào cuộc. Các chiến lược dự phòng định tuyến các lỗi bền vững tới các phản hồi suy giảm, các câu trả lời cache, hoặc các hàng đợi rà soát của con người thay vì trả về lỗi. Truy vết phân tán bao gồm các chú thích đặc thù cho tác nhân và các bước suy luận của [Strands Agents](https://strandsagents.com/docs/user-guide/observability-evaluation/traces/), và bối cảnh vết lan truyền qua mọi đường giao tiếp bao gồm các thông điệp bất đồng bộ. [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) kiểm định rằng các đầu ra được phục hồi khớp với các đường cơ sở chất lượng trước-khi-lỗi. |
| 5 | Tối ưu (Optimized) | Các chiến lược phục hồi được tinh chỉnh liên tục dựa trên các số liệu phục hồi và phân tích vết. Các đường dự phòng được kiểm thử cùng với các triển khai chính, và việc phân rã giai đoạn được dẫn dắt bởi các mẫu lỗi và timeout quan sát được. Cảnh báo dựa trên vết bắn khi có bất thường trước khi chúng trở thành sự cố, và các bảng điều khiển tương quan biến các vết, số liệu và log thành một bề mặt điều tra duy nhất. Tổ chức công bố các mẫu phục hồi nội bộ và chia sẻ các bài học giữa các đội. |

## Các vấn đề thường gặp cần lưu ý

- Các luồng công việc chạy lâu chạy như các tiến trình đơn khối, nên một lỗi muộn trong luồng công việc làm mất toàn bộ tiến độ và buộc khởi động lại hoàn toàn.
- Logic thử lại được áp dụng đồng nhất cho mọi lỗi, thử lại các lỗi không thể thử lại vốn sẽ không bao giờ thành công và trì hoãn việc con người can thiệp để giải quyết chúng.
- Các lần thử lại chạy ở các khoảng cố định mà không có exponential backoff hay jitter, tạo ra các hiệu ứng "đàn sấm sét" (thundering herd) khuếch đại sự cố thay vì phục hồi từ chúng.
- Chỉ triển khai phục hồi dựa trên thử lại, nên các lỗi bền vững sau khi thử lại trở thành các lỗi mà người dùng nhìn thấy thay vì suy giảm qua một dự phòng.
- Truy vết dừng ở ranh giới ứng dụng hoặc ở các ranh giới hàng đợi, nên việc gỡ lỗi trong các hệ thống đa tác nhân phụ thuộc vào tương quan log thủ công qua các dịch vụ.
- Các vết được bắt mà không có các chú thích đặc thù cho tác nhân, nên các truy vấn vết không thể lọc xuống đúng tác nhân, loại tác vụ hay mô hình đã lỗi.

###### Các thực hành tốt

- [AGENTREL07-BP01 Thiết kế luồng công việc theo giai đoạn với phục hồi tăng dần](agentrel07-bp01.md)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi của tác nhân](agentrel07-bp02.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và tạo điều kiện phục hồi](agentrel07-bp03.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
