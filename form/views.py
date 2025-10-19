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
    reports = Report.objects.filter(patient = patient).order_by('created_date')
    
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
    
    prescriptions = Prescription.objects.filter(patient = patient)
    return render(request, 'form/patient_detail.html',
        {'patient':patient, 
        'reports':reports,
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
        })

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
    
    
def report_new_for_patient(request, pk):
    if request.method == "POST":
        form = ReportFormForPatient(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.patient = get_object_or_404(Patient, pk=pk)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=pk)
    else:
        form = ReportFormForPatient()
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
    
    
    
@login_required()
def inflammatorymarkers_new(request, pk):
    if request.method == "POST":
        form = InflammatoryMarkersForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = InflammatoryMarkersForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
@login_required()
def allergiesinfections_new(request, pk):
    if request.method == "POST":
        form = AllergiesInfectionsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = AllergiesInfectionsForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
    
@login_required()
def thyroidfunction_new(request, pk):
    if request.method == "POST":
        form = ThyroidFunctionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = ThyroidFunctionForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
    
    
@login_required()
def hematology_new(request, pk):
    if request.method == "POST":
        form = HematologyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = HematologyForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
    
    
@login_required()
def platelets_new(request, pk):
    if request.method == "POST":
        form = PlateletsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = PlateletsForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
    
@login_required()
def leukocytes_new(request, pk):
    if request.method == "POST":
        form = LeukocytesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = LeukocytesForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
    
    
@login_required()
def hormonallevels_new(request, pk):
    if request.method == "POST":
        form = HormonalLevelsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=post.patient.pk)
    else:
        form = HormonalLevelsForm()
    return render(request, 'form/report_edit.html', {'form': form})
    
