# AGENTPERF02-BP02 Triển khai chiến lược lựa chọn Model phù hợp tác vụ

Các tác vụ tác nhân biến thiên rộng về mức suy luận chúng đòi hỏi, nhưng định tuyến mặc định thường gửi mọi tác vụ tới cùng một **Model** lớn, trả phí latency của một Model hạng nặng ngay cả cho công việc mà một Model nhỏ hơn giải quyết cũng tốt. Khớp năng lực Model với nhu cầu tác vụ là một trong những quyết định hiệu năng được dùng nhiều nhất trong một hệ thống tác nhân, vì **latency** và **throughput** suy luận tỉ lệ trực tiếp với kích thước Model. Làm một cách hệ thống, lựa chọn Model giảm latency mỗi tác vụ mà không hy sinh chất lượng trên suy luận phức tạp.

**Kết quả mong muốn:**

- Bạn có các tác vụ tác nhân được phân loại theo độ phức tạp suy luận, với mỗi lớp được ánh xạ tới Model nhỏ nhất đáp ứng mức chất lượng của nó.
- Bạn có logic định tuyến hướng mỗi yêu cầu tới Model được gán tại runtime, với dự phòng theo tầng (cascading fallback) tới một Model có năng lực cao hơn khi Model được gán tạo ra đầu ra độ-tin-cậy-thấp hoặc thất bại.
- Bạn có các phép gán Model được xác nhận đối chiếu chất lượng và latency được đánh giá trên chính phân phối tác vụ của khối công việc thay vì trên các bảng xếp hạng chung.
- Bạn có lựa chọn Model được coi là một tham số có-thể-cấu-hình-tại-runtime để các bản phát hành Model mới có thể được đánh giá và triển khai mà không cần deploy lại tác nhân.
- Bạn có latency suy luận và chất lượng tác vụ được theo dõi theo từng lớp tác vụ, để các quyết định định tuyến được xác nhận liên tục đối chiếu cả hai.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng một Model lớn duy nhất cho mọi tác vụ tác nhân bất kể độ phức tạp, trả phí bảo hiểm về latency và chi phí của một Model hạng nặng cho công việc mà một Model nhỏ hơn giải quyết cũng tốt.
- Dùng một Model nhỏ hoặc đa-dụng cho các tác vụ đòi hỏi suy luận sâu hơn, tạo ra các đầu ra chất lượng thấp kích hoạt thử lại, vòng lặp suy luận thừa, hoặc leo thang thủ công và bào mòn phần tiết kiệm latency mà Model nhỏ đáng lẽ mang lại.
- Chọn Model từ các bảng xếp hạng benchmark chung thay vì từ các benchmark chạy trên chính phân phối tác vụ của khối công việc, tạo ra các lựa chọn tối ưu cho bảng xếp hạng nhưng dưới tối ưu cho lưu lượng thực tế.
- Coi lựa chọn Model là một quyết định kiến trúc một-lần được nướng vào mã ứng dụng, nên đánh giá hoặc triển khai một Model mới ra mắt đòi hỏi thay đổi mã và deploy lại thay vì cập nhật cấu hình.
- Vận hành không có đường dự phòng khi Model được gán trả về đầu ra độ-tin-cậy-thấp hoặc thất bại, buộc pipeline trả về câu trả lời kém hoặc thất bại hoàn toàn thay vì leo thang yêu cầu đó tới một Model có năng lực cao hơn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Định tuyến công việc nhẹ tới các Model nhỏ hơn, nhanh hơn tránh trả thời gian suy luận của một Model lớn cho các tác vụ không cần tới nó.
- Định tuyến tường minh tới các Model có năng lực và dự phòng theo tầng khi một Model nhỏ hơn kém hiệu quả bảo vệ độ chính xác hướng-người-dùng trên các tác vụ phức tạp.
- Benchmark đối chiếu phân phối tác vụ thực tế của khối công việc liên tục cải thiện các phép gán khi dữ liệu đánh giá mới tích lũy.
- Lựa chọn có-thể-cấu-hình-tại-runtime cho phép các cải thiện năng lực và latency từ các Model mới tới production mà không cần các chu kỳ deploy lại.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Thành phần chi phí chi phối của pipeline suy luận là lệnh gọi suy luận, và latency cùng throughput suy luận tỉ lệ trực tiếp với kích thước Model. Các khối công việc tác nhân điển hình có hỗn hợp tác vụ không đồng nhất và phân loại đơn giản bên cạnh suy luận nhiều-bước, nên áp Model lớn nhất đồng đều buộc latency và chi phí pha trộn bám theo tùy chọn có năng lực nhất dù hầu hết yêu cầu không cần. Lựa chọn Model hệ thống dịch chuyển điều này bằng cách gán mỗi tác vụ tới Model nhỏ nhất vẫn đáp ứng mức chất lượng của nó.

Hai cách tiếp cận khớp với nhau:

