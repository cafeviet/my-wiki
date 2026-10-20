# AGENTOPS06-BP02 Đánh giá và theo dõi hiệu năng agent liên tục

Đánh giá trước triển khai kiểm định rằng một agent đã sẵn sàng để đưa ra. Đánh giá sau triển khai kiểm định rằng nó vẫn hoạt động. Không có đánh giá liên tục, sự suy giảm chất lượng dần dần từ trôi lệch dữ liệu, cập nhật Model, và các mẫu người dùng thay đổi sẽ không được chú ý cho đến khi việc khắc phục trở nên tốn kém.

**Kết quả mong muốn:**

- Hiệu năng agent được đánh giá liên tục so với các mốc chuẩn chất lượng được xác định.
- Các pipeline tự động phát hiện suy giảm về chất lượng đầu ra, độ chính xác suy luận, và sự phù hợp với kết quả kinh doanh.
- Các nhóm có tầm nhìn rõ ràng vào các xu hướng hiệu năng theo thời gian và có thể tương quan các thay đổi chất lượng với các cập nhật cấu hình, Model, hoặc dữ liệu cụ thể.
- Các kết quả đánh giá dẫn dắt các hành động cải tiến được ưu tiên và cung cấp bằng chứng khách quan cho việc báo cáo tới các bên liên quan.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ đánh giá hiệu năng agent tại thời điểm triển khai mà không có đánh giá sau triển khai liên tục, bỏ lỡ suy giảm dần dần từ trôi lệch dữ liệu, cập nhật Model, hoặc các mẫu người dùng thay đổi.
- Chỉ dựa hoàn toàn vào các chỉ số tự động mà không có đánh giá định kỳ của con người, bỏ lỡ các chiều chất lượng mà các chỉ số tự động không thể nắm bắt trọn vẹn (như sắc thái, tính phù hợp, và sự bám sát ngữ cảnh kinh doanh).
- Dùng các tiêu chí đánh giá chung cho mọi agent mà không tùy biến các chỉ số theo trường hợp sử dụng và mục tiêu kinh doanh cụ thể của mỗi agent, tạo ra các kết quả đánh giá không phản ánh giá trị thực tế.
- Xem đánh giá như tách rời khỏi vận hành thay vì tích hợp nó vào luồng công việc vận hành, tạo ra "nợ đánh giá" tích tụ theo thời gian.

**Lợi ích khi áp dụng thực hành tốt này:**

- Đánh giá liên tục cung cấp nền tảng thực nghiệm cho cải tiến dựa trên bằng chứng, xác định agent nào cần chú ý và thay đổi nào tạo ra lợi ích đo lường được.
- Theo dõi xu hướng hiệu năng bộc lộ các mẫu cung cấp thông tin cho cải tiến có hệ thống, biến dữ liệu đánh giá thành các insight thực tế.
- Chấm điểm đa chiều bắt được các vấn đề chất lượng mà một chỉ số đơn lẻ sẽ bỏ lỡ.
- Tương quan giữa các dịch chuyển chất lượng và các thay đổi cấu hình nén phân tích nguyên nhân gốc.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) là một dịch vụ đánh giá cho việc đánh giá liên tục. Chế độ theo yêu cầu (on-demand) của nó chạy các mốc chuẩn trong quá trình phát triển, và chế độ trực tuyến (online) của nó lấy mẫu và đánh giá các tương tác trực tiếp trong sản xuất mà không yêu cầu kích hoạt thủ công. Mười ba bộ đánh giá dựng sẵn bao phủ tính đúng đắn, tính hữu ích, tính an toàn, và độ chính xác lựa chọn Tools, với các bộ đánh giá tùy chỉnh sẵn có cho các yêu cầu đặc thù kinh doanh. [Amazon Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) bổ sung điều này bằng đánh giá ở cấp Model, và đánh giá định kỳ của con người bao phủ các chiều mà các chỉ số tự động bỏ lỡ.

Các khung đánh giá cần nhiều chiều vì một chỉ số đơn lẻ bỏ lỡ quá nhiều. Ví dụ:

