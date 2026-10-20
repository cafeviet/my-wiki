---
title: "AgentCore Memory: Thêm bộ nhớ cho agent của bạn"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html"
---

# AgentCore Memory: Thêm bộ nhớ cho agent của bạn

# Thêm bộ nhớ (memory) cho agent Amazon Bedrock AgentCore của bạn

AgentCore Memory (bộ nhớ) là một dịch vụ được quản lý hoàn toàn, mang lại cho các agent (tác tử AI) của bạn khả năng ghi nhớ các tương tác trước đây, giúp chúng cung cấp những cuộc trò chuyện thông minh hơn, nhận biết ngữ cảnh và được cá nhân hóa. Nó cung cấp một cách đơn giản và mạnh mẽ để xử lý cả ngữ cảnh ngắn hạn lẫn lưu giữ kiến thức dài hạn mà không cần xây dựng hay quản lý hạ tầng phức tạp.

AgentCore Memory giải quyết một thách thức cơ bản trong AI dạng agentic: tính vô trạng thái (statelessness). Nếu không có khả năng bộ nhớ, các agent AI xem mỗi tương tác như một phiên bản mới mà không có kiến thức về các cuộc trò chuyện trước đó. AgentCore Memory cung cấp khả năng thiết yếu này, cho phép agent của bạn xây dựng một sự hiểu biết mạch lạc về người dùng theo thời gian.

AgentCore Memory hỗ trợ nhiều SDK và framework agent khác nhau. Xem ví dụ tại [Ví dụ về Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html).

###### Các chủ đề

- [Các loại memory](#memory-types-overview)

- [Lợi ích chính của memory](#memory-key-benefits)

- [Các trường hợp sử dụng phổ biến của memory](#memory-common-use-cases)

- [Cách hoạt động](/dich-thuat/aws-bedrock-agentcore/07-memory/how-it-works)

- [Bắt đầu với AgentCore Memory](/dich-thuat/aws-bedrock-agentcore/07-memory/memory-get-started)

- [Tạo một AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-create-a-memory-store.html)

- [Sử dụng bộ nhớ ngắn hạn (short-term memory)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-memory-short-term.html)

- [Sử dụng bộ nhớ dài hạn (long-term memory)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-memory-long-term.html)

- [Ví dụ về Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html)

- [Amazon Bedrock capacity cho các chiến lược built-in with overrides](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-capacity.html)

- [Observability (khả năng quan sát)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-observability.html)

- [Thực hành tốt nhất](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)

- [Tính năng và chủ đề nâng cao cho Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-advanced.html)

## Các loại memory

AgentCore Memory cung cấp [hai loại](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html) memory phối hợp với nhau để tạo ra các agent AI thông minh, nhận biết ngữ cảnh:

Bộ nhớ ngắn hạn (short-term memory) ghi lại các tương tác theo từng lượt trong một phiên duy nhất. Điều này cho phép agent duy trì ngữ cảnh tức thời mà không yêu cầu người dùng lặp lại thông tin.

**Ví dụ:** Khi người dùng hỏi "What’s the weather like in Seattle?" và tiếp theo hỏi "What about tomorrow?", agent dựa vào lịch sử trò chuyện gần đây để hiểu rằng "tomorrow" đề cập đến thời tiết ở Seattle.

Bộ nhớ dài hạn (long-term memory) tự động trích xuất và lưu trữ những thông tin cốt lõi từ các cuộc trò chuyện qua nhiều phiên, bao gồm sở thích người dùng, các sự kiện quan trọng, và tóm tắt phiên — nhằm lưu giữ kiến thức bền vững qua nhiều phiên.

**Ví dụ:** Nếu một khách hàng đề cập rằng họ thích ghế cạnh cửa sổ trong lúc đặt vé máy bay, agent lưu sở thích này vào bộ nhớ dài hạn. Trong các tương tác sau, agent có thể chủ động đề xuất ghế cạnh cửa sổ, tạo ra trải nghiệm được cá nhân hóa.

## Lợi ích chính của memory

- **Tạo các cuộc trò chuyện tự nhiên hơn:** Bằng cách ghi nhớ các lượt trước trong một cuộc trò chuyện, các agent có thể hiểu ngữ cảnh, làm rõ các phát biểu mơ hồ, và tương tác theo cách giống con người hơn.

- **Mang lại trải nghiệm được cá nhân hóa:** Lưu giữ sở thích người dùng, dữ liệu lịch sử, và các sự kiện quan trọng qua các phiên để điều chỉnh phản hồi và hành động phù hợp với từng người dùng.

- **Giảm độ phức tạp phát triển:** Chuyển giao công việc nặng nhọc, không tạo khác biệt của việc quản lý trạng thái hội thoại và bộ nhớ, cho phép bạn tập trung vào việc xây dựng logic nghiệp vụ cốt lõi của agent.

## Các trường hợp sử dụng phổ biến của memory

- **Agent hội thoại:** Một chatbot hỗ trợ khách hàng ghi nhớ các vấn đề và sở thích trước đây của người dùng, cho phép nó cung cấp hỗ trợ phù hợp hơn trong các tương tác về sau.

- **Agent hướng tác vụ / theo quy trình:** Một agent AI điều phối một quy trình nghiệp vụ nhiều bước, chẳng hạn phê duyệt hóa đơn, sử dụng memory để theo dõi trạng thái của từng bước và duy trì tiến độ quy trình.

- **Hệ thống đa agent (multi-agent):** Một nhóm agent AI quản lý chuỗi cung ứng chia sẻ memory để đồng bộ mức tồn kho, dự đoán nhu cầu, và tối ưu logistics.

- **Agent tự chủ hoặc lập kế hoạch:** Một xe tự hành sử dụng memory để lập lộ trình, điều chỉnh theo điều kiện giao thông, và học từ các trải nghiệm trước đây để cải thiện các quyết định lái xe trong tương lai.
