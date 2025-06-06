from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from .forms import LoginForm, UserRegistrationForm
from helpers.decorators import anonymousRequired,contactLoginRequired
from django.contrib.auth.decorators import login_required


#index view
def index(request):
    return render(request, 'main/index.html')


#login view
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    # User is active, log them in
                    login(request, user)
                    return redirect('admin:index')
                
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

@contactLoginRequired
def contactView(request):
    pass


# test view
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Suspects, Investigators

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