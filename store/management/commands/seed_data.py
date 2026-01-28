"""
Custom management command to seed the database with sample data.
"""

from django.core.management.base import BaseCommand
from store.models import Category, Product, Coupon
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create categories
        categories = self.create_categories()
        
        # Create products
        self.create_products(categories)
        
        # Create coupons
        self.create_coupons()
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))

    def create_categories(self):
        """Create product categories."""
        categories_data = [
            {'name': 'iPhone', 'sort_order': 1},
            {'name': 'Samsung', 'sort_order': 2},
            {'name': 'Xiaomi', 'sort_order': 3},
            {'name': 'OPPO', 'sort_order': 4},
            {'name': 'vivo', 'sort_order': 5},
            {'name': 'realme', 'sort_order': 6},
            {'name': 'Honor', 'sort_order': 7},
            {'name': 'RedMagic', 'sort_order': 8},
            {'name': 'Tecno', 'sort_order': 9},
            {'name': 'Benco', 'sort_order': 10},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'sort_order': cat_data['sort_order'],
                    'is_active': True,
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'  Created category: {category.name}')
            else:
                self.stdout.write(f'  Category already exists: {category.name}')
        
        return categories

    def create_products(self, categories):
        """Create sample products."""
        products_data = [
            # iPhone products
            {
                'name': 'iPhone 16 Pro Max 256GB',
                'description': 'iPhone 16 Pro Max với màn hình Super Retina XDR 6.9 inch, chip A18 Pro, camera 48MP, pin suốt ngày.',
                'price': 34990000,
                'original_price': None,
                'brand': 'Apple',
                'category_name': 'iPhone',
                'image': 'images/products/iphone/iphone-16-pro-max.jpg',
                'stock': 50,
                'is_featured': True,
            },
            {
                'name': 'iPhone 16 Pro 128GB',
                'description': 'iPhone 16 Pro với camera tetraprism 5x, chip A18 Pro, thiết kế sang trọng.',
                'price': 28990000,
                'original_price': 32990000,
                'brand': 'Apple',
                'category_name': 'iPhone',
                'image': 'images/products/iphone/iphone-16-pro.jpg',
                'stock': 30,
                'is_featured': True,
            },
            {
                'name': 'iPhone 16 128GB',
                'description': 'iPhone 16 với Action Button, chip A18, camera 48MP, 5 màu sắc mới.',
                'price': 22990000,
                'original_price': None,
                'brand': 'Apple',
                'category_name': 'iPhone',
                'image': 'images/products/iphone/iphone-16.jpg',
                'stock': 100,
                'is_featured': False,
            },
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'description': 'iPhone 15 Pro Max với khung titanium, chip A17 Pro, camera 5x quang học.',
                'price': 32990000,
                'original_price': 39990000,
                'brand': 'Apple',
                'category_name': 'iPhone',
                'image': 'images/products/iphone/iphone-15-pro-max.jpg',
                'stock': 25,
                'is_featured': True,
            },
            {
                'name': 'iPhone 15 128GB',
                'description': 'iPhone 15 với Dynamic Island, camera 48MP, cổng USB-C.',
                'price': 19990000,
                'original_price': None,
                'brand': 'Apple',
                'category_name': 'iPhone',
                'image': 'images/products/iphone/iphone-15.jpg',
                'stock': 80,
                'is_featured': False,
            },
            
            # Samsung products
            {
                'name': 'Samsung Galaxy S24 Ultra 256GB',
                'description': 'Samsung Galaxy S24 Ultra với S Pen, camera 200MP, AI features.',
                'price': 28990000,
                'original_price': 34990000,
                'brand': 'Samsung',
                'category_name': 'Samsung',
                'image': 'images/products/samsung/s24-ultra.jpg',
                'stock': 40,
                'is_featured': True,
            },
            {
                'name': 'Samsung Galaxy S24+ 256GB',
                'description': 'Samsung Galaxy S24+ với màn hình 6.7 inch, chip Snapdragon 8 Gen 3.',
                'price': 24990000,
                'original_price': None,
                'brand': 'Samsung',
                'category_name': 'Samsung',
                'image': 'images/products/samsung/s24-plus.jpg',
                'stock': 35,
                'is_featured': False,
            },
            {
                'name': 'Samsung Galaxy Z Fold 5 256GB',
                'description': 'Điện thoại gập ngang, màn hình 7.8 inch, chip Snapdragon 8 Gen 2.',
                'price': 35990000,
                'original_price': 42990000,
                'brand': 'Samsung',
                'category_name': 'Samsung',
                'image': 'images/products/samsung/z-fold-5.jpg',
                'stock': 15,
                'is_featured': True,
            },
            {
                'name': 'Samsung Galaxy A55 5G',
                'description': 'Samsung Galaxy A55 với màn hình Super AMOLED 6.6 inch, camera 50MP.',
                'price': 10990000,
                'original_price': None,
                'brand': 'Samsung',
                'category_name': 'Samsung',
                'image': 'images/products/samsung/a55.jpg',
                'stock': 120,
                'is_featured': False,
            },
            
            # Xiaomi products
            {
                'name': 'Xiaomi 14 Ultra 512GB',
                'description': 'Xiaomi 14 Ultra với camera Leica, chip Snapdragon 8 Gen 3, pin 5000mAh.',
                'price': 24990000,
                'original_price': 32990000,
                'brand': 'Xiaomi',
                'category_name': 'Xiaomi',
                'image': 'images/products/xiaomi/14-ultra.jpg',
                'stock': 20,
                'is_featured': True,
            },
            {
                'name': 'Xiaomi 14 Pro 512GB',
                'description': 'Xiaomi 14 Pro với màn hình cong, chip Snapdragon 8 Gen 3.',
                'price': 21990000,
                'original_price': None,
                'brand': 'Xiaomi',
                'category_name': 'Xiaomi',
                'image': 'images/products/xiaomi/14-pro.jpg',
                'stock': 25,
                'is_featured': False,
            },
            {
                'name': 'Xiaomi Redmi Note 13 Pro 5G',
                'description': 'Xiaomi Redmi Note 13 Pro với camera 200MP, màn hình 1.5K.',
                'price': 8990000,
                'original_price': 10990000,
                'brand': 'Xiaomi',
                'category_name': 'Xiaomi',
                'image': 'images/products/xiaomi/note-13-pro.jpg',
                'stock': 150,
                'is_featured': False,
            },
            
            # OPPO products
            {
                'name': 'OPPO Find X8 Pro',
                'description': 'OPPO Find X8 Pro với Hasselblad camera, chip Dimensity 9400.',
                'price': 29990000,
                'original_price': None,
                'brand': 'OPPO',
                'category_name': 'OPPO',
                'image': 'images/products/oppo/find-x8-pro.jpg',
                'stock': 30,
                'is_featured': True,
            },
            {
                'name': 'OPPO Find X8',
                'description': 'OPPO Find X8 với camera telephoto periscope, AI features.',
                'price': 24990000,
                'original_price': 29990000,
                'brand': 'OPPO',
                'category_name': 'OPPO',
                'image': 'images/products/oppo/find-x8.jpg',
                'stock': 40,
                'is_featured': False,
            },
            {
                'name': 'OPPO Reno12 Pro 5G',
                'description': 'OPPO Reno12 Pro với AI portrait, màn hình cong 120Hz.',
                'price': 16990000,
                'original_price': None,
                'brand': 'OPPO',
                'category_name': 'OPPO',
                'image': 'images/products/oppo/reno12-pro.jpg',
                'stock': 60,
                'is_featured': False,
            },
            
            # vivo products
            {
                'name': 'vivo X200 Pro',
                'description': 'vivo X200 Pro với camera ZEISS, chip Dimensity 9400.',
                'price': 32990000,
                'original_price': None,
                'brand': 'vivo',
                'category_name': 'vivo',
                'image': 'images/products/vivo/x200-pro.jpg',
                'stock': 25,
                'is_featured': True,
            },
            {
                'name': 'vivo X100 Pro',
                'description': 'vivo X100 Pro với ZEISS camera, chip Dimensity 9300.',
                'price': 26990000,
                'original_price': 32990000,
                'brand': 'vivo',
                'category_name': 'vivo',
                'image': 'images/products/vivo/x100-pro.jpg',
                'stock': 35,
                'is_featured': True,
            },
            {
                'name': 'vivo V30e 5G',
                'description': 'vivo V30e với camera 50MP, pin 5000mAh, sạc nhanh 44W.',
                'price': 9990000,
                'original_price': None,
                'brand': 'vivo',
                'category_name': 'vivo',
                'image': 'images/products/vivo/v30e.jpg',
                'stock': 80,
                'is_featured': False,
            },
            
            # realme products
            {
                'name': 'realme GT 6',
                'description': 'realme GT 6 với chip Snapdragon 8s Gen 3, sạc 120W.',
                'price': 14990000,
                'original_price': 17990000,
                'brand': 'realme',
                'category_name': 'realme',
                'image': 'images/products/realme/gt-6.jpg',
                'stock': 45,
                'is_featured': True,
            },
            {
                'name': 'realme 12 Pro+ 5G',
                'description': 'realme 12 Pro+ với camera periscope 64MP, design sang trọng.',
                'price': 10990000,
                'original_price': None,
                'brand': 'realme',
                'category_name': 'realme',
                'image': 'images/products/realme/12-pro-plus.jpg',
                'stock': 70,
                'is_featured': False,
            },
            {
                'name': 'realme C67 5G',
                'description': 'realme C67 với camera 108MP, pin 5000mAh.',
                'price': 4990000,
                'original_price': None,
                'brand': 'realme',
                'category_name': 'realme',
                'image': 'images/products/realme/c67.jpg',
                'stock': 100,
                'is_featured': False,
            },
            
            # Honor products
            {
                'name': 'Honor Magic 7 Pro',
                'description': 'Honor Magic 7 Pro với AI-powered camera, chip Snapdragon 8 Elite.',
                'price': 29990000,
                'original_price': None,
                'brand': 'Honor',
                'category_name': 'Honor',
                'image': 'images/products/honor/magic-7-pro.jpg',
                'stock': 20,
                'is_featured': True,
            },
            {
                'name': 'Honor 200 Pro',
                'description': 'Honor 200 Pro với camera Harcourt Portrait.',
                'price': 15990000,
                'original_price': 19990000,
                'brand': 'Honor',
                'category_name': 'Honor',
                'image': 'images/products/honor/200-pro.jpg',
                'stock': 40,
                'is_featured': False,
            },
            
            # RedMagic products
            {
                'name': 'RedMagic 9 Pro+',
                'description': 'Điện thoại gaming với quạt lấy gió, chip Snapdragon 8 Gen 3.',
                'price': 24990000,
                'original_price': 28990000,
                'brand': 'RedMagic',
                'category_name': 'RedMagic',
                'image': 'images/products/redmagic/9-pro-plus.jpg',
                'stock': 25,
                'is_featured': True,
            },
            {
                'name': 'RedMagic 9 Pro',
                'description': 'RedMagic 9 Pro với hệ thống làm mát thế hệ 10.',
                'price': 21990000,
                'original_price': None,
                'brand': 'RedMagic',
                'category_name': 'RedMagic',
                'image': 'images/products/redmagic/9-pro.jpg',
                'stock': 30,
                'is_featured': False,
            },
            
            # Tecno products
            {
                'name': 'Tecno Phantom V Fold2',
                'description': 'Điện thoại gập ngang, màn hình 7.85 inch, thiết kế sang trọng.',
                'price': 24990000,
                'original_price': None,
                'brand': 'Tecno',
                'category_name': 'Tecno',
                'image': 'images/products/tecno/phantom-v-fold2.jpg',
                'stock': 15,
                'is_featured': True,
            },
            {
                'name': 'Tecno Camon 30 Premier',
                'description': 'Tecno Camon 30 Premier với camera 50MP, AI features.',
                'price': 11990000,
                'original_price': 14990000,
                'brand': 'Tecno',
                'category_name': 'Tecno',
                'image': 'images/products/tecno/camon-30-premier.jpg',
                'stock': 50,
                'is_featured': False,
            },
            {
                'name': 'Tecno Spark 20 Pro+',
                'description': 'Tecno Spark 20 Pro+ với camera 108MP, pin 5000mAh.',
                'price': 5990000,
                'original_price': None,
                'brand': 'Tecno',
                'category_name': 'Tecno',
                'image': 'images/products/tecno/spark-20-pro-plus.jpg',
                'stock': 100,
                'is_featured': False,
            },
            
            # Benco products
            {
                'name': 'Benco V80',
                'description': 'Benco V80 với pin 5000mAh, màn hình 6.5 inch HD+.',
                'price': 1990000,
                'original_price': None,
                'brand': 'Benco',
                'category_name': 'Benco',
                'image': 'images/products/benco/v80.jpg',
                'stock': 200,
                'is_featured': False,
            },
            {
                'name': 'Benco V80s',
                'description': 'Benco V80s với camera 50MP, pin 5000mAh.',
                'price': 2490000,
                'original_price': 2990000,
                'brand': 'Benco',
                'category_name': 'Benco',
                'image': 'images/products/benco/v80s.jpg',
                'stock': 180,
                'is_featured': False,
            },
            {
                'name': 'Benco S1',
                'description': 'Benco S1 với màn hình 6.8 inch, pin 5000mAh.',
                'price': 2990000,
                'original_price': None,
                'brand': 'Benco',
                'category_name': 'Benco',
                'image': 'images/products/benco/s1.jpg',
                'stock': 150,
                'is_featured': False,
            },
        ]
        
        created_count = 0
        for prod_data in products_data:
            category = categories.get(prod_data['category_name'])
            if category:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'original_price': prod_data.get('original_price'),
                        'image': prod_data['image'],
                        'category': category,
                        'brand': prod_data['brand'],
                        'stock': prod_data['stock'],
                        'is_featured': prod_data.get('is_featured', False),
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(f'  Created product: {product.name}')
                else:
                    self.stdout.write(f'  Product already exists: {product.name}')
            
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new products'))

    def create_coupons(self):
        """Create sample discount coupons."""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        coupons_data = [
            {
                'code': 'WELCOME500',
                'name': 'Chao mung thanh vien moi',
                'description': 'Giam 500k cho don hang tu 5 triệu',
                'discount_type': 'amount',
                'discount_value': 500000,
                'min_order_amount': 5000000,
                'max_discount': 500000,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=90),
                'usage_limit': 1000,
            },
            {
                'code': 'SALE10',
                'name': 'Giam 10% toan bo',
                'description': 'Giam 10% cho tat ca san pham, toi da 200k',
                'discount_type': 'percent',
                'discount_value': 10,
                'min_order_amount': 0,
                'max_discount': 200000,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=30),
                'usage_limit': 500,
            },
            {
                'code': 'FREESHIP',
                'name': 'Mien phi van chuyen',
                'description': 'Mien phi van chuyen cho don hang tu 2 triệu',
                'discount_type': 'amount',
                'discount_value': 30000,
                'min_order_amount': 2000000,
                'max_discount': 30000,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=60),
                'usage_limit': 2000,
            },
            {
                'code': 'IPHONE15',
                'name': 'Giam 1 triệu iPhone 15',
                'description': 'Giam 1 triệu khi mua iPhone 15 series',
                'discount_type': 'amount',
                'discount_value': 1000000,
                'min_order_amount': 20000000,
                'max_discount': 1000000,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=45),
                'usage_limit': 200,
            },
            {
                'code': 'NEWYEAR2026',
                'name': 'Tet 2026 Sale',
                'description': 'Giam 15% cho don hang tu 10 triệu',
                'discount_type': 'percent',
                'discount_value': 15,
                'min_order_amount': 10000000,
                'max_discount': 3000000,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=30),
                'usage_limit': 300,
            },
        ]
        
        created_count = 0
        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created coupon: {coupon.code}')
            else:
                self.stdout.write(f'  Coupon already exists: {coupon.code}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new coupons'))

