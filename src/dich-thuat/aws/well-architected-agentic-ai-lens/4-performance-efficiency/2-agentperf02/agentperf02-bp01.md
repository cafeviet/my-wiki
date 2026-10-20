# AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả

Mỗi vòng lặp của vòng lặp nhận-thức–suy-luận–hành-động thường liên quan đến một lệnh gọi suy luận LLM, nên số vòng lặp một tác nhân thực hiện nhân lên cả **latency** lẫn chi phí. Một pipeline hiệu quả đạt được các quyết định chính xác trong số vòng lặp ít nhất mà tác vụ đòi hỏi, dùng giới hạn vòng lặp có ràng buộc và kết thúc sớm dựa-trên-độ-tin-cậy để giúp ngăn các vòng lặp mất kiểm soát, và xử lý thử lại (retry) trong ngân sách hiệu năng tường minh thay vì âm thầm bào mòn chúng.

**Kết quả mong muốn:**

- Bạn có giới hạn vòng lặp theo tác vụ và kết thúc sớm dựa-trên-độ-tin-cậy được cấu hình, để các vòng lặp suy luận không thể chạy vô giới hạn.
- Bạn có các hình dạng pipeline mở rộng độ sâu suy luận theo độ phức tạp tác vụ, với tác vụ đơn giản giải quyết trong một hoặc hai vòng lặp và tác vụ phức tạp nhận số vòng lặp cần thiết.
- Bạn có các chiến lược thử lại bị giới hạn bởi ngân sách latency tường minh, với việc tái-prompt ngữ nghĩa (semantic re-prompting) hoặc suy giảm nhẹ nhàng được kích hoạt trước khi SLO đầu-cuối bị vượt.
- Bạn có số vòng lặp suy luận trung bình mỗi tác vụ được theo dõi như một KPI hạng nhất, hiển thị cạnh các chỉ số latency và token.

**Các phản mẫu thường gặp (anti-patterns):**

- Cho phép các tác nhân suy luận vô hạn mà không có giới hạn vòng lặp hay điều kiện kết thúc sớm, tạo ra các vòng lặp mất kiểm soát tiêu tốn token và thời gian mà không cải thiện chất lượng đầu ra.
- Thiết kế các pipeline suy luận luôn thực thi cùng một chuỗi bước bất kể độ phức tạp tác vụ, áp suy luận hạng nặng lên các tác vụ đơn giản vốn có thể giải quyết bằng một lệnh gọi suy luận duy nhất.
- Thiết kế các chiến lược thử lại không có ngân sách hiệu năng, nên các lần thử lại lùi theo cấp số nhân (exponential backoff) tích lũy latency vượt quá SLO đầu-cuối trong khi tái-prompt ngữ nghĩa hoặc suy giảm nhẹ nhàng sẽ bảo toàn được các mục tiêu hiệu năng.
- Thử lại một lệnh gọi LLM thất bại với prompt và Model giống hệt, thay vì tái-prompt ngữ nghĩa, diễn đạt lại chỉ dẫn, đơn giản hóa tác vụ, hoặc dự phòng sang một Model có năng lực cao hơn, để tăng khả năng lần thử lại thành công trong ngân sách latency còn lại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thiết kế pipeline hiệu quả giảm số lệnh gọi suy luận LLM mỗi tác vụ, vốn là một trong những tối ưu tác động cao nhất cho latency và chi phí tác nhân.
- Hình dạng pipeline thích ứng khiến các tác vụ đơn giản giải quyết nhanh trong khi các tác vụ phức tạp nhận số vòng lặp cần thiết.
- Ngân sách thử lại tường minh và tái-prompt ngữ nghĩa giữ latency đuôi trong SLO ngay cả khi một lệnh gọi Tools hoặc Model thất bại ở lần thử đầu.
- Trần vòng lặp tạo ra các phân phối latency chặt hơn giúp đơn giản hóa lập kế hoạch dung lượng, ngưỡng auto scaling, và dự báo chi phí.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Tổng latency và mức tiêu token tỉ lệ theo số vòng lặp mà pipeline thực hiện để đạt một đầu ra được chấp nhận, nên thiết kế pipeline, cách cấu trúc vòng lặp, khi nào nó kết thúc, và cách xử lý lỗi có hiệu ứng nhân lên trên cả latency lẫn chi phí. Một pipeline được thiết kế tốt đạt được đầu ra được chấp nhận trong số vòng lặp ít nhất mà tác vụ thực sự đòi hỏi.

