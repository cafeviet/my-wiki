# AGENTSEC06-BP03 Thiết lập các ranh giới tin cậy giữa các agent

Một mạng agent phẳng cho mỗi agent bị ảnh hưởng một đường trực tiếp tới mọi agent khác. Các vùng tin cậy được phân đoạn ở các lớp mạng và IAM, với việc kiểm chứng danh tính người gọi ở lớp ứng dụng, chặn một agent bị ảnh hưởng leo thang qua toàn bộ hệ thống.

**Kết quả mong muốn:**

- Agent hoạt động trong các vùng tin cậy được định nghĩa rõ ràng, chỉ chấp nhận các chỉ thị từ các bộ điều phối được ủy quyền và từ chối các yêu cầu từ các agent ngoài ranh giới tin cậy của chúng.
- Phân đoạn mạng thực thi các ranh giới tin cậy ở lớp hạ tầng và các chính sách IAM thực thi chúng ở lớp API.
- Một agent bị ảnh hưởng trong một vùng tin cậy không thể trực tiếp phát các chỉ thị tới các agent trong các vùng tin cậy cao hơn mà không đi qua các kiểm soát ủy quyền.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai mọi agent trong một mạng phẳng không có phân đoạn, để cho bất kỳ agent nào giao tiếp trực tiếp với bất kỳ agent khác bất kể mức tin cậy, nên một vấn đề lan ngang.
- Chỉ dựa vào các ranh giới tin cậy ở cấp mạng mà không có ủy quyền ở lớp ứng dụng, nên bất kỳ agent nào chạm tới điểm cuối của một agent khác có thể phát các chỉ thị.
- Không kiểm chứng danh tính của agent điều phối trước khi thực thi các chỉ thị, để cho bất kỳ agent nào mạo danh một bộ điều phối và phát các lệnh trái phép.
- Coi mọi agent nội bộ là tin cậy ngầm định trong khi chỉ hiện thực các ranh giới tin cậy cho các agent hướng ra ngoài, tạo ra một mô hình tin cậy nội bộ phẳng khuếch đại tác động của bất kỳ vấn đề nội bộ nào.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phân đoạn vùng tin cậy kiềm chế tác động của một agent bị ảnh hưởng vào chính vùng tin cậy của nó, giúp ngăn di chuyển ngang.
- Thực thi phân lớp ở cả cấp mạng (phân đoạn VPC, security group) lẫn cấp ứng dụng (chính sách IAM, kiểm chứng danh tính agent) cung cấp chiều sâu phòng thủ.
- Kiến trúc tin cậy có tài liệu hỗ trợ các kiểm tra tuân thủ tự động bắt được trôi dạt khi các cấu hình tiến hóa.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các kiểm soát ranh giới tin cậy áp dụng bất kể giao thức giữa các agent được dùng, dù là A2A, MCP hay REST tùy chỉnh. Các kiểm soát ở lớp mạng (phân đoạn VPC, security group, AWS PrivateLink) và các kiểm soát ở lớp IAM (chính sách dựa trên tài nguyên, các Điều kiện IAM) thực thi các ranh giới độc lập với giao thức ứng dụng. Hướng dẫn riêng theo giao thức áp dụng lên trên các kiểm soát chung này.

Một kiến trúc vùng tin cậy bắt đầu với các tầng phản ánh rủi ro thực tế: công khai (public), vận hành nội bộ (internal operational), đặc quyền (privileged). Hãy thực thi các tầng ở mạng với các Amazon VPC hoặc VPC security group riêng, và dùng Amazon VPC peering hoặc AWS Transit Gateway với các kiểm soát bảng định tuyến để hạn chế giao tiếp giữa các vùng chỉ ở các đường cần thiết. Riêng phân đoạn mạng không kiểm chứng danh tính người gọi, nên hãy kết hợp nó với ủy quyền ở lớp ứng dụng.

Hỗ trợ giao thức A2A của [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/) cung cấp một framework có cấu trúc cho giao tiếp giữa các agent với cô lập phiên và xác thực dựng sẵn. Khi các agent khám phá các đồng đẳng qua các agent card A2A, lược đồ card quảng bá các năng lực và các yêu cầu xác thực của agent. Hãy cấu hình các agent chỉ chấp nhận các kết nối A2A từ các bộ điều phối mà agent card của chúng khớp với danh tính và mức tin cậy mong đợi. Với các agent không dùng A2A, Amazon API Gateway với các AWS Lambda authorizer hiện thực logic ủy quyền agent-tới-agent tùy chỉnh kiểm chứng các token danh tính agent và thực thi các yêu cầu mức tin cậy.