- Chất lượng đầu ra (độ liên quan, độ chính xác, tính mạch lạc) đo liệu các phản hồi có tốt hay không.
- An toàn (tỷ lệ ảo giác, tính độc hại, sự bám sát Guardrails) đo liệu các phản hồi có an toàn hay không.
- Hiệu quả (tỷ lệ hoàn thành tác vụ, thành công gọi Tools) đo liệu agent có tiết kiệm hay không.
- Sự phù hợp kinh doanh (đạt được kết quả, mức độ hài lòng của người dùng, mức tuân thủ SLA) đo liệu agent có mang lại giá trị hay không.

Trọng số phụ thuộc vào trường hợp sử dụng. Chẳng hạn, một agent hỗ trợ khách hàng có thể gán trọng số cho mức độ hài lòng cao hơn hiệu quả, trong khi một agent tự động hóa nội bộ có thể gán trọng số cho hiệu quả cao hơn độ liên quan. Trọng số chung tạo ra kết quả chung chung.

Các dashboard hiển thị các điểm đánh giá theo thời gian khiến suy giảm trở nên thấy được trước khi nó trở thành sự cố. Cảnh báo trên các vi phạm ngưỡng và trên các xu hướng âm dai dẳng, trái với các sụt giảm đơn điểm, bắt được các vấn đề chậm chạp vốn khó chẩn đoán nhất sau khi đã xảy ra. Hãy tương quan các dịch chuyển đánh giá với các thay đổi cấu hình và Model để việc quy kết nhanh chóng khi một chỉ số dịch chuyển.

Các mẫu LLM-as-a-Judge có thể dùng nhiều Prompt đánh giá bao phủ các chiều chất lượng khác nhau để tạo ra một điểm tổng hợp đáng tin cậy hơn bất kỳ Prompt đơn lẻ nào. Rà soát định kỳ của con người kiểm định các điểm số tự động và bắt được các điểm mù.

### Các bước triển khai

- **Cấu hình [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html):** Dùng chế độ theo yêu cầu cho việc lập mốc chuẩn trong phát triển và chế độ trực tuyến cho giám sát sản xuất liên tục.
- **Định nghĩa một khung đánh giá đa chiều:** Áp dụng trọng số đặc thù cho trường hợp sử dụng trên các chiều chất lượng, an toàn, hiệu quả, và sự phù hợp kinh doanh.
- **Triển khai các mẫu LLM-as-judge:** Dùng nhiều Prompt đánh giá và bổ sung bằng đánh giá định kỳ của con người.
- **Xây dựng các dashboard đánh giá:** Hiển thị các xu hướng theo thời gian với cảnh báo cho các vi phạm ngưỡng và các xu hướng âm dai dẳng.
- **Tương quan các kết quả đánh giá với các sự kiện thay đổi:** Gắn thẻ các triển khai, cập nhật cấu hình, và thay đổi Model để các dịch chuyển chất lượng có thể được quy kết nhanh chóng.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS06-BP01 Thiết kế các khung kiểm thử đa lớp](agentops06-bp01.md)
- [AGENTOPS06-BP03 Thiết lập kiểm định do SME dẫn dắt và các luồng phê duyệt kinh doanh](agentops06-bp03.md)
- [AGENTOPS02-BP04 Duy trì các vòng lặp điều khiển phản hồi cho cải tiến liên tục](../2-agentops02/agentops02-bp04.md)
- [AGENTOPS05-BP04 Định nghĩa và theo dõi KPI cho các luồng công việc agent](../5-agentops05/agentops05-bp04.md)
- [AGENTPERF01-BP01 Định nghĩa tiêu chí thành công phù hợp với hiệu năng cho workload agent](../../4-performance-efficiency/1-agentperf01/agentperf01-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Evaluate models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html)
- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Build reliable AI agents with Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [LLM-as-a-judge on Amazon Bedrock Model Evaluation](https://aws.amazon.com/blogs/machine-learning/llm-as-a-judge-on-amazon-bedrock-model-evaluation/)
- [Evaluating AI agents for production: A practical guide to Strands Evals](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/)
- [From AI agent prototype to product: Lessons from building AWS DevOps Agent](https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent)

**Workshop liên quan:**

- [Getting started with Amazon Bedrock AgentCore, Lab 5: Evaluate Agent Performance](https://catalog.workshops.aws/agentcore-getting-started/en-US/65-evaluation)
- [Diving Deep into Bedrock AgentCore, Evaluations](https://catalog.workshops.aws/agentcore-deep-dive/en-US/80-agentcore-evaluations)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
