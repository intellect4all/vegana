
import requests, json
from django.contrib.auth import login
from django.http import request, response
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
# from django.template import context
from django.views.generic import View, DetailView
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
import string, uuid
from django.conf import settings

# Create your views here.


def HomePage(request):
    all_categories = Category.objects.all()
    trending_products = Product.objects.filter(tags__slug="trending-products")
    best_selling_products = Product.objects.filter(tags__slug="best-selling-products", is_on_sale=True)
    new_products = Product.objects.filter(is_on_sale=True)[:9]
    context = {
        'trending_products': trending_products,
        'best_selling_products': best_selling_products,
        'new_products': new_products,
        'all_categories': all_categories,
    }
    return render(request, 'store/index.html', context)


def ProductDetails(request, slug):
    all_categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    
    def get_related():
        product = get_object_or_404(Product, slug=slug, is_on_sale=True)
        if product.category:
            cat_related = Product.objects.filter(category__slug=product.category.slug, is_on_sale=True).exclude(slug=product.slug)
        if product.tags.all().exists():
            tag_related = Product.objects.filter(tags__name=product.tags.all()[0], is_on_sale=True).exclude(slug=product.slug)
        if product.tags.all().exists() and product.category:
            # tag_related = Product.objects.filter(tags__name=product.tags.all()[0], is_on_sale=True).exclude(slug=product.slug)
            # cat_related = Product.objects.filter(category__slug=product.category.slug, is_on_sale=True).exclude(slug=product.slug)
            related = cat_related.union(tag_related)
            return related.reverse()
        elif product.tags.all().exists() and not product.category:
            related = tag_related
            return related
        elif product.category and not product.tags.all().exists():
            related = tag_related
            return related
        else:
            return None
    new_arrivals = Product.objects.filter(is_on_sale=True)[:9]
    print(get_related())
    context = {
        'new_arrivals': new_arrivals,
        'product': product,
        'all_categories': all_categories,
        'related': get_related()
    }
    return render(request, 'store/product-details.html', context)

class Contact(View):
    def get(self, *args, **kwargs):
        all_categories = Category.objects.all()
        context = {
            'all_categories': all_categories
        }
        return render(self.request, 'store/contact.html', context)
    
    def post(self, *args, **kwargs):
        pass

def CategoryView(request, category):
    all_categories = Category.objects.all()
    cat_products = Product.objects.filter(
        category__name=category.title(), is_on_sale=True)
    cat = Category.objects.get(name=category.title())
    if cat_products.exists():
        context = {
            'cat_products': cat_products,
            'all_categories': all_categories,
            'cat' : cat
        }
        return render(request, 'store/category.html', context)
    else:
        messages.info(request, "The category is empty or does not exist")
        return redirect('store:home')

def shop(request):
    all_categories = Category.objects.all()
    cat_products = Product.objects.filter(is_on_sale=True)
    if cat_products.exists():
        context = {
            'cat_products': cat_products,
            'all_categories': all_categories,
        }
        return render(request, 'store/shop.html', context)
    else:
        messages.info(request, "The category is empty or does not exist")
        return redirect('store:home')

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = product.name + " already exists in your cart. The quantity has been incremented."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            order.items.add(order_item)
            msg = product.name + " has been added to your cart."
            messages.info(request, msg)
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        msg = product.name + " has been added to your cart."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def checkout(request):
    all_categories = get_list_or_404(Category)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    billing_form = BillingAddForm()
    shipping_form = ShippingAddForm()
    detail_form = OrderDetailsForm()
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.filter(ordered=False)
        if order_items.exists():    
            cart_total = order.get_order_total()
            order_total = order.get_final_price()
            
            context = {
                'order_items': order_items,
                'all_categories': all_categories,
                'cart_total': cart_total,
                'order_total': order_total,
                'billing_form': billing_form,
                'shipping_form': shipping_form,
                'detail_form': detail_form,
                'order' : order
            }
            return render(request, 'store/checkout.html', context)
        else:
            messages.info(request, "You do not have any item in your cart, please continue shopping.")
            return redirect('store:home')
    else:
        messages.info(request, "You do not have an active order, please continue shopping.")
        return redirect('store:home')


