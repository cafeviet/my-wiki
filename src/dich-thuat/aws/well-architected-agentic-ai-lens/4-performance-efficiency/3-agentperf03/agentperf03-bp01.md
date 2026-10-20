# AGENTPERF03-BP01 Triển khai các hệ thống quản lý bộ nhớ phân tầng

Các tác nhân mang ngữ cảnh qua các lượt và phiên mang lại phản hồi cá nhân hóa và chính xác hơn, nhưng chỉ khi truy xuất bộ nhớ không trở thành điểm nghẽn **latency** trên mỗi vòng lặp suy luận. Một kiến trúc bộ nhớ phân tầng tách trạng thái phiên nhanh, tạm thời khỏi tri thức liên-phiên bền để công nghệ lưu trữ, mẫu truy cập, và vòng đời của mỗi tầng có thể được tối ưu độc lập thay vì bị ép qua một kho lưu duy nhất.

**Kết quả mong muốn:**

- Bạn có bộ nhớ tác nhân tách thành một tầng ngắn hạn cho ngữ cảnh trong-phiên và một tầng dài hạn cho tri thức liên-phiên, mỗi tầng được hậu thuẫn bởi lưu trữ khớp với mẫu truy cập của nó.
- Bạn có các chính sách vòng đời tự động trích xuất các hiểu biết bền từ bộ nhớ ngắn hạn vào các chiến lược dài hạn (ngữ nghĩa, giai thoại/episodic, tóm tắt, và sở thích người dùng) và đuổi (evict) trạng thái ngắn hạn cũ mà không cần can thiệp thủ công.
- Bạn có latency truy xuất theo-tầng được theo dõi như một KPI hạng nhất, với các ngân sách giữ truy cập bộ nhớ khỏi chi phối vòng lặp suy luận.
- Bạn có bộ nhớ dài hạn được phạm-vi-hóa và namespace theo người dùng, phiên, hoặc tenant để các truy xuất chỉ trả về các bản ghi liên quan tới actor hiện tại.

**Các phản mẫu thường gặp (anti-patterns):**

- Lưu toàn bộ bộ nhớ tác nhân trong một cơ sở dữ liệu duy nhất bất kể mẫu truy cập, buộc các lượt đọc phiên dưới-một-giây và các tìm kiếm ngữ nghĩa quy-mô-lớn qua cùng lớp lưu trữ.
- Lưu bền mọi lượt của bộ nhớ ngắn hạn vô thời hạn mà không trích xuất vào các chiến lược dài hạn hoặc đuổi, cho phép các kho phiên tăng vô giới hạn và latency truy xuất suy giảm theo thời gian.
- Coi bộ nhớ dài hạn như một túi bản ghi duy nhất thay vì phân biệt giữa các sự kiện ngữ nghĩa, các sự kiện giai thoại, các tóm tắt hội thoại, và sở thích người dùng, điều này buộc mọi truy vấn tìm kiếm tất cả các loại bản ghi.
- Phạm-vi-hóa bộ nhớ dài hạn toàn cục thay vì theo người dùng, phiên, hoặc tenant, nên các truy xuất trả về các bản ghi liên-actor làm phình ngữ cảnh và rò rỉ thông tin.
- Xây dựng hạ tầng bộ nhớ phân tầng tùy chỉnh từ đầu thay vì đánh giá các dịch vụ được quản lý cung cấp kho phiên, chiến lược trích xuất, và truy xuất vector như các nguyên hàm.

**Lợi ích khi áp dụng thực hành tốt này:**

