# AGENTCOST05-BP03 Thiết kế phân bổ chi phí nhận biết tenant cho các mô hình định giá agent as a service (AaaS)

Các sản phẩm agent as a service (AaaS) thiếu quy gán chi phí theo từng tenant chỉ có thể tính hóa đơn theo các ước lượng công suất, không thể phát hiện các hàng xóm ồn ào (noisy neighbor) cho đến khi hạ tầng đã scale lên, và không thể quyết định khi nào một tenant nên chuyển sang hạ tầng chuyên dụng. Lan truyền ngữ cảnh tenant qua mọi thao tác và theo dõi chi phí ở cấp tenant khắc phục cả ba vấn đề cùng lúc.

**Kết quả mong muốn:**

- Bạn lan truyền các định danh tenant qua tất cả các thao tác của agent: các lần gọi model, các lần thực thi công cụ, các thao tác bộ nhớ, và lưu trữ dữ liệu.
- Bạn có các mô hình phân bổ chi phí linh hoạt hỗ trợ định giá theo từng quyết định, theo từng tác vụ, và theo từng agent-giờ.
- Bạn phát hiện các hàng xóm ồn ào trước khi chúng đẩy việc scale hạ tầng ảnh hưởng tới mọi khách hàng.
- Bạn thực thi các kiểm soát ngân sách cấp tenant giới hạn chi tiêu theo từng tenant.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ theo dõi chi phí agent ở cấp tài khoản mà không có ngữ cảnh tenant, khiến không thể tạo các hóa đơn tenant chính xác.
- Cho phép các tenant sử dụng nhiều tiêu thụ các tài nguyên dùng chung mà không bị phát hiện, đẩy các chi phí scale hạ tầng ảnh hưởng tới mọi khách hàng.
- Chỉ triển khai một cách tiếp cận tính hóa đơn vì hệ thống phân bổ chi phí không thể hỗ trợ nhiều chiều định giá.
- Cho phép chi phí agent không giới hạn mà không có các giới hạn sử dụng cấp tenant, tạo rủi ro tài chính khi các cú tăng đột biến sử dụng bất ngờ xảy ra.
- Xây dựng các sản phẩm agent as a service với một mô hình định giá cố định duy nhất, làm giảm khả năng tối ưu doanh thu dựa trên các mẫu sử dụng thực tế.

**Lợi ích khi áp dụng thực hành tốt này:**

- Theo dõi chi phí theo từng tenant cho phép tính hóa đơn dựa trên mức tiêu thụ tài nguyên thực tế thay vì các ước lượng dựa trên công suất.
- Phát hiện hàng xóm ồn ào và throttle cấp tenant giúp ngăn việc scale hạ tầng bất ngờ từ các mẫu sử dụng tích cực.
- Dữ liệu phân bổ chi phí cho phép các quyết định dựa trên dữ liệu về khi nào hạ tầng chuyên dụng trở nên tiết kiệm chi phí hơn các tài nguyên dùng chung (pooled).

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Ngữ cảnh tenant phải đi kèm với mọi sự kiện có thể tính phí. [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) gắn thẻ các danh tính workload, các nhà cung cấp thông tin xác thực (credential provider), và các nhà cung cấp API key với metadata tenant lan truyền qua các thao tác về sau. Các thẻ đó tích hợp với AWS Cost Explorer để phân rã chi phí theo từng tenant mà không cần các tài khoản AWS riêng cho từng tenant. Với các agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), kiến trúc dựa-trên-phiên cung cấp các ranh giới tenant tự nhiên, và giá theo mức tiêu thụ nghĩa là hóa đơn của mỗi phiên phản ánh công việc thực tế được làm cho tenant đó.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) nắm bắt tất cả các sự kiện có thể tính phí với các định danh tenant trong các chiều số liệu: tiêu thụ token, chi phí gọi công cụ từ [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), và chi phí thao tác bộ nhớ từ [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html). Thực thi quota cấp tenant sống trong [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html) với các chính sách Cedar, đó là cách bạn giới hạn chi tiêu theo từng tenant mà không đẩy việc thực thi vào mã ứng dụng nơi nó có thể bị lách qua.

