import django

from .views import notify_handler

from django.urls import path
from .views import notify_handler

urlpatterns = [
    path('notify/', notify_handler, name='payfast_notify'),
]
