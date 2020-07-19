from django.db import models
from django.db.utils import IntegrityError

from model_utils.models import TimeStampedModel

from .exceptions import WalletLocked

class WalletLock(TimeStampedModel):
    wallet = models.OneToOneField('wallet.Wallet', unique=True, on_delete=models.PROTECT)


class Locked(object):
    def __init__(self, wallet):
        self.wallet = wallet
        self.lock = None
        super(Locked, self).__init__()

    def __enter__(self):
        try:
            self.lock = WalletLock.objects.create(wallet=self.wallet)
        except IntegrityError:
            raise WalletLocked('Wallet %s already locked' % self.wallet.pk)
        return self.lock

    def __exit__(self, exc_type, value, trace_back):
        self.lock.delete()
