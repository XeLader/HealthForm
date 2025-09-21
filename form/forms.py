from django import forms

from .models import Report, Patient, Prescription

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('patient', 'title', 'text', 'complaints', 'anamnesis', 'diet', 'mealscount', 'snacks', 'pref_Meat', 'pref_Fish',
        'pref_Dair', 'pref_Eggs', 'pref_Vegs', 'pref_Frut', 'pref_Groa', 'pref_Swet',
        'pref_Fast', 'pref_Cofe', 'pref_Alco', 'intol_Lact', 'intol_Glut' ,'intol_Nuts' ,'intol_Sea' ,'intol_Other',
        'cardiovascular', 'oncological', 'diabetes', 'thyroid', 'autoimmune',
        'allergic', 'foodAllergy', 'medicineAllergy', 'seasonalAllergy', 'contactAllergy', 'noAllergy', 'insp_General', 'insp_Body', 'insp_Skin',
        'insp_Lymph', 'insp_Thyroid', 'insp_Abdomen', 'insp_Liver', 'insp_Liver_protudes', 'insp_Musculoskeletal', 'insp_Other',
        'next_date')
        
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'growth', 'weight')
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('patient', 'medicine', 'dosage' ,'regime', 'duration')
