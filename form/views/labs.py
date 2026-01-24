from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST
from django import forms

from collections import defaultdict, OrderedDict

from ..models import *
from ..forms import *

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

@login_required
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
    
@login_required
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
    
    
    
@login_required
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
    
    
    
    
    
@login_required
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
    
    
    
@login_required
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
    
    
    
@login_required
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
    
    
    
@login_required
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
    
    
    
@login_required
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
    
    
    
    
@login_required
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
    
    
    
    
    
@login_required
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
    
    
    
    

@login_required
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
    
    
    
    
@login_required
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
    
    
    
@login_required
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
    
@login_required
def labentry_detail(request, pk):
    entry = get_object_or_404(LabEntry, pk=pk)

    if not request.user.is_staff:
        raise Http404()

    obj = entry.content_object 
    if obj is None:
        raise Http404("Исходный объект анализа не найден")

    docs = (
        LabDocument.objects
        .filter(entries=entry)
        .order_by("-created_at")
    )
    primary_doc = docs.first()

    context = {
        "entry": entry,
        "obj": obj,
        "docs": docs,
        "primary_doc": primary_doc,
        "has_doc": primary_doc is not None,
    }
    return render(request, "labs/labentry_detail.html", context)
