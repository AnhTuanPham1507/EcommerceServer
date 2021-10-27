from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class Account(AbstractUser):
    avatar = models.ImageField(upload_to='static/image/avatar',default=None, blank=True)

    ROLE_ACCOUNT = (
        ('ADMIN', 'admin'),
        ('SELLER', 'seller'),
        ('CUSTOMER', 'customer')
    )
    role = models.CharField(max_length=8, choices=ROLE_ACCOUNT, default='CUSTOMER')

    STATUS_ACCOUNT = {
        ('PENDING', 'pending'),
        ('ACTIVE', 'active'),
        ('BANED', 'banned')
    }
    status = models.CharField(max_length=7, choices=STATUS_ACCOUNT, default='ACTIVE')

    class Meta:
        verbose_name = _("Accounts")
        verbose_name_plural = _("Accounts")

class InfoBase(models.Model):
    identity = models.CharField(max_length=20, unique=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, blank=True)

    class Meta:
        abstract = True

class Customer(InfoBase):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    def __str__(self):
        return self.account.first_name + ' ' + self.account.last_name
class Seller(InfoBase):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    wallet = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.account.first_name + ' ' + self.account.last_name

class Classification(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE, default=None, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    main_type = models.CharField(max_length=255)
    sub_type = models.CharField(max_length=255, default='',blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    total_sold_quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    main_content = models.CharField(max_length=255)
    sub_content = models.CharField(max_length=255,default='',blank=True)
    price = models.BigIntegerField()
    quantity = models.IntegerField()
    sold_quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='static/image/product', default=None, blank=True)

    def __str__(self):
        return self.product.name + ' ' + self.main_content + ' ' + self.sub_content

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='static/image/brand', default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='static/image/category', default=None)

    def __str__(self):
        return self.name

class Evaluate(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    class Rating(models.IntegerChoices):
        diamond = 5, _('rất hài lòng')
        gold = 4, _('hài lòng')
        silver = 3, _('bình thường')
        bronze = 2, _('tệ')
        iron = 1, _('rất tệ')

    rate = models.IntegerField(choices=Rating.choices, default=3)

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField( blank=True, null=True)
    address = models.CharField(max_length=255)
    total_price = models.FloatField()

    class StatusOrder(models.IntegerChoices):
        pending = 1, _('Pending Order')
        delivery = 2, _('delivering Order')
        success = 3, _('Successful Order ')
        failure = 4, _('failure Order')

    status = models.IntegerField(choices=StatusOrder.choices,
                                 default=1)

class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('ProductDetail', on_delete=models.CASCADE)

    quantity = models.IntegerField(validators=[MinValueValidator(1)])

class Payment(models.Model):
    order = models.OneToOneField('Order',on_delete=models.CASCADE)
    momo_id = models.BigIntegerField(default='')

    class StatusPayment(models.IntegerChoices):
        success = 1, _('Successful Payment ')
        refund = 2, _('Refunded Payment')
    status = models.IntegerField(choices=StatusPayment.choices,
                                 default=1)
    TypePayment = (
        ('IN_PERSON', 'pay in person'),
        ('MOMO', 'pay by momo wallet')
    )
    type = models.CharField(max_length=9,choices=TypePayment, default='IN_PERSON')

class Revenue(models.Model):
    order = models.OneToOneField('Order',on_delete=models.CASCADE)
    seller_income = models.FloatField(default=0.0)
    ecommerce_income = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, blank=True)

