# Các nguyên tắc thiết kế

Ngoài các nguyên tắc thiết kế ở cấp độ lăng kính (lens), những thực hành tốt về độ tin cậy trong lăng kính này được thể hiện qua ít nhất một trong các nguyên tắc sau:

- **Tách rời các tác nhân bằng nhắn tin bền vững (durable messaging):** Tính bền vững, cơ chế thử lại (retry) và xử lý hàng đợi thư chết (dead-letter) hấp thụ các lỗi thoáng qua ngay bên trong lớp nhắn tin, thay vì để chúng lan truyền theo chuỗi lời gọi đồng bộ.
- **Giới hạn bán kính ảnh hưởng qua các trách nhiệm nguyên tử (atomic):** Các tác nhân đơn tác vụ với quyền hạn tối thiểu và chỉ dẫn rõ ràng giới hạn mức độ lan truyền của bất kỳ lỗi hay hành vi sai lệch riêng lẻ nào.
- **Phục hồi từ trạng thái tốt gần nhất, không phải từ đầu:** Các quy trình có điểm kiểm tra (checkpoint), các bước bất biến khi lặp lại (**idempotency**) và **suy giảm nhẹ nhàng (graceful degradation)** cho phép công việc tiếp tục sau lỗi thay vì khởi động lại từ số không.
- **Làm cho sự phối hợp đa tác nhân bền bỉ ngay từ thiết kế:** Các **mẫu trọng tài (arbiter pattern)**, phân loại năng lực và các đường dự phòng giữ cho luồng công việc cộng tác tiếp tục chạy khi từng tác nhân trở nên không khả dụng hoặc không đáng tin.
- **Đặt nền suy luận trên bằng chứng có thể kiểm chứng:** Việc truy xuất từ nguồn có thẩm quyền, trích dẫn tường minh và phát hiện ảo giác (hallucination) giữ cho đầu ra của tác nhân luôn truy vết được về dữ liệu thực, thay vì nội dung bịa đặt.
- **Diễn tập các đường lỗi thường xuyên:** Tiêm lỗi (inject faults), chạy các bài kiểm thử với phụ thuộc bị suy giảm, và diễn tập các quy trình phục hồi. Lần đầu tiên một dạng lỗi xảy ra không nên là ở môi trường vận hành.

**Javascript đang bị vô hiệu hóa hoặc không khả dụng trong trình duyệt của bạn.**

Để sử dụng Tài liệu Amazon Web Services, cần bật Javascript. Vui lòng tham khảo trang Trợ giúp của trình duyệt để biết hướng dẫn.
