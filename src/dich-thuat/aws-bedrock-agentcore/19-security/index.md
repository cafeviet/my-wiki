---
title: "Bảo mật"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security.html"
---

# Bảo mật

# Bảo mật trong Amazon Bedrock AgentCore

Bảo mật đám mây tại AWS là ưu tiên cao nhất. Là một khách hàng của AWS, bạn được hưởng lợi từ các trung tâm dữ liệu và kiến trúc mạng được thiết kế để đáp ứng yêu cầu của những tổ chức nhạy cảm nhất về bảo mật.

Bảo mật là trách nhiệm chung giữa AWS và bạn. [Mô hình trách nhiệm chung (shared responsibility model)](https://aws.amazon.com/compliance/shared-responsibility-model/) mô tả điều này là bảo mật *của* đám mây và bảo mật *trong* đám mây:

- **Bảo mật của đám mây** – AWS chịu trách nhiệm bảo vệ hạ tầng chạy các dịch vụ AWS trong AWS Cloud. AWS cũng cung cấp cho bạn các dịch vụ mà bạn có thể sử dụng một cách an toàn. Các bên kiểm toán thứ ba thường xuyên kiểm tra và xác minh hiệu quả bảo mật của chúng tôi như một phần của [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/). Để tìm hiểu về các chương trình tuân thủ áp dụng cho Amazon Bedrock AgentCore, xem [AWS Services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/).

- **Bảo mật trong đám mây** – Trách nhiệm của bạn được xác định bởi dịch vụ AWS mà bạn sử dụng. Bạn cũng chịu trách nhiệm cho các yếu tố khác bao gồm mức độ nhạy cảm của dữ liệu, yêu cầu của công ty bạn, và các luật lệ và quy định áp dụng.

Tài liệu này giúp bạn hiểu cách áp dụng mô hình trách nhiệm chung khi dùng AgentCore. Các chủ đề sau cho bạn thấy cách cấu hình AgentCore để giúp đáp ứng các mục tiêu bảo mật và tuân thủ của bạn. Bạn cũng học cách dùng các dịch vụ AWS khác giúp bạn giám sát và bảo vệ các tài nguyên AgentCore của mình.

###### Các chủ đề

- [Bảo vệ dữ liệu trong Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/data-protection.html)

- [Quản lý danh tính và truy cập (Identity and access management) cho Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html)

- [Runtime Instances và capacity providers](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-instances.html)

- [Chính sách dựa trên tài nguyên (Resource-based policies) cho Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/resource-based-policies.html)

- [Xác nhận tuân thủ (Compliance validation) cho Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/compliance-validation.html)

- [Khả năng chống chịu (Resilience) trong Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/disaster-recovery-resiliency.html)

- [Ngăn ngừa confused deputy giữa các dịch vụ (Cross-service confused deputy prevention)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/cross-service-confused-deputy-prevention.html)
