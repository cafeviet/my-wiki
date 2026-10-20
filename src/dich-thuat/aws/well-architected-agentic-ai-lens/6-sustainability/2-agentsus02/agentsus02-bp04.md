# AGENTSUS02-BP04 Đo lường và tối ưu hóa dấu chân môi trường của các khối công việc Agent

Không có đo lường, các tuyên bố bền vững chỉ là nguyện vọng và các tối ưu hóa không được theo dõi đối chiếu với dữ liệu thực tế. Theo dõi dấu chân môi trường (environmental footprint) của các khối công việc Agent biến tính bền vững thành một chỉ số kỹ thuật. Các đường cơ sở cho thấy nơi công sức đáng đầu tư, và các xu hướng cho thấy các thay đổi có thực sự hiệu quả hay không.

**Kết quả mong muốn:**

- Bạn có các đường cơ sở phát thải carbon cho hạ tầng Agent được thiết lập qua một giai đoạn quan sát xác định.
- Các chỉ số hiệu quả tài nguyên cho mỗi tác vụ (token trên mỗi lần hoàn thành thành công, giờ compute trên mỗi quy trình, và tỷ lệ hit của cache) được theo dõi song song với các kết quả kinh doanh.
- Các khối công việc có thể trì hoãn được lập lịch trong các giai đoạn ngoài giờ cao điểm hoặc định tuyến tới các Region có hồ sơ năng lượng thuận lợi.
- Các chỉ số vận hành và bền vững được kết hợp trong các bảng điều khiển (dashboard) thông tin cho các đợt rà soát tối ưu hóa định kỳ.

**Các phản mẫu thường gặp (anti-patterns):**

- Tuyên bố lợi ích bền vững từ các tối ưu hóa Agent mà không thiết lập đường cơ sở, khiến không thể xác thực liệu các thay đổi có thực sự giảm tác động không.
- Coi mọi khối công việc đều nhạy cảm với thời gian như nhau, chạy xử lý batch và các tác vụ nền trong giờ cao điểm trong khi trì hoãn chúng sẽ giảm tranh chấp và mức tiêu thụ năng lượng.
- Bỏ qua các khác biệt vùng miền trong hạ tầng năng lượng khi chọn Region triển khai cho các khối công việc có yêu cầu độ trễ linh hoạt.
- Chỉ theo dõi hiệu suất sử dụng hạ tầng mà không gắn nó với kết quả kinh doanh, nên các cải thiện hiệu quả về compute không kết nối với giá trị mang lại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các đường cơ sở đo được làm cho các cải thiện bền vững có thể kiểm chứng thay vì mang tính nguyện vọng.
- Công sức tối ưu hóa chảy tới các khối công việc có tác động môi trường lớn nhất, thay vì được áp dụng đồng đều.
- Các khối công việc có thể trì hoãn chạy khi hạ tầng đang được sử dụng thiếu, cải thiện hiệu quả toàn-đội-hình mà không ảnh hưởng đến hiệu năng hướng người dùng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

