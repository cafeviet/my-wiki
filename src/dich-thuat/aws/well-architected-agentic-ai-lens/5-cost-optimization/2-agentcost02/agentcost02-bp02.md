# AGENTCOST02-BP02 Tối ưu chi phí tiêu thụ token thông qua kỹ thuật prompt hiệu quả

Mỗi token trong một system prompt đều phải trả tiền ở mọi lần gọi, nên sự phình prompt tăng theo tuyến tính cùng với lưu lượng. Nén các system prompt, mô tả công cụ và định dạng đầu ra khiến chi phí cố định của mỗi lần gọi agent tỷ lệ với quyết định mà nó phải đưa ra, chứ không theo độ dài dòng của các chỉ thị.

**Kết quả mong muốn:**

- Bạn có các system prompt của agent được nén xuống mức token tối thiểu cần thiết để hoàn thành tác vụ chính xác.
- Bạn có các mô tả công cụ được trình ra động dựa trên tác vụ hiện tại thay vì được truyền đầy đủ ở mọi lần gọi.
- Bạn ràng buộc độ dài đầu ra một cách tường minh để các phản hồi dài dòng không dồn lại qua suy luận nhiều lượt.
- Bạn đánh phiên bản các prompt và theo dõi chi phí trên mỗi tác vụ cho từng phiên bản để các thay đổi về hiệu quả có thể đo lường được theo thời gian.

**Các phản mẫu thường gặp (anti-patterns):**

- Viết các system prompt dài dòng với các mô tả nhân cách lê thê và các giải thích dư thừa, làm phồng chi phí token cố định ở mọi lần gọi.
- Đưa mọi mô tả công cụ vào mọi lần gọi bất kể mức độ liên quan tới tác vụ, làm phồng token đầu vào khi chỉ một tập con các công cụ được áp dụng.
- Cho phép độ dài đầu ra không ràng buộc mà không có chỉ thị định dạng, tạo điều kiện cho các phản hồi dài dòng dồn lại qua các chu kỳ suy luận nhiều lượt.
- Coi các prompt là chuỗi không kiểm soát thay vì các tạo tác được đánh phiên bản, nên các hồi quy về hiệu quả token không được để ý cho đến một lần xem xét hóa đơn.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các khoản giảm chi phí cố định từ việc nén prompt dồn lại qua mọi lần gọi agent trong các triển khai khối lượng lớn.
- Nạp công cụ động chỉ truyền các công cụ liên quan tới tác vụ, giảm chi phí mô tả công cụ tỷ lệ với kích thước danh mục.
- Đánh phiên bản prompt kèm theo dõi token biến việc nén thành một thực hành liên tục, đo lường được thay vì một lần dọn dẹp duy nhất.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

System prompt là chi phí cố định lớn nhất trong mọi lần gọi model, nghĩa là mọi câu không cần thiết đều phải trả tiền lại mỗi khi agent được gọi. Bắt đầu bằng việc kiểm toán các prompt với [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để đo dấu chân token, rồi nén một cách hệ thống. Thay các chỉ thị dài dòng bằng các chỉ thị có cấu trúc, siết chặt các định nghĩa vai trò, và loại bỏ các giải thích dư thừa.

Các mô tả công cụ hành xử theo cách tương tự. Nếu prompt mang toàn bộ danh mục công cụ ngay cả khi chỉ ba công cụ liên quan, bạn đang trả tiền cho phần còn lại của danh mục ở mọi lần gọi. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) dùng Semantic Tool Selection dựa trên MCP để chỉ trình ra các công cụ liên quan tới ý định hiện tại, và [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) quản lý trạng thái hội thoại qua các phiên nhiều lượt để bạn không phải trả tiền cho việc nối lịch sử thủ công.

