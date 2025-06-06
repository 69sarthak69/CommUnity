from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    attendee_count = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.id')
    attendees = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'date',
            'location',
            'category',
            'latitude',  
            'longitude',
            'created_by',
            'attendees',
            'attendee_count',
            'created_at'
        ]

    def get_attendee_count(self, obj):
        return obj.attendees.count()
