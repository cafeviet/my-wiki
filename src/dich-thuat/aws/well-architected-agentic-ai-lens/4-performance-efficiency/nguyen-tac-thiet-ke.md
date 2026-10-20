# Các nguyên tắc thiết kế

Ngoài các nguyên tắc thiết kế ở cấp độ lens, các thực hành tốt về hiệu quả hiệu năng trong lens này được thể hiện qua ít nhất một trong các nguyên tắc sau:

- **Đặt mục tiêu theo từng lớp tác nhân, không phải theo nền tảng:** Các tác nhân dạng streaming, hướng-tác-vụ, và batch có các KPI chính khác nhau (**thời gian tới token đầu tiên (time-to-first-token)**, thời gian hoàn thành, **throughput**). Hãy cam kết đúng những chỉ số cho từng lớp thay vì một SLA duy nhất áp cho toàn nền tảng.
- **Thiết kế và tinh chỉnh pipeline suy luận theo ngân sách latency:** **Latency** đầu-cuối là tổng của suy luận (inference), truy xuất (retrieval), các lệnh gọi Tools, và các lượt bàn giao (handoff). Hãy đo xem thời gian thực sự đi đâu, phân bổ ngân sách theo từng pha, và tối ưu đường tới hạn (critical path) đã được kiểm chứng chứ không phải đường được phỏng đoán.
- **Chuyển công việc ra khỏi đường đồng bộ:** Nhắn tin bất đồng bộ, phản hồi dạng streaming, gọi Tools song song, và điều phối hướng-sự-kiện tách rời latency mà người dùng cảm nhận khỏi tổng khối lượng công việc thực hiện.
- **Phân tầng bộ nhớ và truy xuất theo mẫu truy cập:** Ngữ cảnh nóng đặt gần tác nhân, ấm đặt trong các cache lân cận, lạnh đặt trong các kho lưu bền. Chi phí truy xuất (latency, compute, **Token**) nên khớp với độ mới và tần suất truy cập, chứ không phải theo mức tối đa.
- **Cô lập các tenant mà không tuần tự hóa chúng:** Nền tảng tác nhân multitenant cần throttling, hạn ngạch (quota), và đặt chỗ dung lượng theo từng tenant để các khối công việc nặng không thể bỏ đói các tenant lân cận.