class add_billing_address(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = BillingAddForm(self.request.POST)
        print(form)
        if form.is_valid():
            print("cool")
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            company = form.cleaned_data.get('company')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            post_code = form.cleaned_data.get('post_code')
            state =form.cleaned_data.get('state')
            phone = form.cleaned_data.get('phone')
            same_as_shipping = form.cleaned_data.get('same_as_shipping')
            billing_add = BillingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                same_as_shipping=same_as_shipping
                )
            billing_add.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            order = order_qs[0]
            order.billing = billing_add
            order.save()
            if billing_add.same_as_shipping:
                shipping_add = ShippingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                )
                shipping_add.save()
                order.shipping = shipping_add
                order.save()
                messages.info(self.request, "Billing Address successfully added and set as shipping address.")
                return redirect('store:checkout')
            messages.info(self.request, "Billing Address successfully added.")
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

class add_shipping_address(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = ShippingAddForm(self.request.POST)
        if form.is_valid():
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            company = form.cleaned_data.get('company')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            post_code = form.cleaned_data.get('post_code')
            state =form.cleaned_data.get('state')
            phone = form.cleaned_data.get('phone')
            same_as_billing = form.cleaned_data.get('same_as_billing')
            shipping_add = ShippingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                same_as_billing=same_as_billing
                )
            shipping_add.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            shipping= ShippingAdd.objects.filter(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,)[0]
            order = order_qs[0]
            order.shipping = shipping
            order.save()
            messages.info(self.request, "Shipping Address successfully added to the order.")
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

class add_order_details(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = OrderDetailsForm(self.request.POST)
        if form.is_valid():
            quote = form.cleaned_data.get('quote')
            user = self.request.user
            payment = form.cleaned_data.get('payment')
            agree = form.cleaned_data.get('agree')
            details = OrderDetail.objects.create(user=user, quote=quote, payment=payment, agree=agree)
            details.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            order = order_qs[0]
            order.details = details
            order.save()

            def get_id():
                rand = uuid.uuid1()
                return rand
            
            rand = get_id()
            order2 = Order.objects.filter(ref=rand)
            if not order2.exists():
                order.ref = rand
                order.save()
                if details.payment == 'PS':
                    return redirect('store:paystack')
                elif details.payment == 'PP':
                    return redirect('store:wishlist')

                return redirect('store:checkout')
            else:
                c = order2.exists()
                while c == True:
                    r = get_id()
                    order1 = Order.objects.filter(r=rand)
                    c = order1.exists()
                order.ref=r
                order.save()
                if details.payment == 'PS':
                    return redirect('store:paystack')
                elif details.payment == 'PP':
                    return redirect('store:wishlist')
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

@login_required
def Cart(request):
    all_categories = Category.objects.all()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        cart_total = order.get_order_total()
        context = {
            'order_items': order_items,
            'all_categories': all_categories,
            'cart_total': cart_total,
        }
        return render(request, 'store/cartlist.html', context)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store:home')

@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    wish_item, created = WishItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(product__slug=slug).exists():
            messages.info(request, f'{wish_item.product.name} already exists in your wishlist.')
            return redirect('store:home')
        else:
            wishlist.items.add(wish_item)
            messages.info(request, f'{wish_item.product.name} has been added to your wishlist.')
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        wishlist = Wishlist.objects.create(user=request.user, ordered_date=ordered_date)
        wishlist.items.add(wish_item)
        messages.info(request, f'{wish_item.product.name} has been added to your wishlist.')
        return redirect('store:home')

@login_required
def wishlist(request):
    all_categories = Category.objects.all()
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        wishlist_items = wishlist.items.all()
        context = {
            'wishlist': wishlist_items,
            'all_categories': all_categories,
        }
        return render(request, 'store/wishlist.html', context)
    else:
        messages.info(request, "You do not have a wishlist. Kindly add a product to your wishlist")
        return redirect('store:home')

@login_required
def add_wishlist_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    wish_item, created = WishItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            wishlist = wishlist_qs[0]
            wishlist.items.remove(wish_item)
            msg = product.name + " already exists in your cart. The quantity has been incremented and removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
        else:
            order.items.add(order_item)
            wishlist = wishlist_qs[0]
            wishlist.items.remove(wish_item)
            msg = product.name + " has been added to your cart and removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        wishlist = wishlist_qs[0]
        wishlist.items.remove(wish_item)
        msg = product.name + " has been added to your cart and removed from your wishlist."
        messages.info(request, msg)
        return redirect('store:wishlist')

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product, ordered=False)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.delete()
            msg = product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:cart')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

