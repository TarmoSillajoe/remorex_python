from pathlib import Path
from django.urls import path
from django.views.generic import TemplateView
from .views import part_detail_view

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("parts/<int:part_id>/", part_detail_view, name="part_detail"),
]
