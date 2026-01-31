from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from django.views import View
from django import forms

from collections import defaultdict

from ..models import *
from ..forms import *


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

@login_required
def report_list(request):
    reports = Report.objects.order_by('created_date')
    return render(request, 'form/report_list.html',{"reports":reports, "nav_section": "reports"})

@login_required
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
    
    #Life style fields
    fields_lifeStyle = {}
    for field in Report._meta.get_fields():
        if field.name.startswith("life_"):
           fields_lifeStyle[field] = field.verbose_name

    return render(request, "form/report_detail.html", {
        "report": report,
        "fields_verbose": fields_verbose,
        "fields_lifeStyle":fields_lifeStyle,
        "nav_section": "reports",
    })

@login_required
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
        LifeStyle = [field.name for field in Report._meta.get_fields() if field.name.startswith("life_")]
    return render(request, 'form/report_edit.html', {
                                            'form': form,
                                            'prefs':Preferable,
                                            'intols':Intolerances, 
                                            'allergies': Allergies,
                                            'lifeStyle': LifeStyle,
                                             "nav_section": "reports"})
    
@login_required    
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
        LifeStyle = [field.name for field in Report._meta.get_fields() if field.name.startswith("life_")]
    return render(request, 'form/report_edit.html', {
                                            'form': form,
                                            'patient': patient,
                                            'prefs':Preferable,
                                            'intols':Intolerances, 
                                            'herr':Heredity,
                                            'allergies': Allergies,
                                            'lifeStyle': LifeStyle,
                                             "nav_section": "patients"})

@login_required
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
   
   
@login_required
def prescription_new(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    type_id = request.GET.get("type") or ""
    effect_id = request.GET.get("effect") or ""

    meds_qs = Medicine.objects.select_related("mtype", "effect").order_by("title")
    if type_id:
        meds_qs = meds_qs.filter(mtype_id=type_id)
    if effect_id:
        meds_qs = meds_qs.filter(effect_id=effect_id)

    if request.method == "POST":
        form = PrescriptionForm(request.POST, medicines_qs=meds_qs)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = patient
            obj.save()
            return redirect("patient_detail", pk=patient.pk)
        else:
            print(form.errors) 
    else:
        form = PrescriptionForm(medicines_qs=meds_qs)

    return render(request, "prescriptions/prescription_form.html", {
        "patient": patient,
        "form": form,
        "types": MedicineType.objects.order_by("name"),
        "effects": MedicineEffect.objects.order_by("name"),
        "selected_type": type_id,
        "selected_effect": effect_id,
    })
@login_required
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
    

@login_required    
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
    
