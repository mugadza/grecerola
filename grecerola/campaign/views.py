from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Campaign, CampaignType

def campaign_home(request):
    return render(request, "campaign/index.html", {"campaigns": Campaign.objects.all()})


class CampaignListView(ListView):
    model = Campaign
    context_object_name = 'campaigns'
    template_name = 'campaign/explore.html'

    def get_queryset(self):
        self.campaign_type = get_object_or_404(CampaignType, name=self.kwargs['typename'])
        return Campaign.objects.filter(campaign_type=self.campaign_type)
