from rest_framework import serializers
from .models import Group
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
        # ✅ Make sure creator is included
        member_ids = list(obj.members.values_list('id', flat=True))
        if obj.created_by_id not in member_ids:
            member_ids.append(obj.created_by_id)
        return member_ids
