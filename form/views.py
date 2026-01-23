from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.db.models import Sum, Count
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db import transaction
from django import forms

from collections import defaultdict, OrderedDict

from .models import *
from .forms import *

# Create your views here.

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
                "nav_section": "patients",  # или отдельный раздел, как хочешь
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
        # Приглашение уже использовано
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


@login_required()
def report_list(request):
    reports = Report.objects.order_by('created_date')
    return render(request, 'form/report_list.html',{"reports":reports, "nav_section": "reports"})


@login_required()
def patient_list(request):
    patients = Patient.objects.order_by('full_name')
    return render(request, 'form/patient_list.html',{'patients':patients, "nav_section": "patients"})
    
    
    

@login_required()
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
        "nav_section": "patients"
        })

@login_required()
def report_detail(request, pk):
    report = get_object_or_404(Report, pk = pk)
    fields_verbose = {
        "complaints": Report._meta.get_field("complaints").verbose_name,
        "anamnesis": Report._meta.get_field("anamnesis").verbose_name,

        # Питание
        "diet": Report._meta.get_field("diet").verbose_name,
        "mealscount": Report._meta.get_field("mealscount").verbose_name,
        "snacks": Report._meta.get_field("snacks").verbose_name,

        # Непереносимости
        "intol_Lact": Report._meta.get_field("intol_Lact").verbose_name,
        "intol_Glut": Report._meta.get_field("intol_Glut").verbose_name,
        "intol_Nuts": Report._meta.get_field("intol_Nuts").verbose_name,
        "intol_Sea": Report._meta.get_field("intol_Sea").verbose_name,
        "intol_Other": Report._meta.get_field("intol_Other").verbose_name,

        # Наследственность
        "cardiovascular": Report._meta.get_field("cardiovascular").verbose_name,
        "oncological": Report._meta.get_field("oncological").verbose_name,
        "diabetes": Report._meta.get_field("diabetes").verbose_name,
        "thyroid": Report._meta.get_field("thyroid").verbose_name,
        "autoimmune": Report._meta.get_field("autoimmune").verbose_name,
        "allergic": Report._meta.get_field("allergic").verbose_name,

        # Аллергии
        "foodAllergy": Report._meta.get_field("foodAllergy").verbose_name,
        "medicineAllergy": Report._meta.get_field("medicineAllergy").verbose_name,
        "seasonalAllergy": Report._meta.get_field("seasonalAllergy").verbose_name,
        "contactAllergy": Report._meta.get_field("contactAllergy").verbose_name,
        "noAllergy": Report._meta.get_field("noAllergy").verbose_name,

        # Объективный статус
        "insp_General": Report._meta.get_field("insp_General").verbose_name,
        "insp_Body": Report._meta.get_field("insp_Body").verbose_name,
        "insp_Abdomen": Report._meta.get_field("insp_Abdomen").verbose_name,
        "insp_Liver": Report._meta.get_field("insp_Liver").verbose_name,
        "insp_Liver_protudes": Report._meta.get_field("insp_Liver_protudes").verbose_name,
        "insp_Other": Report._meta.get_field("insp_Other").verbose_name,

        # Итоги
        "title": Report._meta.get_field("title").verbose_name,
        "text": Report._meta.get_field("text").verbose_name,
    }

    return render(request, "form/report_detail.html", {
        "report": report,
        "fields_verbose": fields_verbose,
        "nav_section": "reports",
    })

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
        Preferable = ["pref_Meat", "pref_Fish", "pref_Dair", "pref_Dair", "pref_Eggs", "pref_Vegs", "pref_Frut", "pref_Groa", "pref_Swet", "pref_Fast", "pref_Cofe", "pref_Alco"]
        Intolerances = ["intol_Lact", "intol_Glut", "intol_Nuts", "intol_Sea", "intol_Other"]
        Allergies = ["foodAllergy", "medicineAllergy", "seasonalAllergy", "contactAllergy", "noAllergy"]
    return render(request, 'form/report_edit.html', {
                                            'form': form,
                                            'prefs':Preferable,
                                            'intols':Intolerances, 
                                            'allergies': Allergies,
                                             "nav_section": "reports"})
    
    