- Phân loại tác vụ tường minh, nơi tác nhân gán mỗi tác vụ vào một lớp và mỗi lớp vào một Model hoặc tầng Model, cho kiểm soát chi tiết và hoạt động trên các nhà cung cấp và họ Model.
- Định tuyến được quản lý như [định tuyến prompt thông minh của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html) dự đoán chất lượng phản hồi cho mỗi yêu cầu trong một họ Model và định tuyến tới Model nhỏ nhất được dự đoán đáp ứng mức chất lượng, việc này giao lại lựa chọn theo-yêu-cầu khi quyết định thuần túy là năng-lực-so-với-chi-phí bên trong một họ.

Nhiều khối công việc kết hợp cả hai. Tác nhân chọn tầng theo loại tác vụ trong khi bộ định tuyến chọn Model cụ thể trong tầng đó. Các dịch vụ chuyên-dụng như [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) cho xử lý tài liệu thông minh cũng đáng cân nhắc như một mẫu cho các tác vụ nặng-tài-liệu, nơi một pipeline chuyên dụng thường nhanh hơn và chính xác hơn việc định tuyến tài liệu qua một Model thị giác đa-dụng.

Các quyết định định tuyến chỉ tốt bằng các benchmark đứng sau chúng. Các bảng xếp hạng công khai xếp các Model theo trung bình qua các benchmark không đồng nhất mà phân phối tác vụ của chúng có thể ít giống với một khối công việc cụ thể, nên một Model dẫn đầu một benchmark chung có thể kém hiệu quả trên lưu lượng mà một tác nhân cụ thể thực sự phục vụ.

[Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) cung cấp các trình đánh giá tích hợp sẵn, LLM-as-a-Judge, độ đúng đối chiếu ground-truth, và khớp quỹ đạo (trajectory matching) khiến việc benchmark các Model ứng viên đối chiếu một tập đánh giá đại diện cho lưu lượng thực trở nên khả thi. Không có đánh giá riêng của khối công việc, các lựa chọn định tuyến thực chất là phỏng đoán.

Lựa chọn là điểm khởi đầu của một yêu cầu, không phải kết thúc của quyết định. Dự phòng theo tầng bảo toàn chất lượng mà không buộc cả lớp tác vụ sang Model lớn hơn. Dự phòng khác với thử lại: thử lại lặp lại cùng lệnh gọi hy vọng có kết quả tốt hơn, còn dự phòng thay đổi một biến bằng cách chuyển Model. Để thăng cấp các Model mới qua các đợt triển khai tiệm tiến với rollback tự động, giữ các định danh Model, ánh xạ tầng, và luật dự phòng dưới dạng cấu hình runtime trong feature flags của [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) (hoặc một dịch vụ cấu hình tương đương), kết hợp với [các chiến lược triển khai](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-deployment-strategy-create.html) được kiểm soát bởi cảnh báo CloudWatch trên latency và chất lượng.

Latency theo lớp, mức tiêu token, điểm chất lượng, và tỷ lệ leo-thang-dự-phòng thuộc về cùng bảng điều khiển hiệu năng với tổng latency và số vòng lặp suy luận. Một tỷ lệ dự phòng tăng trên một lớp là chỉ báo sớm rằng Model chính không còn phù hợp, hoặc vì lưu lượng đã dịch chuyển hoặc vì một Model mới sẵn có sẽ phục vụ lớp đó tốt hơn. Điều này thường hiện lên trước khi hồi quy hướng-người-dùng đủ lớn để kích hoạt cảnh báo.

### Các bước triển khai

