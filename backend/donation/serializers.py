# donations/serializers.py
from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'user', 'amount', 'status', 'pidx', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'pidx', 'created_at']