# AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác

Truy xuất-tăng-cường-sinh (**RAG**) cho tác nhân truy cập tri thức vượt ra ngoài dữ liệu huấn luyện của **Model**, nhưng mỗi vòng lặp suy luận truy vấn một pipeline truy xuất đều trả **latency** của nó và thừa hưởng chất lượng kết quả của nó. Một pipeline RAG được tinh chỉnh tốt trả về các đoạn liên-quan-cao trong một ngân sách latency nhỏ. Không có kỷ luật này, truy xuất hoặc chi phối latency mỗi-vòng-lặp hoặc trả về ngữ cảnh nhiễu làm suy giảm chất lượng suy luận.

**Kết quả mong muốn:**

- Bạn có một chiến lược phân đoạn (chunking) khớp với cấu trúc và hình dạng truy vấn của mỗi kho nguồn, với kích thước và ranh giới đoạn được tinh chỉnh đối chiếu độ chính xác truy xuất thay vì mặc định về một kích thước cố định duy nhất.
- Bạn có latency truy xuất được theo dõi theo từng giai đoạn (nhúng/embedding, tìm kiếm, và re-ranking) với các ngân sách tường minh để truy xuất không thể âm thầm tiêu thời gian dành cho suy luận hoặc gọi Tools.
- Bạn có truy xuất lai (hybrid) và re-ranking được dùng nơi kho và hỗn hợp truy vấn biện minh cho latency thêm của chúng, thay vì xếp chồng theo mặc định.
- Bạn có tái tạo truy vấn (query reformulation) trước mỗi lần truy xuất, để recall giữ vững khi cách diễn đạt của tác nhân phân kỳ khỏi từ vựng của kho.
- Bạn có độ chính xác và độ liên quan truy xuất được đánh giá liên tục đối chiếu một tập truy vấn đại diện để các hồi quy chất lượng được bắt trước khi chúng tới hành vi production.

**Các phản mẫu thường gặp (anti-patterns):**

- Dùng một kích thước đoạn cố định duy nhất qua mọi loại tài liệu, buộc nội dung có cấu trúc (bảng, mã, danh sách) qua cùng ranh giới như văn xuôi trôi chảy và tách thông tin liên quan qua các đoạn.
- Chuyển các kết quả truy xuất top-K thô tới LLM mà không có re-ranking hoặc lọc liên quan, để các đoạn tín-hiệu-thấp thay thế ngữ cảnh tín-hiệu-cao trong prompt của tác nhân.
- Nhúng truy vấn thô của tác nhân mà không tái tạo, bỏ sót các tài liệu liên quan dùng thuật ngữ khác với cách diễn đạt truy vấn.
- Chạy mọi truy xuất qua tìm kiếm tương đồng dày (dense) thuần túy khi kho chứa các định danh chính xác, mã, hoặc giá trị số mà tìm kiếm từ khóa (keyword) khôi phục đáng tin hơn.
- Chọn một Model nhúng một lần và không bao giờ xem lại, bỏ lỡ các phần lợi về độ chính xác từ các Model mới hơn hoặc các lựa chọn được-tinh-chỉnh-theo-lĩnh-vực.
- Coi latency truy xuất như một chỉ số duy nhất thay vì quy về các giai đoạn embedding, tìm kiếm, và re-ranking, nên các hồi quy hiệu năng không thể được khoanh vùng.

**Lợi ích khi áp dụng thực hành tốt này:**

- Quy trách nhiệm cấp-giai-đoạn và tinh chỉnh chỉ mục giữ embedding, tìm kiếm, và re-ranking trong một ngân sách mỗi-lần-truy-xuất có thể dự đoán.
- Khớp chiến lược phân đoạn với cấu trúc tài liệu, truy xuất lai nơi cần, và re-ranking trước khi phân phối ngữ cảnh giữ nhiễu ra khỏi prompt.
- Các lần truy xuất đầu-tiên độ-chính-xác-cao giảm số vòng lặp suy luận phải thử lại truy xuất với các truy vấn được tái tạo.
- Đánh giá liên tục đối chiếu một tập truy vấn đại diện phát hiện độ trôi liên quan trước khi nó tới production.
- Các lần truy xuất chặt hơn, liên quan hơn tiêu ít context window hơn, để lại nhiều ngân sách hơn cho suy luận.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Tại thời điểm nạp (ingest), bốn quyết định cố định những gì bất kỳ truy xuất tương lai nào có thể thấy trước khi một truy vấn duy nhất chạy: phân tích cú pháp (parsing), phân đoạn, nhúng, và lựa chọn [kho vector](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/introduction.html). Các giai đoạn tại-thời-điểm-truy-vấn có thể lọc và sắp xếp lại những gì ingest tạo ra, nhưng không thể phục hồi thông tin mà ingest loại bỏ. Sự bất đối xứng này là lý do kiến trúc mà các pipeline RAG không thể được tinh chỉnh như một núm duy nhất. Các lỗi được nướng vào tại ingest đòi hỏi nạp lại toàn bộ kho để sửa. Các cấu hình sai tại-thời-điểm-truy-vấn có thể được vá mà không đụng tới lưu trữ. Khi các nhà thiết kế coi RAG như một ẩn số, họ thừa hưởng cả hai phía của cam kết đó mà không thấy nó được thực hiện ở đâu.

