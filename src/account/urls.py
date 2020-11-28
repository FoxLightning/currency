from account import views

from django.urls import path


app_name = 'account'

urlpatterns = [
    path('myprofile/', views.MyProfile.as_view(), name='myprofile'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<str:username>/', views.ActivateUser.as_view(), name='activate'),
    path('password_change/<int:pk>', views.UserPasswordChange.as_view(), name='password_change'),
    path('avatar/create/<int:pk>', views.CreateUserAvatar.as_view(), name='avatar_create'),
    path('avatar/list/<int:pk>', views.AvatarList.as_view(), name='avatar_list'),
]
