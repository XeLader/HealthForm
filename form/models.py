import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class UserInvite(models.Model):
    email = models.EmailField("E-mail ассистента")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    make_staff = models.BooleanField(
        "Сделать сотрудником (доступ в админку/панель)",
        default=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кем создано",
    )

    def mark_used(self):
        self.used = True
        self.used_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Приглашение для {self.email}"

class Patient(models.Model):
    class Sex(models.TextChoices):
        MALE       = "M", "Мужской"
        FEMALE     = "F", "Женский"
        UNKNOWN    = "U", "Не указан"

    full_name = models.CharField("Ф.И.О.", max_length=150, default = "None")
    growth = models.IntegerField("Рост, см", default = 0)
    weight = models.DecimalField("Вес, кг", max_digits = 10, decimal_places=3, default = 0)
    date_of_birth = models.DateField("Дата рождения", blank=True, null=True)
    sex = models.CharField(
        "Пол",
        max_length=2,
        choices=Sex.choices,
        blank=True,
        null=True,
        default="U",
    )
    
    def __str__(self):
	    return self.full_name

class Biochemistry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateField(verbose_name = "Дата",default=timezone.now)
    alat = models.DecimalField(verbose_name = "АлАТ", max_digits = 10, decimal_places=7)
    asat = models.DecimalField(verbose_name = "АсАТ", max_digits = 10, decimal_places=7)
    ldh = models.DecimalField(verbose_name = "ЛДГ", max_digits = 10, decimal_places=7)
    cpk = models.DecimalField(verbose_name = "КФК", max_digits = 10, decimal_places=7)

class ProteinMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    gammaGT = models.DecimalField(verbose_name = "Гамма‑ГТ", max_digits = 10, decimal_places=7)
    ttlProtein = models.DecimalField(verbose_name = "Общий белок", max_digits = 10, decimal_places=7)
    albumin = models.DecimalField(verbose_name = "Альбумин", max_digits = 10, decimal_places=7)
    phosphatase = models.DecimalField(verbose_name = "Щелочная фосфатаза", max_digits = 10, decimal_places=7)
    urea = models.DecimalField(verbose_name = "Мочевина", max_digits = 10, decimal_places=7)
    creatinine = models.DecimalField(verbose_name = "Креатинин", max_digits = 10, decimal_places=7)
    uricAcid = models.DecimalField(verbose_name = "Мочевая кислота", max_digits = 10, decimal_places=7)
    alpha1Globulins = models.DecimalField(verbose_name = "α1‑глобулины", max_digits = 10, decimal_places=7)
    alpha2Globulins = models.DecimalField(verbose_name = "α2‑глобулины", max_digits = 10, decimal_places=7)
    beta1Globulins = models.DecimalField(verbose_name = "β1‑глобулины", max_digits = 10, decimal_places=7)
    beta2Globulins = models.DecimalField(verbose_name = "β2‑глобулины", max_digits = 10, decimal_places=7)
    gammaGlobulins = models.DecimalField(verbose_name = "γ‑глобулины", max_digits = 10, decimal_places=7)

class LipidMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    ttlBilirubin = models.DecimalField(verbose_name = "Общий билирубин", max_digits = 10, decimal_places=7)
    drctBilirubin = models.DecimalField(verbose_name = "Прямой билирубин", max_digits = 10, decimal_places=7)
    indrctBilirubin = models.DecimalField(verbose_name = "Непрямой билирубин", max_digits = 10, decimal_places=7)
    ttlCholesterol = models.DecimalField(verbose_name = "Холестерин общий", max_digits = 10, decimal_places=7)
    LDL = models.DecimalField(verbose_name = "ЛПНП", max_digits = 10, decimal_places=7)
    VLDL = models.DecimalField(verbose_name = "ЛПОНП", max_digits = 10, decimal_places=7)
    HDL = models.DecimalField(verbose_name = "ЛПВП", max_digits = 10, decimal_places=7)
    Triglycerides = models.DecimalField(verbose_name = "Триглицериды", max_digits = 10, decimal_places=7)

class CarbohydrateMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    fastingGlucose = models.DecimalField(verbose_name = "Глюкоза (натощак)", max_digits = 10, decimal_places=7) 
    glycatedHemoglobin = models.DecimalField(verbose_name = "Гликированный гемоглобин", max_digits = 10, decimal_places=7)

class IronMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    serumIron = models.DecimalField(verbose_name = "Сывороточное железо", max_digits = 10, decimal_places=7)
    ferritin = models.DecimalField(verbose_name = "Ферритин", max_digits = 10, decimal_places=7)
    transferrin = models.DecimalField(verbose_name = "Трансферрин", max_digits = 10, decimal_places=7)
    TIBC = models.DecimalField(verbose_name = "ОЖСС", max_digits = 10, decimal_places=7)
    transferrinSat = models.DecimalField(verbose_name = "Насыщение трансферрина", max_digits = 10, decimal_places=7)



class Micronutrients(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    copper = models.DecimalField(verbose_name = "Медь", max_digits = 10, decimal_places=7)
    zinc = models.DecimalField(verbose_name = "Цинк", max_digits = 10, decimal_places=7)
    magnesium = models.DecimalField(verbose_name = "Магний", max_digits = 10, decimal_places=7)
    ttlCalcium = models.DecimalField(verbose_name = "Кальций общий", max_digits = 10, decimal_places=7)
    potassium = models.DecimalField(verbose_name = "Калий", max_digits = 10, decimal_places=7)
    sodium = models.DecimalField(verbose_name = "Натрий", max_digits = 10, decimal_places=7)
    chloride = models.DecimalField(verbose_name = "Хлор", max_digits = 10, decimal_places=7)


class InflammatoryMarkers(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    cReactiveProtein = models.DecimalField(verbose_name = "C‑реактивный белок", max_digits = 10, decimal_places=7)
    fibrinogen = models.DecimalField(verbose_name = "Фибриноген", max_digits = 10, decimal_places=7)
    ASLO = models.DecimalField(verbose_name = "АСЛО", max_digits = 10, decimal_places=7)
    homocysteine = models.DecimalField(verbose_name = "Гомоцистеин", max_digits = 10, decimal_places=7)



class AllergiesInfections(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    ttlIgE = models.DecimalField(verbose_name = "IgE общий", max_digits = 10, decimal_places=7)
    IgA = models.DecimalField(verbose_name = "IgA", max_digits = 10, decimal_places=7)
    IgM = models.DecimalField(verbose_name = "IgM", max_digits = 10, decimal_places=7)
    IgG = models.DecimalField(verbose_name = "IgG", max_digits = 10, decimal_places=7)
    antiCandida = models.DecimalField(verbose_name = "Антитела к Candida", max_digits = 10, decimal_places=7)
    antiAspergillus = models.DecimalField(verbose_name = "Антитела к Aspergillus", max_digits = 10, decimal_places=7)
    antiParasitic = models.DecimalField(verbose_name = "Антитела к паразитам", max_digits = 10, decimal_places=7)




class ThyroidFunction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    TSH = models.DecimalField(verbose_name = "ТТГ", max_digits = 10, decimal_places=7)
    freeT4 = models.DecimalField(verbose_name = "Т4 свободный", max_digits = 10, decimal_places=7)
    freeT3 = models.DecimalField(verbose_name = "Т3 свободный", max_digits = 10, decimal_places=7)
    totalT4 = models.DecimalField(verbose_name = "Т4 общий", max_digits = 10, decimal_places=7)
    totalT3 = models.DecimalField(verbose_name = "Т3 общий", max_digits = 10, decimal_places=7)
    reverseT3 = models.DecimalField(verbose_name = "Реверсивный Т3", max_digits = 10, decimal_places=7)
    TPOAb = models.DecimalField(verbose_name = "АТ к ТПО", max_digits = 10, decimal_places=7)
    TgAb = models.DecimalField(verbose_name = "АТ к ТГ", max_digits = 10, decimal_places=7)


class Hematology(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    hemoglobin = models.DecimalField(verbose_name = "Гемоглобин", max_digits = 10, decimal_places=7)
    hematocrit = models.DecimalField(verbose_name = "Гематокрит", max_digits = 10, decimal_places=7)
    redBloodCells = models.DecimalField(verbose_name = "Эритроциты", max_digits = 10, decimal_places=7)
    MCV = models.DecimalField(verbose_name = "MCV (средний объём)", max_digits = 10, decimal_places=7)
    RDW = models.DecimalField(verbose_name = "RDW (ширина распределения)", max_digits = 10, decimal_places=7)
    MCH = models.DecimalField(verbose_name = "MCH (среднее содержание Hb)", max_digits = 10, decimal_places=7)
    MCHC = models.DecimalField(verbose_name = "MCHC (средняя концентрация Hb)", max_digits = 10, decimal_places=7)


class Platelets(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    platelets = models.DecimalField(verbose_name = "Тромбоциты", max_digits = 10, decimal_places=7)
    MPV = models.DecimalField(verbose_name = "MPV (средний объём тромбоцитов)", max_digits = 10, decimal_places=7)
    PCT = models.DecimalField(verbose_name = "PCT (тромбокрит)", max_digits = 10, decimal_places=7)
    PDW = models.DecimalField(verbose_name = "PDW (ширина распределения)", max_digits = 10, decimal_places=7)


class Leukocytes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    leukocytes = models.DecimalField(verbose_name = "Лейкоциты", max_digits = 10, decimal_places=7)
    neutrophilsPer = models.DecimalField(verbose_name = "Нейтрофилы (%)", max_digits = 10, decimal_places=7)
    neutrophilsAbs = models.DecimalField(verbose_name = "Нейтрофилы (абс.)", max_digits = 10, decimal_places=7)
    lymphocytesPer = models.DecimalField(verbose_name = "Лимфоциты (%)", max_digits = 10, decimal_places=7)
    lymphocytesAbs = models.DecimalField(verbose_name = "Лимфоциты (абс.)", max_digits = 10, decimal_places=7)
    monocytesPer = models.DecimalField(verbose_name = "Моноциты (%)", max_digits = 10, decimal_places=7)
    monocytesAbs = models.DecimalField(verbose_name = "Моноциты (абс.)", max_digits = 10, decimal_places=7)
    eosinophilsPer = models.DecimalField(verbose_name = "Эозинофилы (%)", max_digits = 10, decimal_places=7)
    eosinophilsAbs = models.DecimalField(verbose_name = "Эозинофилы (абс.)", max_digits = 10, decimal_places=7)
    basophilsPer = models.DecimalField(verbose_name = "Базофилы (%)", max_digits = 10, decimal_places=7)
    basophilsAbs = models.DecimalField(verbose_name = "Базофилы (абс.)", max_digits = 10, decimal_places=7)
    ESR = models.DecimalField(verbose_name = "СОЭ", max_digits = 10, decimal_places=7)


class HormonalLevels(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    FSH = models.DecimalField(verbose_name = "ФСГ", max_digits = 10, decimal_places=7)
    LH = models.DecimalField(verbose_name = "ЛГ", max_digits = 10, decimal_places=7)
    estradiol = models.DecimalField(verbose_name = "Эстрадиол", max_digits = 10, decimal_places=7)
    progesterone = models.DecimalField(verbose_name = "Прогестерон", max_digits = 10, decimal_places=7)
    ttlTestosterone = models.DecimalField(verbose_name = "Тестостерон общий", max_digits = 10, decimal_places=7)
    freeTestosterone = models.DecimalField(verbose_name = "Тестостерон общий", max_digits = 10, decimal_places=7)
    DHT = models.DecimalField(verbose_name = "ДГТ", max_digits = 10, decimal_places=7)
    DHEASulfate = models.DecimalField(verbose_name = "ДГЭА-сульфат", max_digits = 10, decimal_places=7)
    SHBG  = models.DecimalField(verbose_name = "ГСПГ", max_digits = 10, decimal_places=7)
    prolactin = models.DecimalField(verbose_name = "Пролактин", max_digits = 10, decimal_places=7)
    PSA = models.DecimalField(verbose_name = "ПСА", max_digits = 10, decimal_places=7)

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

class Medicine(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(verbose_name = "Дозировка", max_length=200)
    regime = models.CharField(verbose_name = "Режим", max_length=200)
    duration = models.CharField(verbose_name = "Длительность", max_length = 200)
    comment = models.TextField(verbose_name = "Комментариий")

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
    "EDM":"отёки",
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
    "TNS":"напряжённый; безболезненный",
    "PNF":"болезненный; перистальтика сохранена",
    "WEA":"ослаблена",
    "ABS":"отсутствует",
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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    complaints = models.CharField("Жалобы", max_length=1000)
    anamnesis = models.CharField("Анамнез", max_length=1000)
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

    #Heredity
    cardiovascular = models.CharField(verbose_name = "Сердечно‑сосудистые заболевания", max_length=1, choices=YNU)
    oncological = models.CharField(verbose_name = "Онкологические заболевания", max_length=1, choices=YNU)
    diabetes = models.CharField(verbose_name = "Онкологические заболевания", max_length=1, choices=YNU)
    thyroid = models.CharField(verbose_name = "Заболевания щитовидной железы", max_length=1, choices=YNU)
    autoimmune = models.CharField(verbose_name = "Аутоиммунные заболевания", max_length=1, choices=YNU)
    allergic = models.CharField(verbose_name = "Аллергические заболевания", max_length=1, choices=YNU)

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
    
    insp_Other = models.CharField("Прочее:", max_length = 150, default = "")

    title = models.CharField(verbose_name = "Название", max_length=200)
    text = models.TextField(verbose_name = "Комментарий")
    created_date = models.DateTimeField(default=timezone.now)
    next_date = models.DateTimeField(default=timezone.now, verbose_name = "Следующий приём")
    def __str__(self):
        return self.title
        
        

class QuestionnaireTemplate(models.Model):
    code = models.CharField(max_length=64, unique=True)  # "v1_2025_10"
    title = models.CharField(max_length=255)

class SectionTemplate(models.Model):
    template = models.ForeignKey(QuestionnaireTemplate, on_delete=models.CASCADE, related_name="sections")
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    low = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

class QuestionTemplate(models.Model):
    section = models.ForeignKey(SectionTemplate, on_delete=models.CASCADE, related_name="questions")
    code = models.CharField(max_length=64)  # "Q1_03"
    order = models.PositiveIntegerField()
    text = models.TextField()
    scale = models.CharField(max_length=16, default="0148")  # "0/1/4/8" или "0/8"
    class Meta:
        unique_together = ("section", "code")


class Questionnaire(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="questionnaires")
    template = models.ForeignKey(QuestionnaireTemplate, on_delete=models.PROTECT)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    #payload = models.JSONField(default=dict, blank=True)  # черновик
    
    def is_valid(self) -> bool:
        if self.submitted_at:
            return False
        return True

    def mark_used(self):
        self.submitted_at = timezone.now()
        self.save(update_fields=["submitted_at"])

class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuestionTemplate, on_delete=models.PROTECT)
    score = models.SmallIntegerField(null=True, blank=True)  # 0/1/4/8 и т.п.

    class Meta:
        unique_together = ("questionnaire", "question")
        indexes = [
            models.Index(fields=["questionnaire"]),
            models.Index(fields=["question"]),
        ]

