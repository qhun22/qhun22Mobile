"""
Script to populate database with phone products for ShopMobile.
Usage: python manage.py shell < populate_phones.py
"""

from store.models import Category, Product
from django.utils.text import slugify

# Clear existing products and categories
print("🗑️  Đang xóa dữ liệu cũ...")
Product.objects.all().delete()
Category.objects.all().delete()

# Create categories for each brand
print("📱 Đang tạo danh mục...")

categories_data = [
    {'name': 'iPhone (Apple)', 'slug': 'iphone-apple', 'description': 'Điện thoại iPhone chính hãng, hệ điều hành iOS mượt mà'},
    {'name': 'Samsung', 'slug': 'samsung', 'description': 'Điện thoại Samsung đa dạng từ giá rẻ đến cao cấp'},
    {'name': 'Xiaomi', 'slug': 'xiaomi', 'description': 'Điện thoại Xiaomi cấu hình mạnh, giá tốt'},
    {'name': 'OPPO', 'slug': 'oppo', 'description': 'Điện thoại OPPO thiết kế thời trang, camera selfie đẹp'},
    {'name': 'Vivo', 'slug': 'vivo', 'description': 'Điện thoại Vivo thiết kế mỏng nhẹ, camera chụp đêm tốt'},
    {'name': 'Realme', 'slug': 'realme', 'description': 'Điện thoại Realme sạc nhanh, hiệu năng gaming tốt'},
    {'name': 'Honor', 'slug': 'honor', 'description': 'Điện thoại Honor độ bền cao, đầy đủ dịch vụ Google'},
    {'name': 'RedMagic', 'slug': 'redmagic', 'description': 'Điện thoại gaming RedMagic cấu hình mạnh nhất'},
    {'name': 'Tecno', 'slug': 'tecno', 'description': 'Điện thoại Tecno cấu hình hời, thiết kế độc lạ'},
    {'name': 'Benco', 'slug': 'benco', 'description': 'Điện thoại Benco phân khúc giá rẻ, học sinh sinh viên'},
]

categories = {}
for cat_data in categories_data:
    cat = Category.objects.create(**cat_data)
    categories[cat_data['slug']] = cat
    print(f"  ✅ {cat_data['name']}")

# Products data
print("\n📦 Đang thêm sản phẩm...")

