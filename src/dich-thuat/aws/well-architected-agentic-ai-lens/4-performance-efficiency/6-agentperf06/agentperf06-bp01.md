# AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu

Các tác nhân hiển thị đúng **Tools** vào đúng lúc phản hồi nhanh hơn và ra quyết định tốt hơn. Các LLM ra quyết định lựa chọn Tool ngày càng kém một khi tập ứng viên tăng vượt 10-15 Tools, nên lọc động, thực thi song song, và các kết quả được cache giữ vòng lặp suy luận chặt ngay cả khi danh mục Tools tăng. Các lệnh gọi Tools xảy ra bên trong vòng lặp suy luận, nghĩa là **latency** của chúng thêm trực tiếp vào thời gian phản hồi.

**Kết quả mong muốn:**

- Bạn có các lệnh gọi Tools thêm latency tối thiểu vào vòng lặp suy luận của tác nhân.
- Bạn có lựa chọn Tools nhanh và chính xác, với các tác nhân chọn từ một tập được lọc gồm 5-10 lựa chọn liên quan thay vì đánh giá toàn danh mục.
- Bạn có các lệnh gọi Tools độc lập thực thi song song.
- Bạn có các kết quả Tools được cache nơi phù hợp.
- Bạn có các chỉ số latency, tỷ lệ lỗi, và mức dùng theo-Tool cung cấp khả năng thấy hiệu năng Tool.

**Các phản mẫu thường gặp (anti-patterns):**

- Trình mọi Tool sẵn có cho tác nhân trên mọi vòng lặp suy luận, buộc LLM đánh giá hàng chục mô tả Tool, tiêu dung lượng context window và làm suy giảm độ chính xác lựa chọn.
- Thực thi các lệnh gọi Tools tuần tự khi chúng không có phụ thuộc dữ liệu, thêm latency bằng tổng của mọi thời lượng Tool thay vì giá trị cực đại.
- Bỏ qua caching kết quả Tools, nên các tác nhân gọi-lại cùng một Tool với các tham số giống hệt nhiều lần trong một tác vụ duy nhất.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thực thi Tools song song và caching kết quả giảm latency vòng lặp suy luận.
- Lọc động chỉ trình các Tools liên quan cải thiện độ chính xác lựa chọn Tools.
- Giám sát theo-Tool tăng tốc phát hiện các vấn đề hiệu năng Tool.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Áp dụng MCP làm giao thức tích hợp Tools chuẩn và dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để phơi bày các Tools dưới dạng các endpoint tương thích MCP. AgentCore Gateway cung cấp khám phá Tools ngữ nghĩa tích hợp sẵn (x_amz_bedrock_agentcore_search) để các tác nhân truy vấn các Tools liên quan bằng mô tả ngôn ngữ tự nhiên thay vì nhận toàn danh mục. Với các tác nhân có quyền truy cập các danh mục Tools lớn, một mẫu lựa chọn hai-giai-đoạn hoạt động tốt: một bộ tiền-lọc nhẹ thu hẹp toàn danh mục về 5-10 Tools liên quan nhất dựa trên ngữ cảnh tác vụ hiện tại, và chỉ các Tools được lọc đó xuất hiện trong prompt của LLM. Với các tác nhân xây dựng bằng Strands Agents hoặc một framework tác nhân khác, thực thi Tools song song tích hợp sẵn chạy các lệnh gọi Tools độc lập một cách đồng thời.

Thiết kế các API Tools riêng cho tiêu thụ tác nhân, như các lược đồ phản hồi gọn chỉ trả về các trường mà tác nhân cần, phân trang cho các tập kết quả lớn, và hỗ trợ phản hồi một phần. Cache các kết quả Tools ở nhiều cấp, phạm-vi-yêu-cầu (trong một phiên suy luận duy nhất), phạm-vi-phiên (qua các vòng lặp suy luận cho cùng người dùng), và toàn cục (dữ liệu dùng chung với TTL phù hợp). Giám sát sức khỏe Tool theo dõi latency, tỷ lệ lỗi, và tính sẵn sàng theo-Tool, và các cắt-mạch tự động định tuyến vòng qua các Tools chậm hoặc thất bại.

### Các bước triển khai

- **Áp dụng MCP làm giao thức tích hợp Tools chuẩn và phơi bày các Tools qua AgentCore Gateway:** Phơi bày các Tools dưới dạng các endpoint tương thích MCP qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) để các tác nhân dùng một giao diện nhất quán duy nhất.
- **Bật khám phá Tools ngữ nghĩa của AgentCore Gateway để lọc Tools theo độ liên quan tác vụ:** Dùng x_amz_bedrock_agentcore_search để thu hẹp tập Tools theo từng yêu cầu để LLM chỉ đánh giá 5-10 Tools liên quan nhất.
- **Triển khai thực thi Tools song song cho các lệnh gọi Tools độc lập trong cùng bước suy luận:** Dùng thực thi Tools song song nguyên bản của framework của bạn (Strands Agents, LangGraph) để các lệnh gọi Tools độc lập chạy đồng thời.
- **Triển khai caching kết quả Tools đa-cấp với TTL phù hợp theo từng Tool:** Cache các kết quả Tools ở phạm-vi-yêu-cầu, phạm-vi-phiên, và phạm-vi-toàn-cục với TTL khớp yêu cầu độ mới của mỗi Tool.
- **Cấu hình giám sát sức khỏe Tool với các chỉ số latency và tỷ lệ lỗi theo-Tool, và các cắt-mạch tự động cho các Tools suy giảm:** Theo dõi latency và tỷ lệ lỗi theo-Tool trong Amazon CloudWatch và dùng các cắt-mạch tự động để định tuyến vòng qua các Tools suy giảm.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF06-BP02 Triển khai các mẫu gọi Tools hiệu quả](agentperf06-bp02.md)
- [AGENTPERF06-BP03 Tối ưu sử dụng meta-tool và chuỗi hóa Tools](agentperf06-bp03.md)
- [AGENTPERF04-BP02 Triển khai giao tiếp tác nhân dựa-trên-giao-thức hiệu quả](../4-agentperf04/agentperf04-bp02.md)

**Tài liệu liên quan:**

- [Blog: Giới thiệu Amazon Bedrock AgentCore Gateway: Biến đổi phát triển Tool tác nhân AI doanh nghiệp](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Blog: Biến đổi kiến trúc MCP của bạn: Hợp nhất các máy chủ MCP qua AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)
- [Blog: Các giao thức mở cho khả năng tương tác tác nhân Phần 3: Strands Agents & MCP](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-3-strands-agents-mcp/)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [Các framework, giao thức, và Tools AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/introduction.html)

**Video liên quan:**

- [Mở rộng các Tool tác nhân với AgentCore Gateway (AIM3313)](https://www.youtube.com/watch?v=DlIHB8i6uyE)
- [Tích hợp các Tool MCP với Strands Agents](https://www.youtube.com/watch?v=bHSbjCZZFjE)
- [Strands Tools: Xây dựng các tác nhân AI tùy chỉnh với Python](https://www.youtube.com/watch?v=EGhIZCfOvG4)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/02-AgentCore-gateway)

**Workshop liên quan:**

- [Bắt đầu với Amazon Bedrock AgentCore, Lab 3: Gateway, Identity & Policy](https://catalog.workshops.aws/agentcore-getting-started/en-US/50-add-tool-gateway)
- [Đào sâu vào Bedrock AgentCore, Gateway](https://catalog.workshops.aws/agentcore-deep-dive/en-US/30-agentcore-gateway)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
