# AGENTSUS01-BP05 Áp dụng tác vụ theo hướng đặc tả (specification-driven) cho các Agent frontier và quy trình chạy dài

Các Agent chạy dài không có tiêu chí thành công tường minh và ngân sách tài nguyên sẽ trôi dạt vào việc thăm dò không bao giờ hoàn toàn kết thúc, tiêu tốn giờ compute vào những nhánh không mang lại giá trị. Các đặc tả (specification) khai báo trước những đầu ra chấp nhận được, mức trần chi phí và điều kiện kết thúc sẽ biến việc thực thi kéo dài thành một khoản đầu tư có giới hạn thay vì vô hạn định.

**Kết quả mong muốn:**

- Bạn có các đặc tả cho mỗi Agent frontier khai báo thời lượng thực thi tối đa, ngân sách token, cấp phát bộ nhớ và các điều kiện kích hoạt kết thúc trước khi triển khai.
- Các quy trình chạy dài tạm dừng tại các điểm kiểm tra được xác định để đánh giá tiến độ đối chiếu với đặc tả, và các quyết định tiếp tục, sửa đổi hay kết thúc được thông tin bởi đánh giá đó.
- Các Agent frontier cha xếp tầng ngân sách và thời gian còn lại xuống các Agent con mà chúng sinh ra, để việc ủy quyền kế thừa mức trần của Agent cha.
- Sự tuân thủ đặc tả được giám sát trong production và phản hồi ngược vào việc tinh chỉnh template cho các quy trình frontier trong tương lai.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các Agent chạy dài mà không có ngân sách tài nguyên tường minh hay điều kiện kết thúc, nên việc thăm dò vô giới hạn là điều có thể xảy ra về mặt cấu trúc.
- Bỏ sót tiêu chí thành công và các ranh giới ra quyết định khỏi cấu hình quy trình frontier, tạo ra các mẫu thực thi lãng phí nơi compute bị tiêu thụ mà không có giá trị tương xứng.
- Chạy các quy trình kéo dài mà không đánh giá dựa trên điểm kiểm tra, nên không ai có thể đưa ra quyết định có thông tin về việc sửa đổi hay kết thúc một lần chạy đang diễn ra.
- Sinh các Agent con từ quy trình frontier mà không chuyển ngân sách còn lại xuống dưới, phá vỡ mức trần chi phí ngay ở lần ủy quyền đầu tiên.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các quy trình kéo dài đi kèm trách nhiệm giải trình: khoản đầu tư compute được đối chiếu với giá trị kinh doanh tạo ra thay vì bị tiêu thụ vô hạn định.
- Các đánh giá tại điểm kiểm tra cho người vận hành cơ hội chuyển hướng hoặc dừng công việc trước khi nó đốt hạ tầng một cách bất cân xứng.
- Các template đặc tả tích lũy tri thức tổ chức về hành vi kỳ vọng cho các mẫu khối công việc frontier phổ biến.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Các Agent frontier — các cây viết mã, các Agent nghiên cứu chuyên sâu và các bộ lập kế hoạch tự chủ — vốn được thiết kế theo kiểu mở (open-ended). Điều đó khiến chúng là nơi mà kỷ luật tài nguyên quan trọng nhất, vì chi phí của một cuộc thăm dò vô giới hạn cao hơn nhiều bậc so với chi phí của một lệnh gọi bị định tuyến sai đơn lẻ. Một đặc tả được viết trước khi triển khai cho Agent một thứ để đối chiếu khi kết thúc:

- Một tiêu chí thành công nói rằng "việc này đã xong"
- Một ngân sách token giới hạn tổng mức tiêu thụ
- Một giới hạn thời lượng giúp ngăn các lần chạy vô thời hạn
- Các điều kiện kích hoạt kết thúc tường minh cho những tình huống mà việc tiếp tục đã trở nên vô nghĩa

Không có hợp đồng đó, Agent chạy cho đến khi tình cờ tạo ra được thứ gì đó hoặc chạm mức trần do hạ tầng áp đặt.

Ngân sách phải xếp tầng để đặc tả có hiệu lực. Khi một Agent cha frontier ủy quyền cho các Agent con, mức trần của Agent cha trở nên vô nghĩa trừ khi các con kế thừa nó. Đây là mối bận tâm về điều phối, không phải một tính năng nền tảng. Trong [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html), ngân sách còn lại được truyền dưới dạng tham số vào các lần gọi quy trình con. Trong một hệ thống được điều phối bởi Strands, nó được đưa vào system prompt hoặc ngữ cảnh gọi của Agent con. Hãy làm cho việc xếp tầng tường minh trong thiết kế thay vì giả định các con kế thừa theo quy ước.

