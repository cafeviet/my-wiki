# AGENTOPS02-BP02 Triển khai phát hiện và khắc phục trôi lệch cấu hình

Cấu hình có thể trôi lệch, tạo ra các phiên bản lỗi thời hoặc không ổn định theo thời gian. Ví dụ, một chỉnh sửa thủ công trong một môi trường, một cờ Guardrail bị thay đổi trong lúc sự cố, hoặc một ghi đè thử nghiệm không bao giờ được hoàn nguyên có thể tạo ra các agent hành xử khác trong sản xuất so với trong kiểm thử. Phát hiện trôi lệch tự động bắt được các sự kiện này trước khi chúng biến thành sự cố.

**Kết quả mong muốn:**

- Cấu hình agent giữ nhất quán với các baseline được phê duyệt trên mọi môi trường.
- Các thay đổi trái phép hoặc ngoài ý muốn được phát hiện và khắc phục tự động.
- Mỗi thay đổi cấu hình tuân theo một luồng phê duyệt được tài liệu hóa với vết kiểm toán đầy đủ.
- Tính nhất quán liên môi trường được kiểm định liên tục để phát triển, staging, và sản xuất không trôi lệch khỏi nhau.

**Các phản mẫu thường gặp (anti-patterns):**

- Quản lý cấu hình agent thông qua các thay đổi console thủ công mà không có kiểm soát phiên bản, khiến không thể theo dõi điều gì đã thay đổi, khi nào, và bởi ai.
- Cho phép các môi trường khác nhau trôi lệch khỏi nhau mà không có kiểm tra nhất quán tự động, khiến các agent hành xử khác trong sản xuất so với trong kiểm thử.
- Chỉ phát hiện trôi lệch cấu hình sau khi nó gây ra một sự cố sản xuất thay vì thông qua giám sát chủ động.
- Xem các cấu hình hành vi (system prompt, thiết lập Guardrail) là rủi ro thấp và bỏ qua các luồng phê duyệt cho những thay đổi làm biến đổi căn bản hành vi agent.

**Lợi ích khi áp dụng thực hành tốt này:**

- Phát hiện trôi lệch tự động giúp giữ cấu hình agent trong các ranh giới được phê duyệt một cách liên tục, hỗ trợ các yêu cầu kiểm toán và giảm rủi ro thay đổi hành vi trái phép.
- Giám sát cấu hình cung cấp tầm nhìn vượt ra ngoài các chỉ số tại runtime, bộc lộ các vấn đề ở tầng cấu hình trước khi chúng biểu hiện thành các vấn đề hành vi.
- Kiểm định nhất quán liên môi trường giúp phát hiện các lỗi đã vượt qua trong môi trường kiểm thử hoặc staging bằng cách phát hiện sớm sự phân kỳ giữa các môi trường.
- Các sự kiện thay đổi được nắm bắt với đầy đủ quy kết, giúp phân tích nguyên nhân gốc nhanh hơn khi sự cố thực sự xảy ra.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Cao

## Hướng dẫn triển khai

