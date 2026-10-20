# Phạm vi quản trị

**Quản trị (governance)** AI hiệu quả đòi hỏi các tổ chức thiết lập sự giám sát toàn diện đối với hệ sinh thái **AI tác tử (agentic AI)** của mình thông qua các **sổ đăng ký (registry)** tập trung, các biện pháp kiểm soát chất lượng và các khung quản lý truy cập. Khi các **tác tử AI (AI agent)** gia tăng tràn lan thông qua các nền tảng low-code, việc duy trì khả năng quan sát các tài sản đã triển khai – bao gồm năng lực, quyền hạn và các mối phụ thuộc lẫn nhau của chúng – trở nên thiết yếu cho bảo mật, tuân thủ và sự xuất sắc trong vận hành. Nền tảng quản trị này giúp các tổ chức cân bằng giữa tốc độ đổi mới và quản lý rủi ro, bảo đảm các hệ thống AI vận hành trong các ranh giới đã xác định đồng thời ngăn chặn các triển khai **AI ngầm (shadow AI)** trái phép.

## Quản lý sổ đăng ký tác tử, công cụ và MCP

Khả năng quan sát toàn diện đối với các tài sản AI tạo nên nền tảng của quản trị hiệu quả. Các tổ chức phải duy trì các sổ đăng ký tập trung ghi lại tất cả các tác tử đã triển khai, bao gồm năng lực, quyền hạn, phân loại bảo mật, giới hạn tốc độ (rate limit) và quy trình phê duyệt, các mô hình truy cập dữ liệu, quyền sở hữu và mục đích nghiệp vụ của chúng. Mỗi mục ghi lại các siêu dữ liệu quan trọng, chẳng hạn như lịch sử phiên bản, các mối phụ thuộc, các chỉ số hiệu năng và lịch sử sự cố.

Trong một bối cảnh biến đổi nhanh chóng, tài liệu phải mang tính chiến lược chứ không phải vét cạn. Hãy tập trung vào cơ sở lý giải cho quyết định, các mẫu kiến trúc và các điểm tích hợp – những yếu tố mang lại giá trị lâu dài ngay cả khi cách triển khai thay đổi. Mục tiêu của bạn là nắm bắt tri thức thể chế giúp các nhóm tìm thấy và hiểu các triển khai hiện có, đồng thời tránh lặp lại sai lầm.

## Quản lý mô hình LLM

Danh mục mô hình **LLM** theo dõi những **foundation model** nào được phê duyệt cho những tình huống sử dụng nào, bao gồm tính sẵn có theo khu vực, phân bổ hạn ngạch (quota) và thông tin vòng đời để nhận diện các mô hình đã ngừng hỗ trợ. Lý tưởng nhất, danh mục này chứa danh sách các ứng dụng sử dụng từng mô hình, các chủ sản phẩm của chúng, các triển khai theo khu vực cụ thể và giới hạn sử dụng, nhằm cho phép cập nhật chủ động và quản lý năng lực, ngăn ngừa gián đoạn khi các mô hình cũ đến cuối vòng đời hoặc khi phát sinh các ràng buộc về năng lực.

## Kiểm soát chất lượng và quy trình phê duyệt

Khi việc xây dựng tác tử trở nên dễ dàng hơn thông qua các nền tảng low-code, các cơ chế kiểm soát chất lượng bảo đảm rằng chỉ những tác tử đáp ứng các tiêu chuẩn tối thiểu mới có thể được chia sẻ trong toàn tổ chức.

Các khung đánh giá tác tử (agent evaluation framework) đánh giá tính đúng đắn về mặt chức năng, chất lượng phản hồi, các ranh giới an toàn và sự phù hợp với các chính sách của tổ chức trước khi triển khai. Các đánh giá này kết hợp kiểm thử tự động đối với hiệu năng kỹ thuật với rà soát của con người đối với tính phù hợp nghiệp vụ, tạo ra một cổng chất lượng cân bằng có khả năng mở rộng khi số lượng tác tử gia tăng.

Việc phê duyệt mô hình cân nhắc các mốc chuẩn hiệu năng (benchmark), các ràng buộc chi phí, các yêu cầu về nơi lưu trú dữ liệu (data residency) và sự phù hợp với các nguyên tắc AI có trách nhiệm. Khi năng lực của mô hình tiến bộ nhanh chóng, bạn nên thiết lập các quy trình rà soát được rút gọn cho các cập nhật hiệu năng trong khi vẫn duy trì đánh giá kỹ lưỡng đối với các tính năng hoàn toàn mới.

Hãy hiệu chỉnh các tiêu chuẩn này tương xứng với rủi ro gắn với từng ứng dụng, đồng thời ý thức rằng các thực hành tốt nhất vẫn đang hình thành, qua đó thiết lập các yêu cầu an toàn và bảo mật cơ sở trong khi vẫn sẵn sàng điều chỉnh các chỉ số chất lượng khi kinh nghiệm tích lũy thêm.

## Chuẩn nền tảng và nền tảng tác tử

