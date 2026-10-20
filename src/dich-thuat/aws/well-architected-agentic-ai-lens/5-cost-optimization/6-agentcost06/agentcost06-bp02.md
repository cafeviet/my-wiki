# AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tạo tác hiệu quả

Các agent runtime tạo một phiên bản bất biến ở mỗi thay đổi cấu hình tích lũy hàng trăm phiên bản trong quá trình phát triển bình thường, mỗi phiên bản giữ các tham chiếu tới các container image không thể quản lý dễ dàng. Các image cơ sở phân lớp, định tuyến lưu lượng dựa trên endpoint, và các chính sách dọn dẹp tự động giữ cho chi phí triển khai tỷ lệ với việc sử dụng thực tế chứ không theo số lượng cấu hình trong quá khứ.

**Kết quả mong muốn:**

- Bạn có khử trùng lặp lớp container lưu các phụ thuộc dùng chung một lần xuyên các phiên bản agent.
- Bạn dùng định tuyến lưu lượng dựa trên endpoint cho các triển khai blue/green và canary mà không có hạ tầng đang chạy trùng lặp.
- Bạn có các chính sách vòng đời tự động xóa các phiên bản không dùng, giúp ngăn tích lũy lưu trữ vô hạn.
- Bạn giám sát tồn kho phiên bản và bắt các phiên bản không dùng trước khi chúng trở thành một chi phí đáng kể.

**Các phản mẫu thường gặp (anti-patterns):**

- Giữ tất cả các phiên bản agent vô hạn mà không có chính sách vòng đời, tích lũy chi phí lưu trữ cho các phiên bản nhận không lần gọi nào.
- Tạo các container image riêng biệt mà không chia sẻ các lớp cơ sở chung, nhân chi phí lưu trữ xuyên các phiên bản agent.
- Chạy các môi trường song song đầy đủ cho các triển khai blue/green thay vì chỉ định tuyến các tỷ lệ phần trăm lưu lượng kiểm thử.
- Cho phép các phiên bản agent không dùng tích lũy mà không giám sát, làm giảm khả năng dọn dẹp tự động và tăng đều đặn chi phí lưu trữ mà không có khả năng nhìn thấy các mẫu gọi theo phiên bản.

**Lợi ích khi áp dụng thực hành tốt này:**

