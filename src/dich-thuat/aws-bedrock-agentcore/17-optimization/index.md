---
title: "AgentCore optimization"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/optimization.html"
---

# AgentCore optimization

# AgentCore optimization: Cải thiện vòng lặp chất lượng agent bằng recommendation và A/B test

Amazon Bedrock AgentCore optimization cung cấp các công cụ để liên tục cải thiện hiệu năng agent (tác tử AI) của bạn thông qua các thay đổi cấu hình dựa trên dữ liệu. Thay vì viết lại prompt thủ công và kiểm thử bằng tay, bạn sử dụng các agent trace để tạo ra các cải tiến và xác nhận chúng bằng các thí nghiệm có kiểm soát.

AgentCore optimization được xây dựng trên nền [AgentCore Evaluations](/dich-thuat/aws-bedrock-agentcore/16-evaluations/) và giới thiệu ba khả năng:

- **Recommendations (khuyến nghị):** Các cải tiến do AI tạo ra cho system prompt và tool description dựa trên các agent trace thực tế và một evaluator mục tiêu. Dịch vụ phân tích các mẫu lỗi dựa trên evaluator mục tiêu và tạo ra một biến thể (variant) đã được tối ưu của system prompt hoặc tool description.

- **Configuration bundles (gói cấu hình):** Các bản chụp (snapshot) có phiên bản, bất biến của cấu hình agent (system prompt, model ID, tool description) tách rời hành vi agent khỏi mã, cho phép thay đổi hành vi mà không cần redeploy. Configuration bundle là tùy chọn; bạn cũng có thể xác nhận các thay đổi bằng cách deploy tới một runtime endpoint riêng.

- **A/B testing:** Chia lưu lượng có kiểm soát giữa hai biến thể thông qua AgentCore Gateway (cổng), với việc chấm điểm đánh giá online cho mỗi session và báo cáo mức ý nghĩa thống kê. Các biến thể có thể là các phiên bản configuration bundle khác nhau trên cùng một runtime, hoặc các gateway target khác nhau trỏ tới các runtime endpoint khác nhau.

Cùng nhau, các khả năng này tạo thành một vòng lặp cải tiến liên tục:

###### Các chủ đề

- [Cách hoạt động](/dich-thuat/aws-bedrock-agentcore/17-optimization/optimization-how-it-works)

- [Điều kiện tiên quyết](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/optimization-prereqs.html)

- [Configuration bundles](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/configuration-bundles.html)

- [Recommendations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/optimization-recommendations.html)

- [A/B testing](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/ab-testing.html)

- [AgentCore insights: Phân loại (triage) lỗi agent bằng phân tích mẫu](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/insights.html)
