from django.shortcuts import render, redirect, get_object_or_404
from .models import Part
from .forms import PartForm


def part_detail_view(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    return render(request, "yard/part_detail.html", {"part": part})


def part_create_view(request):
    if request.method == "POST":
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save()
            return redirect("part_detail", part_id=part.id)
    else:
        form = PartForm()
    return render(request, "yard/part_edit.html", {"form": form})
