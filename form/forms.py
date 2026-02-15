from django import forms
from django.contrib.auth.models import User
from .models import *
from .models.medicine import *
from .models.foodplan import *
from .models.report import HeredityOption
from .models.models import DiagnosticHypothesis
from django.db import models


class UserInviteCreateForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ["email", "make_staff"]
        labels = {
            "email": "E-mail ассистента",
            "make_staff": "Дать права сотрудника (staff)",
        }


class InviteRegisterForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают")
        return cleaned


class ReportForm(forms.ModelForm):


    def lifeStyles(self):
        return [self[name] for name in filter(lambda x: x.startswith('life_'), self.fields)]


    YNU = {
    "U":"неизвестно",
    "N":"нет",
    "Y":"да",
    }

    cardiovascular = forms.ChoiceField(choices=YNU, widget=forms.RadioSelect())

    class Meta:
        model = Report
        fields = ('patient', 'title', 'text', 'complaints', 'anamnesis', 'diet', 'mealscount', 'snacks', 'pref_Meat', 'pref_Fish',
        'pref_Dair', 'pref_Eggs', 'pref_Vegs', 'pref_Frut', 'pref_Groa', 'pref_Swet',
        'pref_Fast', 'pref_Cofe', 'pref_Alco', 'intol_Lact', 'intol_Glut' ,'intol_Nuts' ,'intol_Sea' ,'intol_Other', "comment_diet",
        'cardiovascular', 'cardiovascular_label', 'oncological','oncological_label', 'diabetes', 'diabetes_label', 'thyroid', 'thyroid_label', 'autoimmune', 'autoimmune_label', 'heredity_Other',
        'foodAllergy', 'medicineAllergy', 'seasonalAllergy', 'contactAllergy', 'noAllergy', 'insp_General', 'insp_Body', 'insp_Skin',
        'insp_lymph', 'insp_thyroid', 'insp_abdomen', 'insp_Liver', 'insp_Liver_protudes', 'insp_musculoskeletal', 'insp_Swelling', 'insp_Muscle', 'insp_Tongue','insp_Limbs', 'insp_Other',
        'next_date', 'life_physAct', 'life_sleepMode', 'life_stress', 'life_antibiotics', 'life_covid', 'life_vaccinationDate')
        widgets = {
            "insp_lymph": forms.CheckboxSelectMultiple,
            "insp_thyroid": forms.CheckboxSelectMultiple,
            "insp_skin": forms.CheckboxSelectMultiple,
            "insp_musculoskeletal": forms.CheckboxSelectMultiple,
            "insp_abdomen":forms.CheckboxSelectMultiple,
            "insp_Tongue": forms.CheckboxSelectMultiple,
            "oncological": forms.RadioSelect,
            "diabetes": forms.RadioSelect,
            "thyroid": forms.RadioSelect,
            "autoimmune": forms.RadioSelect,
        }
        
