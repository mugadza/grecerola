from django.urls import path
from .views import (
    campaign_home,
    campaign_detail,
    explore,
    campaign_management,
    investment_detail,
    contact_us,
    faq,
    about,
)

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('management/', campaign_management, name='campaign-management'),
    path('explore/', explore, name='explore'),
    path('explore/<slug:campaign_type_slug>/', explore, name='explore-by-campaign-type'),
    path('contact/', contact_us, name='contact-us'),
    path('faq/', faq, name='faq'),
    path('about/', about, name='about'),
    path('explore/<int:pk>/<slug:slug>/', campaign_detail, name='campaign-detail'),
    path('invest=?<int:pk>/', investment_detail, name='investment-detail')
]
