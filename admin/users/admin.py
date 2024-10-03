from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AppUsers

# Define a custom user admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'is_staff', 'is_active', 'user_type', 'is_banned')
    list_filter = ('is_staff', 'is_active', 'user_type', 'is_banned')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'username', 'user_type', 'app')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'user_type', 'app', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register the AppUsers model
@admin.register(AppUsers)
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'app', 'source', 'created_at', 'updated_at')
    list_filter = ('source', 'app')
    search_fields = ('name',)
    ordering = ('created_at',)
