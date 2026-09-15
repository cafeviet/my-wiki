# Factor 3: Own your context window (Chủ động kiểm soát Context Window)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-03-own-your-context-window.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Bạn không nhất thiết phải bị ràng buộc vào các định dạng message-based tiêu chuẩn (như OpenAI chat completions format) khi truyền ngữ cảnh (context) vào LLM.

> #### Tại bất kỳ thời điểm nào trong vòng đời của Agent, payload đầu vào gửi tới LLM về bản chất luôn là: "Đây là toàn bộ trạng thái & sự kiện đã diễn ra từ đầu đến giờ, bước xử lý tiếp theo là gì?"

<!-- ![130-own-your-context-building](/nghien-cuu/agents/12-factor-agents/assets/img/130-own-your-context-building.png) -->

`[Dịch]` **Về bản chất, mọi thứ trong kiến trúc Agent đều quy về Context Engineering (Kỹ nghệ Ngữ cảnh).** [LLM là những hàm phi trạng thái (stateless functions)](https://thedataexchange.media/baml-revolution-in-ai-engineering/) thuần túy biến đổi Input thành Output. Để thu được Output chất lượng và chính xác nhất, bạn bắt buộc phải cung cấp cho mô hình một Input Context đạt chuẩn cao nhất.

`[Dịch]` Việc kiến tạo một ngữ cảnh xuất sắc (Context Engineering) bao gồm:

- **System Prompt & Chỉ dẫn vận hành:** Persona, ràng buộc nghiệp vụ và quy chuẩn hoạt động đưa cho model.
- **Dữ liệu ngoại vi & Tài liệu truy xuất:** Bất kỳ nguồn tri thức nào được nạp động từ bên ngoài (ví dụ: qua RAG pipeline).
- **Trạng thái thực thi & Lịch sử thao tác:** Toàn bộ chuỗi state, các lệnh gọi công cụ (tool calls), tham số đầu vào và kết quả trả về trong quá khứ.
- **Ký ức ngữ cảnh (In-Context Memory):** Các message hoặc sự kiện được chắt lọc từ các phiên làm việc / luồng hội thoại liên quan nhưng độc lập.
- **Ràng buộc cấu trúc đầu ra (Structured Output Schemas):** Định nghĩa rõ ràng về schema dữ liệu mà LLM cần phản hồi.

![Mọi thứ đều là context engineering](/nghien-cuu/agents/12-factor-agents/assets/img/factor-03-context-engineering.png)

---

### Bàn về Context Engineering

`[Dịch]` Bản hướng dẫn này tập trung vào việc **khai thác tối đa năng lực của các mô hình nền tảng hiện nay**. Những giải pháp sau đây chủ ý **không** được đề cập:

- Tinh chỉnh siêu tham số mô hình như `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`, v.v.
- Tự huấn luyện (train) mô hình completion hay embedding riêng của doanh nghiệp.
- Fine-tune các mô hình mã nguồn mở hoặc thương mại sẵn có.

`[Dịch]` Nhắc lại một lần nữa: Chúng ta chưa thể khẳng định đâu là định dạng duy nhất tốt nhất để truyền context cho LLM, nhưng với tư cách là người thiết kế hệ thống, bạn cần **sự linh hoạt tuyệt đối để thử nghiệm MỌI PHƯƠNG ÁN**.

---

#### Định dạng Context Chuẩn vs Định dạng Tùy biến

`[Dịch]` Đa số các LLM client và SDK hiện nay đều ép lập trình viên sử dụng định dạng danh sách message chuẩn hóa dạng:

```yaml
[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": "Can you deploy the backend?"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "1",
        "name": "list_git_tags",
        "arguments": "{}"
      }
    ]
  },
  {
    "role": "tool",
    "name": "list_git_tags",
    "content": "{\"tags\": [{\"name\": \"v1.2.3\", \"commit\": \"abc123\", \"date\": \"2024-03-15T10:00:00Z\"}, {\"name\": \"v1.2.2\", \"commit\": \"def456\", \"date\": \"2024-03-14T15:30:00Z\"}, {\"name\": \"v1.2.1\", \"commit\": \"abe033d\", \"date\": \"2024-03-13T09:15:00Z\"}]}",
    "tool_call_id": "1"
  }
]
```

`[Dịch]` Mặc dù cấu trúc này đáp ứng tốt các tác vụ chatbot thông thường, nhưng nếu muốn **khai phóng tối đa hiệu năng và độ chuẩn xác của LLM**, bạn cần đóng gói context vào cửa sổ ngữ cảnh theo cách **tối ưu hóa ngân sách token và phân bổ cơ chế chú ý (attention budget)** hiệu quả nhất.

`[Dịch]` Thay vì bị bó buộc trong định dạng message chuẩn, bạn hoàn toàn có thể tự thiết kế **định dạng context riêng biệt được tối ưu hóa cho use-case cụ thể của mình**. Ví dụ: bạn có thể định nghĩa các đối tượng dữ liệu tùy chỉnh, sau đó gom gọn (pack) hoặc trải đều (spread) chúng vào một hoặc nhiều message `user`, `system`, `assistant`, hay `tool` tùy theo chiến lược kiến trúc của bạn.

`[Dịch]` Dưới đây là một ví dụ về việc nén toàn bộ trace ngữ cảnh vào **một User Message duy nhất** bằng cấu trúc thẻ kiểu XML:

```yaml
[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": |
        Here's everything that happened so far:

        <slack_message>
            From: @alex
            Channel: #deployments
            Text: Can you deploy the backend?
        </slack_message>

        <list_git_tags>
            intent: "list_git_tags"
        </list_git_tags>

        <list_git_tags_result>
            tags:
              - name: "v1.2.3"
                commit: "abc123"
                date: "2024-03-15T10:00:00Z"
              - name: "v1.2.2"
                commit: "def456"
                date: "2024-03-14T15:30:00Z"
              - name: "v1.2.1"
                commit: "ghi789"
                date: "2024-03-13T09:15:00Z"
        </list_git_tags_result>

        what's the next step?
  }
]
```

`[Dịch]` Mô hình có thể tự suy luận ra câu hỏi `what's the next step?` dựa vào các tool schema mà bạn cung cấp, nhưng việc gắn tường minh chỉ dẫn này vào prompt template sẽ giúp định hướng hành vi của mô hình chặt chẽ hơn.

---

### Mẫu Kiến trúc & Hiện thực Code

`[Dịch]` Trong codebase, chúng ta có thể mô hình hóa luồng xử lý này bằng cấu trúc dữ liệu tường minh:

```python
class Thread:
  events: List[Event]

class Event:
  # Có thể dùng string tự do, hoặc định kiểu chặt chẽ (discriminated union) - tùy kiến trúc hệ thống
  type: Literal[
      "list_git_tags", "deploy_backend", "deploy_frontend", 
      "request_more_information", "done_for_now", 
      "list_git_tags_result", "deploy_backend_result", 
      "deploy_frontend_result", "request_more_information_result", 
      "done_for_now_result", "error"
  ]
  data: (
      ListGitTags | DeployBackend | DeployFrontend | RequestMoreInformation |
      ListGitTagsResult | DeployBackendResult | DeployFrontendResult | 
      RequestMoreInformationResult | str
  )

def event_to_prompt(event: Event) -> str:
    data = event.data if isinstance(event.data, str) \
           else stringifyToYaml(event.data)

    return f"<{event.type}>\n{data}\n</{event.type}>"

def thread_to_prompt(thread: Thread) -> str:
    return '\n\n'.join(event_to_prompt(event) for event in thread.events)
```

#### Diễn tiến Cửa sổ Ngữ cảnh (Context Window Walkthrough)

`[Dịch]` Dưới đây là cách mà Context Window biến đổi theo từng bước thực thi trong hệ thống:

**1. Yêu cầu Slack ban đầu từ người dùng:**
```xml
<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
</slack_message>
```

**2. Sau khi Agent gọi công cụ liệt kê Git Tags:**
```xml
<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
    Thread: []
</slack_message>

<list_git_tags>
    intent: "list_git_tags"
</list_git_tags>

<list_git_tags_result>
    tags:
      - name: "v1.2.3"
        commit: "abc123"
        date: "2024-03-15T10:00:00Z"
      - name: "v1.2.2"
        commit: "def456"
        date: "2024-03-14T15:30:00Z"
      - name: "v1.2.1"
        commit: "ghi789"
        date: "2024-03-13T09:15:00Z"
</list_git_tags_result>
```

**3. Sau khi gặp lỗi kết nối và bước vào luồng phục hồi (Error Recovery):**
```xml
<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
    Thread: []
</slack_message>

<deploy_backend>
    intent: "deploy_backend"
    tag: "v1.2.3"
    environment: "production"
</deploy_backend>

<error>
    error running deploy_backend: Failed to connect to deployment service
</error>

<request_more_information>
    intent: "request_more_information_from_human"
    question: "I had trouble connecting to the deployment service, can you provide more details and/or check on the status of the service?"
</request_more_information>

<human_response>
    data:
      response: "I'm not sure what's going on, can you check on the status of the latest workflow?"
</human_response>
```

`[Dịch]` Từ payload ngữ cảnh giàu thông tin này, lời gọi quyết định bước tiếp theo sẽ rất gọn gàng và tất định:

```python
nextStep = await determine_next_step(thread_to_prompt(thread))
```

`[Dịch]` Kết quả LLM trả về cấu trúc hành động tiếp theo:

```json
{
  "intent": "get_workflow_status",
  "workflow_name": "tag_push_prod.yaml"
}
```

`[Dịch]` Định dạng thẻ XML ở trên chỉ là một ví dụ minh họa — thông điệp cốt lõi là: **bạn hoàn toàn có quyền tự xây dựng định dạng ngữ cảnh phù hợp nhất cho bài toán của mình**. Chất lượng và độ tin cậy của Agent sẽ tăng vọt nếu bạn có quyền tự do thử nghiệm các cấu trúc context khác nhau, cũng như chủ động phân tách giữa **những gì cần lưu trữ lâu dài trong cơ sở dữ liệu** và **những gì thực sự cần serialize để truyền cho LLM**.

---

### Các Lợi ích Cốt lõi của việc Làm chủ Context Window

Dưới góc độ Kiến trúc sư Giải pháp, việc kiểm soát trực tiếp Context Window mang lại 5 lợi ích chiến lược:

1. **Mật độ Thông tin (Information Density):** Tối đa hóa tỷ lệ tín hiệu trên nhiễu (Signal-to-Noise Ratio). Định dạng dữ liệu tinh gọn giúp cơ chế Attention của mô hình nắm bắt bản chất vấn đề với số lượng token ít nhất.
2. **Khả năng Phục hồi & Cắt tỉa Ngữ cảnh (Error Handling & Context Pruning):** Cung cấp chi tiết lỗi theo định dạng chuẩn hóa giúp LLM tự suy luận và phục hồi (self-heal). Đồng thời cho phép hệ thống chủ động cắt tỉa (prune) các lỗi đã giải quyết xong để tránh làm ô nhiễm không gian suy luận.
3. **An toàn & Kiểm soát Dữ liệu (Safety & Data Sanitization):** Kiểm soát chặt chẽ bề mặt dữ liệu gửi ra ngoài, dễ dàng lọc bỏ thông tin nhạy cảm (PII, credentials, token bí mật) trước khi serialize vào context window.
4. **Độ Linh hoạt & Tách biệt Tầng (Decoupling & Flexibility):** Tách rời mô hình dữ liệu nội bộ (Domain Model / Persistence Layer) khỏi mô hình biểu diễn ngữ cảnh (Prompt Representation Layer), giúp thích ứng nhanh chóng khi chuyển đổi model hoặc cải tiến schema.
5. **Tối ưu hóa Chi phí & Hiệu năng Token (Token Budget & Latency Optimization):** Giảm dung lượng context giúp hạ chi phí API, tăng tốc độ xử lý (giảm Time-to-First-Token) và hạn chế hiện tượng suy giảm chú ý ở giữa văn bản dài (*Lost in the Middle*).

> **Ghi nhớ:** Context Window là **giao diện lập trình chính (Primary Interface)** giữa hệ thống của bạn và LLM. Nắm quyền kiểm soát cách cấu trúc và biểu diễn thông tin sẽ tạo ra bước nhảy vọt về hiệu năng và độ ổn định của Agent.

![Mật độ thông tin — cùng thông điệp, ít token hơn](/nghien-cuu/agents/12-factor-agents/assets/img/factor-03-information-density.png)

---

### Sự Đồng thuận từ Cộng đồng Chuyên gia

`[Dịch]` Khoảng 2 tháng sau khi tài liệu 12-Factor Agents được công bố, thuật ngữ **Context Engineering** đã trở thành một khái niệm tiêu chuẩn trong ngành (cả Andrej Karpathy và Tobi Lütke - CEO Shopify - đều nhấn mạnh tầm quan trọng của nó):

<a href="https://x.com/karpathy/status/1937902205765607626"><img width="378" alt="Tweet của Karpathy về context engineering" src="/nghien-cuu/agents/12-factor-agents/assets/img/factor-03-karpathy-tweet.png" /></a> <a href="https://x.com/tobi/status/1935533422589399127"><img width="378" alt="Tweet của Tobi Lütke về context engineering" src="/nghien-cuu/agents/12-factor-agents/assets/img/factor-03-tobi-tweet.png" /></a>

`[Ghi chú]` Bảng tổng hợp [Context Engineering Cheat Sheet](https://x.com/lenadroid/status/1943685060785524824) xuất sắc từ [@lenadroid](https://x.com/lenadroid) (tháng 7/2025):

<a href="https://x.com/lenadroid/status/1943685060785524824"><img width="256" alt="Context Engineering Cheat Sheet của lenadroid" src="/nghien-cuu/agents/12-factor-agents/assets/img/factor-03-lenadroid-cheatsheet.png" /></a>

`[Dịch]` Thông điệp xuyên suốt: Chúng ta không đi tìm một công thức cố định duy nhất, mà xây dựng một **kiến trúc cho phép bạn sở hữu toàn quyền linh hoạt để thử nghiệm và tối ưu MỌI THỨ**.

---

**Điều hướng:** [← Factor 2: Own your prompts](./factor-02-so-huu-prompt.md) · [Mục lục](./) · [Factor 4: Tools are just structured outputs →](./factor-04-tool-chi-la-output-co-cau-truc.md)

