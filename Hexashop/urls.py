"""Hexashop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shopping import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    #------------------------------------------------------------------
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('products/',views.products,name='products'),
    path('single_product/',views.single_product,name='single_product'),
    #-----------------------------------------------------------------
    path('signup/',views.signup,name='signup'),
    path('buyer/',views.buyer_signup,name='buyer_signup'),
    path('seller/',views.seller_signup,name='seller_signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('changepass',views.user_change_password,name='changepass'),
    path('profile/',views.user_profile,name='profile'),
    path('addproduct/',views.add_product,name='addproduct'),
    # path('userdetail/<int:id>',views.user_detail,name='userdetail'),
    # path('addProduct/', views.addProduct,name='addProduct'),
    path('cart/',views.cart,name='cart'),
    # path('paginator/',views.post_list,name='postlist'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('removetocart/',views.removetocart,name='removetocart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('success/', views.PaymentSuccessView, name='success'),
    path('failed/', views.PaymentFailedView, name='failed'),
    path('search/',views.search,name='search'),
   

    path('api/checkout-session/<id>/', views.create_checkout_session, name='api_checkout_session'),





] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
