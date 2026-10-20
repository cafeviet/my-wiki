---
title: "AgentCore Browser: tương tác với ứng dụng web"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser.html"
---

# Tương tác với ứng dụng web bằng Amazon Bedrock AgentCore Browser

Amazon Bedrock AgentCore Browser cung cấp một môi trường trình duyệt biệt lập, bảo mật để các agent (tác tử AI) của bạn tương tác với các ứng dụng web. Nó chạy trong một môi trường được container hóa, tách biệt hoạt động web khỏi hệ thống của bạn. Nó bao gồm các tính năng bảo mật như cô lập phiên (session isolation), khả năng quan sát (observability) tích hợp thông qua xem trực tiếp (live viewing), ghi log CloudTrail, và các năng lực phát lại phiên (session replay).

Amazon Bedrock AgentCore Browser cung cấp khả năng duyệt web theo phiên với khả năng quan sát toàn diện. Quy trình gồm bốn bước chính:

- **Tạo một Browser Tool**

         Bạn bắt đầu bằng việc tạo một Browser Tool để bật năng lực duyệt web cho agent của bạn nhằm tương tác với ứng dụng web, điền biểu mẫu, điều hướng website, và trích xuất thông tin trong một môi trường được quản lý hoàn toàn. Bạn có thể chọn giữa Browser do AWS quản lý (aws.browser.v1) để thiết lập nhanh, hoặc tạo một trình duyệt tùy chỉnh với các tính năng nâng cao như ghi phiên, cấu hình mạng tùy chỉnh, và các IAM execution role cụ thể.

- **Bắt đầu một phiên trình duyệt**

         Khởi chạy các phiên biệt lập với thời gian chờ (timeout) có thể cấu hình (mặc định: 15 phút, tối đa: 8 giờ). Chạy nhiều phiên đồng thời.

- **Tương tác với trình duyệt**

         Khi một phiên đã bắt đầu, bạn có thể tương tác với trình duyệt bằng các API streaming dựa trên WebSocket. Automation endpoint cho phép agent của bạn thực hiện các hành động trình duyệt như điều hướng tới website, nhấp vào phần tử, điền biểu mẫu, chụp ảnh màn hình, và nhiều hơn nữa. Các thư viện như Strands, Nova Act, hoặc Playwright có thể được dùng để đơn giản hóa các tương tác này. Trong khi đó, Live View endpoint cho phép người dùng cuối xem phiên trình duyệt theo thời gian thực và tương tác trực tiếp với nó thông qua luồng trực tiếp.

- **Giám sát và ghi phiên**

         Mọi phiên trình duyệt đều cung cấp khả năng quan sát tích hợp, bao gồm Live View để giám sát thời gian thực, Session recording (ghi phiên, có sẵn cho các trình duyệt tùy chỉnh), và các chỉ số CloudWatch để có thông tin hiệu năng theo thời gian thực. Session recording ghi lại các thay đổi DOM, hành động người dùng, log console, và sự kiện mạng. Các phiên đã ghi được lưu trong Amazon S3 bucket của bạn và có thể phát lại qua AWS Console để phân tích chi tiết, bao gồm phát lại video, điều hướng theo dòng thời gian, theo dõi hành động người dùng, và các log toàn diện phục vụ khắc phục sự cố và tối ưu hóa.

**Tại sao dùng trình duyệt từ xa cho việc phát triển agent?**

Một trình duyệt từ xa chạy trong một môi trường riêng biệt thay vì trên máy cục bộ. Đối với việc phát triển agent, trình duyệt từ xa cho phép các AI agent tương tác với web như con người vẫn làm. Các năng lực chính bao gồm:

- Điều hướng website, điền biểu mẫu, nhấp nút, phân tích nội dung động

- Hạ tầng serverless tự động mở rộng quy mô

- Hiểu trực quan thông qua ảnh chụp màn hình

- Can thiệp của con người với chế độ xem tương tác trực tiếp

- Cô lập phiên để bảo mật

- Điều hướng ứng dụng web phức tạp

- Các năng lực kiểm toán toàn diện

**Tính năng bảo mật**

Browser Tool bao gồm một số tính năng bảo mật giúp bảo vệ môi trường của bạn:

- Cô lập: Môi trường được container hóa, tách biệt khỏi hệ thống của bạn

- Phiên tạm thời (ephemeral): Các phiên tạm thời được đặt lại sau mỗi lần dùng

- Tự động chấm dứt khi time-to-live hết hạn

## Chủ đề

- [Bắt đầu với AgentCore Browser](/dich-thuat/aws-bedrock-agentcore/12-browser/browser-quickstart)

- [Kiến thức nền tảng](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-resource-session-management.html)

- [Khả năng quan sát](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-observability.html)

- [Tính năng](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-features.html)

- [Cấu hình hệ thống tệp cho AgentCore Browser](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-filesystem-configurations.html)

- [Khắc phục sự cố AgentCore Browser](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool-troubleshooting.html)
