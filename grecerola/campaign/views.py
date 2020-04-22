from django.shortcuts import render

def campaign_home(request):
    return render(request, "campaign/index.html")
