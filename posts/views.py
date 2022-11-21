from django.shortcuts import render
from .models import Post


def posts_list_view(request):
    latest_posts = Post.objects.order_by("-timestamp")[:10]
    context = {"latest_posts": latest_posts}
    return render(request, "posts/posts_list.html", context)


def post_detail_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)
