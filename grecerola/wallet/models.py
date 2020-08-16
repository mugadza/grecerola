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
    reference = models.CharField(max_length=50)

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
