# AGENTPERF03-BP02 Tối ưu sử dụng context window và quản lý prompt

Mỗi **Token** gửi tới một LLM cạnh tranh cho sự chú ý của Model, tiêu thụ chi phí token-đầu-vào, và thêm **latency** suy luận, điều này khiến nội dung prompt trở thành một đòn bẩy hiệu năng bậc-nhất. Quản lý **context window** hiệu quả phân bổ ngân sách token qua các thành phần prompt, lắp ráp chỉ những gì tác vụ hiện tại cần, và nén hoặc tóm tắt phần còn lại. Không có kỷ luật này, lịch sử hội thoại và lược đồ **Tools** chèn ép năng lực suy luận và phình latency trên mỗi vòng lặp.

**Kết quả mong muốn:**

- Bạn có một ngân sách token tường minh được phân bổ qua các thành phần prompt, chỉ dẫn hệ thống, lịch sử hội thoại, tri thức được truy xuất, và lược đồ Tools, với mức dùng token theo-thành-phần được đo trên mọi yêu cầu.
- Bạn có ngữ cảnh được lắp ráp động theo từng yêu cầu, chỉ bao gồm các định nghĩa Tools, các đoạn được truy xuất, và ngữ cảnh hội thoại liên quan tới tác vụ hiện tại thay vì một payload cực-đại cố định.
- Bạn có lịch sử hội thoại bị giới hạn bởi tóm tắt, cửa sổ trượt, hoặc nén ngữ nghĩa để kích thước prompt không tăng tuyến tính theo độ dài phiên.
- Bạn có các mẫu prompt được phiên bản hóa và đánh giá để các thay đổi về cách diễn đạt, thứ tự, hoặc thành phần được đo đối chiếu các đường cơ sở chất lượng và chi-phí-token trước khi triển khai.

**Các phản mẫu thường gặp (anti-patterns):**

- Bao gồm toàn bộ lịch sử hội thoại trong mọi prompt mà không có tóm tắt hoặc cắt bớt, khiến kích thước prompt và latency suy luận tăng tuyến tính theo độ dài phiên.
- Đưa toàn bộ danh mục Tools vào mọi prompt bất kể độ liên quan tới tác vụ, chi ngân sách ngữ cảnh cho các lược đồ mà tác nhân sẽ không gọi cho yêu cầu hiện tại.
- Chuyển các truy xuất RAG thẳng vào prompt mà không lọc hoặc cắt bớt theo-đoạn, nên các đoạn liên-quan-thấp thay thế ngữ cảnh hữu ích hơn.
- Coi prompt như một chuỗi mờ đục duy nhất thay vì một hợp thành các thành phần, khiến không thể quy mức tiêu token về chỉ dẫn hệ thống, lịch sử, truy xuất, hoặc lược đồ Tools.
- Đưa các thay đổi prompt lên mà không phiên bản hóa hoặc đánh giá song-song, nên các hồi quy chất lượng hoặc chi-phí-token chỉ được phát hiện sau khi triển khai.

**Lợi ích khi áp dụng thực hành tốt này:**

