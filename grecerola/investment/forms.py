from django import forms
from .models import Investment


class InvestmentCreateForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['shares']
