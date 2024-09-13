from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django import views
from .views import Addlike, AddCommentLike, CommentReplyView, CommentDeleteView


app_name = 'network'

urlpatterns = [
    path('Principal/<slug:slug>/like', Addlike.as_view(), name='like'),
    path('Principal/<slug:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment-delete"),
    path('Principal/<slug:post_pk>/comment/<int:slug>/like', AddCommentLike.as_view(), name="comment-like"),
    path('Principal/<slug:post_pk>/comment/<int:slug>/reply',CommentReplyView.as_view(), name='comment-reply'),
]  