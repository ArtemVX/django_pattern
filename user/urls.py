from django.urls import path

from user.views import *

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('logout', logout_user, name='logout'),
    path('password_change', PasswordChange.as_view(), name='password_change'),
    path('password_change/done', PasswordChangeDone.as_view(), name='password_change_done'),
    path('profile/<int:user_pk>', Profile.as_view(), name='profile'),

]
