from account.models import Avatar, User

from django.contrib import admin


class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (AvatarInline, )


class AvatarAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', ]
    list_display = ('id', 'user')
    list_select_related = ['user']  # Avatar.objects.select_related('user')


admin.site.register(User, UserAdmin)
admin.site.register(Avatar, AvatarAdmin)
