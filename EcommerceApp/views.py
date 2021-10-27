from array import array

from django.db.models import Prefetch
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import DefaultPagination

from .models import *
from .permission import *
from .serializer import *
from .util import *


class CustomerViewset(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(methods=['get'], detail=False, url_path='current-customer')
    def current_customer(self, request):
        try:
            customer = Customer.objects.filter(account=request.user.id).first()
            return Response(status=status.HTTP_202_ACCEPTED, data = self.serializer_class(customer).data)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST,
                            data={'message': 'ban khong co quyen sua doi thong tin nay'})

    def assistant_update(self, request):
        customer = self.get_object()
        reqData = request.data
        if customer.account.id != request.user.id :
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'ban khong co quyen sua doi thong tin nay'})

        else:

            cusData = {}
            accData = {}

            for key in reqData:

                if key in ['username', 'password', 'role', 'is_superuser', 'is_staff']:
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                                    data={'message': 'ban khong co quyen sua doi thong tin nay'})

                if key in ['identity', 'phone']:
                    cusData[key] = reqData.get(key)
                else:
                    accData[key] = reqData.get(key)

            cusSerializer = self.serializer_class(data=cusData, partial=True)
            accSerializer = AccountSerializer(data=accData, partial=True)

            if cusSerializer.is_valid():
                for key in cusData:
                    customer.__setattr__(key, cusData[key])
            if accSerializer.is_valid():
                for key in accData:
                    customer.account.__setattr__(key, accData[key])

                customer.account.save()
                customer.save()

                return Response(status=status.HTTP_202_ACCEPTED, data = self.serializer_class(customer).data)

            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Loi du lieu, xin kiem tra lai"})

    def update(self, request, pk = None):
        return self.assistant_update(request)

    def partial_update(self, request, pk = None):
        return self.assistant_update(request)

class SellerViewset(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    @action(methods=['get'], detail=False, url_path='current-seller')
    def current_seller(self, request):
        try:
            seller = Seller.objects.filter(account=request.user.id).first()
            return Response(status=status.HTTP_202_ACCEPTED, data=self.serializer_class(seller).data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'ban khong co quyen sua doi thong tin nay'})

    def assistant_update(self, request):
        seller = self.get_object()
        reqData = request.data

        if seller.account.id != request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'ban khong co quyen sua doi thong tin nay'})

        else:

            sellerData = {}
            accData = {}

            for key in reqData:

                if key in ['username', 'password', 'role', 'is_superuser', 'is_staff', 'wallet']:
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                                    data={'message': 'ban khong co quyen sua doi thong tin nay'})

                if key in ['identity', 'phone']:
                    sellerData[key] = reqData.get(key)
                else:
                    accData[key] = reqData.get(key)

            sellerSerializer = self.serializer_class(data=sellerData, partial=True)
            accSerializer = AccountSerializer(data=accData, partial=True)

            if sellerSerializer.is_valid():

                for key in sellerData:
                    seller.__setattr__(key, sellerData[key])
            if accSerializer.is_valid():
                for key in accData:
                    seller.account.__setattr__(key, accData[key])

                seller.account.save()
                seller.save()

                return Response(status=status.HTTP_202_ACCEPTED, data=self.serializer_class(seller).data)

            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Loi du lieu, xin kiem tra lai"})

    def update(self, request, pk=None):
        return self.assistant_update(request)

    def partial_update(self, request, pk=None):
        return self.assistant_update(request)

class BrandViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def list(self, request):
        try:
            category = request.query_params.get('category')
            queryset = Brand.objects.filter(category__id = category)
            return Response(status=status.HTTP_200_OK, data = self.serializer_class(queryset,many=True).data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e.__class__.__str__(e)})