Các chính sách dựa trên tài nguyên trên các điểm cuối agent liệt kê tường minh các principal IAM được ủy quyền gọi mỗi agent. Các Điều kiện IAM hạn chế các lần gọi tới các agent trong cùng vùng tin cậy hoặc tới các vai trò agent điều phối cụ thể. AWS PrivateLink giữ các giao tiếp agent xuyên vùng trên các đường mạng riêng tư. [Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) củng cố các ranh giới tin cậy ở lớp công cụ: các chính sách Cedar có thể bao gồm các điều kiện về danh tính và mức tin cậy của principal đang gọi, nên ngay cả khi một agent có thể chạm tới các công cụ của một agent khác qua gateway, bộ máy chính sách chặn các lời gọi công cụ vi phạm các quy tắc vùng tin cậy.

Kiểm chứng tuân thủ phát hiện trôi dạt so với tư thế mạng dự định. Các quy tắc AWS Config quản lý — vpc-sg-open-only-to-authorized-ports cho ingress công khai ngoài ý muốn, restricted-ssh cho truy cập SSH từ 0.0.0.0/0, vpc-sg-port-restriction-check cho các hạn chế ở cấp cổng — bao phủ vệ sinh mạng đường cơ sở. Kiểm chứng riêng theo vùng tin cậy (rằng các quy tắc security group chỉ tham chiếu các dải CIDR hoặc các ID security group từ cùng vùng tin cậy) cần các quy tắc AWS Config tùy chỉnh được hậu thuẫn bởi AWS Lambda, và các cảnh báo kích hoạt khi có bất kỳ thay đổi cấu hình nào sẽ tạo ra kết nối xuyên vùng trái phép.

### Các bước triển khai

- **Thiết kế các tầng vùng tin cậy:** Định nghĩa các tầng (công khai, vận hành nội bộ, đặc quyền) và ghi tài liệu các đường giao tiếp được ủy quyền giữa các vùng.
- **Phân đoạn ở lớp mạng:** Tạo các Amazon VPC hoặc security group riêng cho từng vùng tin cậy và cấu hình các kiểm soát mạng (VPC peering, các bảng định tuyến AWS Transit Gateway) để thực thi các ranh giới vùng.
- **Thực thi danh tính ở lớp ứng dụng:** Với các agent trên [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/), cấu hình khám phá agent card A2A với các yêu cầu xác thực thực thi kiểm chứng mức tin cậy. Với các agent không trên AgentCore Runtime, dùng Amazon API Gateway với các AWS Lambda authorizer để thực thi ranh giới tin cậy tùy chỉnh.
- **Áp dụng các chính sách IAM dựa trên tài nguyên:** Chỉ liệt kê các principal điều phối được ủy quyền trong chính sách tài nguyên của mỗi điểm cuối agent, với các Điều kiện IAM hạn chế các lần gọi theo vùng tin cậy.
- **Củng cố ở lớp công cụ bằng Policy:** Cấu hình các chính sách Cedar trong [Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/) với các điều kiện về danh tính và mức tin cậy của principal đang gọi.
- **Giữ lưu lượng xuyên vùng ở dạng riêng tư:** Hiện thực AWS PrivateLink cho các giao tiếp agent xuyên vùng.
- **Kiểm chứng các cấu hình liên tục:** Triển khai các quy tắc AWS Config quản lý (vpc-sg-open-only-to-authorized-ports, restricted-ssh, vpc-sg-port-restriction-check) cho vệ sinh đường cơ sở và các quy tắc AWS Config tùy chỉnh cho kiểm chứng riêng theo vùng tin cậy, cảnh báo về bất kỳ thay đổi nào sẽ tạo ra kết nối xuyên vùng trái phép.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](../3-agentsec03/agentsec03-bp03.md)
- [AGENTSEC06-BP01 Mã hóa và ký các thông điệp giữa các agent](agentsec06-bp01.md)
- [AGENTSEC06-BP02 Triển khai các kiểm soát bảo mật điều phối luồng công việc](agentsec06-bp02.md)

**Tài liệu liên quan:**

- [Introducing agent-to-agent protocol support in Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [Secure AI agents with Policy in Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore/)
- [AWS VPC security best practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [AWS Config managed rules reference](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)
- [AWS Config custom rules with Lambda](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_lambda-functions.html)
- [Security reference architecture for generative AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/gen-ai-sra.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [Amazon VPC](https://aws.amazon.com/vpc/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [AWS PrivateLink](https://aws.amazon.com/privatelink/)
- [AWS Config](https://aws.amazon.com/config/)
