from rest_framework import serializers
from .models import Donation, InKindDonation, DonationCampaign

class DonationCampaignSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DonationCampaign
        fields = ['id', 'title', 'description', 'target_amount', 'current_amount', 'location', 'created_by', 'created_at']
        read_only_fields = ['id', 'current_amount', 'created_by', 'created_at']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'user', 'campaign', 'amount', 'status', 'pidx', 'anonymous', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'pidx', 'created_at']

class InKindDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InKindDonation
        fields = ['id', 'user', 'item', 'description', 'quantity', 'location', 'drop_off_date', 'image', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']