- Loại token khỏi prompt có thể giảm chi phí yêu cầu và rút ngắn time-to-first-token trên mỗi vòng lặp.
- Ngữ cảnh được cắt tỉa, mật-độ-cao để nhiều sự chú ý hiệu quả của Model hơn dồn vào tác vụ hiện tại thay vì phân tích lịch sử cũ hoặc lược đồ Tools không dùng.
- Các chiến lược tóm tắt và cửa-sổ-trượt tách rời kích thước prompt khỏi độ dài hội thoại, giữ latency và chi phí mỗi-lượt ổn định.
- Các prompt ổn định, cấu-trúc-theo-thành-phần với tiền tố bất biến soạn với prompt caching, biến một phần lớn token đầu vào thành các lượt đọc được cache với một phần nhỏ chi phí đầu vào chuẩn.
- Các mẫu được phiên bản hóa với cổng đánh giá cho phép các thay đổi prompt đi kèm bằng chứng chất lượng và chi phí thay vì bằng phỏng đoán.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Prompt hoạt động như các hợp thành của các thành phần rời rạc, chỉ dẫn hệ thống, lược đồ Tools, tri thức được truy xuất, lịch sử hội thoại, và lượt người dùng hiện tại. Coi chúng như một chuỗi mờ đục duy nhất khiến sự tăng trưởng mất-kiểm-soát không thể quy trách nhiệm. Quy trách nhiệm token theo-thành-phần trên mọi yêu cầu làm sáng tỏ các vấn đề, như một danh mục Tools tăng gấp đôi khi một Tool mới được đăng ký. Các ngân sách cấp-thành-phần cộng lại thành mục tiêu độ-dài-đầu-vào của khối công việc khiến các đánh đổi tường minh: nhiều ngân sách hơn cho truy xuất nghĩa là ít hơn cho lịch sử, và mỗi lần tái phân bổ trở thành một quyết định có chủ đích.

[Hướng dẫn thiết kế prompt của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html) mô tả cách các chỉ dẫn rõ ràng, chỉ báo đầu ra, và đặt câu hỏi ở cuối prompt định hình các thành phần chỉ-dẫn-hệ-thống và lượt-người-dùng riêng lẻ.

Các token rẻ nhất là các token không bao giờ được gửi. Hầu hết các tác nhân đăng ký nhiều Tools hơn bất kỳ lượt nào sẽ gọi tới, nên đưa toàn bộ danh mục Tools vào mọi yêu cầu chi ngân sách ngữ cảnh cho các lược đồ mà Model bỏ qua. [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-advanced-performance.html) xử lý điều này bằng tìm kiếm ngữ nghĩa chỉ trả về các Tools liên quan tới ý định người dùng hiện tại.

Ngữ cảnh truy-xuất-tăng-cường chịu cùng chế độ lỗi, chuyển các đoạn top-K thô vào prompt mà không có ngưỡng liên quan hoặc trần theo-đoạn cho phép các đoạn tín-hiệu-thấp thay thế ngữ cảnh tín-hiệu-cao hơn.

