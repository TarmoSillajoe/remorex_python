from django.shortcuts import render, get_object_or_404
from .models import Part


def part_detail_view(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    return render(request, "yard/part_detail.html", {"part": part})
