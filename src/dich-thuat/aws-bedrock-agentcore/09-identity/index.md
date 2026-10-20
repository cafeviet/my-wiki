---
title: "AgentCore Identity: Quản lý danh tính cho các ứng dụng agent"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html"
---

# Cung cấp quản lý danh tính và thông tin xác thực cho các ứng dụng agent với Amazon Bedrock AgentCore Identity

Amazon Bedrock AgentCore Identity (danh tính) là một dịch vụ quản lý danh tính và thông tin xác thực (credential) được thiết kế riêng cho các AI agent (tác tử AI) và các workload tự động. Dịch vụ cung cấp các năng lực xác thực, ủy quyền và quản lý thông tin xác thực bảo mật, cho phép các agent và tool (công cụ) truy cập tài nguyên AWS và dịch vụ bên thứ ba thay mặt cho người dùng, đồng thời giúp duy trì các kiểm soát bảo mật nghiêm ngặt và các dấu vết kiểm toán. Danh tính của agent được triển khai dưới dạng workload identity với các thuộc tính chuyên biệt cho phép các năng lực đặc thù của agent, đồng thời giúp duy trì tính tương thích với các mẫu workload identity theo chuẩn ngành. Dịch vụ tích hợp nguyên bản với Amazon Bedrock AgentCore để cung cấp quản lý danh tính và thông tin xác thực cho các ứng dụng agent, bao gồm [Host agent hoặc tool với Amazon Bedrock AgentCore Runtime](/dich-thuat/aws-bedrock-agentcore/06-runtime/) và [Amazon Bedrock AgentCore Gateway: Kết nối bảo mật tool và các tài nguyên khác tới Gateway của bạn](/dich-thuat/aws-bedrock-agentcore/08-gateway/).

## Chủ đề

- [Tổng quan về Amazon Bedrock AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/identity-overview)

- [Bắt đầu với AgentCore Identity](/dich-thuat/aws-bedrock-agentcore/09-identity/identity-getting-started)

- [Sử dụng bảng điều khiển AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-how-to.html)

- [Quản lý workload identity với AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-manage-agent-ids.html)

- [Cấu hình inbound JWT authorizer](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/inbound-jwt-authorizer.html)

- [Quản lý credential provider với AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-outbound-credential-provider.html)

- [Thiết lập và cấu hình nhà cung cấp](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-idps.html)

- [Cấu hình cổng đồng thuận (consent portal)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-consent-portal.html)

- [Kết nối tới các nhà cung cấp danh tính riêng tư](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-private-idp.html)

- [Bảo vệ dữ liệu trong Amazon Bedrock AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-data-protection.html)

- [Gắn thẻ (tagging) cho tài nguyên AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-tagging.html)
