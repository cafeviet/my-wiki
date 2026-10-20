# AGENTREL04-BP02 Phân loại các tác nhân bằng một phân loại năng lực kỹ lưỡng

Các bộ điều phối chọn tác nhân theo các định danh gán cứng không thể thích ứng khi tác nhân ưu tiên không khả dụng hoặc khi một tác nhân tương đương mới xuất hiện. Một phân loại năng lực có cấu trúc cho bộ điều phối một cơ sở để ra quyết định định tuyến, và việc thay thế trở nên tự động thay vì một lần triển khai lại.

**Kết quả mong muốn:**

- Bạn có mọi tác nhân được đăng ký với các loại năng lực, kỹ năng, ràng buộc đầu vào/đầu ra, hồ sơ hiệu năng và phụ thuộc.
- Các bộ điều phối của bạn tham vấn registry để chọn tác nhân thay vì gán cứng các định danh.
- Bạn giữ registry luôn cập nhật thông qua đường ống CI/CD để nó phản ánh trạng thái đã triển khai.

**Các phản mẫu thường gặp (anti-patterns):**

- Gán cứng việc chọn tác nhân trong logic điều phối mà không tham vấn một registry năng lực, làm giảm khả năng định tuyến động.
- Định nghĩa năng lực ở mức chi tiết quá thô, bỏ lỡ các sắc thái về kỹ năng, hạn chế và yêu cầu tài nguyên.
- Để registry năng lực trôi khỏi trạng thái đã triển khai khi các tác nhân được cập nhật.

**Lợi ích khi áp dụng thực hành tốt này:**

- Định tuyến tác vụ tất định thông qua khớp năng lực có cấu trúc thay vì thử-và-sai.
- Thay thế tác nhân tự động khi các tác nhân ưu tiên không khả dụng, mà không cần cấu hình lại thủ công.
- Ít lỗi tác vụ hơn do các sai khớp năng lực thông qua khớp năng lực-tới-tác vụ chính xác.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Một registry năng lực chỉ hữu ích nếu nó luôn cập nhật. Để giữ nó cập nhật, hãy tích hợp việc đăng ký vào đường ống triển khai. Một tác nhân tới môi trường vận hành bằng cách đi qua một bước cũng cập nhật mục của nó trong [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html). Bỏ qua bước đó và registry trở thành một hiện vật tài liệu phân kỳ khỏi thực tế trong vòng vài tuần.

Tìm kiếm năng lực ngữ nghĩa của AgentCore Registry làm cho registry hữu ích lúc chạy. Các bộ điều phối khám phá tác nhân qua các truy vấn ngôn ngữ tự nhiên khớp yêu cầu tác vụ với năng lực tác nhân mà không cần logic định tuyến gán cứng. Chất lượng kết quả tìm kiếm phụ thuộc nặng vào chất lượng của các mô tả bản ghi. Các mô tả giải thích mỗi tác nhân làm gì và các vấn đề nó giải quyết bằng ngôn ngữ giản dị sẽ tạo ra các kết quả khớp tốt. Các mô tả đọc như chữ ký hàm sẽ tạo ra các kết quả khớp tồi.

Định tuyến được xây dựng bên trên dữ liệu registry. Lớp khớp năng lực nhận một đặc tả tác vụ và trả về các tác nhân đã xếp hạng thỏa mãn các yêu cầu, sắp theo chất lượng khớp và độ phù hợp vận hành. Dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để định tuyến các lời gọi tới tác nhân được chọn. Giám sát hiệu quả định tuyến qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Các lỗi khớp năng lực và các quyết định định tuyến dẫn tới lỗi là các tín hiệu bạn dùng để tìm ra các khoảng trống năng lực.

### Các bước triển khai

- **Đăng ký mọi tác nhân trong AgentCore Registry:** Điền vào [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) các loại năng lực, kỹ năng, ràng buộc và hồ sơ hiệu năng cho mỗi tác nhân.
- **Tự động hóa việc đăng ký trong đường ống CI/CD:** Làm cho bước triển khai cập nhật môi trường vận hành cũng cập nhật registry để cả hai luôn đồng bộ.
- **Dùng tìm kiếm lai (hybrid search) của AgentCore Registry để khớp tác vụ với tác nhân:** Viết các mô tả bản ghi bằng ngôn ngữ tự nhiên giải thích mỗi tác nhân làm gì và các vấn đề nó giải quyết, để tìm kiếm ngữ nghĩa tạo ra các kết quả khớp chính xác.
- **Cấu hình các bộ điều phối để tham vấn registry:** Thay các định danh tác nhân gán cứng bằng tra cứu registry.
- **Giám sát hiệu quả định tuyến:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để tìm các sai khớp và khoảng trống năng lực.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL04-BP01 Triển khai mẫu tác nhân trọng tài (arbiter) cho các hệ thống đa tác nhân được phối hợp](agentrel04-bp01.md)
- [AGENTREL04-BP03 Triển khai các cơ chế dự phòng và suy giảm nhẹ nhàng cho các luồng công việc cộng tác](agentrel04-bp03.md)
- [AGENTREL04-BP04 Triển khai các control plane bền bỉ cho việc phối hợp tác nhân](agentrel04-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [The future of managing agents at scale: AWS Agent Registry now in preview](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Registry: Discover, Govern, and Reuse AI Agents at Scale](https://www.youtube.com/watch?v=rIcOJrE-fTk)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
