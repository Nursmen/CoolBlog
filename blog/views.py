from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    post = Post.objects.exclude(published_date = None).\
        filter(published_date__lte=timezone.now()).\
        order_by('-published_date')
    
    for i in post:
        if len(i.text) > 300:
            i.text = i.text[:300] + '...'
    # means published_date <= timezone.now() (меньше или равно)
    # just QuerySet 

    return render(request, 'blog/post_list.html', {'posts':post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = create_post(form, request)
            return redirect('post_detail', pk=post.pk)
        return redirect('posts')
    else:
        form = PostForm
    return render(request, 'blog/edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = create_post(form, request)
            return redirect('post_detail', pk=post.pk)
        return redirect('posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'form':form, 'post':post})

def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts')

def create_post(form, request):
    post = form.save(commit=False)
    # form.save() <- сохранит всё за нас.
    # form.save(commit=false) - не сохранит, ведь нам нужно добавить автора.
    # Зато вернет пост почти готовый как QuerySet

    post.author = request.user
    post.publish()
    return post