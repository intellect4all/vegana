from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.HomePage, name='home' ),
    path("cart/", views.Cart, name="cart"),
    path('products/<slug>/', views.ProductDetails, name='product' ),
    path("category/<category>/", views.CategoryView, name="category"),
    path('add_to_cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('add_to_wishlist/<slug>/', views.add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path('add_wish_to_cart/<slug>/', views.add_wishlist_to_cart, name="add-wish-to-cart"),
]