# Các mô hình quản trị

Các tổ chức phải lựa chọn các cách tiếp cận **quản trị (governance)** phù hợp với văn hóa, mức độ chấp nhận rủi ro, độ trưởng thành vận hành và các mục tiêu chiến lược của mình. Việc lựa chọn mô hình tập trung (centralized), liên bang (federated) hay lai (hybrid) tác động đáng kể đến tốc độ đổi mới, hiệu quả quản lý rủi ro và hiệu suất sử dụng nguồn lực.

Bằng cách triển khai các yếu tố quản trị một cách thấu đáo, bạn có thể khai thác tiềm năng biến đổi của **AI tác tử (agentic AI)** trong khi vẫn duy trì sự kiểm soát cần thiết. Quan trọng là, các khung quản trị phải luôn mang tính thích ứng, tiến hóa khi công nghệ trưởng thành và năng lực của tổ chức tăng lên. Mục tiêu không phải là một hệ thống quản trị hoàn hảo ngay hôm nay mà là thiết lập các cấu trúc cho phép đổi mới an toàn trong khi vẫn đủ linh hoạt để tích hợp những bài học của ngày mai.

## So sánh cách tiếp cận tập trung, liên bang và lai

Việc lựa chọn mô hình quản trị vừa chịu ảnh hưởng bởi, vừa ảnh hưởng đến các quyết định kiến trúc.

Khác với hạ tầng đám mây truyền thống, nơi các tổ chức hiếm khi xây dựng các lớp trừu tượng để chuyển đổi giữa các nhà cung cấp do sự phức tạp và tích hợp sâu của các dịch vụ đặc thù theo nền tảng, AI tạo sinh (generative AI) đưa vào một động lực khác. Vì suy luận (inference) của **mô hình ngôn ngữ lớn (large language model – LLM)** là không trạng thái (stateless), nó có thể được trừu tượng hóa hiệu quả thông qua các **lớp cổng (gateway layer)**. Điều này khiến các kiến trúc tập trung, và mở rộng ra là quản trị tập trung, trông khả thi hơn trên nhiều nhà cung cấp so với trường hợp của các dịch vụ đám mây tổng quát.

Tuy nhiên, lợi thế trừu tượng hóa này giảm dần với sự trỗi dậy của AI tác tử và các dịch vụ được quản lý vốn đưa vào các năng lực có trạng thái, đặc thù theo nền tảng và khó trừu tượng hóa. Do đó, các tổ chức phải cân nhắc mô hình quản trị của mình sẽ tiến hóa như thế nào khi năng lực AI trưởng thành vượt ra ngoài suy luận LLM đơn giản. Chúng tôi khám phá các cân nhắc kiến trúc này chi tiết hơn trong phần Kiến trúc Doanh nghiệp (Enterprise Architecture).

Sự tương tác giữa các khả năng trừu tượng hóa và các năng lực đám mây gốc (cloud-native) định hình các lựa chọn quản trị mà các tổ chức phải đối mặt:

**Quản trị tập trung (Centralized Governance)** thiết lập một thẩm quyền duy nhất trên toàn doanh nghiệp cho các chính sách, phê duyệt và quản lý hệ sinh thái. Điều này mang lại sự kiểm soát mạnh mẽ, thực thi chính sách nhất quán và quản lý tuân thủ được đơn giản hóa. Cách tiếp cận tập trung được kết hợp với các nền tảng như LLM gateway để tập trung hóa quyền truy cập đến các LLM. Nó phù hợp với các ngành được quản lý chặt chẽ hoặc các tổ chức đang ở giai đoạn đầu của hành trình AI. Tuy nhiên, các cách tiếp cận tập trung có thể tạo ra điểm nghẽn và có thể gặp khó khăn trong việc đáp ứng các tình huống sử dụng đa dạng khi mức độ áp dụng mở rộng.

**Quản trị liên bang (Federated Governance)** phân phối trách nhiệm cho các đơn vị kinh doanh trong khi vẫn duy trì sự đồng bộ thông qua các chuẩn chung. Điều này cho phép đổi mới nhanh hơn, bám sát nhu cầu kinh doanh hơn và có khả năng mở rộng. Nó phù hợp với các doanh nghiệp lớn có các đơn vị kinh doanh đa dạng và quản trị CNTT trưởng thành. Các thách thức bao gồm rủi ro diễn giải chính sách thiếu nhất quán và khó khăn trong việc duy trì khả năng quan sát trên toàn doanh nghiệp.

**Quản trị lai (Hybrid Governance)** kết hợp sự giám sát tập trung với việc thực thi liên bang. Một khung chính sách trung tâm định hướng việc triển khai phân tán, với các chuẩn trên toàn doanh nghiệp cho các tác tử rủi ro cao và quyền tự chủ cục bộ cho các ứng dụng rủi ro thấp. Điều này cân bằng giữa kiểm soát và sự nhanh nhẹn, và phù hợp với hầu hết các tổ chức doanh nghiệp. Thành công đòi hỏi sự phân định rõ ràng về trách nhiệm và các kênh truyền thông mạnh mẽ.

