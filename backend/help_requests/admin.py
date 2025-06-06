from django.contrib import admin
from .models import HelpRequest, HelpResponse, CommunityPost, HelpApplication

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'status', 'is_emergency', 'created_by', 'created_at')
    list_filter = ('category', 'status', 'is_emergency', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
    filter_horizontal = ('applicants',)

@admin.register(HelpResponse)
class HelpResponseAdmin(admin.ModelAdmin):
    list_display = ('request', 'helper', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('request__title', 'helper__email')
    readonly_fields = ('created_at',)

@admin.register(HelpApplication)
class HelpApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'help_request', 'created_at')
    search_fields = ('user__email', 'help_request__title')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['user', 'help_request']

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'location', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'location')
    readonly_fields = ('created_at',)
