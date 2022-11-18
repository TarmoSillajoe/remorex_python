from pathlib import Path
from django.urls import path
from .views import posts_list_view, post_detail_view

urlpatterns = [
    path("", posts_list_view, name="posts"),
    path("<int:post_id>/", post_detail_view, name="post_detail"),
]
