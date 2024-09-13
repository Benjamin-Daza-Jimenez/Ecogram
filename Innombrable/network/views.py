from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.urls.base import reverse_lazy
from django.views import View
from users.models import UserProfile
from .forms import PosteoForm, ComentariosForm
from .models import Post, Comentarios
from django.http import HttpResponseRedirect, HttpResponse

class Addlike(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        post = Post.objects.get(slug=slug)
        
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
        
        if is_like:
            post.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        comment = Comentarios.objects.get(id=slug)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, slug, *args, **kwargs):
        post= Post.objects.get(slug=post_pk)
        parent_comment = Comentarios.objects.get(id=slug)
        form= ComentariosForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('detalle_post', slug=post_pk)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Comentarios
    template_name = 'comment_delete.html' 
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('detalle_post', kwargs={'slug': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff