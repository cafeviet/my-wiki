# Định nghĩa

Phần này định nghĩa các thuật ngữ chính được sử dụng xuyên suốt AWS Well-Architected Agentic AI Lens. Những định nghĩa này thiết lập một vốn từ vựng chung để thảo luận về kiến trúc agentic AI và được dùng nhất quán trên tất cả các trụ cột và thực hành tốt nhất.

**Agent** — Một hệ thống phần mềm tự chủ sử dụng mô hình ngôn ngữ lớn (LLM) làm động cơ suy luận để nhận thức ngữ cảnh, lập kế hoạch hành động, thực thi tác vụ và điều chỉnh hành vi nhằm theo đuổi một mục tiêu đã xác định. Agent khác với các ứng dụng AI thông thường ở khả năng thực hiện hành động nhiều bước, gọi công cụ (**Tools**) bên ngoài, duy trì trạng thái qua các lần tương tác, và ra quyết định mà không cần chỉ thị rõ ràng của con người ở từng bước.

**Hệ thống agentic AI (agentic AI system)** — Một hệ thống phần mềm gồm một hoặc nhiều Agent cộng tác để hoàn thành các tác vụ phức tạp, nhiều bước. Các hệ thống agentic AI có thể bao gồm các Agent đơn lẻ với nhiều công cụ, các kiến trúc đa Agent nơi các Agent chuyên biệt cộng tác dưới sự điều phối, hoặc các hệ thống lai kết hợp thành phần phần mềm agentic và thông thường.

**Agentic RAG** — Một mẫu tạo sinh tăng cường truy xuất (retrieval-augmented generation) trong đó Agent chủ động kiểm soát quá trình truy xuất như một phần của vòng lặp suy luận, quyết định khi nào truy xuất, truy xuất cái gì, dùng công cụ truy xuất nào, và liệu ngữ cảnh đã truy xuất có đủ trước khi tiếp tục hay không. Không giống RAG tiêu chuẩn nơi truy xuất là một bước tiền xử lý tĩnh, agentic RAG coi truy xuất như một hành động suy luận động mà Agent gọi lặp lại dựa trên sự hiểu biết đang tiến triển về tác vụ. Các mẫu agentic RAG bao gồm truy xuất lặp, phân rã truy vấn, đánh giá tính đầy đủ của truy xuất, và truy xuất tăng cường bằng công cụ.

**Nhận thức của Agent (agent cognition)** — Quá trình suy luận mà qua đó Agent nhận thức ngữ cảnh, hình thành kế hoạch, chọn hành động và đánh giá kết quả. Nhận thức của Agent được vận hành bởi suy luận LLM và bao gồm truy xuất ngữ cảnh, xây dựng Prompt, suy luận mô hình, phân tích cú pháp đầu ra và lựa chọn hành động.

**Bộ nhớ của Agent (agent memory)** — Các cơ chế mà qua đó Agent lưu trữ và truy xuất thông tin qua các lần tương tác. Bộ nhớ của Agent thường được tổ chức thành các tầng:

- **Bộ nhớ ngắn hạn (phiên)**: Ngữ cảnh tạm thời giới hạn trong tác vụ hoặc cuộc hội thoại hiện tại, thường được lưu trong các kho in-memory tốc độ cao với hết hạn theo TTL.
- **Bộ nhớ dài hạn (bền vững)**: Tri thức bền vững tồn tại qua các phiên, bao gồm các sở thích đã học, kết quả lịch sử và tri thức miền.
- **Bộ nhớ tình tiết (episodic)**: Bản ghi về các tương tác cụ thể trong quá khứ có thể được truy xuất để thông tin cho các quyết định hiện tại.
- **Bộ nhớ ngữ nghĩa (semantic)**: Tri thức miền tổng quát được lưu dưới dạng vector embedding để truy xuất theo ngữ nghĩa.
- **Bộ nhớ thủ tục (procedural)**: Các mẫu đã học để thực thi tác vụ, giúp định hướng cách Agent tiếp cận các loại tác vụ lặp lại.

