from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.urls import reverse
from django.db import transaction
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
    if not key:  # дефолтная бинарная шкала
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
