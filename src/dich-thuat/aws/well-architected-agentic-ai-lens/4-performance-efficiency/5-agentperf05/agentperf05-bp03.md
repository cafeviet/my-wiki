# AGENTPERF05-BP03 Tối ưu thực thi pipeline AI đa-giai-đoạn

Các tác vụ tác nhân thực tế hiếm khi hoàn thành trong một bước duy nhất. Xử lý tài liệu, phân tích dữ liệu, và các luồng công việc dịch vụ khách hàng đều liên quan đến nhiều giai đoạn tuần tự nơi **throughput** của mỗi giai đoạn bị giới hạn bởi tiến trình hoặc cơ chế chậm nhất. Mỗi chuyển tiếp giai đoạn đưa vào chi phí (như tuần tự hóa, truyền tải mạng, hoặc khởi động lạnh), và streaming hoặc micro-batching cho phép các giai đoạn hạ nguồn bắt đầu xử lý trước khi các giai đoạn thượng nguồn hoàn thành, chồng lấp thực thi để cắt tổng **latency**.

**Kết quả mong muốn:**

- Bạn có các pipeline AI đa-giai-đoạn thực thi với chi phí liên-giai-đoạn tối thiểu, với dữ liệu chảy hiệu quả giữa các giai đoạn.
- Bạn có throughput pipeline được cân bằng qua các giai đoạn mà không giai đoạn nào tạo ra một điểm nghẽn dai dẳng.
- Bạn có streaming được triển khai nơi có thể để chồng lấp xử lý.
- Bạn có tài nguyên compute của mỗi giai đoạn được định-cỡ-đúng cho yêu cầu cụ thể của nó.

**Các phản mẫu thường gặp (anti-patterns):**

- Chờ toàn bộ một lô hoàn thành một giai đoạn trước khi bắt đầu giai đoạn tiếp theo, khi streaming hoặc micro-batching sẽ cho các giai đoạn hạ nguồn bắt đầu xử lý khi các kết quả thượng nguồn trở nên sẵn có.
- Dùng cùng cấu hình compute cho mọi giai đoạn pipeline bất kể yêu cầu xử lý của chúng, cấp dư cho các giai đoạn nhẹ và cấp thiếu cho các giai đoạn nặng-compute.
- Tuần tự hóa các kết quả trung gian lớn tới lưu trữ bền giữa mọi giai đoạn khi truyền trong-bộ-nhớ hoặc streaming sẽ hiệu quả hơn cho các giai đoạn thực thi liên tiếp gần nhau.

**Lợi ích khi áp dụng thực hành tốt này:**

