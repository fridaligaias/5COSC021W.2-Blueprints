from django.shortcuts import render
from .models import VoteSummary

def results_dashboard(request):
    summaries = VoteSummary.objects.all()
    return render(request, 'results/results_dashboard.html', {'summaries': summaries})
