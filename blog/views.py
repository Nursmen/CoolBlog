from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone

# Create your views here.
def post_list(request):
    post = Post.objects.exclude(published_date = None).\
        filter(published_date__lte=timezone.now()).\
        order_by('published_date')
    # means published_date <= timezone.now() (меньше или равно)
    # just QuerySet 

    return render(request, 'blog/post_list.html', {'posts':post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})