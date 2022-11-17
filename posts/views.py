from django.shortcuts import render
from .models import Post


def homepage(request):
    latest_posts = Post.objects.order_by("-timestamp")[0:3]
    context = {"latest_posts": latest_posts}
    return render(request, "home.html", context)
