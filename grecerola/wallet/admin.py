from django.contrib import admin
from .models import (
    Wallet,
    Bank,
    Transaction
)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "bank",
    )

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "account_name",
        "account_holder_name",
        "bank_name",
        "account_number",
        "account_type",
        "bank_branch_code",
        "user",
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "reference",
        "transaction_amount",
        "is_pending",
        "confirmed_at",
    )
