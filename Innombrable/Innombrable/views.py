from math import prod
from django.db.models.query import RawQuerySet
from django.forms.fields import ImageField
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
import os
from django.template import Template, Context, context
from django.template.loader import get_template
from network.models import Post, Comentarios
from network.forms import PosteoForm, ComentariosForm
from users.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def diseño(request):

    return render(request,'Diseños de bootstrap.html',)    

def perfil(request):
    return render(request, 'users/perfil.html')

def comienzo(request):
    data = Post.objects.all()
    
    return render(request,'Plantilla_principal.html',{'posts': data})

def fecha(request):

    #clase 6 para usar la fecha en otras páginas
    #clase 7 (al final) para usar dia/mes/año
    fecha=datetime.datetime.now()
    return HttpResponse(fecha)

def temasnuevos(request):
    form=PosteoForm()
    if request.method == 'POST':
        form=PosteoForm(request.POST)

        if form.is_valid():
            print('Válido')
            post = Post()
            post.title = form.cleaned_data['title']
            post.description = form.cleaned_data['description']
            post.image = request.FILES.get('image')
            post.author = request.user
            post.save()
            return redirect('comienzo')
        else:
            print('Inválido')
    return render(request,'Temas Nuevos.html',{'form': form,})

def detallePost(request,slug):
    posteo= get_object_or_404(Post, slug=slug)
    form=ComentariosForm()

    if request.method == 'POST':
        form=ComentariosForm(request.POST)
    
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = posteo
            new_comment.save()

    comments = Comentarios.objects.filter(post=posteo).order_by('-created_on')

    print(posteo)
    return render(request,'Post.html', {'posts':posteo, 'likes':posteo.cantidad_likes(), 'form':form, 'comments':comments})

def menu(request):

    return render(request,'Menu.html',)

def registro(request):

    return render(request,'Registro.html',)

def ayuda(request):

    return render(request,'Ayuda.html',)

@login_required(login_url='Innombrable:comienzo')
def borrar(request, slug):
    post_eliminar = Post.objects.get(identifier=slug)
    post_eliminar.delete()
    return redirect('comienzo')
