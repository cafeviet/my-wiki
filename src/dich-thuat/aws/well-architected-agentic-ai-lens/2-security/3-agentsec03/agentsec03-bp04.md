# AGENTSEC03-BP04 Rà soát quyền hạn và truy cập định kỳ

Các vai trò agent tích lũy quyền hạn theo thời gian. Phân tích tự động theo lịch kết hợp với các cuộc rà soát định kỳ do con người dẫn dắt bắt được trôi dạt trước khi nó biến thành sự dư đặc quyền đáng kể và tạo ra dấu vết kiểm toán có tài liệu mà việc tuân thủ cần.

**Kết quả mong muốn:**

- Bạn liên tục giám sát quyền hạn agent và rà soát chúng theo một nhịp khớp với hồ sơ rủi ro của agent, nhận diện và loại bỏ truy cập không dùng đến một cách thường xuyên.
- Các cảnh báo tự động kích hoạt ngay lập tức khi quyền hạn agent bị chỉnh sửa, cho phép phát hiện nhanh các thay đổi chính sách trái phép.
- Bạn ghi tài liệu các cuộc rà soát truy cập với các phát hiện có dấu thời gian và các hành động khắc phục phục vụ mục đích tuân thủ.

**Các phản mẫu thường gặp (anti-patterns):**

- Chỉ tiến hành các cuộc rà soát quyền hạn hằng năm hoặc để đáp lại các sự cố, để cho trôi dạt tích lũy không bị phát hiện trong nhiều tháng.
- Đặt một nhịp rà soát duy nhất cho mọi agent bất kể rủi ro, khiến các agent rủi ro cao (những agent có quyền hạn rộng, quyền truy cập công cụ biến đổi, hoặc chạm tới dữ liệu sản xuất) nhận cùng mức soi xét như các agent thông tin rủi ro thấp.
- Rà soát quyền hạn thủ công mà không có hỗ trợ công cụ, khiến việc đánh giá toàn bộ phạm vi truy cập của agent qua hàng chục hoặc hàng trăm vai trò trở nên không khả thi.
- Coi các phát hiện của IAM Access Analyzer là thông tin tham khảo thay vì các mục khắc phục thực tế, nên sự dư đặc quyền được nhận diện tồn tại vô thời hạn.
- Không cảnh báo về các thay đổi quyền hạn theo thời gian thực, chỉ phát hiện các chỉnh sửa chính sách trái phép trong chu kỳ rà soát theo lịch tiếp theo hàng tuần hoặc hàng tháng sau đó.

**Lợi ích khi áp dụng thực hành tốt này:**

- Giám sát quyền hạn liên tục phát hiện trôi dạt trước khi nó tích lũy thành sự dư đặc quyền đáng kể.
- Các phát hiện có dấu thời gian và các hành động khắc phục hỗ trợ các yêu cầu tuân thủ và các cuộc điều tra bảo mật.
- Bằng chứng dựa trên việc sử dụng từ AWS CloudTrail thúc đẩy việc giảm quyền hạn bằng dữ liệu thay vì phỏng đoán về quyền hạn nào vẫn còn cần.

**Mức độ rủi ro nếu không áp dụng thực hành tốt này:** Trung bình

## Hướng dẫn triển khai

Hai chế độ rà soát đều cần thiết. Phân tích tự động cung cấp tốc độ và độ bao phủ — khả năng quét mọi vai trò agent trên mọi tài khoản mỗi ngày. Các cuộc rà soát định kỳ do con người dẫn dắt cung cấp ngữ cảnh mà tự động hóa không thể cung cấp, chẳng hạn như liệu một quyền hạn về mặt kỹ thuật không dùng đến có còn cần cho công việc sắp tới hay không, liệu một thay đổi chính sách gần đây có được dự kiến hay không, và liệu mức đặc quyền hiện tại có khớp với vai trò hiện tại của agent trong doanh nghiệp hay không. Chỉ chạy một trong hai để lại một khoảng trống: chỉ tự động hóa tạo ra các phát hiện mà không ai hành động, và chỉ rà soát thủ công diễn ra quá thưa để bắt được trôi dạt kịp thời.

AWS IAM Access Analyzer ở cấp tổ chức liên tục phân tích các chính sách IAM của agent và sinh các phát hiện cho các quyền hạn cấp quyền truy cập tới các tài nguyên ngoài phạm vi dự định. Phân tích quyền hạn không dùng đến của nó sử dụng dữ liệu hoạt động AWS CloudTrail để nhận diện truy cập chưa được thực hiện, cho một cơ sở dựa trên dữ liệu để giảm quyền hạn thay vì phỏng đoán. Rà soát và khắc phục hàng tuần các phát hiện của Access Analyzer, được ưu tiên theo mức độ nghiêm trọng, giữ cho tồn đọng có giới hạn và biến các phát hiện thành các ticket thay đổi.

