# Nhận thức của tác nhân

Các tác nhân đặt nền suy luận của mình trên thông tin hiện thời, chính xác và thích ứng dựa trên phản hồi có cấu trúc sẽ mang lại nhận thức đáng tin cậy ngay cả khi yêu cầu tác vụ và phân bố dữ liệu tiến hóa. Các động cơ nhận thức của tác nhân phải được cung cấp thông tin phù hợp ở mọi lớp của quá trình thực thi luồng công việc để thực thi tác vụ một cách đáng tin cậy.

| AGENTREL05: Làm thế nào để bạn triển khai nhận thức của tác nhân đáng tin cậy, truy cập đúng dữ liệu vào đúng thời điểm? |
| --- |
|  |

## Mục tiêu năng lực

- Suy luận của tác nhân được phân rã thành các giai đoạn mô-đun với các giao diện tường minh, nhờ đó một lỗi ở một giai đoạn tạo ra dự phòng thu hẹp theo giai đoạn thay vì lỗi nhận thức hoàn toàn.
- Việc truy xuất ngữ cảnh và suy luận mô hình mỗi thứ dùng các chiến lược theo tầng, nhờ đó nhận thức giảm bớt nhưng vẫn hữu ích vẫn khả dụng khi tầng truy xuất chính hoặc mô hình chính bị suy giảm.
- Nhận thức của tác nhân được đặt nền trên thông tin thực tế được truy xuất thông qua sinh tăng cường truy xuất (RAG) và các lời gọi công cụ thời gian thực, nhờ đó tỷ lệ ảo giác thấp hơn và đầu ra phản ánh các sự kiện hiện thời.
- Hành vi của tác nhân cải thiện qua các chu kỳ dẫn dắt bởi kiểm định (evaluation-driven), nơi phản hồi được thu thập, kết quả được đánh giá, và các thay đổi prompt hoặc cấu hình được kiểm định ngoại tuyến trước khi triển khai, thay vì qua tự sửa đổi lúc chạy.
- Sức khỏe theo từng giai đoạn, chất lượng truy xuất và kết quả kiểm định đều quan sát được như telemetry hạng nhất, nhờ đó các mắt xích yếu nhất trong nhận thức nổi lên trong bảng điều khiển thay vì trong lời phàn nàn của người dùng.

## Các cấp độ trưởng thành

Các cấp độ này tóm tắt hình hài của từng giai đoạn trưởng thành đối với nhận thức của tác nhân như một tổng thể.

| Cấp | Tên | Biểu hiện |
| --- | --- | --- |
| 1 | Sơ khởi (Initial) | Nhận thức của tác nhân là một đường ống đơn khối, nơi bất kỳ lỗi thành phần nào đều gây ra lỗi nhận thức hoàn toàn. Các tác nhân dựa vào dữ liệu huấn luyện của mô hình cho kiến thức miền, không có nền truy xuất và không thu thập phản hồi. Các lỗi hệ thống được phát hiện qua lời phàn nàn của người dùng, và việc thích ứng diễn ra qua các chỉnh sửa prompt một lần áp thẳng vào môi trường vận hành. |
| 2 | Manh nha (Emerging) | Suy luận được chia thành các giai đoạn nhận diện được, và việc truy xuất cơ bản đặt nền đầu ra của tác nhân trên kiến thức của tổ chức qua [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Các đội bắt một số tín hiệu phản hồi, và các bản kiểm định định kỳ so sánh đầu ra của tác nhân với một tập nhỏ các ví dụ golden-path. Các dự phòng tồn tại cho các đường lỗi hiển nhiên nhưng không được diễn tập một cách hệ thống. |
| 3 | Xác lập (Defined) | Mỗi giai đoạn suy luận có lược đồ đầu vào và đầu ra tường minh và xử lý lỗi độc lập, triển khai trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html). Phản hồi đa tầng (cấp hành động, cấp tác vụ, cấp phiên) được bắt và lưu bên cạnh các bản ghi tác vụ, và [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) đánh giá hiệu suất của tác nhân so với các tập tác vụ đại diện. Các đường ống đồng bộ hóa knowledge base được tự động hóa, và các chiến lược chunking và reranking được tinh chỉnh theo từng loại nội dung. |
| 4 | Chủ động (Proactive) | Các cơ chế ngắt tự động giữa các giai đoạn kích hoạt các dự phòng đặc thù giai đoạn khi tỷ lệ lỗi vượt ngưỡng, và truy xuất ngữ cảnh theo tầng cùng [suy luận đa Vùng của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) giữ cho nhận thức khả dụng khi các tầng chính suy giảm. Tiền xử lý đa phương thức (multimodal) qua [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) là một giai đoạn riêng biệt với các dự phòng của riêng nó. Các luồng tối ưu prompt ngoại tuyến triển khai các cải tiến đã kiểm định thông qua triển khai từ từ, và các ngưỡng độ mới của kiến thức tạo ra các cảnh báo quan sát được. |
| 5 | Tối ưu (Optimized) | Chất lượng theo từng giai đoạn, hiệu quả truy xuất và kết quả kiểm định nuôi một vòng lặp cải tiến liên tục tinh chỉnh chunking, reranking, chọn tầng mô hình và các chiến lược prompt. Tỷ lệ ảo giác, độ phủ nền (grounding coverage) và kích hoạt dự phòng theo từng giai đoạn được theo dõi như các chỉ số độ tin cậy chính, và các quyết định kiến trúc nhận thức được dẫn dắt bởi dữ liệu quan trắc thay vì trực giác. Tổ chức đóng góp lại các mẫu và số đo nhận thức của tác nhân cho các cộng đồng thực hành nội bộ của mình. |

## Các vấn đề thường gặp cần lưu ý

- Các đội xây dựng nhận thức của tác nhân như một đường ống đơn khối, nên bất kỳ lỗi giai đoạn nào cũng gây ra lỗi nhận thức hoàn toàn và việc gỡ lỗi phải tháo rời một hộp đen lớn duy nhất sau đó.
- Các tác nhân chỉ dựa vào dữ liệu huấn luyện của mô hình cho kiến thức đặc thù miền và tạo ra các câu trả lời sai một cách tự tin về các sự kiện hiện thời, vì không có nền truy xuất.
- Truy xuất bị coi là một phụ thuộc khả dụng cứng, nên các sự cố knowledge base trở thành sự cố tác nhân thay vì nền suy luận suy giảm được truyền đạt rõ ràng.
- Các tác nhân được triển khai mà không thu thập phản hồi đa tầng, nên các lỗi hệ thống được phát hiện từ lời phàn nàn của người dùng thay vì từ telemetry.
- Các thay đổi prompt và cấu hình được áp dụng lúc chạy mà không có kiểm định ngoại tuyến, tạo ra các thoái lui khó lường khi phản hồi nhiễu hoặc các bản kiểm định bị bỏ qua.

###### Các thực hành tốt

- [AGENTREL05-BP01 Thiết kế các thành phần suy luận của tác nhân mô-đun, chịu lỗi](agentrel05-bp01.md)
- [AGENTREL05-BP02 Tạo điều kiện cho thích ứng đáng tin cậy qua các chu kỳ cải tiến dẫn dắt bởi kiểm định](agentrel05-bp02.md)
- [AGENTREL05-BP03 Đặt nền nhận thức của tác nhân trên thông tin thực](agentrel05-bp03.md)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
