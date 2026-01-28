"""
Store application models for ShopMobile.
"""

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Category model for organizing products.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Tên danh mục'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name='Hình ảnh'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Hoạt động'
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name='Thứ tự sắp xếp'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Cập nhật lần cuối'
    )

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Product model for the store.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Tên sản phẩm'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )
    description = models.TextField(
        verbose_name='Mô tả chi tiết'
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Giá bán'
    )
    original_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name='Giá gốc'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Hình ảnh'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Danh mục'
    )
    brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Hãng'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Số lượng tồn kho'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Hoạt động'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Nổi bật'
    )
    discount_percent = models.PositiveIntegerField(
        default=0,
        verbose_name='Phần trăm giảm giá'
    )
    # Variants & Options
    storage_options = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Tùy chọn bộ nhớ'
    )
    color_options = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Tùy chọn màu sắc'
    )
    warranty_options = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Tùy chọn bảo hành'
    )
    # Technical Specifications (dynamic key-value pairs)
    specifications = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Thông số kỹ thuật'
    )
    # Sales Policies
    free_shipping = models.BooleanField(
        default=False,
        verbose_name='Miễn phí vận chuyển'
    )
    allow_open_box = models.BooleanField(
        default=False,
        verbose_name='Cho phép kiểm tra khi nhận hàng'
    )
    return_policy_30days = models.BooleanField(
        default=False,
        verbose_name='Chính sách đổi trả 30 ngày'
    )
    # Status
    is_out_of_stock = models.BooleanField(
        default=False,
        verbose_name='Hết hàng'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Cập nhật lần cuối'
    )

    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at', '-is_featured']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug and calculate discount."""
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-').replace('+', '-')
        
        # Calculate discount if original price is set
        if self.original_price and self.original_price > self.price:
            self.discount_percent = int(
                (1 - self.price / self.original_price) * 100
            )
        
        # Auto-set is_out_of_stock based on stock
        self.is_out_of_stock = (self.stock == 0)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return product detail URL."""
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def is_on_sale(self):
        """Check if product is on sale."""
        return self.original_price and self.original_price > self.price


class Address(models.Model):
    """
    Model for user saved addresses.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên')
    phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    province = models.CharField(max_length=100, verbose_name='Tỉnh/Thành')
    district = models.CharField(max_length=100, verbose_name='Quận/Huyện')
    ward = models.CharField(max_length=100, verbose_name='Phường/Xã')
    address_detail = models.CharField(max_length=255, verbose_name='Địa chỉ chi tiết')
    is_default = models.BooleanField(default=False, verbose_name='Là địa chỉ mặc định')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Địa chỉ'
        verbose_name_plural = 'Địa chỉ'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.address_detail}'

    def save(self, *args, **kwargs):
        # If this address is being set as default, unset other defaults
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        # If no default exists, set this as default
        elif not Address.objects.filter(user=self.user, is_default=True).exists():
            self.is_default = True
        super().save(*args, **kwargs)

    def get_full_address(self):
        """Return full address string."""
        return f'{self.address_detail}, {self.ward}, {self.district}, {self.province}'


class Order(models.Model):
    """
    Order model for customer purchases.
    """
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('approved', 'Đã xác nhận'),
        ('rejected', 'Đã hủy'),
        ('shipping', 'Đang giao'),
        ('delivered', 'Đã giao'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    note = models.TextField(blank=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return f'Đơn hàng #{self.id} - {self.user.username}'

    def get_status_display(self):
        """Return Vietnamese status text."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def get_status_color(self):
        """Return color class based on status."""
        colors = {
            'pending': 'bg-yellow-100 text-yellow-700',
            'approved': 'bg-blue-100 text-blue-700',
            'rejected': 'bg-red-100 text-red-700',
            'shipping': 'bg-purple-100 text-purple-700',
            'delivered': 'bg-green-100 text-green-700',
        }
        return colors.get(self.status, 'bg-gray-100 text-gray-700')

    def calculate_total(self):
        """Calculate total amount from order items."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        return total


class OrderItem(models.Model):
    """
    Order item model for individual products in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    product_name = models.CharField(max_length=255, verbose_name='Tên sản phẩm')
    product_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='Giá tại thời điểm đặt')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')

    class Meta:
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    @property
    def subtotal(self):
        """Calculate subtotal for this item."""
        return self.product_price * self.quantity


class Coupon(models.Model):
    """
    Coupon model for discount codes.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Phần trăm'),
        ('amount', 'Số tiền cố định'),
    ]
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Mã giảm giá'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Tên chương trình'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percent',
        verbose_name='Loại giảm giá'
    )
    discount_value = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        verbose_name='Giá trị giảm'
    )
    min_order_amount = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name='Đơn tối thiểu'
    )
    max_discount = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='Giảm tối đa'
    )
    start_date = models.DateTimeField(
        verbose_name='Ngày bắt đầu'
    )
    end_date = models.DateTimeField(
        verbose_name='Ngày kết thúc'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Hoạt động'
    )
    usage_limit = models.IntegerField(
        default=100,
        verbose_name='Giới hạn sử dụng'
    )
    used_count = models.IntegerField(
        default=0,
        verbose_name='Đã sử dụng'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Cập nhật cuối'
    )

    class Meta:
        verbose_name = 'Mã giảm giá'
        verbose_name_plural = 'Mã giảm giá'
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.code} - {self.name}'

    def is_valid(self):
        """Check if coupon is valid."""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            self.used_count < self.usage_limit
        )


class SpecialPromotion(models.Model):
    """
    Special promotion model for featured products on home page (max 5).
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='special_promotions',
        verbose_name='Sản phẩm'
    )
    discount_percent = models.PositiveIntegerField(
        default=0,
        verbose_name='Giảm giá (%)'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Hoạt động'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Cập nhật cuối'
    )

    class Meta:
        verbose_name = 'Khuyến mãi đặc biệt'
        verbose_name_plural = 'Khuyến mãi đặc biệt'
        ordering = ['-created_at']

    def __str__(self):
        return f'Khuyến mãi: {self.product.name} - Giảm {self.discount_percent}%'

    @property
    def discounted_price(self):
        """Calculate discounted price."""
        return self.product.price * (100 - self.discount_percent) / 100

    def save(self, *args, **kwargs):
        # Check limit of 5 promotions
        if not self.pk and SpecialPromotion.objects.count() >= 5:
            raise ValueError('Chỉ được phép có tối đa 5 khuyến mãi đặc biệt')
        super().save(*args, **kwargs)
