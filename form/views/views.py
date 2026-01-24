from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django import forms

from ..models import *
from ..forms import *


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def invite_new(request):
    if request.method == "POST":
        form = UserInviteCreateForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.created_by = request.user
            invite.save()

            invite_url = request.build_absolute_uri(
                reverse("accept_invite", args=[invite.token])
            )

            return render(request, "users/invite_created.html", {
                "invite": invite,
                "invite_url": invite_url,
                "nav_section": "patients", 
            })
    else:
        form = UserInviteCreateForm()

    return render(request, "users/invite_new.html", {
        "form": form,
        "nav_section": "patients",
    })

def accept_invite(request, token):
    invite = get_object_or_404(UserInvite, token=token)

    if invite.used:
        return render(request, "users/invite_used.html", {
            "invite": invite,
        })

    if request.method == "POST":
        form = InviteRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                username=username,
                email=invite.email,
                password=password,
            )
            if invite.make_staff:
                user.is_staff = True
            user.save()

            invite.mark_used()

            login(request, user)
            return redirect("dashboard")  # или другая главная страница
    else:
        form = InviteRegisterForm()

    return render(request, "users/accept_invite.html", {
        "form": form,
        "invite": invite,
    })

@login_required()
def dashboard(request):
    reports = Report.objects.order_by('created_date')
    patients = Patient.objects.order_by('full_name')
    return render(request, 'form/dash.html',{
        "reports":reports,
        "patients":patients,
        "nav_section": "dashboard",})





        
        


