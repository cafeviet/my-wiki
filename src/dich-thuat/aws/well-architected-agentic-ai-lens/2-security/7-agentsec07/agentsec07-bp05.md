# AGENTSEC07-BP05 Đánh giá bảo mật định kỳ và red teaming

Các kiểm soát bảo mật chưa được kiểm thử suy giảm âm thầm khi các kỹ thuật tiến hóa và các cấu hình trôi dạt. Sự kết hợp giữa quét tự động liên tục và các bài tập red team định kỳ do con người dẫn dắt kiểm chứng rằng các guardrail, các quy tắc phát hiện và các quy trình ứng phó vẫn hoạt động trước các cuộc tấn công hiện tại.

**Kết quả mong muốn:**

- Bạn chạy quét bảo mật tự động liên tục đối với các lần triển khai agent (trên mỗi lần triển khai và theo lịch) và tiến hành các bài tập red team do con người dẫn dắt theo một nhịp định kỳ với các kịch bản nhắm vào việc thao túng agent, bao gồm prompt injection, chiếm đoạt mục tiêu (goal hijacking) và lạm dụng công cụ.
- Bạn ghi tài liệu các phát hiện, theo dõi chúng đến lúc khắc phục, và dùng chúng để cập nhật các kiểm soát bảo mật và các quy tắc phát hiện.

**Các phản mẫu thường gặp (anti-patterns):**

- Tiến hành các đánh giá bảo mật ứng dụng chung mà không có các kịch bản riêng của agent, bỏ sót prompt injection, đầu độc bộ nhớ, và các vấn đề phối hợp đa agent mà kiểm thử truyền thống không bao phủ.
- Chỉ thực hiện các bài tập red team tại lần triển khai ban đầu mà không lên lịch các đánh giá định kỳ, bỏ sót các kỹ thuật nổi lên khi môi trường đe dọa tiến hóa.
- Không theo dõi các phát hiện đến lúc khắc phục, để cho các vấn đề được nhận diện tồn tại nên cuộc đánh giá tạo ra công việc nhưng không cải thiện tình trạng.
- Tiến hành các hoạt động red team và blue team một cách cô lập mà không có sự phối hợp purple team, giới hạn việc chuyển giao tri thức giúp cải thiện phát hiện và ứng phó.

**Lợi ích khi áp dụng thực hành tốt này:**