- Các kho trong-bộ-nhớ nhanh phục vụ các lượt đọc phiên trong vài mili-giây một chữ số trong khi các kho vector xử lý các truy vấn ngữ nghĩa dài hạn mà không ghép cặp hai.
- Các chính sách trích xuất và đuổi tự động giữ dấu chân và latency truy xuất của mỗi tầng ổn định khi mức dùng mở rộng.
- Tách bộ nhớ dài hạn thành các chiến lược riêng biệt, ngữ nghĩa, giai thoại, tóm tắt, sở thích, cho phép tác nhân chỉ truy vấn loại bản ghi liên quan tới bước suy luận hiện tại của nó.
- Namespace bộ nhớ dài hạn theo người dùng, phiên, hoặc tenant giúp ngăn các truy xuất liên-actor và giữ ngữ cảnh liên quan.
- Các nguyên hàm bộ nhớ được quản lý loại bỏ nhu cầu vận hành các kho phiên, pipeline trích xuất, và chỉ mục vector như hạ tầng riêng chế.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Truy cập bộ nhớ nằm trên đường nóng của mỗi vòng lặp suy luận. Một tác nhân đọc ngữ cảnh phiên và truy xuất tri thức dài hạn liên quan ở mỗi bước trả latency truy xuất đó nhân với số vòng lặp, điều này khiến bộ nhớ là một trong các điểm dùng lớn nhất trong vòng lặp suy luận.

Nguyên nhân gốc của hiệu năng bộ nhớ kém thường là một sự không-khớp-mẫu-truy-cập. Dùng một lớp lưu trữ duy nhất cho cả các lượt đọc phiên dưới-mili-giây lẫn các tìm kiếm ngữ nghĩa quy-mô-lớn buộc một mẫu mang các đặc trưng chi phí và latency phù hợp cho mẫu kia. Phân tầng giải quyết sự không-khớp bằng cách tách bộ nhớ thành một tầng ngắn hạn cho ngữ cảnh trong-phiên và một tầng dài hạn cho tri thức liên-phiên, rồi khớp mỗi tầng với lưu trữ có latency, độ bền, và mô hình truy vấn đúng.

Bộ nhớ ngắn hạn giữ trạng thái lượt-theo-lượt mà một tác nhân đọc và ghi trong một phiên: N lượt gần nhất, suy luận trung gian, đầu ra Tools, và ngữ cảnh tạm thời do-người-dùng-cung-cấp. [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) cung cấp một tầng ngắn hạn được quản lý lưu các sự kiện phiên và tích hợp trích xuất vào tầng dài hạn, loại bỏ nhu cầu vận hành một kho phiên hoặc pipeline trích xuất riêng.

Với các khối công việc cần các lượt đọc ngắn hạn dưới-mili-giây hoặc muốn sở hữu pipeline trích xuất, [Amazon ElastiCache (Valkey)](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/agentic-memory-why-elasticache.html) cung cấp các lượt đọc trong-bộ-nhớ, hết hạn dựa-trên-TTL, và các cấu trúc nguyên bản (hash, list, sorted set) ánh xạ tốt tới dữ liệu phiên. Yêu cầu độ bền cho bộ nhớ ngắn hạn thường thấp, trạng thái có thể tái tạo hoặc bị loại bỏ khi phiên kết thúc, nên tầng nên được định cỡ cho latency, không cho lưu trữ dài hạn.

Bộ nhớ dài hạn giữ tri thức bền tồn tại qua các phiên: sở thích người dùng, sự kiện lĩnh vực, tóm tắt tương-tác-trong-quá-khứ, và các bản ghi giai thoại về kết quả tác vụ trong quá khứ. Truy cập ít thường xuyên hơn nhưng vận hành trên một kho lớn hơn nhiều và thường dựa vào độ tương đồng ngữ nghĩa thay vì tra cứu khóa. AgentCore Memory cung cấp một tầng dài hạn được quản lý với [bốn chiến lược tích hợp sẵn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html), ngữ nghĩa, giai thoại, tóm tắt, và sở thích người dùng, mỗi cái được trích xuất từ các sự kiện phiên và lập chỉ mục riêng biệt, để tác nhân có thể chỉ truy vấn kho liên quan tới bước suy luận hiện tại của nó.

