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
    path('avatar/list/', views.AvatarList.as_view(), name='avatar_list'),
    path('avatar/active/<int:pk>', views.SetActiveAvatar.as_view(), name='avatar_active'),
    path('avatar/delete/<int:pk>', views.DeleteAvatar.as_view(), name='avatar_delete'),
    path('avatar/deleteall/<int:pk>', views.DeleteAllAvatar.as_view(), name='delete_all'),
]
