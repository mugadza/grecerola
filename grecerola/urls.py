from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', include('grecerola.campaign.urls')),
    path('account/', include('grecerola.account.urls')),
    path('account/login', auth_views.LoginView.as_view(template_name='account/login.html'), name="account-login"),
    path('account/logout', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="account-logout"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)