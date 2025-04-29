from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import Vote 

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

@login_required
def summary_view(request):
    
    # 1. Grab the first name for the header
    firstname = request.user.first_name

    # 2. Fetch all Vote records for this user
    user_votes = Vote.objects.filter(user=request.user).select_related('sessionCardID')

    # 3. Render 'summary.html' with exactly the context your template uses
    return render(request, 'summary.html', {
        'firstname': firstname,
        'user_votes': user_votes,
    })
