from django.db import models
from django.conf import settings
from django.utils.timezone import now

from django_prices.models import MoneyField

from . import InvestmentStatus
from grecerola.campaign.models import Campaign
from grecerola.core.models import TimeStampMixin

class Investment(TimeStampMixin):
    created = models.DateTimeField(default=now, editable=False)

    invester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="investments",
        on_delete=models.SET_NULL,
    )

    campaign = models.ForeignKey(
        Campaign, related_name="investments", on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=32, default=InvestmentStatus.UNFULFILLED, choices=InvestmentStatus.CHOICES
    )

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    total_investment_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )

    total_investment = MoneyField(amount_field="total_investment_amount", currency_field="currency")

    shares = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Investment {self.pk}'
    
    def get_total_investment_cost(self):
        return campaign.share_price_amount * campaign.shares