from django.shortcuts import render
from .models import Campaign, CampaignType

def campaign_home(request):
    return render(request, "campaign/index.html", {"campaigns": Campaign.objects.all(), "campaign_types": CampaignType.objects.all()})
