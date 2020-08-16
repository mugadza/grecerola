from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.contrib.sites.models import Site

from ..payfast.forms import PayFastForm

from .models import Transaction


def full_url(link):
    current_site = Site.objects.get_current()
    url = current_site.domain + link
    if not url.startswith('http'):
        url = 'http://' + url
    return url

def success_url():
    return full_url(reverse('success-payfast'))

def cancel_url():
    return full_url(reverse('cancel-payfast'))


@login_required
def investor_wallet(request):
    return render(request, 'wallet/investor_wallet.html', {'bank': request.user.bank})

@login_required
def deposit(request):
    # transaction = get_object_or_404(Transaction, pk=transaction_id)

    # form = PayFastForm(initial={
    #     'amount': transaction.transaction_amount,
    #     'item_name': transaction.wallet.bank.account_reference_id() + " - " + transaction.reference,
    #     'return_url' : success_url(),
    #     'cancel_url' : cancel_url()
    # }, user=transaction.wallet.bank.user)

    return render(request, 'wallet/deposit.html', {'form': 'form', 'bank': request.user.bank})
