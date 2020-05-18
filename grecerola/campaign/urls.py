from django.urls import path
from .views import (
    campaign_home,
    campaign_management,
    CampaignListView
)

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('management/', campaign_management, name='campaign-management'),
    path('explore/<typename>', CampaignListView.as_view()),
]