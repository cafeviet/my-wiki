# AGENTPERF02-BP04 Tối ưu phản hồi streaming và time-to-first-token cho các tương tác tác nhân

Các tác nhân hướng-người-dùng được đánh giá theo **latency** cảm nhận, không phải tổng thời gian xử lý. **Time-to-first-token (TTFT)**, độ trễ trước khi đầu ra đầu tiên tới người dùng, là tín hiệu hiệu-năng-cảm-nhận chi phối, và phân phối dạng streaming giữ TTFT ngắn ngay cả khi tổng xử lý mất vài giây. Streaming dạng tác nhân bị làm phức tạp bởi các vòng lặp suy luận phải dừng giữa luồng để gọi **Tools** và bởi các luồng công việc đa tác nhân nơi tác nhân cuối stream trong khi các tác nhân thượng nguồn vẫn đang tạo ra kết quả.

**Kết quả mong muốn:**

- Bạn có TTFT được theo dõi như một KPI riêng biệt với latency đầu-cuối, với mục tiêu bị giới hạn bởi loại tương tác.
- Bạn có đầu ra LLM được stream tới người dùng khi nó được sinh ra, để người dùng bắt đầu thấy đầu ra sớm trước khi vòng lặp suy luận kết thúc.
- Bạn có latency tiền-suy-luận, lắp ráp ngữ cảnh, dựng prompt, truy xuất, được giữ đủ ngắn để nó không chi phối TTFT.
- Bạn có các lệnh gọi Tools được xử lý trong luồng để người dùng nhận phản hồi tiến trình thay vì một khoảng dừng không giải thích khi tác nhân gọi một Tool giữa phản hồi.
- Bạn có các luồng công việc đa tác nhân được thiết kế để tác nhân hướng-người-dùng bắt đầu stream ngay khi các đầu vào của nó sẵn sàng, thay vì chặn cho tới khi mọi tác nhân thượng nguồn hoàn thành đầy đủ.

**Các phản mẫu thường gặp (anti-patterns):**

- Chờ phản hồi tác nhân hoàn chỉnh trước khi phân phối bất kỳ đầu ra nào, khiến latency cảm nhận bằng tổng thời gian xử lý thay vì time-to-first-token.
- Stream lệnh gọi suy luận LLM nhưng không stream pipeline tiền-suy-luận, nên truy xuất ngữ cảnh và dựng prompt thêm vài giây trễ trước khi token đầu tiên tới người dùng.
- Dừng luồng đầu ra mà không có chỉ báo khi tác nhân gọi một Tool giữa phản hồi, nên người dùng thấy đầu ra một phần rồi một khoảng dừng không giải thích.
- Chặn các luồng công việc đa tác nhân cho tới khi mọi tác nhân thượng nguồn hoàn thành trước khi tác nhân hướng-người-dùng bắt đầu stream, chuyển trễ điều phối tuần tự thành latency người-dùng-thấy.
- Coi TTFT là hoán đổi được với latency đầu-cuối trong KPI và cảnh báo, nên các hồi quy về time-to-first-token không được chú ý trong khi các chỉ số tổng-thời-lượng trông không đổi.

**Lợi ích khi áp dụng thực hành tốt này:**

