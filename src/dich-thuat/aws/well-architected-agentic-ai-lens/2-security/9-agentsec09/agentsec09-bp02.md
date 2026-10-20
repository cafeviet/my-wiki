# AGENTSEC09-BP02 Tiến hành kiểm thử xâm nhập có nhận thức ngữ cảnh với mô phỏng tấn công đa agent

Các bộ quét chung bỏ sót các lỗ hổng chỉ nổi lên trong điều phối agent, dựng tham số công cụ và ủy thác giữa các agent. Kiểm thử có nhận thức ngữ cảnh được điều khiển bởi các agent tấn công chuyên biệt thích ứng với những gì ứng dụng phơi bày tìm được các khai thác được xâu chuỗi mà các script tĩnh không thể vươn tới.

**Kết quả mong muốn:**

- Bạn dùng mô phỏng tấn công đa agent, có nhận thức ngữ cảnh cho kiểm thử xâm nhập thích ứng với ứng dụng cụ thể đang được kiểm thử.
- Hệ thống kiểm thử phát triển sự hiểu biết sâu về kiến trúc, các luồng dữ liệu và các tương tác agent của ứng dụng, rồi thực thi các chuỗi tấn công tinh vi kết hợp nhiều loại lỗ hổng.
- Các phát hiện được kiểm chứng qua khai thác thực tế, được ưu tiên theo khả năng khai thác trong thực tế, và được ghi tài liệu với các đường tấn công có thể tái tạo và các bản sửa sẵn sàng để hiện thực.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy các bộ quét lỗ hổng chung đối với các hệ thống AI tác tử mà không điều chỉnh các kịch bản kiểm thử theo các năng lực cụ thể và các tích hợp công cụ của agent, bỏ sót tiêm nhiễm tham số công cụ, đầu độc bộ nhớ và leo thang đặc quyền chuỗi ủy thác.
- Kiểm thử các thành phần agent riêng lẻ một cách cô lập mà không thực thi các đường phối hợp đa agent, bỏ sót các vi phạm ranh giới tin cậy và các thất bại lan tràn từ một agent bị xâm phạm trong một chuỗi điều phối.
- Dựa vào các script kiểm thử được định trước không thích ứng dựa trên các phản hồi của ứng dụng, bỏ sót các lỗ hổng đòi hỏi khám phá động vì các hệ thống tác tử hành xử khác nhau dựa trên ngữ cảnh và các tương tác trước đó.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm thử có nhận thức ngữ cảnh thích ứng với ứng dụng cụ thể, khám phá các lỗ hổng mà các script kiểm thử tĩnh và các bộ quét chung bỏ sót.
- Khai thác thực tế kiểm chứng các phát hiện, giảm các dương tính giả và cho phép các nhóm ưu tiên dựa trên rủi ro thực.
- Các agent chuyên biệt phối hợp về trinh sát, phân tích lỗ hổng, kiểm chứng khai thác và ưu tiên phát hiện, nhận diện các lỗ hổng được xâu chuỗi kết hợp tiết lộ thông tin với leo thang đặc quyền.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Kiểm thử xâm nhập truy đuổi các lỗ hổng agent phải trông giống cuộc tấn công mà nó đang mô phỏng. Các agent tấn công không chạy cùng một script trên mọi mục tiêu. Chúng lập bản đồ bề mặt, dò tìm các điểm yếu, thích ứng với các phản hồi, và xâu chuỗi các phát hiện. Các công cụ kiểm thử cần làm điều tương tự nếu không chúng bỏ sót đúng những kịch bản quan trọng nhất đối với các hệ thống tác tử.

Một hệ thống kiểm thử xâm nhập đa agent điều phối các agent bảo mật chuyên biệt một cách phối hợp. Hệ thống bắt đầu với quét đường cơ sở để thiết lập độ bao phủ, rồi tiến hành trinh sát rộng để lập bản đồ bề mặt ứng dụng và nhận diện các vector tấn công ban đầu. Xây dựng trên các phát hiện này, nó động sinh ra các tác vụ kiểm thử tập trung được tùy chỉnh theo ngữ cảnh ứng dụng cụ thể, suy luận về các điểm cuối được khám phá, các mẫu logic kinh doanh và các chuỗi lỗ hổng tiềm tàng.

