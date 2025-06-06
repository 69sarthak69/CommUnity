from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'created_by', 'attendee_count')
    search_fields = ('title', 'location', 'category', 'description')
    list_filter = ('category', 'date')
    readonly_fields = ('created_at', 'attendee_count')

    # Optional: make attendees editable in the admin
    filter_horizontal = ('attendees',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date', 'location', 'category', 'latitude', 'longitude')
        }),
        ('User & Attendance', {
            'fields': ('created_by', 'attendees', 'attendee_count'),
        }),
        ('System Info', {
            'fields': ('created_at',),
        }),
    )