**Điều phối (orchestration)** — Sự phối hợp giữa nhiều Agent hoặc thành phần Agent để hoàn thành một tác vụ phức tạp. Điều phối có thể được triển khai bằng một Agent điều phối chuyên dụng, một công cụ luồng công việc (như AWS Step Functions), hoặc kết hợp cả hai. Các mẫu điều phối trải dài từ luồng công việc tĩnh (được định nghĩa hoàn toàn tại thời điểm thiết kế) đến điều phối đồ thị động (nơi suy luận của Agent quyết định bước tiếp theo tại thời điểm chạy).

**Danh mục Agent (agent portfolio)** — Toàn bộ tập hợp các Agent được triển khai trong một tổ chức, được quản lý như tài sản tổ chức với quyền sở hữu, năng lực, phụ thuộc, trạng thái vòng đời, hồ sơ chi phí và giá trị kinh doanh được theo dõi. Quản lý danh mục Agent cho phép các tổ chức giúp ngăn chặn sự bùng nổ tràn lan của Agent (agent sprawl), nhận diện dư thừa, quản lý các phụ thuộc liên nhóm, và ra quyết định có cơ sở về đầu tư, hợp nhất và loại bỏ.

**Agent trọng tài (arbiter agent)** — Một Agent điều phối chuyên biệt giải quyết xung đột giữa các Agent chuyên biệt, quản lý tranh chấp tài nguyên, và giúp giữ cho hành vi tập thể của một hệ thống đa Agent căn chỉnh với mục tiêu tổng thể của tác vụ.

**Tác vụ nguyên tử (atomic task)** — Một đơn vị công việc rời rạc, được xác định rõ mà một Agent có thể thực thi độc lập với đầu vào, đầu ra và tiêu chí thành công rõ ràng. Các tác vụ nguyên tử là những khối xây dựng của các kiến trúc Agent mô-đun.

**Ngắt tự động (automatic cutoff)** — Một mẫu độ tin cậy phát hiện khi một thành phần hạ nguồn đang gặp tỷ lệ lỗi hoặc độ trễ tăng cao và tạm thời dừng gửi yêu cầu đến thành phần đó, cho phép nó phục hồi mà không bị quá tải. Ngắt tự động vận hành theo ba chế độ: bình thường (yêu cầu lưu thông), chặn (yêu cầu dừng sau khi vượt ngưỡng lỗi), và dò tìm (yêu cầu thử định kỳ để phát hiện phục hồi). Còn được gọi là mẫu circuit breaker.

**Phân loại năng lực (capability taxonomy)** — Một hệ thống phân loại có cấu trúc về các năng lực của Agent, ghi lại kỹ năng, giới hạn, yêu cầu tài nguyên và ràng buộc vận hành của từng Agent. Phân loại năng lực cho phép các hệ thống điều phối ra quyết định định tuyến có cơ sở và triển khai các chiến lược dự phòng.

**Cửa sổ ngữ cảnh (context window)** — Lượng văn bản tối đa (đo bằng Token) mà một mô hình ngôn ngữ lớn có thể xử lý trong một lần suy luận. Mức sử dụng cửa sổ ngữ cảnh là một chỉ số hiệu năng và độ tin cậy chính cho các hệ thống Agent, vì vượt quá cửa sổ ngữ cảnh sẽ gây lỗi suy luận.

**Hàng đợi thư chết (dead-letter queue, DLQ)** — Một hàng đợi thông điệp thu giữ các thông điệp thất bại sau nhiều lần xử lý, giúp ngăn các thông điệp "viên độc" (poison-pill) chặn việc thực thi luồng công việc lành mạnh. DLQ là một thành phần quan trọng của các kiến trúc nhắn tin Agent có khả năng chống chịu.

**Suy giảm nhẹ nhàng (graceful degradation)** — Khả năng của một hệ thống Agent duy trì chức năng một phần khi các thành phần lỗi hoặc hiệu năng suy giảm, thay vì trải qua lỗi hệ thống hoàn toàn. Suy giảm nhẹ nhàng bao gồm phát hiện các điều kiện suy giảm, kích hoạt hành vi dự phòng, và truyền đạt về năng lực bị giảm cho người dùng.