- Time-to-first-token dưới một giây giữ tác nhân cảm thấy nhanh ngay cả khi tổng thời gian xử lý trải qua vài giây.
- Phản hồi tiến trình thay thế các khoảng dừng không giải thích mà nếu không sẽ xuất hiện với người dùng như một khựng khi Tools chạy giữa luồng.
- Theo dõi TTFT như một KPI riêng biệt phơi bày độ trôi trong độ nhạy bén cảm nhận mà các bảng điều khiển latency đầu-cuối sẽ che giấu.
- Streaming tiệm tiến trong các luồng công việc đa tác nhân cho phép tác nhân hướng-người-dùng phân phối đầu ra đồng thời với xử lý thượng nguồn thay vì chặn cho tới khi mọi bước thượng nguồn hoàn thành.
- Một TTFT ngắn giảm tỷ lệ người dùng bỏ các khối công việc tương tác trước khi bất kỳ đầu ra nào xuất hiện.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Time-to-first-token (TTFT) thường là chỉ số hiệu năng định hình trực tiếp nhất nhận thức của người dùng về một tác nhân tương tác. Một phản hồi bắt đầu trong vài trăm mili-giây thường cảm thấy nhanh với người dùng ngay cả khi tổng sinh mất vài giây. Latency đầu-cuối và TTFT dịch chuyển độc lập. Một Model nhanh hơn cải thiện tổng thời lượng nhưng để TTFT không đổi khi pipeline tiền-suy-luận là điểm nghẽn, nên chỉ theo dõi tổng latency che giấu các hồi quy mà người dùng thực sự cảm nhận. Khác biệt nằm ở việc đo TTFT như một chỉ số riêng biệt, tách khỏi các bảng điều khiển tổng-thời-lượng.

Stream đầu ra của Model là cần thiết nhưng chưa đủ: đến lúc token đầu tiên rời Model, tác nhân đã có thể tiêu hết ngân sách TTFT vào công việc xảy ra trước khi suy luận bắt đầu. Lắp ráp ngữ cảnh, dựng prompt, truy xuất, và các kiểm-tra-trước tuần tự đều tính, và streaming không phục hồi được gì từ cửa sổ đó.

Đường tiền-suy-luận thường là nơi các cải thiện TTFT đáng kể nhất đến từ: nén truy xuất, thu hẹp ngữ cảnh được truy xuất, và song song hóa các bước tiền-suy-luận độc lập. Cùng các mẫu đồng thời và kết-nối-ấm giảm tổng latency ở nơi khác trong trụ cột này áp cho đường tiền-suy-luận, và chúng hoàn vốn cụ thể đối chiếu TTFT. Lọc hậu-suy-luận cũng trong ngân sách. [Các chế độ streaming của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html) đưa vào một đánh đổi tường minh giữa độ chính xác kiểm duyệt và TTFT phải được tinh chỉnh theo khối công việc thay vì để mặc định.

Trên Amazon Bedrock, [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) là API suy luận streaming không-phụ-thuộc-Model được khuyến nghị cho các khối công việc chat và tác nhân, trong khi [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) vẫn sẵn có khi cần hình dạng payload riêng-của-Model. Cả hai phát ra một luồng sự kiện gồm các sự kiện bắt đầu, delta, và dừng của khối nội dung mà lớp tác nhân dịch thành đầu ra người-dùng-thấy.

Gọi Tools đưa vào một đứt gãy. Khi Model quyết định gọi một Tool, luồng sự kiện mở một khối nội dung loại toolUse, stream đầu vào của Tool dưới dạng delta, rồi dừng trong khi tác nhân chạy Tool và nạp kết quả trở lại. Một client không nhận tín hiệu nào trong khoảng trống này hiển thị cho người dùng đầu ra một phần rồi một khựng im lặng. Mẫu cơ sở, đệm-rồi-tiếp-tục (buffer-and-resume) với một chỉ báo tiến trình tường minh, chuyển tiếp một trạng thái người-dùng-thấy ngay khi một khối tool-use xuất hiện và tiếp tục stream khi khối nội dung tiếp theo bắt đầu. Các mẫu nâng cao hơn như speculative streaming tồn tại, nhưng cơ sở là không có khoảng dừng im lặng nào tới người dùng.

Các pipeline đa tác nhân khuếch đại vấn đề TTFT khi mọi tác nhân thượng nguồn phải hoàn thành đầy đủ trước khi tác nhân hướng-người-dùng bắt đầu. Mỗi lượt bàn giao tuần tự đóng góp toàn bộ thời lượng của nó vào TTFT thay vì chồng lấp với công việc hạ nguồn. Streaming tiệm tiến là lựa chọn thay thế, nơi tác nhân hướng-người-dùng bắt đầu suy luận ngay khi các đầu vào tối thiểu cần thiết sẵn sàng, và các đầu ra trung gian của các tác nhân thượng nguồn stream vào ngữ cảnh của nó khi chúng được tạo ra.

