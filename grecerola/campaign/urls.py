from django.urls import path
from .views import (
    campaign_home,
    campaign_detail,
    campaign_management,
    CampaignListView,
    investment_detail,
    contact_us,
    faq,
    about,
)

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('management/', campaign_management, name='campaign-management'),
    path('explore/', CampaignListView.as_view(), name='explore'),
    path('explore/<typename>', CampaignListView.as_view()),
    path('contact/', contact_us, name='contact-us'),
    path('faq/', faq, name='faq'),
    path('about/', about, name='about'),
    path('explore/campaign-no=?<int:pk>/', campaign_detail, name='campaign-detail'),
    path('invest-no=?<int:pk>/', investment_detail, name='investment-detail')
]
