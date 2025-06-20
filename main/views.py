from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, ProfileUpdateForm
from .models import Suspects, Investigators, Murders, Interviews
from helpers.decorators import anonymousRequired
import json


def index(request):
    murders = Murders.objects.all()  
    return render(request, 'main/index.html', {'murders': murders}) 


@anonymousRequired
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                try:
                    user = User.objects.get(username=username)
                    if user and user.check_password(password) and not user.is_active:
                        return render(request, 'main/account_inactive.html', {'user': user})
                    form.add_error('password', 'Invalid username or password')
                except User.DoesNotExist:
                    form.add_error('password', 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})



@anonymousRequired
def registerView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't login yet
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it's verified
            user.save()
            
            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your Mur_Mys account'
            message = render_to_string('main/email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.profile.email_token,
            })
            
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.content_subtype = "html"
            email.send()
            
            return render(request, 'main/register_confirm.html')
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

from django.contrib.auth.models import User

@anonymousRequired
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Check if the token matches
        if str(user.profile.email_token) == str(token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            user.profile.save()
            
            # Auto-login the user
            login(request, user)
            return render(request, 'main/activation_success.html')
        else:
            return render(request, 'main/activation_invalid.html')
            
    except Exception as e:
        user = None
        return render(request, 'main/activation_invalid.html')
    


@require_POST
def resend_activation(request):
    data = json.loads(request.body)
    username = data.get('username')
    
    try:
        user = User.objects.get(username=username)
        
        if user.is_active:
            return JsonResponse({
                'success': False,
                'message': 'Account is already active'
            })
            
        # Send verification email
        current_site = get_current_site(request)
        mail_subject = 'Activate your Mur_Mys account'
        message = render_to_string('main/email/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user.profile.email_token,
        })
        
        email = EmailMessage(
            mail_subject, message, to=[user.email]
        )
        email.content_subtype = "html"
        email.send()
        
        return JsonResponse({
            'success': True,
            'message': 'Activation email sent successfully!'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Failed to send email'
        }, status=500)
    


def passwordReset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    messages.error(request, 'Account is not active. Please activate your account first.')
                    return render(request, 'main/password_reset.html', {'form': form})
                
                # Generate token
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                
                # Create email
                mail_subject = 'Reset your Mur_Mys password'
                message = render_to_string('main/email/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
                
                email = EmailMessage(
                    mail_subject, message, to=[user.email]
                )
                email.content_subtype = "html"
                email.send()
                
                return render(request, 'main/password_reset_sent.html')
            except User.DoesNotExist:
                # Don't reveal that the user doesn't exist
                return render(request, 'main/password_reset_sent.html')
    else:
        form = PasswordResetForm()
    
    return render(request, 'main/password_reset.html', {'form': form})

def passwordResetConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(f"Found user: {user.username}")  # Debug info
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        print(f"Error finding user: {str(e)}")  # Debug info
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                try:
                    # Save the form which updates the password
                    user = form.save()
                    
                    # Force user to re-authenticate with new password
                    from django.contrib.auth import update_session_auth_hash
                    update_session_auth_hash(request, user)
                    
                    # messages.success(request, 'Your password has been successfully reset. You can now log in with your new password.')
                    # print("Password successfully reset")  # Debug info
                    # return redirect('login')
                    return render(request, 'main/password_reset_success.html')
                except Exception as e:
                    print(f"Error saving password: {str(e)}")  # Debug info
                    form.add_error(request, f"An error occurred: {str(e)}")
            else:
                print(f"Form errors: {form.errors}")  # Debug info
        else:
            form = SetPasswordForm(user)
        return render(request, 'main/password_reset_confirm.html', {'form': form})
    else:
        print("Invalid token or user is None")  # Debug info
        return render(request, 'main/password_reset_invalid.html')