def report_new_for_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
        Preferable = ["pref_Meat", "pref_Fish", "pref_Dair", "pref_Dair", "pref_Eggs", "pref_Vegs", "pref_Frut", "pref_Groa", "pref_Swet", "pref_Fast", "pref_Cofe", "pref_Alco"]
        Intolerances = ["intol_Lact", "intol_Glut", "intol_Nuts", "intol_Sea", "intol_Other"]
        Heredity = ["cardiovascular","oncological","diabetes","thyroid","autoimmune","allergic",]
        Allergies = ["foodAllergy", "medicineAllergy", "seasonalAllergy", "contactAllergy", "noAllergy"]
    return render(request, 'form/report_edit.html', {
                                            'form': form,
                                            'patient': patient,
                                            'prefs':Preferable,
                                            'intols':Intolerances, 
                                            'herr':Heredity,
                                            'allergies': Allergies,
                                             "nav_section": "patients"})
    
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
    return render(request, 'form/patient_edit.html', {'form': form,"nav_section": "patients"})

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
    return render(request, 'form/report_edit.html', {'form': form,"nav_section": "reports", 'patient': report.patient})
    
    
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
    
@login_required()
def prescription_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Назначение",
        "card_title": "назначение",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })


LAB_FORMS = {
    "biochem":  (LabKind.BIOCHEM, Biochemistry, BiochemistryForm, "Биохимия"),
    "protein":  (LabKind.PROTEIN, ProteinMetabolism, ProteinMetabolismForm, "Белковый обмен"),
    "lipid":    (LabKind.LIPID, LipidMetabolism, LipidMetabolismForm, "Липидный обмен"),
    "carb":     (LabKind.CARB, CarbohydrateMetabolism, CarbohydrateMetabolismForm, "Углеводный обмен"),
    "iron":     (LabKind.IRON, IronMetabolism, IronMetabolismForm, "Железо"),
    "micro":    (LabKind.MICRO, Micronutrients, MicronutrientsForm, "Микронутриенты"),
    "inflamm":  (LabKind.INFLAMM, InflammatoryMarkers, InflammatoryMarkersForm, "Воспаление"),
    "allergy":  (LabKind.ALLERGY, AllergiesInfections, AllergiesInfectionsForm, "Аллергии/инфекции"),
    "thyroid":  (LabKind.THYROID, ThyroidFunction, ThyroidFunctionForm, "Щитовидная железа"),
    "hemat":    (LabKind.HEMAT, Hematology, HematologyForm, "Гематология"),
    "platelet": (LabKind.PLATELET, Platelets, PlateletsForm, "Тромбоциты"),
    "leuko":    (LabKind.LEUKO, Leukocytes, LeukocytesForm, "Лейкоциты"),
    "hormon":   (LabKind.HORMON, HormonalLevels, HormonalLevelsForm, "Гормоны"),
}

@login_required()
def biochemistry_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Новый анализ — биохимия",
        "card_title": "Биохимический анализ",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
@login_required()
def proteinmetabolism_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Белковый обмен",
        "card_title": "Белковый обмен",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def lipidmetabolism_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Липидный обмен",
        "card_title": "Липидный обмен",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
    
    
@login_required()
def carbohydratemetabolism_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Углеводный обмен",
        "card_title": "Углеводный обмен",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def ironmetabolism_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Обмен железа",
        "card_title": "Обмен железа",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def micronutrients_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Микроэлементы",
        "card_title": "Микроэлементы",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def inflammatorymarkers_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Маркеры воспаления",
        "card_title": "Маркеры воспаления",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def allergiesinfections_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Аллергия и инфекция",
        "card_title": "Аллергия и инфекция",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
    
@login_required()
def thyroidfunction_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Функция щитовидной железы",
        "card_title": "Функция щитовидной железы",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
    
    
@login_required()
def hematology_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Гематология (эритроцитарное звено)",
        "card_title": "Гематология (эритроцитарное звено)",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
    
    
@login_required()
def platelets_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Тромбоцитарное звено",
        "card_title": "Тромбоцитарное звено",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
    
@login_required()
def leukocytes_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Лейкоцитарное звено",
        "card_title": "Лейкоцитарное звено",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    
    
    
@login_required()
def hormonallevels_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
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
    return render(request, 'form/analysis_form.html', {
        "form": form,
        "page_title": "Гормональный фон",
        "card_title": "Гормональный фон",
        "cancel_url": request.META.get("HTTP_REFERER") or redirect("patient_detail", pk=patient.pk).url,
        "nav_section": "patients",
    })
    


