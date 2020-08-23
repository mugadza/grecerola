from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvestmentCreateForm

from grecerola.campaign.models import Campaign


@login_required
def investment_create(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        form = InvestmentCreateForm(request.POST)

        if form.is_valid():
            form.cleaned_data['invester'] = request.user
            form.cleaned_data['campaign'] = campaign
            form.cleaned_data['status'] = False
            form.cleaned_data['total_investment_amount'] = campaign.share_price * form.cleaned_data['shares']

            investment = form.save()
            
            # clear the cart
            return render(request, 'investment/investment_create.html', {'investment': investment})
    else:
        form = InvestmentCreateForm()
    
    return render(request, 'investment/investment_create.html', {'campaign': campaign, 'form': form})

