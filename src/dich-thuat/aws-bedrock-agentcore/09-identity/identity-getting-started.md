---
title: "Bắt đầu với AgentCore Identity"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started.html"
---

# Bắt đầu với AgentCore Identity

Nếu bạn đang xây dựng các AI agent (tác tử AI) cần truy cập các dịch vụ bên ngoài như Google Drive, Slack hoặc GitHub, Amazon Bedrock AgentCore Identity (danh tính) cung cấp hạ tầng xác thực an toàn mà bạn cần. Phần này cung cấp hai hướng dẫn bắt đầu thực hành minh họa cách triển khai các tính năng danh tính trong agent của bạn. Tùy nhu cầu nghiệp vụ cụ thể, bạn có thể bắt đầu với một triển khai agent đầu cuối hoàn chỉnh, hoặc tập trung vào các mẫu tích hợp OAuth2 với Google Drive để hiểu các luồng xác thực cốt lõi.

###### Topics

- [Primary getting started tutorial](#primary-tutorial)

- [OAuth2 integration getting started tutorial](#additional-tutorial)

- [Common prerequisites](#common-prerequisites)

- [Build your first authenticated agent](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-cognito.html)

- [Integrate with Google Drive using OAuth2](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-google.html)

## Hướng dẫn bắt đầu chính

Bắt đầu tại đây để có hướng dẫn đầu cuối hoàn chỉnh về các tính năng của AgentCore Identity:

**Điểm khởi đầu được khuyến nghị** cho người dùng mới

**Những gì bạn sẽ xây dựng:** Một agent hoạt động hoàn chỉnh có xác thực, được triển khai lên AgentCore Runtime (môi trường chạy)

**Những gì bạn sẽ học:** Tạo Cognito user pool, cấu hình credential provider, triển khai agent, thiết lập chính sách IAM và kiểm thử các luồng xác thực

**Kết quả:** Agent được triển khai đầy đủ có thể xác thực người dùng và lấy access token

## Hướng dẫn bắt đầu tích hợp OAuth2

Sau khi hoàn thành hướng dẫn chính, khám phá các mẫu OAuth2 với các dịch vụ bên ngoài:

**Trọng tâm:** Các luồng OAuth2 và tích hợp Google Drive

**Những gì bạn sẽ học:** Thiết lập OAuth2 credential provider, lấy access token và tích hợp với các dịch vụ của Google

**Phù hợp nhất cho:** Hiểu các mẫu xác thực OAuth2 với các dịch vụ bên ngoài thực tế

## Điều kiện tiên quyết chung

Cả hai hướng dẫn đều yêu cầu những điều sau:

- Một tài khoản AWS với quyền phù hợp

- Quen thuộc cơ bản với lập trình Python

- Hiểu các khái niệm OAuth2 (khuyến nghị)

Mỗi hướng dẫn bao gồm các chỉ dẫn thiết lập cụ thể và các điều kiện tiên quyết bổ sung khi cần.
