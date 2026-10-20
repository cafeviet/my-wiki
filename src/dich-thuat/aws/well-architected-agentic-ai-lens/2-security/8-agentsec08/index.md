# Bảo vệ đầu vào và đầu ra của agent

Agent xử lý các đầu vào từ người dùng, công cụ (Tools) và các agent khác, và chúng sinh các đầu ra cho các hệ thống phía sau, các kho bộ nhớ và người dùng cuối. Nếu không có kiểm định phù hợp, các đầu vào đối kháng như prompt injection có thể tác động đến hành vi của agent, và các đầu ra của agent có thể vô tình tiết lộ thông tin nhạy cảm hoặc sinh nội dung có hại. Kiểm định nhiều lớp ở cả ranh giới đầu vào lẫn đầu ra giúp kiểm chứng rằng agent hoạt động an toàn trong phạm vi dự định của nó.

| AGENTSEC08: Bạn kiểm định và bảo vệ đầu vào và đầu ra của agent như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Mọi bề mặt đầu vào của agent (thông điệp trực tiếp của người dùng, đầu ra công cụ, thông điệp giữa các agent, nội dung ngoài được truy xuất, và các lần đọc bộ nhớ) đều có kiểm định phù hợp với hồ sơ rủi ro của nó, không có đầu vào nào tới quá trình suy luận của agent mà chưa được kiểm tra.
- Prompt injection gián tiếp qua các tài liệu được truy xuất, các trang web và các phản hồi API được coi là một rủi ro hạng nhất và được lọc với cùng sự nghiêm ngặt áp dụng cho các đầu vào trực tiếp của người dùng.
- Các đầu ra của agent được kiểm tra tìm thông tin định danh cá nhân (PII), thông tin xác thực và dữ liệu nhạy cảm khác trên mọi đường ra (các phản hồi cho người dùng, các thông điệp giữa các agent, các lượt ghi bộ nhớ, và các log kiểm toán), với việc che hoặc chặn nhất quán được áp dụng tại mỗi ranh giới.
- Độ nghiêm ngặt của kiểm định được hiệu chỉnh theo khả năng xảy ra và tác động của từng kịch bản rủi ro thay vì được áp dụng đồng nhất, và dữ liệu đo lường về các điểm độ tin cậy, nội dung bị chặn và các tỷ lệ dương tính giả thúc đẩy điều chỉnh liên tục.
- Các quyết định lọc và guardrail được ghi log với đủ ngữ cảnh để hỗ trợ kiểm toán tuân thủ, để phát hiện các mẫu rò rỉ dữ liệu mang tính hệ thống, và để cung cấp cho việc tái tối ưu định kỳ các chủ đề bị cấm, các prompt mẫu và các ngưỡng bộ lọc.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt diện mạo của từng giai đoạn trưởng thành đối với việc bảo vệ đầu vào và đầu ra của agent như một tổng thể.

