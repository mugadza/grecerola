from django.urls import path
from .views import campaign_home
from .views import campaign_explore

urlpatterns = [
    path('', campaign_home, name='campaign-home'),
    path('explore/',campaign_explore,name='campaign-explore')
]