Các quy tắc AWS Config phát hiện các thay đổi đối với các chính sách IAM, vai trò và ranh giới quyền hạn của agent gần thời gian thực. Hãy cấu hình các quy tắc quản lý như iam-policy-no-statements-with-admin-access cùng với các quy tắc tùy chỉnh kiểm chứng các ràng buộc chính sách riêng của agent, và định tuyến các vi phạm quy tắc qua Amazon EventBridge tới một chủ đề Amazon SNS để đội bảo mật được thông báo ngay lập tức thay vì trong cuộc rà soát theo lịch tiếp theo.

Đối với cuộc rà soát định kỳ chính thức, hãy tương quan các phát hiện của Access Analyzer với dữ liệu sử dụng CloudTrail để nhận diện các quyền hạn chưa được thực hiện trong kỳ. Nhịp rà soát nên khớp với hồ sơ rủi ro của agent: các agent rủi ro cao (những agent có quyền hạn rộng, quyền ghi vào dữ liệu sản xuất, hoặc các đặc quyền công cụ biến đổi) đáng được rà soát thường xuyên, trong khi các agent thông tin rủi ro thấp có thể được rà soát thưa hơn. [AWS CloudTrail Lake](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html) cung cấp khả năng lưu giữ dài hạn có thể truy vấn cho phân tích này, và các hàm AWS Lambda có thể tự động hóa việc sinh các báo cáo rà soát bằng cách truy vấn dữ liệu IAM và CloudTrail và công bố kết quả tới Amazon S3. Đầu ra cung cấp cho cuộc họp rà soát và tạo ra bằng chứng có tài liệu mà việc tuân thủ cần.

AWS Security Hub CSPM là lớp tổng hợp cho các đội tàu agent lớn. Các phát hiện từ IAM Access Analyzer, AWS Config và Amazon GuardDuty chảy vào một khung nhìn duy nhất nơi mức độ nghiêm trọng và tác động kinh doanh thúc đẩy việc ưu tiên, nên đội làm việc từ một danh sách thay vì ba console.

### Các bước triển khai

- **Bật IAM Access Analyzer ở cấp tổ chức:** Bật AWS IAM Access Analyzer ở cấp tổ chức và cấu hình nó để phân tích mọi vai trò IAM agent về truy cập không dùng đến và quá phóng khoáng.
- **Phát hiện các thay đổi chính sách bằng AWS Config:** Triển khai các quy tắc AWS Config để phát hiện các thay đổi đối với các chính sách IAM của agent và kích hoạt các thông báo Amazon EventBridge để cảnh báo ngay tới đội bảo mật.
- **Lưu giữ dữ liệu hoạt động trong CloudTrail Lake:** Cấu hình AWS CloudTrail Lake để lưu giữ dài hạn dữ liệu hoạt động API của agent, hỗ trợ tương quan rà soát truy cập và báo cáo tuân thủ.
- **Tự động hóa rà soát phát hiện hàng tuần:** Hiện thực các cuộc rà soát tự động hàng tuần đối với các phát hiện của Access Analyzer, sinh các báo cáo ưu tiên các phát hiện mức độ nghiêm trọng cao để khắc phục.
- **Chạy một cuộc rà soát truy cập chính thức theo nhịp dựa trên rủi ro:** Đặt nhịp rà soát theo từng agent dựa trên hồ sơ rủi ro của nó (các agent rủi ro cao được rà soát thường xuyên, các agent thông tin rủi ro thấp được rà soát thưa hơn). Tương quan các phát hiện của Access Analyzer với dữ liệu sử dụng CloudTrail, ghi tài liệu các phát hiện và các hành động khắc phục, và ghi lại phê duyệt cho từng chu kỳ rà soát.
- **Tổng hợp các phát hiện trong Security Hub CSPM:** Kéo các phát hiện IAM từ Access Analyzer, AWS Config và Amazon GuardDuty vào AWS Security Hub CSPM để có một khung nhìn thống nhất về các vấn đề liên quan đến quyền hạn trên toàn đội tàu agent.

## Tài nguyên

**Các thực hành tốt liên quan:**

- [AGENTSEC03-BP03 Triển khai đặc quyền tối thiểu với ranh giới động](agentsec03-bp03.md)
- [AGENTSEC03-BP02 Tách biệt quyền hạn của agent và của người dùng con người](agentsec03-bp02.md)
- [AGENTSEC05-BP01 Triển khai ghi log toàn diện và lưu trữ tạo phẩm quyết định](../5-agentsec05/agentsec05-bp01.md)

**Tài liệu liên quan:**

- [Tài liệu AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [AWS Config managed rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)

**Dịch vụ liên quan:**

- [AWS IAM Access Analyzer](https://aws.amazon.com/iam/features/analyze-access/)
- [AWS Config](https://aws.amazon.com/config/)
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
- [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
