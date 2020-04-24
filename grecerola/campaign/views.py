from django.shortcuts import render
from .models import Campaign

def campaign_home(request):
    return render(request, "campaign/index.html", {"campaigns": Campaign.objects.all()})

def campaign_explore(request):
    return render(request,"campaign/explore.html", {"campaigns":Campaign.objects.all()})
