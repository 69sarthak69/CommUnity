# donations/urls.py
from django.urls import path
from .views import InitiateKhaltiPaymentView, VerifyKhaltiPaymentView

urlpatterns = [
    path('initiate/', InitiateKhaltiPaymentView.as_view(), name='initiate-donation'),
    path('verify/', VerifyKhaltiPaymentView.as_view(), name='verify-donation'),
]