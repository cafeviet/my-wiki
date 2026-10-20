# AGENTCOST03-BP02 Tối ưu chi phí thông qua nén và cắt tỉa cửa sổ ngữ cảnh một cách thông minh

Trong các phiên agent chạy dài, lịch sử hội thoại thô có thể âm thầm đẩy chi phí lên, vì mỗi lượt lại phải trả tiền một lần nữa ở mọi lần gọi sau đó. Nén, truy xuất chọn lọc và cắt tỉa giữ ngữ cảnh tỷ lệ với những gì agent cần cho quyết định hiện tại chứ không tăng theo độ dài phiên.

**Kết quả mong muốn:**

- Bạn nén các lượt hội thoại cũ hơn thành các bản tóm tắt để ngữ cảnh lịch sử không nhân chi phí token cho mỗi lần gọi.
- Bạn chỉ truy xuất top-K các mục bộ nhớ liên quan nhất cho mỗi bước suy luận.
- Bạn cắt tỉa các bản trùng lặp, suy luận đã bị thay thế và kết quả công cụ không liên quan trước mỗi lần gọi.
- Bạn giám sát mức sử dụng cửa sổ ngữ cảnh và cảnh báo với các phiên đang tiến gần tràn.

**Các phản mẫu thường gặp (anti-patterns):**

- Đưa toàn bộ lịch sử hội thoại vào mọi lần gọi bất kể mức liên quan tới tác vụ, gây tăng chi phí token tuyến tính theo độ dài phiên.
- Cho phép lịch sử tương tác thô tích lũy mà không nén, nên các cửa sổ ngữ cảnh bị chi phối bởi các lượt lịch sử có giá trị giảm dần.
- Triển khai các agent mà không giám sát mức sử dụng ngữ cảnh, bỏ lỡ các phiên tiến gần ngưỡng tràn và kích hoạt các lỗi gọi lại tốn kém.
- Truy xuất quá nhiều chunk RAG hoặc độ dài chunk quá lớn trong khi các truy xuất nhỏ hơn, có mục tiêu có thể duy trì chất lượng suy luận với chi phí thấp hơn.
- Không cắt tỉa thông tin trùng lặp hoặc đã bị thay thế, trả phí token cho nội dung không đóng góp cho tác vụ suy luận hiện tại.

**Lợi ích khi áp dụng thực hành tốt này:**

- Nén lịch sử giúp ngăn sự tăng chi phí token tuyến tính trong các phiên chạy dài, khiến các trợ lý bền vững trở nên khả thi về kinh tế.
- Truy xuất chọn lọc chỉ bao gồm ngữ cảnh giá trị cao liên quan tới tác vụ hiện tại, giảm lãng phí token từ dữ liệu liên quan biên.
- Giám sát cửa sổ ngữ cảnh giúp ngăn các lỗi tràn kích hoạt việc gọi lại tốn kém với ngữ cảnh bị cắt cụt.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

[Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) tách bộ nhớ ngắn hạn và dài hạn, đây là mẫu kiến trúc đằng sau tóm tắt cuộn (rolling summarization). Bộ nhớ ngắn hạn giữ các lượt gần đây dạng thô, và bộ nhớ dài hạn tự động trích xuất và hợp nhất các hiểu biết then chốt xuyên các phiên. Với các agent trên AgentCore Runtime, hành vi hai-tầng này triển khai tóm tắt cuộn mà không cần mã tùy chỉnh, và nó là sự khác biệt giữa một trợ lý bền vững có chi phí token bị giới hạn và một trợ lý có chi phí tăng tuyến tính theo tuổi hội thoại.

Truy xuất chọn lọc giúp xử lý vấn đề chi phí lịch sử hội thoại. Thao tác RetrieveMemoryRecords của AgentCore Memory thực hiện tìm kiếm ngữ nghĩa với chấm điểm mức liên quan và lọc metadata, nên bạn có thể tiền-lọc theo độ mới hoặc chủ đề trước khi tìm kiếm tương đồng chạy. Cấu hình top-K giữa ba và năm mục cho mỗi bước suy luận.

