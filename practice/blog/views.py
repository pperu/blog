from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    current_path = request.path
    prev_path = request.GET.get('current_path')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'current_path': current_path, 'prev_path': request.build_absolute_uri(prev_path)})


def post_detail(request, pk):
    current_path = request.path
    prev_path = request.GET.get('current_path')
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'current_path': current_path, 'prev_path': request.build_absolute_uri(prev_path)})


def post_new(request):
    current_path = request.path
    prev_path = request.GET.get('current_path')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:

        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'current_path': current_path, 'prev_path': request.build_absolute_uri(prev_path)})
