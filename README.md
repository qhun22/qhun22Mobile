# ShopMobile - Điện Thoại Chính Hãng

<div align="center">
    <img src="static/images/QHUN22-min.gif" alt="ShopMobile Logo" width="200">
    <p><strong>ShopMobile</strong> - Hệ thống bán điện thoại di động chính hãng</p>
</div>

---

## Mục lục

1. [Giới thiệu dự án](#1-giới-thiệu-dự-án)
2. [Công nghệ sử dụng](#2-công-nghệ-sử-dụng)
3. [Cấu trúc thư mục](#3-cấu-trúc-thư-mục)
4. [Hướng dẫn cài đặt](#4-hướng-dẫn-cài-đặt)
5. [Hướng dẫn chạy hệ thống](#5-hướng-dẫn-chạy-hệ-thống)
6. [Tài khoản mẫu](#6-tài-khoản-mẫu)
7. [Tiến độ thực hiện](#7-tiến-độ-thực-hiện)
8. [Các tính năng chính](#8-các-tính-năng-chính)

---

## 1. Giới thiệu dự án

### 1.1 Tổng quan

**ShopMobile** là một trang web thương mại điện tử chuyên kinh doanh điện thoại di động chính hãng, được phát triển bằng framework Django (Python). Dự án cung cấp đầy đủ các tính năng cần thiết cho một hệ thống bán hàng trực tuyến.

### 1.2 Các thực thể dữ liệu

| Thực thể | Mô tả | Quan hệ |
|----------|-------|---------|
| User | Người dùng hệ thống | 1-n với Address, Order |
| Category | Danh mục sản phẩm | 1-n với Product |
| Product | Sản phẩm điện thoại | n-1 với Category |
| Address | Địa chỉ giao hàng | n-1 với User |
| Order | Đơn hàng | n-1 với User |

### 1.3 Vai trò người dùng

- **Khách (Guest)**: Xem sản phẩm, tìm kiếm, đăng ký, đăng nhập
- **Người dùng**: Đặt hàng, quản lý địa chỉ, xem lịch sử mua hàng
- **Quản trị (Admin)**: Quản lý sản phẩm, danh mục, đơn hàng (via Django Admin)

---

## 2. Công nghệ sử dụng

### 2.1 Backend

| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| Python | 3.12+ | Ngôn ngữ lập trình chính |
| Django | 4.2.x | Framework web Python |
| SQLite | 3.x | Cơ sở dữ liệu |
| Pillow | 10.0+ | Thư viện xử lý hình ảnh |

### 2.2 Frontend

| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| HTML5 | - | Ngôn ngữ đánh dấu |
| CSS3 | - | Ngôn ngữ định kiểu |
| JavaScript | ES6+ | Ngôn lập trình script |
| Tailwind CSS | 3.x | Framework CSS utility-first |
| Font Awesome | 6.4 | Thư viện biểu tượng |

---

## 3. Cấu trúc thư mục

```
D:\Py\ShopMobile\
├── db.sqlite3                      # CSDL SQLite
├── manage.py                       # Django management script
├── README.md                       # Tài liệu dự án
├── requirements.txt                # Danh sách thư viện Python
│
├── shopmobile/                     # Project Django
│   ├── __init__.py
│   ├── settings.py                 # Cấu hình project
│   ├── urls.py                     # URL routing chính
│   ├── asgi.py
│   └── wsgi.py
│
├── static/                         # Static files
│   ├── css/
│   │   ├── base.css                # Styles cơ bản
│   │   ├── home.css                # Styles trang chủ
│   │   └── toast.css               # Styles toast notification
│   ├── js/
│   │   ├── auth.js                 # JavaScript xác thực
│   │   ├── main.js                 # JavaScript chính
│   │   └── toast.js                # Toast notification
│   ├── images/                     # Hình ảnh
│   └── videos/                     # Video
│
├── store/                          # App chính
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Database models
│   ├── views.py                    # Views xử lý request
│   ├── forms.py                    # Django forms
│   ├── urls.py                     # URL routing app
│   ├── migrations/
│   │   └── ...
│   └── management/commands/
│       └── seed_data.py            # Seeding dữ liệu mẫu
│
└── templates/                      # Templates
    ├── base.html                   # Base template (layout)
    ├── header.html                 # Header component
    ├── footer.html                 # Footer component
    ├── home.html                   # Trang chủ
    ├── login.html                  # Trang đăng nhập
    ├── register.html               # Trang đăng ký
    ├── forgot_password.html        # Trang quên mật khẩu
    ├── profile.html                # Trang cá nhân
    └── product_detail.html         # Trang chi tiết sản phẩm
```

---

## 4. Hướng dẫn cài đặt

### 4.1 Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|---------|
| Hệ điều hành | Windows 10/11 |
| Python | 3.12 trở lên |
| RAM | 4GB trở lên |
| Ổ cứng | 1GB trống |

### 4.2 Cài đặt

```powershell
# Di chuyển vào thư mục dự án
cd D:\Py\ShopMobile

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy migrations
python manage.py migrate

# Tạo dữ liệu mẫu
python manage.py seed_data

# Tạo superuser (tùy chọn)
python manage.py createsuperuser
```

---

## 5. Hướng dẫn chạy hệ thống

### 5.1 Khởi động Server

```powershell
cd D:\Py\ShopMobile
venv\Scripts\activate
python manage.py runserver
```

### 5.2 Truy cập Website

| Trang | URL | Mô tả |
|-------|-----|-------|
| Trang chủ | http://127.0.0.1:8000/ | Hiển thị sản phẩm |
| Đăng nhập | http://127.0.0.1:8000/login/ | Đăng nhập |
| Đăng ký | http://127.0.0.1:8000/register/ | Đăng ký tài khoản |
| Quên mật khẩu | http://127.0.0.1:8000/forgot-password/ | Khôi phục mật khẩu |
| Hồ sơ | http://127.0.0.1:8000/profile/ | Quản lý tài khoản |
| Chi tiết SP | http://127.0.0.1:8000/product/slug/ | Xem sản phẩm |
| Admin | http://127.0.0.1:8000/admin/ | Quản trị (cần superuser) |

---

## 6. Tài khoản mẫu

### 6.1 Tài khoản người dùng thường

| Username | Password | Quyền |
|----------|----------|-------|
| user1 | user123 | Người dùng |
| user2 | user123 | Người dùng |

**Đăng ký tài khoản mới:**
1. Truy cập http://127.0.0.1:8000/register/
2. Điền thông tin và nhấn "Đăng ký"
3. Tự động chuyển về trang chủ

### 6.2 Tài khoản Admin

```powershell
python manage.py createsuperuser
```

- URL: http://127.0.0.1:8000/admin/
- Username/Password: do bạn tự đặt

---

## 7. Tiến độ thực hiện

### 7.1 Thiết kế giao diện

| Nhiệm vụ | Trạng thái |
|----------|------------|
| Banner slider | ✅ Hoàn thành |
| Section thương hiệu | ✅ Hoàn thành |
| Section khuyến mãi | ✅ Hoàn thành |
| Danh sách sản phẩm | ✅ Hoàn thành |
| Tìm kiếm và lọc | ✅ Hoàn thành |
| Phân trang | ✅ Hoàn thành |
| Responsive design | ✅ Hoàn thành |

### 7.2 Backend

| Nhiệm vụ | Trạng thái |
|----------|------------|
| Django project | ✅ Hoàn thành |
| Database models | ✅ Category, Product, Address, Order |
| Authentication | ✅ Login, Register, Logout, Forgot Password |
| CRUD operations | ✅ Product, Address |
| Search/Filter/Sort | ✅ Hoàn thành |
| Order management | ✅ Với trạng thái |

### 7.3 Thống kê

| Thống kê | Số lượng |
|----------|----------|
| Django models | 4 (User, Category, Product, Address, Order) |
| Views | 12+ |
| URLs | 15+ |
| Templates | 10 |
| Categories | 10 |
| Products | 32+ |

---

## 8. Các tính năng chính

### 8.1 Xác thực & Phân quyền

- ✅ Đăng ký với validation
- ✅ Đăng nhập/Đăng xuất
- ✅ Forgot Password (demo)
- ✅ @login_required protection
- ✅ Toast notification

### 8.2 Quản lý sản phẩm (CRUD)

- ✅ Danh sách sản phẩm
- ✅ Chi tiết sản phẩm
- ✅ Tìm kiếm theo tên/hãng
- ✅ Lọc theo hãng, khoảng giá
- ✅ Sắp xếp theo giá
- ✅ Phân trang

### 8.3 Quản lý tài khoản

- ✅ Cập nhật thông tin cá nhân
- ✅ Đổi mật khẩu
- ✅ Quản lý địa chỉ (Thêm/Sửa/Xóa)
- ✅ Đặt địa chỉ mặc định
- ✅ Xem lịch sử mua hàng
- ✅ Gửi góp ý

### 8.4 Nghiệp vụ đặc thù

- ✅ Order với trạng thái: Pending → Approved → Rejected → Shipping → Delivered
- ✅ Quản lý địa chỉ giao hàng
- ✅ Tính toán giảm giá tự động

### 8.5 Thống kê & Báo cáo

- ✅ Tổng số sản phẩm
- ✅ Tổng số danh mục
- ✅ Tổng số đơn hàng (theo trạng thái)
- ✅ Doanh thu

---

## Liên hệ & Hỗ trợ

- Email: support@shopmobile.com
- GitHub: Repository của dự án

---

<div align="center">
    <p>© 2026 ShopMobile - Điện Thoại Chính Hãng</p>
    <p>Phát triển với ❤️ bằng Django & Tailwind CSS</p>
</div>
