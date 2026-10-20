---
title: "Tìm hiểu service contract của AgentCore Runtime"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-service-contract.html"
---

# Tìm hiểu service contract của AgentCore Runtime

Service contract của AgentCore Runtime (môi trường chạy) định nghĩa giao thức giao tiếp chuẩn hóa mà ứng dụng agent (tác tử AI) của bạn phải triển khai để tích hợp với hạ tầng hosting agent của Amazon Bedrock. Contract này đảm bảo giao tiếp liền mạch giữa code agent tùy chỉnh của bạn và môi trường hosting được quản lý của AWS.

- [Các giao thức được hỗ trợ](#supported-protocols)

- [So sánh các giao thức được hỗ trợ](#protocol-comparison)

- [HTTP protocol contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html)

- [MCP protocol contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp-protocol-contract.html)

- [A2A protocol contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html)

- [AG-UI protocol contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html)

## Các giao thức được hỗ trợ

Service contract của AgentCore Runtime hỗ trợ các giao thức giao tiếp sau:

- [HTTP](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html) : Các endpoint REST API trực tiếp cho các mẫu request/response truyền thống

- [MCP](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp-protocol-contract.html) : Model Context Protocol cho các tool (công cụ) và agent server

- [A2A](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html) : Giao thức Agent-to-Agent cho giao tiếp và khám phá đa agent

- [AG-UI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html) : Giao thức Agent-to-User Interface cho các trải nghiệm agent tương tác với việc render UI

## So sánh các giao thức được hỗ trợ

So sánh các giao thức HTTP, MCP, A2A và AG-UI để hiểu sự khác biệt và các trường hợp dùng.

| Tính năng | HTTP Protocol | MCP Protocol | A2A Protocol | AG-UI Protocol |
| --- | --- | --- | --- | --- |
| **Port** | 8080 | 8000 | 9000 | 8080 |
| **Mount Path** | /invocations (HTTP), /ws (WebSocket) | /mcp | / (root) | /invocations (SSE), /ws (WebSocket) |
| **Message Format** | REST JSON/SSE, WebSocket (text/binary) | JSON-RPC | JSON-RPC 2.0 | Event streams (SSE/WebSocket) |
| **Discovery** | N/A | Tool listing | Agent Cards | N/A |
| **Authentication** | SigV4, OAuth 2.0; WebSocket hỗ trợ SigV4 qua header và query param | SigV4, OAuth 2.0 | SigV4, OAuth 2.0 | SigV4, OAuth 2.0 |
| **Use Case** | Gọi API trực tiếp, streaming thời gian thực | Tool server | Giao tiếp agent-to-agent | Trải nghiệm UI tương tác |