class paystack(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            order = order_qs[0]
            if order.details:
                if order.details.payment == 'PS':
                    print(order.details.payment)
                    order_items = order.items.all()
                    context = {
                        'order':order,
                        'order_items': order_items
                    }
                    return render(self.request, 'store/paystack.html', context)
                else:
                    msg = "Paystack is not your chosen payment option. Please select the proper option here."
                    messages.info(request, msg)
                    return redirect('store:checkout')
            else:
                msg = "Please fill the order details form to proceed to payment"
                messages.info(request, msg)
                return redirect('store:checkout')
        except ObjectDoesNotExist:
            msg = "You do not have an active order, please continue shopping."
            messages.info(request, msg)
            return redirect('store:home')

    def post(self, *args, **kwargs):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        order = order_qs[0]
        ordered_date = timezone.now()
        order.ordered = True
        order.ordered_date = ordered_date
        order.save()
        order.items.update(ordered=True)
        for o in order.items.all():
            o.save()
        msg = f'Your order (Order ref: {order.ref}) has been placed and being processed for delivery.'
        messages.info(self.request, msg)
        return redirect('store:home')
        

@login_required
def remove_single_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product, ordered=False)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity < 1 :
                order_item.delete()
                #order.items.remove(order_item)
            msg = "1 x of " + product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:cart')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def remove_from_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishitem = WishItem.objects.get(user=request.user, product=product)
    wishlist_qs= Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(product__slug=slug):
            wishlist.items.remove(wishitem)
            msg = product.name + " has been removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
        else:
            msg = product.name + " is not in your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
    else:
        msg = "You have not added any item to your wishlist, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def add_single_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = "1 x " + product.name + " added."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            order.items.add(order_item)
            msg = product.name + " has been added to your cart."
            messages.info(request, msg)
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        msg = product.name + " has been added to your cart."
        messages.info(request, msg)
        return redirect('store:home')


# Checkout functionality views
@login_required
def add_single_to_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = "1 x " + product.name + " added."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            order.items.add(order_item)
            msg = product.name + " has been added to your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')


@login_required
def remove_single_from_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product, ordered=False)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity < 1 :
                order_item.delete()
                # order.items.remove(order_item)
                # order_item.quantity = 1
                # order_item.save()
            msg = "1 x of " + product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')


@login_required
def remove_from_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product, ordered=False)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.delete()
            msg = product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

class Account(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=self.request.user)
            customer_form = CustomerInfoForm(instance=customer)
            all_categories = Category.objects.all()
            user = self.request.user
            customer = Customer.objects.get(user=user)
            orders = Order.objects.all()
            total_spending = 0
            for order in orders:
                price = order.get_final_price()
                total_spending += price
            context = {
                'customer': customer,
                'all_categories': all_categories,
                'orders' : orders,
                'customer_form' : customer_form,
                'total_spending' : total_spending
                
            }
            return render(self.request, 'store/account.html', context)
        else:
            msg = "You do not have an account yet. Create an account now."
            messages.info(self.request, msg)
            return redirect('account_login')

    def post(self, *args, **kwargs):
        user, created = Customer.objects.get_or_create(user=self.request.user)
        form = CustomerInfoForm(self.request.POST, self.request.FILES, instance=user, )
        if form.is_valid():
            form.save()
            msg = "Profile updated successfully."
            messages.info(self.request, msg)
            return redirect('store:account')
        else:
            msg = "Something went wrong. Please try updating again."
            messages.info(self.request, msg)
            return redirect('store:account')

class PaystackVerification(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        tx_ref = self.request.GET.get('tx_ref', '')
        transaction_id = self.request.GET.get('transaction_id', '')
        status = self.request.GET.get('status', '')
        orders = Order.objects.all()
        order = orders[0]

        url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
        headers={
            'Content-Type': 'application/json',
            'Authorization': settings.FLUTTER_SECRET_KEY,
        }
        res = requests.get(url, headers=headers)
        
        response = res.json()
        if response['status'] == 'success' and response['data']['tx_ref'] == order.ref:
            order.ordered=True
            order.ordered_date = timezone.now()
            order_items = order.items.all()
            for item in order_items:
                item.ordered=True
                item.save()
            order.save()
            msg = f"Your order with reference: {tx_ref} has been verified and being processed for delivery. Thanks"
            messages.info(self.request, msg)
            return redirect('store:home')
        else:
            msg = f"Your order with reference: {tx_ref} is not yet verified. Please save this Transaction id: {transaction_id} for record process."
            messages.info(self.request, msg)
            return redirect('store:home')
        