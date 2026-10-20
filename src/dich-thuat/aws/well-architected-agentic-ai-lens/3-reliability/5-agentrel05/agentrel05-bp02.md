# AGENTREL05-BP02 Tạo điều kiện cho thích ứng đáng tin cậy qua các chu kỳ cải tiến dẫn dắt bởi kiểm định

Các tác nhân suy giảm âm thầm khi không ai theo dõi, và việc tự sửa đổi lúc chạy dựa trên phản hồi nhiễu làm mọi thứ tệ hơn. Thu thập phản hồi có cấu trúc cùng kiểm định ngoại tuyến và các bản triển khai đã được kiểm định giữ cho việc thích ứng đáng tin cậy vì mọi thay đổi đều được đo lường trước khi tới người dùng.

**Kết quả mong muốn:**

- Bạn thu thập các tín hiệu phản hồi cấp hành động, cấp tác vụ và cấp phiên trên mỗi tương tác của tác nhân.
- Bạn chạy các bản kiểm định tự động và kiểm định LLM-làm-trọng-tài (LLM-as-a-judge) định kỳ, so sánh hành vi hiện tại với các ví dụ golden-path.
- Bạn kiểm định các thay đổi prompt và cấu hình ngoại tuyến trước khi triển khai thông qua triển khai từ từ.

**Các phản mẫu thường gặp (anti-patterns):**

- Triển khai các tác nhân mà không thu thập phản hồi, bỏ lỡ cơ hội nhận diện các lỗi hệ thống.
- Áp dụng các thay đổi hành vi tự động lúc chạy mà không kiểm định ngoại tuyến, gánh rủi ro thoái lui từ phản hồi nhiễu.
- Bỏ qua giám sát bản thân vòng lặp phản hồi, nên các lỗi âm thầm của đường ống chặn việc thích ứng diễn ra.

**Lợi ích khi áp dụng thực hành tốt này:**

- Chất lượng thực thi tác vụ cải thiện đều đặn thông qua thu thập phản hồi có cấu trúc và các điều chỉnh đã được kiểm định.
- Các lỗi hệ thống được nhận diện và sửa chữa nhanh hơn vì phân tích tự động bắt các mẫu mà con người bỏ lỡ.
- Can thiệp thủ công giảm vì tối ưu prompt dẫn dắt bởi kiểm định với triển khai có kiểm soát thay thế việc tinh chỉnh thủ công.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Phản hồi chỉ hữu ích ở mức chi tiết mà bạn thu thập nó. Ba tầng bao phủ hầu hết tín hiệu. Cấp hành động bắt liệu một lời gọi công cụ có thành công không, cấp tác vụ bắt liệu tác nhân có hoàn thành tác vụ đúng không, và cấp phiên bắt liệu tương tác có đạt mục tiêu của người dùng không. Phản hồi cấp hành động thường đến từ các bộ kiểm định tự động so sánh đầu ra với các lược đồ kỳ vọng. Phản hồi cấp tác vụ có thể tự động hóa cho các tiêu chí thành công tất định và cần LLM-làm-trọng-tài cho các chiều chất lượng chủ quan. Phản hồi cấp phiên thường đến từ người dùng, hoặc trực tiếp hoặc qua các tín hiệu hành vi như các câu hỏi tiếp theo.

[Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) chạy các bản đánh giá chất lượng định kỳ so với các tập tác vụ đại diện, so sánh đầu ra với các ví dụ golden-path và gắn cờ các thoái lui. Lưu kết quả kiểm định bên cạnh các bản ghi tác vụ để hiệu suất của tác nhân theo thời gian trở thành một tập dữ liệu đã gán nhãn mà bạn có thể truy vấn. Khi các bản kiểm định chỉ ra sự suy giảm hệ thống, đó là tín hiệu để kích hoạt một luồng tối ưu prompt ngoại tuyến, kiểm thử các cách diễn đạt khác so với các chuẩn kiểm định và triển khai phiên bản hiệu suất cao nhất thông qua triển khai từ từ.

Kỷ luật giữ cho điều này đáng tin cậy là "kiểm định trước khi triển khai, không sửa đổi lúc chạy". Tự sửa đổi lúc chạy hấp dẫn vì nó tạo ra phản hồi nhanh hơn, nhưng phản hồi nhiễu có thể đẩy các tác nhân vào hành vi tệ hơn. Phạm vi ảnh hưởng của một bản tự cập nhật tồi là toàn bộ đội vận hành. Kiểm định ngoại tuyến với triển khai từ từ giữ các cải tiến trong tầm kiểm soát. Giám sát sức khỏe vòng lặp phản hồi qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). Theo dõi tỷ lệ thu thập, độ trễ xử lý và tần suất kiểm định, với các cảnh báo khi các lỗi đường ống chặn chu kỳ cải tiến hoạt động.

### Các bước triển khai

- **Triển khai thu thập phản hồi đa tầng:** Bắt các tín hiệu cấp hành động, cấp tác vụ và cấp phiên cho mỗi tương tác.
- **Triển khai các bộ kiểm định kết quả tự động cho các tiêu chí tất định:** So sánh đầu ra với các lược đồ kỳ vọng khi các tiêu chí thành công không mơ hồ.
- **Dùng AgentCore Evaluations với LLM-làm-trọng-tài cho chất lượng chủ quan:** Chạy [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) theo một lịch định kỳ so với các ví dụ golden-path.
- **Kích hoạt tối ưu prompt ngoại tuyến khi các bản kiểm định cho thấy suy giảm:** Kiểm định các ứng viên so với các chuẩn ngoại tuyến, rồi triển khai thông qua triển khai từ từ thay vì tự sửa đổi lúc chạy.
- **Giám sát sức khỏe vòng lặp phản hồi:** Theo dõi tỷ lệ thu thập, độ trễ xử lý và tần suất kiểm định qua [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) với các cảnh báo cho các lỗi đường ống.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTREL02-BP03 Triển khai phát hiện và giám sát bất thường hành vi](../2-agentrel02/agentrel02-bp03.md)
- [AGENTREL05-BP01 Thiết kế các thành phần suy luận của tác nhân mô-đun, chịu lỗi](agentrel05-bp01.md)
- [AGENTREL05-BP03 Đặt nền nhận thức của tác nhân trên thông tin thực](agentrel05-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [Evaluate models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html)
- [Build reliable AI agents with Amazon Bedrock AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/)
- [Evaluating AI agents: Real-world lessons from building agentic systems at Amazon](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)

**Video liên quan:**

- [AWS re:Invent 2024 - Using Strands Agents to build autonomous, self-improving AI agents (AIM426)](https://www.youtube.com/watch?v=RQfW7eQsXqk)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
