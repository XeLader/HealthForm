from django import forms
from django.contrib.auth.models import User
from .models import *
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
    class Meta:
        model = Report
        fields = ('patient', 'title', 'text', 'complaints', 'anamnesis', 'diet', 'mealscount', 'snacks', 'pref_Meat', 'pref_Fish',
        'pref_Dair', 'pref_Eggs', 'pref_Vegs', 'pref_Frut', 'pref_Groa', 'pref_Swet',
        'pref_Fast', 'pref_Cofe', 'pref_Alco', 'intol_Lact', 'intol_Glut' ,'intol_Nuts' ,'intol_Sea' ,'intol_Other',
        'cardiovascular', 'oncological', 'diabetes', 'thyroid', 'autoimmune',
        'allergic', 'foodAllergy', 'medicineAllergy', 'seasonalAllergy', 'contactAllergy', 'noAllergy', 'insp_General', 'insp_Body', 'insp_Skin',
        "insp_lymph", 'insp_Thyroid', 'insp_Abdomen', 'insp_Liver', 'insp_Liver_protudes', 'insp_Musculoskeletal', 'insp_Other',
        'next_date')
        widgets = {
            "insp_lymph": forms.CheckboxSelectMultiple,
        }
        
class ReportFormForPatient(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'text', 'complaints', 'anamnesis', 'diet', 'mealscount', 'snacks', 'pref_Meat', 'pref_Fish',
        'pref_Dair', 'pref_Eggs', 'pref_Vegs', 'pref_Frut', 'pref_Groa', 'pref_Swet',
        'pref_Fast', 'pref_Cofe', 'pref_Alco', 'intol_Lact', 'intol_Glut' ,'intol_Nuts' ,'intol_Sea' ,'intol_Other',
        'cardiovascular', 'oncological', 'diabetes', 'thyroid', 'autoimmune',
        'allergic', 'foodAllergy', 'medicineAllergy', 'seasonalAllergy', 'contactAllergy', 'noAllergy', 'insp_General', 'insp_Body', 'insp_skin',
        'insp_lymph', 'insp_thyroid', 'insp_Abdomen', 'insp_Liver', 'insp_Liver_protudes', 'insp_musculoskeletal', 'insp_Other',
        'next_date')
        
        widgets = {
            "insp_lymph": forms.CheckboxSelectMultiple,
            "insp_thyroid": forms.CheckboxSelectMultiple,
            "insp_skin": forms.CheckboxSelectMultiple,
            "insp_musculoskeletal": forms.CheckboxSelectMultiple,
        }
        
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name',"date_of_birth", "sex", 'growth', 'weight')
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('patient', 'medicine', 'dosage' ,'regime', 'duration')
        
        
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
