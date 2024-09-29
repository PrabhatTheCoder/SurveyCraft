from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Make sure to import AllQuiz
from quizzes.models import AllQuiz
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'user_type', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'user_type')
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'user_type', 'quizes')}),  # Include quizes field
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'user_type', 'quizes')}),  # Include quizes field
    )
    
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    # Optional: Customizing the form for better user experience
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "quizes":
            kwargs["queryset"] = AllQuiz.objects.all()  # You can customize this queryset if needed
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)