Lịch sử hội thoại là nguồn phình thứ ba: [SummaryMemoryStrategy trong Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html#long-term-session-summaries-strategy) duy trì một tóm tắt theo-phiên đang chạy thay thế các lượt thô sau khi phiên vượt một ngưỡng, tách rời kích thước prompt khỏi độ dài phiên để latency mỗi-lượt vẫn ổn định khi hội thoại tăng.

Các tiền tố tĩnh mở khóa phần tiết kiệm token-đầu-vào lớn, lặp lại. [Prompt caching của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) chấp nhận các điểm kiểm tra cache trong các trường system, tools, và messages trên Converse API, với các lượt đọc cache tính phí ở mức giảm trên một TTL mặc định 5 phút, hoặc một TTL 1 giờ trên Claude Opus 4.5, Haiku 4.5, và Sonnet 4.5 cho lưu lượng tác nhân chạy-dài hoặc gián đoạn.

Nội dung bất biến (chỉ dẫn hệ thống, định nghĩa Tools ổn định, và ngữ cảnh được ghim) thuộc về trước điểm kiểm tra, và nội dung biến thiên (lượt người dùng hiện tại và các truy xuất riêng-của-phiên) thuộc về sau nó để tiền tố được cache vẫn giống hệt qua các lượt. Quản lý cache đơn giản hóa cho các Model Claude nhìn lại khoảng 20 khối nội dung cho tiền tố khớp dài nhất, nên nội dung được-tái-dùng-nhiều-nhất nên nằm trong phạm vi đó.

Prompt hoạt động như mã, nên một thay đổi về cách diễn đạt, thứ tự thành phần, hoặc một mô tả Tool có thể dịch chuyển chất lượng, số đếm token, và tỷ lệ trúng cache đồng thời, trong khi các hiệu ứng vẫn vô hình cho tới khi triển khai trừ khi chúng được đo. [Amazon Bedrock Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-create.html) lưu prompt dưới dạng các hiện vật được phiên bản hóa với biến, cấu hình suy luận, và cài đặt prompt-caching tùy chọn, và so-sánh-biến-thể trên console của nó hiển thị khác biệt chất lượng và token cạnh nhau trước khi thăng cấp.

[Prompt Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-optimize.html) tạo các bản viết lại riêng-của-Model phục vụ như các biến thể ứng viên thay vì thay thế trực tiếp, và các benchmark chất lượng cộng chi-phí-token trên các tập kiểm thử đại diện nên kiểm soát việc thăng cấp bất kỳ biến thể nào.

### Các bước triển khai

- **Định nghĩa phân loại thành phần prompt và ngân sách token theo-thành-phần:** Phân rã mọi prompt thành một tập cố định các thành phần, chỉ dẫn hệ thống, lược đồ Tools, tri thức được truy xuất, lịch sử hội thoại, và lượt người dùng hiện tại, và phân bổ một ngân sách token cho mỗi cái cộng lại thành mục tiêu độ-dài-đầu-vào suy ra từ SLO latency và chi phí của khối công việc. Áp [hướng dẫn thiết kế prompt của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html) để giữ thành phần chỉ-dẫn-hệ-thống rõ ràng, súc tích, và nhất quán với truy vấn người dùng đặt ở cuối prompt.
- **Đo mức dùng token theo-thành-phần trên mọi yêu cầu:** Phát số đếm token cho mỗi thành phần dưới dạng log có cấu trúc hoặc chỉ số CloudWatch cạnh inputTokens và outputTokens trả về bởi [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), có kích thước theo agent ID và loại tác vụ. Bao gồm cacheReadInputTokens và cacheWriteInputTokens từ phản hồi Converse để hiệu quả cache được đo cạnh tăng trưởng thành phần, và cảnh báo khi bất kỳ thành phần nào có xu hướng ra ngoài ngân sách của nó trước khi nó tác động tới SLO đầu-cuối.
- **Lắp ráp lược đồ Tools động với lựa chọn đúng-lúc (just-in-time):** Thay việc đưa toàn-danh-mục bằng lựa chọn liên-quan-tới-tác-vụ để prompt chỉ mang các Tools mà tác nhân có thể gọi cho lượt hiện tại. Với các tác nhân dùng [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-advanced-performance.html), bật tìm kiếm ngữ nghĩa bằng cách đặt "searchType": "SEMANTIC" trên giao thức mcp trong protocolConfiguration của gateway để truy xuất Tools thu hẹp theo ý định người dùng. Giữ lược đồ mỗi Tool gọn với mô tả tham số rõ ràng và các trường bắt buộc để giảm trọng số token mỗi-lần-gọi của nó.
- **Giới hạn lịch sử hội thoại bằng tóm tắt và một cửa sổ trượt:** Chặn việc lưu giữ lượt-thô và thay các lượt cũ hơn bằng một tóm tắt đang chạy sau khi phiên vượt một ngưỡng biểu thị bằng số lượt hoặc token. Cấu hình [SummaryMemoryStrategy trong Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html#long-term-session-summaries-strategy) với một mục namespaceTemplates như /summaries/{actorId}/{sessionId}/ và đưa tóm tắt thay vì bản ghi thô vào prompt, ghép với một cửa sổ trượt nhỏ các lượt gần đây để bảo toàn chi tiết hội thoại gần-hạn.
- **Lọc và cắt bớt các đoạn được truy xuất trước khi lắp ráp prompt:** Áp một ngưỡng liên quan, một trần token theo-đoạn, và một ngân sách truy xuất tổng để các đoạn tín-hiệu-thấp không thể thay thế ngữ cảnh tín-hiệu-cao hơn. Xếp hạng các đoạn theo điểm liên quan, bỏ bất kỳ đoạn nào dưới ngưỡng, và cắt bớt các đoạn dài về trần theo-đoạn trước khi soạn thành phần tri-thức-được-truy-xuất.
- **Cấu trúc prompt để chúng soạn với prompt caching:** Sắp xếp mọi prompt để nội dung bất biến (chỉ dẫn hệ thống, định nghĩa Tools ổn định, tài liệu tham chiếu được ghim) xuất hiện trước nội dung biến thiên (lượt người dùng, truy xuất mỗi-yêu-cầu), rồi đặt [các điểm kiểm tra prompt cache của Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) trong các trường system, tools, và messages tại ranh giới giữa nội dung tĩnh và động. Với các phiên chạy-dài hoặc gián đoạn trên các Model Claude được hỗ trợ, đặt "ttl": "1h" trên cachePoint để mở rộng cửa sổ cache vượt mặc định 5 phút, giữ mục 1-giờ trước bất kỳ mục 5-phút nào trong cùng yêu cầu.
- **Phiên bản hóa prompt và kiểm soát các thay đổi trên đánh giá:** Lưu prompt dưới dạng các hiện vật được phiên bản hóa trong [Amazon Bedrock Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-create.html) với biến cho các đầu vào động và cấu hình suy luận gắn với phiên bản, rồi dùng [Tạo phiên bản](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-version-create.html) để chụp nhanh các bản nháp được-biết-là-tốt. Dùng so sánh biến thể cạnh nhau trong trình dựng prompt để đánh giá các ứng viên với nhau, và thăng cấp một phiên bản mới chỉ sau khi nó vượt các đường cơ sở chất lượng và chi-phí-token trên một tập kiểm thử đại diện.
- **Tạo các bản viết lại được-tinh-chỉnh-theo-Model với prompt optimization:** Chạy các prompt ứng viên qua [Amazon Bedrock Prompt Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-optimize.html) để tạo các bản viết lại riêng-của-Model, truyền Model đích qua targetModelId khi dùng OptimizePrompt API. Coi đầu ra được tối ưu như một biến thể ứng viên thay vì thay thế trực tiếp, và so sánh nó với bản gốc trên cùng tập đánh giá để cân nhắc phần giảm số-đếm-token với bất kỳ tác động chất lượng nào trước khi thăng cấp.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTPERF03-BP01 Triển khai các hệ thống quản lý bộ nhớ phân tầng](agentperf03-bp01.md)
- [AGENTPERF03-BP03 Tối ưu các pipeline truy xuất RAG cho latency và độ chính xác](agentperf03-bp03.md)
- [AGENTPERF03-BP04 Thiết lập các mẫu caching và truy cập dữ liệu tác nhân hiệu quả](agentperf03-bp04.md)
- [AGENTPERF06-BP01 Thiết kế các chiến lược tích hợp Tools được tối ưu](../6-agentperf06/agentperf06-bp01.md)

**Tài liệu liên quan:**

- [Amazon Bedrock, Prompt caching cho suy luận Model nhanh hơn](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- [Amazon Bedrock, Tạo một prompt dùng Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-create.html)
- [Amazon Bedrock, Tạo một phiên bản của prompt trong Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-version-create.html)
- [Amazon Bedrock, Tối ưu một prompt](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-optimize.html)
- [Amazon Bedrock, Thiết kế một prompt](https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html)
- [AgentCore Gateway, Tối ưu hiệu năng (lược đồ Tools tinh chỉnh và tìm kiếm ngữ nghĩa)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-advanced-performance.html)
- [AgentCore Memory, Các chiến lược dài hạn tích hợp sẵn (ngữ nghĩa, giai thoại, tóm tắt, sở thích người dùng)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html)
- [Nền tảng của AI dạng tác nhân trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/introduction.html)

**Dịch vụ liên quan:**

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
