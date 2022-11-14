from pathlib import Path
from django.urls import path
from django.views.generic import TemplateView
from .views import (
    part_detail_view,
    part_create_view,
    part_edit_view,
    assembly_groups_view,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "contact/", TemplateView.as_view(template_name="contact.html"), name="contact"
    ),
    path("part/<int:part_id>/", part_detail_view, name="part_detail"),
    path("parts/", assembly_groups_view, name="assembly_groups"),
    path(
        "parts/group/<int:assembly_group_id>",
        TemplateView.as_view(template_name="contact.html"),
        name="assemby_group_parts",
    ),
    path("part/new/", part_create_view, name="part_create"),
    path("part/<int:part_id>/edit/", part_edit_view, name="part_edit"),
]