Với các nhóm muốn sở hữu kho dài hạn trực tiếp, [bộ nhớ dạng tác nhân trong Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application-agentic-memory.html) cung cấp truy xuất dày (dense) và lai trên các bản ghi dài hạn, và [Amazon Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html) cung cấp một lựa chọn dựa-trên-đồ-thị cho các lĩnh vực nơi bộ nhớ dài hạn được định nghĩa bởi các mối quan hệ giữa các thực thể, cho phép các truy vấn đa-bước (multi-hop) mà độ tương đồng vector không thể tự trả lời. Tách các chiến lược (được quản lý hoặc tự-lập-chỉ-mục) quan trọng cho hiệu năng, vì mỗi bản ghi không liên quan được truy xuất là latency và ngân sách ngữ cảnh chi cho nhiễu.

Các tầng chỉ hiệu năng cao khi vòng đời của chúng được tự động hóa. Trạng thái ngắn hạn không được đuổi tăng cho tới khi các lượt đọc chậm lại và các kho phiên cạn bộ nhớ, trong khi các bản ghi dài hạn không được trích xuất từ các sự kiện ngắn hạn biểu thị tri thức mà tác nhân phải học lại mỗi phiên.

Các dịch vụ được quản lý xử lý cả hai chuyển động: AgentCore Memory trích xuất các chiến lược dài hạn từ các sự kiện ngắn hạn một cách bất đồng bộ và áp TTL cho các bản ghi ngắn hạn, trong khi các ngăn xếp tự-quản-lý phải xây dựng trích xuất và đuổi một cách tường minh, hoặc bằng cách áp dụng một lớp điều phối mã nguồn mở như Mem0 hoặc bằng cách viết các pipeline riêng chế trên các nguyên hàm như ElastiCache, OpenSearch, hoặc Neptune Analytics.

Bộ nhớ dài hạn cũng phải được namespace theo actor (người dùng, phiên, hoặc tenant), vì các truy xuất không-phạm-vi-hóa trả về các bản ghi từ các actor khác làm phình ngữ cảnh và, tùy triển khai, rò rỉ thông tin qua các ranh giới cô lập. Phạm-vi-hóa vừa là một kiểm soát hiệu năng (một không gian tìm kiếm nhỏ hơn cho mỗi truy vấn trả về nhanh hơn) vừa là một kiểm soát tính đúng đắn.

### Các bước triển khai

