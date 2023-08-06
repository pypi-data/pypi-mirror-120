from django.contrib import admin
from .models import BluelineId


class BluelineIdAdmin(admin.ModelAdmin):
    fields = ['server_url', 'blueline_id', 'blueline_username', 'blueline_password']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['server_url', 'blueline_id', 'blueline_username',
                    'blueline_password']
        return []

    def has_add_permission(self, request):
        if BluelineId.objects.count():
            return False
        return admin.ModelAdmin.has_add_permission(self, request)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(BluelineId, BluelineIdAdmin)
