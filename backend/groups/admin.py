from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'created_at', 'member_count')
    search_fields = ('name', 'category', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'member_count')

    filter_horizontal = ('members',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category')
        }),
        ('Ownership & Membership', {
            'fields': ('created_by', 'members', 'member_count'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
