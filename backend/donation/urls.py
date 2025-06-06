# donation/urls.py
from django.urls import path
from .views import DonationCampaignListView, InitiateKhaltiPaymentView, VerifyKhaltiPaymentView, InKindDonationView, MyDonationsView

urlpatterns = [
    path('', DonationCampaignListView.as_view(), name='donation-campaigns'),  
    path('initiate/', InitiateKhaltiPaymentView.as_view(), name='initiate-donation'),
    path('verify/', VerifyKhaltiPaymentView.as_view(), name='verify-donation'),
    path('in-kind-donations/', InKindDonationView.as_view(), name='in-kind-donation'),
    path('my-donations/', MyDonationsView.as_view(), name='my-donations'),
]