Cắt tỉa ngữ cảnh hỗ trợ truy xuất bằng cách loại bỏ các bản trùng lặp giữa các bản tóm tắt và các lượt gần đây trước mỗi lần gọi, bỏ các bước suy luận đã bị thay thế, và loại bỏ các kết quả công cụ không liên quan. Mục tiêu là mức sử dụng ngữ cảnh 60 đến 80% cửa sổ của model, để lại đủ khoảng trống cho các phản hồi trong khi vẫn hưởng lợi từ ngữ cảnh sẵn có.

Định cỡ chunk RAG cũng giúp giải quyết vấn đề này. Khi truy xuất từ [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), các kích thước chunk 256 đến 512 token cân bằng độ chính xác truy xuất với sự phình ngữ cảnh, và giới hạn số chunk truy xuất ở mức tối thiểu cần thiết giúp ngăn dữ liệu liên quan biên chiếm chỗ của tác vụ hiện tại. Việc xác minh rằng nén không âm thầm làm tổn hại chất lượng là một kiểm tra tương quan: ghép mức sử dụng ngữ cảnh với tỷ lệ thành công tác vụ trong CloudWatch Logs Insights và theo dõi xem liệu việc cắt tỉa tích cực có tương quan với sự suy giảm tỷ lệ thành công hay không.

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) làm lộ các số liệu sử dụng token đưa vào các dashboard và cảnh báo CloudWatch. Cảnh báo với các phiên liên tục trên 80% mức sử dụng đánh dấu các ứng viên cho tóm tắt chặt hơn, và việc tương quan chính những số liệu đó với tỷ lệ thành công tác vụ xác nhận liệu nén có đem lại lợi ích về chi phí mà không phải trả giá về chất lượng hay không.

### Các bước triển khai

- **Áp dụng tóm tắt cuộn được quản lý:** Tích hợp [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cho nén được quản lý, hoặc triển khai tóm tắt cuộn tùy chỉnh nén N lượt cũ nhất sau mỗi N lượt.
- **Cấu hình truy xuất được chấm điểm theo mức liên quan:** Dùng RetrieveMemoryRecords của AgentCore Memory với các ngưỡng mức liên quan và lọc metadata, chỉ truy xuất top-K các mục liên quan nhất cho mỗi bước suy luận.
- **Cắt tỉa ngữ cảnh trước mỗi lần gọi:** Loại bỏ các bản trùng lặp, các bước suy luận đã bị thay thế và các kết quả công cụ không liên quan trước mỗi lần gọi model để cửa sổ ngữ cảnh phản ánh những gì quyết định hiện tại cần.
- **Tinh chỉnh kích thước chunk RAG:** Tối ưu kích thước chunk của [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) xuống 256 đến 512 token, giới hạn số chunk truy xuất ở mức tối thiểu cần thiết, và thêm re-ranking để tối đa hóa mức liên quan.
- **Cảnh báo trên mức sử dụng ngữ cảnh:** Xây dựng các dashboard Amazon CloudWatch cho mức sử dụng cửa sổ ngữ cảnh và đặt cảnh báo với các phiên vượt 80% mức sử dụng.
- **Tương quan mức sử dụng với thành công tác vụ:** Dùng CloudWatch Logs Insights để tương quan mức sử dụng ngữ cảnh với tỷ lệ thành công tác vụ, xác thực rằng các chiến lược nén giảm chi phí mà không làm suy giảm chất lượng suy luận.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả](../2-agentcost02/agentcost02-bp02.md)
- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](../2-agentcost02/agentcost02-bp03.md)
- [AGENTCOST03-BP01 Thiết kế các hệ thống truy xuất tiết kiệm chi phí với bộ nhớ theo tầng](agentcost03-bp01.md)
- [AGENTCOST03-BP03 Triển khai lưu bền trạng thái và quản lý vòng đời tối ưu chi phí](agentcost03-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)

**Video liên quan:**

- [AWS 2025 - AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)
- [AWS 2025 - AgentCore Observability: Monitor and Debug with OpenTelemetry](https://www.youtube.com/watch?v=wWQgawUPr1k)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Memory tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
