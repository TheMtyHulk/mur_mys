from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from .forms import LoginForm, UserRegistrationForm, ProfileUpdateForm
from helpers.decorators import anonymousRequired,contactLoginRequired
from django.contrib.auth.decorators import login_required
from .models import Suspects, Investigators,Murders,Interviews
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
#index view
#index view
def index(request):
    murders = Murders.objects.all()  
    return render(request, 'main/index.html', {'murders': murders}) 


#login view
@anonymousRequired
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # if user.is_superuser:
                #     # User is active, log them in
                #     login(request, user)
                #     return redirect('admin:index')
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

#register user view
@anonymousRequired
def registerView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

#logout view
@login_required
def logoutView(request):    
    logout(request)
    return redirect('index')  # Redirect to the index page after logout

def solveMurderView(request,murder_id):
    murder = get_object_or_404(Murders, id=murder_id)
    return render(request,'main/solve_murder.html',{'murder':murder})

def suspectsProfileView(request,murder_id):
    murder=get_object_or_404(Murders,id=murder_id)
    return render(request,'main/suspect_profile.html',{'murder':murder})

def investigatorsProfileView(request,murder_id):
    murder=get_object_or_404(Murders,id=murder_id)
    return render(request,'main/investigator_profile.html',{'murder':murder})
    

def interviewsView(request, murder_id):
    murder = get_object_or_404(Murders, id=murder_id)
    interviews = murder.interviews.all()
    
    context = {
        'murder': murder,
        'interviews': interviews,
    }
    return render(request, 'main/interviews.html', context)



# API views to get suspects and investigators AJAX
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def get_suspects_by_murder(request):
    murder_id = request.GET.get('murder_id')
    if murder_id:
        suspects_list = Suspects.objects.filter(murders_id=murder_id).values('id', 'name')
        return JsonResponse({'suspects': list(suspects_list)})
    return JsonResponse({'suspects': []})

@staff_member_required
def get_investigators_by_murder(request):
    murder_id = request.GET.get('murder_id')
    if murder_id:
        investigators_list = Investigators.objects.filter(murders_id=murder_id).values('id', 'name')
        return JsonResponse({'investigators': list(investigators_list)})
    return JsonResponse({'investigators': []})


def get_suspect_details(request, suspect_id):
    try:
        suspect = get_object_or_404(Suspects, id=suspect_id)
        data = {
            'success': True,
            'suspect': {
                'name': suspect.name,
                'age': suspect.age,
                'description': suspect.description,
                'image': suspect.image.url if suspect.image else None
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def get_investigator_details(request, investigator_id):
    try:
        investigator = get_object_or_404(Investigators, id=investigator_id)
        data = {
            'success': True,
            'investigator': {
                'name': investigator.name,
                'age': investigator.age,
                'description': investigator.description,
                'image': investigator.image.url if investigator.image else None
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_interview_details(request, interview_id):
    try:
        interview = get_object_or_404(Interviews, id=interview_id)
        data = {
            'success': True,
            'interview': {
                'id': interview.id,
                'suspect_name': interview.suspects.name,
                'investigator_name': interview.investigators.name,
                'date': interview.date.strftime('%B %d, %Y at %I:%M %p') if interview.date else 'Unknown',
                'content': interview.content,
                'image': interview.image.url if interview.image else None
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    




@login_required
def profileView(request):
    edit_mode = request.GET.get('edit') == 'true'
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            edit_mode = True  # Stay in edit mode if there are errors
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'edit_mode': edit_mode,
    }
    return render(request, 'main/profile.html', context)

