import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Donation, InKindDonation, DonationCampaign
from .serializers import DonationSerializer, InKindDonationSerializer, DonationCampaignSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class DonationCampaignListView(APIView):
    
    def get(self, request):
        campaigns = DonationCampaign.objects.all()
        in_kind_donations = InKindDonation.objects.all()
        return Response({
            'cash_donations': DonationCampaignSerializer(campaigns, many=True).data,
            'in_kind_donations': InKindDonationSerializer(in_kind_donations, many=True).data
        })

    def post(self, request):
        serializer = DonationCampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InitiateKhaltiPaymentView(APIView):
    def post(self, request):
        data = request.data
        amount = data.get('amount')
        campaign_id = data.get('campaign_id')
        anonymous = data.get('anonymous', False)

        try:
            campaign = DonationCampaign.objects.get(id=campaign_id)
        except DonationCampaign.DoesNotExist:
            return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if campaign.current_amount >= campaign.target_amount:
         return Response({'error': 'This campaign has already reached its goal.'}, status=status.HTTP_400_BAD_REQUEST)

        donation = Donation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            campaign=campaign,
            amount=amount,
            anonymous=anonymous
        )

        payload = {
            "return_url": "http://localhost:5173/donations/success",
            "website_url": "http://localhost:5173",
            "amount": int(float(amount) * 100),  # Khalti expects amount in paisa
            "purchase_order_id": str(donation.id),
            "purchase_order_name": f"Donation to {campaign.title}",
            "customer_info": {
                "name": request.user.get_full_name() if request.user.is_authenticated else "Anonymous",
                "email": request.user.email if request.user.is_authenticated else "anonymous@community.org"
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
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class VerifyKhaltiPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pidx = request.data.get("pidx")
            print("🔍 Verifying pidx:", pidx)

            url = "https://a.khalti.com/api/v2/epayment/lookup/"
            headers = { "Authorization": f"Key {settings.KHALTI_SECRET_KEY}" }
            payload = { "pidx": pidx }

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            print("📡 Khalti response:", data)

            if data.get("status") == "Completed":
                donation = Donation.objects.get(pidx=pidx)
                donation.status = "success"
                donation.campaign.current_amount += donation.amount
                donation.campaign.save()
                donation.save()
                return Response({ "message": "Donation successful!" })

            return Response({
                "message": "Payment not completed.",
                "status": data.get("status")
            }, status=400)

        except Donation.DoesNotExist:
            return Response({ "error": "Donation not found for this pidx" }, status=404)

        except Exception as e:
            import traceback
            print("❌ ERROR during verification:", e)
            traceback.print_exc()
            return Response({ "error": "Something went wrong", "details": str(e) }, status=500)


class InKindDonationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = InKindDonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'In-kind donation submitted successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyDonationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        in_kind_donations = InKindDonation.objects.filter(user=request.user)
        return Response({
            'cash_donations': DonationSerializer(donations, many=True).data,
            'in_kind_donations': InKindDonationSerializer(in_kind_donations, many=True).data
        })