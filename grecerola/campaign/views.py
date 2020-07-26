from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Campaign, CampaignType

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

def campaign_detail(request, pk):
    campaign = get_object_or_404 (Campaign, pk=pk)
    return render(request,"campaign/campaign_detail.html", {'campaign':campaign, 'images': campaign.images.all()})

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
