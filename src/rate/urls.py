from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'rate'


urlpatterns = [
    path('list/', views.RateListView.as_view(), name='list'),
    path('contactus/list', views.ContactUsListView.as_view(), name='contactuslist'),
    path('contactus/create', views.CreateContactUsView.as_view(), name='contactuscreate'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('showrating/', views.FeedbackShowView.as_view(), name='showrating'),
    path('error/', TemplateView.as_view(template_name='error/error_voted.html'), name='error'),
    path('sublist/', views.SubListView.as_view(), name='sublist'),
    path('dellsub/<int:pk>', views.subdel, name='dellsub'),
    path('addsubscription/', views.addsub, name='addsubscription'),
    path('latestrates/', views.LatestRates.as_view(), name='latestrates'),
    path('downloadlatestrates/', views.DownloadLatestRates.as_view(), name='downloadlatestrates'),
    path('downloadallrates/', views.DownloadAllRates.as_view(), name='downloadallrates'),
    path('deleterate/<int:pk>', views.DeleteRate.as_view(), name='deleterate'),
    path('updaterate/<int:pk>', views.UpdateRate.as_view(), name='updaterate'),
    # TODO create reate

]
