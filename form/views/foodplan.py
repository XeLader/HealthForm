from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from ..models import *
from ..forms import *

@login_required
def foodplan_create(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = FoodplanForm(request.POST)
        if form.is_valid():
            foodplan = form.save(commit=False)
            foodplan.patient = patient
            foodplan.author = request.user
            foodplan.create_date = timezone.now()
            foodplan.save()
            return redirect("patient_detail", pk=patient.id)

    else:
        template_id = request.GET.get("template")
        initial_data = {}

        if template_id:
            template = FoodplanTemplate.objects.get(id=template_id)
            initial_data = {
                "title": template.title,
                "subtitle": template.subtitle,
                "text": template.text,
            }

        form = FoodplanForm(initial=initial_data)

    return render(request, "foodplan/foodplan_form.html", {
        "form": form,
        "patient": patient
    })

@login_required
def foodplan_edit(request, foodplan_id):
    foodplan = get_object_or_404(Foodplan, id=foodplan_id)
    if request.method == "POST":
        form = FoodplanForm(request.POST)
        if form.is_valid():
            foodplan = form.save(commit=False)
            foodplan.author = request.user
            foodplan.create_date = timezone.now()
            foodplan.save()
            return redirect("foodplan_detail", pk=foodplan_id)
    else:
        form = FoodplanForm(instance=foodplan)
    return render(request, 'foodplan/foodplan_form.html', {
        'form': form,
        'patient': foodplan.patient
    })

@login_required
def foodplan_detail(request, foodplan_id):
    foodplan = get_object_or_404(Foodplan, id=foodplan_id)
    return render(request, "foodplan/foodplan_detail.html", {
        "foodplan": foodplan,
    })

@login_required
def get_foodplan_template(request, template_id):
    template = get_object_or_404(FoodplanTemplate, id=template_id)

    if not template:
        raise Http404()
    return JsonResponse({
        "title": template.title,
        "subtitle": template.subtitle,
        "text": template.text,
    })


@login_required
def foodplan_template_create(request):
    if request.method == "POST":
        form = FoodplanTemplateForm(request.POST)
        if form.is_valid():
            foodplanTemplate = form.save(commit=False)
            foodplanTemplate.save()
            return redirect("handbook")
    else:
        form = FoodplanTemplateForm()

    return render(request, "foodplan/foodplan_template_form.html", {
        "form": form,
    })

@login_required
def foodplan_template_edit(request, foodplan_template_id):
    foodplan_template = get_object_or_404(Report, id=foodplan_template_id)
    if request.method == "POST":
        form = FoodplanTemplateForm(request.POST)
        if form.is_valid():
            foodplan = form.save(commit=False)
            foodplan.save()
            return redirect("foodplan_template_detail", pk=foodplan_template_id)
    else:
        form = FoodplanTemplateForm(instance=foodplan)
    return render(request, 'foodplan/foodplan_template_form.html', {
        'form': form,
    })

@login_required
def foodplan_template_detail(request, foodplan_template_id):
    foodplan_template = get_object_or_404(FoodplanTemplate, id=foodplan_template_id)

    return render(request, "foodplan/foodplan_template_detail.html", {
        "foodplan_template": foodplan_template,
    })
