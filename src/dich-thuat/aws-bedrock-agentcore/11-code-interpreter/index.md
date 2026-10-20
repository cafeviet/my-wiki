---
title: "AgentCore Code Interpreter: Thực thi code và phân tích dữ liệu"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter.html"
---

# AgentCore Code Interpreter: Thực thi code và phân tích dữ liệu

# Thực thi code và phân tích dữ liệu bằng Amazon Bedrock AgentCore Code Interpreter

Amazon Bedrock AgentCore Code Interpreter cho phép các agent (tác tử AI) viết và thực thi code một cách an toàn trong các môi trường sandbox, nâng cao độ chính xác và mở rộng khả năng giải quyết các tác vụ end-to-end phức tạp của chúng. Điều này rất quan trọng trong các ứng dụng AI dạng agentic, nơi agent có thể thực thi code tùy ý dẫn tới rủi ro rò rỉ dữ liệu hoặc bảo mật. Tool (công cụ) AgentCore Code Interpreter cung cấp việc thực thi code an toàn, giúp bạn tránh gặp phải các vấn đề này.

Code Interpreter đi kèm các runtime (môi trường chạy) dựng sẵn cho nhiều ngôn ngữ và các tính năng nâng cao, bao gồm hỗ trợ tập tin lớn, truy cập internet, và khả năng ghi log CloudTrail. Với upload inline, kích thước file có thể lên tới 100 MB. Còn với việc upload lên Amazon S3 thông qua các lệnh terminal, kích thước file có thể lớn tới 5 GB.

Các lập trình viên có thể tùy chỉnh môi trường bằng các session property và network mode để đáp ứng yêu cầu doanh nghiệp và bảo mật của họ. AgentCore Code Interpreter giảm can thiệp thủ công trong khi cho phép phát triển AI tinh vi mà không đánh đổi bảo mật hay hiệu năng.

###### Các chủ đề

- [Tổng quan](#code-interpreter-overview)

- [Vì sao dùng Code Interpreter trong phát triển agent](#code-interpreter-why-important)

- [Thực hành tốt nhất](#code-interpreter-best-practices)

- [Các thư viện được cài sẵn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-preinstalled-libraries.html)

- [Bắt đầu với AgentCore Code Interpreter](/dich-thuat/aws-bedrock-agentcore/11-code-interpreter/code-interpreter-getting-started)

- [Chạy code trong Code Interpreter từ các Agent](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-building-agents.html)

- [Ghi file vào một session](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-file-operations.html)

- [Dùng các lệnh Terminal với một execution role](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-s3-integration.html)

- [Quản lý tài nguyên và session](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-resource-session-management.html)

- [Cấu hình hệ thống file cho AgentCore Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-filesystem-configurations.html)

- [Ví dụ API Reference của Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-api-reference-examples.html)

- [Observability (khả năng quan sát)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-observability.html)

- [Cấu hình Root Certificate Authority cho Amazon Bedrock AgentCore Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-root-ca-certificates.html)

- [Khắc phục sự cố AgentCore Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-troubleshooting.html)

## Tổng quan

AgentCore Code Interpreter là một khả năng cho phép các agent AI viết, thực thi, và debug code an toàn trong các môi trường sandbox. Nó cung cấp cầu nối giữa hiểu biết ngôn ngữ tự nhiên và thực thi tính toán, cho phép agent thao tác dữ liệu và thực hiện các phép tính bằng lập trình.

AgentCore Code Interpreter chạy trong một môi trường containerized bên trong Amazon Bedrock AgentCore, đảm bảo việc thực thi code luôn được cô lập và an toàn.

## Vì sao dùng Code Interpreter trong phát triển agent

AgentCore Code Interpreter nâng cao việc phát triển agent theo các cách sau:

- Thực thi code an toàn: Phát triển các agent có thể thực hiện các quy trình và phân tích dữ liệu phức tạp trong các môi trường sandbox, đồng thời truy cập các nguồn dữ liệu nội bộ mà không lộ dữ liệu nhạy cảm hay đánh đổi bảo mật.

- Nhiều ngôn ngữ lập trình: Code Interpreter hỗ trợ nhiều ngôn ngữ lập trình bao gồm Python, JavaScript, và TypeScript, khiến nó linh hoạt cho các trường hợp sử dụng khác nhau.

- Giám sát và xử lý dữ liệu quy mô lớn: Theo dõi và khắc phục sự cố thực thi code. Khi làm việc với các tập dữ liệu lớn, bạn có thể dễ dàng tham chiếu các file lưu trong Amazon S3, cho phép xử lý dữ liệu quy mô gigabyte hiệu quả mà không bị giới hạn API.

- Dễ sử dụng: Dùng chế độ mặc định được quản lý hoàn toàn với các runtime thực thi dựng sẵn hỗ trợ các ngôn ngữ lập trình phổ biến với các thư viện thông dụng được cài sẵn.

- Mở rộng khả năng giải quyết vấn đề: Cho phép agent giải quyết các bài toán tính toán khó xử lý chỉ bằng suy luận, và cho phép các phép toán chính xác cùng xử lý dữ liệu ở quy mô lớn.

- Hỗ trợ thời gian thực thi dài: Tool Code Interpreter hỗ trợ thời gian thực thi mặc định 15 phút, có thể được kéo dài lên tới tám giờ.

- Xử lý dữ liệu có cấu trúc: Xử lý CSV, Excel, JSON, và các định dạng dữ liệu khác, thực hiện làm sạch và phân tích dữ liệu.

- Cho phép các quy trình phức tạp: Cho phép giải quyết vấn đề nhiều bước kết hợp suy luận với tính toán và hỗ trợ phát triển cùng debug lặp.

AgentCore Code Interpreter khiến các agent mạnh mẽ hơn bằng cách bổ sung khả năng thực thi tính toán cho khả năng suy luận của chúng, cho phép chúng xử lý hiệu quả một phạm vi tác vụ rộng lớn hơn nhiều.

## Thực hành tốt nhất

Để tận dụng tối đa AgentCore Code Interpreter:

- Giữ các đoạn code ngắn gọn và tập trung vào các tác vụ cụ thể

- Dùng comment để tài liệu hóa code của bạn

- Tối ưu code cho hiệu năng khi làm việc với các tập dữ liệu lớn

- Lưu các kết quả trung gian khi thực hiện các thao tác phức tạp

- Dùng context manager `code_session` để đảm bảo dọn dẹp đúng cách

- Bao gồm các khối try/except trong code để xử lý lỗi một cách mượt mà

- Kết quả thực thi code được trả về và xử lý dưới dạng stream

- Dọn dẹp các file tạm khi không còn cần

- Đóng các session khi bạn hoàn tất để giải phóng tài nguyên
