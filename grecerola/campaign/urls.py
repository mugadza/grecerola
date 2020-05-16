from django.urls import path
from .views import (
    campaign_home,
    CampaignListView
)

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('explore/<typename>', CampaignListView.as_view()),
]