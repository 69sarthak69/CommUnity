from django.contrib import admin
from .models import DonationCampaign, Donation, InKindDonation
from django.contrib.admin import ModelAdmin

@admin.register(DonationCampaign)
class DonationCampaignAdmin(ModelAdmin):
    list_display = ['title', 'location', 'target_amount', 'current_amount', 'created_by', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['title', 'description', 'location']
    autocomplete_fields = ['created_by', 'help_request', 'group']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by', 'help_request', 'group')

@admin.register(Donation)
class DonationAdmin(ModelAdmin):
    list_display = ['user', 'campaign', 'amount', 'status', 'anonymous', 'created_at']
    list_filter = ['status', 'anonymous', 'created_at']
    search_fields = ['campaign__title', 'user__username']
    autocomplete_fields = ['user', 'campaign']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'campaign')

@admin.register(InKindDonation)
class InKindDonationAdmin(ModelAdmin):
    list_display = ['item', 'user', 'location', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    actions = ['approve_donations', 'reject_donations']
    search_fields = ['item', 'description', 'location']
    autocomplete_fields = ['user']
    date_hierarchy = 'created_at'
    def approve_donations(self, request, queryset):
        queryset.update(status='approved')
    approve_donations.short_description = "Mark selected donations as approved"

    def reject_donations(self, request, queryset):
        queryset.update(status='rejected')
    reject_donations.short_description = "Mark selected donations as rejected"


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')