# Quản trị và kiến trúc cho sự đa dạng của AI tác tử ở quy mô lớn

> **Bản dịch tiếng Việt từ:** [Governing and architecting the diversity of agentic AI at scale](https://docs.aws.amazon.com/prescriptive-guidance/latest/govern-architect-agentic-ai/introduction.html), AWS Prescriptive Guidance, Amazon Web Services.
> **Tác giả:** Jocelyn Pinault, Massimiliano Angelino, Sebastien Grazzini, Florent Lacroute, và Lior Perez (AWS).
> **Ngày xuất bản nguồn:** 23/04/2026.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên sản phẩm, giao thức và kỹ thuật (AWS, Amazon Bedrock AgentCore, Kiro, MCP, A2A, LLM...) được giữ nguyên.

Hướng dẫn này giải quyết một thách thức then chốt với bất kỳ tổ chức nào triển khai AI ở quy mô lớn: làm thế nào để **quản trị (govern)** và kiến trúc hóa sự đa dạng ngày càng tăng của **AI tác tử (agentic AI)** trên phạm vi toàn tổ chức, chứ không chỉ trong từng khối lượng công việc (workload) hay dự án riêng lẻ. Khi các tổ chức triển khai ngày càng nhiều loại **tác tử AI (AI agent)** khác nhau — từ các chatbot đơn giản đến các hệ thống tự chủ phục vụ khách hàng — họ cần những chiến lược mạch lạc, bao trùm nhiều trường hợp sử dụng (use case), nhiều nhóm và nhiều đơn vị kinh doanh.

## Đối tượng độc giả

Hướng dẫn này được thiết kế cho CIO, CTO, VP AI, các **kiến trúc sư doanh nghiệp (enterprise architect)**, các lãnh đạo về **quản trị AI (AI governance)**, các **kỹ sư nền tảng (platform engineer)** và những người ra quyết định kỹ thuật — những người cần mở rộng quy mô agentic AI trên toàn tổ chức trong khi vẫn duy trì khả năng kiểm soát và tuân thủ (compliance).

## Mục tiêu

Việc hiểu cách quản trị và kiến trúc hóa agentic AI ở quy mô lớn đòi hỏi một cách tiếp cận có cấu trúc, đi từ sự rõ ràng về khái niệm đến triển khai thực tiễn.

**Phân loại trường hợp sử dụng (Use case typologies)** xem xét toàn bộ phổ các kiểu trường hợp sử dụng, từ các chatbot đơn giản và **trợ lý AI cá nhân (personal AI assistant)** cho đến các **tác tử nhóm tự chủ (autonomous team agent)** và các ứng dụng phục vụ khách hàng. Mỗi nhóm đòi hỏi mức độ chặt chẽ về quản trị và các mẫu kiến trúc khác nhau.

**Quản trị AI tác tử (Agentic AI governance)** khảo sát các khung quản trị bao gồm quản lý sổ đăng ký (registry) tác tử/công cụ/MCP, quản lý mô hình LLM, các tiêu chuẩn nền tảng, kiểm soát truy cập đa cấp và các yêu cầu kiểm toán (audit). Phần này trình bày ba mô hình quản trị — tập trung (centralized), liên bang (federated) và lai (hybrid) — và đề cập việc trao quyền cho **nhà phát triển công dân (citizen developer)**.

**Kiến trúc AI tác tử trong doanh nghiệp (Agentic AI architecture in the enterprise)** trình bày các lớp (layer) riêng biệt bao gồm: lớp ứng dụng (các giải pháp GenAI như Amazon Quick Suite và Kiro, cùng các tích hợp hệ thống nghiệp vụ), lớp tác tử (các dịch vụ Amazon Bedrock AgentCore cho runtime và điều phối), và các dịch vụ lõi (truy cập mô hình, công cụ và cơ sở tri thức).

Cấu trúc này phản ánh một thực tế quan trọng: các yêu cầu về quản trị và kiến trúc tiến hóa theo mức độ trưởng thành của tổ chức. Dù các yếu tố nền tảng như bảo mật áp dụng phổ quát, các yếu tố khác — như độ chặt chẽ về tuân thủ, tiêu chuẩn độ tin cậy và độ chính xác đầu ra — sẽ gia tăng khi việc triển khai dịch chuyển từ các công cụ năng suất nội bộ sang các ứng dụng phục vụ khách hàng. Hãy sử dụng hướng dẫn này dựa trên giai đoạn trưởng thành của doanh nghiệp bạn:

- **Giai đoạn đầu**, khi bạn đang khám phá các chatbot và trợ lý cá nhân — hãy tập trung vào phân loại trường hợp sử dụng và quản trị nền tảng. Đừng cố xây toàn bộ kiến trúc tham chiếu ngay trong lần lặp đầu tiên. Thay vào đó, hãy tập trung vào một hoặc hai trường hợp sử dụng thí điểm (pilot) và chỉ xây các thành phần cần thiết cho chúng. Sau đó bổ sung năng lực một cách lặp đi lặp lại khi có thêm trường hợp sử dụng mới.
- **Mức trưởng thành đang tăng**, khi bạn đang triển khai các tác tử nhóm và ứng dụng nghiệp vụ — hãy nhấn mạnh các mô hình quản trị agentic AI và các mẫu kiến trúc.
- **Mức trưởng thành nâng cao**, khi bạn đang xây các ứng dụng phục vụ khách hàng — hãy ưu tiên kiến trúc agentic AI doanh nghiệp, cung cấp các biện pháp kiểm soát nâng cao cho quyền hạn của tác tử, có tham chiếu đến các yêu cầu quản trị và kiểm toán.

## Về loạt nội dung này

Hướng dẫn này là một phần của loạt bài về agentic AI trên AWS. Để biết thêm thông tin và xem các hướng dẫn khác trong loạt bài này, hãy xem [Agentic AI](https://aws.amazon.com/prescriptive-guidance/agentic-ai/) trên website AWS Prescriptive Guidance.

## Mục lục

- **[1. Phân loại trường hợp sử dụng — hiểu về AI tạo sinh và ứng dụng tác tử](./1-use-case-typologies/)**
  - [Ứng dụng năng suất nội bộ](./1-use-case-typologies/internal-productivity.md)
  - [Ứng dụng nghiệp vụ](./1-use-case-typologies/business-applications.md)
- **[2. Quản trị AI tác tử](./2-agentic-ai-governance/)**
  - [Phạm vi quản trị](./2-agentic-ai-governance/governance-scope.md)
  - [Các mô hình quản trị](./2-agentic-ai-governance/governance-models.md)
- **[3. Kiến trúc AI tác tử trong doanh nghiệp](./3-enterprise-architecture/)**
  - [Lớp ứng dụng — giải pháp AI tạo sinh cho người dùng cuối](./3-enterprise-architecture/applications-genai.md)
  - [Lớp ứng dụng — giải pháp phi AI tạo sinh](./3-enterprise-architecture/applications-non-genai.md)
  - [Lớp tác tử (Agents layer)](./3-enterprise-architecture/agents-layer.md)
  - [Dịch vụ lõi: truy cập mô hình](./3-enterprise-architecture/model-access.md)
  - [Dịch vụ lõi: công cụ](./3-enterprise-architecture/tools.md)
  - [Dịch vụ lõi: cơ sở tri thức](./3-enterprise-architecture/knowledge-bases.md)
  - [Mối quan tâm xuyên lớp](./3-enterprise-architecture/cross-cutting-concerns.md)
- [Tài nguyên](./resources.md)
- [Người đóng góp](./contributors.md)
- [Lịch sử tài liệu](./doc-history.md)
