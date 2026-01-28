"""
Store app views for shopmobile project.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from store.models import Category, Product, SpecialPromotion, Coupon
from store.forms import UserRegistrationForm, UserLoginForm, ForgotPasswordForm


# Home page view
def home(request):
    """
    Render the home page with product listings and promotions.
    Fetch products from database.
    """
    # Get search query
    search_query = request.GET.get('q', '')
    brand_filter = request.GET.get('brand', '')
    price_filter = request.GET.get('price', '')
    sort = request.GET.get('sort', 'default')

    # Get all active categories
    categories = Category.objects.filter(is_active=True).order_by('sort_order')

    # Get special promotions for promotion section (max 5)
    special_promotions = SpecialPromotion.objects.filter(
        is_active=True
    ).select_related('product', 'product__category')[:5]

    # Get all active products with filters
    products = Product.objects.filter(is_active=True).select_related('category')

    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Apply brand filter
    if brand_filter:
        products = products.filter(brand__iexact=brand_filter)

    # Apply price filter
    if price_filter:
        if price_filter == '0-2000000':
            products = products.filter(price__lt=2000000)
        elif price_filter == '2000000-4000000':
            products = products.filter(price__gte=2000000, price__lt=4000000)
        elif price_filter == '4000000-7000000':
            products = products.filter(price__gte=4000000, price__lt=7000000)
        elif price_filter == '7000000-13000000':
            products = products.filter(price__gte=7000000, price__lt=13000000)
        elif price_filter == '13000000-20000000':
            products = products.filter(price__gte=13000000, price__lt=20000000)
        elif price_filter == '20000000-999999999':
            products = products.filter(price__gte=20000000)

    # Apply sorting
    if sort == 'asc':
        products = products.order_by('price')
    elif sort == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at', '-is_featured')

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    product_page = paginator.get_page(page_number)

    context = {
        'page_title': 'QHUN22',
        'categories': categories,
        'special_promotions': special_promotions,
        'products': product_page,
        'search_query': search_query,
        'brand_filter': brand_filter,
        'price_filter': price_filter,
        'sort': sort,
        'total_products': products.count(),
    }
    return render(request, 'home.html', context)


# API endpoint for AJAX pagination
def api_products(request):
    """
    Return products as JSON for AJAX pagination.
    """
    import json
    
    # Get search query
    search_query = request.GET.get('q', '')
    brand_filter = request.GET.get('brand', '')
    price_filter = request.GET.get('price', '')
    sort = request.GET.get('sort', 'default')
    page = int(request.GET.get('page', 1))

    # Get all active products with filters
    products = Product.objects.filter(is_active=True).select_related('category')

    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Apply brand filter
    if brand_filter:
        products = products.filter(brand__iexact=brand_filter)

    # Apply price filter
    if price_filter:
        if price_filter == '0-2000000':
            products = products.filter(price__lt=2000000)
        elif price_filter == '2000000-4000000':
            products = products.filter(price__gte=2000000, price__lt=4000000)
        elif price_filter == '4000000-7000000':
            products = products.filter(price__gte=4000000, price__lt=7000000)
        elif price_filter == '7000000-13000000':
            products = products.filter(price__gte=7000000, price__lt=13000000)
        elif price_filter == '13000000-20000000':
            products = products.filter(price__gte=13000000, price__lt=20000000)
        elif price_filter == '20000000-999999999':
            products = products.filter(price__gte=20000000)

    # Apply sorting
    if sort == 'asc':
        products = products.order_by('price')
    elif sort == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at', '-is_featured')

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 10)
    product_page = paginator.get_page(page)

    # Build query string for pagination links
    def build_query(page_num):
        params = []
        if search_query: params.append(f'q={search_query}')
        if brand_filter: params.append(f'brand={brand_filter}')
        if price_filter: params.append(f'price={price_filter}')
        if sort != 'default': params.append(f'sort={sort}')
        params.append(f'page={page_num}')
        return '?' + '&'.join(params)

    # Serialize products
    products_data = []
    for product in product_page:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'brand': product.brand or '',
            'price': float(product.price),
            'original_price': float(product.original_price) if product.original_price else None,
            'discount_percent': product.discount_percent,
            'is_on_sale': product.is_on_sale,
            'image': str(product.image) if product.image else None,
            'stock': product.stock,
            'category_name': product.category.name if product.category else '',
        })

    return JsonResponse({
        'success': True,
        'products': products_data,
        'current_page': page,
        'total_pages': paginator.num_pages,
        'has_previous': product_page.has_previous(),
        'has_next': product_page.has_next(),
        'previous_page': build_query(page - 1) if product_page.has_previous() else None,
        'next_page': build_query(page + 1) if product_page.has_next() else None,
        'start_index': product_page.start_index(),
        'end_index': product_page.end_index(),
        'total_products': paginator.count,
        'filters': {
            'q': search_query,
            'brand': brand_filter,
            'price': price_filter,
            'sort': sort,
        }
    })


# Registration view
def register(request):
    """
    Handle user registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Đăng ký thành công, chào mừng bạn đến với QHUN22!')
                return redirect('home')
        # Form is invalid, continue to render with errors
    else:
        form = UserRegistrationForm()

    context = {
        'page_title': 'Đăng ký - QHUN22',
        'form': form,
    }
    return render(request, 'register.html', context)


