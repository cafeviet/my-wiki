# AGENTOPS07-BP04 Triển khai các runbook vận hành phá kính (break-glass)

Hãy viết và kiểm thử các runbook khẩn cấp trước khi cần đến chúng. Các quy trình dự phòng thủ công đã được diễn tập, các đường leo thang có thể truy cập, và thông tin liên hệ cập nhật biến một lỗi agent hoàn toàn thành một giai đoạn thủ công ngắn ngủi thay vì một gián đoạn kéo dài.

**Kết quả mong muốn:**

- Khi các agent thất bại hoàn toàn hoặc hành xử bất ngờ, người vận hành thực thi các quy trình thủ công được tài liệu hóa tốt để duy trì tính liên tục kinh doanh.
- Các runbook phá kính được kiểm thử thường xuyên, và người vận hành được đào tạo và tự tin về các quy trình thủ công.
- Các đường leo thang và thông tin liên hệ luôn cập nhật.
- Thời gian ứng phó khẩn cấp đáp ứng các mục tiêu được xác định vì các quy trình được tài liệu hóa, có thể truy cập, và được thực hành.

**Các phản mẫu thường gặp (anti-patterns):**

- Giả định rằng các hệ thống agent sẽ luôn sẵn có và không tài liệu hóa các quy trình dự phòng thủ công, khiến người vận hành không có hướng dẫn khi các agent thất bại trong các hoạt động kinh doanh quan trọng.
- Tạo các runbook phá kính một lần và không bao giờ kiểm thử hay cập nhật chúng, dẫn tới các quy trình tham chiếu các hệ thống lỗi thời, các liên hệ không chính xác, hoặc các bước không còn hoạt động.
- Lưu các quy trình khẩn cấp trong các vị trí không thể truy cập trong các kịch bản gián đoạn mà chúng được thiết kế để giải quyết (ví dụ, trong các hệ thống phụ thuộc vào chính hạ tầng agent đang thất bại).
- Thiết kế các quy trình dự phòng thủ công đòi hỏi kiến thức chuyên biệt chỉ có ở một hoặc hai thành viên nhóm, tạo ra các điểm lỗi đơn trong ứng phó khẩn cấp.
- Không xác định các tác nhân kích hoạt rõ ràng cho khi nào nên kích hoạt các quy trình phá kính, gây ra chậm trễ khi người vận hành tranh luận liệu tình huống có xứng đáng để can thiệp thủ công hay không.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các quy trình phá kính được tài liệu hóa hỗ trợ các phản ứng khẩn cấp nhất quán bất kể ai đang trực.
- Các runbook phá kính chính thức hóa việc chuyển từ vận hành agent tự động sang các quy trình do con người điều khiển, giữ cho tính liên tục kinh doanh nguyên vẹn khi các hệ thống agent không thể hoạt động.
- Các buổi diễn tập thường xuyên giữ cho các quy trình cập nhật và người vận hành sẵn sàng, để chất lượng ứng phó không phụ thuộc vào việc ai đang trực.
- Các tác nhân kích hoạt rõ ràng loại bỏ sự do dự làm chậm phản ứng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hãy kiểm kê hệ thống của bạn bằng cách xác định mọi quy trình kinh doanh quan trọng phụ thuộc vào các hệ thống agent và đánh giá tác động của tình trạng agent không khả dụng cho mỗi quy trình. Đầu ra là một danh sách xếp hạng các quy trình cần được bao phủ phá kính, từ các bất tiện ngắn ngủi tới các vấn đề dừng dịch vụ. Các quy trình ở đầu danh sách nhận runbook trước.

Mỗi runbook nên bao phủ các điều kiện kích hoạt, các chỉ dẫn thực thi thủ công từng bước, các thông tin xác thực truy cập cần thiết, các liên hệ leo thang với nhân sự chính và dự phòng, các thời gian hoàn thành kỳ vọng, và các tiêu chí để trở về vận hành tự động. Chế độ lỗi phổ biến nhất, và cũng nguy hiểm nhất, là các runbook được lưu trong các hệ thống phụ thuộc vào chính hạ tầng mà chúng được thiết kế để làm việc thay thế. Một runbook khẩn cấp được lưu trong một wiki phụ thuộc vào chính hạ tầng agent là một runbook bạn không thể đọc trong lúc gián đoạn. Hãy lưu các runbook trong một vị trí sẵn sàng cao, độc lập với agent, với các bản sao ngoại tuyến (offline) có thể truy cập cho người vận hành trực.

