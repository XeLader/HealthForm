from django.db import models
from django.conf import settings
from django.utils import timezone

from .models import Patient
from .medicine import Medicine
from .labs import *

class LymphInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра лимфоузлов"
        verbose_name_plural = "Опции осмотра лимфоузлов"

    def __str__(self):
        return self.label
        
class SkinInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра кожи и слизистых"
        verbose_name_plural = "Опции осмотра кожи и слизистых"

    def __str__(self):
        return self.label
        
        
class ThyroidInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра щитовидной железы"
        verbose_name_plural = "Опции осмотра щитовидной железы"

    def __str__(self):
        return self.label
        
        
class MuscoskeletalInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра опорно‑двигательного аппарата"
        verbose_name_plural = "Опции осмотра опорно‑двигательного аппарата"

    def __str__(self):
        return self.label


class AbdomenInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра живота"
        verbose_name_plural = "Опции осмотра живота"

    def __str__(self):
        return self.label


class TongueInspectOption(models.Model):
    code = models.CharField(max_length=3, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опция осмотра языка"
        verbose_name_plural = "Опции осмотра языка"

    def __str__(self):
        return self.label

class HeredityOption(models.Model):
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Наследственное заболевание"
        verbose_name_plural = "Наследственные заболевания"

    def __str__(self):
        return self.label


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    regime = models.CharField(verbose_name = "Режим", max_length=200)
    duration = models.CharField(verbose_name = "Длительность", max_length = 200, null=True)
    comment = models.TextField(verbose_name = "Комментариий", null=True, blank=True)
    created_at = models.DateField(verbose_name = "Дата",default=timezone.now)

    class Meta:
        verbose_name = "Нутрицевтическая коррекция"
        verbose_name_plural = "Нутрицевтические коррекции"

    def __str__(self):
        return  self.medicine.title


class Report(models.Model):
    NUTR_TYPE = {
    "MEAT":"преимущественно мясной",
    "PLANT":"преимущественно растительный",
    "VEG":"вегатарианский",
    "LOWCARB":"низкоуглеводный",
    "KET":"кетогенный",
    "RAW":"сыроедение",
    "OTHER":"другое",
    }

    SNACK_OFT = {
    "N":"нет",
    "R":"редко",
    "O":"несколько раз в день",
    }

    PREFS = {
    "MEAT":"мясо",
    "FISH":"рыба",
    "DAIR":"молочные продукты",
    "EGGS":"яйца",
    "VEGS":"овощи",
    "FRUT":"фрукты",
    "GROA":"крупы",
    "SWET":"сладкое",
    "FAST":"фаст-фуд",
    "COFE":"напитки с кофе",
    "ALCO":"алкоголь",
    }

    YNU = {
    "Y":"да",
    "N":"нет",
    "U":"неизвестно",
    }

    INSP_GEN = {
    "SAT":"удовлетворительно",
    "MOD":"среденей тяжести",
    "SEV":"тяжёлое",
    "NON":"-",
    }

    INSP_BODY = {
    "AST":"астеническое",
    "NRM":"нормостеническое",
    "HYP":"гиперстеническое",
    "NON":"-",
    }

    INSP_SKIN = {
    "CLN":"чистые, без высыпаний",
    "DRY":"сухость",
    "PAL":"бледность",
    "PIG":"гиперпигментация",
    "JAN":"желтушность",
    "EDM":"чёрный акантоз",
    "NON":"-",
    }

    INSP_LYMP_THYR = {
    "NRM":"не увеличены",
    "PAL":"пальпируются",
    "PNF":"болезненны",
    "PNL":"безболезненны",
    "NON":"-",
    }

    INSP_ABDOMEN = {
    "SFT":"мягкий",
    "MTN":"умеренно напряжённый",
    "TNS":"напряжённый",
    "BLT":"вздутие",
    "NPN":"безболезненный",
    "PNF":"болезненный",
    "SAV":"перистальтика сохранена",
    "WEA":"перистальтика ослаблена",
    "ABS":"перистальтика отсутствует",
    "NON":"-",
    }

    INSP_LIVER = {
    "NRM":"не увеличена",
    "PRO":"выступает из подреберья",
    "NON":"-",
    }

    INSP_MUSC = {
    "NRM":"суставы без деформаций",
    "PAI":"отмечаются боли",
    "LMT":"ограничение движений",
    "EDE":"отёк",
    "NON":"-",
    }

    INSP_TUNG = {
    "PLQ":"налёт",
    "MRK":"отпчетки зубов",
    "GEO":"географический язык",
    "CLR":"цвет",
    }

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    complaints = models.CharField("Жалобы", max_length=1000)
    anamnesis = models.CharField("Анамнез заболевания", max_length=1000)
    diet = models.CharField(verbose_name = "Тип питания", max_length=7, choices=NUTR_TYPE)
    mealscount = models.IntegerField(verbose_name = "Количество приёмов пищи в день")
    snacks = models.CharField(verbose_name = "Перекусы", max_length=1, choices=SNACK_OFT)
    #Preferable diet
    pref_Meat = models.BooleanField("мясо")
    pref_Fish = models.BooleanField("рыба") 
    pref_Dair = models.BooleanField("молочные продукты")
    pref_Eggs = models.BooleanField("яйца")
    pref_Vegs = models.BooleanField("овощи")
    pref_Frut = models.BooleanField("фрукты")
    pref_Groa = models.BooleanField("крупы")
    pref_Swet = models.BooleanField("сладкое")
    pref_Fast = models.BooleanField("фаст-фуд")
    pref_Cofe = models.BooleanField("напистки с кофе")
    pref_Alco = models.BooleanField("алкоголь")

    #Intolerances
    intol_Lact = models.BooleanField("лактоза")
    intol_Glut = models.BooleanField("глютен")
    intol_Nuts = models.BooleanField("орехи")
    intol_Sea = models.BooleanField("морепродукты")
    intol_Other = models.CharField("другое", max_length = 100)

    #Diet comment
    comment_diet = models.CharField(verbose_name = "Комментарий", max_length = 300, null=True)

    #Heredity
    cardiovascular = models.CharField(verbose_name = "Сердечно‑сосудистые заболевания", max_length=1, choices=YNU)
    cardiovascular_label = models.OneToOneField(HeredityOption, on_delete=models.CASCADE, null=True, related_name = "cardiovascular+")

    oncological = models.CharField(verbose_name = "Онкологические заболевания", max_length=1, choices=YNU)
    oncological_label = models.OneToOneField(HeredityOption, on_delete=models.CASCADE, null=True,  related_name = "oncological+")

    diabetes = models.CharField(verbose_name = "Диабет", max_length=1, choices=YNU)
    diabetes_label = models.OneToOneField(HeredityOption, on_delete=models.CASCADE, null=True,  related_name = "diabetes+")

    thyroid = models.CharField(verbose_name = "Заболевания щитовидной железы", max_length=1, choices=YNU)
    thyroid_label = models.OneToOneField(HeredityOption, on_delete=models.CASCADE, null=True,  related_name = "thyroid+")

    autoimmune = models.CharField(verbose_name = "Аутоиммунные заболевания", max_length=1, choices=YNU)
    autoimmune_label = models.OneToOneField(HeredityOption, on_delete=models.CASCADE, null=True,  related_name = "autoimmune+")

    heredity_Other = models.CharField("другое", max_length = 100, blank=True)

    #Allergies
    foodAllergy = models.CharField("Пищевая аллергия", max_length=150)
    medicineAllergy = models.CharField("Медикаментозная аллергия", max_length=150)
    seasonalAllergy = models.CharField("Сезонная аллергия", max_length=150)
    contactAllergy = models.CharField("Контактная аллергия", max_length=150)
    noAllergy = models.CharField("Отсутствие аллергии", max_length=150)

    #Inspection data
    insp_General = models.CharField("Общее состояние пациента", max_length=3, choices=INSP_GEN, default = "NON")
    insp_Body = models.CharField("Телосложение", max_length=3, choices=INSP_BODY, default = "NON")
    
    insp_Skin = models.CharField("Кожа и слизистые", max_length=3, choices=INSP_SKIN, default = "NON")
    
    insp_skin = models.ManyToManyField(
        SkinInspectOption,
        verbose_name = "Кожа и слизистые",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )
    
    insp_Swelling = models.CharField("Отёки", max_length=300, blank=True)
    insp_Muscle = models.CharField("Мышечный тонус", max_length=300, blank=True)

    insp_Tongue = models.ManyToManyField(
        TongueInspectOption,
        verbose_name = "Язык",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )

    
    insp_Lymph = models.CharField("Лимфатические узлы", max_length=3, choices=INSP_LYMP_THYR, default = "NON")
    
    insp_lymph = models.ManyToManyField(
        LymphInspectOption,
        verbose_name = "Лимфатические узлы",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )

    
    insp_Thyroid = models.CharField("Щитовидная железа", max_length=3, choices=INSP_LYMP_THYR, default = "NON")
    
    insp_thyroid = models.ManyToManyField(
        ThyroidInspectOption,
        verbose_name = "Щитовидная железа",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )
    
    insp_Abdomen = models.CharField("Живот", max_length=3, choices=INSP_ABDOMEN, default = "NON")
    insp_abdomen = models.ManyToManyField(
        AbdomenInspectOption,
        verbose_name = "Живот",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )
    
    
    insp_Liver = models.CharField("Печень", max_length=3, choices=INSP_LIVER, default = "NON")
    insp_Liver_protudes = models.FloatField("Печень выступает на", default = 0.0)
    
    insp_Musculoskeletal = models.CharField("Опорно‑двигательный аппарат", max_length=3, choices=INSP_MUSC, default = "NON")
    
    insp_musculoskeletal = models.ManyToManyField(
        MuscoskeletalInspectOption,
        verbose_name = "Опорно‑двигательный аппарат",
        related_name="reports",
        blank=True,
        help_text="Можно выбрать несколько состояний"
    )
    
    insp_Limbs = models.CharField("Стопы, ладони, локти, ногти, волосы:", max_length = 150, default = "")
    insp_Other = models.CharField("Прочее:", max_length = 150, default = "")

    #Life Style
    life_physAct = models.CharField(verbose_name = "Физическая активность", max_length=200, null=True)
    life_sleepMode = models.CharField(verbose_name = "Режим сна", max_length=200, null=True)
    life_stress = models.CharField(verbose_name = "Наличие стресса", max_length=200, null=True)
    life_antibiotics = models.CharField(verbose_name = "Последний приём антибиотиков", max_length=200, null=True)
    life_covid = models.BooleanField(verbose_name = "COVID-19", default = False)
    life_vaccinationDate = models.DateTimeField(verbose_name = "Дата вакцинации", null=True)

    title = models.CharField(verbose_name = "Название", max_length=200)
    text = models.TextField(verbose_name = "Комментарий")
    created_date = models.DateTimeField(default=timezone.now)
    next_date = models.DateTimeField(default=timezone.now, verbose_name = "Следующий приём")
    def __str__(self):
        return self.title
 