- Streaming và micro-batching chồng lấp xử lý giai đoạn, giảm latency đầu-cuối.
- Dung lượng giai đoạn cân bằng và giao tiếp liên-giai-đoạn có-đệm cải thiện throughput.
- Compute được-định-cỡ-đúng theo giai đoạn tối ưu chi phí.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Triển khai các pipeline đa-giai-đoạn dùng [AWS Step Functions](https://aws.amazon.com/step-functions/) với các hàm [AWS Lambda](https://aws.amazon.com/lambda/) riêng-của-giai-đoạn, các tác vụ [Amazon ECS](https://aws.amazon.com/ecs/), hoặc các tác nhân host trên [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), nơi cấu hình compute của mỗi giai đoạn được tinh chỉnh độc lập. Với các pipeline có yêu cầu throughput cao, Step Functions Distributed Map xử lý các mục song song qua các giai đoạn. Định-cỡ-đúng compute cho mỗi giai đoạn, dùng Lambda cho xử lý nhẹ, ECS cho các giai đoạn nặng-compute, và AgentCore Runtime cho các giai đoạn đòi hỏi suy luận dựa-trên-LLM.

Streaming giữa các giai đoạn là phần thắng latency đơn lớn nhất khi nó áp dụng được. Dùng API suy luận streaming của Amazon Bedrock để bắt đầu hậu-xử-lý các token đầu ra khi chúng được sinh ra thay vì chờ phản hồi hoàn chỉnh. Với các pipeline dữ-liệu-nặng, [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) hoạt động như một bộ đệm liên-giai-đoạn hỗ trợ luồng dữ liệu streaming, để các giai đoạn hạ nguồn bắt đầu xử lý ngay khi các kết quả thượng nguồn sẵn có. Với các pipeline batch, micro-batching gửi các nhóm nhỏ các mục tới các giai đoạn hạ nguồn khi chúng hoàn thành thay vì chờ toàn bộ lô.

Observability cấp-pipeline qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) hoặc [AWS X-Ray](https://aws.amazon.com/xray/) truy vết các yêu cầu qua mọi giai đoạn, nhận diện đường tới hạn và giai đoạn đóng góp nhiều nhất vào latency đầu-cuối. Cân bằng các thời lượng giai đoạn bằng cách profile mỗi giai đoạn và điều chỉnh độ hạt xử lý, tách các giai đoạn chậm thành các giai-đoạn-con song song hoặc gộp các giai đoạn nhanh để giảm các chuyển tiếp liên-giai-đoạn.

### Các bước triển khai

- **Lập bản đồ pipeline đa-giai-đoạn và nhận diện các phụ thuộc giữa các giai đoạn:** Ghi tài liệu các phụ thuộc giai đoạn, các cơ hội cho streaming, và đường tới hạn để công sức tối ưu rơi vào các giai đoạn dẫn dắt latency đầu-cuối.
- **Triển khai mỗi giai đoạn như một đơn vị compute độc lập với các cấu hình tài nguyên riêng-của-giai-đoạn:** Dùng [AWS Lambda](https://aws.amazon.com/lambda/) cho xử lý nhẹ, [Amazon ECS](https://aws.amazon.com/ecs/) cho các giai đoạn nặng-compute, và AgentCore Runtime cho các giai đoạn đòi hỏi suy luận LLM, và tinh chỉnh tài nguyên của mỗi giai đoạn theo hồ sơ riêng của nó.
- **Bật streaming giữa các giai đoạn dùng API streaming của Amazon Bedrock và Kinesis Data Streams nơi áp dụng được:** Dùng API suy luận streaming để hậu-xử-lý các token đầu ra khi chúng được sinh ra, và [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) như một bộ đệm liên-giai-đoạn để các giai đoạn hạ nguồn bắt đầu xử lý khi các kết quả thượng nguồn tới.
- **Triển khai micro-batching cho các pipeline batch để giảm latency đầu-cuối:** Gửi các nhóm nhỏ các mục tới các giai đoạn hạ nguồn khi chúng hoàn thành thay vì chờ toàn bộ lô.
- **Cấu hình tracing AgentCore Observability hoặc X-Ray qua mọi giai đoạn pipeline để thấy latency đầu-cuối:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) hoặc [AWS X-Ray](https://aws.amazon.com/xray/) để truy vết các yêu cầu qua mọi giai đoạn.
- **Giám sát latency, throughput, và mức dùng tài nguyên theo-giai-đoạn để nhận diện và giải quyết các điểm nghẽn:** Công bố các chỉ số cho mỗi giai đoạn để các giai đoạn điểm-nghẽn hiển thị và có thể được tách, song song hóa, hoặc định-cỡ-lại.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả](agentperf05-bp01.md)
- [AGENTPERF02-BP04 Tối ưu phản hồi streaming và time-to-first-token cho các tương tác tác nhân](../2-agentperf02/agentperf02-bp04.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](../2-agentperf02/agentperf02-bp03.md)

**Tài liệu liên quan:**

- [Mẫu luồng công việc AI đa-giai-đoạn, Xây dựng kiến trúc serverless cho AI dạng tác nhân](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/pattern-multi-stage-ai.html)
- [Blog: Xây dựng tác nhân AI hiệu quả trên AWS Serverless](https://aws.amazon.com/blogs/compute/effectively-building-ai-agents-on-aws-serverless/)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)

**Ví dụ liên quan:**

- [GitHub: Xây dựng các luồng công việc tác nhân GenAI với Step Functions](https://github.com/aws-samples/build-genai-agent-workflows-with-step-functions)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon ECS](https://aws.amazon.com/ecs/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
