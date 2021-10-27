from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from rest_framework.serializers import ModelSerializer

class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        account = Account(**validated_data)
        account.set_password(validated_data['password'])
        account.save()

        return account

class CustomerSerializer(ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'identity', 'phone', 'account']

    def create(self, validated_data):
        validated_data['account'] = AccountSerializer.create(self, validated_data['account'])
        customer = Customer(**validated_data)
        customer.save()

        return customer


class SellerSerializer(ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = Seller
        fields = ['id', 'identity', 'phone', 'wallet', 'account']

    def create(self, validated_data):
        validated_data['account']['role'] = 'SELLER'
        validated_data['account']['status'] = 'PENDING'
        validated_data['wallet'] = 0

        validated_data['account'] = AccountSerializer.create(self, validated_data['account'])
        seller = Seller(**validated_data)
        seller.save()

        return seller

class BrandSerializer(ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'picture']

class AccountNestSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'avatar']

class SellerNestSerializer(ModelSerializer):

    account = AccountNestSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'account']

class CustomerNestSerializer(ModelSerializer):

    account = AccountNestSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'account']



class ProductDetailNestSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    def get_name(self, obj):
        return obj.product.name

    class Meta:
        model = ProductDetail
        fields = ['id','main_content','sub_content', 'price', 'quantity', 'sold_quantity', 'image', 'name']

class ClassificationNestSerializer(ModelSerializer):
    category = SerializerMethodField

    def get_category(self,obj):
        return obj.category.id

    class Meta:
        model = Classification
        fields = ['id', 'name','category']

class ProductSerializer(ModelSerializer):
    brand = BrandSerializer(read_only=True)
    seller = SellerNestSerializer(read_only=True)
    productdetail_set = ProductDetailNestSerializer(read_only=True, many=True)
    classification = ClassificationNestSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'brand', 'name', 'description','created_date', 'total_sold_quantity', 'productdetail_set', 'classification', 'main_type', 'sub_type']

class EvaluateSerializer(ModelSerializer):

    product = ProductSerializer(read_only=True)
    customer = CustomerNestSerializer(read_only=True)

    class Meta:
        model = Evaluate
        fields = ['id', 'rate', 'product', 'customer', 'content']

class OrderDetailNestSerializer(ModelSerializer):

    product = ProductDetailNestSerializer(read_only=True)
    class Meta:
        model = OrderDetail
        fields = ['id', 'product','quantity']

class OrderSerializer(ModelSerializer):

    customer = CustomerNestSerializer(read_only=True)
    seller = SellerNestSerializer(read_only=True)
    orderdetail_set = OrderDetailNestSerializer(read_only=True, many=True)
    status = SerializerMethodField()

    def get_status(self,obj):
        return obj.get_status_display()

    class Meta:
        model = Order
        fields= ['id', 'customer', 'seller', 'created_date', 'shipped_date', 'address', 'total_price', 'orderdetail_set', 'status']

class RevenueSerializer(ModelSerializer):

    class Meta:
        model = Revenue
        fields = ['id', 'seller_income', 'ecommerce_income', 'created_date']

class PaymentSerializer(ModelSerializer):

    created_date = SerializerMethodField(read_only=True)

    def get_created_date(self, obj):
        return obj.order.created_date

    class Meta:
        model = Payment
        fields = ['id', 'momo_id', 'status', 'type']

