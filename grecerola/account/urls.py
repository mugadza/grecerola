from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, dashboard, investor_wallet

urlpatterns = [
    path('signup/', signup, name='account-signup'),
    path('dashboard/', dashboard, name='account-dashboard'),
    path('investor-wallet/', investor_wallet, name='investor-wallet'),
    path('login', auth_views.LoginView.as_view(template_name='account/login.html'), name="account-login"),
    path('logout', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="account-logout")
]