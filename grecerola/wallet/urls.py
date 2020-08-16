from django.urls import path
from .views import investor_wallet, deposit

urlpatterns = [
    path('', investor_wallet, name='investor-wallet'),
    path('deposit/', deposit, name='deposit'),
]