SURVEY_SESSION_KEY = "survey_state"  # будем ключевать по токену

# ---- утилиты (как раньше, но без patient_id в URL) ----
def get_active_questionnaire():
    return QuestionnaireTemplate.objects.latest("code")

def build_section_order(qt: QuestionnaireTemplate):
    sections = (SectionTemplate.objects
             .filter(template=qt)
             .order_by("order"))
    order = []
    for s in sections:
        order.append(s.id)
    return order

def get_choices_by_key(key: str):
    if not key: 
        return [(0, "нет"), (8, "да")]
    k = key.lower()
    if k in ("08"):
        return [(0, "нет"), (8, "да")]
    if k in ("01"):
        return [(0, "нет"), (1, "да")]
    if k in ("0148"):
        return [(0, "нет/редко"), (1, "иногда"), (4, "часто"), (8, "очень часто")]
    return [(0, "нет"), (8, "да")]

def build_dynamic_form(section: SectionTemplate):
    qs = (QuestionTemplate.objects
          .filter(section=section)
          .order_by("order", "id"))
    class SectionForm(forms.Form): pass
    for q in qs:
        name = f"q_{q.id}"
        choices = get_choices_by_key(q.scale)
        field = forms.TypedChoiceField(
            label=q.text,
            choices=choices,
            widget=forms.RadioSelect,
            required=getattr(q, "required", True),
            coerce=int,
        )
        SectionForm.base_fields[name] = field
    return SectionForm

def load_state(request, token_str):
    state = request.session.get(SURVEY_SESSION_KEY, {})
    return state.get(token_str, {"cursor": 0, "answers": {}, "order": None})

def save_state(request, token_str, state):
    all_state = request.session.get(SURVEY_SESSION_KEY, {})
    all_state[token_str] = state
    request.session[SURVEY_SESSION_KEY] = all_state
    request.session.modified = True

def get_valid_invite_or_404(token):
    invite = get_object_or_404(Questionnaire, token=token)
    if not invite.is_valid():
        # 404 вместо «вышла дата/использовано» — чтобы не палить детали
        raise Http404("Invite is not valid")
    return invite