Hình dạng pipeline đúng phụ thuộc vào độ phức tạp và tính dự đoán được của tác vụ. [Các tác nhân suy luận cơ bản](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/basic-reasoning-agents.html) xử lý phân loại, trích xuất, hoặc tóm tắt đơn-lượt trong một lệnh gọi suy luận và không nên bị bọc trong các vòng lặp suy luận lặp đi lặp lại. [Các vòng lặp kiểu ReAct](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html), trong đó tác nhân đan xen suy luận, gọi Tools, và quan sát, phù hợp các tác vụ mở nơi bước tiếp theo không thể dự đoán tại thời điểm thiết kế.

Các hình dạng lập-kế-hoạch-rồi-thực-thi như ReWOO và các lai plan-and-solve tách kế hoạch khỏi thực thi và giới hạn vòng lặp theo độ dài kế hoạch thay vì theo sự sẵn lòng tiếp tục lặp của Model, và các hình dạng phản-ánh-rồi-sửa như Reflexion đưa vào các chu kỳ phê bình tường minh với trần cứng cho số lượt sửa. Cả hai mẫu được mô tả trong [Tùy biến luồng công việc tác nhân với kỹ thuật điều phối nâng cao dùng Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/).

Trần vòng lặp và kết thúc sớm là hai công cụ kiểm soát giữ cho một vòng lặp không tiêu tốn tài nguyên mà không tạo ra giá trị, và chúng đóng các vai bổ trợ. Một trần vòng lặp theo tác vụ là một cận trên giúp ngăn tình trạng mất-kiểm-soát bệnh lý (một Model cứ gọi Tools mà không hội tụ), và nó phải được đặt theo từng lớp tác vụ vì một trần phù hợp cho nghiên cứu nhiều-bước lại lãng phí cho một tra cứu đơn giản.

Kết thúc sớm dừng vòng lặp trước trần khi thêm vòng lặp sẽ không cải thiện đầu ra. Ví dụ, khi một bước phê bình trả về tín hiệu có cấu trúc "không cần sửa thêm", khi tự-đánh-giá độ tin cậy của tác nhân vượt một ngưỡng, hoặc khi một trình xác thực xác định (kiểm tra lược đồ, kiểm tra căn cứ, kiểm tra chính sách) xác nhận đầu ra là chấp nhận được.

Cùng nhau, trần giúp ngăn trường hợp xấu nhất trong khi kết thúc loại bỏ trường hợp phổ biến là trả phí cho các vòng lặp không cần thiết.

Phục hồi lỗi là một phần của ngân sách latency, không phải ngoại lệ với nó. Khi một lệnh gọi Tools hoặc suy luận Model thất bại, exponential backoff ngây thơ có thể tiêu tốn nhiều thời gian hơn mục tiêu đầu-cuối cho phép. Mọi chiến lược thử lại nên bị giới hạn bởi một ngân sách hiệu năng tường minh chỉ định bao nhiêu latency và bao nhiêu token mà các lần thử lại có thể tiêu trước khi pipeline dự phòng sang một phản hồi suy giảm.

Các lần thử lại giống hệt đối chiếu cùng prompt và Model thường thất bại vì cùng lý do:

- Tái-prompt ngữ nghĩa (diễn đạt lại chỉ dẫn, đơn giản hóa tác vụ, hoặc siết hợp đồng đầu ra)
- Leo thang Model (định tuyến lần thử lại tới một Model có năng lực cao hơn)
- Thay thế Tools (dùng một nguồn dữ liệu thay thế)

Mỗi cái trong số này thay đổi một biến trong chế độ lỗi và tăng khả năng lần thử lại thành công trong ngân sách còn lại. Để bảo toàn lòng tin người dùng, hãy triển khai các chiến lược như suy giảm nhẹ nhàng, trả về một câu trả lời một phần với các khoảng trống được đánh dấu, một câu trả lời độ-tin-cậy-thấp với sự bất định tường minh, hoặc một phản hồi "không thể hoàn thành" rõ ràng trước khi mục tiêu latency bị vượt.