**Guardrails** — Một cơ chế kiểm soát ràng buộc hành vi của Agent trong các ranh giới đã xác định. Guardrails có thể được triển khai ở cấp mô hình (Amazon Bedrock Guardrails), cấp ứng dụng (xác thực đầu vào/đầu ra), hoặc cấp hạ tầng (chính sách IAM và kiểm soát mạng).

**Ảo giác (hallucination)** — Một hiện tượng trong đó một mô hình ngôn ngữ lớn tạo ra thông tin nghe hợp lý nhưng sai sự thật hoặc bịa đặt. Ảo giác là một rủi ro độ tin cậy chính trong các hệ thống agentic AI, đặc biệt khi Agent ra quyết định dựa trên thông tin do mô hình tạo ra thay vì các sự kiện đã truy xuất.

**Con người trong vòng lặp (human-in-the-loop, HITL)** — Một mẫu vận hành trong đó phán đoán của con người được lồng vào các luồng công việc Agent tại các điểm quyết định đã xác định. Các luồng HITL trải từ chỉ-thông-báo (con người được thông báo nhưng không can thiệp) đến yêu-cầu-phê-duyệt (Agent không thể tiếp tục nếu không có sự cho phép rõ ràng của con người).

**Tính bất biến (idempotency)** — Thuộc tính của một thao tác tạo ra cùng kết quả khi được thực thi nhiều lần với cùng đầu vào. Các thao tác bất biến (idempotent) có thể được thử lại một cách an toàn sau lỗi mà không có nguy cơ gây tác dụng phụ lặp lại.

**Mô hình ngôn ngữ lớn (large language model, LLM)** — Một mô hình học sâu được huấn luyện trên các kho văn bản lớn, có khả năng tạo sinh, tóm tắt, dịch và suy luận về văn bản. LLM đóng vai trò là động cơ suy luận cho các Agent AI, cho phép chúng diễn giải chỉ thị, lập kế hoạch hành động và tạo phản hồi.

**MCP (Model Context Protocol)** — Một giao thức tiêu chuẩn mở để kết nối các Agent AI với các công cụ, nguồn dữ liệu và dịch vụ bên ngoài. MCP định nghĩa một giao diện chuẩn hóa cho việc khám phá công cụ, gọi công cụ và xử lý kết quả, cho phép Agent tương tác với nhiều loại công cụ mà không cần mã tích hợp tùy biến.

**Hệ thống đa Agent (multi-agent system)** — Một kiến trúc trong đó nhiều Agent chuyên biệt cộng tác để hoàn thành các tác vụ vượt quá năng lực của bất kỳ Agent đơn lẻ nào. Các hệ thống đa Agent có thể dùng điều phối phân cấp (giám sát viên–công nhân), phối hợp ngang hàng (peer-to-peer), cộng tác kiểu bầy đàn (swarm), xử lý theo đường ống (pipeline), điều phối đồ thị động, hoặc các mẫu lai kết hợp nhiều mô hình trong một luồng công việc duy nhất.

**Agent điều phối (orchestrator agent)** — Một Agent chịu trách nhiệm phân rã các tác vụ phức tạp thành các tác vụ con, ủy quyền các tác vụ con cho các Agent chuyên biệt, điều phối luồng thông tin giữa các Agent, và tổng hợp kết quả thành một đầu ra cuối cùng.

**Tiêm nhiễm Prompt (prompt injection)** — Một loại vấn đề trong đó nội dung trong đầu vào của Agent cố gắng ghi đè Prompt hệ thống của Agent hoặc khiến nó thực hiện các hành động ngoài phạm vi đã xác định. Tiêm nhiễm Prompt là một cân nhắc bảo mật chính trong các hệ thống agentic AI xử lý đầu vào không tin cậy.

