from django.urls import path
from .views import signup, dashboard, investor_wallet

urlpatterns = [
    path('signup/', signup, name='account-signup'),
    path('dashboard/', dashboard, name='account-dashboard'),
    path('investor-wallet/', investor_wallet, name='investor-wallet'),
]