class CategoryViewset(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination

class ClassificationViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset =  Classification.objects.all()
    serializers_class = ClassificationNestSerializer

    def list(self, request):
        try:
            category = request.query_params.get('category')
            queryset = Classification.objects.filter(category__id = category)
            return Response(status=status.HTTP_200_OK, data = self.serializers_class(queryset,many=True).data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e.__class__.__str__(e)})

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    pagination_class = DefaultPagination

    def list(self, request, *args, **kwargs):
        title_like = request.query_params.get('title_like')
        new_product = request.query_params.get('new_product')
        most_popular = request.query_params.get('most_popular')
        category = request.query_params.get('category')
        classification = request.query_params.getlist('classification')
        brand = request.query_params.getlist('brand')

        if title_like:
            self.queryset = Product.objects.filter(name__icontains = title_like)
        if category:
            self.queryset = Product.objects.filter(classification__category__id = category)
        if classification and classification != []:
            self.queryset = Product.objects.filter(classification__category__id = category, classification__id__in=classification)
        if brand and brand != []:
            self.queryset = Product.objects.filter(classification__category__id = category, brand__id__in=brand)

        if new_product:
            self.queryset = Product.objects.order_by('-created_date')
        if most_popular:
            self.queryset = Product.objects.order_by('-total_sold_quantity')

        page = self.paginate_queryset(self.queryset)
        return self.get_paginated_response(self.serializer_class(page, many=True,context={'request':request}).data)

    def create(self, request):
        reqData = request.data
        try:
            reqData['seller'] = Seller.objects.filter(account=request.user).first()
            reqData['brand'] = Brand.objects.get(pk = reqData.get('brand'))

            list_pdetail = array(reqData['product_detail'])
            del reqData['product_detail']

            product = Product.objects.create(**reqData)
            product.save()

            for pdetail in list_pdetail:
                pdetail =  ProductDetail(**pdetail, product = product)
                pdetail.save()

            return Response(status=status.HTTP_201_CREATED, data=self.serializer_class(product, context={'request':request}).data)

        except Exception as e:
            product.objects.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e.__class__.__str__(e)})

class EvaluateViewset(viewsets.ModelViewSet):
    queryset = Evaluate.objects.all()
    serializer_class = EvaluateSerializer
    permission_classes = [EvaluatePermission]
    pagination_class = DefaultPagination

    def create(self, request):
        reqData = request.data
        try :
            reqData['product'] = Product.objects.get(pk= reqData.get('product'))
            reqData['customer'] = Customer.objects.filter(account=request.user).first()

            evaluate = Evaluate.objects.create(**reqData)

            evaluate.save()
            return Response(status=status.HTTP_201_CREATED, data=self.serializer_class(evaluate).data)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e.__class__.__str__(e)})

class OrderViewset(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset =  Order.objects.all().prefetch_related(
        Prefetch('orderdetail_set')
    )
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.queryset = Order.objects.filter(customer__account = request.user)
            page = self.paginate_queryset(self.queryset)
            return self.get_paginated_response(self.serializer_class(page, many=True, context={'request': request}).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "không có quyền truy cập"})

    def create(self, request):
        reqData = request.data
        reqOrDetailData = request.data.get('order_detail')
        del reqData['order_detail']
        try:
            reqData['customer'] = Customer.objects.filter(account=request.user).first()
            reqData['seller'] = Seller.objects.get(pk=reqData.get('seller'))
            reqData['status'] = 1

            order = Order.objects.create(**reqData)
            total_price = 0
            for detail in reqOrDetailData:
                product = ProductDetail.objects.get(pk = detail['product'])
                if product.quantity >= detail['quantity']:
                    product.quantity -= detail['quantity']
                    product.sold_quantity += detail['quantity']
                    product.save()
                else:
                    order.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "so luong hang trong kho khong du"})

                order_detail = OrderDetail.objects.create(order= order, product = product, quantity = detail['quantity'])
                order_detail.save()
                total_price += product.price * order_detail.quantity
            order.total_price = total_price
            order.save()
            return Response(status=status.HTTP_201_CREATED, data=self.serializer_class(order).data)

        except Exception as e:
            order.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e.__class__.__str__(e)})

class RevenueViewset(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer

    @action(methods=['POST'], detail=False, url_path='get-revenue')
    def get_revenues(self, request):
        request.user = Account.objects.filter(username=request.data.get('username'),
                                              password=request.data.get('password')).first()
        try:
            if request.user.role == 'SELLER':
                self.queryset = Revenue.objects.filter(order__seller__account=request.user)
            return Response(status=status.HTTP_202_ACCEPTED, data=self.serializer_class(self.queryset,many=True).data)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": e.__class__.__str__(e)})

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN, data={"message":"not working"})

class PayMomoViewset(APIView):

    permission_classes = [PayMomoPermission]

    def post(self, request):
        result = pay_momo(self, request.data)
        if result['code'] == 200:
            return Response(status=status.HTTP_200_OK, data=result['data'])
        if result['code'] == 400:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result['data'])
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=result['data'])

class NotifyMomoViewset(APIView):

    def post(self,request):
        data = notify_momo(self,request.data)
        return Response(status=status.HTTP_200_OK, content_type="application/json;charset=UTF-8", data=data)


class CheckPaymentViewset(APIView):

    permission_classes = [CheckPaymentPermission]

    def post(self,request):
        result = check_payment(self, request.data)
        if result['code'] == 200:
            return Response(status = status.HTTP_200_OK, data= result['data'])
        if result['code'] == 400:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result['data'])
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=result['data'])























