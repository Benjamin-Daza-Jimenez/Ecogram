from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import  HttpResponse, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from network.models import Post
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
import os

from .forms import UserLoginForm, UserSignUpForm, UserChangeForm
from .models import UserProfile, EditProfile
from django.views.generic import View

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Sesión iniciada')
            return redirect('comienzo')
        else:
            messages.warning(request, 'Email o contraseña inválida')
            return redirect('comienzo')

    messages.error(request, 'Formulario inválido')
    return redirect('comienzo')

def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get('email')
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(email=email, first_name=first_name, last_name=last_name, password=make_password(password), is_active = True)
            login(request, user)
            return redirect('comienzo')
        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})

def logout_view(request):
    logout(request)
    return redirect('comienzo')

@login_required(login_url='Innombrable:comienzo')
def profile_view(request):
    return render(request, 'users/perfil.html')


def user_detail(request, slug):
    user = get_object_or_404(get_user_model(), slug=slug)
    
    followers = user.followers.all()

    if len(followers) == 0:
        is_following = False
    
    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    return render(request, 'users/detalles_usuario.html', {'user_detail': user, 'is_following':is_following,})

class AddFollower(LoginRequiredMixin, View):
    def post(self,request, slug, *args, **kwargs):
        perfil = UserProfile.objects.get(slug=slug)
        perfil.followers.add(request.user)
        messages.add_message(self.request, messages.SUCCESS, 'Usuario seguido')
        return redirect('users:user_detail', slug=slug)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self,request, slug, *args, **kwargs):
        perfil = UserProfile.objects.get(slug=slug)
        perfil.followers.remove(request.user)
        messages.add_message(self.request, messages.SUCCESS, 'Dejaste de seguir al usuario')
        return redirect('users:user_detail', slug=slug)

def changes(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.FILES.get('profile_pic', None) != None:
                try:
                    os.remove(request.user.profile_pic.url)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                request.user.profile_pic = request.FILES['profile_pic']
                request.user.save()
            return redirect('/PerfilPropio', id=request.user.id)
    else:
        form = EditProfile(instance=request.user)
        return render(request, 'users/perfil.html', {'form': form})
