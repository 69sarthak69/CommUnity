from django.contrib import admin
from .models import HelpRequest

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "category", "location", "status", "created_at")
    list_filter = ("category", "status", "is_emergency", "created_at")
    search_fields = ("title", "description", "location", "user__email")

    # Read-only fields (Admin cannot modify these)
    readonly_fields = ("created_at",)

    # Order requests by latest created
    ordering = ("-created_at",)
