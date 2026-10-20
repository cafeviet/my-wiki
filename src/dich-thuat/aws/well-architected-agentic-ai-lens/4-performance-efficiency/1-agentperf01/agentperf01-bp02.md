# AGENTPERF01-BP02 Triển khai telemetry hiệu năng toàn diện

Một yêu cầu tác nhân duy nhất tỏa ra thành các chuỗi lệnh gọi suy luận (inference), lệnh gọi **Tools** song song, tra cứu bộ nhớ, và giao tiếp liên tác nhân. Giám sát chỉ-dựa-vào-hạ-tầng tự nó không thể xác định cái nào trong số đó góp phần vào một phản hồi chậm hoặc tốn kém. **Telemetry** nhận-biết-tác-nhân phân rã việc thực thi thành các thao tác có thể quan sát và quy trách nhiệm được, để các quyết định hiệu năng dựa trên hành vi đo được.

**Kết quả mong muốn:**

- Bạn có một trace phân tán hoàn chỉnh cho mọi lần thực thi tác nhân, phân rã tổng latency thành các thao tác cấu thành.
- Bạn có các bảng điều khiển thời gian thực cung cấp khả năng thấy xu hướng hiệu năng tác nhân, với các chỉ số kết quả nạp vào lớp cảnh báo.
- Bạn có dữ liệu telemetry lịch sử hỗ trợ lập kế hoạch dung lượng, các quyết định lựa chọn **Model**, và tối ưu kiến trúc thông qua phân tích dựa-trên-dữ-liệu.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ dựa vào các chỉ số cấp-hạ-tầng như thời lượng hàm hay latency của API gateway mà không đo lường pipeline suy luận của tác nhân, khiến không thể phân biệt giữa suy luận chậm và lệnh gọi Tools chậm.
- Coi telemetry như việc phụ, tạo ra lỗ hổng trong tính liên tục của trace qua các ranh giới tác nhân, lệnh gọi Tools, và thao tác bất đồng bộ.
- Thu thập dữ liệu telemetry mà không thiết lập đường cơ sở (baseline), ngưỡng, hay cảnh báo, tạo ra một hồ dữ liệu chỉ số mà không ai giám sát hay hành động.

**Lợi ích khi áp dụng thực hành tốt này:**

- Dữ liệu hiệu năng chi tiết hướng công sức kỹ thuật vào các thao tác thực sự góp phần vào latency đầu-cuối, giúp ngăn lãng phí công sức vào các thành phần có tác động không đáng kể tới trải nghiệm người dùng.
- Quy trách nhiệm cấp-span giảm thời-gian-trung-bình-để-giải-quyết cho các sự cố production bằng cách chỉ chính xác liệu phản hồi chậm bắt nguồn từ suy luận, gọi Tools, truy xuất, hay điều phối liên tác nhân.
- Dữ liệu telemetry lịch sử hỗ trợ lựa chọn Model, định tuyến, và lập kế hoạch dung lượng có căn cứ bằng cách so sánh profile latency, token, và chi phí giữa các Model và kiến trúc.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Telemetry tác nhân toàn diện nghĩa là nắm bắt chỉ số, trace, và log, đồng thời cấu trúc chúng sao cho mọi bước của pipeline suy luận đều có thể quy trách nhiệm riêng lẻ. Nếu bất kỳ bước nào trong nhiều thao tác riêng của tác nhân bị mờ đục, việc điều tra hiệu năng trở nên ít dựa-trên-dữ-liệu hơn và do đó kém hữu ích hơn.

