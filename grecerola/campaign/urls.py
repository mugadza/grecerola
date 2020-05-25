from django.urls import path
from .views import (
    campaign_home,
    campaign_management,
    CampaignListView,
    contact_us
)

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('management/', campaign_management, name='campaign-management'),
    path('explore/<typename>', CampaignListView.as_view()),
    path('contact/', contact_us, name='contact-us' )
]