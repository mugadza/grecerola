from django.db import models
from django.db.models import Sum

from django.conf import settings

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

from model_utils.models import TimeStampedModel, SoftDeletableModel
from model_utils.managers import QueryManager, SoftDeletableManager
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from shortuuidfield import ShortUUIDField
from django_prices.models import MoneyField

from .utils import Locked


class Bank(TimeStampedModel, SoftDeletableModel):
    ACCOUNT_TYPE = Choices(('Savings', _('Savings')), ('Check', _('Check')))

    uuid                    = ShortUUIDField(
                                max_length=8,
                                unique=True,
                                editable=False,
                                verbose_name='Public identifier'
                            )
    account_name            = models.CharField(max_length=256, blank=True)
    account_holder_name     = models.CharField(max_length=256, blank=True)
    bank_name               = models.CharField(max_length=256, blank=True)
    account_number          = models.PositiveIntegerField(
                                unique=True,
                                validators=[MinValueValidator(10000), MaxValueValidator(999999999999)]
                            )
    account_type            = models.CharField(
                                choices=ACCOUNT_TYPE,
                                default=ACCOUNT_TYPE.Savings,
                                max_length=20
                            )
    bank_branch_code        = models.PositiveIntegerField(
                                unique=False,
                                validators=[MinValueValidator(1000), MaxValueValidator(99999999)]
                            )
    user                    = models.OneToOneField(
                                settings.AUTH_USER_MODEL,
                                related_name='bank',
                                unique=True,
                                on_delete=models.PROTECT
                            )

    objects = SoftDeletableManager()
    removed = QueryManager(is_removed=True)

    class Meta:
        ordering = ['account_number']

    @property
    def account_reference_id(self):
        start_index = int(str(self.account_number)[4])
        account_reference = "ACC-" + str(self.account_number) + "-" + self.uuid[start_index:start_index+4]
        return account_reference.upper()

    def __str__(self):
        return '({}) {}'.format(
            self.account_name.upper(),
            self.account_number)


class Wallet(TimeStampedModel, SoftDeletableModel):
    bank = models.OneToOneField(
            'wallet.Bank',
            related_name='wallet',
            unique=True,
            on_delete=models.PROTECT
        )

    objects = SoftDeletableManager()
    removed = QueryManager(is_removed=True)

    class Meta:
        ordering = ['bank']
        permissions = (('can_view_wallet_report', 'Can view wallet report'),)

    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, Decimal, str)):
            raise ValueError('Amount need to be a string, integer or Decimal.')
        return Decimal(amount)

    def register_income(self, amount, reference):
        amount = self.validate_amount(amount)
        if amount <= Decimal('0'):
            raise ValueError(
                'Amount need to be positive number, not %s' % amount
            )

        return self._create_transaction(value, reference)

    def _create_transaction(self, amount, reference):
        return Transaction.objects.create(
            wallet=self,
            reference=reference,
            amount=amount
        )

    def register_expense(self, amount, reference, current_lock=None):
        amount = self.validate_amount(amount)
        if amount >= Decimal('0'):
            raise ValueError(
                'Amount need to be negative number, not %s' % amount
            )

        if current_lock is not None:
            if current_lock.wallet != self:
                raise ValueError('Lock not for this wallet!')

            if self.balance >= amount:
                return self._create_transaction(amount, reference)
            else:
                raise WalletHasInsufficientFunds(
                    'Not insufficient funds to spend %s' % amount
                )

        with Locked(self):
            if self.balance >= amount:
                return self._create_transaction(amount, reference)
            else:
                raise WalletHasInsufficientFunds(
                    'Not insufficient funds to spend %s' % amount
                )

    @property
    def balance(self):
        return self.transactions.aggregate(Sum('transaction_amount'))['transaction_amount__sum']

    def __str__(self):
        return '({})'.format(self.bank)


class Transaction(TimeStampedModel, SoftDeletableModel):
    reference = models.CharField(max_length=255)

    wallet = models.ForeignKey(
                'wallet.Wallet',
                related_name='transactions',
                on_delete=models.PROTECT
            )

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    transaction_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    amount = MoneyField(amount_field="transaction_amount", currency_field="currency")

    is_pending = models.BooleanField(default=False)

    confirmed_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeletableManager()
    removed = QueryManager(is_removed=True)

    class Meta:
        ordering = ['wallet']

    def __str__(self):
        return '({})'.format(self.wallet)


















