from rest_framework import serializers
from .models import HelpRequest, HelpResponse
from .models import CommunityPost
from django.contrib.auth import get_user_model

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class HelpRequestSerializer(serializers.ModelSerializer):
    """Serializer for Help Requests"""

    created_by = serializers.ReadOnlyField(source='created_by.id')
    applicants = UserMiniSerializer(read_only=True, many=True)


    class Meta:
        model = HelpRequest
        fields = '__all__'
        

    # def create(self, validated_data):
    #     """Ensure request user is set as the creator"""
    #     validated_data['user'] = self.context['request'].user
    #     return super().create(validated_data)


class HelpResponseSerializer(serializers.ModelSerializer):
    """Serializer for Help Responses"""

    class Meta:
        model = HelpResponse
        fields = ['id', 'request', 'helper', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'helper', 'created_at']

    def create(self, validated_data):
        """Ensure helper is set to the current user"""
        validated_data['helper'] = self.context['request'].user
        return super().create(validated_data)


# Add to serializers.py

class CommunityPostSerializer(serializers.ModelSerializer):
    """Serializer for community posts"""

    class Meta:
        model = CommunityPost
        fields = ['id', 'user', 'title', 'content', 'category', 'image', 'location', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



# class NotificationSerializer(serializers.ModelSerializer):
#     """Serializer for Notifications"""

#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'request', 'message', 'is_read', 'created_at']
#         read_only_fields = ['id', 'user', 'created_at']
