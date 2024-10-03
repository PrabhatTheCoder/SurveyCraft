from django.contrib import admin
from .models import App

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'isActive', 'created_at', 'updated_at')
    list_filter = ('industry', 'isActive')
    search_fields = ('name', 'industry')
    ordering = ('created_at',)
    prepopulated_fields = {'name': ('description',)}  # Optional: Prepopulate name field based on description

    def get_queryset(self, request):
        """Customize the queryset for admin view."""
        queryset = super().get_queryset(request)
        return queryset.order_by('-created_at')  # Orders by creation date, most recent first