- Khử trùng lặp lớp container lưu các phụ thuộc dùng chung một lần, giảm chi phí lưu trữ tỷ lệ với việc tái sử dụng phiên bản. Xác minh khử trùng lặp bằng cách so sánh tổng lưu trữ repository trong ECR (được báo cáo trong các số liệu CloudWatch dưới RepositorySize) với tổng của các kích thước manifest image riêng lẻ. Khử trùng lặp hiệu quả cho thấy lưu trữ repository nhỏ hơn đáng kể so với tổng các manifest.
- Định tuyến dựa trên endpoint cho phép các chuyển tiếp triển khai mà không có hạ tầng đang chạy trùng lặp.
- Dọn dẹp tự động xóa các phiên bản không dùng, giúp ngăn sự tăng chi phí lưu trữ vô hạn.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) tạo một phiên bản bất biến ở mỗi lần cập nhật cấu hình. Bản thân phiên bản là metadata nhẹ (tham chiếu container image, cài đặt giao thức, và cấu hình mạng), nhưng mỗi phiên bản giữ một tham chiếu tới các container image mà [Amazon ECR](https://aws.amazon.com/ecr/) không thể quản lý cho đến khi tất cả các tham chiếu được loại bỏ. Cập nhật một biến môi trường, thay đổi một cài đặt giao thức, hoặc sửa đổi cấu hình mạng đều kích hoạt một phiên bản mới. Không có chính sách dọn dẹp, phát triển tích cực tạo ra hàng trăm phiên bản, mỗi phiên bản neo các image được tham chiếu của nó tại chỗ.

Biện pháp giảm thiểu đầu tiên là cấu trúc lớp. Xây dựng các container agent với một lớp cơ sở chung chứa các phụ thuộc dùng chung (runtime, SDK, các công cụ chung) và các lớp đặc thù theo agent ở trên. ECR tự động khử trùng lặp các lớp giống hệt nhau xuyên các image, nên các agent chia sẻ hầu hết các phụ thuộc chia sẻ hầu hết lưu trữ. Biện pháp giảm thiểu thứ hai là định tuyến lưu lượng. Hệ thống endpoint của AgentCore Runtime hỗ trợ các triển khai blue/green và canary mà không có hạ tầng song song: tạo một endpoint production trỏ tới phiên bản ổn định và dùng định tuyến có trọng số để gửi một tỷ lệ phần trăm lưu lượng nhỏ tới các phiên bản mới trong lúc xác thực. [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) cung cấp các số liệu theo từng phiên bản (tỷ lệ lỗi, phân vị độ trễ, chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ) điều khiển quyết định thăng cấp.

Các tiêu chí thăng cấp canary truyền thống nhìn vào tỷ lệ lỗi và độ trễ, nhưng các phiên bản agent có thể khác biệt đáng kể về chi phí suy luận (một prompt mới có thể tạo ra các câu trả lời đúng nhưng tốn thêm 30% token). Đưa chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ vào các tiêu chí thăng cấp giúp ngăn một hồi quy chi phí trượt vào production đằng sau các số liệu chất lượng tốt.

Định nghĩa một mức lưu giữ phiên bản tối đa (một điểm khởi đầu hợp lý là năm phiên bản gần nhất cộng với bất kỳ phiên bản nào hiện đang phục vụ lưu lượng qua một endpoint) và cấu hình [các chính sách vòng đời Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html) để xóa các image không gắn thẻ và các image cũ hơn 90 ngày không được tham chiếu bởi các phiên bản đang hoạt động. Việc xóa tự động các phiên bản vượt quá giới hạn lưu giữ, được cổng dựa trên việc xác minh rằng không có endpoint nào tham chiếu phiên bản và nó đã có không lần gọi nào trong cửa sổ lưu giữ, giữ ECR khỏi biến thành một nghĩa địa của các vòng lặp phát triển.

### Các bước triển khai

- **Cấu trúc các container cho chia sẻ lớp:** Xây dựng các container agent với các lớp cơ sở chung và các lớp đặc thù theo agent để việc khử trùng lặp lớp của [Amazon ECR](https://aws.amazon.com/ecr/) hiệu quả.
- **Dùng định tuyến lưu lượng dựa trên endpoint:** Triển khai các agent lên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) và cấu hình các endpoint tùy chỉnh cho lưu lượng production với định tuyến có trọng số cho các triển khai blue/green và canary.
- **Đưa chi phí vào các tiêu chí thăng cấp:** Giám sát chất lượng triển khai bằng các số liệu [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) trước khi cập nhật các endpoint production, bao gồm chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ cùng với tỷ lệ lỗi và độ trễ.
- **Đặt các chính sách lưu giữ phiên bản:** Định nghĩa một chính sách lưu giữ như năm phiên bản gần nhất cộng với lưu lượng đang hoạt động, và cấu hình [các chính sách vòng đời Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html) để xóa các image không dùng tự động.
- **Giám sát tồn kho phiên bản hàng tuần:** Triển khai một hàm tồn kho phiên bản hàng tuần truy vấn các API AgentCore Runtime tìm tất cả các phiên bản agent, xác định các phiên bản có không lần gọi nào qua các số liệu Amazon CloudWatch, và lưu metadata sử dụng cho phân tích lịch sử trước khi chính sách vòng đời ECR xóa các image.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](../5-agentcost05/agentcost05-bp01.md)
- [AGENTCOST06-BP01 Triển khai khám phá và registry nhẹ cho cộng tác tiết kiệm chi phí](agentcost06-bp01.md)
- [AGENTCOST06-BP03 Thiết kế khởi tạo tiết kiệm chi phí thông qua warm pool và caching](agentcost06-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Amazon ECR lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Runtime](https://www.youtube.com/watch?v=wizEw5a4gvM)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon ECR](https://aws.amazon.com/ecr/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
