from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),

    path('rate/', include('rate.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # path('accounts/', include('allauth.urls'))

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__', include(debug_toolbar.urls)))


handler404 = 'rate.views.handler404'
handler500 = 'rate.views.handler500'
