---
title: "Bắt đầu với AgentCore Memory"
source: "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-get-started.html"
---

# Bắt đầu với AgentCore Memory

Amazon Bedrock AgentCore Memory cho phép bạn tạo và quản lý các tài nguyên AgentCore Memory lưu trữ ngữ cảnh hội thoại cho các agent (tác tử AI) của bạn. Hướng dẫn bắt đầu này dẫn bạn qua việc cài đặt các dependency và triển khai cả tính năng bộ nhớ ngắn hạn (short-term memory) lẫn dài hạn (long-term memory). Hướng dẫn sử dụng AgentCore CLI.

Các bước như sau:

- Tạo một AgentCore Memory chứa một semantic strategy

- Ghi các event (lịch sử hội thoại) vào tài nguyên memory

- Truy xuất các memory record từ bộ nhớ dài hạn

Để xem các ví dụ khác, xem [Ví dụ về Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html).

## Điều kiện tiên quyết

Trước khi bắt đầu, hãy chắc chắn bạn có:

- **AWS Account** với thông tin xác thực đã cấu hình ( `aws configure` )

- **Python 3.10+** đã cài đặt

- Node.js 20+ đã cài đặt (cho AgentCore CLI)

Để bắt đầu với Amazon Bedrock AgentCore Memory, hãy cài đặt các dependency, tạo một dự án AgentCore CLI, và thiết lập một virtual environment. Các lệnh sau có thể được chạy trực tiếp trong terminal.

```bash
npm install -g @aws/agentcore
agentcore create --project-name MemoryQuickstart --no-agent
cd MemoryQuickstart
python -m venv .venv
source .venv/bin/activate
pip install bedrock-agentcore
```

AgentCore CLI cung cấp các lệnh để tạo và quản lý các tài nguyên memory. Dùng `agentcore add memory` để tạo một memory, và `agentcore deploy` để cấp phát nó trên AWS. Đối với các thao tác event và quản lý session, dùng AgentCore Python SDK (`bedrock-agentcore`).

###### Lưu ý

AgentCore CLI giúp bạn tạo và deploy các tài nguyên memory. Đối với các thao tác API dịch vụ trực tiếp, xem tài liệu Boto3: [bedrock-agentcore-control](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html) và [bedrock-agentcore](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html).

**Ví dụ đầy đủ:** Xem [các mẫu Amazon Bedrock AgentCore](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/04-manage-context-of-your-agent/memory) minh họa các bước 1-3.

## Bước 1: Tạo một AgentCore Memory

Bạn cần một AgentCore Memory để bắt đầu lưu trữ thông tin cho agent của mình. Theo mặc định, các memory event (mà chúng ta gọi là bộ nhớ ngắn hạn) có thể được ghi vào một AgentCore Memory. Để các insight được trích xuất và đưa vào các long term memory record, tài nguyên cần một *memory strategy* — một cấu hình định nghĩa cách dữ liệu hội thoại nên được xử lý, và thông tin nào cần trích xuất (chẳng hạn các fact, preference, hoặc summary).

Trong bước này, bạn tạo một AgentCore Memory với một semantic strategy để cả bộ nhớ ngắn hạn lẫn dài hạn đều có thể được sử dụng. Việc này sẽ mất 2-3 phút. Bạn cũng có thể tạo các tài nguyên AgentCore Memory trong AWS console.

Tạo memory với semantic strategy:

- `agentcore add memory --name CustomerSupportSemantic --strategies SEMANTIC
agentcore deploy`

- Chạy `agentcore` để mở TUI, sau đó chọn **add** và chọn **Memory** :

- Nhập tên memory:

- Chọn strategy **Semantic**, sau đó xác nhận:

  Rồi chạy `agentcore deploy` để cấp phát memory trên AWS.

Sau khi deploy, xác minh memory đã được tạo:

```bash
agentcore status
```

## Bước 2: Ghi các event vào memory

Bạn có thể ghi các event vào một AgentCore Memory dưới dạng bộ nhớ ngắn hạn, và nó trích xuất các insight cho bộ nhớ dài hạn.

Việc ghi event vào memory có nhiều mục đích. Thứ nhất, nội dung event (thường gặp nhất là lịch sử hội thoại) được lưu dưới dạng bộ nhớ ngắn hạn. Thứ hai, các insight liên quan được rút ra từ các event và ghi vào các memory record như một phần của bộ nhớ dài hạn.

Cần có memory resource id, actor id, và session id để tạo một event. Trong bước này, bạn tạo ba event, mô phỏng các message giữa một người dùng cuối và một chat bot.

