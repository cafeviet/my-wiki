# Tối ưu bộ nhớ, ngữ cảnh và RAG

Các hệ thống AI dạng tác nhân phụ thuộc vào việc truy cập hiệu quả tới thông tin ngữ cảnh thông qua bộ nhớ hội thoại ngắn hạn, các kho tri thức dài hạn, các pipeline truy xuất-tăng-cường-sinh (**RAG**), và **context window** của LLM để tạo ra phản hồi chính xác, liên quan. Quản lý bộ nhớ và ngữ cảnh ảnh hưởng trực tiếp tới cả hiệu năng lẫn chất lượng. Nhồi nhét quá mức context window làm tăng **latency** suy luận và chi phí, và ngữ cảnh không đủ dẫn tới suy luận kém và ảo giác (hallucination). Tối ưu lớp này đòi hỏi triển khai các kiến trúc bộ nhớ phân tầng khớp đặc trưng lưu trữ và truy xuất với mẫu truy cập, quản lý context window để tối đa hóa mật độ thông tin mà không vượt giới hạn **token**, thiết kế các pipeline RAG truy xuất thông tin liên quan với latency tối thiểu, và thiết lập các chiến lược caching giảm các truy xuất dư thừa. Các tối ưu này quan trọng vì thao tác bộ nhớ và ngữ cảnh xảy ra trên mỗi vòng lặp suy luận, khiến hiệu quả của chúng là một hệ số nhân trên toàn vòng đời tác nhân.

| AGENTPERF03: Bạn tối ưu quản lý bộ nhớ, context window, và truy xuất-tăng-cường-sinh như thế nào? |
| --- |
|  |

## Mục tiêu năng lực

- Bộ nhớ tác nhân được tổ chức thành các tầng khớp công nghệ lưu trữ với mẫu truy cập, để các lượt đọc phiên và truy vấn ngữ nghĩa dài hạn không cạnh tranh trên cùng đường nóng.
- Context window được soạn từ các thành phần rời rạc, có-ngân-sách (chỉ dẫn hệ thống, lịch sử hội thoại, tri thức được truy xuất, và lược đồ Tools), với tóm tắt, lựa chọn Tools động, và truy xuất được-lọc-liên-quan giữ kích thước prompt tách rời khỏi độ dài phiên.
- Các pipeline truy xuất-tăng-cường-sinh kết hợp phân đoạn ngữ nghĩa (semantic chunking), tìm kiếm lai (hybrid search), biến đổi truy vấn, và tái xếp hạng (re-ranking) để tác nhân nhận được ngữ cảnh chính xác với latency dưới một giây ở lần truy xuất đầu.
- Caching đa-lớp (tiền tố prompt, kết quả truy xuất, đầu ra Tools) giảm công việc dư thừa qua các vòng lặp và phiên, với TTL và khóa được tinh chỉnh theo từng lớp đối chiếu tỷ lệ trúng đo được và mức chịu-đựng-dữ-liệu-cũ.
- Truy xuất được biểu diễn dưới dạng một tập Tools được-tác-nhân-gọi với vòng lặp có ràng buộc, kiểm tra đủ (sufficiency check), và thực thi truy-vấn-con song song để các câu hỏi phức tạp hội tụ trong ngân sách latency của khối công việc.

## Các mức trưởng thành

Các mức này tóm tắt tổng thể diện mạo của từng giai đoạn trưởng thành đối với việc tối ưu bộ nhớ, ngữ cảnh, và RAG.

