from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.id')
    members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'category', 'created_by', 'members', 'member_count', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()