Trước tiên, hãy xác định nguồn chân lý (source of truth) cho cấu hình của bạn. Nếu các baseline được phê duyệt nằm trong một wiki, một lịch sử shell, hoặc trong console AWS, thì phát hiện trôi lệch không có gì để so sánh. Lưu các baseline dưới dạng hạ tầng như mã (IaC) trong [AWS CloudFormation](https://aws.amazon.com/cloudformation/) hoặc [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/cdk/) mang lại cho mỗi lần triển khai một điểm tham chiếu tái lập được và biến định nghĩa IaC thành tài liệu duy nhất xác định một cách có thẩm quyền các tài nguyên nên trông như thế nào.

[Phát hiện trôi lệch AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) cho biết khi các tài nguyên đã triển khai phân kỳ khỏi định nghĩa stack của chúng. Các quy tắc [AWS Config](https://aws.amazon.com/config/) bổ sung tầng runtime, giám sát hạ tầng agent liên tục và kích hoạt khắc phục tự động khi xuất hiện sai lệch. [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) nắm bắt mọi sự kiện thay đổi cấu hình với đầy đủ quy kết, để khi trôi lệch được phát hiện, nhóm có thể xác định chính xác một thay đổi đã được thực hiện như thế nào mà không cần tái dựng lại các sự kiện.

Các cấu hình hành vi, system prompt, thiết lập Guardrail, quyền của Tools, và ranh giới quyết định cần một đường riêng vì chúng không nhất quán nằm trong các tài nguyên có thể quản lý bằng CloudFormation. Một kho cấu hình có phiên bản với kiểm soát truy cập nghiêm ngặt và thông báo thay đổi sẽ xử lý tầng này. Các thay đổi sản xuất nên yêu cầu lý do được tài liệu hóa và phê duyệt.

Mục tiêu không phải là làm chậm các nhóm mà là để một điều chỉnh Prompt làm thay đổi hành vi hạ nguồn phải đi qua cùng quy trình rà soát như một thay đổi mã. Các nhóm dùng tệp điều hướng (steering files) trong Kiro hoặc tương đương có thể hệ thống hóa các chuẩn cấu hình để trôi lệch ít có khả năng được đưa vào ngay từ nguồn.

Kiểm định liên môi trường theo lịch bắt được nhóm trôi lệch chậm mà việc phát hiện theo từng sự kiện đơn lẻ bỏ sót. Hãy chụp nhanh (snapshot) cấu hình của mỗi môi trường theo nhịp, so sánh các snapshot, và cảnh báo về bất kỳ chênh lệch nào không được giải thích bằng một thay đổi đã phê duyệt. Kiểm tra này bộc lộ trôi lệch tích tụ dần trong nhiều tháng thay vì xảy ra trong một sự kiện đơn lẻ.

### Các bước triển khai

- **Định nghĩa các baseline cấu hình dưới dạng IaC:** Lưu các định nghĩa hạ tầng agent trong [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) hoặc [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) dưới kiểm soát phiên bản, với định nghĩa IaC là nguồn chân lý duy nhất.
- **Cấu hình phát hiện trôi lệch:** Dùng [phát hiện trôi lệch AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) cho hạ tầng và các quy tắc [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) cho các cấu hình đặc thù agent (thiết lập Guardrail, tham số Model) so với các baseline được phê duyệt.
- **Bật nắm bắt sự kiện thay đổi với đầy đủ quy kết:** Bật [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) và định tuyến các sự kiện thay đổi tới các luồng cảnh báo và khắc phục tự động.
- **Đánh phiên bản các cấu hình hành vi:** Lưu Prompt, thiết lập Guardrail, và ranh giới quyết định trong một kho cấu hình có phiên bản với kiểm soát truy cập và luồng phê duyệt bắt buộc cho các thay đổi sản xuất.
- **Kiểm định tính nhất quán liên môi trường theo lịch:** So sánh các snapshot cấu hình qua phát triển, staging, và sản xuất, và cảnh báo về các chênh lệch không được giải thích.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTOPS02-BP01 Tiến hóa Prompt, lời gọi Tools và cấu hình của agent để phản ánh nhu cầu kinh doanh đang thay đổi](agentops02-bp01.md)
- [AGENTOPS02-BP03 Triển khai năng lực đánh phiên bản và quay lui hành vi agent](agentops02-bp03.md)
- [AGENTOPS03-BP01 Định nghĩa vòng đời agent với quyền sở hữu SME, kiểm thử và quản trị rõ ràng](../3-agentops03/agentops03-bp01.md)
- [AGENTREL08-BP01 Thiết lập các thực hành quản lý cấu hình nhất quán](../../3-reliability/8-agentrel08/agentrel08-bp01.md)

**Tài liệu liên quan:**

- [Vận hành hóa agentic AI trên AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/introduction.html)
- [Guidance for Agentic AI Operational Foundations on AWS](https://aws.amazon.com/solutions/guidance/agentic-ai-operational-foundations-on-aws/)
- [Kiro Steering](https://kiro.dev/docs/steering/)
- [Tiến hóa việc phân phối phần mềm cho agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/software-delivery.html)

**Video liên quan:**

- [AWS re:Invent 2024 - Architecting scalable and secure agentic AI with AgentCore (AIM431)](https://www.youtube.com/watch?v=wqmeZOT6mmc)

**Ví dụ liên quan:**

- [GitHub: Sample Agentic Platform on AWS](https://github.com/aws-samples/sample-agentic-platform)

**Dịch vụ liên quan:**

- [AWS Config](https://aws.amazon.com/config/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
- [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
