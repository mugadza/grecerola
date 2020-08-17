from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Campaign, CampaignType
from . import CampaignStatus

def campaign_home(request):
    return render(request, "campaign/index.html")

def campaign_management(request):
    return render(request, "campaign/management.html")

def contact_us(request):
    return render(request,"campaign/contact.html")

def faq(request):
    return render(request,"campaign/faq.html")

def about(request):
    return  render(request,"campaign/about.html")

def explore(request, campaign_type_slug=None):
    campaign_type = None
    campaign_types = CampaignType.objects.all()
    campaigns = Campaign.objects.filter(Q(is_published=True), Q(status=CampaignStatus.UNFULFILLED)) 

    if campaign_type_slug:
        campaign_type = get_object_or_404(CampaignType, slug=campaign_type_slug)
        campaigns = campaigns.filter(campaign_type=campaign_type)

    return render(request, "campaign/explore.html", {
        'campaign_type': campaign_type,
        'campaign_types': campaign_types,
        'campaigns': campaigns
    })

def campaign_detail(request, pk, slug):
    campaign = get_object_or_404 (Campaign, pk=pk, slug=slug, is_published=True)
    return render(request,"campaign/campaign_detail.html", {'campaign':campaign, 'images': campaign.images.all()})

@login_required
def investment_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    return render(request,"campaign/investment_detail.html", {'campaign':campaign})


class CampaignListView(ListView):
    model = Campaign
    context_object_name = 'campaigns'
    template_name = 'campaign/explore.html'

    def get_queryset(self):
        campains = []
        if 'typename' in self.kwargs:
            self.campaign_type = get_object_or_404(CampaignType, name=self.kwargs['typename'])
            campaigns = Campaign.objects.filter(campaign_type=self.campaign_type)
        else:
            campaigns = Campaign.objects.all()

        return campaigns
