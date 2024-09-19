from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy
from django.conf import settings
from .forms import PartForm, QueryForm
from .models import AssemblyGroup, Part
import requests
from honeypot.decorators import check_honeypot


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


def verify_turnstile_token(token, remote_ip=None):
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {"secret": settings.TURNSTILE_SECRET_KEY, "response": token}
    if remote_ip:
        data["remoteip"] = remote_ip
    response = requests.post(url, data)
    result = response.json()
    return result.get("success", False)


@check_honeypot(field_name="make")
def query_view(request):
    if request.method == "GET":
        form = QueryForm()
    else:
        form = QueryForm(request.POST)
        turnstile_token = request.POST.get("cf-turnstile-response")
        if not turnstile_token:
            return HttpResponseBadRequest("Turnstile token missing")
        is_valid = verify_turnstile_token(
            turnstile_token, request.META.get("REMOTE_ADDR")
        )
        if not is_valid:
            return HttpResponseBadRequest("Invalid Turnstile verification")
        if form.is_valid():

            subject = form.cleaned_data["subject"]
            body = {
                "phone": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "message": form.cleaned_data["message"],
            }
            text_content = "\n".join(body.values())
            html_content = f"""
                <p>{body.get('phone')}</p>
                <p>{body.get('email')}</p>
                <p>{body.get('message')}</p>
                """
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email="remoreks@remoreks.ee",
                to=["tsillajoe@gmail.com", "remoreks@remoreks.ee"],
                reply_to=["remoreks@remoreks.ee"],
            )
            msg.attach_alternative(html_content, mimetype="text/html")
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("query_success")
    return render(request, "yard/query.html", {"form": form})


def query_success_view(request):
    return HttpResponse(gettext_lazy("query_success"))
