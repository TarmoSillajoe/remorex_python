from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Part, AssemblyGroup
from .forms import PartForm


def assembly_groups_view(request):
    assembly_groups = AssemblyGroup.objects.all()
    return render(
        request, "yard/assembly_groups.html", {"assembly_groups": assembly_groups}
    )


def part_detail_view(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    return render(request, "yard/part_detail.html", {"part": part})


@login_required
def part_create_view(request):
    if request.method == "POST":
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save()
            return redirect("part_detail", part_id=part.id)
    else:
        form = PartForm()
    return render(request, "yard/part_edit.html", {"form": form})


@login_required
def part_edit_view(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    if request.method == "POST":
        form = PartForm(request.POST, request.FILES, instance=part)
        if form.is_valid():
            part = form.save()
            return redirect("part_detail", part_id=part.id)
    else:
        form = PartForm(instance=part)
    return render(request, "yard/part_edit.html", {"form": form})