Phân đoạn là một cam kết tại-thời-điểm-ingest không có cách sửa rẻ. Các đoạn kích-thước-cố-định phân mảnh bảng và trộn các đoạn không liên quan khi chủ đề dịch chuyển giữa-đoạn. Phân đoạn phân cấp (hierarchical chunking) bảo toàn các mối quan hệ tài-liệu-lồng-nhau nhưng gần như tăng gấp đôi dấu chân chỉ mục vì các đoạn cha được lập chỉ mục cạnh các con của chúng. Phân đoạn ngữ nghĩa (semantic chunking) ngắt theo ý nghĩa thay vì số-đếm-token và có thể bất đồng với các chuyên gia lĩnh vực về nơi một chủ đề thực sự dịch chuyển. [Phân tích cú pháp nâng cao](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-advanced-parsing.html) khôi phục các hình và bảng từ PDF trước khi phân đoạn chạy nhưng thêm một lệnh gọi foundation-model mỗi tài liệu. Làm sai bất kỳ điều nào trong số này không phải là một vấn đề tinh chỉnh tại-thời-điểm-truy-vấn, đòi hỏi nhúng-lại toàn bộ kho để sửa.

Ba giai đoạn tại-thời-điểm-truy-vấn mỗi cái chuyển latency thành độ chính xác, và Model nhúng dùng tại ingest đặt sàn cho cả ba.

- Truy xuất lai (hybrid) thêm chấm điểm BM25 cạnh tương đồng vector, khôi phục các truy vấn khớp-chính-xác nhưng tăng gấp đôi công việc giai-đoạn-đầu.
- Re-ranking chạy một Model thứ hai, nặng hơn trên một top-k rộng để giành lại các token prompt, chi mili-giây mỗi đoạn.
- Tái tạo truy vấn mở rộng một truy vấn duy nhất thành vài cái, đánh đổi latency fan-out lấy recall khi cách diễn đạt của tác nhân bỏ lỡ thuật ngữ của kho.

Xếp chồng các giai đoạn này không cho các phần lợi độ-chính-xác cộng dồn: rerank trên hybrid thường khớp với rerank trên dense-only, và tái tạo ghép với re-ranking có thể chồng lấp trong những gì mỗi cái sửa. Xếp cả ba tạo ra một lợi tức độ-chính-xác phẳng dần trước khi lớp cuối đóng góp, và một chi phí latency thì không.

Giữa một lần deploy và lần tiếp theo, các kho tăng, các Model nhúng cập nhật, các re-ranker huấn luyện lại, và các mẫu truy vấn của tác nhân dịch chuyển. Mỗi thay đổi có thể di chuyển chất lượng truy xuất theo cả hai hướng mà không có tín hiệu trong-băng. Độ trôi chỉ có thể phát hiện được đối chiếu một tập truy vấn đại diện được gán nhãn với các đoạn kỳ vọng.

Recall@k và nDCG@k định lượng liệu các đoạn đúng có được trả về hay không, và bộ ba RAG (độ liên quan ngữ cảnh, độ liên quan câu trả lời, tính căn cứ/groundedness) mở rộng phép đo tới việc liệu ngữ cảnh được truy xuất có thực sự hỗ trợ câu trả lời hay không. Tập đánh giá cũng là mối nối giữa các chủ sở hữu kho, những người cập nhật tài liệu, và các chủ sở hữu pipeline, những người tinh chỉnh giai đoạn. Không có đánh giá dùng chung, các nhóm có thể đưa lên các hồi quy mà các nhóm khác không biết.

### Các bước triển khai