Tri thức một-người là điểm lỗi đơn phổ biến còn lại. Thiết kế các quy trình thủ công mà chỉ một hoặc hai người có thể thực thi tạo ra một kế hoạch sụp đổ khi những người đó không sẵn có. Hãy mở rộng nền tảng tri thức thông qua các bài tập tabletop, tài liệu không giả định chuyên môn, và đào tạo chéo (cross-training) thường xuyên.

Các tác nhân kích hoạt loại bỏ sự do dự khỏi phản ứng. Các điều kiện rõ ràng, ví dụ, "tỷ lệ lỗi agent vượt 50% trong 15 phút" hoặc "hạ tầng agent hoàn toàn không khả dụng trong 5 phút", cho người vận hành biết khi nào chuyển sang các quy trình thủ công mà không phải chờ các phán đoán dưới áp lực. Các cảnh báo tự động nêu tên rõ ràng các điều kiện kích hoạt mà chúng đã đáp ứng khiến quyết định trở nên hiển nhiên.

Kiểm thử giữ cho các runbook luôn sống. Các bài tập tabletop theo quý, người vận hành đi qua các bước runbook mà không thực thi chúng, bắt được các tham chiếu lỗi thời và các bước bị thiếu. Các buổi diễn tập đầy đủ hai lần một năm, người vận hành thực sự thực thi các quy trình thủ công trong một môi trường phi sản xuất, bắt được mọi thứ mà các bài tập tabletop bỏ lỡ. Kết quả diễn tập trở thành đầu vào cho các bản sửa runbook, không chỉ là phản hồi đào tạo.

### Các bước triển khai

- **Kiểm kê các quy trình kinh doanh quan trọng:** Đánh giá tác động của tình trạng agent không khả dụng cho mỗi quy trình để tạo ra một danh sách xếp hạng.
- **Tài liệu hóa các quy trình dự phòng thủ công:** Bao phủ mỗi quy trình quan trọng, giả định không có tình trạng sẵn sàng của hệ thống agent, với các chỉ dẫn từng bước.
- **Thiết lập các đường leo thang:** Bao gồm các liên hệ chính và dự phòng, với một quy trình để giữ cho thông tin liên hệ luôn cập nhật.
- **Lưu các runbook một cách độc lập:** Dùng một vị trí sẵn sàng cao, độc lập với agent với các bản sao ngoại tuyến có thể truy cập cho người vận hành trực.
- **Xác định các tác nhân kích hoạt rõ ràng:** Cấu hình các cảnh báo tự động thông báo cho người vận hành khi các điều kiện kích hoạt được đáp ứng.
- **Tiến hành các bài tập theo nhịp:** Chạy các bài tập tabletop theo quý và các buổi diễn tập đầy đủ hai lần một năm, và cập nhật các quy trình dựa trên các phát hiện.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS07-BP01 Triển khai các cơ chế ứng phó và phục hồi tự động](agentops07-bp01.xml)
- [AGENTOPS07-BP02 Thiết lập các hệ thống quản lý tri thức vận hành](agentops07-bp02.xml)
- [AGENTOPS07-BP03 Bổ sung quản trị thay đổi để đáp ứng các cải tiến kỹ thuật và các yêu cầu kinh doanh](agentops07-bp03.xml)
- [AGENTOPS04-BP03 Phát triển hành vi dự phòng và xử lý lỗi cho lời gọi Tools](../agentops04/agentops04-bp03.xml)
- [AGENTREL07-BP02 Bật phục hồi tự động từ các lỗi thực thi agent](../../reliability-pillar/agentrel07/agentrel07-bp02.xml)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents)
- [Agentic AI in the Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)
- [From AI agent prototype to product: Lessons from building AWS DevOps Agent](https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent)

**Dịch vụ liên quan:**

- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