Một *noisy neighbor* là một máy ảo hoặc container tiêu thụ tài nguyên hệ thống không tương xứng. Phát hiện hàng xóm ồn ào cần một đường cơ sở và một ngưỡng lệch phản ánh cách độ sâu suy luận của agent thực sự biến thiên. Một số tenant thực thi các quyết định đơn bước đơn giản, trong khi các tenant khác kích hoạt các chuỗi suy luận nhiều lượt phức tạp. Một cảnh báo Amazon CloudWatch khi tiêu thụ của một tenant vượt quá ba lần đường cơ sở lịch sử của họ bắt được việc sử dụng bất thường đủ sớm để giúp ngăn việc scale hạ tầng làm tăng chi phí cho mọi khách hàng. Ngưỡng được tinh chỉnh theo từng workload để tránh kích hoạt thiếu hoặc thừa.

Các quyết định chia sẻ tài nguyên cần một mô hình chi phí. Hạ tầng dùng chung đạt mức tận dụng cao hơn và chi phí theo từng tenant thấp hơn nhưng đòi hỏi cách ly mạnh. Hạ tầng chuyên dụng cung cấp cách ly mạnh hơn và hiệu năng dự đoán được với chi phí cố định cao hơn. Xây dựng một mô hình điểm hòa vốn theo từng tenant tính khi nào việc sử dụng của một tenant sẽ rẻ hơn trên hạ tầng chuyên dụng so với phần chia tỷ lệ của họ trong các tài nguyên dùng chung, và dùng nó để cung cấp các triển khai chuyên dụng cho các tenant đã vượt qua ranh giới đó.

### Các bước triển khai

- **Gắn thẻ các danh tính cho quy gán tenant:** Cấu hình [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) với các thẻ đặc thù theo tenant trên các danh tính workload, và kích hoạt thẻ phân bổ chi phí tenant-id trong bảng điều khiển tính hóa đơn AWS.
- **Triển khai các agent với các thẻ tenant ở cấp phiên:** Chạy các agent trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) với gắn thẻ tenant ở cấp phiên để quy gán chi phí theo phiên, chứ không theo pool.
- **Nắm bắt tất cả các chiều chi phí theo từng tenant:** Cấu hình [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để xuất dữ liệu đo lường sang Amazon CloudWatch với các định danh tenant trong các chiều số liệu.
- **Thực thi quota tenant và phát hiện hàng xóm ồn ào:** Triển khai thực thi quota cấp tenant qua [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), và đặt các cảnh báo CloudWatch cho các cú tăng đột biến tiêu thụ vượt quá ba lần đường cơ sở lịch sử của tenant.
- **Xây dựng một cỗ máy định giá linh hoạt:** Hỗ trợ các mô hình tính hóa đơn theo từng quyết định, theo từng tác vụ, và theo từng agent-giờ với các cấu hình đặc thù theo tenant để định giá có thể tiến hóa mà không cần tái kiến trúc pipeline tính hóa đơn.
- **Mô hình hóa điểm hòa vốn pooled so với dedicated:** Dùng dữ liệu API của AWS Cost Explorer để tính điểm hòa vốn theo từng tenant, xác định các tenant tiến gần ranh giới nơi các triển khai AgentCore chuyên dụng trở nên tiết kiệm chi phí.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST05-BP01 Thiết lập theo dõi và quy gán chi phí suy luận ở cấp agent](agentcost05-bp01.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng đa agent](agentcost05-bp02.md)
- [AGENTCOST05-BP04 Tạo báo cáo chargeback và ROI](agentcost05-bp04.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Manage multi-tenant Amazon Bedrock costs using application inference profiles](https://aws.amazon.com/blogs/machine-learning/manage-multi-tenant-amazon-bedrock-costs-using-application-inference-profiles/)
- [AWS SaaS Lens](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html)
- [Using cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Building multi-tenant SaaS agents with AgentCore (SAS407)](https://www.youtube.com/watch?v=uwXrtyXXuy8)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Observability tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
