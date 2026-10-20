# AGENTSEC05-BP02 Triển khai truy vết phân tán cho các tương tác của agent

Một yêu cầu nhảy qua các agent, hàng đợi và bus sự kiện chỉ có thể điều tra được nếu một định danh duy nhất theo nó đầu-cuối. Truy vết với cả một trace ID cho các dịch vụ được trang bị (instrumented) lẫn một correlation ID ở cấp ứng dụng cho các ranh giới bất đồng bộ làm cho các sự cố xuyên agent có thể tái dựng.

**Kết quả mong muốn:**

- Bạn truy vết đầu-cuối mọi yêu cầu chảy qua một hệ thống đa agent với một định danh tương quan duy nhất, để các đội bảo mật có thể tái dựng chuỗi tương tác agent đầy đủ cho các thao tác được truy vết.
- Các bản đồ dịch vụ (service maps) cho khả năng nhìn thấy thời gian thực về các phụ thuộc của agent và các mẫu giao tiếp.

**Các phản mẫu thường gặp (anti-patterns):**

- Sinh các trace ID mới tại mỗi ranh giới agent thay vì lan truyền cái gốc, làm gãy chuỗi tương quan và khiến không thể liên kết các hành động liên quan.
- Chỉ truy vết các tương tác agent đồng bộ và bỏ sót các thao tác bất đồng bộ (thông điệp Amazon SQS, sự kiện Amazon EventBridge), tạo ra các khoảng trống che khuất đường thực thi đầy đủ.
- Không trang bị các lần gọi công cụ trong các trace của agent, mất khả năng nhìn thấy dịch vụ bên ngoài nào đã được gọi và dữ liệu nào đã được trao đổi trong quá trình thực thi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các trace được tương quan qua các ranh giới agent làm cho mọi lần thực thi của agent có thể tái dựng về sau.
- Các bản đồ dịch vụ và phân tích trace làm nổi bật các mẫu giao tiếp bất ngờ, chẳng hạn như các agent tương tác với các dịch vụ ngoài đồ thị phụ thuộc bình thường của chúng.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Hai định danh cùng làm việc. Một *trace ID* được sinh bởi hệ thống truy vết (Amazon CloudWatch Application Signals, AWS X-Ray, OpenTelemetry) và theo một yêu cầu qua các dịch vụ được trang bị. Đó là định danh mà backend truy vết dùng để tái dựng các span thành một cây trace. Một *correlation ID* được sinh bởi ứng dụng và được lan truyền đầu-cuối, và nó sống sót qua các ranh giới nơi ngữ cảnh trace được tái sinh (phổ biến nhất là các kênh nhắn tin bất đồng bộ, nơi bên tiêu thụ thường bắt đầu một trace mới). Các trace ID cho bạn sự tương quan tự động nơi việc trang bị là liên tục. Các correlation ID cho bạn liên kết đáng tin cậy qua các ranh giới mà việc trang bị không thể vượt qua.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html) cung cấp truy vết dựng sẵn cho các agent được triển khai trên AgentCore Runtime. Các phiên đại diện cho các tương tác người dùng hoàn chỉnh, các trace đại diện cho các chu kỳ yêu cầu-phản hồi riêng lẻ, và các span đại diện cho các thao tác cụ thể trong một trace. AgentCore xuất dữ liệu span cho các tài nguyên bộ nhớ theo mặc định, và các chỉ số ở cấp phiên có thể xem trên trang generative AI observability của Amazon CloudWatch. Việc trang bị dựng sẵn ghi lại vòng lặp thực thi của agent và lan truyền ngữ cảnh trace qua các ranh giới agent mà không cần mã tùy chỉnh.

Để có khả năng nhìn thấy sâu hơn hoặc cho các agent không chạy trên AgentCore Runtime, hãy trang bị cho mã của agent AWS Distro for OpenTelemetry (ADOT) để sinh các trace tương thích với AWS X-Ray và các nền tảng khả năng quan sát bên thứ ba. Hãy tạo các span cho mỗi thao tác đáng kể trong một agent (các lần gọi mô hình, các lời gọi công cụ, đọc và ghi bộ nhớ, các giao tiếp giữa các agent) và cấu hình các quy tắc lấy mẫu (sampling) X-Ray để thu 100% các trace cho các thao tác có tính bảo mật quan trọng trong khi dùng lấy mẫu thống kê cho các thao tác thường lệ khối lượng lớn.

