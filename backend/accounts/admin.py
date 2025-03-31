from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'phone_number', 'location', 'area_of_interest'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new user
            obj.set_password(obj.password)  # ✅ Hash the password
        elif 'password' in form.changed_data:  # If changing password
            obj.set_password(obj.password)  # ✅ Hash new password
        obj.save()

admin.site.register(CustomUser, CustomUserAdmin)
