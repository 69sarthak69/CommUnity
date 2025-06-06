from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



# Registering the CustomUser model with the admin interface using a custom admin class
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'location', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'area_of_interest')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'location')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'location', 'area_of_interest')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    
    # Fields to display when adding a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'location', 'area_of_interest', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
