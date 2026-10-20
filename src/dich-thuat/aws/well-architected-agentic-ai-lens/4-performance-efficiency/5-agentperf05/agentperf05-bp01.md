# AGENTPERF05-BP01 Thiết kế các mẫu điều phối luồng công việc hiệu quả

Các tác nhân phối hợp các sub-agent chuyên biệt có thể giải quyết các tác vụ phức tạp nhanh hơn bất kỳ tác nhân đơn lẻ nào, và mẫu điều phối bạn chọn quyết định liệu việc phối hợp đó thêm mili-giây hay giây. Các mẫu điều phối trải từ các luồng công việc tĩnh (đồ thị thực thi được định nghĩa đầy đủ tại thời điểm thiết kế) tới các luồng công việc động (suy luận của tác nhân quyết định bước tiếp theo tại runtime). Điều phối hiệu quả nghĩa là phân rã các tác vụ để song song hóa, giảm thiểu dữ liệu truyền giữa các bước, và khớp mẫu điều phối với cấu trúc phụ thuộc của tác vụ.

**Kết quả mong muốn:**

- Bạn có các luồng công việc đa tác nhân thực thi với chi phí điều phối tối thiểu, với các tác-vụ-con độc lập chạy song song và các tác vụ phụ thuộc thực thi ngay khi các tiền-đề hoàn thành.
- Bạn có các quyết định định tuyến tác vụ nhanh và chính xác.
- Bạn có **latency** luồng công việc đầu-cuối tiệm cận cực tiểu lý thuyết được định nghĩa bởi đường tới hạn của các thao tác phụ thuộc.

**Các phản mẫu thường gặp (anti-patterns):**

- Chạy mọi bước luồng công việc tuần tự ngay cả khi một số bước không có phụ thuộc dữ liệu và có thể chạy song song, khiến latency đầu-cuối bằng tổng của mọi thời lượng bước thay vì đường tới hạn.
- Dùng tác nhân trình điều phối như một điểm chuyển-tiếp cho mọi dữ liệu giữa các tác nhân worker, tạo ra một điểm nghẽn tuần-tự-hóa ở mỗi bước thay vì để các worker ghi kết quả trực tiếp vào lưu trữ dùng chung.
- Triển khai điều phối đồ thị động mà không có phát hiện chu trình hoặc giới hạn độ sâu cực đại, cho phép các quyết định định tuyến do-LLM-điều-khiển tạo ra các vòng lặp vô hạn nơi các tác nhân liên tục gọi lẫn nhau mà không hội tụ.

**Lợi ích khi áp dụng thực hành tốt này:**

- Thực thi song song các tác-vụ-con độc lập giảm latency đầu-cuối.
- Điều phối được quản lý với thử lại và xử lý lỗi tích hợp sẵn cải thiện độ tin cậy.
- Điều phối có khả năng mở rộng xử lý các mẫu fan-out động mà không cần thay đổi mã.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Hầu hết các luồng công việc dạng tác nhân là động, nghĩa là suy luận của LLM quyết định gọi Tool hoặc sub-agent nào tiếp theo dựa trên các kết quả trung gian. Với các luồng công việc này, dùng các khả năng điều phối tích hợp sẵn của framework tác nhân của bạn:

- Strands Agents cung cấp điều phối dựa-trên-đồ-thị (GraphBuilder), các mẫu supervisor, và phối hợp bầy (swarm)
- LangGraph cung cấp các luồng công việc đồ thị có trạng thái
- CrewAI cung cấp điều phối crew dựa-trên-vai-trò

Các mẫu do-framework-điều-khiển này là phù hợp tự nhiên cho các khối công việc tác nhân vì đường thực thi nảy sinh từ suy luận của Model thay vì được định nghĩa trước. Để giữ điều phối động hiệu năng cao, triển khai phát hiện chu trình (theo dõi các node đã thăm bằng băm đầu vào), giới hạn độ sâu cực đại (10–15 bước), và số lượng fan-out có ràng buộc (5–10 nhánh đồng thời) để giúp ngăn các chuỗi thực thi vô giới hạn.