Các tổ chức phải định nghĩa bộ công nghệ (technology stack) được phê duyệt cho việc phát triển **AI tác tử (agentic AI)**, chỉ rõ những nền tảng và framework nào được phê duyệt. Khi các giao thức được dùng trong các ứng dụng tác tử như MCP (model context protocol) hoặc A2A (agent-to-agent) tiến hóa với tốc độ nhanh, và các giao thức mới có thể xuất hiện theo thời gian, bạn nên thiết lập các chuẩn cho giao tiếp liên tác tử an toàn, cân bằng giữa chuẩn hóa và tính linh hoạt.

Nền tảng nên cung cấp các mẫu và cấu hình đã được kiểm thử, đáp ứng các tiêu chuẩn bảo mật và tuân thủ, cho phép các nhà phát triển khởi đầu từ những nền móng tuân thủ. **Quản trị dưới dạng mã (governance as code)** nhúng việc thực thi chính sách trực tiếp vào nền tảng, trong khi các môi trường sandbox được chỉ định cung cấp không gian cho thử nghiệm với các ranh giới rõ ràng.

## Giảm thiểu AI ngầm

Sự dễ dàng trong việc xây dựng các ứng dụng AI tạo ra rủi ro **AI ngầm (shadow AI)** đáng kể. Việc làm cho con đường được quản trị trở nên hấp dẫn hơn con đường ngầm trở nên then chốt. Hãy tạo ra môi trường này thông qua các quy trình phê duyệt phản hồi nhanh, các năng lực tự phục vụ toàn diện và các đề xuất giá trị rõ ràng. Giáo dục và truyền thông bảo đảm rằng nhân viên hiểu lý do vì sao quản trị tồn tại và cách truy cập các tài nguyên đã được phê duyệt.

Ngoài việc giảm rủi ro AI ngầm, các tổ chức phải thiết lập các chính sách quản lý truy cập toàn diện, điều chỉnh ai có thể tương tác với tác tử và cách các tác tử tương tác với nhau.

## Truy cập đa cấp và quyền hạn của tác tử

Các tổ chức phải triển khai quản trị truy cập cho các tác tử AI để ngăn người dùng lợi dụng tác tử làm trung gian nhằm truy cập thông tin hoặc hệ thống mà họ không có quyền sử dụng trực tiếp.

Các biện pháp kiểm soát việc gọi công cụ (tool invocation) tạo nên một trong những nền tảng của quản trị tác tử. Mỗi tác tử vận hành với một danh tính lõi (core identity) định nghĩa phạm vi quyền hạn và năng lực của nó.

Hãy thiết lập các chính sách bảo đảm rằng:

- Quyền truy cập công cụ bị giới hạn dựa trên danh tính của tác tử.
- Các tác tử chỉ có thể gọi những công cụ mà chúng được cấp quyền tường minh.
- Việc gọi công cụ tôn trọng cả năng lực của tác tử lẫn, trong trường hợp tác tử được một người dùng gọi, quyền truy cập của người dùng đó, nhằm tránh truy cập dữ liệu trái phép.

Trong các hệ thống đa tác tử (multi-agent system), quản trị phải mở rộng xa hơn để bao gồm các quyền hạn giữa tác tử với tác tử (agent-to-agent). Các tác tử chỉ nên có khả năng gọi những tác tử khác mà chúng được cấp quyền tường minh, bổ sung thêm một lớp kiểm soát nữa. [Amazon Bedrock AgentCore Identity](https://aws.amazon.com/bedrock/agentcore/) cung cấp một dịch vụ quản lý danh tính và thông tin xác thực tập trung được thiết kế riêng cho các tác tử AI, cho phép xác thực, cấp quyền và quản lý thông tin xác thực an toàn.

## Yêu cầu về nguồn gốc và kiểm toán

Các khung quản trị phải yêu cầu theo dõi toàn diện các đường thực thi của tác tử để cho phép gỡ lỗi, phân tích bảo mật và kiểm chứng tuân thủ. Hãy thiết lập các chính sách bắt buộc rằng việc gọi tác tử và công cụ phải được ghi nhật ký với mức độ chi tiết đủ để tái dựng toàn bộ chuỗi hành động. Tuy nhiên, các chính sách về nguồn gốc (lineage) phải cân bằng giữa tính toàn diện với các cân nhắc về hiệu năng, lưu trữ và quyền riêng tư. Ví dụ, nếu một tác tử đã tính một điểm tín dụng, cần có khả năng xác định cách thức và lý do nó được tính theo cách đó mà không nhất thiết phải ghi nhật ký tất cả các bước trung gian.

Các chính sách quản lý truy cập cần có các cơ chế thực thi và giám sát liên tục để duy trì hiệu quả. Hãy thiết lập các yêu cầu quản trị bắt buộc rà soát truy cập định kỳ, các quy trình phát hiện và leo thang đối với vi phạm, trách nhiệm giải trình rõ ràng cho các quyết định, và các cơ chế rà soát chính sách định kỳ dựa trên kinh nghiệm vận hành.