- **Kiểm kê bộ nhớ mà tác nhân đọc và ghi:** Liệt kê các mẩu trạng thái riêng biệt mà tác nhân duy trì, ngữ cảnh N-lượt-gần-nhất, suy luận trung gian, đầu ra Tools, sở thích người dùng, tóm tắt tương-tác-trong-quá-khứ, sự kiện lĩnh vực, và với mỗi cái ghi mẫu truy cập (đọc mỗi vòng lặp, đọc mỗi phiên, đọc mỗi lớp tác vụ), yêu cầu lưu giữ (phạm-vi-phiên hoặc bền), và hình dạng truy vấn (tra cứu khóa hoặc tìm kiếm ngữ nghĩa). Bản kiểm kê này là đầu vào cho lựa chọn tầng, vì không có nó, ranh giới tầng được vẽ bằng phỏng đoán và hoặc phân mảnh dữ liệu được nhóm tự nhiên hoặc gộp các mẫu nên được tách. Ghi bản kiểm kê cùng các ngân sách hiệu năng của khối công việc để các quyết định phân tầng có thể được kiểm toán và xem lại.
- **Gán mỗi mục kiểm kê vào một tầng ngắn hạn hoặc dài hạn:** Đặt các mục phạm-vi-phiên, tần-suất-cao, tới-hạn-latency vào tầng ngắn hạn và các mục bền, liên-phiên được truy vấn ngữ nghĩa vào tầng dài hạn. Tránh các tầng "bộ nhớ làm việc" trung gian trừ khi một mẫu truy cập cụ thể biện minh cho một cái, hầu hết "bộ nhớ làm việc" hoặc là trạng thái ngắn hạn đang hoạt động hoặc là một bản ghi dài hạn chưa được trích xuất. Ghi tài liệu ranh giới tầng để mọi mục bộ nhớ mới có một nơi rõ ràng.
- **Chọn lưu trữ cho mỗi tầng dựa trên mẫu truy cập của tầng:** Cho tầng ngắn hạn, chọn [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) nếu bạn cũng muốn trích xuất dài hạn được quản lý, hoặc [Amazon ElastiCache (Valkey)](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/agentic-memory-why-elasticache.html) nếu bạn muốn sở hữu pipeline trích xuất. Cho tầng dài hạn, dùng các chiến lược tích hợp sẵn của AgentCore Memory hoặc [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application-agentic-memory.html) cho truy xuất dày và lai. Cưỡng lại việc dùng một lớp lưu trữ cho cả hai tầng. Đó là nguyên nhân phổ biến nhất của các hồi quy latency giới-hạn-bởi-bộ-nhớ.
- **Cấu hình bộ nhớ dài hạn với các chiến lược khớp những gì tác nhân truy xuất:** Bật tập con các [chiến lược dài hạn tích hợp sẵn của AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html), ngữ nghĩa, giai thoại, tóm tắt, và sở thích người dùng, tương ứng với các mẫu truy xuất trong bản kiểm kê. Mỗi chiến lược trích xuất một hình dạng bản ghi khác từ các sự kiện ngắn hạn và lập chỉ mục riêng biệt, để tác nhân có thể chỉ truy vấn kho liên quan tới bước hiện tại. Trong các ngăn xếp tự-quản-lý, tạo các chỉ mục theo-chiến-lược tương đương thay vì một kho đa-dụng duy nhất.
- **Namespace mọi bản ghi bộ nhớ theo actor của nó (người dùng, phiên, hoặc tenant):** Gắn một định danh actor vào mọi bản ghi ngắn hạn và dài hạn và lọc mọi truy xuất theo định danh đó dùng [phạm-vi-hóa actor và phiên của AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-organization.html) hoặc một bộ lọc tương đương trong các ngăn xếp tự-quản-lý. Phạm-vi-hóa giảm không gian tìm kiếm (latency truy xuất thấp hơn) và giúp ngăn rò rỉ ngữ cảnh liên-actor (tính đúng đắn và cô lập). Căn chỉnh khóa actor với danh tính xác thực mà tác nhân dùng để phạm-vi-hóa không thể bị bỏ qua bởi một bộ lọc thiếu trong mã ứng dụng.
- **Tự động hóa trích xuất từ ngắn hạn sang dài hạn và đuổi trạng thái ngắn hạn cũ:** Cấu hình pipeline trích xuất được quản lý, trích xuất chiến lược bất đồng bộ của AgentCore Memory, hoặc xây dựng một job tương đương trong các ngăn xếp tự-quản-lý đọc các sự kiện phiên, suy ra các bản ghi dài hạn theo mỗi chiến lược được bật, và ghi chúng vào chỉ mục dài hạn. Áp TTL hoặc đuổi cửa-sổ-trượt cho trạng thái ngắn hạn để các kho phiên không tăng vô giới hạn. Cả hai chuyển động phải chạy mà không cần can thiệp thủ công. Nếu cái nào cần hành động của con người, tăng trưởng bộ nhớ và trễ trích xuất sẽ vượt các mục tiêu thiết kế.
- **Phát latency truy xuất theo-tầng như một chỉ số hiệu năng hạng nhất và đặt ngân sách:** Công bố latency đọc ngắn hạn và latency truy vấn dài hạn dưới dạng các chuỗi-thời-gian riêng biệt qua [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html) hoặc một pipeline tương đương, cạnh kích thước tầng, tỷ lệ trúng, và trễ trích xuất. Phân bổ mỗi tầng một phần tường minh của ngân sách latency mỗi-vòng-lặp để bộ nhớ không thể âm thầm tiêu thời gian dành cho suy luận hoặc gọi Tools. Coi latency theo-tầng như một chỉ báo sớm: tăng trưởng bền vững trong latency truy vấn dài hạn thường báo hiệu độ trôi kích thước chỉ mục hoặc phạm vi trước khi nó ghi nhận trên các chỉ số đầu-cuối.
- **Xem lại định cỡ tầng, chiến lược, và ngân sách đối chiếu telemetry production theo nhịp định sẵn:** Lên lịch rà soát các phân phối kích thước tầng ngắn hạn, tốc độ tăng trưởng chiến lược dài hạn, trễ trích xuất, và latency theo-tầng đối chiếu ngân sách. Siết TTL trên các kho ngắn hạn bị quá cỡ một cách nhất quán, tắt các chiến lược dài hạn không bao giờ được truy vấn, và phạm-vi-hóa-lại bộ nhớ nếu các truy xuất trả về nhiều bản ghi liên-actor hơn phạm vi dự định. Các tham số phân tầng đặt lúc ra mắt hiếm khi khớp lưu lượng production trừ khi chúng được rà soát liên tục.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt](agentperf03-bp02.md)
- [AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác](agentperf03-bp03.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](agentperf03-bp04.md)
- [AGENTPERF03-BP05 Triển khai các mẫu truy xuất dạng tác nhân cho truy cập tri thức động, do-tác-nhân-điều-khiển](agentperf03-bp05.md)

