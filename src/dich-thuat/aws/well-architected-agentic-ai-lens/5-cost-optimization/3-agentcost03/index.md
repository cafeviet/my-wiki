# Quản lý chi phí bộ nhớ và trạng thái của agent

Các agent với kiến trúc bộ nhớ (memory) được phân tầng tốt duy trì được chất lượng suy luận trong khi giữ chi phí lưu trữ và truy xuất tỷ lệ với mức sử dụng thực tế chứ không theo tổng kích thước lịch sử. Các hệ thống bộ nhớ agent có thể trở nên đắt đỏ do tích lũy ngữ cảnh không kiểm soát, các mẫu truy xuất kém hiệu quả, và lưu trữ trạng thái bền vững. Các hội thoại chạy dài tiêu thụ các cửa sổ ngữ cảnh ngày càng lớn, và việc truy xuất bộ nhớ episodic có thể kích hoạt các truy vấn vector database ở mỗi bước suy luận.

| AGENTCOST03: Làm thế nào để quản lý chi phí bộ nhớ và trạng thái của agent một cách hiệu quả? |
| --- |
|  |

## Mục tiêu năng lực

- Lưu trữ bộ nhớ được căn chỉnh với tần suất truy cập, với ngữ cảnh hoạt động trên các kho lưu trữ hiệu năng cao và dữ liệu lịch sử trên các tầng chi phí thấp hơn.
- Truy xuất mang tính chọn lọc thay vì đại trà, nên số token tiêu tốn cho mỗi bước suy luận phản ánh ngữ cảnh thực sự quan trọng đối với tác vụ hiện tại.
- Các phiên chạy dài nén và cắt tỉa lịch sử liên tục, giữ chi phí token dưới tuyến tính khi độ dài hội thoại tăng.
- Trạng thái phiên và việc học bền vững của agent được lưu bền qua các kiểm soát vòng đời được quản lý, giúp ngăn sự tăng trưởng lưu trữ không giới hạn mà không loại bỏ kiến thức cải thiện suy luận tương lai.
- Chi phí bộ nhớ và trạng thái quan sát được theo từng agent và từng phiên, với cảnh báo làm nổi các mẫu truy xuất và sự tăng trưởng lưu trữ trước khi chúng trở nên đáng kể.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc quản lý chi phí bộ nhớ và trạng thái của agent nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Bộ nhớ là một lớp đơn không phân biệt. Toàn bộ lịch sử hội thoại được truyền vào mọi lần gọi, và không có lọc truy xuất, nén hay chính sách vòng đời. Chi phí bộ nhớ và trạng thái theo từng phiên không được đo lường, nên sự tăng trưởng token và lưu trữ chỉ được phát hiện khi một hóa đơn hoặc tràn ngữ cảnh buộc phải nhìn nhận vấn đề. |
| 2 | Nhen nhóm (Emerging) | Bộ nhớ ngắn hạn và dài hạn được tách riêng, và một tóm tắt cuộn (rolling summarization) cơ bản giữ cho các phiên dài nhất không tăng trưởng không giới hạn. Truy xuất dùng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) hoặc tìm kiếm vector tương đương với một top-K cố định. Các dashboard cơ sở làm nổi việc sử dụng token theo từng phiên, nhưng việc tinh chỉnh là một lần và được áp dụng bởi từng nhóm riêng lẻ. |
| 3 | Xác định (Defined) | Bộ nhớ theo tầng là tiêu chuẩn xuyên suốt các nhóm agent, với các dịch vụ được quản lý như [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) được dùng cho lưu trữ ngắn hạn và dài hạn. Truy xuất được chấm điểm theo mức liên quan, kích thước chunk được định cỡ đúng, và mức sử dụng ngữ cảnh được giám sát theo một mục tiêu đã định. Các chính sách vòng đời lưu trữ hoặc xóa trạng thái lỗi thời trên [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) hoặc tương đương, và các dashboard [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) bao phủ hầu hết các agent. |
| 4 | Chủ động (Proactive) | Nén bộ nhớ, cắt tỉa và truy xuất chọn lọc là các mặc định được tự động hóa, và các tham số vòng đời phiên được tinh chỉnh theo từng workload. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp việc quy gán chi phí theo từng agent và từng phiên, với cảnh báo cho tràn ngữ cảnh, điểm nóng truy xuất và tăng trưởng lưu trữ bất ngờ. Các tham số chỉ mục vector và top-K được xem xét đều đặn theo dữ liệu recall và chi phí. |
| 5 | Tối ưu (Optimized) | Kiến trúc bộ nhớ được tối ưu liên tục từ các mẫu truy cập quan sát được. Top-K, kích thước chunk, việc đặt tầng và tần suất checkpoint thích nghi với các tín hiệu workload thay vì cấu hình tĩnh. Các hồi quy chi phí về bộ nhớ và trạng thái được bắt trong tiền production bằng các kiểm tra tự động theo các đường cơ sở lịch sử, và các hiểu biết từ vận hành được đưa ngược trở lại vào thiết kế mẫu suy luận và truy xuất. |

## Các vấn đề thường gặp cần chú ý

- Bộ nhớ được coi là một kho đơn không phân biệt, nên mọi byte đều trả mức giá lưu trữ hiệu năng cao bất kể nó có bao giờ được đọc lại hay không.
- Toàn bộ lịch sử hội thoại được tiêm vào mọi lần gọi, khiến chi phí token tăng tuyến tính theo độ dài phiên và đẩy các phiên dài về phía tràn ngữ cảnh.
- Truy xuất thô và bừa bãi, trả về ngữ cảnh lớn, ít liên quan trong khi một tập kết quả nhỏ hơn, được chấm điểm theo mức liên quan có thể giữ được chất lượng suy luận với một phần nhỏ chi phí.
- Trạng thái phiên và bộ nhớ bền vững tích lũy mà không có vòng đời đã định, để lưu trữ tăng vô hạn cho đến khi một lần xem xét chi phí buộc phải dọn dẹp phản ứng.
- Chi phí bộ nhớ và trạng thái vô hình ở cấp từng agent và từng phiên, nên các hồi quy như mẫu truy xuất đắt tiền, tăng trưởng trạng thái bất ngờ và phình phiên rảnh chỉ được phát hiện sau khi chúng hiện lên trên hóa đơn.

###### Các thực hành tốt

- [AGENTCOST03-BP01 Thiết kế các hệ thống truy xuất tiết kiệm chi phí với bộ nhớ theo tầng](agentcost03-bp01.md)
- [AGENTCOST03-BP02 Tối ưu chi phí thông qua nén và cắt tỉa cửa sổ ngữ cảnh một cách thông minh](agentcost03-bp02.md)
- [AGENTCOST03-BP03 Triển khai lưu bền trạng thái và quản lý vòng đời tối ưu chi phí](agentcost03-bp03.md)