| Mức | Tên | Diện mạo |
| --- | --- | --- |
| 1 | Khởi đầu (Initial) | Bộ nhớ, ngữ cảnh, và truy xuất được coi là các mối quan tâm đơn-tầng. Toàn bộ lịch sử hội thoại và toàn bộ danh mục Tools chảy vào mọi prompt, các đoạn RAG có kích thước cố định không có lọc liên quan, và không tồn tại caching ngoài những gì các dịch vụ riêng lẻ cung cấp mặc định. Mức tiêu token và latency truy xuất chỉ được xem lại sau một đợt tăng chi phí hoặc chậm-do-người-dùng-báo-cáo. |
| 2 | Manh nha (Emerging) | Các nhóm đã tách bộ nhớ ngắn hạn khỏi dài hạn và áp dụng tóm tắt cơ bản lịch sử hội thoại. RAG chạy qua một dịch vụ được quản lý như [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), và prompt được cấu trúc để chỉ dẫn hệ thống và định nghĩa Tools ổn định nằm trong một tiền tố tái dùng. Mức dùng token theo-thành-phần và latency truy xuất được đo cho các tác nhân production nhưng việc tinh chỉnh vẫn thủ công và bị động. |
| 3 | Đã định nghĩa (Defined) | Các tầng bộ nhớ dùng lưu trữ khớp với mẫu truy cập, với [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) hoặc [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html) phục vụ trạng thái ngắn hạn và [các chiến lược dài hạn của AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html) hoặc [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application-agentic-memory.html) phục vụ tri thức liên-phiên. Các pipeline RAG dùng semantic chunking, hybrid search, và một giai đoạn re-ranking, với trần top-k và ngưỡng theo-đoạn được cưỡng chế. Prompt soạn với [prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), và các mẫu prompt được phiên bản hóa trong [Amazon Bedrock Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-create.html) với ngân sách token theo-thành-phần. |
| 4 | Chủ động (Proactive) | Truy xuất được biểu diễn dưới dạng một tập Tools tác nhân qua [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) với đánh giá đủ (sufficiency evaluation), vòng lặp có ràng buộc, và thực thi truy-vấn-con song song cho các câu hỏi phức tạp. Caching đa-lớp hoạt động qua tiền tố prompt, khóa truy xuất ngữ nghĩa, và đầu ra Tools, với tỷ lệ trúng theo-lớp được giám sát đối chiếu các sàn. Trích xuất bộ nhớ, đuổi (eviction), và thăng cấp mẫu-prompt chạy qua các pipeline tự động, và latency theo-tầng cùng tỷ lệ trúng cache nạp vào tinh chỉnh liên tục trong [khả năng quan sát AI tạo sinh của Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GenAI-observability.html). |
| 5 | Tối ưu (Optimized) | Định cỡ tầng bộ nhớ, ngân sách truy xuất, và TTL cache được hiệu chỉnh liên tục từ telemetry production thay vì qua rà soát định kỳ. Các thành phần prompt, lựa chọn Tools, và định tuyến truy xuất được đánh giá qua [Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) được kiểm soát trong CI/CD, và các mẫu tối ưu chảy lại về các cộng đồng thực hành nội bộ. Tổ chức đóng góp các mẫu bộ nhớ và truy xuất cho cộng đồng AI dạng tác nhân rộng hơn. |

## Các vấn đề thường gặp cần lưu ý

- Các nhóm lưu toàn bộ bộ nhớ tác nhân trong một cơ sở dữ liệu duy nhất bất kể mẫu truy cập, buộc các lượt đọc phiên dưới-mili-giây và các tìm kiếm ngữ nghĩa quy-mô-lớn cạnh tranh trên cùng backend và làm suy giảm cả hai.
- Lịch sử hội thoại và toàn bộ danh mục Tools được đưa vào mọi prompt mà không có tóm tắt hoặc lựa chọn động, nên kích thước prompt và latency tăng tuyến tính theo độ dài phiên ngay cả sau khi thông tin ngừng hữu ích.
- Các pipeline RAG dựa vào phân đoạn kích-thước-cố-định và các đoạn top-k thô mà không có giai đoạn re-ranking hoặc ngưỡng liên quan theo-đoạn, làm loãng ngữ cảnh hữu ích với các đoạn tín-hiệu-thấp chèn ép các đoạn tín-hiệu-cao hơn.
- Caching hoặc vắng mặt hoặc được áp ở một lớp duy nhất với một TTL duy nhất, bỏ lỡ phần tiết kiệm chồng chất sẵn có khi tiền tố prompt, khóa truy xuất ngữ nghĩa, và đầu ra Tools được cache độc lập với các chính sách riêng-cho-loại-dữ-liệu.
- Các vòng lặp truy xuất dạng tác nhân chạy không có trần vòng lặp, đánh giá đủ, hoặc thực thi truy-vấn-con song song, điều này hoặc cắt các câu hỏi phức tạp quá sớm hoặc để vòng lặp tăng vô giới hạn và tiêu ngân sách latency của khối công việc.

###### Các thực hành tốt

- [AGENTPERF03-BP01 Triển khai các hệ thống quản lý bộ nhớ phân tầng](agentperf03-bp01.md)
- [AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt](agentperf03-bp02.md)
- [AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác](agentperf03-bp03.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](agentperf03-bp04.md)
- [AGENTPERF03-BP05 Triển khai các mẫu truy xuất dạng tác nhân cho truy cập tri thức động, do-tác-nhân-điều-khiển](agentperf03-bp05.md)
