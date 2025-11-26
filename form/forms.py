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
        