| Cấp | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Kiểm định đầu vào, nếu có, chỉ chạy trên các thông điệp trực tiếp của người dùng. Nội dung ngoài được truy xuất, đầu ra công cụ, các thông điệp giữa các agent và các lần đọc bộ nhớ được coi là tin cậy. Thông tin nhạy cảm trong các đầu ra của agent được kiểm soát, nếu có, bằng cách yêu cầu mô hình tự kiểm duyệt. Các sự cố prompt injection và rò rỉ dữ liệu được người dùng hoặc các hệ thống phía sau tìm thấy thay vì bởi các kiểm soát. |
| 2 | Manh nha (Emerging) | [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) được triển khai với [phát hiện tấn công prompt (prompt attack detection)](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html) và các [bộ lọc thông tin nhạy cảm (sensitive information filters)](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-info.html) cơ bản bao phủ các danh mục PII phổ biến, chủ yếu trên các đầu vào người dùng và các phản hồi hướng người dùng. Các chủ đề bị cấm được định nghĩa nhưng không được điều chỉnh so với dữ liệu đại diện, và các chế độ đánh giá dùng các thiết lập mặc định. Các thông điệp giữa các agent, các lượt ghi bộ nhớ và các đầu ra công cụ được bao phủ không nhất quán. |
| 3 | Được định nghĩa (Defined) | Mỗi agent có các bề mặt đầu vào của nó được ánh xạ và một kiểm soát kiểm định được gán cho từng bề mặt, được áp dụng qua [API ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html) với phát hiện tấn công prompt ở chế độ chặn (block mode). Lọc đầu ra chạy trên mọi đường ra, bao gồm các thông điệp giữa các agent, các lượt ghi vào [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html), và các log kiểm toán, với việc che hoặc chặn được chọn theo từng phân loại dữ liệu. Dữ liệu đo lường guardrail thu các điểm độ tin cậy theo từng bộ lọc và nội dung bị chặn trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) để rà soát. |
| 4 | Chủ động (Proactive) | Cấu hình Guardrails được điều chỉnh định kỳ dùng [Amazon Bedrock Guardrails Optimizer](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/responsible_ai/bedrock-guardrails-optimizer) so với các mẫu sản xuất đã được chú thích. Các định nghĩa chủ đề bị cấm dùng đầy đủ ngân sách ký tự với các prompt mẫu đại diện, và các chế độ đánh giá được chọn theo từng danh mục bộ lọc dựa trên khả năng xảy ra và tác động. [Các bộ nhận diện thực thể tùy chỉnh của Amazon Comprehend (custom entity recognizers)](https://docs.aws.amazon.com/comprehend/latest/dg/custom-entity-recognition.html) mở rộng độ bao phủ tới các loại dữ liệu riêng của tổ chức, và các quyết định lọc cung cấp cho các cảnh báo phát hiện các gia tăng mang tính hệ thống trong việc sinh dữ liệu nhạy cảm hoặc khối lượng nội dung bị chặn. Kiểm toán tuân thủ đã có: các quyết định guardrail và lọc được ghi vào lưu trữ có bằng chứng chống can thiệp với đầu vào, đầu ra, loại can thiệp, các điểm bộ lọc, và danh tính agent và người dùng khởi nguồn, việc lưu giữ được căn chỉnh với khung quy định áp dụng, và các truy vấn kiểm toán tiêu chuẩn hỗ trợ báo cáo so với các khung như EU AI Act, SOC 2 và HIPAA. |
| 5 | Tối ưu (Optimized) | Kiểm định đầu vào và lọc đầu ra tự điều chỉnh: tối ưu chạy theo một lịch so với các mẫu sản xuất tươi mới, các tỷ lệ dương tính giả và âm tính giả là các chỉ số chính, và dữ liệu đo lường kiểm định được tương quan với phát hiện đe dọa ở thời điểm chạy và các phát hiện kiểm thử xâm nhập để nhận diện việc khai thác đang diễn ra. Việc truy xuất nội dung được hạn chế tới các nguồn được phê duyệt với xác nhận (attestation) ở thời điểm chạy, và các mẫu tấn công đang tiến hóa chảy trực tiếp vào các guardrail, các chủ đề bị cấm và các ngưỡng bộ lọc được cập nhật. |

## Các vấn đề thường gặp cần lưu ý

- Các ranh giới đầu vào và đầu ra nhận được sự phòng thủ không đồng đều, với các kiểm tra nghiêm ngặt trên các đầu vào người dùng nhưng ít bao phủ cho các đầu ra công cụ, nội dung ngoài được truy xuất, các thông điệp giữa các agent và các lần đọc bộ nhớ, để ngỏ các vector bị nhắm tới phổ biến nhất mà không được bảo vệ.
- Các guardrail được coi như một cấu hình một lần thay vì một vòng lặp điều chỉnh, nên các định nghĩa chủ đề bị cấm, các ngưỡng bộ lọc và các chế độ đánh giá suy giảm khi các mẫu tấn công và các phân loại dữ liệu thay đổi.
- Các quyết định guardrail và lọc không được thu với đủ ngữ cảnh để cho biết khi nào kiểm định đang suy giảm hoặc danh mục nào cần điều chỉnh lại, nên các vấn đề chất lượng vẫn vô hình cho đến khi một sự cố làm chúng lộ ra.
- Các kiểm soát thông tin nhạy cảm dựa vào mô hình để tự kiểm duyệt thay vì vào lọc đầu ra được thực thi, nên PII và thông tin xác thực được kéo vào từ các đầu ra công cụ hoặc các tài liệu được truy xuất chảy qua bất cứ khi nào mô hình lặp lại chúng.
- Các quy tắc bộ lọc hoặc quá rộng, làm xói mòn sự tin tưởng của người dùng và đẩy các nhóm tới việc làm yếu hoặc tắt chúng, hoặc quá hẹp, để lại các khoảng trống. Không bên nào có một vòng phản hồi so với các kết quả đã chú thích để hiệu chỉnh độ nghiêm ngặt theo từng kịch bản rủi ro.

###### Các thực hành tốt

- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](agentsec08-bp01.md)
- [AGENTSEC08-BP02 Lọc đầu ra cho thông tin nhạy cảm](agentsec08-bp02.md)