Các mô hình quản trị phải phù hợp với văn hóa tổ chức mới có thể hiệu quả. Các tổ chức đề cao tính tự chủ thường gặp khó khăn với quản trị tập trung cao độ, trong khi các nền văn hóa ngại rủi ro hoặc các môi trường được quản lý chặt chẽ tự nhiên nghiêng về kiểm soát tập trung. Ngoài ra, văn hóa mua sắm của tổ chức đóng vai trò then chốt trong việc lựa chọn mô hình quản trị. Trong mọi trường hợp, bản chất tiến hóa nhanh chóng của AI tác tử đòi hỏi một tổ chức có khả năng thích ứng.

- **Cách tiếp cận đơn đám mây (single-cloud approach)** mang lại sự tích hợp sâu hơn với hệ sinh thái của nhà cung cấp đám mây, quản trị được đơn giản hóa thông qua công cụ hợp nhất, các lợi ích chi phí tiềm năng thông qua các cam kết theo khối lượng, và giảm sự phức tạp trong vận hành.
- **Cách tiếp cận đa đám mây với quản trị liên bang (multi-cloud approach with federated governance)** cho phép bạn duy trì sự tích hợp sâu với hệ sinh thái của nhà cung cấp đám mây nhưng có thể làm giảm các lợi thế như công cụ hợp nhất hoặc các lợi ích chi phí dựa trên khối lượng.

Một số tổ chức có thể lựa chọn **chiến lược đa đám mây với cách tiếp cận tập trung (multi-cloud strategy with a centralized approach)**, điều này kéo theo các cân nhắc sau: sự phức tạp quản trị gia tăng, công việc tích hợp bổ sung, chi phí có khả năng cao hơn, và đòi hỏi chuyên môn rộng hơn. Ngoài ra, lớp trừu tượng làm giảm khả năng tận dụng nhịp độ đổi mới của từng nhà cung cấp đám mây.

## Cân bằng giữa đổi mới và kiểm soát

Thách thức trung tâm của việc thiết lập một mô hình quản trị là cân bằng đổi mới với kiểm soát sao cho phù hợp với nhu cầu của tổ chức về mặt quy định.

Với nhịp độ đổi mới chưa từng có của AI tạo sinh, điều then chốt là xây dựng một đội ngũ nhanh nhẹn, có khả năng thử nghiệm nhanh với các LLM, framework, giao thức mới và cho phép họ chuyển đổi giữa các công nghệ. Các không gian đổi mới như môi trường sandbox, phòng thí nghiệm đổi mới (innovation lab), hoặc các chương trình thử nghiệm chứng minh khái niệm (proof-of-concept) cho phép khám phá trong khi vẫn bảo vệ các hệ thống sản xuất. Việc định vị quản trị như là nền tảng cho đổi mới an toàn thay vì một rào cản quan liêu sẽ cải thiện động lực này. Các vòng phản hồi bảo đảm rằng các chính sách quản trị tiến hóa dựa trên kinh nghiệm vận hành, hoạt động trên các mốc thời gian được rút gọn ở các giai đoạn đầu.

## Hỗ trợ nhà phát triển công dân

Khả năng tiếp cận ngày càng tăng đối với phát triển AI tạo ra cả cơ hội lẫn rủi ro. Quản trị hiệu quả tạo điều kiện cho các **nhà phát triển công dân (citizen developer)** trong khi vẫn duy trì các biện pháp kiểm soát phù hợp. Nhà phát triển công dân là một người dùng nghiệp vụ tạo ra các ứng dụng AI mà không cần các kỹ năng kỹ thuật chuyên biệt.

Hãy cung cấp đào tạo nền tảng về các kiến thức cơ bản của AI, các nguyên tắc AI có trách nhiệm, các cân nhắc về bảo mật và các yêu cầu quản trị. Các chương trình đào tạo nên nhấn mạnh các nguyên tắc hơn là các quy tắc cứng nhắc, dạy các nhà phát triển tư duy phản biện về rủi ro và các đánh đổi. Các chương trình chứng nhận theo vai trò (role-based certification) khớp mức độ tự chủ với năng lực đã được chứng minh.

Bạn cũng nên cung cấp các thư viện gồm các mẫu tác tử, các tích hợp công cụ và các mẫu prompt đã được kiểm thử và tuân thủ, dùng làm các khối xây dựng. Các nền tảng phát triển có hướng dẫn nhúng sẵn gợi ý các thực hành tốt nhất và tự động thực thi các chính sách. Các nhà phát triển công dân khởi đầu với các năng lực hạn chế, và quyền hạn của họ được mở rộng khi họ chứng minh được năng lực.