products_data = [
    # iPhone
    {'name': 'iPhone 15 Pro Max', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 34990000, 'original_price': 36990000, 'stock': 50, 'discount_percent': 5, 'description': 'iPhone 15 Pro Max với chip A17 Pro, khung titanium, camera 48MP, màn hình 6.7 inch Super Retina XDR.'},
    {'name': 'iPhone 15 Pro', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 29990000, 'original_price': 31990000, 'stock': 50, 'discount_percent': 6, 'description': 'iPhone 15 Pro với chip A17 Pro, khung titanium cao cấp, camera 48MP chuyên nghiệp.'},
    {'name': 'iPhone 15 Plus', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 25990000, 'original_price': 27990000, 'stock': 100, 'discount_percent': 7, 'description': 'iPhone 15 Plus màn hình lớn 6.7 inch, chip A16 Bionic, thiết kế Dynamic Island.'},
    {'name': 'iPhone 15', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 22990000, 'original_price': 24990000, 'stock': 100, 'discount_percent': 8, 'description': 'iPhone 15 với chip A16 Bionic, camera 48MP, cổng USB-C.'},
    {'name': 'iPhone 14', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 18990000, 'original_price': 20990000, 'stock': 150, 'discount_percent': 10, 'description': 'iPhone 14 với chip A15 Bionic, camera 12MP, màn hình 6.1 inch.'},
    {'name': 'iPhone 13', 'brand': 'Apple', 'category': categories['iphone-apple'], 'price': 14990000, 'original_price': 16990000, 'stock': 200, 'discount_percent': 12, 'description': 'iPhone 13 chip A15 Bionic, màn hình Super Retina XDR 6.1 inch, camera kép 12MP.'},
    
    # Samsung
    {'name': 'Samsung Galaxy S24 Ultra', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 32990000, 'original_price': 34990000, 'stock': 50, 'discount_percent': 6, 'description': 'Samsung Galaxy S24 Ultra với S Pen, chip Snapdragon 8 Gen 3, camera 200MP.'},
    {'name': 'Samsung Galaxy S24+', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 26990000, 'original_price': 28990000, 'stock': 80, 'discount_percent': 7, 'description': 'Samsung Galaxy S24+ màn hình 6.7 inch, chip Snapdragon 8 Gen 3, AI thông minh.'},
    {'name': 'Samsung Galaxy S24', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 22990000, 'original_price': 24990000, 'stock': 100, 'discount_percent': 8, 'description': 'Samsung Galaxy S24 nhỏ gọn với chip Snapdragon 8 Gen 3, màn hình 6.2 inch.'},
    {'name': 'Samsung Galaxy Z Fold5', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 39990000, 'original_price': 42990000, 'stock': 30, 'discount_percent': 7, 'description': 'Samsung Galaxy Z Fold5 điện thoại gập, màn hình 7.8 inch, hỗ trợ S Pen.'},
    {'name': 'Samsung Galaxy Z Flip5', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 24990000, 'original_price': 26990000, 'stock': 60, 'discount_percent': 7, 'description': 'Samsung Galaxy Z Flip5 gập nhỏ gọn, màn hình ngoài lớn, chip Snapdragon 8 Gen 2.'},
    {'name': 'Samsung Galaxy A55 5G', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 11990000, 'original_price': 13990000, 'stock': 200, 'discount_percent': 14, 'description': 'Samsung Galaxy A55 5G màn hình 6.6 inch 120Hz, camera 50MP, khung kim loại.'},
    {'name': 'Samsung Galaxy A35 5G', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 9990000, 'original_price': 11990000, 'stock': 200, 'discount_percent': 17, 'description': 'Samsung Galaxy A35 5G màn hình sáng rực rỡ, camera OIS, pin 5000mAh.'},
    {'name': 'Samsung Galaxy A25 5G', 'brand': 'Samsung', 'category': categories['samsung'], 'price': 7990000, 'original_price': 9490000, 'stock': 250, 'discount_percent': 16, 'description': 'Samsung Galaxy A25 5G màn hình Super AMOLED, chip Exynos 1280.'},
    
    # Xiaomi
    {'name': 'Xiaomi 14 Ultra', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 29990000, 'original_price': 32990000, 'stock': 50, 'discount_percent': 9, 'description': 'Xiaomi 14 Ultra camera Leica 50MP, chip Snapdragon 8 Gen 3, sạc 90W.'},
    {'name': 'Xiaomi 14', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 23990000, 'original_price': 26990000, 'stock': 80, 'discount_percent': 11, 'description': 'Xiaomi 14 nhỏ gọn cao cấp, camera Leica, chip Snapdragon 8 Gen 3.'},
    {'name': 'Redmi Note 13 Pro+ 5G', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 11990000, 'original_price': 13990000, 'stock': 200, 'discount_percent': 14, 'description': 'Redmi Note 13 Pro+ camera 200MP, màn hình 1.5K, sạc 120W.'},
    {'name': 'Redmi Note 13 Pro', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 8990000, 'original_price': 10990000, 'stock': 250, 'discount_percent': 18, 'description': 'Redmi Note 13 Pro màn hình 120Hz, camera 108MP, pin 5000mAh.'},
    {'name': 'Redmi Note 13', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 5990000, 'original_price': 7490000, 'stock': 300, 'discount_percent': 20, 'description': 'Redmi Note 13 màn hình AMOLED 120Hz, camera 108MP, giá tốt.'},
    {'name': 'Redmi 13C', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 4490000, 'original_price': 5490000, 'stock': 400, 'discount_percent': 18, 'description': 'Redmi 13C chip MediaTek Helio G85, màn hình lớn, pin 5000mAh.'},
    {'name': 'POCO X6 Pro 5G', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 10990000, 'original_price': 12990000, 'stock': 150, 'discount_percent': 15, 'description': 'POCO X6 Pro chip Dimensity 8300-Ultra, gaming mượt, sạc 67W.'},
    {'name': 'POCO F6', 'brand': 'Xiaomi', 'category': categories['xiaomi'], 'price': 12990000, 'original_price': 14990000, 'stock': 100, 'discount_percent': 13, 'description': 'POCO F6 chip Snapdragon 8s Gen 3, màn hình 1.5K, sạc 90W.'},
    
    # OPPO
    {'name': 'OPPO Find N3', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 35990000, 'original_price': 39990000, 'stock': 30, 'discount_percent': 10, 'description': 'OPPO Find N3 điện thoại gập, màn hình lớn, camera Hasselblad.'},
    {'name': 'OPPO Find N3 Flip', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 24990000, 'original_price': 27990000, 'stock': 50, 'discount_percent': 10, 'description': 'OPPO Find N3 Flip gập nhỏ, màn hình ngoài lớn, camera chân dung.'},
    {'name': 'OPPO Reno11 Pro 5G', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 14990000, 'original_price': 16990000, 'stock': 100, 'discount_percent': 12, 'description': 'OPPO Reno11 Pro 5G camera chân dung, sạc 80W, màn hình cong 3D.'},
    {'name': 'OPPO Reno11 5G', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 11990000, 'original_price': 13990000, 'stock': 150, 'discount_percent': 14, 'description': 'OPPO Reno11 5G thiết kế mỏng nhẹ, camera 50MP, sạc nhanh.'},
    {'name': 'OPPO Reno11 F 5G', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 9990000, 'original_price': 11990000, 'stock': 150, 'discount_percent': 17, 'description': 'OPPO Reno11 F 5G màn hình AMOLED, thiết kế thời trang.'},
    {'name': 'OPPO A98', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 7990000, 'original_price': 9490000, 'stock': 200, 'discount_percent': 16, 'description': 'OPPO A98 màn hình 120Hz, sạc 67W, pin 5000mAh.'},
    {'name': 'OPPO A78', 'brand': 'OPPO', 'category': categories['oppo'], 'price': 5990000, 'original_price': 7490000, 'stock': 250, 'discount_percent': 20, 'description': 'OPPO A78 màn hình sáng, sạc nhanh SuperVOOC, camera 50MP.'},
    
    # Vivo
    {'name': 'Vivo V30', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 13990000, 'original_price': 15990000, 'stock': 100, 'discount_percent': 12, 'description': 'Vivo V30 camera chụp đêm Aura Light, sạc 80W, màn hình cong.'},
    {'name': 'Vivo V30e', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 10990000, 'original_price': 12990000, 'stock': 150, 'discount_percent': 15, 'description': 'Vivo V30e thiết kế mỏng nhẹ, camera 50MP, pin 5000mAh.'},
    {'name': 'Vivo V29 5G', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 11990000, 'original_price': 13990000, 'stock': 150, 'discount_percent': 14, 'description': 'Vivo V29 5G camera Aura Light, màn hình 1.5K, sạc 80W.'},
    {'name': 'Vivo Y100', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 7990000, 'original_price': 9490000, 'stock': 200, 'discount_percent': 16, 'description': 'Vivo Y100 màn hình AMOLED 120Hz, thiết kế thời trang.'},
    {'name': 'Vivo Y03', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 4490000, 'original_price': 5490000, 'stock': 300, 'discount_percent': 18, 'description': 'Vivo Y03 màn hình lớn 6.56 inch, pin 5000mAh, giá rẻ.'},
    {'name': 'Vivo X100 Pro', 'brand': 'Vivo', 'category': categories['vivo'], 'price': 28990000, 'original_price': 31990000, 'stock': 50, 'discount_percent': 9, 'description': 'Vivo X100 Pro camera Zeiss, chip Dimensity 9300, sạc 100W.'},
    
    # Realme
    {'name': 'Realme 12 Pro+ 5G', 'brand': 'Realme', 'category': categories['realme'], 'price': 11990000, 'original_price': 13990000, 'stock': 150, 'discount_percent': 14, 'description': 'Realme 12 Pro+ camera 200MP, zoom 3x, thiết kế sang trọng.'},
    {'name': 'Realme 11 Pro+ 5G', 'brand': 'Realme', 'category': categories['realme'], 'price': 10990000, 'original_price': 12990000, 'stock': 150, 'discount_percent': 15, 'description': 'Realme 11 Pro+ camera 200MP, sạc 100W, màn hình cong.'},
    {'name': 'Realme 11', 'brand': 'Realme', 'category': categories['realme'], 'price': 6990000, 'original_price': 8490000, 'stock': 250, 'discount_percent': 18, 'description': 'Realme 11 màn hình sáng, camera 108MP, pin 5000mAh.'},
    {'name': 'Realme 10', 'brand': 'Realme', 'category': categories['realme'], 'price': 5990000, 'original_price': 7490000, 'stock': 250, 'discount_percent': 20, 'description': 'Realme 10 màn hình 90Hz, chip Helio G99, giá tốt.'},
    {'name': 'Realme C67', 'brand': 'Realme', 'category': categories['realme'], 'price': 4990000, 'original_price': 5990000, 'stock': 350, 'discount_percent': 17, 'description': 'Realme C67 camera 108MP, màn hình 90Hz, pin 5000mAh.'},
    {'name': 'Realme C55', 'brand': 'Realme', 'category': categories['realme'], 'price': 4490000, 'original_price': 5490000, 'stock': 400, 'discount_percent': 18, 'description': 'Realme C55 màn hình lớn, sạc nhanh 33W, camera 64MP.'},
    {'name': 'Realme C53', 'brand': 'Realme', 'category': categories['realme'], 'price': 3990000, 'original_price': 4990000, 'stock': 400, 'discount_percent': 20, 'description': 'Realme C53 thiết kế mỏng, màn hình 90Hz, giá rẻ.'},
    
    # Honor
    {'name': 'Honor Magic6 Pro', 'brand': 'Honor', 'category': categories['honor'], 'price': 28990000, 'original_price': 31990000, 'stock': 50, 'discount_percent': 9, 'description': 'Honor Magic6 Pro chip Snapdragon 8 Gen 3, camera 180MP, pin 5600mAh.'},
    {'name': 'Honor 90', 'brand': 'Honor', 'category': categories['honor'], 'price': 11990000, 'original_price': 13990000, 'stock': 100, 'discount_percent': 14, 'description': 'Honor 90 màn hình 120Hz, camera 200MP, thiết kế sang trọng.'},
    {'name': 'Honor 90 Lite', 'brand': 'Honor', 'category': categories['honor'], 'price': 7990000, 'original_price': 9490000, 'stock': 150, 'discount_percent': 16, 'description': 'Honor 90 Lite 5G, màn hình 90Hz, camera 100MP.'},
    {'name': 'Honor X9b', 'brand': 'Honor', 'category': categories['honor'], 'price': 8990000, 'original_price': 10990000, 'stock': 150, 'discount_percent': 18, 'description': 'Honor X9b màn hình siêu bền, pin 5800mAh, chống va đập.'},
    {'name': 'Honor X8b', 'brand': 'Honor', 'category': categories['honor'], 'price': 6990000, 'original_price': 8490000, 'stock': 200, 'discount_percent': 18, 'description': 'Honor X8b màn hình sáng, camera 108MP, thiết kế mỏng nhẹ.'},
    {'name': 'Honor X7b', 'brand': 'Honor', 'category': categories['honor'], 'price': 4990000, 'original_price': 5990000, 'stock': 300, 'discount_percent': 17, 'description': 'Honor X7b pin 6000mAh, màn hình lớn, giá rẻ.'},
    
    # RedMagic
    {'name': 'RedMagic 9 Pro', 'brand': 'RedMagic', 'category': categories['redmagic'], 'price': 27990000, 'original_price': 30990000, 'stock': 50, 'discount_percent': 10, 'description': 'RedMagic 9 Pro gaming phone, quạt tản nhiệt, chip Snapdragon 8 Gen 3.'},
    {'name': 'RedMagic 9 Pro+', 'brand': 'RedMagic', 'category': categories['redmagic'], 'price': 31990000, 'original_price': 34990000, 'stock': 30, 'discount_percent': 9, 'description': 'RedMagic 9 Pro+ RAM 24GB, sạc 165W, gaming không giới hạn.'},
    {'name': 'RedMagic 8S Pro', 'brand': 'RedMagic', 'category': categories['redmagic'], 'price': 24990000, 'original_price': 27990000, 'stock': 50, 'discount_percent': 11, 'description': 'RedMagic 8S Pro quạt tản nhiệt, màn hình không khuyết, chip Snapdragon 8 Gen 2.'},
    
    # Tecno
    {'name': 'Tecno Phantom V Fold', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 27990000, 'original_price': 31990000, 'stock': 30, 'discount_percent': 13, 'description': 'Tecno Phantom V Fold điện thoại gập, màn hình lớn, giá tốt.'},
    {'name': 'Tecno Phantom V Flip', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 17990000, 'original_price': 20990000, 'stock': 50, 'discount_percent': 14, 'description': 'Tecno Phantom V Flip gập nhỏ, màn hình ngoài vuông độc đáo.'},
    {'name': 'Tecno Camon 30 Premier', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 11990000, 'original_price': 13990000, 'stock': 100, 'discount_percent': 14, 'description': 'Tecno Camon 30 Premier camera 50MP, sạc 70W, thiết kế đẹp.'},
    {'name': 'Tecno Camon 30 Pro', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 8990000, 'original_price': 10990000, 'stock': 150, 'discount_percent': 18, 'description': 'Tecno Camon 30 Pro camera chụp đêm, màn hình 144Hz.'},
    {'name': 'Tecno Camon 20', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 6990000, 'original_price': 8490000, 'stock': 200, 'discount_percent': 18, 'description': 'Tecno Camon 20 camera 64MP, thiết kế độc đáo, giá tốt.'},
    {'name': 'Tecno Pova 6 Pro', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 7990000, 'original_price': 9490000, 'stock': 150, 'discount_percent': 16, 'description': 'Tecno Pova 6 Pro pin 6000mAh, sạc 70W, gaming.'},
    {'name': 'Tecno Spark 20 Pro+', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 5990000, 'original_price': 7490000, 'stock': 250, 'discount_percent': 20, 'description': 'Tecno Spark 20 Pro+ màn hình cong, camera 108MP, giá rẻ.'},
    {'name': 'Tecno Spark 20', 'brand': 'Tecno', 'category': categories['tecno'], 'price': 4490000, 'original_price': 5490000, 'stock': 350, 'discount_percent': 18, 'description': 'Tecno Spark 20 màn hình 90Hz, sạc nhanh, thiết kế trẻ trung.'},
    
    # Benco
    {'name': 'Benco S1 Pro', 'brand': 'Benco', 'category': categories['benco'], 'price': 4990000, 'original_price': 5990000, 'stock': 200, 'discount_percent': 17, 'description': 'Benco S1 Pro camera 108MP, màn hình lớn, giá học sinh sinh viên.'},
    {'name': 'Benco S1', 'brand': 'Benco', 'category': categories['benco'], 'price': 3990000, 'original_price': 4990000, 'stock': 250, 'discount_percent': 20, 'description': 'Benco S1 màn hình 6.5 inch, pin 5000mAh, cơ bản đủ dùng.'},
    {'name': 'Benco V91', 'brand': 'Benco', 'category': categories['benco'], 'price': 3490000, 'original_price': 4490000, 'stock': 300, 'discount_percent': 22, 'description': 'Benco V91 màn hình HD+, pin 5000mAh, giá rẻ.'},
    {'name': 'Benco V90', 'brand': 'Benco', 'category': categories['benco'], 'price': 2990000, 'original_price': 3990000, 'stock': 350, 'discount_percent': 25, 'description': 'Benco V90 màn hình lớn, pin trâu, rất rẻ.'},
    {'name': 'Benco V82', 'brand': 'Benco', 'category': categories['benco'], 'price': 2490000, 'original_price': 3490000, 'stock': 400, 'discount_percent': 29, 'description': 'Benco V82 điện thoại cơ bản, giá sinh viên.'},
    {'name': 'Benco Y11', 'brand': 'Benco', 'category': categories['benco'], 'price': 1990000, 'original_price': 2990000, 'stock': 500, 'discount_percent': 33, 'description': 'Benco Y11 siêu rẻ, đủ dùng cho nhu cầu cơ bản.'},
]

count = 0
for prod_data in products_data:
    prod = Product.objects.create(
        name=prod_data['name'],
        slug=slugify(prod_data['name']),
        description=prod_data['description'],
        price=prod_data['price'],
        original_price=prod_data['original_price'],
        image='',  # No image - will use placeholder
        category=prod_data['category'],
        brand=prod_data['brand'],
        stock=prod_data['stock'],
        is_active=True,
        is_featured=prod_data.get('is_featured', False),
        discount_percent=prod_data.get('discount_percent', 0),
    )
    count += 1
    print(f"  ✅ {prod_data['name']} - {prod_data['price']:,}₫")

# Summary
print(f"\n🎉 Hoàn tất! Đã thêm:")
print(f"   - {len(categories_data)} danh mục")
print(f"   - {count} sản phẩm")
print(f"   - Tổng giá trị: {sum(p.price for p in Product.objects.all()):,}₫")



