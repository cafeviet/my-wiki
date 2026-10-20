# Tối ưu chi phí khám phá và triển khai agent

Các nhóm tối ưu hạ tầng vòng đời agent thông qua khám phá (discovery) nhẹ, đánh phiên bản hiệu quả, và khởi tạo ấm giúp giữ chi phí vận hành không tăng nhanh hơn chính đội agent. Chi phí hạ tầng agent có thể leo thang thông qua các cơ chế khám phá kém hiệu quả, sự sinh sôi phiên bản, và các hình phạt cold start.

| AGENTCOST06: Làm thế nào để tối ưu chi phí khám phá, registry và triển khai agent? |
| --- |
|  |

## Mục tiêu năng lực

- Khám phá agent chạy trên hạ tầng dựa trên mức tiêu thụ, nên chi phí registry theo dõi hoạt động truy vấn và ghi thực tế thay vì một chi phí cố định cho đội.
- Caching metadata phục vụ hầu hết các tra cứu năng lực mà không đọc lại registry, giữ chi phí đọc tỷ lệ với tốc độ thay đổi registry chứ không theo tốc độ gọi.
- Đánh phiên bản agent lưu các phụ thuộc dùng chung một lần và tự động loại bỏ các phiên bản không dùng, nên chi phí lưu trữ được kiềm chế khi đội agent tiến hóa.
- Các triển khai dùng định tuyến lưu lượng có trọng số trên hạ tầng dùng chung, nên các rollout blue/green và canary không phải trả gấp đôi cho các môi trường song song.
- Các agent được gọi thường xuyên tái sử dụng các phiên ấm với các tạo tác khởi tạo đã cache, và các agent ít gọi scale về không để tránh phí công suất rảnh.
- Tỷ lệ cold start, tỷ lệ trúng cache, và lưu trữ theo từng phiên bản được đo lường và xem xét, cho các chủ sở hữu tín hiệu để xử lý các động lực chi phí trước khi chúng scale cùng đội.

## Các mức trưởng thành

Các mức này tóm tắt hình dạng của mỗi giai đoạn trưởng thành đối với việc tối ưu chi phí khám phá và triển khai agent nói chung.

| Mức | Tên | Hình dạng thể hiện |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Khám phá, đánh phiên bản và khởi tạo agent được xử lý một lần. Các nhóm triển khai service mesh nặng hoặc các registry tùy chỉnh mà không đánh giá các lựa chọn thay thế dựa trên mức tiêu thụ. Các phiên bản container tích lũy trong [Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) mà không có chính sách vòng đời, và các cold start bị hấp thụ ở mọi lần gọi vì các session lifetime, caching, và session affinity không được cấu hình. Khả năng nhìn thấy chi phí giới hạn ở việc tính hóa đơn cấp tài khoản, nên các mẫu đắt tiền tăng âm thầm khi đội mở rộng. |
| 2 | Nhen nhóm (Emerging) | Khám phá được quản lý như [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) được áp dụng cho cộng tác agent dựa trên công cụ. Các registry tùy chỉnh, ở nơi cần, dùng lưu trữ dựa trên mức tiêu thụ như [Amazon DynamoDB on-demand capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.OnDemand). Các chính sách lưu giữ phiên bản được định nghĩa nhưng thực thi thủ công. Các mẫu phiên ấm được áp dụng cho một số nhỏ các agent tần suất cao, và tỷ lệ cold start được theo dõi cho các agent đó. |
| 3 | Xác định (Defined) | Gateway hoặc một registry dựa trên mức tiêu thụ là tiêu chuẩn, và caching metadata với các TTL có thể cấu hình được dùng xuyên đội. [Các chính sách vòng đời Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html) xóa các image không dùng tự động, và các lớp container cơ sở được chia sẻ để ECR khử trùng lặp chúng xuyên các phiên bản agent. Định tuyến endpoint có trọng số được dùng cho các triển khai blue/green và canary trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html). Caching hệ thống tệp bền vững khấu hao khởi tạo xuyên các phiên, và chi phí cold start và khởi tạo được đo lường theo từng loại agent qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). |
| 4 | Chủ động (Proactive) | Các số liệu chi phí khám phá, đánh phiên bản và khởi tạo được đưa lên dashboard trong [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) và xem xét theo một nhịp thường quy. Việc thăng cấp canary được tự động hóa dùng chi phí-trên-mỗi-lần-hoàn-thành-tác-vụ cùng với tỷ lệ lỗi và độ trễ, được điều khiển từ logic thăng cấp [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html). Định tuyến session affinity được triển khai trong tầng điều phối, và [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) được cấu hình cho nạp lười (lazy loading) để các agent chỉ lấy ngữ cảnh khởi động thiết yếu. Các bất thường chi phí về khám phá, triển khai, hoặc khởi tạo kích hoạt cảnh báo tự động. |
| 5 | Tối ưu (Optimized) | Các mẫu khám phá, triển khai và khởi tạo được tinh chỉnh liên tục dựa trên dữ liệu vận hành. Việc phát hành phiên bản agent hoàn toàn tự phục vụ với các guardrail nhận biết chi phí, và tỷ lệ cold start ở dưới 10% xuyên đội. Các chính sách lưu giữ, thăng cấp và warm pool tự chữa lành và được điều khiển bởi việc sử dụng quan sát được. Tổ chức xuất bản các mẫu agent và container có thể tái sử dụng nội bộ, và chia sẻ các benchmark về hiệu quả chi phí khám phá, đánh phiên bản và khởi tạo xuyên các nhóm. |

## Các vấn đề thường gặp cần chú ý

- Các tổ chức triển khai hạ tầng service mesh nặng cho các tra cứu năng lực đơn giản, trả các chi phí hàng tháng cố định cho các tính năng mà đội agent không dùng.
- Các nhóm đặt registry trên đường dẫn quan trọng của mọi lần gọi, đọc lại metadata năng lực lặp đi lặp lại thay vì cache nó, nên chi phí đọc tăng tuyến tính theo khối lượng gọi.
- Việc lưu giữ phiên bản agent chạy mà không có chính sách vòng đời, nên mỗi thay đổi cấu hình tích lũy các image trong container registry và chi phí lưu trữ tăng vô hạn.
- Các triển khai blue/green và canary chạy các đội song song đầy đủ thay vì định tuyến một tỷ lệ phần trăm lưu lượng nhỏ, làm gấp đôi chi phí tính toán trong mỗi rollout.
- Các agent được gọi thường xuyên trả chi phí cold start ở mọi lần gọi vì các session lifetime, caching hệ thống tệp bền vững, và session affinity không được cấu hình.
- Chi phí khám phá, đánh phiên bản và khởi tạo không được đo lường, nên các mẫu đắt tiền như các truy vấn nặng-quét, các phiên bản không dùng, và các cold start lặp lại tăng âm thầm khi đội mở rộng.

###### Các thực hành tốt

- [AGENTCOST06-BP01 Triển khai khám phá và registry nhẹ cho cộng tác tiết kiệm chi phí](agentcost06-bp01.md)
- [AGENTCOST06-BP02 Tối ưu chi phí đánh phiên bản và triển khai thông qua quản lý tạo tác hiệu quả](agentcost06-bp02.md)
- [AGENTCOST06-BP03 Thiết kế khởi tạo tiết kiệm chi phí thông qua warm pool và caching](agentcost06-bp03.md)
