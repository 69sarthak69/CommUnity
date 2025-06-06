from rest_framework import serializers
from .models import HelpRequest, HelpResponse
from .models import CommunityPost, Comment, HelpApplication
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



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'username', 'text', 'parent', 'created_at', 'replies']
        read_only_fields = ['user', 'username', 'created_at', 'id', 'replies']

    def get_replies(self, obj):
        child_comments = obj.replies.all().order_by('created_at')
        return CommentSerializer(child_comments, many=True).data


class CommunityPostSerializer(serializers.ModelSerializer):
    """Serializer for community posts"""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CommunityPost
        fields = ['id', 'user', 'title', 'content', 'category', 'image', 'location', 'created_at', 'comments']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class HelpApplicationSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    status = serializers.CharField() 
    help_request_title = serializers.SerializerMethodField()  

    class Meta:
        model = HelpApplication
        fields = ['id', 'user_name', 'letter', 'created_at', 'status', 'help_request_title']  # <-- INCLUDE status

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.email

    def get_help_request_title(self, obj):
        return obj.help_request.title if obj.help_request else ""


