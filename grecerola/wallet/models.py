import uuid
from django.db import models
from django.conf import settings

from . import WalletActionType, WalletReferenceType

from django_prices.models import MoneyField


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

    @classmethod
    def create(cls, user, created_by, asof):
        with transaction.atomic():
            wallet = cls.objects.create(
                user=user,
                created=asof,
                modified=asof,
                balance=0,
            )
            wallet_action = WalletAction.create(
                user=created_by,
                wallet=wallet,
                type=WalletReferenceType.WALLET_ACTION_TYPE_CREATED,
                delta=0,
                asof=asof,
                result_balance=wallet.balance
            )
        return wallet, wallet_action

    @classmethod
    def deposit(
        cls,
        uid,
        deposited_by,
        amount,
        asof,
        comment=None,
    ):

        assert amount > 0
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(uid=uid)
            
            wallet.balance += amount
            wallet.modified = asof
            wallet.save(update_fields=[
                'balance',
                'modified',
            ])
            action = WalletAction.create(
                user=deposited_by,
                wallet=wallet,
                wallet_action_type=WalletAction.WALLET_ACTION_TYPE_DEPOSITED,
                delta=amount,
                asof=asof,
                result_balance=wallet.balance
            )
        return wallet, action

    @classmethod
    def withdraw(
        cls,
        uid,
        withdrawn_by,
        amount,
        asof,
        comment=None,
    ):
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(uid=uid)
            
            if wallet.balance - amount < 0:
                raise errors.ValidationError(
                    {'withdraw': 'insufficient funds.',}
                )
            wallet.balance -= amount
            wallet.modified = asof
            wallet.save(update_fields=[
                'balance',
                'modified',
            ])
            action = WalletAction.create(
                user=withdrawn_by,
                wallet=wallet,
                wallet_action_type=WalletAction.WALLET_ACTION_TYPE_WITHDRAWN,
                delta=-amount,
                asof=asof,
                result_balance=wallet.balance
            )
        return wallet, action
    

    def __str__(self):
        return "%s - %s" % (self.uid, self.balance)

    __hash__ = models.Model.__hash__


class WalletAction(models.Model):
    class Meta:
        verbose_name = 'Wallet Action'
        verbose_name_plural = 'Wallet Actions'

    uid = models.CharField(unique=True, editable=False, max_length=30, verbose_name='Public identifier')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, help_text='User who performed the action.',)
    created = models.DateTimeField(blank=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    wallet_action_type = models.CharField(
        max_length=30, choices=WalletActionType.CHOICES
    )

    delta = models.IntegerField(help_text='balance delta.')
    reference = models.TextField(blank=True)
    
    reference_type = models.CharField(
        max_length=30, default=WalletReferenceType.REFERENCE_TYPE_NONE, choices=WalletReferenceType.CHOICES
    )

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

    @classmethod
    def create(
        cls,
        user,
        wallet,
        wallet_action_type,
        delta,
        asof,
        reference=None,
        reference_type=None,
        comment=None,
    ):
        assert asof is not None

        if (wallet_action_type == WalletActionType.WALLET_ACTION_TYPE_DEPOSITED and  reference_type is None):
            raise errors.ValidationError(
                {'reference_type': 'required for deposit.',}
            )

        if reference_type is None:
            reference_type = WalletReferenceType.REFERENCE_TYPE_NONE

        if reference is None:
            reference = ''

        if comment is None:
            comment = ''

        uid = generate_user_friendly_id()

        return cls.objects.create(
            uid=uid,
            created=asof,
            user=user,
            account=account,
            wallet_action_type=wallet_action_type,
            delta=delta,
            reference=reference,
            reference_type=reference_type,
            comment=comment,
            result_balance=account.balance,
        )

    def __str__(self):
        return "%s - %s - %s" % (self.uid, self.wallet, self.wallet_action_type)

    __hash__ = models.Model.__hash__