[AWS Security Agent](https://aws.amazon.com/security-agent/) cung cấp kiểm thử xâm nhập theo yêu cầu với cách tiếp cận đa agent này. Nó triển khai các agent AI chuyên biệt phát triển ngữ cảnh ứng dụng từ tài liệu và các thông tin xác thực được cung cấp, rồi thực thi các chuỗi tấn công để nhận diện các lỗ hổng phức tạp mà các công cụ thông thường bỏ sót. Kiến trúc bao gồm các agent cho lập bản đồ bề mặt tấn công, phân tích logic kinh doanh, kiểm chứng phát hiện và ưu tiên lỗ hổng dựa trên khả năng khai thác thực tế được chấm điểm bằng Common Vulnerability Scoring System (CVSS). Hệ thống thực hiện các cuộc tấn công được xâu chuỗi, kết hợp một lỗ hổng tiết lộ thông tin với leo thang đặc quyền để chạm tới các tài nguyên nhạy cảm, hoặc xâu chuỗi các tham chiếu đối tượng trực tiếp không an toàn (insecure direct object references) với vượt qua xác thực, thay vì dừng lại ở phát hiện lỗ hổng đơn lẻ.

AWS Security Agent bắt đầu với OWASP Top 10 và rồi tùy chỉnh cách tiếp cận của nó dựa trên ngữ cảnh nó học được từ các tài liệu và mã. Agent thích ứng với các phản hồi nó nhận được, xây dựng một kế hoạch tấn công tùy chỉnh cho mỗi ứng dụng. Hãy cung cấp các URL đích, các chi tiết xác thực, mã nguồn và tài liệu để agent có thể phát triển sự hiểu biết sâu về ứng dụng trước khi kiểm thử bắt đầu.

Các kịch bản riêng của agent cần bổ sung thủ công. Các chuỗi prompt injection xuyên các ranh giới agent, thao túng tham số công cụ, đầu độc bộ nhớ qua các đầu ra công cụ được chế tạo, và các kỹ thuật vượt qua human-in-the-loop đều đòi hỏi các kịch bản vượt ra ngoài đường cơ sở OWASP. Hãy dùng các phát hiện từ AGENTSEC07-BP05 để cung cấp cho thư viện kịch bản.

### Các bước triển khai

- **Cung cấp ngữ cảnh ứng dụng cho agent kiểm thử:** Cấu hình [AWS Security Agent](https://aws.amazon.com/security-agent/) với các chi tiết ứng dụng đích bao gồm các URL, các thông tin xác thực (được lưu trong AWS Secrets Manager), mã nguồn và tài liệu kiến trúc.
- **Chạy các bài kiểm thử trên toàn bộ bề mặt:** Thực thi các bài kiểm thử xâm nhập theo yêu cầu thực thi các điểm cuối điều phối agent, các đường gọi công cụ và các kênh giao tiếp đa agent.
- **Phân loại các phát hiện đã kiểm chứng theo khả năng khai thác:** Rà soát các phát hiện với các đường tấn công có thể tái tạo, phân tích tác động và các bản sửa mã được gợi ý, và ưu tiên khắc phục dựa trên các điểm CVSS và khả năng khai thác thực tế.
- **Thêm các kịch bản riêng của agent một cách thủ công:** Bổ sung kiểm thử tự động bằng các kịch bản nhắm vào các chuỗi prompt injection, thao túng tham số công cụ và các vi phạm ranh giới tin cậy đa agent.
- **Theo dõi tình trạng theo thời gian:** Lưu các kết quả kiểm thử xâm nhập và so sánh chúng qua các chu kỳ kiểm thử để đo lường cải thiện tình trạng bảo mật.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC07-BP05 Đánh giá bảo mật định kỳ và red teaming](../7-agentsec07/agentsec07-bp05.md)
- [AGENTSEC02-BP02 Kiểm định đầu vào và đầu ra của công cụ](../2-agentsec02/agentsec02-bp02.md)
- [AGENTSEC09-BP01 Tích hợp quét lỗ hổng có AI hỗ trợ trên toàn vòng đời phát triển](agentsec09-bp01.md)

**Tài liệu liên quan:**

- [Inside AWS Security Agent: A multi-agent architecture for automated penetration testing](https://aws.amazon.com/blogs/security/inside-aws-security-agent-a-multi-agent-architecture-for-automated-penetration-testing/)
- [AWS Security Agent FAQs](https://aws.amazon.com/security-agent/faqs/)
- [Security Considerations for AWS Security Agent and AI assisted penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Dịch vụ liên quan:**

- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
