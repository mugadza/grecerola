from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('grecerola.campaign.urls')),
    path('account/', include('grecerola.account.urls')),
    path('admin/', admin.site.urls),
]
