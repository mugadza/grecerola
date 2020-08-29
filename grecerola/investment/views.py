from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from decimal import Decimal

from .forms import InvestmentCreateForm

from grecerola.campaign.models import Campaign
from grecerola.investment.models import Investment
from grecerola.wallet.models import Transaction


@login_required
def investment_create(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        form = InvestmentCreateForm(request.POST)

        if form.is_valid():
            form.cleaned_data['invester'] = request.user
            form.cleaned_data['campaign'] = campaign
            form.cleaned_data['campaign_id'] = pk
            form.cleaned_data['status'] = False
            form.cleaned_data['total_investment_amount'] = campaign.share_price_amount * form.cleaned_data['shares']
            
            investment = Investment.objects.create(
                campaign=campaign,
                invester=request.user,
                status=False,
                total_investment_amount=campaign.share_price_amount * form.cleaned_data['shares'],
                shares=form.cleaned_data['shares']
            )
            
            transaction_fee_percentage = Decimal(0.035)
            transaction_fee = investment.total_investment_amount*transaction_fee_percentage

            transaction = Transaction.objects.create(
                reference=campaign.name,
                transaction_fee_amount=transaction_fee,
                transaction_amount=-1*(investment.total_investment_amount + transaction_fee),
                wallet=request.user.bank.wallet,
                is_pending=False
            ) 

            # clear the cart
            return render(request, 'investment/investment_success.html', {'investment': investment})
    else:
        form = InvestmentCreateForm()
    
    return render(request, 'investment/investment_create.html', {'campaign': campaign, 'investment_form': form})

