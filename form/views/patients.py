from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.urls import reverse
from django import forms

from ..models import *
from ..forms import *

@login_required
def patient_list(request):
    patients = Patient.objects.order_by('full_name')
    return render(request, 'form/patient_list.html',{'patients':patients, "nav_section": "patients"})
    
    
    

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk = pk)
    reports = Report.objects.filter(patient = patient).order_by('created_date')
    surveys = Questionnaire.objects.filter(patient = patient).order_by('created_at')
    
    biochems = Biochemistry.objects.filter(patient = patient)
    proteins = ProteinMetabolism.objects.filter(patient = patient)
    lipids = LipidMetabolism.objects.filter(patient = patient)
    carbohydrates = CarbohydrateMetabolism.objects.filter(patient = patient)
    irons = IronMetabolism.objects.filter(patient = patient)
    micros = Micronutrients.objects.filter(patient = patient)
    inflamms = InflammatoryMarkers.objects.filter(patient = patient)
    allergies = AllergiesInfections.objects.filter(patient = patient)
    thyroids = ThyroidFunction.objects.filter(patient = patient)
    hematologies = Hematology.objects.filter(patient = patient)
    platelets = Platelets.objects.filter(patient = patient)
    leukocytes = Leukocytes.objects.filter(patient = patient)
    hormons = HormonalLevels.objects.filter(patient = patient)
    hypotheses = DiagnosticHypothesis.objects.filter(patient=patient).order_by("-created_at")
    
    prescriptions = Prescription.objects.filter(patient = patient)
    return render(request, 'form/patient_detail.html',
        {'patient':patient, 
        'reports':reports,
        'surveys':surveys,
        'biochems': biochems, 
        'proteins':proteins , 
        'lipids':lipids,
        'carbohydrates':carbohydrates,
        'irons':irons,
        'micros':micros,
        'inflamms':inflamms,
        'allergies':allergies,
        'thyroids':thyroids,
        'hematologies':hematologies,
        'platelets':platelets,
        'leukocytes':leukocytes,
        'hormons':hormons,
        'prescriptions': prescriptions,
        "hypotheses": hypotheses,
        "nav_section": "patients"
        })


@login_required
def patient_new(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'form/patient_edit.html', {'form': form,"nav_section": "patients"})


    
    
@login_required()
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('patient_detail', pk=post.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'form/patient_edit.html', {'form': form, "patient": patient, "nav_section": "patients"})
    
