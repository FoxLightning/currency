from . import views

from rest_framework.routers import DefaultRouter


app_name = 'api-rate'

router = DefaultRouter()
router.register('rates', views.RateAPIViewSet, basename='rate')

urlpatterns = router.urls
