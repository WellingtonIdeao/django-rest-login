from django.urls import path
from .views import loginView

app_name = 'api'

urlpatterns = [
    path('login/', loginView, name='login'),
]