Số vòng lặp suy luận trung bình mỗi tác vụ thuộc về cạnh latency, token, và chi phí như một KPI hiệu năng hạng nhất. Đó là tín hiệu sớm nhất rằng hình dạng pipeline, chất lượng prompt, hoặc độ tin cậy Tools thượng nguồn đã trôi dạt, vì số vòng lặp tăng thường đi trước một hồi quy latency hoặc chi phí. Mỗi vòng lặp thừa cộng dồn với các vòng lặp khác ở hạ nguồn trước khi chỉ số hướng-người-dùng dịch chuyển đủ để kích hoạt cảnh báo.

Được theo dõi theo lớp tác vụ và theo hình dạng pipeline, số vòng lặp cũng phơi bày các tác vụ bị định tuyến sai như yêu cầu đơn giản chạy qua các vòng lặp hạng nặng hoặc tác vụ phức tạp bị chặn trần trước khi hội tụ. Cả hai mẫu này đều vô hình với các chỉ số chỉ đo kết quả cuối.

### Các bước triển khai

- **Phân loại mỗi tác vụ tác nhân theo độ phức tạp suy luận:** Nhóm các tác vụ theo độ sâu suy luận chúng đòi hỏi, trích xuất hay phân loại đơn-bước, suy luận nhiều-bước qua các bước đã biết, và điều tra mở nơi đường đi không thể biết trước. Dùng phân loại này làm đầu vào cho việc chọn hình dạng pipeline và ngân sách vòng lặp, vì áp cùng hình dạng và ngân sách cho mọi lớp hoặc lãng phí vòng lặp trên công việc đơn giản hoặc suy luận thiếu trên công việc phức tạp. Ghi tài liệu phân loại cùng tiêu chí thành công của khối công việc để các quyết định định tuyến có thể được kiểm toán và xem lại khi phân phối tác vụ thay đổi.
- **Chọn một hình dạng pipeline khớp với mỗi lớp tác vụ:** Ánh xạ mỗi lớp tới một mẫu suy luận được ghi tài liệu trong [Các mẫu và luồng công việc AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html), một [mẫu suy luận cơ bản](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/basic-reasoning-agents.html) cho tác vụ đơn-bước, một [vòng lặp ReAct](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html) cho suy luận mở nơi việc dùng Tools dẫn dắt bước tiếp theo, và một hình dạng lập-kế-hoạch-rồi-thực-thi hoặc phản-ánh-rồi-sửa cho các tác vụ hưởng lợi từ một trình lập kế hoạch hoặc giai đoạn phê bình tường minh như mô tả trong [Tùy biến luồng công việc tác nhân với kỹ thuật điều phối nâng cao dùng Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/). Tránh bọc các tác vụ đơn-bước trong các vòng lặp lặp đi lặp lại, điều đó thổi phồng chi phí và latency mà không có lợi về độ chính xác.
- **Đặt trần vòng lặp theo tác vụ có kích thước theo lớp phức tạp:** Cấu hình một cực đại cứng cho số vòng lặp suy luận cho mỗi lớp tác vụ dùng nguyên hàm kiểm-soát-vòng-lặp mà framework tác nhân đang dùng phơi bày, và định cỡ trần ở một giá trị mà khối công việc chỉ chạm tới trong các trường hợp bệnh lý. Trần là một sàn cho trường hợp xấu nhất, các tác vụ hội tụ sớm vẫn kết thúc sớm qua các tín hiệu độ tin cậy cấu hình ở bước tiếp, nên tinh chỉnh trần theo biến thể phức tạp nhất của mỗi lớp thay vì theo trường hợp điển hình.
- **Định nghĩa điều kiện kết thúc sớm để vòng lặp dừng khi các vòng lặp ngừng thêm giá trị:** Chỉ định các tín hiệu có cấu trúc kết thúc vòng lặp trước trần, một bước phê bình trả về cờ boolean "cần sửa", một điểm độ tin cậy vượt một ngưỡng định sẵn, hoặc một trình xác thực xác định (kiểm tra lược đồ, căn cứ, hoặc chính sách) xác nhận đầu ra chấp nhận được. Coi các tín hiệu này là dữ liệu mà pipeline tạo ra và ghi log, không phải hành vi Model ngầm định, để các quyết định kết thúc có thể quan sát và kiểm toán được thay vì ẩn bên trong một chuỗi suy nghĩ.
- **Thiết lập một ngân sách thử lại bị giới hạn bởi mục tiêu latency đầu-cuối:** Phân bổ một phần tường minh của mục tiêu latency đầu-cuối cho việc xử lý thử lại và cưỡng chế nó ở cấp pipeline để các lần thử lại tích lũy không thể âm thầm vượt mục tiêu. Phân rã ngân sách thành thành phần latency và token, vì một lần thử lại ở trong ngân sách latency nhưng tăng gấp ba mức tiêu token vẫn làm suy giảm kinh tế đơn vị. Căn chỉnh ngân sách với mục tiêu mức dịch vụ mà khối công việc bị chấm điểm để hành vi thử lại được đo đối chiếu cùng mục tiêu như mọi thứ khác trong pipeline.
- **Thay thế các lần thử lại giống hệt bằng tái-prompt ngữ nghĩa, leo thang Model, hoặc thay thế Tools:** Khi một lệnh gọi thất bại, thử lại với một chỉ dẫn diễn đạt lại, một phân rã tác vụ đơn giản hơn, một Model có năng lực cao hơn, hoặc một Tool thay thế, mỗi cái thay đổi một biến trong chế độ lỗi thay vì lặp lại cùng lệnh gọi thất bại. Chọn cách thay thế dựa trên tín hiệu lỗi: timeout gợi ý leo thang Model hoặc thay thế Tools, lỗi phân tích cú pháp gợi ý tái-prompt với hợp đồng đầu ra chặt hơn, và lỗi căn cứ gợi ý mở rộng truy xuất.
- **Cấu hình các đường suy giảm nhẹ nhàng trả về trước khi mục tiêu bị vượt:** Định nghĩa phản hồi dự phòng cho mỗi lớp tác vụ, một câu trả lời một phần với các khoảng trống được đánh dấu, một câu trả lời độ-tin-cậy-thấp với sự bất định tường minh, hoặc một phản hồi "không thể hoàn thành" rõ ràng, và kích hoạt dự phòng khi ngân sách thử lại cạn kiệt hoặc khi ngân sách latency nằm trong biên an toàn được cấu hình so với mức bị vượt. Hành vi đuôi có thể dự đoán và một phản hồi lỗi rõ ràng bảo toàn lòng tin người dùng tốt hơn việc tối đa hóa khả năng thành công cuối cùng trên mọi yêu cầu.
- **Phát số vòng lặp suy luận, thử lại, và kết thúc dưới dạng telemetry hạng nhất:** Công bố số vòng lặp, nguyên nhân kết thúc (kết thúc sớm, chạm trần, cạn ngân sách thử lại, suy giảm nhẹ nhàng), và số lần thử lại cho mọi lần gọi dưới dạng chỉ số có thể đặt ngưỡng và cảnh báo cạnh các chỉ số latency và token dùng một khả năng như [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html) hoặc một pipeline tương đương trên runtime của tác nhân. Đặt số vòng lặp trung bình mỗi tác vụ trên cùng bảng điều khiển với các phân vị latency và chi phí mỗi lần hoàn thành, vì đó là chỉ báo sớm nhất rằng hình dạng pipeline, chất lượng prompt, hoặc độ tin cậy Tools đã trôi dạt.
- **Xem lại hình dạng pipeline, trần, và ngân sách đối chiếu telemetry production theo nhịp định sẵn:** Lên lịch rà soát định kỳ các phân phối vòng lặp, tỷ lệ kết-thúc-sớm, mức tiêu ngân sách thử lại, và tần suất suy giảm để các tham số pipeline bám theo hành vi thực chứ không phải giả định tại thời điểm ra mắt. Siết các trần bị dùng thiếu một cách nhất quán, nới các trần đang bị chạm trên các tác vụ phức tạp chính đáng, và phân loại lại các tác vụ mà phân phối vòng lặp cho thấy chúng thuộc một lớp phức tạp khác với lớp được gán ban đầu.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF02-BP02 Triển khai chiến lược lựa chọn Model phù hợp tác vụ](agentperf02-bp02.md)
- [AGENTPERF02-BP03 Tối ưu đường thực thi tác nhân để giảm latency](agentperf02-bp03.md)
- [AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt](../3-agentperf03/agentperf03-bp02.md)

**Tài liệu liên quan:**

- [Blog: Tùy biến luồng công việc tác nhân với kỹ thuật điều phối nâng cao dùng Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [Agentic AI - Generative AI Lens (Well-Architected Framework)](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)
- [Khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
