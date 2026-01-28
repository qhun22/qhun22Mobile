"""
shopmobile URL Configuration
"""

from django.urls import path, re_path
from store import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Product detail - allow + and other special chars in slug
    re_path(r'^product/(?P<slug>[-a-zA-Z0-9_+]+)/$', views.product_detail, name='product_detail'),
    # Registration
    path('register/', views.register, name='register'),
    # Login page
    path('login/', views.login_page, name='login'),
    # Forgot password (demo)
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    # Profile page
    path('profile/', views.profile, name='profile'),
    # Change password
    path('profile/change-password/', views.change_password, name='change_password'),
    # Feedback
    path('profile/feedback/', views.feedback, name='feedback'),
    # Address operations
    path('profile/add-address/', views.add_address, name='add_address'),
    path('profile/set-default-address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('profile/delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    # Get product details (AJAX)
    path('api/product/<int:product_id>/', views.get_product_details, name='get_product_details'),
    path('api/products/', views.api_products, name='api_products'),
    # Admin
    path('qhun22/', views.admin_dashboard, name='admin_dashboard'),
    # Admin - Promotions
    path('qhun22/promotions/', views.admin_promotions, name='admin_promotions'),
    path('qhun22/promotions/add/', views.add_promotion, name='add_promotion'),
    path('qhun22/promotions/delete/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    # Admin - Products
    path('qhun22/products/', views.admin_products, name='admin_products'),
    path('qhun22/products/add/', views.add_product, name='add_product'),
    path('qhun22/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    # Admin - Coupons
    path('qhun22/coupons/', views.admin_coupons, name='admin_coupons'),
    path('qhun22/coupons/add/', views.add_coupon, name='add_coupon'),
    path('qhun22/coupons/delete/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    # Logout
    path('logout/', views.logout_view, name='logout'),
]