[OpenTelemetry (OTel)](https://opentelemetry.io/) là nền di động cho việc đo lường này, và [các quy ước ngữ nghĩa AI tạo sinh](https://opentelemetry.io/docs/specs/semconv/gen-ai/) của nó định nghĩa các thuộc tính chuẩn cho thao tác LLM, model, token vào và ra, tham số yêu cầu, và lý do kết thúc để các span vẫn có thể so sánh giữa các framework, Model, và runtime. Dùng các quy ước này thay vì các lược đồ riêng của framework giữ cho telemetry di động khi một tác nhân di chuyển giữa Amazon Bedrock AgentCore Runtime, AWS Lambda, Amazon ECS, Amazon EKS, hay hạ tầng tự vận hành, và giúp tránh việc viết lại mỗi khi đích triển khai thay đổi.

Telemetry tác nhân có một phân cấp ba tầng tự nhiên được ghi tài liệu trong [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html).

- Một *session* biểu diễn một cuộc hội thoại người dùng hoàn chỉnh
- Một *trace* biểu diễn một chu kỳ yêu cầu-phản hồi trong phiên
- Các *span* biểu diễn các thao tác rời rạc bên trong một trace, một vòng lặp suy luận, một lệnh gọi LLM, một lệnh gọi Tools, một tra cứu bộ nhớ, một truy vấn truy xuất, hoặc một lượt bàn giao liên tác nhân

Tổ chức telemetry theo phân cấp này biến một tín hiệu tác nhân chậm mờ đục thành một cây thực thi có thể quy trách nhiệm, nơi mỗi span mang latency riêng, số đếm token, trạng thái lỗi, và các thuộc tính ngữ cảnh. Định danh phiên (session identifier) phải chảy qua mọi span để một trace có thể liên kết ngược về cuộc hội thoại của nó, và ngữ cảnh trace phải lan truyền qua các ranh giới tác nhân và Tools bằng chuẩn [W3C Trace Context](https://www.w3.org/TR/trace-context/) để các luồng công việc bất đồng bộ và đa-dịch-vụ vẫn là một đồ thị liên kết duy nhất.

Cách tiếp cận đo lường khác nhau theo runtime, nhưng telemetry kết quả nên trông giống nhau. Với tác nhân trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), runtime tự-động-đo mã tác nhân và phát ra trace tương thích OTel, chỉ số runtime (số lần gọi, số phiên, latency, lỗi, dùng CPU và bộ nhớ), và log có cấu trúc tới Amazon CloudWatch mà không cần thêm việc.

Với tác nhân trên các runtime khác, [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/docs/introduction) xuất trace, chỉ số, và log tới CloudWatch dùng cùng các quy ước ngữ nghĩa để cả hai nhóm cùng xuất hiện trên một bề mặt observability thống nhất.

Các thư viện đo lường cấp-framework như OpenInference, OpenLLMetry, OpenLit, và Traceloop phát ra các span của pipeline suy luận, các vòng lặp suy luận, nội dung prompt và phản hồi, các quyết định lựa-chọn-Tools, mà việc đo lường runtime chung chung không thể thấy. Hãy chọn một framework dựa trên framework tác nhân đang dùng (ví dụ Strands Agents, LangChain, LangGraph, CrewAI, hay LlamaIndex).

Ở phía nạp dữ liệu, [Amazon CloudWatch Transaction Search](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html) nạp 100% span dưới dạng log có cấu trúc trong log group aws/spans và lập chỉ mục một tỷ lệ có thể cấu hình dưới dạng tóm tắt trace, hỗ trợ tìm kiếm trace đầu-cuối mà không ép lấy mẫu (sampling) ở cấp span. Bật [CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Services-example-scenario-GenerativeAI.html) trên các lệnh gọi API Amazon Bedrock tự động nạp các thuộc tính OTel GenAI, gen_ai.system, gen_ai.request.model, gen_ai.usage.input_tokens, gen_ai.usage.output_tokens, gen_ai.response.finish_reasons, nên phân tích token, chi phí, và lý-do-kết-thúc có sẵn mà không cần span viết tay.

Một số tín hiệu có thể không được nắm bắt ngầm định, như tỷ lệ thành công và thất bại của tác vụ, tỷ lệ trúng cache, độ chính xác lựa chọn Tools, time-to-first-token, và chi phí mỗi tác vụ. Với các tín hiệu này, hãy phát chúng dưới dạng chỉ số tùy chỉnh CloudWatch từ tác nhân hoặc bộ thu OTel, có kích thước (dimension) đồng nhất (agent ID, workflow, môi trường, loại tác vụ, model ID) để chúng có thể tương quan với các span mà chúng bắt nguồn và được tiêu thụ bởi bảng điều khiển, SLO, và phát hiện bất thường ở hạ nguồn.

### Các bước triển khai

- **Định nghĩa một lược đồ telemetry chuẩn hóa:** Ghi tài liệu các loại span mà tác nhân sẽ phát (vòng lặp suy luận, suy luận LLM, gọi Tools, thao tác bộ nhớ, truy xuất, bàn giao liên tác nhân) và các thuộc tính bắt buộc cho mỗi loại, căn chỉnh span LLM theo [các quy ước ngữ nghĩa AI tạo sinh của OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/) và span tác nhân theo [các quy ước span tác nhân GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/). Chỉ định một tập kích thước chỉ số nhất quán, agent ID, workflow, môi trường, loại tác vụ, model ID, mà mọi chỉ số tùy chỉnh và span đều phải mang để tín hiệu vẫn tương quan được trên toàn ngăn xếp.
- **Đo lường pipeline suy luận trên mọi lớp thực thi:** Bọc các vòng lặp suy luận, suy luận LLM, gọi Tools, thao tác bộ nhớ, truy vấn truy xuất, và bàn giao liên tác nhân thành span OpenTelemetry. Với tác nhân trên Amazon Bedrock AgentCore Runtime, runtime tự-động-đo mã tác nhân khi bật [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html). Với tác nhân trên các runtime khác, dùng [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/docs/introduction) cùng một thư viện đo lường riêng của framework (OpenInference, OpenLLMetry, OpenLit, hoặc Traceloop) để nắm bắt span pipeline suy luận chứ không chỉ span cấp-yêu-cầu.
- **Lan truyền ngữ cảnh trace và session qua mọi ranh giới:** Mang các header [W3C Trace Context](https://www.w3.org/TR/trace-context/) qua mọi lệnh gọi đi mà tác nhân thực hiện, gọi Tools, truy vấn truy xuất, bàn giao liên tác nhân, công việc bất đồng bộ dựa-trên-hàng-đợi, để một yêu cầu người dùng duy nhất tạo ra một trace liên kết duy nhất thay vì các mảnh rời rạc. Lan truyền định danh phiên qua baggage của OpenTelemetry để mọi span trong một cuộc hội thoại có thể liên kết ngược về phiên của nó cho phân tích cấp-hội-thoại.
- **Bật nạp CloudWatch cho span và thuộc tính API Amazon Bedrock:** Hoàn tất thiết lập một-lần cho [CloudWatch Transaction Search](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html) để 100% span được nạp dưới dạng log có cấu trúc và một tỷ lệ có thể cấu hình được lập chỉ mục dưới dạng tóm tắt trace. Bật [CloudWatch Application Signals với hỗ trợ thuộc tính GenAI](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Services-example-scenario-GenerativeAI.html) để tự động nạp các thuộc tính OTel GenAI trên các lệnh gọi API Amazon Bedrock, nhờ đó dữ liệu token, model, và lý-do-kết-thúc được nắm bắt mà không cần đo lường tùy chỉnh.
- **Phát chỉ số tùy chỉnh cho các tín hiệu không được nắm bắt nguyên bản:** Công bố tỷ lệ thành công và thất bại của tác vụ, tỷ lệ trúng cache, độ chính xác lựa chọn Tools, time-to-first-token, và chi phí mỗi tác vụ dưới dạng [chỉ số tùy chỉnh CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) từ runtime tác nhân hoặc bộ thu OTel, dùng tập kích thước chuẩn định nghĩa ở bước 1. Không có chúng, công cụ observability có thể hiển thị tín hiệu hạ tầng và suy luận nhưng không thể trả lời câu hỏi cấp-sản-phẩm về chất lượng tác nhân hay kinh tế đơn vị.
- **Xây dựng bề mặt observability:** Dùng [bảng điều khiển khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html) để cung cấp các góc nhìn session, trace, và tác nhân cho phân loại sự cố và phân tích xu hướng, và công bố các bảng điều khiển được soạn cho các lát cắt theo-luồng-công-việc, theo-Model, và theo-tenant dùng tập kích thước chuẩn.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công bám sát hiệu năng cho các khối công việc tác nhân](agentperf01-bp01.md)
- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](agentperf01-bp03.md)
- [AGENTOPS05-BP01 Thiết lập tracing và telemetry đầu-cuối cho các thao tác tác nhân](../../1-operational-excellence/5-agentops05/agentops05-bp01.md)
- [AGENTOPS05-BP05 Tạo bảng điều khiển riêng theo luồng công việc cho sức khỏe vận hành](../../1-operational-excellence/5-agentops05/agentops05-bp05.md)
- [AGENTCOST05-BP02 Triển khai tracing chi phí phân tán cho các luồng công việc đa tác nhân](../../5-cost-optimization/5-agentcost05/agentcost05-bp02.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Blog: Xây dựng tác nhân AI đáng tin cậy với Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/build-trustworthy-ai-agents-with-amazon-bedrock-agentcore-observability/)
- [Khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html)
- [CloudWatch Application Signals: Khắc phục sự cố ứng dụng AI tạo sinh với các thuộc tính OpenTelemetry GenAI](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Services-example-scenario-GenerativeAI.html)
- [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/docs/introduction)
- [Blog: Quan sát các khối công việc AI dạng tác nhân bằng Amazon CloudWatch](https://aws.amazon.com/blogs/mt/observing-agentic-ai-workloads-using-amazon-cloudwatch/)

**Video liên quan:**

- [AWS re:Invent 2024 - Observability cho Agentic AI đáng tin cậy với Strands & OpenTelemetry (NTA406)](https://www.youtube.com/watch?v=qJxF4XfMLhk)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Observability](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/06-AgentCore-observability)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [Amazon CloudWatch Application Signals](https://aws.amazon.com/cloudwatch/features/application-monitoring/)
- [AWS Distro for OpenTelemetry (ADOT)](https://aws.amazon.com/otel/)
