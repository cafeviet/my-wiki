---
title: "Các khái niệm observability"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html"
---

# Các khái niệm observability

# Tìm hiểu observability cho các tài nguyên agentic trong AgentCore

Mục này định nghĩa các khái niệm về session, trace và span khi chúng liên quan đến việc giám sát và observability (khả năng quan sát) của các agent (tác tử AI).

- [Sessions](#sessions)

- [Traces](#traces)

- [Spans](#agent_spans)

- [Mối quan hệ giữa Sessions, Traces và Spans](#relationship)

## Sessions

Một session đại diện cho một ngữ cảnh tương tác hoàn chỉnh giữa một người dùng và một agent. Các session gói toàn bộ luồng hội thoại hoặc tương tác, duy trì trạng thái và ngữ cảnh qua nhiều lượt trao đổi. Mỗi session có một định danh duy nhất và ghi lại toàn bộ vòng đời gắn kết của người dùng với agent, từ khởi tạo đến kết thúc.

Các session cung cấp các khả năng sau cho agent:

- Lưu bền ngữ cảnh qua nhiều tương tác trong cùng một cuộc hội thoại

- Quản lý trạng thái để duy trì thông tin đặc thù của người dùng

- Theo dõi lịch sử hội thoại để hiểu ngữ cảnh

- Cấp phát và quản lý tài nguyên trong suốt thời gian tương tác

- Cô lập giữa các tương tác của những người dùng khác nhau với cùng một agent

Từ góc độ observability, các session cung cấp một góc nhìn cấp cao về các mẫu gắn kết của người dùng, cho phép bạn giám sát hiệu năng agent qua các số liệu, trace và span, và hiểu cách người dùng tương tác với các agent của bạn theo thời gian và trên các trường hợp dùng khác nhau.

Theo mặc định, AgentCore cung cấp một tập các số liệu observability ở cấp session cho các agent đang chạy trong AgentCore runtime (môi trường chạy). Bạn có thể xem các số liệu runtime trong console Amazon CloudWatch trên trang generative AI observability. Trang này cung cấp nhiều loại đồ thị và trực quan hóa để giúp bạn diễn giải dữ liệu của các agent. AgentCore cũng xuất ra một tập số liệu mặc định cho các tài nguyên memory (bộ nhớ), tài nguyên gateway (cổng) và các tool (công cụ) tích hợp sẵn. Tất cả các số liệu này đều có thể xem trong CloudWatch. Ngoài các số liệu được cung cấp, log và span được cung cấp theo mặc định cho các tài nguyên memory, và bằng cách instrument code agent, bạn có thể ghi lại các số liệu, log và span tùy chỉnh cho agent của bạn, cũng có thể xem được trên trang generative AI observability của CloudWatch. Xem các mục sau và [Xem dữ liệu observability cho các agent Amazon Bedrock AgentCore của bạn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html) để tìm hiểu thêm.

## Traces

Một trace đại diện cho một bản ghi chi tiết về một chu trình request-response duy nhất, bắt đầu từ một lần gọi agent và có thể bao gồm thêm các lời gọi tới các agent khác. Các trace ghi lại toàn bộ đường thực thi của một request, bao gồm tất cả các bước xử lý nội bộ, các lời gọi dịch vụ bên ngoài, các điểm ra quyết định và mức sử dụng tài nguyên. Mỗi trace gắn với một session cụ thể và cung cấp khả năng hiển thị chi tiết về hành vi của agent cho một tương tác cụ thể.

Các trace bao gồm các thành phần sau cho agent:

- Chi tiết request bao gồm timestamp, tham số đầu vào và ngữ cảnh

- Các bước xử lý cho thấy trình tự các thao tác được thực hiện

- Các lần gọi tool với tham số input/output và thời gian thực thi

- Các số liệu sử dụng tài nguyên như thời gian xử lý

- Thông tin lỗi bao gồm chi tiết ngoại lệ và các nỗ lực khôi phục

- Chi tiết tạo phản hồi và output cuối cùng

Từ góc độ observability, các trace cung cấp những hiểu biết sâu về hoạt động nội bộ của các agent, cho phép bạn khắc phục sự cố, tối ưu hiệu năng và hiểu các mẫu hành vi. Bằng cách phân tích dữ liệu trace, bạn có thể xác định các điểm nghẽn, phát hiện các bất thường và xác minh rằng agent của bạn đang hoạt động như mong đợi trên các kịch bản và đầu vào khác nhau.

Để thu thập dữ liệu trace, bạn cần instrument code agent bằng AWS Distro for Open Telemetry (ADOT). Xem [Bật observability trong code agent cho các agent được host bởi AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html#observability-configure-custom) và [Bật observability cho các agent được host bên ngoài AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html#observability-configure-3p) để tìm hiểu thêm.

## Spans

Một span đại diện cho một đơn vị công việc rời rạc, có thể đo lường được trong luồng thực thi của một agent. Các span ghi lại các thao tác chi tiết diễn ra trong quá trình xử lý request, cung cấp khả năng hiển thị chi tiết về các thành phần và bước nội bộ tạo nên một trace hoàn chỉnh. Mỗi span có thời gian bắt đầu và kết thúc xác định, tạo ra một dòng thời gian chính xác về các hoạt động của agent và thời lượng của chúng.

Các span bao gồm các thuộc tính thiết yếu sau cho observability của agent:

- Tên thao tác định danh hàm hoặc quy trình cụ thể đang được thực thi

- Các timestamp đánh dấu thời điểm bắt đầu và kết thúc chính xác của thao tác

- Các mối quan hệ cha-con cho thấy các thao tác lồng nhau như thế nào trong các quy trình lớn hơn

- Các tag và thuộc tính cung cấp metadata theo ngữ cảnh về thao tác

- Các event đánh dấu những sự kiện quan trọng trong vòng đời của span

- Thông tin trạng thái chỉ ra thành công, thất bại hoặc các trạng thái hoàn tất khác

- Các số liệu sử dụng tài nguyên đặc thù cho thao tác

Các span tạo thành một cấu trúc phân cấp trong các trace, với các span cha bao trùm các span con đại diện cho các thao tác chi tiết hơn. Ví dụ, một span cấp cao "process user query" có thể chứa các span con cho "parse input", "retrieve context", "generate response" và "format output". Cách tổ chức phân cấp này tạo ra một cây thực thi chi tiết phơi bày toàn bộ luồng thao tác bên trong agent.

Theo mặc định, AgentCore chỉ xuất ra một tập dữ liệu span cho các tài nguyên memory (bộ nhớ). Dữ liệu này có thể được xem trong CloudWatch Logs và CloudWatch Application Signals. Để ghi lại dữ liệu span cho các agent hoặc tài nguyên gateway của bạn, bạn cần instrument agent của mình. Xem [Bật observability trong code agent cho các agent được host bởi AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html#observability-configure-custom) và [Bật observability cho các agent được host bên ngoài AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html#observability-configure-3p) để tìm hiểu thêm.

## Mối quan hệ giữa Sessions, Traces và Spans

Sessions, traces và spans tạo thành một mối quan hệ phân cấp ba tầng trong khung observability cho các agent. Một session chứa nhiều trace, mỗi trace đại diện cho một tương tác rời rạc trong ngữ cảnh rộng hơn của session. Đến lượt mình, mỗi trace chứa nhiều span ghi lại các thao tác và bước chi tiết trong tương tác đó. Cấu trúc phân cấp này cho phép bạn phân tích hành vi agent ở các mức độ chi tiết khác nhau, từ các mẫu session cấp cao đến các luồng tương tác cấp trung đến các đường thực thi chi tiết cho các thao tác cụ thể.

Mối quan hệ giữa ba thành phần observability này có thể được trực quan hóa như sau:

- Sessions (cấp cao nhất) - Đại diện cho các cuộc hội thoại hoặc ngữ cảnh tương tác hoàn chỉnh của người dùng

- Traces (cấp trung) - Đại diện cho các chu trình request-response riêng lẻ trong một session

- Spans (cấp thấp nhất) - Đại diện cho các thao tác hoặc bước cụ thể trong một trace

Mối quan hệ đa tầng này cho phép một số khả năng observability quan trọng:

- Phân tích theo ngữ cảnh các tương tác riêng lẻ trong luồng hội thoại rộng hơn của chúng

- Tương quan các request liên quan trên hành trình tương tác của người dùng

- Khắc phục sự cố tiệm tiến từ các bất thường cấp session đến các mẫu cấp trace đến các nguyên nhân gốc cấp span

- Lập hồ sơ hiệu năng toàn diện trên các chiều thời gian và chức năng khác nhau

- Hiểu tổng thể các mẫu hành vi và sự tiến hóa của agent trong suốt một cuộc hội thoại

- Xác định chính xác các điểm nghẽn hiệu năng ở cấp thao tác thông qua phân tích span

Trong khi các trace cung cấp khả năng hiển thị về các chu trình request-response hoàn chỉnh, các span mang lại những hiểu biết sâu hơn về hoạt động nội bộ của các chu trình đó. Các span phơi bày chính xác thao tác nào tiêu tốn nhiều thời gian nhất, lỗi bắt nguồn từ đâu, và các thành phần khác nhau tương tác với nhau như thế nào trong một trace duy nhất. Độ chi tiết này đặc biệt có giá trị khi khắc phục các sự cố phức tạp hoặc tối ưu hiệu năng trong các triển khai agent tinh vi.

Bằng cách tận dụng dữ liệu session, trace và span trong chiến lược observability của bạn, bạn có thể có được những hiểu biết toàn diện về hành vi, hiệu năng và tính hiệu quả của agent ở nhiều mức độ chi tiết. Cách tiếp cận observability đa lớp này hỗ trợ cải tiến liên tục, khắc phục sự cố vững chắc và tối ưu hóa dựa trên hiểu biết cho các triển khai agent của bạn, từ các mẫu hội thoại cấp cao xuống đến hiệu năng của từng thao tác riêng lẻ.
