---
title: "Cách hoạt động"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/optimization-how-it-works.html"
---
# Cách hoạt động

AgentCore optimization kết nối các phát hiện từ đánh giá (evaluation) với những cải thiện đã được kiểm chứng thông qua một chu trình có thể lặp lại. Một vòng lặp điển hình gồm các bước sau:

- **Sinh ra một khuyến nghị:** Trỏ Recommendations API vào các agent trace trong CloudWatch Logs và chỉ định evaluator bạn muốn tối ưu. Dịch vụ phân tích các mẫu lỗi (failure pattern) và trả về một system prompt đã tối ưu hoặc một tập các tool description, kèm theo giải thích về những gì đã thay đổi và lý do.

- **(Tùy chọn) Đóng gói thành một configuration bundle:** Tạo một phiên bản bundle với cấu hình được khuyến nghị. Một bundle là một ảnh chụp bất biến, có phiên bản của cấu hình một Agent (các system prompt, model ID, tool description) có thể được thay đổi động mà không cần triển khai code. Các configuration bundle hữu ích khi bạn muốn tách hành vi của Agent khỏi code; chúng không bắt buộc. Bạn cũng có thể kiểm chứng các thay đổi bằng cách triển khai lên một runtime endpoint riêng.

- **Kiểm chứng bằng một A/B test:** Chia lưu lượng production giữa Agent hiện tại (control) và phiên bản cải thiện (treatment) qua AgentCore Gateway. Online evaluation chấm điểm từng session và báo cáo kết quả kèm ý nghĩa thống kê (statistical significance). Các A/B test hỗ trợ hai mẫu:

  **Configuration bundle variants:** Cùng runtime, khác phiên bản bundle. Dùng khi thay đổi thuần túy là cấu hình (prompt, model ID, tool description).

- **Target-based variants:** Các gateway target khác nhau trỏ tới các runtime endpoint khác nhau. Dùng khi thay đổi bao gồm thay đổi code, nâng cấp framework, hoặc khi bạn muốn so sánh các hiện thực Agent hoàn toàn khác nhau. Mỗi variant có thể có cấu hình online evaluation riêng.

- **Triển khai variant thắng cuộc và lặp lại:** Định tuyến 100% lưu lượng đến variant thắng cuộc. Các trace mới từ baseline mới cung cấp nền tảng cho vòng lặp tiếp theo.
