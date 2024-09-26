from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'user_type', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'user_type')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'user_type')}),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)
