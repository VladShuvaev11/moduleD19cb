from datetime import datetime
from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Comment, Author, Category
from .forms import PostForm, CommentForm
from django.core.mail import send_mail




class PostList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CommentCreate(LoginRequiredMixin, CreateView):
    model = CommentForm
    fields = ['text']
    template_name = 'comment_create.html'
    success_url = reverse_lazy('post_detail')

    def get(self, request, *args, **kwargs):
        return render(request, 'comment_create.html', {})


class Comments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_accept.html'
    context_object_name = 'comments'


class CommentFilter(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_filter.html'
    context_object_name = 'comments'


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('comment_list')




@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей'
    return render(request, 'subscribe.html', {'category':category, 'message':message})