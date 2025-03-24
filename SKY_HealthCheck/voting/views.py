from django.shortcuts import render, redirect
from .models import Session, Vote
from django.contrib.auth.decorators import login_required

@login_required
def choose_session(request):
    sessions = Session.objects.all()
    return render(request, 'voting/choose_session.html', {'sessions': sessions})

@login_required
def vote(request, session_id):
    session = Session.objects.get(id=session_id)
    # Handle vote logic here
    return render(request, 'voting/vote.html', {'session': session})

@login_required
def vote_summary(request):
    # Aggregate and show summary
    return render(request, 'voting/vote_summary.html')