- **Kiểm kê các kho nguồn và mẫu truy vấn:** Với mỗi kho tri thức mà tác nhân sẽ truy vấn, ghi loại tài liệu (văn xuôi, tài liệu phân cấp, PDF có hình, bảng có cấu trúc, mã), hình dạng truy vấn điển hình (ý định khái niệm so với định danh chính xác), lượng truy vấn kỳ vọng, và ngân sách độ-chính-xác/latency. Bản kiểm kê này dẫn dắt mọi lựa chọn hạ nguồn (chiến lược phân đoạn, Model nhúng, cấu hình chỉ mục, và vị trí re-ranker). Không có nó, pipeline được tinh chỉnh bằng phỏng đoán đối chiếu một trung bình tưởng tượng.
- **Chọn một chiến lược phân đoạn và phân tích cú pháp theo từng kho:** Với văn xuôi trôi chảy, dùng semantic chunking để ngắt theo ý nghĩa. Với tài liệu lồng nhau, dùng hierarchical chunking để bảo toàn ngữ cảnh cha-con. Với PDF và nội dung đa phương thức có hình hoặc bảng, bật [phân tích cú pháp nâng cao](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-advanced-parsing.html) qua một foundation model hoặc Amazon Bedrock Data Automation trước khi phân đoạn. Cấu hình chiến lược trong [cấu hình phân đoạn Knowledge Base](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) theo từng nguồn dữ liệu thay vì mặc định mọi nguồn về đoạn kích-thước-cố-định.
- **Chọn một Model nhúng và số chiều:** Chọn một Model nhúng bao trùm các phương thức, ngôn ngữ, và lĩnh vực của các kho và có chi phí cùng latency phù hợp ngân sách mỗi-lần-truy-xuất. [Amazon Titan Text Embeddings V2](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) phơi bày các số chiều đầu ra có thể cấu hình để kích thước chỉ mục kho-văn-bản, recall, và latency truy vấn có thể cân bằng với nhau, và [Amazon Nova Multimodal Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-amazon-nova-multimodal-embeddings.html) tạo một không gian nhúng duy nhất qua văn bản, hình ảnh, video, và âm thanh cho các kho chứa các phương thức trộn lẫn. Đánh giá lại lựa chọn khi các Model mới ra mắt, vì các cải thiện chất lượng nhúng chuyển trực tiếp thành độ chính xác truy xuất.
- **Cấu hình chỉ mục cho mẫu truy xuất:** Với các kho có cả truy vấn khái niệm lẫn khớp-chính-xác, bật hybrid search thay vì dựa vào tương đồng dày thuần túy. Với Amazon Bedrock Knowledge Bases hậu thuẫn bởi Amazon OpenSearch Service Serverless, đặt [overrideSearchType: HYBRID](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html) trên yêu cầu Retrieve để kết hợp chấm điểm vector và văn-bản-thô trong một lệnh gọi duy nhất. Với các khối công việc OpenSearch trực tiếp, cấu hình [tìm kiếm neural và hybrid](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-configure-neural-search.html) một cách tường minh. Áp bộ lọc metadata trên yêu cầu retrieve để thu hẹp không gian tìm kiếm theo nguồn tài liệu, độ mới, hoặc phạm vi trước khi tương đồng vector chạy, và tinh chỉnh [các tham số chỉ mục vector](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html) đối chiếu độ chính xác truy xuất trên một tập truy vấn đại diện để chỉ mục ưu tiên recall hoặc latency theo ngân sách của khối công việc.
- **Thêm re-ranking trước khi phân phối ngữ cảnh:** Chạy truy xuất giai-đoạn-đầu ở một top-K rộng hơn ngân sách ngữ cảnh prompt cho phép, rồi chuyển các kết quả qua [Amazon Bedrock Rerank](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html) để tạo một tập con độ-chính-xác-cao hơn. Re-ranker bù cho nhiễu tìm-kiếm-vector và cho phép LLM nhận ít hơn nhưng các đoạn liên-quan-cao hơn, việc này vừa siết chất lượng prompt vừa giảm token đầu vào. Cấu hình re-ranker trên yêu cầu retrieve của Knowledge Base thay vì điều phối nó phía-client để bước nhảy vẫn ở trong đường truy xuất.
- **Bật tái tạo truy vấn:** Biến đổi các truy vấn do-tác-nhân-tạo trước khi chúng chạm chỉ mục để truy xuất không thất bại trên các không-khớp thuật ngữ với kho nguồn. Knowledge Bases hỗ trợ [tái tạo và phân rã truy vấn](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-query-reformulation-giving-greater-control-of-accuracy-in-rag-based-applications/) qua Retrieve API, mở rộng một câu hỏi rộng thành các truy-vấn-con tập trung được thực thi đối chiếu chỉ mục. Ưu tiên đường tái tạo được quản lý hơn một bước tiền-xử-lý riêng chế để nó ở cùng với bước nhảy truy xuất và hưởng lợi từ các cải thiện tương lai của tính năng.
- **Đo latency truy xuất và độ liên quan theo-giai-đoạn:** Phát các chỉ số riêng biệt cho latency embedding, latency tìm kiếm, latency re-ranker, kích thước top-k, và phân phối điểm liên quan của các đoạn được trả về, có kích thước theo nguồn dữ liệu và lớp truy vấn. Quy trách nhiệm theo-giai-đoạn khiến việc khoanh vùng hồi quy khả thi. Một latency re-ranker tăng với latency tìm kiếm ổn định chỉ tới một nguyên nhân gốc khác với chiều ngược lại. Đặt ngân sách theo-giai-đoạn cộng lại thành mục tiêu latency đầu-cuối của pipeline để bất kỳ giai đoạn nào vượt ngân sách của nó cảnh báo trước khi hiệu năng đầu-cuối bị ảnh hưởng.
- **Đánh giá pipeline trên một tập truy vấn đại diện theo nhịp định sẵn:** Duy trì một tập đánh giá cố định trải rộng các kho và hình dạng truy vấn trong bản kiểm kê, và chạy nó đối chiếu pipeline trên mỗi thay đổi đáng kể (nguồn dữ liệu mới, thay đổi phân đoạn, nâng cấp nhúng hoặc re-ranker, tinh chỉnh tham số chỉ mục), theo cách tiếp cận trong [Đánh giá và cải thiện hiệu năng của Amazon Bedrock Knowledge Bases](https://aws.amazon.com/blogs/machine-learning/evaluate-and-improve-performance-of-amazon-bedrock-knowledge-bases/). Theo dõi Recall@k, nDCG@k, và điểm bộ ba RAG mỗi thay đổi để các hồi quy chất lượng được bắt trước khi triển khai, và làm mới tập đánh giá khi các mẫu truy vấn thực trôi dạt.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP01 Triển khai các hệ thống quản lý bộ nhớ phân tầng](agentperf03-bp01.md)
- [AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt](agentperf03-bp02.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](agentperf03-bp04.md)
- [AGENTPERF03-BP05 Triển khai các mẫu truy xuất dạng tác nhân cho truy cập tri thức động, do-tác-nhân-điều-khiển](agentperf03-bp05.md)

**Tài liệu liên quan:**

- [Amazon Bedrock Knowledge Bases, Cách phân đoạn nội dung hoạt động](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
- [Amazon Bedrock Knowledge Bases, Các tùy chọn phân tích cú pháp cho nguồn dữ liệu](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-advanced-parsing.html)
- [Amazon Bedrock Knowledge Bases, Cấu hình truy vấn](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html)
- [Amazon Bedrock, Cải thiện độ liên quan của phản hồi truy vấn bằng một Model re-ranker](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html)
- [Các Model Amazon Titan Text Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
- [Amazon Nova Multimodal Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-amazon-nova-multimodal-embeddings.html)
- [Amazon OpenSearch Service, Tìm kiếm vector](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html)
- [Amazon OpenSearch Service Serverless, Cấu hình Neural Search và Hybrid Search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-configure-neural-search.html)
- [Blog: Amazon Bedrock Knowledge Bases, phân tích cú pháp nâng cao, phân đoạn, và tái tạo truy vấn](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-query-reformulation-giving-greater-control-of-accuracy-in-rag-based-applications/)
- [Blog: Đánh giá và cải thiện hiệu năng của Amazon Bedrock Knowledge Bases](https://aws.amazon.com/blogs/machine-learning/evaluate-and-improve-performance-of-amazon-bedrock-knowledge-bases/)
- [Chọn một cơ sở dữ liệu vector AWS cho các trường hợp dùng RAG](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/introduction.html)

**Video liên quan:**

- [AWS re:Invent 2025 - Các hệ thống RAG dạng tác nhân nâng cao: Đào sâu với Amazon Bedrock (AIM425)](https://www.youtube.com/watch?v=bu2cD1pCFTs)

**Ví dụ liên quan:**

- [GitHub: Amazon Bedrock samples, Knowledge Bases và RAG](https://github.com/aws-samples/amazon-bedrock-samples)

**Công cụ liên quan:**

- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
