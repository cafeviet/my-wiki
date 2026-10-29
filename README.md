# my-wiki

Hệ thống wiki cá nhân xây trên [VitePress](https://vitepress.dev/) để lưu trữ và đọc các bài viết **dịch thuật** (Markdown) kèm sơ đồ kiến trúc. Sidebar tự sinh từ cây thư mục, có tìm kiếm toàn văn cục bộ và giao diện sáng/tối.

> Nhánh `public` này chỉ chứa phần nội dung dịch thuật + mã nguồn hiển thị của wiki. Phần nghiên cứu nội bộ không được công bố.

## Yêu cầu

- Node.js >= 18
- npm

## Cài đặt & chạy

```bash
# 1. Cài dependency
npm install

# 2. Chạy dev server (http://localhost:6677)
npm run dev

# 3. Build tĩnh ra src/.vitepress/dist
npm run build

# 4. Xem thử bản build
npm run preview
```

## Cấu trúc thư mục

```
src/
├── index.md              # Trang chủ (hero)
├── .vitepress/
│   ├── config.mts        # Cấu hình VitePress + sidebar tự sinh + theme
│   └── theme/            # Theme tùy biến (component chat, v.v.)
├── dich-thuat/           # Nội dung bài dịch (.md), gom theo nguồn
├── tai-lieu/             # Hướng dẫn sử dụng hệ thống
└── public/               # Tài nguyên tĩnh: sơ đồ HTML, favicon, ảnh
```

## Thêm bài viết

Thêm file `.md` mới vào `src/dich-thuat/<nguồn>/<bài>/`. Sidebar và điều hướng cập nhật tự động — không cần khai báo thủ công.

File HTML sơ đồ đặt trong `src/public/.../assets/` và nhúng bằng `<iframe>` với đường dẫn tuyệt đối.

## Giấy phép

ISC
