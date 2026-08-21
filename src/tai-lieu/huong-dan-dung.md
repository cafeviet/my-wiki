# Hướng dẫn sử dụng hệ thống

Trang này hướng dẫn bạn cách quản lý và sử dụng kho tài liệu cá nhân của mình.

## Cách thêm tài liệu mới

Hệ thống hoạt động trên nguyên tắc **Flat-file**, nghĩa là mọi cấu trúc file và thư mục trên ổ đĩa của bạn chính là cấu trúc hiển thị trên trang web.

Để thêm bài viết mới:

1. **Chọn phân vùng:**
   - Để thêm tài liệu chung: Bỏ vào thư mục `src/tai-lieu/`
   - Để thêm bài viết nghiên cứu: Bỏ vào thư mục `src/nghien-cuu/`
   - Để thêm bài dịch thuật: Bỏ vào thư mục `src/dich-thuat/`

2. **Tạo file mới:**
   Tạo file có đuôi `.md` (Ví dụ: `huong-dan-moi.md`).

3. **Viết nội dung:**
   Viết nội dung bằng Markdown tiêu chuẩn. Tiêu đề chính `#` ở đầu file sẽ được sử dụng làm tên hiển thị trên Sidebar.

## Các cú pháp Markdown nâng cao hỗ trợ sẵn

### 1. Hộp thông tin (Alerts)

> [!NOTE]
> Đây là hộp thông tin chung (Note).

> [!TIP]
> Đây là hộp gợi ý / mẹo (Tip).

> [!IMPORTANT]
> Đây là hộp thông tin quan trọng cần lưu ý (Important).

> [!WARNING]
> Đây là hộp cảnh báo (Warning).

> [!CAUTION]
> Đây là hộp cảnh báo nguy hiểm (Caution).

### 2. Code block hỗ trợ tô sáng cú pháp

```javascript
// Ví dụ mã Javascript
const hello = "Xin chào các bạn!";
console.log(hello);
```
