from django.urls import path

from . import views


app_name = 'rate'

urlpatterns = [
    path('list/', views.RateListView.as_view(), name='list'),
    path('contactus/list', views.ContactUsListView.as_view(), name='contactuslist'),
    path('contactus/create', views.CreateContactUsView.as_view(), name='contactuscreate'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('showrating/', views.FeedbackShowView.as_view(), name='showrating')
]
