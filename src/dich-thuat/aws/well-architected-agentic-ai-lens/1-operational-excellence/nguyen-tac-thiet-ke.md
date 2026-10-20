# Các nguyên tắc thiết kế

Bên cạnh các nguyên tắc thiết kế ở cấp độ lens, các thực hành tốt về xuất sắc trong vận hành trong lens này được thể hiện qua ít nhất một trong những nguyên tắc sau:

- **Xác định mục đích, mức độ tự chủ và tiêu chí thành công trước khi triển khai:** Mô tả vai trò, ranh giới phạm vi, và các kết quả đo lường được là điều kiện tiên quyết để đưa vào vận hành. Chúng dẫn dắt các Guardrails, ngưỡng giám sát, và tác nhân kích hoạt leo thang (escalation triggers) ở các bước phía sau.
- **Đưa agent qua một vòng đời với các cổng (gate) rõ ràng:** Kiểm định do chuyên gia lĩnh vực (SME) dẫn dắt, CI/CD được thiết kế cho các hệ thống phi tất định (non-deterministic), và triển khai theo giai đoạn (staged rollouts) ngăn các thay đổi về Prompt, Tools hay Model làm suy giảm âm thầm chất lượng sản xuất (production).
- **Phát hiện trôi lệch và khắc phục tự động ở những chỗ an toàn:** Trôi lệch cấu hình (configuration drift), bất thường hành vi, và lỗi Tools được phát hiện, khoanh vùng và phục hồi mà không cần con người can thiệp đối với các trường hợp thường lệ. Con người được dành cho các ngoại lệ.
- **Vận hành theo các KPI ánh xạ tới kết quả kinh doanh:** Tỷ lệ giải quyết, tỷ lệ leo thang, mức độ hài lòng của khách hàng, và tỷ lệ hoàn thành tác vụ đứng ngang hàng với các chỉ số hạ tầng, với trọng số như nhau trên bảng điều khiển (dashboard) và trong các buổi rà soát.
- **Quản lý agent như một danh mục (portfolio):** Các sổ đăng ký (registries), catalog, hồ sơ quyền sở hữu, và quy trình ngừng vận hành (decommissioning) xem agent như một quần thể cần được quản trị, chứ không phải các dự án riêng lẻ.
- **Hệ thống hóa và tái sử dụng tri thức vận hành:** Runbook, các tài liệu quyết định (decision artifacts), hồ sơ thay đổi, và bài học từ sự cố trở thành đầu vào có cấu trúc cho việc cải thiện agent trong tương lai và đào tạo người vận hành, chứ không phải tri thức truyền miệng.
