from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.HomePage, name='home'),
    path("cart/", views.Cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.Contact.as_view(), name="contact"),
    path("shop/", views.shop, name="shop"),
    path('products/<slug>/', views.ProductDetails, name='product'),
    path("category/<category>/", views.CategoryView, name="category"),
    path('account/', views.Account.as_view(), name="account"),

    # cart urls
    path('add_to_cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('remove_from_cart/<slug>/',
         views.remove_from_cart, name="remove-from-cart"),
    path('add_single_to_cart/<slug>/',
         views.add_single_to_cart, name="add-single-to-cart"),
    path('remove_single_from_cart/<slug>/',
         views.remove_single_from_cart, name="remove-single-from-cart"),

    # wishlist urls
    path('add_to_wishlist/<slug>/', views.add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path('add_wish_to_cart/<slug>/',
         views.add_wishlist_to_cart, name="add-wish-to-cart"),
    path('remove_from_wishlist/<slug>/',
         views.remove_from_wishlist, name="remove-from-wishlist"),

    # checkout urls
    path('add_single_to_checkout_cart/<slug>/',
         views.add_single_to_checkout_cart, name="add-single-to-checkout-cart"),
    path('remove_single_from_checkout_cart/<slug>/',
         views.remove_single_from_checkout_cart, name="remove-single-from-checkout-cart"),
    path('remove_from_checkout_cart/<slug>/',
         views.remove_from_checkout_cart, name="remove-from-checkout-cart"),
    path('add_billing_add/', views.add_billing_address.as_view(), name="add-billing"),
    path('add_shipping_add/', views.add_shipping_address.as_view(),
         name="add-shipping"),
    path('add_order_details/', views.add_order_details.as_view(), name="add-details"),

    # Payment urls
    path('checkout/paystack/', views.paystack.as_view(), name="paystack"),
    path('checkout/paystack/verification/', views.PaystackVerification.as_view(), name="paystack-verification"),

]
