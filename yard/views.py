from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Part, AssemblyGroup
from .forms import PartForm
from django.http import HttpResponse, HttpResponseRedirect


def assembly_groups_view(request):
    assembly_groups = AssemblyGroup.objects.all()
    return render(
        request, "yard/assembly_groups.html", {"assembly_groups": assembly_groups}
    )


def parts_for_the_assembly_group(request, assembly_group_id):
    the_assembly_group = AssemblyGroup.objects.get(pk=assembly_group_id)
    parts_for = the_assembly_group.part_set.all()
    return render(request, "yard/parts_for_assemblygroup.html", {"parts": parts_for})


def part_detail_view(request, part_id):
    user = request.user
    part = get_object_or_404(Part, id=part_id)
    return render(request, "yard/part_detail.html", {"part": part, "user": user})


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
def part_delete_view(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    context = {"part": part}
    if request.method == "POST":
        part.delete()
        return HttpResponseRedirect("/")
    return render(request, "yard/part_delete.html", context)


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