- **Phân loại các tác vụ tác nhân theo độ phức tạp suy luận:** Nhóm các tác vụ của khối công việc thành các lớp dựa trên suy luận chúng đòi hỏi, ví dụ trích xuất hoặc phân loại đơn-bước, suy luận nhiều-bước có cấu trúc qua các bước đã biết, và điều tra mở. Ghi tài liệu các ví dụ đại diện cho mỗi lớp để các quyết định định tuyến có thể kiểm toán và xem lại khi phân phối tác vụ dịch chuyển. Dùng phân loại làm đầu vào cho phép gán Model thay vì để mỗi bên gọi chọn Model tùy trường hợp.
- **Benchmark các Model ứng viên trên chính phân phối tác vụ của khối công việc:** Xây dựng một tập đánh giá đại diện cho lưu lượng production và chấm điểm các Model ứng viên đối chiếu nó dùng [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) hoặc một khung đánh giá tương đương. Nắm bắt tín hiệu chất lượng (độ đúng, tỷ lệ thành công mục tiêu, khớp quỹ đạo Tools) cạnh latency và token để bạn có thể nhận diện Model nhỏ nhất đáp ứng mức chất lượng cho mỗi lớp. Coi các bảng xếp hạng như một danh sách rút gọn ban đầu, không phải quyết định.
- **Ánh xạ mỗi lớp tác vụ tới một Model hoặc tầng Model:** Định nghĩa một tập nhỏ các tầng, ví dụ nhanh, chuẩn, và nâng cao, và gán mỗi lớp tới tầng mà benchmark chứng minh là đủ. Với mỗi tầng, chọn một Model cụ thể hoặc một inference profile của Amazon Bedrock. Nơi định tuyến trong một họ là mục tiêu, [định tuyến prompt thông minh của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html) có thể thực hiện lựa chọn theo-yêu-cầu tự động. Với các tác vụ nặng-tài-liệu, cân nhắc [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html) như lựa chọn đúng thay vì một LLM thị giác đa-dụng.
- **Triển khai logic định tuyến điều phối yêu cầu tới Model được gán tại runtime:** Giải quyết ánh xạ lớp-tác-vụ-tới-Model ở đầu mỗi yêu cầu và phát lệnh gọi suy luận đối chiếu Model đã chọn. Khi vượt qua các nhà cung cấp hoặc họ Model, một trừu tượng framework như [các nhà cung cấp Model của Strands Agents](https://strandsagents.com/docs/user-guide/concepts/model-providers/) giữ mã định tuyến ổn định khi nhà cung cấp thay đổi bên dưới.
- **Cấu hình dự phòng theo tầng tới một Model có năng lực cao hơn cho đầu ra độ-tin-cậy-thấp hoặc thất bại:** Định nghĩa các tín hiệu có cấu trúc, điểm độ tin cậy dưới ngưỡng, lỗi xác thực lược đồ, lỗi phân tích cú pháp, hoặc một phản hồi không-hoàn-chỉnh tường minh, để leo thang yêu cầu cụ thể tới một Model có năng lực cao hơn. Giới hạn leo thang ở một bước duy nhất để latency đuôi vẫn dự đoán được, và ghi log cả quyết định chính lẫn dự phòng cho mỗi yêu cầu leo thang.
- **Đưa các phép gán Model và luật định tuyến ra ngoài dưới dạng cấu hình runtime:** Giữ các định danh Model, ánh xạ lớp-tác-vụ-tới-tầng, và luật dự phòng trong feature flags của [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) (hoặc một dịch vụ cấu hình tương đương) và đọc chúng tại thời điểm yêu cầu. Tách rời lựa chọn khỏi triển khai cho phép các Model mới được đánh giá, thăng cấp, hoặc rollback mà không cần deploy lại tác nhân.
- **Triển khai thay đổi Model một cách tiệm tiến với rollback tự động:** Dùng [các chiến lược triển khai AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-deployment-strategy-create.html) để dịch lưu lượng sang một Model mới theo từng bước với xác nhận thời-gian-ủ (bake-time), và gắn cảnh báo CloudWatch trên latency và chất lượng để thay đổi rollback tự động khi cảnh báo kích hoạt. Coi việc đổi Model như một triển khai được giám sát khiến các cập nhật Model thường xuyên trở nên an toàn.
- **Phát telemetry theo lớp-tác-vụ cho latency, token, chất lượng, và tỷ lệ dự phòng:** Công bố các chỉ số theo lớp để hiệu ứng của mỗi quyết định định tuyến hiển thị trên bảng điều khiển và có thể cảnh báo. Dùng [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html) cùng [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html) để quy latency, token, và điểm đánh giá về lớp và Model đã phục vụ mỗi yêu cầu.
- **Xem lại các quyết định định tuyến đối chiếu telemetry production theo nhịp định sẵn:** Lên lịch rà soát định kỳ các phân phối latency theo lớp, tỷ lệ leo-thang-dự-phòng, và điểm chất lượng, và chạy lại AgentCore Evaluations đối chiếu các Model mới ra mắt dùng cùng benchmark phân-phối-tác-vụ. Thăng cấp, hạ cấp, hoặc phân-tầng-lại các Model dựa trên dữ liệu quan sát được thay vì theo nhịp phát hành của nhà cung cấp.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF01-BP03 Phân tích latency tác nhân đầu-cuối và nhận diện mục tiêu tối ưu](../1-agentperf01/agentperf01-bp03.md)
- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](agentperf02-bp01.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](agentperf02-bp03.md)
- [AGENTPERF02-BP04 Tối ưu phản hồi streaming và time-to-first-token cho các tương tác tác nhân](agentperf02-bp04.md)

**Tài liệu liên quan:**

- [Hiểu về định tuyến prompt thông minh trong Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)
- [Đánh giá hiệu năng tác nhân với Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [AWS AppConfig là gì?](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
- [Tạo một chiến lược triển khai (AWS AppConfig)](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-deployment-strategy-create.html)
- [Khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)
- [Kinh tế cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/introduction.html)
- [Blog: Xây dựng tác nhân AI đáng tin cậy với Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [Strands Agents Model Providers](https://strandsagents.com/docs/user-guide/concepts/model-providers/)

**Video liên quan:**

- [AWS re:Invent 2025 - Làm chủ lựa chọn Model: Lợi thế 3 bước của Amazon Bedrock (AIM391)](https://www.youtube.com/watch?v=Vu91YwZxskY)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, Evaluations](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/07-AgentCore-evaluations)

**Workshop liên quan:**

- [Đào sâu vào Bedrock AgentCore, Evaluations](https://catalog.workshops.aws/agentcore-deep-dive/en-US/80-agentcore-evaluations)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS AppConfig](https://aws.amazon.com/systems-manager/features/appconfig/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