```python
import boto3
from bedrock_agentcore.memory import MemorySessionManager
from bedrock_agentcore.memory.constants import ConversationalMessage, MessageRole

control_client = boto3.client('bedrock-agentcore-control', region_name='us-west-2')

# Retrieve the memory created in Step 1
response = control_client.list_memories()
memory = response['memories'][0]
memory_id = memory['id']

# Create a session to store memory events
session_manager = MemorySessionManager(
    memory_id=memory_id,
    region_name="us-west-2")

session = session_manager.create_memory_session(
    actor_id="User1",
    session_id="OrderSupportSession1"
)

# Write memory events (conversation turns)
session.add_turns(
    messages=[
        ConversationalMessage(
            "Hi, how can I help you today?",
            MessageRole.ASSISTANT)],
)

session.add_turns(
    messages=[
        ConversationalMessage(
            "Hi, I am a new customer. I just made an order, but it hasn't arrived. The Order number is #35476",
            MessageRole.USER)],
)

session.add_turns(
    messages=[
        ConversationalMessage(
            "I'm sorry to hear that. Let me look up your order.",
            MessageRole.ASSISTANT)],
)
```

Bạn có thể lấy các event (turn) cho một actor cụ thể sau khi chúng đã được ghi.

```python
# Get the last k turns in the session
turns = session.get_last_k_turns(k=5)

for turn in turns:
    print(f"Turn: {turn}")
```

Trong trường hợp này, bạn có thể thấy ba event gần nhất cho actor và session.

## Bước 3: Truy xuất các record từ bộ nhớ dài hạn

Sau khi các event được ghi vào tài nguyên memory, chúng được phân tích và thông tin hữu ích được gửi vào bộ nhớ dài hạn. Vì memory chứa một semantic long term memory strategy, hệ thống trích xuất và lưu trữ thông tin dạng fact.

Bạn có thể liệt kê tất cả các memory record với:

```python
# List all memory records
memory_records = session.list_long_term_memory_records(
    namespace_path="/"
)

for record in memory_records:
    print(f"Memory record: {record}")
    print("--------------------------------------------------------------------")
```

Hoặc yêu cầu thông tin liên quan nhất như một phần của tìm kiếm ngữ nghĩa (semantic search):

```python
# Perform a semantic search
memory_records = session.search_long_term_memories(
    query="can you summarize the support issue",
    namespace_path="/",
    top_k=3
)
```

Thông tin quan trọng về người dùng có khả năng được lưu trong bộ nhớ dài hạn. Các agent có thể dùng bộ nhớ dài hạn thay vì toàn bộ lịch sử hội thoại để đảm bảo các LLM không bị quá tải với ngữ cảnh.

## Thêm memory vào một agent hiện có

Nếu bạn đã tạo một Strands agent không có memory và muốn thêm sau, làm theo các bước sau:

- Thêm một tài nguyên memory vào dự án của bạn:
  `agentcore add memory --name MyMemory --strategies SEMANTIC,SUMMARIZATION
agentcore deploy`

- Tạo thư mục `memory/` trong agent của bạn:
  `mkdir -p app/MyAgent/memory`

- Tạo `app/MyAgent/memory/session.py` :
  `import os
from typing import Optional
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

MEMORY_ID = os.getenv("MEMORY_MYMEMORY_ID")
REGION = os.getenv("AWS_REGION")

def get_memory_session_manager(session_id: str, actor_id: str) -> Optional[AgentCoreMemorySessionManager]:
    if not MEMORY_ID:
        return None

    retrieval_config = {
        f"/users/{actor_id}/facts": RetrievalConfig(top_k=3, relevance_score=0.5),
        f"/summaries/{actor_id}/{session_id}": RetrievalConfig(top_k=3, relevance_score=0.5)
    }

    return AgentCoreMemorySessionManager(
        AgentCoreMemoryConfig(
            memory_id=MEMORY_ID,
            session_id=session_id,
            actor_id=actor_id,
            retrieval_config=retrieval_config,
        ),
        REGION
    )`

- Cập nhật `main.py` để dùng session manager:
  `from memory.session import get_memory_session_manager

@app.entrypoint
async def invoke(payload, context):
    session_id = getattr(context, 'session_id', 'default-session')
    user_id = getattr(context, 'user_id', 'default-user')

    agent = Agent(
        model=load_model(),
        session_manager=get_memory_session_manager(session_id, user_id),
        system_prompt="You are a helpful assistant.",
    )

    response = agent(str(payload.get("prompt", "")))
    return response`

- Deploy dự án đã cập nhật:
  `agentcore deploy`

###### Lưu ý

Mỗi tài nguyên memory nhận được một biến môi trường `MEMORY__ID` (viết hoa, kèm dấu gạch dưới) tự động có sẵn trong môi trường runtime của agent sau khi deploy.

## Dọn dẹp

Khi bạn đã dùng xong tài nguyên memory, bạn có thể xóa nó:

```bash
agentcore remove memory --name CustomerSupportSemantic
agentcore deploy
```

## Các bước tiếp theo

Hãy cân nhắc các mục sau:

- [Thêm một strategy khác](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-enabling-long-term-memory.html#long-term-adding-strategies-to-existing-memory) vào tài nguyên memory của bạn.

- [Bật observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-observability.html) để có nhiều tầm nhìn hơn về cách memory hoạt động

- Xem thêm các [ví dụ](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html).
