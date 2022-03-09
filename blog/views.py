from django.shortcuts import render
from .models import Post
from django.utils import timezone

# Create your views here.
def post_list(request):
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # means published_date <= timezone.now() (меньше или равно)
    # just QuerySet 

    return render(request, 'blog/post_list.html', {'posts':post})