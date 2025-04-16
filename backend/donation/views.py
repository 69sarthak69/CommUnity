# donations/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Donation
from .serializers import DonationSerializer

class InitiateKhaltiPaymentView(APIView):
    

    def post(self, request):
        amount = request.data.get('amount')
        donation = Donation.objects.create(user=request.user, amount=amount)

        payload = {
            "return_url": "http://localhost:5173/donations/success",
            "website_url": "http://localhost:5173",
            "amount": int(float(amount) * 100),
            "purchase_order_id": str(donation.id),
            "purchase_order_name": "Community Donation",
            "customer_info": {
                "name": request.user.get_full_name(),
                "email": request.user.email
            }
        }

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        response = requests.post("https://a.khalti.com/api/v2/epayment/initiate/", json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200:
            donation.pidx = data['pidx']
            donation.save()
            return Response({"payment_url": data['payment_url']})
        else:
            return Response(data, status=400)

class VerifyKhaltiPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pidx = request.data.get("pidx")
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        payload = {"pidx": pidx}
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if data.get("status") == "Completed":
            donation = Donation.objects.get(pidx=pidx)
            donation.status = "success"
            donation.save()
            return Response({"message": "Donation successful!"})

        return Response({"message": "Payment not completed.", "status": data.get("status")}, status=400)