#
# class Wallet(models.Model):
#     class Meta:
#         verbose_name = 'Wallet'
#         verbose_name_plural = 'Wallets'
#         ordering = ("pk",)
#
#     uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
#
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
#
#     created = models.DateTimeField(blank=True)
#     modified = models.DateTimeField(blank=True)
#     balance = models.PositiveIntegerField()
#
#     currency = models.CharField(
#         max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
#         default=settings.DEFAULT_CURRENCY,
#     )
#
#     balance_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#     )
#
#     balance = MoneyField(amount_field="balance_amount", currency_field="currency")
#
#     @classmethod
#     def create(cls, user, created_by, asof):
#         with transaction.atomic():
#             wallet = cls.objects.create(
#                 user=user,
#                 created=asof,
#                 modified=asof,
#                 balance=0,
#             )
#             wallet_action = WalletAction.create(
#                 user=created_by,
#                 wallet=wallet,
#                 type=WalletReferenceType.WALLET_ACTION_TYPE_CREATED,
#                 delta=0,
#                 asof=asof,
#                 result_balance=wallet.balance
#             )
#         return wallet, wallet_action
#
#     @classmethod
#     def deposit(
#         cls,
#         uid,
#         deposited_by,
#         amount,
#         asof,
#         comment=None,
#     ):
#
#         assert amount > 0
#         with transaction.atomic():
#             wallet = cls.objects.select_for_update().get(uid=uid)
#
#             wallet.balance += amount
#             wallet.modified = asof
#             wallet.save(update_fields=[
#                 'balance',
#                 'modified',
#             ])
#             action = WalletAction.create(
#                 user=deposited_by,
#                 wallet=wallet,
#                 wallet_action_type=WalletAction.WALLET_ACTION_TYPE_DEPOSITED,
#                 delta=amount,
#                 asof=asof,
#                 result_balance=wallet.balance
#             )
#         return wallet, action
#
#     @classmethod
#     def withdraw(
#         cls,
#         uid,
#         withdrawn_by,
#         amount,
#         asof,
#         comment=None,
#     ):
#         with transaction.atomic():
#             wallet = cls.objects.select_for_update().get(uid=uid)
#
#             if wallet.balance - amount < 0:
#                 raise errors.ValidationError(
#                     {'withdraw': 'insufficient funds.',}
#                 )
#             wallet.balance -= amount
#             wallet.modified = asof
#             wallet.save(update_fields=[
#                 'balance',
#                 'modified',
#             ])
#             action = WalletAction.create(
#                 user=withdrawn_by,
#                 wallet=wallet,
#                 wallet_action_type=WalletAction.WALLET_ACTION_TYPE_WITHDRAWN,
#                 delta=-amount,
#                 asof=asof,
#                 result_balance=wallet.balance
#             )
#         return wallet, action
#
#
#     def __str__(self):
#         return "%s - %s" % (self.uid, self.balance)
#
#     __hash__ = models.Model.__hash__
#
#
# class WalletAction(models.Model):
    # class Meta:
    #     verbose_name = 'Wallet Action'
    #     verbose_name_plural = 'Wallet Actions'
    #
    # uid = models.CharField(unique=True, editable=False, max_length=30, verbose_name='Public identifier')
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, help_text='User who performed the action.',)
    # created = models.DateTimeField(blank=True)
    # wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    #
    # wallet_action_type = models.CharField(
    #     max_length=30, choices=WalletActionType.CHOICES
    # )
    #
    # delta = models.IntegerField(help_text='balance delta.')
    # reference = models.TextField(blank=True)
    #
    # reference_type = models.CharField(
    #     max_length=30, default=WalletReferenceType.REFERENCE_TYPE_NONE, choices=WalletReferenceType.CHOICES
    # )
    #
    # comment = models.TextField(blank=True)
    #
    # currency = models.CharField(
    #     max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
    #     default=settings.DEFAULT_CURRENCY,
    # )
    #
    # result_balance_amount = models.DecimalField(
    #     max_digits=settings.DEFAULT_MAX_DIGITS,
    #     decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    # )
    #
    # result_balance = MoneyField(amount_field="result_balance_amount", currency_field="currency", help_text='balance after the action.')
    #
    # @classmethod
    # def create(
    #     cls,
    #     user,
    #     wallet,
    #     wallet_action_type,
    #     delta,
    #     asof,
    #     reference=None,
    #     reference_type=None,
    #     comment=None,
    # ):
    #     assert asof is not None
    #
    #     if (wallet_action_type == WalletActionType.WALLET_ACTION_TYPE_DEPOSITED and  reference_type is None):
    #         raise errors.ValidationError(
    #             {'reference_type': 'required for deposit.',}
    #         )
    #
    #     if reference_type is None:
    #         reference_type = WalletReferenceType.REFERENCE_TYPE_NONE
    #
    #     if reference is None:
    #         reference = ''
    #
    #     if comment is None:
    #         comment = ''
    #
    #     uid = generate_user_friendly_id()
    #
    #     return cls.objects.create(
    #         uid=uid,
    #         created=asof,
    #         user=user,
    #         account=account,
    #         wallet_action_type=wallet_action_type,
    #         delta=delta,
    #         reference=reference,
    #         reference_type=reference_type,
    #         comment=comment,
    #         result_balance=account.balance,
    #     )
    #
    # def __str__(self):
    #     return "%s - %s - %s" % (self.uid, self.wallet, self.wallet_action_type)
    #
    # __hash__ = models.Model.__hash__