# ---- приватный (для врача/сотрудника): создать приглашение и показать ссылку ----
class CreateSurveyInviteView(View):
    # добавьте @permission_required / @login_required по своей системе
    def post(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        qt = get_active_questionnaire()
        invite = Questionnaire.objects.create(
            patient=patient,
            template=qt
        )
        public_url = request.build_absolute_uri(
            reverse("survey_run_public", kwargs={"token": str(invite.token)})
        )
        # здесь можете отправить SMS/Email, а пока просто покажем
        return render(request, "survey/invite_created.html", {
            "patient": patient,
            "public_url": public_url,
            "token": invite.token,
        })

    def get(self, request, pk):
        # по GET можно показать подтверждение/кнопку «создать ссылку»
        patient = get_object_or_404(Patient, pk=pk)
        return render(request, "survey/invite_confirm.html", {
            "patient": patient,
        })


# ---- публичный мастер по токену ----
class PublicSurveySectionView(View):
    template_name = "survey/section_public.html"

    def get(self, request, token):
        invite = get_valid_invite_or_404(token)
        qt = invite.template
        token_key = str(invite.token)

        state = load_state(request, token_key)
        order = state.get("order") or build_section_order(qt)
        state["order"] = order
        save_state(request, token_key, state)

        if not order:
            return render(request, self.template_name, {"empty": True})

        cursor = max(0, min(state.get("cursor", 0), len(order)-1))
        section_id = order[cursor]
        section = get_object_or_404(SectionTemplate, id=section_id)

        FormCls = build_dynamic_form(section)
        # префилл
        initial = {}
        for q in QuestionTemplate.objects.filter(section=section):
            key = f"q_{q.id}"
            if key in state["answers"]:
                initial[key] = state["answers"][key]
        form = FormCls(initial=initial)

        return render(request, self.template_name, {
            # НИЧЕГО персонального о пациенте!
            "questionnaire": qt,
            "section": section,
            "form": form,
            "cursor": cursor,
            "total": len(order),
            "is_first": cursor == 0,
            "is_last": cursor == len(order)-1,
            "token": token,  # нужен для action’ов кнопок
        })

    def post(self, request, token):
        invite = get_valid_invite_or_404(token)
        qt = invite.template
        token_key = str(invite.token)

        state = load_state(request, token_key)
        order = state.get("order") or build_section_order(qt)

        cursor = max(0, min(state.get("cursor", 0), len(order)-1))
        section_id = order[cursor]
        section = get_object_or_404(SectionTemplate, id=section_id)

        FormCls = build_dynamic_form(section)
        form = FormCls(request.POST)
        if form.is_valid():
            # сохранить в session
            for name, value in form.cleaned_data.items():
                state["answers"][name] = value

            if "prev" in request.POST and cursor > 0:
                state["cursor"] = cursor - 1
            elif "next" in request.POST and cursor < len(order)-1:
                state["cursor"] = cursor + 1
            elif "finish" in request.POST and cursor == len(order)-1:
                save_state(request, token_key, state)
                return redirect("survey_finish_public", token=str(invite.token))

            save_state(request, token_key, state)
            return redirect("survey_run_public", token=str(invite.token))

        return render(request, self.template_name, {
            "questionnaire": qt,
            "section": section,
            "form": form,
            "cursor": cursor,
            "total": len(order),
            "is_first": cursor == 0,
            "is_last": cursor == len(order)-1,
            "token": token,
        })


class PublicSurveyFinishView(View):
    template_name = "survey/finish_public.html"

    def get(self, request, token):
        # простая страница-подтверждение перед отправкой
        invite = get_valid_invite_or_404(token)
        return render(request, self.template_name, {
            # ничего личного
            "questionnaire": invite.template,
            "token": str(invite.token),
            "confirm": True,
        })

    @transaction.atomic
    def post(self, request, token):
        invite = get_valid_invite_or_404(token)
        qt = invite.template
        token_key = str(invite.token)
        state = load_state(request, token_key)
        answers_map = state.get("answers", {})

        to_create = []
        for key, raw_value in answers_map.items():
            try:
                qid = int(key.split("_", 1)[1])
            except Exception:
                continue
            q = QuestionTemplate.objects.filter(id=qid).select_related("section").first()
            if not q:
                continue
            to_create.append(Answer(
                questionnaire = invite,  # связь только на бэке
                question=q,
                score=raw_value,         # уже int
            ))

        if to_create:
            Answer.objects.bulk_create(to_create, batch_size=200)

        # по желанию одноразовость:
        invite.mark_used()

        # очистить сессию под этот токен
        save_state(request, token_key, {"cursor": 0, "answers": {}, "order": state.get("order", [])})

        return render(request, self.template_name, {
            "questionnaire": qt,
            "saved": len(to_create),
            "done": True,
        })
        
        
class SurveyResultsView(View):
    template_name = "survey/results.html"
    
    def classify_priority(total, low, high):
        if low is None:
            low = -10**9
        if high is None:
            high = 10**9

        if total is None:
            total = 0

        if total < low:
            return ("low",  "#14a44d", "низкий")
        elif total >= high:
            return ("high", "#dc4c64", "высокий")
        else:
            return ("mid",  "#e4a11b", "средний")


    def get(self, request, pk, token):
        patient = get_object_or_404(Patient, pk=pk)
        invite = get_object_or_404(Questionnaire, token=token, patient=patient)

        # Все ответы по этому приглашению
        qs = (Answer.objects
              .filter(questionnaire=invite)
              .select_related("question__section"))

        # Суммы по секциям
        by_section = (qs
            .values(
                "question__section__id",
                "question__section__title",
                "question__section__description",
                "question__section__low",
                "question__section__height"
            )
            .annotate(
                total=Sum("score"),
                cnt=Count("id"),
            )
            .order_by("question__section__title")
        )

        sections = []
        for row in by_section:
            total      = row["total"] or 0
            low_thr    = row.get("question__section__low")
            height_thr = row.get("question__section__height")
            section_id = row["question__section__id"]
            section_title = row["question__section__title"]
            section_description = row["question__section__description"]
            count = row["cnt"] or 0
            if height_thr is None:
                height_thr = row.get("question__section__high")
            pri_slug, pri_color, pri_label = SurveyResultsView.classify_priority(total, low_thr, height_thr)
            sections.append({
                "section_id": section_id,
                "section_title": section_title,
                "section_description": section_description,
                "total": total,
                "count": count,
                "priority": {
                    "slug": pri_slug,     # "low" / "mid" / "high"
                    "label": pri_label,   
                    "color": pri_color,   
                    "low": low_thr,
                    "high": height_thr,
                },
            })
    
        raw_answers = (qs
            .values(
                "question_id",
                "question__text",
                "question__section__title",
                "score",
            )
            .order_by("question__section__id", "question_id")
        )

        ctx = {
            "patient": patient,
            "invite": invite,
            "parts": sections,
            "raw_answers": raw_answers,
            "priority_palette": {
                "low":  {"color": "#14a44d", "label": "низкий"},
                "mid":  {"color": "#e4a11b", "label": "средний"},
                "high": {"color": "#dc4c64", "label": "высокий"},
            }
        }
        return render(request, self.template_name, ctx)
        


def build_preview_pairs(obj, limit=6):
    skip = {"id", "patient", "created_date"}
    pairs = []
    for f in obj._meta.fields:
        if f.name in skip:
            continue
        val = getattr(obj, f.name, None)
        if val in (None, "", 0):
            continue
        if getattr(f, "choices", None):
            try:
                val = getattr(obj, f"get_{f.name}_display")()
            except Exception:
                pass
        pairs.append((f.verbose_name or f.name, val))
        if len(pairs) >= limit:
            break
    return pairs        
        
        
def report_print_config(request, pk):
    report = get_object_or_404(Report, pk=pk)


    labs_qs = LabEntry.objects.filter(patient=report.patient).order_by("-taken_at")
    rx_qs = Prescription.objects.filter(patient=report.patient).order_by("-created_at")
    
    lab_previews = {}
    rx_previews = {}
    lab_links = {}
    
    for le in labs_qs[:100]:
        obj = le.content_object
        lab_previews[le.pk] = build_preview_pairs(obj, limit=8)
        
    for rx in rx_qs[:100]:
        rx_previews[rx.pk] = {
        "regime": rx.regime,
        "duration": rx.duration,
        "comment": rx.comment,
    }

    if request.method == "POST":
        form = ReportPrintConfigForm(
            request.POST,
            labs_queryset=labs_qs,
            rx_queryset=rx_qs,
        )
        sess_key = f"print_cfg_report_{report.pk}"
        selected_rx = set(request.POST.getlist("rx"))
        selected_labs = set(request.POST.getlist("labs"))
        if form.is_valid():
            cfg = form.cleaned_payload()
            rx_ids = [int(x) for x in request.POST.getlist("rx")]
            cfg["rx_ids"] = rx_ids
            request.session[sess_key] = cfg
            return redirect("report_print_preview", pk=report.pk)
    else:
        sess_key = f"print_cfg_report_{report.pk}"
        saved = request.session.get(sess_key, {})
        selected_labs = set(str(x) for x in saved.get("labs_ids", []))
        selected_rx = set(str(x) for x in saved.get("rx_ids", []))
        if saved:
            form = ReportPrintConfigForm(
                initial={
                    "doc_type": saved.get("doc_type", ReportPrintConfigForm.DocType.PATIENT),
                    "sections": saved.get("sections", []),
                    "labs": saved.get("labs_ids", []),
                    "prescriptions": saved.get("rx_ids", []),
                },
                labs_queryset=labs_qs,
                rx_queryset=rx_qs,
            )
        else:
            form = ReportPrintConfigForm(
                labs_queryset=labs_qs,
                rx_queryset=rx_qs,
                initial_doc_type=ReportPrintConfigForm.DocType.PATIENT,
            )

    return render(request, "form/report_print_config.html", {
        "report": report,
        "form": form,
        "page_title": "Настройка печати",
        "nav_section": "reports",
        "labs_qs": labs_qs,
        "lab_previews": lab_previews,
        "lab_links": lab_links,
        "selected_labs": selected_labs,
        "rx_qs": rx_qs,
        "selected_rx": selected_rx,
        "rx_previews": rx_previews,
    })
    
    
def report_print_preview(request, pk):
    report = get_object_or_404(Report, pk=pk)

    sess_key = f"print_cfg_report_{report.pk}"
    cfg = request.session.get(sess_key)

    if not cfg:
        return redirect("report_print_config", pk=report.pk)

    sections = cfg.get("sections", [])
    doc_type = cfg.get("doc_type", "patient")
    labs_grouped = []

    labs_ids = cfg.get("labs_ids", [])
    
    if labs_ids:
            qs = (
                LabEntry.objects
                .filter(pk__in=labs_ids, patient=report.patient)
                .select_related("content_type")
                .order_by("kind", "-taken_at")
            )

            buckets = defaultdict(list)
            kind_titles = {}
            for entry in qs:
                buckets[entry.kind].append(entry)
                kind_titles[entry.kind] = entry.get_kind_display()

            for kind in sorted(buckets.keys(), key=lambda k: kind_titles.get(k, k)):
                labs_grouped.append({
                    "kind": kind,
                    "title": kind_titles.get(kind, kind),
                    "items": buckets[kind],
                })

    rx_rows = []
    rx_ids = cfg.get("rx_ids", [])
    if rx_ids:
        rx_rows = (
            Prescription.objects
            .filter(pk__in=rx_ids, patient=report.patient)
            .order_by("-created_at")
        )


    context = {
        "report": report,
        "doc_type": doc_type,
        "sections": sections,
        "labs_grouped": labs_grouped,
        "rx_rows": rx_rows,
    }

    return render(request, "print/report_print_preview.html", context)
    
@login_required
def labdoc_upload(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        form = LabDocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.patient = patient
            doc.uploaded_by = request.user
            doc.original_name = request.FILES["file"].name if "file" in request.FILES else ""
            doc.status = LabDocument.Status.NEW
            doc.save()
            return redirect("labdoc_fill", doc_id=doc.id)
    else:
        form = LabDocumentUploadForm()

    return render(request, "labs/labdoc_upload.html", {
        "patient": patient,
        "form": form,
    })
    
@login_required
def labdoc_file(request, doc_id):
    doc = get_object_or_404(LabDocument, id=doc_id)

    if not request.user.is_staff:
        raise Http404()

    return FileResponse(
        doc.file.open("rb"),
        content_type="application/pdf",
        as_attachment=False,
        filename=doc.original_name or "lab.pdf",
    )

@login_required
def labdoc_fill(request, doc_id):
    doc = get_object_or_404(LabDocument, id=doc_id)

    lab_types = []
    for slug, (_kind, _model, _form, title) in LAB_FORMS.items():
        lab_types.append({"slug": slug, "title": title})

    entries = (
        doc.entries
        .select_related("content_type")
        .order_by("-taken_at")
    )

    return render(request, "labs/labdoc_fill.html", {
        "doc": doc,
        "patient": doc.patient,
        "lab_types": lab_types,
        "entries": entries,
    })
    
    
@login_required
def labdoc_add_lab(request, doc_id, kind):
    doc = get_object_or_404(LabDocument, id=doc_id)

    if kind not in LAB_FORMS:
        raise Http404("Unknown lab kind")

    lab_kind, Model, FormClass, title = LAB_FORMS[kind]

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = doc.patient
            if hasattr(obj, "created_date") and not obj.created_date:
                obj.created_date = timezone.now()
            obj.save()

            ct = ContentType.objects.get_for_model(Model)
            entry = LabEntry.objects.get(content_type=ct, object_id=obj.pk)

            doc.entries.add(entry)
            doc.status = LabDocument.Status.IN_PROGRESS
            doc.save(update_fields=["status"])

            return redirect("labdoc_fill", doc_id=doc.id)
    else:
        form = FormClass()

    return render(request, "labs/labdoc_add_lab.html", {
        "doc": doc,
        "patient": doc.patient,
        "form": form,
        "title": title,
        "kind": kind,
    })
    
@login_required
@require_POST
def labdoc_unlink_entry(request, doc_id, entry_id):
    doc = get_object_or_404(LabDocument, id=doc_id)
    entry = get_object_or_404(LabEntry, pk=entry_id, patient=doc.patient)

    doc.entries.remove(entry)
    return redirect("labdoc_fill", doc_id=doc.id)
    
@login_required
@require_POST
def labdoc_mark_done(request, doc_id):
    doc = get_object_or_404(LabDocument, id=doc_id)

    if not request.user.is_staff:
        return redirect("labdoc_fill", doc_id=doc.id)

    doc.status = LabDocument.Status.DONE
    doc.save(update_fields=["status"])

    return redirect("patient_labdocs", pk=doc.patient.pk)

@login_required
def patient_labdocs(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    docs = (
        LabDocument.objects
        .filter(patient=patient)
        .select_related("uploaded_by")
        .prefetch_related("entries")
        .order_by("-created_at")
    )

    return render(request, "labs/patient_labdocs.html", {
        "patient": patient,
        "docs": docs,
    })