**RAG (retrieval-augmented generation)** — Một kỹ thuật nâng cao đầu ra của LLM bằng cách truy xuất thông tin liên quan từ các nguồn tri thức bên ngoài và đưa vào ngữ cảnh của mô hình. RAG giảm tỷ lệ ảo giác và cải thiện độ chính xác về mặt sự kiện bằng cách neo suy luận của mô hình vào thông tin thực tế đã truy xuất.

**Mẫu saga (saga pattern)** — Một mẫu giao dịch phân tán điều phối một chuỗi các giao dịch cục bộ trên nhiều dịch vụ, với các giao dịch bù trừ được định nghĩa cho mỗi bước để cho phép cuộn ngược (rollback) khi các bước hạ nguồn thất bại. Mẫu saga thường được dùng trong các luồng công việc đa Agent để duy trì tính nhất quán dữ liệu qua các ranh giới Agent.

**Agent chuyên biệt (specialized agent)** — Một Agent được thiết kế để thực hiện một năng lực đơn lẻ, được xác định rõ với các thao tác nguyên tử. Các Agent chuyên biệt là những khối xây dựng của các hệ thống đa Agent, mỗi Agent chịu trách nhiệm một tác vụ rời rạc trong luồng công việc lớn hơn.

**Tính ngẫu nhiên (stochasticity)** — Sự ngẫu nhiên vốn có trong đầu ra của LLM khiến cùng một đầu vào tạo ra các đầu ra khác nhau qua các lần gọi. Tính ngẫu nhiên là một đặc điểm cơ bản của các Agent do LLM điều khiển và phải được tính đến trong các chiến lược về độ tin cậy và kiểm thử.

**Bầy đàn (swarm)** — Một mẫu cộng tác đa Agent trong đó nhiều Agent làm việc độc lập trên các khía cạnh chồng lấn của một vấn đề, chia sẻ các phát hiện trung gian qua một không gian làm việc chung, mà không có sự giám sát tập trung. Các mẫu bầy đàn hiệu quả cho các tác vụ hưởng lợi từ khám phá song song không gian giải pháp, các góc nhìn đa dạng, hoặc giải quyết vấn đề mang tính nổi lên (emergent). Các triển khai bầy đàn cần các biện pháp kiểm soát để ngăn công việc dư thừa, phát hiện hội tụ, và giới hạn ngân sách tài nguyên nhằm giúp ngăn tiêu thụ không giới hạn.

**Thời gian tới token đầu tiên (time-to-first-token, TTFT)** — Thời gian trôi qua giữa lúc người dùng gửi yêu cầu và lúc nhận được token đầu ra đầu tiên từ Agent. TTFT là chỉ số hiệu năng cảm nhận chính cho các tương tác Agent có tính tương tác, vì người dùng cảm nhận các Agent có TTFT thấp nhanh hơn hẳn ngay cả khi tổng thời gian xử lý là như nhau. TTFT gồm độ trễ tiền-luồng (xử lý đầu vào, truy xuất ngữ cảnh và xây dựng Prompt) và TTFT suy luận (thời gian từ lúc gọi mô hình đến token được tạo đầu tiên).

**Token** — Đơn vị văn bản cơ bản được xử lý bởi các mô hình ngôn ngữ lớn. Token gần tương ứng với các mảnh từ, với khoảng 750 từ tương đương 1.000 Token. Tiêu thụ Token là yếu tố chi phí chính cho các hệ thống Agent dựa trên LLM.

**Công cụ (Tools)** — Một hàm hoặc API mà một Agent có thể gọi để tương tác với các hệ thống bên ngoài, truy xuất thông tin hoặc thực hiện hành động. Công cụ mở rộng năng lực của Agent vượt ra ngoài tạo văn bản, bao gồm tìm kiếm web, truy vấn cơ sở dữ liệu, thực thi mã, gọi API và các thao tác khác.

**Luồng công việc (workflow)** — Một chuỗi có cấu trúc gồm các hành động của Agent, các lần gọi công cụ và các điểm quyết định hoàn thành một tác vụ phức tạp. Luồng công việc có thể được triển khai dưới dạng máy trạng thái Step Functions, các vòng lặp suy luận của Agent, hoặc kết hợp cả hai.
