from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "invester",
        "campaign",
        "status",
        "total_investment_amount",
    )
