from account.models import Avatar, User

from django.contrib import admin


class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (AvatarInline, )

    list_display = [
        'email',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_filter = [
        'is_staff',
        'is_active',
        'date_joined',
    ]
    readonly_fields = [
        'email',
        'date_joined',
        'last_login',
        'username',
        'password',
    ]
    search_fields = [
        'email',
    ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('rate.full_edit') \
                or request.user.is_superuser:
            return ()
        return super().get_readonly_fields(request, obj=obj)


class AvatarAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', ]
    list_display = ('id', 'user')
    list_select_related = ['user']  # Avatar.objects.select_related('user')


admin.site.register(User, UserAdmin)
admin.site.register(Avatar, AvatarAdmin)
