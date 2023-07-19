from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    NewUserForm, ProfileForm, ModeratorRequestForm, StudentForm
    )
from .tasks import (
    welcome_user, send_welcome_sms
) 
from django.contrib.auth.views import (
    LoginView
)
from accounts.models import (
     Moderator, Designer, Admin, Profile, ModeratorRequest, Network
)
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.views.generic.edit import (
    UpdateView, DeleteView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()


def check_admin(user):
    if user.is_superuser:
        return True
    else:
        return False

def register(request, utype=None):
    if request.user.is_authenticated:
        logout(request)
    new_user = None
    form = None
    if request.method == 'POST':
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            if utype == 'admin':
                new_user.is_superuser = True
                new_user.is_staff = True
                
            elif utype == 'moderator':              
                new_user.is_staff = True
                new_user.is_moderator = True
            elif utype == 'premium_member':
                new_user.is_premium = True
            elif utype == 'designer':
                new_user.is_designer = True
            elif utype == 'student':
                new_user.is_student = True
            else:
                 new_user.is_member = True
            new_user.save()
            welcome_user(new_user.id)
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = NewUserForm()
    return render(request, 'accounts/forms/registration_form.html', {
            'form': form,
            'utype': utype
        })

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_student = True
            student.is_active = True
            student.save()
            return redirect('accounts:login')
    else:
        form = StudentForm()
    return render(request, 'accounts/forms/registration_form.html', {
        'form': form,
        'form_type': 'Student'
    })


class SignInView(LoginView):
    template_name = 'accounts/forms/signin_form.html'
    
    
@login_required(login_url='/accounts/login')
def profile(request):

    if request.user.is_superuser:
        return redirect('dashboard:index')
    elif request.user.is_moderator:
        return redirect('moderator:index')
    elif request.user.is_designer:
        return redirect('studio:index')
    elif request.user.is_student:
        return redirect('student:index')
    else:
        return redirect('home:index')

@login_required(login_url='/accounts/login')
def create_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            form.save_m2m()
            return redirect('accounts:user_profile', user.pk)
    else: 
        form= ProfileForm()
    return render(request, 'accounts/forms/profile_form.html', {
        'user': user,
        'form': form,
        'form_title': 'Complete your profile'
    })


@login_required(login_url='/accounts/login')
def update_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('accounts:user_profile', user.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/forms/update_form.html', {
        'form': form
    })

@login_required(login_url='/accounts/login')
def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'accounts/user_profile.html',{
            'user': user,
            'profile': profile,
            'user_id': str(user.id)

        })


class UpdateUserView(UpdateView):
    model = User
    fields = ['username', 'email', 'tel_no', 'instagram_handle']
    template_name = 'accounts/forms/update_form.html'
    success_url = '/accounts/profile/'


@login_required(login_url='/accounts/login')
@user_passes_test(check_admin)
def  new_moderator(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ModeratorRequestForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save()
            return redirect('accounts:profile')
    else:
        form = ModeratorRequestForm()
    return render(request, 'accounts/forms/moderator_request_form.html',{
        'form': form,
        'user': user,
        'form_title': 'Request To Moderate'
    })
    

def moderator_request_detail(request, moderator_request_pk):
    moderator_request = get_object_or_404(ModeratorRequest, pk=moderator_request_pk)
    return render(request, 'accounts/moderator_request_detail.html', {
        'moderator_request': moderator_request
    })


@login_required(login_url='/accounts/login')
def connect_with_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    current_user = request.user
    current_user.connected_users.add(user)
    current_user.save()
    return redirect('accounts:user_profile', user.pk)


@login_required(login_url='/accounts/login')
def activate_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.activated = True
    user.save()
    return redirect('accounts:user_profile', user.pk)


@login_required(login_url='/accounts/login')
def deactivate_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.activated = False
    user.save()
    return redirect('accounts:user_profile', user.pk)


@login_required(login_url='/accounts/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render('accounts/change_password_done.html')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/registration/password_change_form.html', {
        'form': form,
        'form_title': "Change Your Password"
    })

