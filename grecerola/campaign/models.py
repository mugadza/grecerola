from django.db import models

from django.urls import reverse

from django.conf import settings
from django.utils.timezone import now

from ..core.models import (
    PublishableModel,
    SortableModel,
    TimeStampMixin,
    PublishedQuerySet
)

from ..core.permissions import CampaignPermissions
from ..core.models import Address
from . import CampaignStatus

from versatileimagefield.fields import (
    PPOIField, 
    VersatileImageField,
)

from django_prices.models import MoneyField


class CampaignType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        app_label = "campaign"

    def get_absolute_url(self):
        return reverse('explore-by-campaign-type', args=[self.slug])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )


class Campaign(PublishableModel, TimeStampMixin):
    campaign_type = models.ForeignKey(
        CampaignType, related_name="campaigns", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
   
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    total_investment_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    total_investment = MoneyField(amount_field="total_investment_amount", currency_field="currency")

    investment_raised_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    investment_raised = MoneyField(amount_field="investment_raised_amount", currency_field="currency")

    mininum_allowed_investment_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    mininum_allowed_investment = MoneyField(amount_field="mininum_allowed_investment_amount", currency_field="currency")

    share_price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    share_price = MoneyField(amount_field="share_price_amount", currency_field="currency")


    location = models.OneToOneField(
        Address, related_name="location", on_delete=models.CASCADE, blank=True, null=True
    )

    estimated_investment_date = models.DateTimeField(blank=False)

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="campaigns_owened",
        on_delete=models.SET_NULL,
    )

    investors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="campaigns_invested_in"
    )
    
    status = models.CharField(
        max_length=32, default=CampaignStatus.UNFULFILLED, choices=CampaignStatus.CHOICES
    )

    class Meta:
        app_label = "campaign"
        ordering = ("name", "total_investment_amount",)
        permissions = (
            (CampaignPermissions.MANAGE_CAMPAIGNS.codename, "Manage campaigns."),
        )

    def get_first_image(self):
        images = list(self.images.all())
        return images[0] if images else None

    def get_first_image_url(self):
        images = list(self.images.all())
        return images[0].image.url if images else "/static/assets/img/placeholder800x470.png"

    def get_first_image_alt(self):
        images = list(self.images.all())
        return images[0].alt if images else "placeholder image"

    def get_campaign_progress(self):
        return round(((self.investment_raised_amount)/(self.total_investment_amount))*100, 1)

    def investment_raised_amount_formatted(self):
        return round(self.investment_raised_amount, 0)

    def total_investment_amount_formatted(self):
        return round(self.total_investment_amount, 0)

    def get_absolute_url(self):
        return reverse('campaign-detail', args=[self.id, self.slug])

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )

    def __str__(self) -> str:
        return self.name


class CampaignImage(SortableModel):
    campaign = models.ForeignKey(
        Campaign, related_name="images", on_delete=models.CASCADE
    )
    alt = models.CharField(max_length=128, blank=True)

    image = VersatileImageField('image', upload_to='campaigns', default='placeholder1080x1080.png')
  
    class Meta:
        ordering = ("sort_order",)
        app_label = "campaign"

    def get_ordering_queryset(self):
        return self.campaign.images.all()


class CampaignComment(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    reply = models.ForeignKey(
        'self', related_name="replies", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    campaign = models.ForeignKey(
        Campaign, related_name="campaign_comments", on_delete=models.DO_NOTHING
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="campaign_comments",
        on_delete=models.DO_NOTHING,
    )


class CampaignQuestion(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    reply = models.ForeignKey(
        'self', related_name="replies", on_delete=models.CASCADE
    )
    topic  = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    author_name  = models.CharField(max_length=256, blank=True)
    author_email = models.EmailField(blank=True, default="")

    campaign = models.ForeignKey(
        Campaign, related_name="campaign_questions", on_delete=models.DO_NOTHING
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="campaign_questions",
        on_delete=models.DO_NOTHING,
    )


class CampaignUpdate(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    title  = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)

    campaign = models.ForeignKey(
        Campaign, related_name="campaign_updates", on_delete=models.DO_NOTHING
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="campaign_updates",
        on_delete=models.DO_NOTHING,
    )

