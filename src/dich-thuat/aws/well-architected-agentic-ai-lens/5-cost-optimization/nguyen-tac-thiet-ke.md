# Các nguyên tắc thiết kế

Bên cạnh các nguyên tắc thiết kế ở cấp lens, các thực hành tốt về tối ưu chi phí trong lens này được đại diện bởi ít nhất một trong những nguyên tắc sau:

- **Chỉ trả tiền cho lượng suy luận mà tác vụ thực sự cần:** Khớp lớp model, độ dài ngữ cảnh và độ sâu suy luận với độ phức tạp của tác vụ, thay vì cấp phát model lớn nhất và ngữ cảnh dài nhất cho trường hợp tệ nhất.
- **Áp trần tiêu thụ ở mọi tầng:** Ngân sách token, giới hạn số vòng lặp, giới hạn thời gian và trần đồng thời tồn tại dưới dạng chính sách (policy) tại tầng gateway, runtime và điều phối (orchestration), để việc thực thi không giới hạn bị từ chối ngay tại ranh giới thay vì bị phát hiện sau khi đã phải trả tiền.
- **Tái sử dụng trước khi tính lại:** Việc **caching** prompt, kết quả công cụ, kết quả truy xuất (retrieval) và trạng thái trung gian biến công việc lặp lại thành các tra cứu. Suy luận (inference) là thao tác đắt nhất trong hệ thống; hãy xây dựng kiến trúc xoay quanh sự thật đó.
- **Quy gán chi tiêu về đúng đơn vị tạo ra nó:** Gắn thẻ mỗi lần gọi với agent, tenant, phiên (session) và luồng công việc (workflow) để việc báo cáo chuyển từ mức hạ tầng sang kế toán theo từng quyết định, và các thành phần được cấp phát dư trở nên hiển thị.
- **Khép kín vòng lặp giữa dữ liệu chi phí và kiến trúc:** Dữ liệu đo lường chi phí (telemetry) được đưa ngược trở lại vào lựa chọn model, thiết kế prompt và các quyết định điều phối theo một nhịp đều đặn. Tối ưu là quá trình liên tục, không phải một lần đánh giá duy nhất.
