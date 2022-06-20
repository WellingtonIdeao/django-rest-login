from django.urls import path
from .views import UserLoginView, UserLogoutView, UserPasswordChangeView,\
    UserPasswordChangeDoneView, logout_view

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('logout/', logout_view, name='logout'),
]