# Login page view
def login_page(request):
    """
    Render the login page.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xin chào {user.first_name}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Vui lòng kiểm tra lại thông tin đăng nhập.')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin đăng nhập.')
    else:
        form = UserLoginForm()

    context = {
        'page_title': 'Đăng nhập - QHUN22',
        'form': form,
    }
    return render(request, 'login.html', context)


# Forgot password view (demo purpose)
def forgot_password(request):
    """
    Handle forgot password - demo only.
    Resets password to Qhun22@ if email exists.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                # Reset password using set_password() for proper hashing
                user.set_password('Qhun22@')
                user.save()
                messages.success(request, 'Mật khẩu mới đã được đặt là: Qhun22@')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Email không tồn tại trong hệ thống.')
        # Form is invalid
    else:
        form = ForgotPasswordForm()

    context = {
        'page_title': 'Quên mật khẩu - QHUN22',
        'form': form,
    }
    return render(request, 'forgot_password.html', context)


# Logout view
def logout_view(request):
    """
    Logout the user and redirect to home page.
    """
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')


# Profile view (requires login)
@login_required
def profile(request):
    """
    Render user profile page.
    """
    from store.forms import UserProfileForm
    from store.models import Order, Coupon
    from django.utils import timezone

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin đã được cập nhật thành công!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Get user orders
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    
    # Get valid coupons
    coupons = Coupon.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('end_date')

    context = {
        'page_title': 'Thông tin tài khoản - QHUN22',
        'user': request.user,
        'form': form,
        'orders': orders,
        'coupons': coupons,
    }
    return render(request, 'profile.html', context)


# Change password view (requires login)
@login_required
def change_password(request):
    """
    Handle password change for authenticated users.
    """
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mật khẩu đã được cập nhật thành công!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'page_title': 'Đổi mật khẩu - QHUN22',
        'form': form,
    }
    return render(request, 'profile.html', context)


# Feedback view (requires login)
@login_required
def feedback(request):
    """
    Handle user feedback submission.
    """
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if subject and message:
            # In a real app, you would save this to a database or send email
            # For demo, just show success message
            messages.success(request, 'Cảm ơn bạn đã gửi góp ý! Chúng tôi sẽ xem xét và phản hồi sớm nhất.')
            return redirect('profile')
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin góp ý.')

    context = {
        'page_title': 'Gop y - QHUN22',
    }
    return render(request, 'profile.html', context)


# Address views (requires login)
@login_required
def add_address(request):
    """
    Add new address for user.
    """
    from store.forms import AddressForm
    from store.models import Address

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Địa chỉ đã được thêm thành công!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, str(error))
    else:
        form = AddressForm()

    context = {
        'page_title': 'Thêm địa chỉ - QHUN22',
        'form': form,
    }
    return render(request, 'profile.html', context)


@login_required
def set_default_address(request, address_id):
    """
    Set an address as the default address.
    """
    from django.http import JsonResponse
    from store.models import Address

    if request.method == 'POST':
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            address.is_default = True
            address.save()
            return JsonResponse({'success': True, 'message': 'Địa chỉ mặc định đã được cập nhật!'})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Địa chỉ không tồn tại.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'}, status=400)