Lan truyền correlation ID là mối quan tâm chính trong mọi giao tiếp agent-tới-agent. Hãy bao gồm cả correlation ID lẫn trace ID hiện tại trong các thông điệp giữa các agent, các lời gọi API và các payload sự kiện, để chuỗi thực thi đầy đủ có thể được tái dựng từ bất kỳ điểm nào. Với các thao tác bất đồng bộ qua Amazon SQS hoặc Amazon EventBridge, hãy lan truyền cả hai ID qua các thuộc tính thông điệp. Correlation ID bảo tồn liên kết đầu-cuối ngay cả khi hệ thống truy vết bắt đầu một trace mới ở phía tiêu thụ.

Trang generative AI observability của Amazon CloudWatch cung cấp các chỉ số phiên và trace riêng cho agent đối với AgentCore Runtime. Để trực quan hóa xuyên dịch vụ bao phủ các thành phần không phải agent trong cùng đường yêu cầu (cơ sở dữ liệu, hàng đợi, các dịch vụ phía sau), Amazon CloudWatch ServiceLens dựng một bản đồ dịch vụ về các tương tác agent và làm nổi bật các mẫu giao tiếp bất ngờ. Các truy vấn Amazon CloudWatch Logs Insights nhận diện các trace có mẫu bất thường: các agent gọi các dịch vụ bất ngờ, các trace có số lượng gọi công cụ cao bất thường, hoặc các trace trải qua các region địa lý bất ngờ.

### Các bước triển khai

- **Kiểm chứng truy vết dựng sẵn của AgentCore:** Với các agent trên AgentCore Runtime, xác nhận [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html) đang thu dữ liệu phiên, trace và span và xem xét các chỉ số mặc định trên trang generative AI observability của Amazon CloudWatch.
- **Trang bị các agent tùy chỉnh bằng ADOT:** Với các agent tùy chỉnh hoặc để có khả năng nhìn thấy sâu hơn, hãy trang bị cho mã của agent AWS Distro for OpenTelemetry để sinh các span cho các lần gọi mô hình, các lời gọi công cụ, các thao tác bộ nhớ và các giao tiếp giữa các agent.
- **Lan truyền correlation ID qua các ranh giới async:** Bao gồm correlation ID và trace ID hiện tại trong mọi thông điệp giữa các agent, lời gọi API và payload sự kiện, và lan truyền chúng qua các thuộc tính thông điệp Amazon SQS và detail sự kiện Amazon EventBridge cho các thao tác bất đồng bộ.
- **Cấu hình lấy mẫu X-Ray theo rủi ro:** Thu 100% các trace cho các thao tác có tính bảo mật quan trọng và lấy mẫu thống kê cho các thao tác thường lệ qua các quy tắc lấy mẫu AWS X-Ray.
- **Trực quan hóa các bản đồ dịch vụ và phát hiện bất thường:** Dùng Amazon CloudWatch ServiceLens để trực quan hóa các bản đồ dịch vụ agent và xây dựng các truy vấn Amazon CloudWatch Logs Insights để phát hiện các mẫu trace bất thường.
- **Đặt việc lưu giữ trace:** Cấu hình các chính sách lưu giữ trace khớp với các yêu cầu điều tra sự cố và tuân thủ của bạn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](agentsec05-bp01.md)
- [AGENTSEC06-BP04 Giám sát và phát hiện các bất thường trong phối hợp](../6-agentsec06/agentsec06-bp04.md)
- [AGENTREL07-BP03 Triển khai truy vết phân tán để theo dõi các phụ thuộc hệ thống và hỗ trợ phục hồi](../../3-reliability/7-agentrel07/agentrel07-bp03.md)
- [AGENTPERF01-BP03 Lập hồ sơ độ trễ agent đầu-cuối và nhận diện các mục tiêu tối ưu](../../4-performance-efficiency/1-agentperf01/agentperf01-bp03.md)

**Tài liệu liên quan:**

- [AgentCore Observability: Sessions, traces, and spans](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html)
- [Build trustworthy AI agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Tài liệu AWS X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
- [AWS Distro for OpenTelemetry](https://aws-otel.github.io/)
- [Amazon CloudWatch ServiceLens](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ServiceLens.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS X-Ray](https://aws.amazon.com/xray/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
