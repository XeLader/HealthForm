from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import *

# Create your views here.

@login_required()
def dashboard(request):
    reports = Report.objects.order_by('created_date')
    patients = Patient.objects.order_by('full_name')
    return render(request, 'form/dash.html',{'reports':reports, "patients":patients})


@login_required()
def report_list(request):
    forms = Report.objects.order_by('created_date')
    return render(request, 'form/report_list.html',{'forms':forms})


@login_required()
def patient_list(request):
    patients = Patient.objects.order_by('full_name')
    return render(request, 'form/patient_list.html',{'patients':patients})
    
    
    

@login_required()
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk = pk)
    biochems = Biochemistry.objects.filter(patient = patient)
    proteins = ProteinMetabolism.objects.filter(patient = patient)
    prescriptions = Prescription.objects.filter(patient = patient)
    return render(request, 'form/patient_detail.html',{'patient':patient, 'biochems': biochems, 'proteins':proteins , 'prescriptions': prescriptions,})

@login_required()
def report_detail(request, pk):
	report = get_object_or_404(Report, pk = pk)
	biochems = Biochemistry.objects.filter(patient = report.patient)
	return render(request, 'form/report_detail.html', {'report':report, 'biochems':biochems})

@login_required()
def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('report_detail', pk=post.pk)
    else:
        form = ReportForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
@login_required()
def patient_new(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'form/report_edit.html', {'form': form})

@login_required()
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('report_detail', pk=post.pk)
    else:
        form = ReportForm(instance=report)
    return render(request, 'form/report_edit.html', {'form': form})
    
    
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
    return render(request, 'form/report_edit.html', {'form': form})
    
@login_required()
def prescription_new(request, pk):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.pk)
    else:
        form = PrescriptionForm()
    return render(request, 'form/report_edit.html', {'form': form})

@login_required()
def biochemistry_new(request, pk):
    if request.method == "POST":
        form = BiochemistryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = BiochemistryForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
@login_required()
def proteinmetabolism_new(request, pk):
    if request.method == "POST":
        form = ProteinMetabolismForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = ProteinMetabolismForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
@login_required()
def lipidmetabolism_new(request, pk):
    if request.method == "POST":
        form = LipidMetabolismForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = LipidMetabolismForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
    
    
@login_required()
def carbohydratemetabolism_new(request, pk):
    if request.method == "POST":
        form = CarbohydrateMetabolismForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = CarbohydrateMetabolismForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
@login_required()
def ironmetabolism_new(request, pk):
    if request.method == "POST":
        form = IronMetabolismForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = IronMetabolismForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
@login_required()
def micronutrients_new(request, pk):
    if request.method == "POST":
        form = MicronutrientsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = MicronutrientsForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
