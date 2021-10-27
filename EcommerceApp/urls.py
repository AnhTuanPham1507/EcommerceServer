from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('customer', views.CustomerViewset)
router.register('seller', views.SellerViewset)
router.register('product', views.ProductViewset)
router.register('brand', views.BrandViewset)
router.register('category', views.CategoryViewset)
router.register('evaluate', views.EvaluateViewset)
router.register('order', views.OrderViewset)
router.register('revenue', views.RevenueViewset)
router.register('classification', views.ClassificationViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('paymomo/', views.PayMomoViewset.as_view()),
    path('notifymomo/', views.NotifyMomoViewset.as_view()),
    path('checkpayment/', views.CheckPaymentViewset.as_view())
]