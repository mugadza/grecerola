from django.urls import path
from .views import investment_create

urlpatterns = [
    path('invest=?<int:pk>/', investment_create, name='investment-create')
]

