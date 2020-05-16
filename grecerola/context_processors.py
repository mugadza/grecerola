from grecerola.campaign.models import CampaignType

def add_campaign_types_to_context(request):
    return {"campaign_types": CampaignType.objects.all()}
