from rest_framework import serializers
from .models import Group
from .models import GroupPost, GroupPostReaction, GroupActivity
from django.contrib.auth import get_user_model

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.id')
    members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'category', 'created_by', 'members', 'member_count', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_members(self, obj):
        # Make sure creator is included
        member_ids = list(obj.members.values_list('id', flat=True))
        if obj.created_by_id not in member_ids:
            member_ids.append(obj.created_by_id)
        return member_ids

class GroupPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    like_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    class Meta:
        model = GroupPost
        fields = ['id', 'group', 'author', 'author_name', 'content', 'image', 'created_at', 'like_count', 'user_liked']

    def get_like_count(self, obj):
        return obj.reactions.filter(reaction_type='like').count()

    def get_user_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user and request.user.is_authenticated:
            return obj.reactions.filter(user=request.user, reaction_type='like').exists()
        return False

    
    


class GroupPostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPostReaction
        fields = ['id', 'post', 'user', 'reaction_type', 'created_at']


class GroupActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    post_content = serializers.CharField(source='post.content', read_only=True)
    class Meta:
        model = GroupActivity
        fields = ['id', 'activity_type', 'user', 'user_name', 'group', 'timestamp', 'post', 'post_content', 'extra']
