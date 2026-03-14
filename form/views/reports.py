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
    skip = {"id", "patient", "created_date", "entry"}
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
        "comment_diet": Report._meta.get_field("comment_diet").verbose_name,

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

        "heredity_Other": Report._meta.get_field("heredity_Other").verbose_name,

        # Аллергии
        "foodAllergy": Report._meta.get_field("foodAllergy").verbose_name,
        "medicineAllergy": Report._meta.get_field("medicineAllergy").verbose_name,
        "seasonalAllergy": Report._meta.get_field("seasonalAllergy").verbose_name,
        "contactAllergy": Report._meta.get_field("contactAllergy").verbose_name,
        "noAllergy": Report._meta.get_field("noAllergy").verbose_name,

        # Объективный статус
        "insp_General": Report._meta.get_field("insp_General").verbose_name,
        "insp_Body": Report._meta.get_field("insp_Body").verbose_name,
        "insp_Skin": Report._meta.get_field("insp_skin").verbose_name,
        "insp_Abdomen": Report._meta.get_field("insp_abdomen").verbose_name,
        "insp_Liver": Report._meta.get_field("insp_Liver").verbose_name,
        "insp_Liver_protudes": Report._meta.get_field("insp_Liver_protudes").verbose_name,
        "insp_Swelling": Report._meta.get_field("insp_Swelling").verbose_name,
        "insp_Muscle": Report._meta.get_field("insp_Muscle").verbose_name,
        "insp_Tongue": Report._meta.get_field("insp_Tongue").verbose_name,
        "insp_lymph": Report._meta.get_field("insp_lymph").verbose_name,
        "insp_thyroid": Report._meta.get_field("insp_thyroid").verbose_name,
        "insp_musculoskeletal": Report._meta.get_field("insp_musculoskeletal").verbose_name,
        "insp_Limbs": Report._meta.get_field("insp_Limbs").verbose_name,
        "insp_Other": Report._meta.get_field("insp_Other").verbose_name,

        # Итоги
        "title": Report._meta.get_field("title").verbose_name,
        "text": Report._meta.get_field("text").verbose_name,
    }

    fields_heredity = {}
    for field_name in Report.heredity_fields:
        field = Report._meta.get_field(field_name)
        field_value = field.value_from_object(report)
        if field_value == "Y":
            try:
                label = HeredityOption.objects.get(pk = Report._meta.get_field(field_name+"_label").value_from_object(report)).label
            except HeredityOption.DoesNotExist:
                label = "Присутствуют. Без подробностей."
            fields_heredity[field.verbose_name] = label
        elif field_value == "N":
            fields_heredity[field.verbose_name] = "Нет"
    
    #Life style fields
    fields_lifeStyle = {}
    #Diet Preferables
    pref_Diet = []

    for field in Report._meta.get_fields():
        if field.name.startswith("life_"):
            fields_lifeStyle[field.verbose_name] = field.value_from_object(report)
        elif field.name.startswith("pref_"):
            if field.value_from_object(report):
                pref_Diet.append(field.verbose_name)

    if fields_lifeStyle["COVID-19"]:
        fields_lifeStyle["COVID-19"] = "Перенесён"
    else:
        fields_lifeStyle.pop("COVID-19")

    pref_Diet_count = (len(pref_Diet) > 0)
    if pref_Diet_count:
        pref_Diet[0] = pref_Diet[0].capitalize()
        for i in range(len(pref_Diet)-1):
            pref_Diet[i] = pref_Diet[i] + ', '
        pref_Diet[-1] += '.'



    return render(request, "form/report_detail.html", {
        "report": report,
        "fields_verbose": fields_verbose,
        "fields_lifeStyle":fields_lifeStyle,
        "pref_Diet_count":pref_Diet_count,
        "pref_Diet":pref_Diet,
        "heredity":fields_heredity,
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
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.patient = get_object_or_404(Patient, pk=pk)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('patient_detail', pk=pk)


    form = ReportFormForPatient()
    Preferable = ["pref_Meat", "pref_Fish", "pref_Dair", "pref_Dair", "pref_Eggs", "pref_Vegs", "pref_Frut", "pref_Groa", "pref_Swet", "pref_Fast", "pref_Cofe", "pref_Alco"]
    Intolerances = ["intol_Lact", "intol_Glut", "intol_Nuts", "intol_Sea"]
    Heredity = ["cardiovascular","oncological","diabetes","thyroid","autoimmune","heredity_Other"]
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
        form = ReportFormForPatient(request.POST, instance=report)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('report_detail', pk=post.pk)

    form = ReportFormForPatient(instance=report)
    Preferable = ["pref_Meat", "pref_Fish", "pref_Dair", "pref_Dair", "pref_Eggs", "pref_Vegs", "pref_Frut", "pref_Groa", "pref_Swet", "pref_Fast", "pref_Cofe", "pref_Alco"]
    Intolerances = ["intol_Lact", "intol_Glut", "intol_Nuts", "intol_Sea"]
    Heredity = ["cardiovascular","oncological","diabetes","thyroid","autoimmune","heredity_Other"]
    Allergies = ["foodAllergy", "medicineAllergy", "seasonalAllergy", "contactAllergy", "noAllergy"]
    LifeStyle = [field.name for field in Report._meta.get_fields() if field.name.startswith("life_")]
    return render(request, 'form/report_edit.html', {
                                        'form': form,
                                        'patient': report.patient,
                                        'prefs':Preferable,
                                        'intols':Intolerances,
                                        'herr':Heredity,
                                        'allergies': Allergies,
                                        'lifeStyle': LifeStyle,
                                        'nav_section': "patients"})
   
   
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

    hypotheses_qs = DiagnosticHypothesis.objects.filter(patient=report.patient).order_by("-created_at")
    labs_qs = LabEntry.objects.filter(patient=report.patient).order_by("-taken_at")
    prescript_qs = Prescription.objects.filter(patient=report.patient).order_by("-created_at")
    foodplans_qs = Foodplan.objects.filter(patient=report.patient).order_by("-created_date")
    
    lab_previews = {}
    prescript_previews = {}
    lab_links = {}
    
    for le in labs_qs[:100]:
        obj = le.content_object
        lab_previews[le.pk] = build_preview_pairs(obj, limit=8)
        
    for prescript in prescript_qs[:100]:
        prescript_previews[prescript.pk] = {
        "regime": prescript.regime,
        "duration": prescript.duration,
        "comment": prescript.comment,
    }

    if request.method == "POST":
        form = ReportPrintConfigForm(
            request.POST,
            labs_queryset=labs_qs,
            prescript_queryset=prescript_qs,
            hypoth_queryset = hypotheses_qs,
            foodplan_queryset = foodplans_qs
        )
        sess_key = f"print_cfg_report_{report.pk}"
        if form.is_valid():
            cfg = form.cleaned_payload()
            request.session[sess_key] = cfg
            return redirect("report_print_preview", pk=report.pk)
    else:
        sess_key = f"print_cfg_report_{report.pk}"
        saved = request.session.get(sess_key, {})
        selected_labs = set(str(x) for x in saved.get("labs_ids", []))
        selected_prescripts = set(str(x) for x in saved.get("prescripts_ids", []))
        if saved:
            form = ReportPrintConfigForm(
                initial={
                    "doc_type": saved.get("doc_type", ReportPrintConfigForm.DocType.PATIENT),
                    "sections": saved.get("sections", []),
                    "labs": saved.get("labs_ids", []),
                    "prescriptions": saved.get("prescripts_ids", []),
                },
                labs_queryset=labs_qs,
                prescript_queryset=prescript_qs,
                hypoth_queryset = hypotheses_qs,
                foodplan_queryset = foodplans_qs,
            )
        else:
            form = ReportPrintConfigForm(
                labs_queryset=labs_qs,
                prescript_queryset=prescript_qs,
                hypoth_queryset = hypotheses_qs,
                foodplan_queryset = foodplans_qs,
                initial_doc_type=ReportPrintConfigForm.DocType.PATIENT,
            )

    return render(request, "form/report_print_config.html", {
        "report": report,
        "hypotheses_qs": hypotheses_qs,
        "foodplans_qs": foodplans_qs,
        "form": form,
        "page_title": "Настройка печати",
        "nav_section": "reports",
        "labs_qs": labs_qs,
        "lab_previews": lab_previews,
        "lab_links": lab_links,
        "selected_labs": selected_labs,
        "prescript_qs": prescript_qs,
        "selected_prescripts": selected_prescripts,
        "prescript_previews": prescript_previews,
    })
    

@login_required    
def report_print_preview(request, pk):
    report = get_object_or_404(Report, pk=pk)
    hypotheses = DiagnosticHypothesis.objects.filter(patient=report.patient).order_by("-created_at")

    sess_key = f"print_cfg_report_{report.pk}"
    cfg = request.session.get(sess_key)

    if not cfg:
        return redirect("report_print_config", pk=report.pk)

    sections = cfg.get("sections", [])
    doc_type = cfg.get("doc_type", "patient")
    labs_grouped = []

    labs_ids = cfg.get("labs_ids", [])
    hypotheses_ids = cfg.get("hypotheses_ids",[])
    prescripts_ids = cfg.get("prescripts_ids",[])
    foodplans_ids = cfg.get("foodplans_ids",[])
    
    if labs_ids:
            qs = (
                LabEntry.objects
                .filter(pk__in=labs_ids, patient=report.patient)
                .select_related("content_type")
                .order_by("kind", "-taken_at")
            )

            buckets = {}
            dates = defaultdict(list)
            kind_titles = {}
            for entry in qs:
                pairs = build_preview_pairs(entry.content_object)
                dates[entry.kind].append(getattr(entry, "taken_at", None))
                if not entry.kind in buckets:
                    buckets[entry.kind] = {}
                for f in pairs:
                    if not f[0] in buckets[entry.kind]:
                        buckets[entry.kind][f[0]] = []
                    buckets[entry.kind][f[0]].append(f[1])
                kind_titles[entry.kind] = entry.get_kind_display()


            for kind in sorted(buckets.keys(), key=lambda k: kind_titles.get(k, k)):
                labs_grouped.append({
                    "kind": kind,
                    "title": kind_titles.get(kind, kind),
                    "items": buckets[kind],
                    "dates": dates[kind],
                })

    prescripts_rows = []
    if prescripts_ids:
        prescripts_rows = (
            Prescription.objects
            .filter(pk__in=prescripts_ids, patient=report.patient)
            .order_by("-created_at")
        )

    hypotheses_rows = []
    if hypotheses_ids:
        hypotheses_rows = (
            DiagnosticHypothesis.objects
            .filter(pk__in=hypotheses_ids, patient=report.patient)
            .order_by("-created_at")
        )

    foodplans_rows = []
    if foodplans_ids:
        foodplans_rows = (
            Foodplan.objects
            .filter(pk__in=foodplans_ids, patient=report.patient)
            .order_by("-created_date")
        )


    context = {
        "report": report,
        "hypotheses": hypotheses_rows,
        "doc_type": doc_type,
        "sections": sections,
        "labs_grouped": labs_grouped,
        "prescripts_rows": prescripts_rows,
        "foodplans_rows": foodplans_rows,
    }
    print(prescripts_rows)
    return render(request, "print/report_print_preview.html", context)
    
