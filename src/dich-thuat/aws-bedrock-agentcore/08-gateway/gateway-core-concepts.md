---
title: "Các khái niệm cốt lõi của Amazon Bedrock AgentCore Gateway"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html"
---

# Các khái niệm cốt lõi của Amazon Bedrock AgentCore Gateway

Amazon Bedrock AgentCore Gateway (cổng) cung cấp một điểm vào chuẩn hóa và bảo mật cho luồng lưu lượng của các tác tử, cho phép các AI agent (tác tử AI) khám phá và tương tác với tool (công cụ), với các agent khác, và với các mô hình ngôn ngữ lớn (LLM). Hiểu rõ các khái niệm cốt lõi của Gateway sẽ giúp bạn thiết kế và triển khai các chiến lược tích hợp hiệu quả cho AI agent của mình.

## Các khái niệm chính

Một AgentCore Gateway cung cấp một điểm truy cập duy nhất, bảo mật để một agent tiếp cận tool, các agent khác và các mô hình. Một gateway có thể có nhiều target thuộc ba nhóm — MCP, HTTP và inference. Đối với target loại MCP, gateway hoạt động ở chế độ tổng hợp (aggregation mode), đóng vai trò như một MCP server kết hợp năng lực của tất cả các MCP target thành một MCP server ảo, hợp nhất. Đối với target loại HTTP, gateway gửi lưu lượng trực tiếp tới target (ví dụ, một agent khác hoặc một dịch vụ A2A) mà không tổng hợp hay dịch giao thức. Đối với target loại inference, gateway định tuyến các yêu cầu LLM tới một hoặc nhiều nhà cung cấp mô hình thông qua một endpoint định tuyến hợp nhất dựa trên mô hình.

Một target định nghĩa backend mà gateway kết nối tới. Có ba nhóm target. MCP target định nghĩa các API, hàm Lambda, MCP server, hoặc định nghĩa tool mà gateway tổng hợp lại thành một MCP server hợp nhất. HTTP target định nghĩa các dịch vụ dựa trên HTTP, chẳng hạn như các AgentCore Runtime (môi trường chạy) agent và các agent khác, mà gateway ủy nhiệm (proxy) yêu cầu tới một cách trực tiếp. Inference target định tuyến lưu lượng LLM tới một hoặc nhiều nhà cung cấp mô hình thông qua một endpoint hợp nhất, chọn đích đến dựa trên mô hình được yêu cầu.

Mỗi gateway phải có một cấu hình ủy quyền vào (inbound authorization) để kiểm soát quyền truy cập của client. Gateway hỗ trợ các loại ủy quyền vào sau: OAuth (JWT) cho ủy quyền dựa trên token, IAM (AWS Signature Version 4) cho ủy quyền dựa trên danh tính AWS, "authenticate only" để xác thực token trong khi ủy nhiệm việc ủy quyền cho target, và "no authorization" cho các kịch bản phát triển và kiểm thử. Bạn có thể cấu hình authorizer khi tạo hoặc cập nhật một gateway.

Khi Gateway gọi tới các API hoặc hàm Lambda của bạn, nó phải sử dụng một loại thông tin xác thực (credentials) nào đó để truy cập các chức năng đó. Khi bạn tạo một Smithy target hoặc Lambda target, Gateway sử dụng execution role được gắn kèm để gọi tới các target đó. Khi bạn tạo một OpenAPI target hoặc MCP server target, bạn có thể gắn kèm một AgentCore credential provider lưu trữ API Key hoặc thông tin xác thực OAuth, cấu hình ủy quyền dựa trên IAM với chữ ký SigV4, hoặc dùng "no authorization" cho các endpoint có thể truy cập công khai.

## Các loại target

Gateway hỗ trợ ba nhóm target:

MCP target hoạt động ở chế độ tổng hợp. Gateway kết hợp năng lực của tất cả MCP target thành một MCP server ảo, hợp nhất duy nhất. Các client nhìn thấy một phản hồi `tools/list` hợp nhất bao gồm các tool từ tất cả MCP target được gắn kèm. MCP target hỗ trợ đồng bộ hóa năng lực, tìm kiếm tool theo ngữ nghĩa, và three-legged OAuth (3LO) ở cấp target. Các loại MCP target bao gồm hàm Lambda, API Gateway REST API, đặc tả OpenAPI, mô hình Smithy, MCP server, các mẫu (template) nhà cung cấp tích hợp có sẵn, và các connector có sẵn tới tool.

HTTP target gửi lưu lượng trực tiếp tới target mà không tổng hợp hay dịch giao thức. HTTP target không hỗ trợ đồng bộ hóa năng lực hay tìm kiếm tool theo ngữ nghĩa. Các client địa chỉ hóa từng target riêng lẻ thông qua định tuyến dựa trên path. Các loại HTTP target bao gồm Amazon Bedrock AgentCore Runtime agent, các agent khác (bao gồm dịch vụ Agent-to-Agent (A2A)), các MCP server bên ngoài, và bất kỳ HTTP endpoint nào tiếp cận được thông qua một passthrough target.

Inference target định tuyến lưu lượng mô hình ngôn ngữ lớn (LLM) tới một hoặc nhiều nhà cung cấp mô hình thông qua một endpoint hợp nhất. Gateway chọn nhà cung cấp đích dựa trên trường `model` trong yêu cầu, mang lại cho các agent một giao diện duy nhất, nhất quán qua các nhà cung cấp như Amazon Bedrock, OpenAI và Anthropic.

## Các loại MCP tool

Gateway hỗ trợ một số loại MCP tool và phương thức tích hợp:

Chuyển đổi các REST API hiện có thành các tool tương thích MCP bằng cách cung cấp một đặc tả OpenAPI. Gateway tự động xử lý việc chuyển đổi giữa định dạng MCP và REST.

Kết nối các hàm Lambda như những tool, cho phép bạn triển khai logic nghiệp vụ tùy chỉnh bằng ngôn ngữ lập trình bạn ưa thích. Gateway gọi hàm Lambda và chuyển đổi phản hồi sang định dạng MCP.

Sử dụng mô hình Smithy để định nghĩa các giao diện API của bạn và tạo ra các tool tương thích MCP. Smithy là một ngôn ngữ để định nghĩa dịch vụ và SDK có thể dùng với các dịch vụ AWS. Gateway có thể dùng mô hình Smithy để tạo ra các tool tương tác với dịch vụ AWS hoặc API tùy chỉnh.

Sử dụng các MCP server từ xa để kết nối tool, prompt và tài nguyên (resource) với agent runtime của bạn. Gateway hỗ trợ các năng lực tool, prompt và resource của MCP. Tool là bắt buộc; prompt và resource là tùy chọn. Prompt cung cấp các mẫu prompt có thể tái sử dụng kèm đối số. Resource cung cấp dữ liệu ngữ cảnh được định danh bằng URI. Trong quá trình đồng bộ hóa, gateway khám phá tất cả các năng lực mà MCP server công bố.

Sử dụng các mẫu có sẵn từ các nhà cung cấp tích hợp.

Sử dụng các connector có sẵn tới tool.
