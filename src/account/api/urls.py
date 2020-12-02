from . import views

from rest_framework.routers import DefaultRouter


app_name = 'api-account'

router = DefaultRouter()
router.register('avatars', views.AvatarAPIViewSet, basename='account')
router.register('user', views.UserAPIViewSet, basename='user')

urlpatterns = router.urls
