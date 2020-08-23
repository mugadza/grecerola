from decimal import Decimal
from django.conf import settings
from ..campaign.models import Campaign


class Investment(object):
    def __init__(self, request):
        """
        Initialize the investment
        """
        self.session = request.session
        investment = self.session.get(settings.INVESTMENT_SESSION_ID)
        if not investment:
            # Save an empty investment session
            investment = self.session[settings.INVESTMENT_SESSION_ID] = {}

        self.investment = investment

    def add(self, campaign, shares=1):
        """
        Add a campaign this investment is related to
        """
        campaign_id = str(campaign.pk)
        self.investment["campaign_id"] = campaign_id
        self.investment["campaign"] = 
        {
            'campaign_id': campaign_id,
            'shares': shares,
            'share_price': str(campaign.share_price_amount),
            'object': campaign
        }
        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it gets saved
        """
        self.session.modified = True

    def clear(self):
        """
        Remove the investment from session
        """
        del self.session[settings.INVESTMENT_SESSION_ID]
        self.save()

    

