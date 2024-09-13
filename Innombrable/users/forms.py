from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'loginEmail','type': 'email','class':'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'loginPassword','type': 'password','class': 'form-control'}))


class UserSignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'singupEmail','type': 'email','class': 'form-control'}))

    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'type': 'text','class': 'form-control'}))

    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'type': 'text','class': 'form-control'}))  

    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'singupPassword','type': 'password','class': 'form-control'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password','class': 'form-control'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']

class UserChangeForm(forms.ModelForm):
    profile_pic = forms.ImageField()