[AWS Sustainability](https://docs.aws.amazon.com/sustainability/latest/userguide/what-is-sustainability.html) cung cấp việc theo dõi phát thải carbon với phân tách theo dịch vụ và Region cho phía hạ tầng, và [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) bổ sung các chỉ số đặc thù cho Agent — token trên mỗi tác vụ thành công, giờ compute trên mỗi quy trình, và tỷ lệ hit của cache — vốn gắn mức tiêu thụ với các kết quả kinh doanh. Hãy thiết lập các đường cơ sở qua một cửa sổ quan sát 30 ngày để bao gồm biến thiên khối công việc thông thường, và theo dõi xu hướng hàng tháng sau đó để công việc tối ưu hóa có thể được xác thực đối chiếu với thay đổi đo được thay vì thay đổi tuyên bố.

Không phải mọi khối công việc Agent đều có cùng độ nhạy cảm với độ trễ. Các tương tác hướng người dùng cần phản hồi độ trễ thấp. Các job batch, lập chỉ mục knowledge base định kỳ, làm giàu dữ liệu hàng loạt, các lần chạy đánh giá, và các quy trình nghiên cứu phi tương tác có thể chờ hàng giờ hoặc qua đêm mà không ảnh hưởng đến người dùng. Dịch chuyển công việc có thể trì hoãn sang các giai đoạn ngoài giờ cao điểm giảm tranh chấp tài nguyên trên hạ tầng dùng chung và tận dụng các khung thời gian khi lưới điện rộng hơn sạch hơn. [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) mở rộng cùng nguyên tắc này qua các vùng địa lý. Các khối công việc batch không có ràng buộc độ trễ chặt có thể chạy trong các Region có hồ sơ năng lượng thuận lợi thay vì mặc định chọn Region gần nhất.

Các bảng điều khiển Amazon CloudWatch kết hợp các chỉ số vận hành với các chỉ báo bền vững làm cho tính bền vững hiển thị ngay tại nơi người vận hành đã nhìn. Theo dõi hiệu quả sử dụng tài nguyên, các chỉ số lãng phí (các lần thực thi thất bại hoặc bị bỏ dở tính theo phần trăm tổng số), và tỷ lệ sử dụng giờ cao điểm so với ngoài giờ cao điểm. Tích hợp các bảng điều khiển này vào các đợt rà soát tối ưu hóa định kỳ để tác động môi trường là một đầu vào thường trực cho các ưu tiên kỹ thuật thay vì một chuyện phụ hàng năm.

### Các bước triển khai

- **Bật theo dõi phát thải carbon:** Bật [AWS Sustainability](https://docs.aws.amazon.com/sustainability/latest/userguide/what-is-sustainability.html) và thiết lập các đường cơ sở môi trường cho hạ tầng Agent qua một cửa sổ quan sát 30 ngày.
- **Đo đạc hiệu quả tài nguyên theo từng tác vụ:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để theo dõi token trên mỗi lần hoàn thành thành công, giờ compute trên mỗi lần thực thi quy trình, và tỷ lệ hit của cache.
- **Lập lịch các khối công việc có thể trì hoãn ngoài giờ cao điểm:** Nhận diện các khối công việc phi tương tác và dịch chuyển chúng sang các cửa sổ ngoài giờ cao điểm: Xử lý batch
- Lập chỉ mục knowledge base
- Các lần chạy AgentCore Evaluations định kỳ
- Làm giàu dữ liệu hàng loạt
- **Đánh giá việc bố trí Region cho công việc batch:** Với các khối công việc có độ trễ linh hoạt, dùng [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) để định tuyến yêu cầu tới các Region có hồ sơ năng lượng thuận lợi.
- **Xây dựng các bảng điều khiển kết hợp và rà soát theo nhịp:** Tạo các bảng điều khiển Amazon CloudWatch ghép các chỉ số vận hành với các chỉ báo bền vững (hiệu quả sử dụng tài nguyên, phần trăm lãng phí, và tỷ lệ sử dụng giờ cao điểm so với ngoài giờ cao điểm), và rà soát chúng như một phần của các chu kỳ tối ưu hóa định kỳ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS02-BP01 Tối ưu hóa quản lý ngữ cảnh và sử dụng bộ nhớ](agentsus02-bp01.md)
- [AGENTSUS02-BP03 Mở rộng các phụ thuộc dữ liệu, mạng và compute một cách phù hợp](agentsus02-bp03.md)
- [SUS01-BP01 Choose Region based on both business requirements and sustainability goals](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_region_a2.html)

**Các tài liệu liên quan:**

- [AWS Sustainability User Guide](https://docs.aws.amazon.com/sustainability/latest/userguide/what-is-sustainability.html)
- [Announcing the AWS Sustainability console](https://aws.amazon.com/blogs/aws/announcing-the-aws-sustainability-console-programmatic-access-configurable-csv-reports-and-scope-1-3-reporting-in-one-place/)
- [Sustainability Pillar - AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html)
- [Amazon Bedrock cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)

**Các video liên quan:**

- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)

**Các dịch vụ liên quan:**

- [AWS Sustainability](https://aws.amazon.com/sustainability/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
