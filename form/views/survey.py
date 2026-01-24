from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Sum, Count
from django.utils import timezone
from django.views import View
from django.urls import reverse
from django.db import transaction
from django import forms

from ..models import *
from ..forms import *

SURVEY_SESSION_KEY = "survey_state"

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
        raise Http404("Invite is not valid")
    return invite

class CreateSurveyInviteView(LoginRequiredMixin, View):
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
        
        return render(request, "survey/invite_created.html", {
            "patient": patient,
            "public_url": public_url,
            "token": invite.token,
        })

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        return render(request, "survey/invite_confirm.html", {
            "patient": patient,
        })


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
        initial = {}
        for q in QuestionTemplate.objects.filter(section=section):
            key = f"q_{q.id}"
            if key in state["answers"]:
                initial[key] = state["answers"][key]
        form = FormCls(initial=initial)

        return render(request, self.template_name, {
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
        invite = get_valid_invite_or_404(token)
        return render(request, self.template_name, {
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

        invite.mark_used()
        save_state(request, token_key, {"cursor": 0, "answers": {}, "order": state.get("order", [])})

        return render(request, self.template_name, {
            "questionnaire": qt,
            "saved": len(to_create),
            "done": True,
        })
              
class SurveyResultsView(LoginRequiredMixin, View):
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

        qs = (Answer.objects
              .filter(questionnaire=invite)
              .select_related("question__section"))

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
        