**Tài liệu liên quan:**

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)
- [AgentCore Memory, tổ chức bộ nhớ](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-organization.html)
- [AgentCore Memory, các chiến lược dài hạn tích hợp sẵn](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html)
- [Bộ nhớ dạng tác nhân trong Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application-agentic-memory.html)
- [Vì sao dùng ElastiCache cho bộ nhớ dạng tác nhân](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/agentic-memory-why-elasticache.html)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)
- [Blog: Amazon Bedrock AgentCore Memory, Xây dựng tác nhân nhận-biết-ngữ-cảnh](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/)
- [Blog: Xây dựng tác nhân AI thông minh hơn, đào sâu bộ nhớ dài hạn AgentCore](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)
- [Blog: Xây dựng tác nhân học từ trải nghiệm dùng bộ nhớ giai thoại AgentCore](https://aws.amazon.com/blogs/machine-learning/build-agents-to-learn-from-experiences-using-amazon-bedrock-agentcore-episodic-memory/)
- [Blog: Xây dựng bộ nhớ bền cho ứng dụng AI dạng tác nhân với Mem0, ElastiCache for Valkey, và Neptune Analytics](https://aws.amazon.com/blogs/database/build-persistent-memory-for-agentic-ai-applications-with-mem0-open-source-amazon-elasticache-for-valkey-and-amazon-neptune-analytics/)

**Video liên quan:**

- [AWS re:Invent 2024 - Khiến tác nhân ghi nhớ với Amazon Bedrock AgentCore Memory (AIM331)](https://www.youtube.com/watch?v=Sh0Ro00_rpA)
- [AgentCore Deep Dive: Memory](https://www.youtube.com/watch?v=-N4v6-kJgwA)
- [Giải quyết chứng quên của LLM: Bộ nhớ liên phiên](https://www.youtube.com/watch?v=ZY5WXDDp9g8)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock AgentCore samples, hướng dẫn Memory](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials/04-AgentCore-memory)

**Workshop liên quan:**

- [Đào sâu vào Bedrock AgentCore, Memory](https://catalog.workshops.aws/agentcore-deep-dive/en-US/50-agentcore-memory)

**Dịch vụ liên quan:**

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
- [Amazon Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html)
