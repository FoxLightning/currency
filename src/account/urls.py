from account import views

from django.urls import path


app_name = 'account'

urlpatterns = [
    path('myprofile/', views.MyProfile.as_view(), name='myprofile'),
]
