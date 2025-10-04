from django import forms

from .models import *

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