Cấu trúc các quy trình chạy dài để tạm dừng tại các điểm được xác định — sau khi sinh kế hoạch, sau khi thu thập thông tin, và sau mỗi giai đoạn chính — và đánh giá xem tiến độ đến thời điểm đó có biện minh cho việc tiếp tục đầu tư không. Lưu giữ trạng thái điểm kiểm tra trong AgentCore Memory để việc đánh giá có thể tạm dừng và tiếp tục Agent mà không khởi động lại nó, giữ được chi phí chìm (sunk cost) của công việc đã làm. Định nghĩa chính các đặc tả qua [Strands Agents](https://strandsagents.com/) dưới dạng cấu hình hạng nhất được đưa vào tại thời điểm gọi thông qua [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html). Bằng cách này, hợp đồng di chuyển cùng Agent. Các công cụ phát triển theo hướng đặc tả như [Kiro](https://www.aboutamazon.com/news/aws/amazon-ai-frontier-agents-autonomous-kiro) áp dụng cùng mẫu này cho các Agent viết mã, cấp cho chúng các chỉ dẫn có định hướng và có giới hạn thay vì diễn giải mở.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) theo dõi tần suất vi phạm đặc tả, các điểm kiểm tra nào đang tạo ra quyết định hữu ích, và nơi các ngân sách đang bị ràng buộc (binding). Các đặc tả không bao giờ ràng buộc và các quy trình luôn vượt qua điểm kiểm tra báo hiệu các template nên được nới lỏng. Các đặc tả thường xuyên ràng buộc báo hiệu các khối công việc cần phạm vi chặt hơn hoặc các Agent con nhỏ hơn.

### Các bước triển khai

- **Viết đặc tả trước khi triển khai:** Với mỗi Agent frontier, khai báo các thông tin sau và ghi lại tiêu chí thành công định nghĩa "đã xong": Thời lượng thực thi tối đa
- Ngân sách token
- Cấp phát bộ nhớ
- Điều kiện kích hoạt kết thúc
- **Đưa đặc tả vào tại thời điểm gọi:** Truyền các đặc tả vào [Amazon Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) qua [Strands Agents](https://strandsagents.com/) dưới dạng cấu hình hạng nhất, để hợp đồng là một phần của lần gọi thay vì ngầm ẩn trong mã Agent.
- **Xếp tầng ngân sách xuống các Agent con:** Khi một Agent cha frontier ủy quyền, truyền thời lượng, ngân sách token và ngân sách bộ nhớ còn lại vào lần gọi Agent con qua các tham số [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html) hoặc điều phối Strands, để mức trần giữ được qua việc ủy quyền.
- **Triển khai đánh giá dựa trên điểm kiểm tra:** Cấu trúc các quy trình chạy dài để tạm dừng tại các điểm được xác định, đánh giá tiến độ đối chiếu với đặc tả, và lưu giữ trạng thái trong AgentCore Memory để Agent tiếp tục từ điểm kiểm tra sau một quyết định tiếp tục/sửa đổi/kết thúc.
- **Giám sát mức tuân thủ và tinh chỉnh template:** Theo dõi các thông tin sau qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), và đưa dữ liệu quay lại các template đặc tả cho các mẫu khối công việc frontier phổ biến: Vi phạm đặc tả
- Kết quả điểm kiểm tra
- Mức sử dụng ngân sách

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSUS01-BP01 Thiết kế các Agent chuyên biệt với ranh giới tài nguyên tường minh](agentsus01-bp01.md)
- [AGENTSUS01-BP04 Điều chỉnh các đường dẫn xử lý nhận thức một cách phù hợp](agentsus01-bp04.md)
- [SUS02-BP03 Stop the creation and maintenance of unused assets](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sus_sus_software_a4.html)
- [COST02-BP02 Implement goals and targets](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_govern_usage.html)

**Các tài liệu liên quan:**

- [AWS Frontier Agents](https://aws.amazon.com/ai/frontier-agents/)
- [Introducing AWS Frontier Agents and Kiro](https://www.aboutamazon.com/news/aws/amazon-ai-frontier-agents-autonomous-kiro)
- [AWS Step Functions - Standard workflows](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html)
- [Strands Agents](https://strandsagents.com/)

**Các ví dụ liên quan:**

- [Build multi-step applications and AI workflows with AWS Lambda durable functions](https://aws.amazon.com/blogs/aws/build-multi-step-applications-and-ai-workflows-with-aws-lambda-durable-functions/)

**Các dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)

**Javascript đang bị tắt hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Amazon Web Services Documentation, Javascript phải được bật. Vui lòng tham khảo các trang Trợ giúp của trình duyệt để biết hướng dẫn.