- Kiểm thử thực tế xác nhận các guardrail, các quy tắc phát hiện và các quy trình ứng phó hoạt động trước các kỹ thuật hiện tại.
- Các phát hiện đánh giá thúc đẩy các cập nhật cho các cấu hình guardrail, các ranh giới quyền hạn và các quy tắc phát hiện trong một vòng phản hồi liên tục.
- Các hoạt động purple team chuyển giao tri thức từ red team sang blue team, cải thiện khả năng của tổ chức trong việc phát hiện và ứng phó các vấn đề riêng của agent.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Nhịp đánh giá cần khớp với mức rủi ro của từng lần triển khai agent. Quét tự động chạy liên tục, và các bài tập red team thủ công chạy theo một lịch. Đối với kiểm thử tác tử tự động, [AWS Security Agent](https://aws.amazon.com/security-agent/) cung cấp kiểm thử xâm nhập theo yêu cầu thực thi các chuỗi tấn công được điều chỉnh theo ứng dụng đích, bao phủ prompt injection, jailbreak, chiếm đoạt mục tiêu và các mẫu liên quan (xem AGENTSEC09-BP02 để tích hợp nó vào các luồng công việc kiểm thử xâm nhập rộng hơn). Hãy bổ sung kiểm thử tự động bằng các bài tập thủ công khám phá các kịch bản mới riêng của kiến trúc agent của bạn.

Các kịch bản red team cần có cấu trúc. [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) bao phủ các rủi ro thao túng agent một cách cụ thể — prompt injection, lạm dụng công cụ, lạm dụng danh tính và đặc quyền, và chiếm đoạt hành vi agent — và [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) bao phủ các rủi ro ở cấp mô hình vẫn còn áp dụng. Hãy xây dựng một thư viện kịch bản bao phủ các vấn đề phối hợp đa agent, đầu độc bộ nhớ, lạm dụng công cụ và các kỹ thuật vượt qua human-in-the-loop, và ghi tài liệu mỗi kịch bản với mô tả, cơ chế phát hiện mong đợi và tiêu chí thành công.

[Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) hỗ trợ quá trình đánh giá bằng cách cung cấp một đường cơ sở chất lượng liên tục. Chạy các đánh giá trước và sau các bài tập red team đo lường liệu bài tập có phơi bày sự suy giảm chất lượng mà các trình đánh giá hiện có không bắt được, và các kết quả tinh chỉnh các prompt trình đánh giá tùy chỉnh và các ngưỡng chấm điểm.

Lưu trữ bền vững, có quản lý phiên bản giữ cho bản ghi lịch sử nguyên vẹn. Hãy lưu các kịch bản, các kết quả thực thi và việc theo dõi khắc phục trong Amazon S3 với versioning được bật, hoặc trong một hệ thống quản lý kiểm thử riêng duy trì lịch sử thay đổi. Hãy ánh xạ các phát hiện red team vào khung kiểm soát tuân thủ của bạn để các kết quả đánh giá tạo ra bằng chứng kiểm toán nhất quán với các yêu cầu quy định của bạn.

Các hoạt động purple team đóng vòng lặp. Đưa red team và blue team lại với nhau để rà soát các kịch bản và các phản hồi phát hiện cập nhật các cảnh báo Amazon CloudWatch, các cấu hình Guardrails và các runbook ứng phó sự cố dựa trên các mẫu quan sát được. Theo dõi các cải thiện về thời gian phát hiện và hiệu quả ứng phó qua các chu kỳ chứng minh giá trị của chương trình.

### Các bước triển khai

- **Thiết lập một lịch đánh giá:** Đặt một nhịp phù hợp với mức rủi ro của từng lần triển khai agent.
- **Xây dựng một thư viện kịch bản:** Phát triển các kịch bản red team dựa trên OWASP Top 10 for Agentic Applications (chính) và OWASP Top 10 for LLM Applications (bổ sung), bao phủ prompt injection, đầu độc bộ nhớ, lạm dụng công cụ và vượt qua HITL.
- **Tích hợp kiểm thử tác tử tự động:** Triển khai các công cụ red teaming AI tác tử và đưa chúng vào luồng công việc đánh giá để bao phủ tự động các mẫu phổ biến.
- **Đo tác động chất lượng trước và sau:** Chạy [Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/) trước và sau các bài tập red team để đo tác động chất lượng và tinh chỉnh các cấu hình trình đánh giá.
- **Lưu bền vững và ánh xạ các phát hiện:** Lưu các kịch bản, kết quả và việc theo dõi khắc phục trong lưu trữ bền vững, có quản lý phiên bản (Amazon S3 với versioning được bật), và ánh xạ các phát hiện vào khung kiểm soát tuân thủ của bạn để có bằng chứng kiểm toán.
- **Chạy các phiên purple team:** Cập nhật các quy tắc phát hiện, các cấu hình guardrail và các runbook ứng phó sự cố dựa trên các phát hiện của mỗi chu kỳ đánh giá.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC04-BP01 Triển khai guardrails và các kiểm soát căn chỉnh](../4-agentsec04/agentsec04-bp01.md)
- [AGENTSEC07-BP04 Phát hiện bất thường hành vi và kiềm chế agent](agentsec07-bp04.md)
- [AGENTSEC08-BP01 Kiểm định đầu vào nhiều lớp và phòng thủ chống prompt injection](../8-agentsec08/agentsec08-bp01.md)

**Tài liệu liên quan:**

- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [Responsible AI in action: How Data Reply red teaming supports generative AI safety on AWS](https://aws.amazon.com/blogs/machine-learning/responsible-ai-in-action-how-data-reply-red-teaming-supports-generative-ai-safety-on-aws/)
- [Protect DeepSeek model deployments with Protect AI and Amazon Bedrock](https://aws.amazon.com/blogs/apn/protect-deepseek-model-deployments-with-protect-ai-and-amazon-bedrock/)
- [Amazon Bedrock AgentCore adds quality evaluations and policy controls](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)

**Dịch vụ liên quan:**

- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
