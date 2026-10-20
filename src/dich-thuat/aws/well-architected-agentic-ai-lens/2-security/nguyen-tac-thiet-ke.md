# Nguyên tắc thiết kế

Ngoài các nguyên tắc thiết kế ở cấp lens, các thực hành tốt về bảo mật trong lens này được thể hiện qua ít nhất một trong những nguyên tắc sau:

- **Coi mọi đầu vào là không đáng tin và mọi đầu ra là có khả năng gây hại:** Việc kiểm định (validation) nhiều lớp, các cơ chế phòng thủ chống tiêm nhiễm lệnh (prompt injection) và lọc đầu ra được áp dụng cho cả đầu vào của người dùng, các thao tác đọc bộ nhớ, luồng I/O của công cụ (Tools) và thông điệp giữa agent với agent. Bản thân agent không phải là một ranh giới tin cậy (trust boundary).
- **Cấp cho mỗi agent một danh tính riêng và quyền hạn tối thiểu đủ để làm việc:** Xác thực theo từng agent, ranh giới quyền hạn động và thông tin xác thực (credentials) được giới hạn phạm vi theo từng phiên (session) sẽ giới hạn những gì mà bất kỳ agent đơn lẻ hay phiên bị xâm phạm nào có thể truy cập tới.
- **Phân vùng bộ nhớ, công cụ và kênh giao tiếp theo các ranh giới tin cậy:** Các phiên, người dùng, thuê bao (tenants) và agent nhận được không gian tên (namespace) riêng, các phép kiểm tra tính toàn vẹn trên trạng thái được lưu trữ, cùng với giao tiếp được xác thực và mã hóa để sự nhiễm bẩn không thể lan ngang.
- **Xếp lớp các rào chắn (guardrails) giữa ý định và hành động:** Các bộ lọc đầu vào trước khi thực thi, các kiểm soát căn chỉnh ở thời điểm chạy (runtime) và các bộ lọc đầu ra sau khi thực thi giữ cho hành vi của agent luôn được căn chỉnh, ngay cả khi prompt hoặc ngữ cảnh mang tính đối kháng. Các hành động quan trọng vẫn được đặt sau cổng phê duyệt của con người.
- **Liên tục kiểm thử tình trạng bảo mật:** Việc quét lỗ hổng có nhận thức về AI (AI-aware), mô phỏng red team đa agent và phát hiện mối đe dọa ở thời điểm chạy được thực hiện như một phần của vòng đời, không phải là hoạt động một lần.
