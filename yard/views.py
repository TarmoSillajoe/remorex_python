from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Part, AssemblyGroup
from .forms import PartForm, QueryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.utils import translation
from django import http
from django.conf import settings


def language_switcher(func):
    """
    A decorator that wraps a view in a new function that checks for language-cookie presence in request.
    If a language-change was requested i.e cookie is present, the wrapper
    - activates the requested language,
    - creates the response bye rendering the view, using the new language,
    - sets the language cookie to be used in session,
    - returns the response

    Args:
        request

    Returns:
        django.http.HttpResponse
    """

    def wrapper(request: http.HttpRequest) -> http.HttpResponse:
        request_cookie_lang = request.COOKIES.get(
            settings.LANGUAGE_COOKIE_NAME,
            None,
        )
        if request_cookie_lang is None:
            return func(request)
        translation.activate(request_cookie_lang)
        response = func(request)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request_cookie_lang)
        return response

    return wrapper


@language_switcher
def homeview(request):
    return render(
        request=request,
        template_name="home.html",
    )


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


def part_card_view(request, part_id):
    user = request.user
    part = get_object_or_404(Part, id=part_id)
    return render(request, "yard/part_card.html", {"part": part, "user": user})


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


def query_view(request):
    if request.method == "GET":
        form = QueryForm()
    else:
        form = QueryForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            body = {
                "phone": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(
                    subject,
                    message,
                    from_email="remoreks@remoreks.ee",
                    recipient_list=[
                        "remoreks@remoreks.ee",
                        "tsillajoe@gmail.com",
                    ],
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("query_success")
    return render(request, "yard/query.html", {"form": form})


def query_success_view(request):
    return HttpResponse("Päring saadetud. Täname.")
