---
title: "AgentCore Observability: Quan sát các agent và tài nguyên của bạn"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/index.html"
---

# AgentCore Observability: Quan sát các agent và tài nguyên của bạn

# Quan sát các ứng dụng agent của bạn trên Amazon Bedrock AgentCore Observability

Với AgentCore, bạn có thể trace, gỡ lỗi và giám sát hiệu năng của các agent (tác tử AI) trong môi trường production.

AgentCore Observability (khả năng quan sát) giúp bạn trace, gỡ lỗi và giám sát hiệu năng agent trong môi trường production. Nó cung cấp các trực quan hóa chi tiết cho từng bước trong quy trình làm việc của agent, cho phép bạn kiểm tra đường thực thi của agent, kiểm toán các output trung gian, và gỡ lỗi các điểm nghẽn hiệu năng cũng như lỗi.

AgentCore Observability cho bạn khả năng hiển thị thời gian thực về hiệu năng vận hành của agent thông qua quyền truy cập các dashboard được cung cấp sức mạnh bởi Amazon CloudWatch và telemetry cho các số liệu chính như số lượng session, độ trễ, thời lượng, mức dùng token và tỷ lệ lỗi. Việc gắn thẻ và lọc metadata phong phú giúp đơn giản hóa việc điều tra sự cố và duy trì chất lượng ở quy mô lớn. AgentCore phát ra dữ liệu telemetry theo định dạng chuẩn tương thích OpenTelemetry (OTEL), cho phép bạn dễ dàng tích hợp nó với ngăn xếp giám sát và observability hiện có của bạn.

Theo mặc định, AgentCore xuất ra một tập các số liệu tích hợp sẵn chính cho các agent, tài nguyên gateway (cổng) và tài nguyên memory (bộ nhớ). Với các tài nguyên memory, AgentCore còn xuất ra span và dữ liệu log nếu bạn bật tính năng đó. Bạn cũng có thể instrument code agent của mình để cung cấp thêm dữ liệu span và trace cùng các số liệu và log tùy chỉnh. Xem [Thêm observability vào các tài nguyên Amazon Bedrock AgentCore của bạn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html) để tìm hiểu thêm.

Tất cả các số liệu, span và log do AgentCore xuất ra đều được lưu trong Amazon CloudWatch, và có thể được xem trong console CloudWatch hoặc tải xuống từ CloudWatch bằng AWS CLI hoặc một trong các AWS SDK.

Ngoài dữ liệu thô lưu trong CloudWatch Logs, riêng đối với dữ liệu agent runtime (môi trường chạy), console CloudWatch cung cấp một dashboard observability chứa các trực quan hóa trace, đồ thị cho các số liệu span tùy chỉnh, phân tách lỗi và nhiều hơn nữa. Để tìm hiểu thêm về việc xem dữ liệu observability của các agent, xem [Xem dữ liệu observability cho các agent Amazon Bedrock AgentCore của bạn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html)

- [Bắt đầu với AgentCore Observability](/dich-thuat/aws-bedrock-agentcore/13-observability/observability-get-started)

- [Thêm observability vào các tài nguyên Amazon Bedrock AgentCore của bạn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html)

- [Tìm hiểu observability cho các tài nguyên agentic trong AgentCore](/dich-thuat/aws-bedrock-agentcore/13-observability/observability-telemetry)

- [Dữ liệu observability do Amazon Bedrock AgentCore tạo ra](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-service-provided.html)

- [Xem dữ liệu observability cho các agent Amazon Bedrock AgentCore của bạn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html)

- [Giám sát các tài nguyên AgentCore trên nhiều tài khoản](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-cross-account.html)
