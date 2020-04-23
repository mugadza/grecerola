from django.urls import path
from .views import signup, dashboard

urlpatterns = [
    path('signup/', signup, name='account-signup'),
    path('dashboard/', dashboard, name='account-dashboard'),
]