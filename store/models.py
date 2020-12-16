from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=50)
    class_icon = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)           # add this
        super().save(*args, **kwargs)   

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(max_length=3000, default="This is an auto generated product description.")
    featured_image = models.ImageField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    shipping_fee = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

    #this returns the slug of the product
    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)            # add this
        super().save(*args, **kwargs)                                 # add this

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})

    def get_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.actual_price
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_item_total_price(self):
        return self.quantity * self.product.get_price()    


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing = models.ForeignKey('BillingAdd', on_delete=models.SET_NULL, null=True)
    shipping = models.ForeignKey('ShippingAdd', on_delete=models.SET_NULL, null=True)

    def get_order_total(self):
        all_items = self.items.all()
        total = 0
        if all_items.exists():
            for item in all_items:
                total += item.get_item_total_price()
            return total
        else:
            return total

    def get_shipping_total(self):
        all_items = self.items.all()
        shipping = 0
        for item in all_items:
            shipping += item.product.shipping_fee
        return shipping
    
    def get_final_price(self):
        total = self.get_order_total() + self.get_shipping_total() 
        return total

    class Meta:
        ordering = ['-date_created']


class WishItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(WishItem)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

class BillingAdd(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = PhoneNumberField()
    same_as_shipping = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Billling Address")
        verbose_name_plural = ("Billing Addresses")

    def __str__(self):
        return self.user.username


class ShippingAdd(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = PhoneNumberField()
    same_as_billing = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Shipping Address")
        verbose_name_plural = ("shipping Addresses")

    def __str__(self):
        return self.user.username