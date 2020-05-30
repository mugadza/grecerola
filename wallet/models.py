from django.db import models
from django.conf import settings

from . import WalletActionType


class Wallet(models.Model):
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ("pk",)

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)
    balance = models.PositiveIntegerField()

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    balance_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )

    balance = MoneyField(amount_field="balance_amount", currency_field="currency")

    def __str__(self):
        return "%s - %s" % (self.uid, self.balance)

    __hash__ = models.Model.__hash__


class WalletAction(models.Model):
    class Meta:
        verbose_name = 'Wallet Action'
        verbose_name_plural = 'Wallet Actions'

    uid = models.CharField(unique=True, editable=False, max_length=30, verbose_name='Public identifier')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, help_text=’User who performed the action.’,)
    created = models.DateTimeField(blank=True)
    wallet = models.ForeignKey(Wallet)

    wallet_action_type = models.CharField(
        max_length=30, default=WalletActionType.WALLET_ACTION_TYPE_CREATED, choices=WalletActionType.CHOICES
    )

    delta = models.IntegerField(help_text=‘balance delta.')
    reference = models.TextField(blank=True)
    reference_type = models.CharField(max_length=30, choices=REFERENCE_TYPE_CHOICES, default=REFERENCE_TYPE_NONE)
    comment = models.TextField(blank=True)
    
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    result_balance_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )

    result_balance = MoneyField(amount_field="result_balance_amount", currency_field="currency", help_text='balance after the action.')

    def __str__(self):
        return "%s - %s - %s" % (self.uid, self.wallet, self.wallet_action_type)

    __hash__ = models.Model.__hash__