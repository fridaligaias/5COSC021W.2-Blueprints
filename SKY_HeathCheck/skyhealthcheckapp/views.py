from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Assign user to group after registration
            selected_group = request.POST.get('role')
            try:
                group = Group.objects.get(name=selected_group)  # Check if the group exists
                user.groups.add(group)
            except Group.DoesNotExist:
                # Handle the error gracefully
                return render(request, 'registration/register.html', {
                    'form': form,
                    'error': f"The group '{selected_group}' does not exist. Please contact an admin.",
                })

            login(request, user)  # Automatically log in the user after sign up
            return redirect('dashboard')  # Redirect to dashboard page after successful sign up
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Check user's group/role and redirect to the corresponding dashboard
    if request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    elif request.user.groups.filter(name='Senior Manager').exists():
        return redirect('seniorManager_dashboard')
    elif request.user.groups.filter(name='Department Leader').exists():
        return redirect('departmentLeader_dashboard')
    elif request.user.groups.filter(name='Team Leader').exists():
        return redirect('teamLeader_dashboard')
    else:
        return redirect('engineer_dashboard')
    
@login_required
def admin_dashboard(request):
    return render(request, 'dashboards/admin.html')

@login_required
def departmentLeader_dashboard(request):
    return render(request, 'dashboards/departmentleader.html')

@login_required
def seniorManager_dashboard(request):
    return render(request, 'dashboards/seniormanager.html')

@login_required
def teamLeader_dashboard(request):
    return render(request, 'dashboards/teamleader.html')

@login_required
def engineer_dashboard(request):
    return render(request, 'dashboards/engineer.html')

#summary.html
@login_required
def summary(request):
    # Get the currently logged-in user
    user = request.user

    # Look up the department this user belongs to
    your_dept = user.account.departmentID

    # Fetch all departments except the user's own
    other_departments = Department.objects.exclude(pk=your_dept.pk)

    # Annotate each team with its average votes across all sessions
    teams = Team.objects.annotate(
        green_avg=Avg('session__sessioncard__greenVote'),
        amber_avg=Avg('session__sessioncard__amberVote'),
        red_avg=Avg('session__sessioncard__redVote'),
    )

    # Compute the overall average votes across all Vote records
    overall = Vote.objects.aggregate(
        green_avg=Avg('greenVote'),
        amber_avg=Avg('amberVote'),
        red_avg=Avg('redVote'),
    )

    # Render the summary template, passing in user, departments, teams, and overall stats
    return render(request, 'yourapp/summary.html', {
        'user': user,
        'departments': other_departments,
        'teams': teams,
        'overall': overall,
    })
