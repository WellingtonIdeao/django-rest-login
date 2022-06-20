from django.urls import path
from .views import UserLoginView, UserLogoutView, logout_view

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    #path('logout/', logout_view, name='logout'),
]