Với các luồng công việc xác định nơi đồ thị chạy được biết đầy đủ tại thời điểm thiết kế, các pipeline xử lý batch, luồng công việc phê duyệt, các chuỗi biến đổi dữ liệu, dùng [AWS Step Functions](https://aws.amazon.com/step-functions/) với các trạng thái Parallel và Map để chạy các bước đồng thời, các trạng thái Choice cho phân nhánh có điều kiện, và Catch cùng Retry tích hợp sẵn cho xử lý lỗi. Step Functions cũng có giá trị như một lớp lai xử lý điều phối bền và lưu trạng thái trong khi chỉ gọi các tác nhân dựa-trên-LLM tại các điểm quyết định đòi hỏi suy luận.

Giữ các payload trạng thái nhỏ bằng cách lưu các kết quả trung gian lớn trong [Amazon S3](https://aws.amazon.com/s3/) hoặc [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) và chỉ truyền các tham chiếu qua lớp điều phối.

Với mọi mẫu điều phối, cấu hình các timeout theo-bước và cấp-luồng-công-việc giúp ngăn các tác nhân chậm chặn toàn bộ luồng công việc. Với các luồng công việc đồ thị động, phân bổ các ngân sách latency theo-nhánh suy ra từ SLO tác vụ tổng thể, nếu một nhánh vượt ngân sách của nó, kết thúc nó và tiếp tục với kết quả một phần tốt nhất sẵn có. Thiết kế các luồng công việc để tối đa hóa song song hóa bằng cách phân tích các phụ thuộc tác vụ và thực thi các tác-vụ-con độc lập đồng thời.

Giám sát các chỉ số thực thi luồng công việc gồm thời lượng bước, hiệu quả song song, kích thước payload trạng thái, và phân phối độ sâu đồ thị.

### Các bước triển khai

- **Phân tích các phụ thuộc tác vụ đa tác nhân và phân loại mỗi luồng công việc:** Phân loại mỗi luồng công việc là đồ thị động (định tuyến do-LLM-điều-khiển, hầu hết luồng công việc tác nhân), lai (luồng xác định với các điểm quyết định LLM), hoặc tĩnh (đồ thị thực thi được định nghĩa đầy đủ trước), và dùng phân loại để dẫn dắt lựa chọn điều phối.
- **Với các luồng công việc đồ thị động, dùng điều phối nguyên bản của framework tác nhân của bạn:** Dùng Strands GraphBuilder, LangGraph, hoặc tương đương với phát hiện chu trình, giới hạn độ sâu cực đại, và số lượng fan-out có ràng buộc để giúp ngăn các chuỗi thực thi vô giới hạn.
- **Với các luồng công việc tĩnh/lai, triển khai dùng Step Functions với các trạng thái Parallel và Map:** Dùng các trạng thái Parallel và Map của [AWS Step Functions](https://aws.amazon.com/step-functions/) để chạy các bước đồng thời với thử lại và xử lý lỗi tích hợp sẵn trên các đường xác định.
- **Triển khai truyền trạng thái hiệu quả dùng tham chiếu S3/DynamoDB thay vì payload nội tuyến:** Giữ các payload điều phối nhỏ bằng cách lưu các kết quả trung gian lớn trong S3 hoặc DynamoDB và chỉ truyền tham chiếu.
- **Cấu hình các timeout theo-bước và cấp-luồng-công-việc với các chiến lược dự phòng cho các tác nhân chậm:** Đặt timeout ở cả cấp-bước và cấp-luồng-công-việc, và định nghĩa hành vi dự phòng để một tác nhân chậm duy nhất không thể làm khựng toàn bộ luồng công việc.
- **Giám sát các chỉ số thực thi luồng công việc: thời lượng bước, hiệu quả song song, kích thước payload trạng thái, và phân phối độ sâu đồ thị:** Công bố các chỉ số này tới CloudWatch để hiệu năng điều phối có thể được tinh chỉnh từ dữ liệu thay vì giả định.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF05-BP02 Triển khai các mô hình cộng tác đa tác nhân được tối ưu](agentperf05-bp02.md)
- [AGENTPERF05-BP03 Tối ưu thực thi pipeline AI đa-giai-đoạn](agentperf05-bp03.md)
- [AGENTPERF02-BP01 Thiết kế pipeline suy luận hiệu quả](../2-agentperf02/agentperf02-bp01.md)

**Tài liệu liên quan:**

- [Blog: Tùy biến luồng công việc tác nhân với kỹ thuật điều phối nâng cao dùng Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/)
- [Các mẫu và luồng công việc AI dạng tác nhân trên AWS, Các tác nhân điều phối luồng công việc](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-orchestration-agents.html)
- [Xây dựng kiến trúc serverless cho AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/introduction.html)
- [Blog: Xây dựng tác nhân AI hiệu quả trên AWS Serverless](https://aws.amazon.com/blogs/compute/effectively-building-ai-agents-on-aws-serverless/)

**Video liên quan:**

- [Kiến trúc AI dạng tác nhân có khả năng mở rộng và an toàn với AgentCore (AIM431)](https://www.youtube.com/watch?v=wqmeZOT6mmc)
- [Xây dựng luồng công việc tác nhân đầu tiên của bạn với Strands](https://www.youtube.com/watch?v=oGzEKQVhKQU)
- [Xây dựng tác nhân AI đáng tin cậy với LangGraph](https://www.youtube.com/watch?v=E0BtW2yt2pA)

**Ví dụ liên quan:**

- [GitHub: Hướng dẫn điều phối đa tác nhân dùng Bedrock AgentCore](https://github.com/aws-solutions-library-samples/guidance-for-multi-agent-orchestration-using-bedrock-agentcore-on-aws)

**Công cụ liên quan:**

- [Strands Agents](https://strandsagents.com/)

**Dịch vụ liên quan:**

- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
