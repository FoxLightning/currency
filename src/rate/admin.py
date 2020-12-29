from django.contrib import admin

from .models import Rate


class RateAdmin(admin.ModelAdmin):
    list_display = [
        'currency',
        'source',
        'buy',
        'sale',
        'created',
    ]
    list_filter = [
        'currency',
        'source',
        'created',
    ]
    readonly_fields = [
        'source',
        'currency',
    ]
    actions = None

    def hes_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('rate.full_edit') \
                or request.user.is_superuser:
            return ()
        return super().get_readonly_fields(request, obj=obj)


admin.site.register(Rate, RateAdmin)
