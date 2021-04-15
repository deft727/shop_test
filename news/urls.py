from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns=[

    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page="/"), name='logout'),
    path('contact/',contact,name='contact'),
    path('',IndexView.as_view(),name='home'),
    path('category/<str:slug>/',ProductByCategory.as_view(),name='category'),
    path('product/<str:slug>/',ProductView.as_view(),name='view_prdouct'),
    path('checkout/', MakeOrderView.as_view(), name='checkout'),
    path('add_comment/<int:id>/',AddReview.as_view(),name='add_comment'),
    path('profile/',ProfileView.as_view(),name='profile'),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
]