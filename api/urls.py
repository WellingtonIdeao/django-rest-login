from django.urls import path
from .views import UserLoginView, UserLogoutView, UserPasswordChangeView,\
    UserPasswordChangeDoneView, UserPasswordResetView, UserPasswordResetDoneView,\
    UserPasswordResetConfirmView, UserPasswordResetCompleteView, logout_view

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path(
        'password_change/', UserPasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/', UserPasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path(
        'password_reset/done/', UserPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', UserPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    # path('logout/', logout_view, name='logout'),
]
