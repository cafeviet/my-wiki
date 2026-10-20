# AGENTPERF07-BP01 Thiết kế các mô hình triển khai tác nhân multitenant hiệu quả

Các tổ chức phục vụ nhiều tenant từ một dịch vụ tác nhân dùng chung đạt được hiệu quả tài nguyên tốt hơn và onboarding tenant nhanh hơn khi mô hình triển khai mang lại hiệu năng nhất quán cho mọi tenant. Các triển khai siloed cung cấp cô lập mạnh với chi phí cao hơn. Các triển khai gộp (pooled) tối đa hóa hiệu quả nhưng cần các cơ chế giúp ngăn các hiệu ứng hàng-xóm-ồn-ào. Các mô hình lai kết hợp cả hai, dùng các tài nguyên gộp cho các tenant standard và các tài nguyên chuyên dụng cho các tenant premium.

**Kết quả mong muốn:**

- Bạn có các triển khai tác nhân multitenant dùng các mô hình triển khai khớp với yêu cầu tenant.
- Bạn có các mô hình triển khai được ghi tài liệu với các đặc trưng hiệu năng rõ ràng và các cam kết SLA cho mỗi tầng.
- Bạn có một mô hình triển khai hỗ trợ onboarding tenant hiệu quả qua cấu hình thay vì cấp phát hạ tầng.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai hạ tầng hoàn-toàn-siloed cho mọi tenant bất kể yêu cầu hiệu năng của họ, tạo ra lãng phí tài nguyên cho các tenant vốn sẽ được phục vụ tốt bởi các tài nguyên gộp.
- Dùng một triển khai gộp duy nhất không có các cơ chế cô lập, cho phép các tenant lượng-lớn tiêu tài nguyên không cân xứng và làm suy giảm hiệu năng cho các bên khác.
- Bỏ qua các tầng tenant với các SLA hiệu năng khác nhau, đối xử với mọi tenant giống hệt bất kể giá trị kinh doanh.

**Lợi ích khi áp dụng thực hành tốt này:**

- Đầu tư tài nguyên giữ tỉ lệ với giá trị tenant và yêu cầu hiệu năng.
- Các cơ chế cô lập phù hợp mang lại hiệu năng nhất quán cho mọi tenant.
- Cấp phát cấu-hình-điều-khiển tăng tốc onboarding tenant.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Định nghĩa các tầng tenant dựa trên yêu cầu hiệu năng và giá trị kinh doanh:

- Một tầng standard dùng các tài nguyên gộp với hiệu năng nỗ-lực-tốt-nhất (best-effort)
- Một tầng premium dùng các tài nguyên chuyên dụng với các mục tiêu SLA mạnh hơn
- (Tùy chọn) Một tầng enterprise với hạ tầng cô lập hoàn toàn

Với các triển khai gộp, [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) cung cấp thực thi cô-lập-phiên tự nhiên giúp ngăn can thiệp liên-tenant ở cấp thực thi tác nhân. Với các tenant cần môi trường container tùy chỉnh, triển khai trên [Amazon EKS](https://aws.amazon.com/eks/) hoặc [Amazon ECS](https://aws.amazon.com/ecs/) với cô lập cấp-namespace hoặc cấp-tác-vụ. Với các nhu cầu tenant đơn giản hơn như trợ lý chat riêng-theo-nhóm hoặc Q&A doanh nghiệp, [Amazon Quick Suite](https://aws.amazon.com/quicksuite/) cung cấp một lựa chọn no-code được quản lý nơi người dùng nghiệp vụ tạo và triển khai các tác nhân mà không cần hạ tầng tùy chỉnh.

Định tuyến nhận-biết-tenant ở lớp API dùng [Amazon API Gateway](https://aws.amazon.com/api-gateway/) với các usage plan cưỡng chế các giới hạn tốc độ theo-tenant và throttling. Ở lớp suy luận, provisioned throughput của Amazon Bedrock cho các tenant premium dung lượng được đặt chỗ trong khi các tenant standard dùng dung lượng theo-yêu-cầu (on-demand). Ngữ cảnh tenant lan truyền qua ngăn xếp tác nhân để mọi thành phần (runtime, bộ nhớ, Tools) áp các cấu hình riêng-của-tenant. Cho cô lập dữ liệu, dùng [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) với các partition key tenant cho truy cập gộp, hoặc các bảng riêng cho các tenant siloed. Onboarding tenant tự động hóa qua [AWS CDK](https://aws.amazon.com/cdk/) hoặc CloudFormation khiến các tenant standard mới là một thay đổi cấu hình thay vì một dự án cấp phát hạ tầng.

### Các bước triển khai

- **Định nghĩa các tầng tenant với các SLA hiệu năng, yêu cầu cô lập, và giá cụ thể:** Định nghĩa các tầng standard, premium, và enterprise tùy chọn với các SLA và kỳ vọng cô lập tường minh.
- **Thiết kế kiến trúc triển khai cho mỗi tầng:** Kiến trúc các triển khai gộp (AgentCore Runtime dùng chung, Amazon Bedrock on-demand), premium (tài nguyên chuyên dụng, provisioned throughput), và enterprise (cô lập hoàn toàn).
- **Triển khai định tuyến nhận-biết-tenant dùng API Gateway với các usage plan và giới hạn tốc độ theo-tenant:** Dùng các usage plan của [Amazon API Gateway](https://aws.amazon.com/api-gateway/) với các giới hạn tốc độ và burst theo-tenant.
- **Cấu hình cô lập dữ liệu dùng các partition key tenant của DynamoDB (gộp) hoặc các bảng riêng (siloed):** Cưỡng chế cô lập dữ liệu ở lớp dữ liệu với các partition key hoặc các bảng riêng tùy theo tầng phù hợp.
- **Tự động hóa onboarding tenant cho mỗi tầng dùng các mẫu CDK/CloudFormation:** Lập mẫu onboarding để các tenant mới được cấp phát qua cấu hình thay vì công việc hạ tầng thủ công.
- **Giám sát các chỉ số hiệu năng theo-tenant để xác nhận tuân thủ SLA:** Công bố các chỉ số theo-tenant tới CloudWatch và cảnh báo khi hiệu năng quan sát được trôi ra ngoài SLA.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF07-BP02 Triển khai cô lập hiệu năng và throttling nhận-biết-tenant](agentperf07-bp02.md)
- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](../2-agentperf02/agentperf02-bp01.md)

**Tài liệu liên quan:**

- [Xây dựng các kiến trúc multi-tenant cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-multitenant/introduction.html)
- [Cưỡng chế cô lập tenant, AI dạng tác nhân multi-tenant](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-multitenant/enforcing-tenant-isolation.html)
- [Vận hành hóa AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)

**Video liên quan:**

- [Xây dựng các tác nhân SaaS multi-tenant với AgentCore (SAS407)](https://www.youtube.com/watch?v=uwXrtyXXuy8)
- [Chuyển đổi từ SaaS sang SaaS dạng tác nhân multi-tenant (SAS304)](https://www.youtube.com/watch?v=YOQlbZojPB4)
- [Triển khai các tác nhân sẵn-sàng-production trong 22 phút với AgentCore Runtime](https://www.youtube.com/watch?v=Q-tYIAuv9WI)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon EKS](https://aws.amazon.com/eks/)
- [AWS CDK](https://aws.amazon.com/cdk/)
