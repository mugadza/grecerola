from django.contrib import admin
from .models import Wallet, WalletAction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass
    # list_display = (
    #     "email",
    #     "first_name",
    #     "last_name",
    #     "phone",
    #     "is_active",
    #     "date_joined",
    # )

@admin.register(WalletAction)
class WalletActionAdmin(admin.ModelAdmin):
    pass