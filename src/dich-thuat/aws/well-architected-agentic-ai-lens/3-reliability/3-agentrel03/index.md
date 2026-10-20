# Quản lý bộ nhớ và trạng thái của tác nhân

Các tác nhân phân loại, lưu bền và phục hồi bộ nhớ một cách đáng tin cậy sẽ mang lại hành vi nhất quán qua các phiên và duy trì chức năng ngay cả khi các thành phần bị lỗi. Bộ nhớ của tác nhân chịu cùng những cân nhắc về độ tin cậy như bất kỳ kho dữ liệu nào. Làm thế nào để bạn hỗ trợ việc trả về đúng thông tin, và tác nhân hành xử ra sao khi trạng thái không khả dụng?

| AGENTREL03: Làm thế nào để bạn hỗ trợ bộ nhớ và trạng thái của tác nhân luôn truy cập được một cách đáng tin cậy xuyên suốt vòng đời tác nhân? |
| --- |
|  |

## Mục tiêu năng lực

- Bộ nhớ của tác nhân được phân loại tường minh theo phạm vi và độ bền, nhờ đó ngữ cảnh phiên ngắn hạn không bao giờ làm nhiễm kiến thức dài hạn và việc truy xuất có thể dự đoán qua các loại tác vụ.
- Các kho bộ nhớ có tính dư thừa (redundant) và có các đường chuyển đổi dự phòng (failover) tự động, nhờ đó lỗi của từng thành phần tạo ra bộ nhớ suy giảm nhưng vẫn dùng được thay vì mất hoàn toàn.
- Các luồng công việc chạy lâu lưu bền các điểm kiểm tra tại ranh giới giai đoạn và tiếp tục từ trạng thái tốt gần nhất sau gián đoạn, thay vì khởi động lại từ số không.
- Các tác nhân phát hiện điều kiện bộ nhớ suy giảm, chuyển sang các chế độ giảm bớt được định nghĩa tốt, và truyền đạt minh bạch các năng lực hiện tại của chúng cho người dùng và các hệ thống điều phối.
- Sức khỏe của bộ nhớ và trạng thái được trang bị công cụ đo như telemetry hạng nhất, nhờ đó chất lượng truy xuất, số lần kích hoạt failover và vòng đời điểm kiểm tra đều quan sát được và tinh chỉnh được lúc vận hành.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với quản lý bộ nhớ và trạng thái của tác nhân như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Bộ nhớ của tác nhân nằm trong một kho không phân biệt duy nhất, không phân loại, không chính sách lưu giữ, không kế hoạch failover. Các luồng công việc chạy lâu khởi động lại từ số không khi có bất kỳ lỗi nào vì không có trạng thái nào được lưu bền giữa các bước. Sự cố bộ nhớ không phân biệt được với sự cố tác nhân vì không có chế độ suy giảm để lùi về, và sức khỏe bộ nhớ chỉ được rà soát sau một sự cố. |
| 2 | Manh nha (Emerging) | Các đội đã tách bộ nhớ ngắn hạn và dài hạn, thường dùng các namespace theo phiên và bền vững của [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html). Có các chính sách lưu giữ cơ bản cho bộ nhớ ngắn hạn, và một số luồng công việc chạy lâu lưu bền trạng thái điểm kiểm tra một cách tường minh. Tính dư thừa và failover dựa vào mặc định của dịch vụ được quản lý, và các dạng lỗi chỉ được kiểm thử như một phần của các bản rà soát sẵn sàng phát hành lớn. |
| 3 | Xác lập (Defined) | Một phân loại bộ nhớ được tài liệu hóa (ngữ cảnh phiên, kiến thức bền vững, bản ghi tình tiết) dẫn dắt việc phân loại tại thời điểm nạp, và [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) bổ sung cho bộ nhớ của tác nhân bằng các kho ngữ liệu của tổ chức cho sinh tăng cường truy xuất (RAG). Các luồng công việc nhiều bước được điều phối qua [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) hoặc các máy trạng thái tương đương với các bước idempotent, nhờ đó việc phục hồi là một lần phát lại (replay) rẻ tiền từ điểm kiểm tra gần nhất. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) báo cáo chất lượng truy xuất và sức khỏe điểm kiểm tra, và các chuyển đổi chế độ cho suy giảm nhẹ nhàng tuân theo các runbook được viết ra. |
| 4 | Chủ động (Proactive) | Logic fail-fast định tuyến truy cập bộ nhớ tới các kho dự phòng hoặc cache trong tiến trình khi các kho chính hành xử sai, và các cache đọc xuyên (read-through) phục vụ bộ nhớ dài hạn trong thời gian tạm không khả dụng. Các chuyển đổi chế độ cho suy giảm nhẹ nhàng (đầy đủ, chỉ theo phiên, không trạng thái) được tự động hóa từ các số liệu sức khỏe bộ nhớ, và việc phát hiện phục hồi đưa các tác nhân về chế độ đầy đủ mà không cần con người can thiệp. Các thí nghiệm [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) đối với lớp bộ nhớ chạy theo lịch, và vòng đời điểm kiểm tra được quản lý qua hết hạn dựa trên TTL thay vì dọn dẹp thủ công. |
| 5 | Tối ưu (Optimized) | Việc phân loại bộ nhớ, chính sách lưu giữ và điểm kiểm tra được tinh chỉnh liên tục từ dữ liệu quan trắc thay vì qua các bản rà soát định kỳ. Bộ nhớ dùng chung giữa các tác nhân, truy xuất theo tầng và các chiến lược tái xếp hạng (reranking) được hiệu chỉnh lại trên chất lượng truy xuất đo được, và kết quả kỹ thuật hỗn loạn (chaos-engineering) dẫn dắt các thay đổi thiết kế về topo bộ nhớ thay vì các bản vá một lần. Các dạng lỗi liên quan đến bộ nhớ nổi lên trong telemetry và bảng điều khiển trước khi ảnh hưởng đến người dùng, và tổ chức đóng góp lại các mẫu bộ nhớ và trạng thái cho các cộng đồng thực hành nội bộ của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các đội lưu toàn bộ bộ nhớ của tác nhân trong một tầng không phân biệt duy nhất, nên việc truy xuất trả về các suy luận trung gian cũ kỹ lẫn với các sự kiện miền ổn định và âm thầm làm giảm chất lượng tác vụ.
- Các luồng công việc chạy lâu thiếu điểm kiểm tra, nên bất kỳ lỗi thoáng qua nào cũng buộc khởi động lại toàn bộ và luồng công việc phải trả toàn bộ chi phí mỗi khi có sự cố.
- Các bước của luồng công việc không idempotent, nên việc phát lại dựa trên điểm kiểm tra tạo ra các tác dụng phụ trùng lặp thay vì tiếp tục công việc một cách an toàn.
- Sự cố bộ nhớ bị coi là sự cố tác nhân vì không có phân cấp suy giảm, và người dùng thấy các lỗi khó hiểu thay vì năng lực giảm bớt được truyền đạt rõ ràng.
- Các đường failover chỉ tồn tại trên giấy, và các lỗ hổng trong tính dư thừa và phục hồi bị phát hiện trong các sự cố vận hành vì kiểm thử tiêm lỗi không phải là một phần của quy trình phát hành.

###### Các thực hành tốt

- [AGENTREL03-BP01 Thiết kế mô hình phân loại thông tin để xác định bộ nhớ ngắn hạn và dài hạn](agentrel03-bp01.md)
- [AGENTREL03-BP02 Kiến trúc các kho bộ nhớ chịu lỗi với dư thừa và failover](agentrel03-bp02.md)
- [AGENTREL03-BP03 Triển khai quản lý trạng thái toàn diện và phục hồi dựa trên điểm kiểm tra](agentrel03-bp03.md)
- [AGENTREL03-BP04 Triển khai suy giảm nhẹ nhàng cho các thao tác bộ nhớ và trạng thái](agentrel03-bp04.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