Trong cửa sổ ngữ cảnh của bạn, hãy phân bổ token cho system prompt (20 đến 30%), ngữ cảnh người dùng (30 đến 40%), các ví dụ few-shot (10 đến 20%), và scratchpad của agent (20 đến 30%), và điều chỉnh dựa trên các mẫu suy luận của agent. Riêng với các ví dụ few-shot, hãy kiểm tra xem model có hoạt động tốt ở chế độ zero-shot hay không trước khi trả tiền cho các ví dụ ở mọi lần gọi. Khi cần ví dụ, hãy xác định số lượng tối thiểu duy trì được độ chính xác tác vụ theo đường cơ sở chất lượng. Hai hoặc ba ví dụ thường là đủ, và việc chọn ví dụ động từ một chỉ mục ngữ nghĩa chỉ giữ những cái liên quan trong ngữ cảnh.

Độ dài đầu ra là thứ cuối cùng cần điều chỉnh. Các chỉ thị định dạng tường minh trong system prompt (cấu trúc phản hồi, độ dài tối đa) kiểm soát trực tiếp chi phí token đầu ra. Hãy coi các prompt là các tạo tác được đánh phiên bản. Ghi lại số token, tỷ lệ thành công tác vụ và chi phí trên mỗi tác vụ cho từng phiên bản bằng dữ liệu đo lường của AgentCore Observability, và thiết lập một nhịp xem xét hàng tháng theo dõi khoản tiết kiệm tích lũy trong AWS Cost Explorer.

### Các bước triển khai

- **Kiểm toán và nén các system prompt:** Dùng [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) để đo dấu chân token cho mọi prompt, rồi áp dụng nén để tối thiểu hóa kích thước prompt trong khi duy trì độ chính xác quyết định.
- **Trình ra công cụ một cách động qua Gateway:** Dùng Semantic Tool Selection của [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để chỉ trình ra các công cụ liên quan cho mỗi lần gọi, và nén các mô tả công cụ xuống tên công cụ, một câu mô tả, và một lược đồ tham số súc tích.
- **Ràng buộc độ dài đầu ra:** Thêm các chỉ thị định dạng đầu ra tường minh vào system prompt và cấu hình các tham số giới hạn token đặc thù theo model để thực thi các trần cứng về kích thước phản hồi.
- **Dùng bộ nhớ được quản lý cho ngữ cảnh nhiều lượt:** Cấu hình [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) để trạng thái hội thoại được duy trì tự động thay vì được truyền lại như lịch sử đầy đủ.
- **Giảm chi phí ví dụ few-shot:** Đánh giá xem mỗi tác vụ agent có cần ví dụ hay không, rồi giảm xuống số lượng hiệu quả tối thiểu là hai đến ba. Nạp ví dụ động từ một thư viện lưu trên Amazon S3 bằng truy xuất theo độ tương đồng ngữ nghĩa.
- **Đánh phiên bản prompt và theo dõi hiệu quả:** Ghi lại số token và tỷ lệ thành công tác vụ cho từng phiên bản prompt, và thiết lập một nhịp xem xét tối ưu hàng tháng theo dõi khoản tiết kiệm tích lũy theo các mục tiêu chi phí trên mỗi tác vụ.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTCOST01-BP01 Dùng reflection pattern để thiết kế các vòng lặp suy luận agent hiệu quả](../1-agentcost01/agentcost01-bp01.md)
- [AGENTCOST02-BP01 Kiến trúc lựa chọn model theo tầng để tối ưu chi phí-hiệu năng](agentcost02-bp01.md)
- [AGENTCOST02-BP03 Dùng caching thông minh để giảm các lần gọi model dư thừa](agentcost02-bp03.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [Economics for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/index.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Sustainable and cost-efficient generative AI with agentic workflows (AIM333)](https://www.youtube.com/watch?v=tFiDkSG2ess)
- [Strands Tools: Building Custom AI Agents with Python](https://www.youtube.com/watch?v=EGhIZCfOvG4)

**Ví dụ liên quan:**

- [GitHub: awslabs/amazon-bedrock-agentcore-samples - Runtime tutorials](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/01-AgentCore-runtime)

**Công cụ liên quan:**

- [Strands Agents Custom Tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