@login_required
def delete_address(request, address_id):
    """
    Delete an address.
    """
    from django.http import JsonResponse
    from store.models import Address

    if request.method == 'POST':
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            address.delete()
            return JsonResponse({'success': True, 'message': 'Địa chỉ đã được xóa!'})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Địa chỉ không tồn tại.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'}, status=400)
# Product detail view
def product_detail(request, slug):
    """
    Render product detail page.
    """
    from django.shortcuts import get_object_or_404

    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:5]

    # Get reviews for this product (empty list for now)
    reviews = []

    context = {
        'page_title': f'{product.name} - QHUN22',
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'product_detail.html', context)


# Admin Dashboard View
@login_required
def admin_dashboard(request):
    """
    Render admin dashboard with statistics.
    Only accessible by superuser/staff.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')
    
    from django.utils import timezone
    from datetime import datetime, timedelta
    from django.db.models import Sum, Count
    from django.contrib.auth.models import User
    from store.models import Order
    
    # Get current date/time
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Total orders
    total_orders = Order.objects.count()
    
    # Monthly revenue
    monthly_revenue = Order.objects.filter(
        created_at__gte=start_of_month
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Total revenue
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # New users this month
    new_users = User.objects.filter(
        date_joined__gte=start_of_month
    ).count()
    
    # Orders by status
    pending_orders = Order.objects.filter(status='pending').count()
    approved_orders = Order.objects.filter(status='approved').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    rejected_orders = Order.objects.filter(status='rejected').count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:10]
    
    context = {
        'page_title': 'PANEL - QHUN22',
        'total_orders': total_orders,
        'monthly_revenue': monthly_revenue,
        'total_revenue': total_revenue,
        'new_users': new_users,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'delivered_orders': delivered_orders,
        'rejected_orders': rejected_orders,
        'recent_orders': recent_orders,
        'current_date': now,
    }
    return render(request, 'qhun22.html', context)


# ==================== PROMOTION MANAGEMENT VIEWS ====================

@user_passes_test(lambda u: u.is_staff)
def admin_promotions(request):
    """
    Render promotion management page in admin panel.
    """
    promotions = SpecialPromotion.objects.select_related('product').order_by('-created_at')
    products = Product.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_title': 'Quản lý khuyến mãi đặc biệt - QHUN22',
        'promotions': promotions,
        'products': products,
        'promotion_count': promotions.count(),
        'max_promotions': 5,
    }
    return render(request, 'admin_promotions.html', context)


@user_passes_test(lambda u: u.is_staff)
def add_promotion(request):
    """
    Add a new special promotion via AJAX.
    """
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            discount_percent = int(data.get('discount_percent', 0))
            
            # Check limit
            if SpecialPromotion.objects.count() >= 5:
                return JsonResponse({
                    'success': False, 
                    'message': 'Chỉ được phép có tối đa 5 khuyến mãi đặc biệt!'
                })
            
            # Check if product already has promotion
            if SpecialPromotion.objects.filter(product_id=product_id).exists():
                return JsonResponse({
                    'success': False, 
                    'message': 'Sản phẩm này đã có trong khuyến mãi!'
                })
            
            promotion = SpecialPromotion.objects.create(
                product_id=product_id,
                discount_percent=discount_percent,
                is_active=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thêm khuyến mãi thành công!',
                'promotion': {
                    'id': promotion.id,
                    'product_name': promotion.product.name,
                    'discount_percent': promotion.discount_percent,
                    'discounted_price': float(promotion.discounted_price)
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'}, status=400)


@user_passes_test(lambda u: u.is_staff)
def delete_promotion(request, promotion_id):
    """
    Delete a special promotion via AJAX.
    """
    if request.method == 'POST':
        try:
            promotion = SpecialPromotion.objects.get(id=promotion_id)
            promotion.delete()
            return JsonResponse({'success': True, 'message': 'Xóa khuyến mãi thành công!'})
        except SpecialPromotion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Khuyến mãi không tồn tại.'}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'}, status=400)


def get_product_details(request, product_id):
    """
    Get product details for the detail modal via AJAX.
    """
    try:
        product = Product.objects.select_related('category').get(id=product_id)
        
        # Check if product has promotion
        promotion = SpecialPromotion.objects.filter(product_id=product_id, is_active=True).first()
        discounted_price = float(promotion.discounted_price) if promotion else None
        discount_percent = promotion.discount_percent if promotion else None
        
        context = {
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'brand': product.brand,
                'price': float(product.price),
                'original_price': float(product.original_price) if product.original_price else None,
                'discounted_price': discounted_price,
                'discount_percent': discount_percent,
                'image': str(product.image),
                'description': product.description,
                'stock': product.stock,
                'is_active': product.is_active,
                'category_name': product.category.name if product.category else '',
            }
        }
        return JsonResponse(context)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Sản phẩm không tồn tại.'}, status=404)


# ==================== PRODUCT MANAGEMENT (CUSTOM ADMIN) ====================

@user_passes_test(lambda u: u.is_staff)
def admin_products(request):
    """
    Trang quản lý sản phẩm trong custom admin (QHUN22).
    Hiển thị danh sách sản phẩm + form/modal để thêm mới.
    Nhóm sản phẩm theo brand với accordion.
    """
    from django.db.models import Count
    
    products = Product.objects.order_by('-created_at')
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    # Group products by brand
    products_by_brand = {}
    products_without_brand = []
    
    for product in products:
        brand = product.brand.strip() if product.brand else ''
        if brand:
            if brand not in products_by_brand:
                products_by_brand[brand] = []
            products_by_brand[brand].append(product)
        else:
            products_without_brand.append(product)
    
    # Sort brands alphabetically
    sorted_brands = sorted(products_by_brand.keys())
    
    # If there are products without brand, add them to a special category
    if products_without_brand:
        products_by_brand['Không có hãng'] = products_without_brand
        sorted_brands.append('Không có hãng')
    
    # Convert to list of tuples for easier template iteration
    brands_with_products = [(brand, products_by_brand[brand]) for brand in sorted_brands]

    context = {
        'page_title': 'Quản lý sản phẩm - QHUN22',
        'brands_with_products': brands_with_products,
        'categories': categories,
        'total_products': products.count(),
    }
    return render(request, 'admin_products.html', context)


@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    """
    Thêm sản phẩm mới từ trang admin custom.
    Hỗ trợ multi-step wizard với tất cả các trường mới.
    """
    if request.method == 'POST':
        import json
        
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price') or '0'
        original_price = request.POST.get('original_price') or None
        brand = request.POST.get('brand', '').strip()
        stock = request.POST.get('stock') or '0'
        category_id = request.POST.get('category_id') or None
        description = request.POST.get('description', '').strip()
        image_file = request.FILES.get('image')
        is_active = request.POST.get('is_active', '1') == '1'
        
        # Variants & Options
        storage_options_json = request.POST.get('storage_options_json', '[]')
        color_options_json = request.POST.get('color_options_json', '[]')
        warranty_options_json = request.POST.get('warranty_options_json', '[]')
        
        # Sales Policies
        free_shipping = request.POST.get('free_shipping') == '1'
        allow_open_box = request.POST.get('allow_open_box') == '1'
        return_policy_30days = request.POST.get('return_policy_30days') == '1'
        
        # Technical Specifications
        specifications_json = request.POST.get('specifications', '{}')

        # Tìm category (nếu chọn)
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None

        try:
            # Parse JSON data
            try:
                storage_options = json.loads(storage_options_json) if storage_options_json else []
            except:
                storage_options = []
            
            try:
                color_options = json.loads(color_options_json) if color_options_json else []
            except:
                color_options = []
            
            try:
                warranty_options = json.loads(warranty_options_json) if warranty_options_json else []
            except:
                warranty_options = []
            
            try:
                specifications = json.loads(specifications_json) if specifications_json else {}
            except:
                specifications = {}

            product = Product(
                name=name,
                price=price,
                brand=brand,
                stock=stock,
                category=category,
                description=description or 'Mô tả đang update...',
                is_active=is_active,
                storage_options=storage_options,
                color_options=color_options,
                warranty_options=warranty_options,
                specifications=specifications,
                free_shipping=free_shipping,
                allow_open_box=allow_open_box,
                return_policy_30days=return_policy_30days,
            )
            if original_price:
                product.original_price = original_price
            if image_file:
                product.image = image_file

            product.save()
            messages.success(request, 'Đã thêm sản phẩm mới thành công!')
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'Lỗi khi thêm sản phẩm: {e}')

        return redirect('admin_products')

    # Nếu không phải POST thì quay lại danh sách
    return redirect('admin_products')


@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    """
    Xóa sản phẩm từ admin custom (dùng POST).
    """
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            messages.success(request, 'Đã xóa sản phẩm thành công!')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại!')
        return redirect('admin_products')

    return redirect('admin_products')


# ==================== COUPON MANAGEMENT VIEWS ====================

@user_passes_test(lambda u: u.is_staff)
def admin_coupons(request):
    """
    Render coupon management page in admin panel.
    """
    from django.utils import timezone
    coupons = Coupon.objects.order_by('-created_at')
    
    # Get active coupons count
    active_coupons = coupons.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).count()
    
    context = {
        'page_title': 'Quản lý mã khuyến mãi - QHUN22',
        'coupons': coupons,
        'active_coupons': active_coupons,
    }
    return render(request, 'admin_coupons.html', context)


@user_passes_test(lambda u: u.is_staff)
def add_coupon(request):
    """
    Add a new coupon via AJAX or form.
    """
    from django.http import JsonResponse
    import json
    from django.utils import timezone
    
    if request.method == 'POST':
        try:
            # Try to parse as JSON (AJAX)
            try:
                data = json.loads(request.body)
                code = data.get('code', '').strip().upper()
                name = data.get('name', '').strip()
                discount_type = data.get('discount_type', 'percent')
                discount_value = float(data.get('discount_value', 0))
                min_order_amount = float(data.get('min_order_amount', 0))
                max_discount = data.get('max_discount') and float(data.get('max_discount'))
                usage_limit = int(data.get('usage_limit', 100))
                start_date = data.get('start_date')
                end_date = data.get('end_date')
            except (json.JSONDecodeError, TypeError):
                # Form submission
                code = request.POST.get('code', '').strip().upper()
                name = request.POST.get('name', '').strip()
                discount_type = request.POST.get('discount_type', 'percent')
                discount_value = float(request.POST.get('discount_value', 0))
                min_order_amount = float(request.POST.get('min_order_amount', 0))
                max_discount = request.POST.get('max_discount') and float(request.POST.get('max_discount'))
                usage_limit = int(request.POST.get('usage_limit', 100))
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
            
            # Validate
            if not code or not name:
                return JsonResponse({'success': False, 'message': 'Vui lòng nhập đầy đủ thông tin!'}, status=400)
            
            if Coupon.objects.filter(code=code).exists():
                return JsonResponse({'success': False, 'message': 'Mã giảm giá này đã tồn tại!'}, status=400)
            
            # Parse dates
            from datetime import datetime
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M') if start_date else timezone.now()
                end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M') if end_date else timezone.now() + timezone.timedelta(days=30)
            except ValueError:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else timezone.now()
                    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else timezone.now() + timezone.timedelta(days=30)
                except:
                    start_date = timezone.now()
                    end_date = timezone.now() + timezone.timedelta(days=30)
            
            # Create coupon
            coupon = Coupon.objects.create(
                code=code,
                name=name,
                discount_type=discount_type,
                discount_value=discount_value,
                min_order_amount=min_order_amount,
                max_discount=max_discount,
                usage_limit=usage_limit,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            
            # Check if AJAX or form
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thêm mã giảm giá thành công!',
                    'coupon': {
                        'id': coupon.id,
                        'code': coupon.code,
                        'name': coupon.name,
                        'discount_type': coupon.discount_type,
                        'discount_value': float(coupon.discount_value),
                    }
                })
            else:
                messages.success(request, 'Thêm mã giảm giá thành công!')
                return redirect('admin_coupons')
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)}, status=400)
            messages.error(request, f'Lỗi: {e}')
            return redirect('admin_coupons')
    
    return redirect('admin_coupons')


@user_passes_test(lambda u: u.is_staff)
def delete_coupon(request, coupon_id):
    """
    Delete a coupon via AJAX.
    """
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.delete()
            return JsonResponse({'success': True, 'message': 'Xóa mã giảm giá thành công!'})
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Mã giảm giá không tồn tại.'}, status=404)
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'}, status=400)