Các framework tác nhân phơi bày mẫu này trực tiếp: [Strands Agents](https://strandsagents.com/) yield các sự kiện tác nhân (token, gọi Tools, message) dưới dạng một async iterator mà các bên tiêu thụ hạ nguồn có thể đăng ký, và các trình điều phối dựa-trên-đồ-thị như LangGraph phơi bày các nguyên hàm streaming tương đương. Dành bàn-giao-phản-hồi-đầy-đủ đồng bộ cho các luồng công việc nơi tác nhân hạ nguồn thực sự không thể bắt đầu cho tới khi kết quả thượng nguồn hoàn chỉnh.

Hai khả năng của AWS giảm inter-token latency và chi phí điều phối vượt ra ngoài những gì lựa chọn API một mình có thể mang lại. [Suy luận tối-ưu-latency của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html) (bản xem trước tại thời điểm công bố) giảm inter-token latency trên các Model được hỗ trợ qua các tối ưu định tuyến và dung lượng, với cái giá là giới hạn throughput chặt hơn và trần token riêng-của-Model. Với các khối công việc thoại và tương tác thời-gian-thực, [streaming hai chiều của Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-bidirectional-streaming.html) qua WebSocket hoặc WebRTC cho phép client gửi đầu vào trong khi tác nhân vẫn đang stream đầu ra, tiền đề cho hành vi ngắt lời và luân-phiên-lượt tự nhiên trong các tác nhân thoại.

[Amazon Nova Sonic](https://docs.aws.amazon.com/nova/latest/userguide/speech.html) cung cấp một đường thoại-tới-thoại trên Amazon Bedrock. Bạn có thể định tuyến thoại qua Amazon Nova Sonic thay vì các giai đoạn thoại-tới-văn-bản, sinh-văn-bản, và văn-bản-tới-thoại riêng biệt, gộp nhiều giai đoạn tuần tự thành một luồng hai chiều. Cách tiếp cận này thường mang lại cải thiện TTFT đáng kể cho các khối công việc thoại.

### Các bước triển khai

- **Định nghĩa mục tiêu TTFT cho mỗi loại tương tác hướng-người-dùng:** Đặt một mục tiêu TTFT cho mỗi khối công việc dựa trên cách người dùng tiêu thụ đầu ra, chat văn bản chịu được hàng trăm mili-giây, thoại chịu được ít hơn nhiều, các pipeline batch hoàn toàn không có TTFT hướng-người-dùng. Coi mục tiêu là một ngân sách được phân bổ qua công việc tiền-suy-luận, latency token-đầu-tiên của Model, và bất kỳ hậu-xử-lý nào, và neo nó vào nghiên cứu người dùng hoặc chuẩn thiết-kế-tương-tác đã công bố thay vì một con số tròn.
- **Đo TTFT như hai chỉ số riêng biệt, TTFT pipeline và TTFT model:** Phát *TTFT pipeline* tại ranh giới hướng-người-dùng (byte đầu ra đầu tiên tới client) như KPI của SLO, và *TTFT model* tại delta văn bản đầu tiên từ lệnh gọi suy luận mà đầu ra của nó lần đầu stream tới người dùng, việc này cô lập hành vi Model và định tuyến khỏi các đóng góp tiền-suy-luận và hậu-xử-lý. Công bố cả hai qua [OpenTelemetry qua endpoint OTLP của CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) hoặc [CloudWatch Embedded Metric Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html). Khi TTFT pipeline và TTFT model phân kỳ, khoảng cách chỉ tới các bên đóng góp không-phải-Model.
- **Mở rộng đo TTFT tới các khối công việc đa-suy-luận và thoại:** Khi một tác nhân thực hiện nhiều lệnh gọi suy luận mỗi yêu cầu, trình lập kế hoạch, bộ định tuyến, fan-out sub-agent, coi các lệnh gọi thượng nguồn im lặng như một phần của ngân sách tiền-suy-luận và phát TTFT theo-lệnh-gọi dưới dạng một kích thước có nhãn để đóng góp của mỗi lệnh gọi suy luận vẫn hiển thị cho chẩn đoán. Với các khối công việc thoại, thêm time-to-first-audio-chunk vì việc token văn bản tới là một tín hiệu thượng nguồn, không phải ranh giới người dùng.
- **Giảm latency tiền-suy-luận trên đường tới hạn tới token đầu tiên:** Profile công việc xảy ra giữa lúc yêu cầu tới và lệnh gọi suy luận đầu tiên, lắp ráp ngữ cảnh, truy xuất, dựng prompt, kiểm-tra-trước, và nén hoặc song song hóa nó để phần lớn ngân sách TTFT còn lại khi Model bắt đầu sinh. Các mẫu đồng thời và tái-dùng-kết-nối áp dụng ở nơi khác để giảm latency đầu-cuối hoàn vốn cụ thể đối chiếu TTFT khi áp cho đường tiền-suy-luận. Phân phối token streaming không thể phục hồi bất kỳ thời gian nào mất trước lệnh gọi Model đầu tiên.
- **Dùng các API suy luận streaming thay vì suy luận đồng bộ cho các tác nhân hướng-người-dùng:** Gọi [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) như mặc định không-phụ-thuộc-Model cho các khối công việc chat và tác nhân. Dùng [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) chỉ khi cần hình dạng payload riêng-của-Model. Tiêu thụ luồng sự kiện khi nó tới và chuyển tiếp mỗi delta khối nội dung tới client thay vì đệm phản hồi đầy đủ ở phía máy chủ.
- **Tinh chỉnh chế độ streaming của Amazon Bedrock Guardrails khi guardrail nằm trên đường tới hạn:** Nếu [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html) lọc đầu ra trên đường hướng-người-dùng, chọn chế độ xử lý luồng dựa trên khả năng chịu chính sách của khối công việc, xử lý đồng bộ nâng độ chính xác kiểm duyệt và nâng TTFT, xử lý bất đồng bộ bảo toàn TTFT với cái giá có thể phát ra một token sau đó bị thu hồi. Dẫn dắt quyết định chế độ theo hồ sơ rủi-ro-nội-dung của khối công việc.
- **Hiển thị các sự kiện gọi-Tools cho người dùng thay vì dừng luồng một cách im lặng:** Khi Model phát ra một sự kiện tool-use giữa luồng, chuyển tiếp một chỉ báo tiến trình người-dùng-thấy tới client trước khi tác nhân bắt đầu thực thi Tool, và tiếp tục stream khi khối nội dung tiếp theo bắt đầu. Dùng các ranh giới bắt đầu và dừng tường minh của khối nội dung tool-use làm tín hiệu để chuyển UI giữa các trạng thái streaming và đang-làm-việc, thay vì để client thấy một khoảng trống im lặng.
- **Stream các luồng công việc đa tác nhân một cách tiệm tiến thay vì chặn theo hoàn thành thượng nguồn:** Thiết kế điều phối để tác nhân hướng-người-dùng bắt đầu suy luận ngay khi các đầu vào tối thiểu cần thiết sẵn sàng, và đường ống các sự kiện trung gian thượng nguồn vào ngữ cảnh của nó khi chúng được tạo ra. Các framework tác nhân phơi bày mẫu bàn-giao-streaming này trực tiếp qua các nguyên hàm async-iterator như API streaming của [Strands Agents](https://strandsagents.com/) và các cơ chế tương đương trong các trình điều phối dựa-trên-đồ-thị. Dành bàn-giao-phản-hồi-đầy-đủ đồng bộ cho các luồng công việc nơi tác nhân hạ nguồn thực sự không thể bắt đầu cho tới khi kết quả thượng nguồn hoàn chỉnh.
- **Đánh giá suy luận tối-ưu-latency cho inter-token latency trên các Model được hỗ trợ:** [Suy luận tối-ưu-latency của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html) (bản xem trước tại thời điểm công bố) giảm inter-token latency trên các Model được hỗ trợ, Amazon Nova Pro, Anthropic Claude 3.5 Haiku, và Meta Llama 3.1 70B/405B, qua các tối ưu định tuyến và dung lượng, với cái giá là giới hạn throughput chặt hơn và trần token riêng-của-Model. Bật chế độ latency trên API runtime và xác nhận bằng đo TTFT hai-chỉ-số rằng phần giảm là thực cho khối công việc chứ không phải một hiện vật do cache-được-làm-ấm.
- **Dùng streaming hai chiều của AgentCore Runtime và Amazon Nova Sonic cho các khối công việc thoại và thời-gian-thực:** Với các tác nhân thoại và các khối công việc khác nơi người dùng phải ngắt lời hoặc luân-phiên-lượt, chạy tác nhân trên [streaming hai chiều của Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-bidirectional-streaming.html) qua WebSocket hoặc WebRTC để client có thể gửi đầu vào trong khi tác nhân đang stream đầu ra. Định tuyến thoại cụ thể qua [Amazon Nova Sonic](https://docs.aws.amazon.com/nova/latest/userguide/speech.html), vốn gộp các giai đoạn thoại-tới-văn-bản, sinh-văn-bản, và văn-bản-tới-thoại riêng biệt của một pipeline thoại truyền thống thành một luồng hai chiều duy nhất, thường là một cải thiện TTFT đáng kể cho các khối công việc thoại.
- **Đo lại TTFT sau mỗi thay đổi và khi lưu lượng dịch chuyển:** Profile lại cả TTFT pipeline lẫn TTFT model dưới tải production đại diện sau khi áp dụng các thay đổi streaming, tiền-suy-luận, xử-lý-Tools, hoặc runtime, vì các tối ưu hoạt động khi cô lập thường hồi quy ở quy mô. Cảnh báo trên các vi phạm phân vị TTFT riêng biệt với các SLO latency đầu-cuối để các hồi quy về độ nhạy bén cảm nhận hiện lên trước khi chúng tới người dùng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](../1-agentperf01/agentperf01-bp03.md)
- [AGENTPERF02-BP02 Triển khai chiến lược lựa chọn Model phù hợp tác vụ](agentperf02-bp02.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](agentperf02-bp03.md)
- [AGENTPERF05-BP04 Triển khai các mẫu ủy quyền và bàn giao tác nhân hiệu quả](../5-agentperf05/agentperf05-bp04.md)

**Tài liệu liên quan:**

- [API Amazon Bedrock ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)
- [API Amazon Bedrock InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)
- [Suy luận tối-ưu-latency của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html)
- [Streaming của Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html)
- [Streaming hai chiều của Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-bidirectional-streaming.html)
- [Bắt đầu với streaming hai chiều dùng WebSocket trên AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-websocket.html)
- [Amazon Nova Sonic, thoại hội thoại thời-gian-thực](https://docs.aws.amazon.com/nova/latest/userguide/speech.html)
- [Đặc tả CloudWatch Embedded Metric Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html)
- [Công bố chỉ số tùy chỉnh tới Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html)
- [AWS blog: Streaming hai chiều cho tương tác tác nhân thời-gian-thực nay đã có trong Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/bi-directional-streaming-for-real-time-agent-interactions-now-available-in-amazon-bedrock-agentcore-runtime/)

**Ví dụ liên quan:**

- [Amazon Bedrock AgentCore samples, hướng dẫn Runtime](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)
- [Amazon Bedrock AgentCore samples, tích hợp Nova Sonic](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/nova/nova-sonic)

**Workshop liên quan:**

- [Đào sâu vào Bedrock AgentCore, Runtime](https://catalog.workshops.aws/agentcore-deep-dive/en-US/20-agentcore-runtime)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
