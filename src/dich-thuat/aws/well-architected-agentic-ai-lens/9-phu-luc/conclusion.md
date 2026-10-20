# Kết luận

Agentic AI Lens cung cấp một khung toàn diện để xây dựng các hệ thống agentic AI xuất sắc về vận hành, bảo mật, tin cậy, hiệu năng cao, hiệu quả chi phí và bền vững. Khi agentic AI chuyển từ công nghệ thử nghiệm sang workload sản xuất, các quyết định kiến trúc được đưa ra trong quá trình thiết kế hệ thống sẽ để lại hệ quả lâu dài cho hồ sơ độ tin cậy, bảo mật và chi phí của các hệ thống đã triển khai.

## Các chủ đề chính

Một số chủ đề nổi lên nhất quán trên các trụ cột của Lens này:

- **Tính mô-đun tạo điều kiện cho độ tin cậy và hiệu quả:** Các hệ thống agentic được xây dựng từ các Agent chuyên biệt, đơn mục đích với các giao diện rõ ràng thì dễ kiểm thử, gỡ lỗi, mở rộng và tối ưu hơn so với các kiến trúc Agent nguyên khối. Mẫu mô hình tác nhân (actor model), trong đó mỗi Agent đóng gói một năng lực đơn lẻ và giao tiếp độc quyền qua truyền thông điệp, cung cấp một nền tảng đã được kiểm chứng để xây dựng các môi trường agentic tin cậy và dễ bảo trì.
- **Khả năng quan sát là nền tảng, không phải tùy chọn:** Bản chất ngẫu nhiên của các Agent do LLM điều khiển nghĩa là hành vi bất ngờ là điều không thể tránh khỏi. Các hệ thống thiếu khả năng quan sát toàn diện, truy vết phân tán, ghi log có cấu trúc, đường cơ sở hành vi và phát hiện bất thường thì không thể phát hiện hoặc chẩn đoán lỗi trước khi chúng lan tràn. Khả năng quan sát phải được thiết kế vào các hệ thống agentic ngay từ đầu, chứ không phải bổ sung như một suy tính về sau.
- **Suy giảm nhẹ nhàng bảo toàn giá trị trong lúc gặp lỗi:** Các hệ thống agentic thất bại hoàn toàn khi bất kỳ thành phần nào suy giảm sẽ mang lại ít giá trị hơn các hệ thống duy trì chức năng một phần với sự truyền đạt minh bạch về năng lực bị giảm. Mỗi phụ thuộc quan trọng trong một hệ thống agentic phải có một hành vi dự phòng được xác định, tự động kích hoạt khi đường chính không khả dụng.
- **Giám sát của con người vẫn là điều thiết yếu:** Ngay cả các hệ thống agentic có năng lực cao cũng hưởng lợi từ sự giám sát của con người tại các điểm quyết định phù hợp. Các mô hình giám sát phân tầng, nơi các hành động rủi ro thấp tiến hành tự chủ, các hành động rủi ro trung bình kích hoạt thông báo, và các hành động rủi ro cao yêu cầu phê duyệt rõ ràng, cân bằng giữa hiệu quả vận hành và quản trị phù hợp. Mục tiêu không phải là loại bỏ phán đoán của con người mà là áp dụng nó ở nơi quan trọng nhất.
- **Chi phí và tính bền vững đòi hỏi thiết kế có chủ đích:** Mô hình chi phí dựa trên Token của suy luận LLM, kết hợp với các vòng lặp suy luận lặp lại của các hệ thống agentic, tạo ra động lực chi phí khác biệt về căn bản so với các workload đám mây truyền thống. Thiết kế nhận thức về chi phí, điều chỉnh đúng kích thước mô hình theo độ phức tạp tác vụ, triển khai quản lý ngữ cảnh hiệu quả và thiết lập khả năng hiển thị chi phí đầy đủ, phải là một mối quan tâm kiến trúc hàng đầu chứ không phải là tối ưu hóa sau triển khai.

## Lĩnh vực đang tiến hóa

Agentic AI là một lĩnh vực đang tiến hóa nhanh chóng. Các mô hình, framework, giao thức và dịch vụ có sẵn cho những người xây dựng đang tiến bộ nhanh, và các mẫu kiến trúc đại diện cho thực hành tốt nhất hôm nay sẽ tiếp tục tiến hóa. Lens này sẽ được cập nhật khi lĩnh vực trưởng thành và khi các mẫu mới nổi lên từ các triển khai sản xuất.

Các nguyên tắc nền tảng của Lens này — tính mô-đun, khả năng quan sát, suy giảm nhẹ nhàng, giám sát của con người và nhận thức về chi phí — là bền vững bất kể các công nghệ cụ thể tiến hóa ra sao. Các nhóm nội hóa được những nguyên tắc này sẽ có vị thế tốt để điều chỉnh kiến trúc của mình khi lĩnh vực agentic AI tiếp tục phát triển.

## Các bước tiếp theo

Các nhóm bắt đầu hành trình agentic AI có thể:

- Rà soát các nguyên tắc thiết kế để hiểu các giá trị nền tảng định hướng các quyết định kiến trúc trên tất cả các trụ cột.
- Tham khảo các định nghĩa để thiết lập một vốn từ vựng chung khi thảo luận về kiến trúc agentic AI.
- Đi qua các vùng trọng tâm và thực hành tốt nhất của từng trụ cột, ưu tiên các thực hành rủi ro cao để triển khai ngay.
- Sử dụng hướng dẫn triển khai và ví dụ mã trong mỗi thực hành tốt nhất làm điểm khởi đầu cho bối cảnh cụ thể của bạn, điều chỉnh chúng theo các lựa chọn công nghệ và yêu cầu vận hành của nhóm.
- Thiết lập các đợt rà soát Well-Architected định kỳ sử dụng Lens này để đánh giá các hệ thống agentic AI của bạn khi chúng tiến hóa.

Xây dựng các hệ thống agentic AI tin cậy, bảo mật và hiệu quả chi phí là công việc đầy thử thách. Các thực hành tốt nhất trong Lens này đại diện cho kinh nghiệm tập thể của những nhóm đã vượt qua các thách thức này trong môi trường sản xuất. Chúng tôi hy vọng hướng dẫn này sẽ tăng tốc hành trình của bạn và giúp bạn xây dựng các hệ thống agentic AI mang lại giá trị lâu dài.
