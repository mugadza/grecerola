from django.contrib import admin
from .models import (
    Campaign, 
    CampaignComment, 
    CampaignQuestion, 
    CampaignUpdate, 
    CampaignType,
    CampaignImage
)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "campaign_type",
        "slug",
        "total_investment_amount",
        "investment_raised_amount",
        "mininum_allowed_investment_amount",
        "location",
        "estimated_investment_date",
        "posted_by",
        "status",
    )


@admin.register(CampaignType)
class CampaignTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


@admin.register(CampaignComment)
class CampaignCommentAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "description",
        "posted_by",
    )


@admin.register(CampaignQuestion)
class CampaignQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "topic",
        "description",
        "posted_by",
        "author_name",
        "author_email",
        "campaign",
    )

@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "title",
        "description",
        "posted_by",
        "campaign",
    )

@admin.register(CampaignImage)
class CampaignImageAdmin(admin.ModelAdmin):
    list_display = (
        "image",
        "alt",
        "campaign",
    )
