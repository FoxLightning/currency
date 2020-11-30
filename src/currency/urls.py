from account.views import SignUp

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),

    path('rate/', include('rate.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # authentification app
    # path('accounts/', include('allauth.urls'))

    # django password recovery
    path('account/', include('django.contrib.auth.urls')),
    path('account/signup', SignUp.as_view(), name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__', include(debug_toolbar.urls)))

handler404 = 'rate.views.handler404'
handler500 = 'rate.views.handler500'