class ReportFormForPatient(forms.ModelForm):
    def lifeStyles(self):
        return [self[name] for name in filter(lambda x: x.startswith('life_'), self.fields)]

    def heredity(self):
        pair={}
        for name in ['cardiovascular', 'oncological', 'diabetes', 'thyroid', 'autoimmune']:
            k = self[name]
            pair[k] = self[name+"_label"]
        return pair
    
    cardiovascular_label = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если да, то укажите какое.",
    )

    oncological_label = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если да, то укажите какое.",
    )


    diabetes_label = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если да, то укажите какое.",
    )


    thyroid_label = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если да, то укажите какое.",
    )


    autoimmune_label = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если да, то укажите какое.",
    )


    class Meta:
        model = Report
        fields = ('title', 'text', 'complaints', 'anamnesis', 'diet', 'mealscount', 'snacks', 'pref_Meat', 'pref_Fish',
        'pref_Dair', 'pref_Eggs', 'pref_Vegs', 'pref_Frut', 'pref_Groa', 'pref_Swet',
        'pref_Fast', 'pref_Cofe', 'pref_Alco', 'intol_Lact', 'intol_Glut' ,'intol_Nuts' ,'intol_Sea' ,'intol_Other', "comment_diet",
        'cardiovascular', 'oncological', 'diabetes', 'thyroid', 'autoimmune', 'heredity_Other',
        'foodAllergy', 'medicineAllergy', 'seasonalAllergy', 'contactAllergy', 'noAllergy', 'insp_General', 'insp_Body', 'insp_skin',
        'insp_lymph', 'insp_thyroid', 'insp_abdomen', 'insp_Liver', 'insp_Liver_protudes', 'insp_musculoskeletal', 'insp_Swelling', 'insp_Muscle', 'insp_Tongue','insp_Limbs', 'insp_Other',
        'next_date', 'life_physAct', 'life_sleepMode', 'life_stress', 'life_antibiotics', 'life_covid', 'life_vaccinationDate')
        
        widgets = {
            "insp_lymph": forms.CheckboxSelectMultiple,
            "insp_thyroid": forms.CheckboxSelectMultiple,
            "insp_skin": forms.CheckboxSelectMultiple,
            "insp_musculoskeletal": forms.CheckboxSelectMultiple,
            "insp_abdomen":forms.CheckboxSelectMultiple,
            "insp_Tongue": forms.CheckboxSelectMultiple,
            "cardiovascular": forms.RadioSelect,
            "oncological": forms.RadioSelect,
            "diabetes": forms.RadioSelect,
            "thyroid": forms.RadioSelect,
            "autoimmune": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        inst = getattr(self, "instance", None)
        if inst and inst.pk:
            self.fields["cardiovascular_label"].initial = inst.cardiovascular_label_id
            self.fields["oncological_label"].initial = inst.oncological_label_id
            self.fields["diabetes_label"].initial = inst.diabetes_label_id
            self.fields["thyroid_label"].initial = inst.thyroid_label_id
            self.fields["autoimmune_label"].initial = inst.autoimmune_label_id


    def clean(self):
        cleaned = super().clean()

        cardiovascular_label = (cleaned.get("cardiovascular_label") or "").strip()
        oncological_label = (cleaned.get("oncological_label") or "").strip()
        diabetes_label = (cleaned.get("diabetes_label") or "").strip()
        thyroid_label = (cleaned.get("thyroid_label") or "").strip()
        autoimmune_label = (cleaned.get("autoimmune_label") or "").strip()

        cleaned["cardiovascular_label"] = cardiovascular_label
        cleaned["oncological_label"] = oncological_label
        cleaned["diabetes_label"] = diabetes_label
        cleaned["thyroid_label"] = thyroid_label
        cleaned["autoimmune_label"] = autoimmune_label

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        cd = self.cleaned_data
        if cd.get("cardiovascular") == "Y":
            obj.cardiovascular_label, _ = HeredityOption.objects.get_or_create(label=cd["cardiovascular_label"])


        if  cd.get("oncological")== "Y":
            obj.oncological_label, _ = HeredityOption.objects.get_or_create(label=cd["oncological_label"])



        if cd.get("diabete")== "Y":
            obj.cardiovascular_label, _ = HeredityOption.objects.get_or_create(label=cd["diabetes_label"])


        if cd.get("thyroid")== "Y":
            obj.thyroid_label, _ = HeredityOption.objects.get_or_create(label=cd["thyroid_label"])


        if cd.get("autoimmune")== "Y":
            obj.autoimmune_label, _ = HeredityOption.objects.get_or_create(label=cd["autoimmune_label"])

        if commit:
            obj.save()
        return obj

        
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name',"date_of_birth", "sex", 'growth', 'weight')
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
        
class PrescriptionForm(forms.ModelForm):
    def __init__(self, *args, medicines_qs=None, **kwargs):
        super().__init__(*args, **kwargs)
        if medicines_qs is not None:
            self.fields["medicine"].queryset = medicines_qs
    class Meta:
        model = Prescription
        fields = ('medicine','regime', 'duration', 'comment')
        
        
class BiochemistryForm(forms.ModelForm):
    class Meta:
        model = Biochemistry
        fields = ('patient', 'alat', 'asat', 'ldh' ,'cpk')
        
        
class ProteinMetabolismForm(forms.ModelForm):
    class Meta:
        model = ProteinMetabolism
        fields = ('patient', 'gammaGT', 'ttlProtein', 'albumin' ,'phosphatase', 'urea', 'creatinine', 'uricAcid', 'alpha1Globulins', 'alpha2Globulins', 'beta1Globulins', 'beta2Globulins', 'gammaGlobulins')
        
        
class LipidMetabolismForm(forms.ModelForm):
    class Meta:
        model = LipidMetabolism
        fields = ('patient', 'ttlBilirubin', 'drctBilirubin' ,'indrctBilirubin', 'ttlCholesterol', 'LDL', 'VLDL', 'HDL' ,'Triglycerides')
        
class CarbohydrateMetabolismForm(forms.ModelForm):
    class Meta:
        model = CarbohydrateMetabolism
        fields = ('patient', 'fastingGlucose', 'glycatedHemoglobin')
        
class IronMetabolismForm(forms.ModelForm):
    class Meta:
        model = IronMetabolism
        fields = ('patient', 'serumIron', 'ferritin' ,'transferrin', 'TIBC', 'transferrinSat')
        
        
class MicronutrientsForm(forms.ModelForm):
    class Meta:
        model = Micronutrients
        fields = ('patient', 'copper', 'zinc' ,'magnesium', 'ttlCalcium', 'potassium', 'sodium', 'chloride')
        
        
class InflammatoryMarkersForm(forms.ModelForm):
    class Meta:
        model = InflammatoryMarkers
        fields = ('patient', 'cReactiveProtein', 'fibrinogen' ,'ASLO', 'homocysteine')
        
        
class AllergiesInfectionsForm(forms.ModelForm):
    class Meta:
        model = AllergiesInfections
        fields = ('patient', 'ttlIgE', 'IgA' ,'IgM', 'IgG', 'antiCandida', 'antiParasitic')
        
        
class ThyroidFunctionForm(forms.ModelForm):
    class Meta:
        model = ThyroidFunction
        fields = ('patient', 'TSH', 'freeT4' ,'freeT3', 'totalT4', 'totalT3', 'reverseT3', 'TPOAb', 'TgAb')

                
class HematologyForm(forms.ModelForm):
    class Meta:
        model = Hematology
        fields = ('patient', 'hemoglobin', 'hematocrit' ,'redBloodCells', 'MCV', 'RDW', 'MCH', 'MCHC')

        
class PlateletsForm(forms.ModelForm):
    class Meta:
        model = Platelets
        fields = ('patient', 'platelets', 'MPV' ,'PCT', 'PDW')
        
        
class LeukocytesForm(forms.ModelForm):
    class Meta:
        model = Leukocytes
        fields = ('patient', 'leukocytes', 'neutrophilsPer' ,'neutrophilsAbs', 'lymphocytesPer', 'lymphocytesAbs', 'monocytesPer', 'monocytesAbs', 'eosinophilsPer', 'eosinophilsAbs', 'basophilsPer', 'basophilsAbs', 'ESR')
        
        
class HormonalLevelsForm(forms.ModelForm):
    class Meta:
        model = HormonalLevels
        fields = ('patient', 'FSH', 'LH' ,'estradiol', 'progesterone', 'ttlTestosterone', 'freeTestosterone', 'DHT', 'DHEASulfate', 'SHBG', 'prolactin', 'PSA')
        
class ReportPrintConfigForm(forms.Form):
    class DocType(models.TextChoices):
        PATIENT = "patient", "Для пациента"
        CLINIC = "clinic", "Для клиники"

    SECTION_CHOICES = [
        ("complaints_anamnesis", "Жалобы и анамнез"),
        ("diet_preferences", "Питание и предпочтения"),
        ("intolerances", "Непереносимости"),
        ("heredity", "Наследственность"),
        ("allergies", "Аллергический анамнез"),
        ("inspection", "Объективный статус"),
        ("conclusion", "Заключение (текст/рекомендации)"),
        ("followup", "Следующий приём (дата)"),
    ]

    PRESETS = {
        DocType.PATIENT: {
            "sections": [
                "complaints_anamnesis",
                "diet_preferences",
                "intolerances",
                "allergies",
                "conclusion",
                "followup",
            ],
            "include_labs": True,
            "include_rx": True,
        },
        DocType.CLINIC: {
            "sections": [
                "complaints_anamnesis",
                "diet_preferences",
                "intolerances",
                "heredity",
                "allergies",
                "inspection",
                "conclusion",
                "followup",
            ],
        },
    }

    doc_type = forms.ChoiceField(
        label="Вариант документа",
        choices=DocType.choices,
        initial=DocType.PATIENT,
        widget=forms.RadioSelect,
    )

    sections = forms.MultipleChoiceField(
        label="Какие разделы включить",
        choices=SECTION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )



    def __init__(self, *args, labs_queryset=None, rx_queryset=None, initial_doc_type=None, **kwargs):
        super().__init__(*args, **kwargs)

        if initial_doc_type in self.PRESETS and not self.is_bound:
            preset = self.PRESETS[initial_doc_type]
            self.initial.setdefault("doc_type", initial_doc_type)
            self.initial.setdefault("sections", preset["sections"])

        if labs_queryset is not None:
            self.fields["labs"] = forms.ModelMultipleChoiceField(
                label="Анализы",
                queryset=labs_queryset,
                required=False,
                widget=forms.CheckboxSelectMultiple,
            )

        if rx_queryset is not None:
            self.fields["prescriptions"] = forms.ModelMultipleChoiceField(
                label="Рецепты",
                queryset=rx_queryset,
                required=False,
                widget=forms.CheckboxSelectMultiple,
            )

    @classmethod
    def preset_for(cls, doc_type: str) -> dict:
        return cls.PRESETS.get(doc_type, cls.PRESETS[cls.DocType.PATIENT])

    def cleaned_payload(self) -> dict:
        data = {
            "doc_type": self.cleaned_data.get("doc_type"),
            "sections": self.cleaned_data.get("sections", []),
        }

        if "labs" in self.fields:
            data["labs_ids"] = [obj.pk for obj in self.cleaned_data.get("labs", [])]

        if "prescriptions" in self.fields:
            data["rx_ids"] = [obj.pk for obj in self.cleaned_data.get("prescriptions", [])]

        return data
        
class LabDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = LabDocument
        fields = ["file", "note"]

class MedicineCreateForm(forms.ModelForm):
    mtype = forms.ModelChoiceField(
        queryset=MedicineType.objects.order_by("name"),
        required=False,
        label="Тип (из списка)",
        empty_label="— не выбран —",
    )
    effect = forms.ModelChoiceField(
        queryset=MedicineEffect.objects.order_by("name"),
        required=False,
        label="Воздействие (из списка)",
        empty_label="— не выбрано —",
    )

    mtype_new = forms.CharField(
        required=False,
        label="Тип (новый)",
        max_length=100,
        help_text="Если нужного типа нет — введите здесь, он будет создан.",
    )
    effect_new = forms.CharField(
        required=False,
        label="Воздействие (новое)",
        max_length=100,
        help_text="Если нужного воздействия нет — введите здесь, оно будет создано.",
    )

    class Meta:
        model = Medicine
        fields = ["title", "usage"] 
        widgets = {
            "usage": forms.Textarea(attrs={"rows": 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        inst = getattr(self, "instance", None)
        if inst and inst.pk:
            self.fields["mtype"].initial = inst.mtype_id
            self.fields["effect"].initial = inst.effect_id

            self.fields["mtype_new"].initial = ""
            self.fields["effect_new"].initial = ""

    def clean(self):
        cleaned = super().clean()

        mtype_new = (cleaned.get("mtype_new") or "").strip()
        effect_new = (cleaned.get("effect_new") or "").strip()

        cleaned["mtype_new"] = mtype_new
        cleaned["effect_new"] = effect_new

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        cd = self.cleaned_data
        if cd.get("mtype_new"):
            obj.mtype, _ = MedicineType.objects.get_or_create(name=cd["mtype_new"])
        else:
            obj.mtype = cd.get("mtype")

        if cd.get("effect_new"):
            obj.effect, _ = MedicineEffect.objects.get_or_create(name=cd["effect_new"])
        else:
            obj.effect = cd.get("effect")

        if commit:
            obj.save()
        return obj


class DiagnosticHypothesisForm(forms.ModelForm):
    class Meta:
        model = DiagnosticHypothesis
        fields = [
            "main_diagnosis",
            "comorbidities",
            "comment",
        ]
        widgets = {
            "main_diagnosis": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "comorbidities": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
        }

class FoodplanForm(forms.ModelForm):
    template = forms.ModelChoiceField(
        queryset=FoodplanTemplate.objects.all(),
        required=False,
        label="Шаблон протокола"
    )

    class Meta:
        model = Foodplan
        fields = ["template", "title", "subtitle", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 12}),
        }


class FoodplanTemplateForm(forms.ModelForm):
    class Meta:
        model = FoodplanTemplate
        fields = ["title", "subtitle", "text", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 12}),
            "text": forms.Textarea(attrs={"rows": 30}),
        }
