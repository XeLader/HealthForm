import uuid
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone

from .models import Patient

class LabKind(models.TextChoices):
    BIOCHEM = "biochem", "Биохимия"
    PROTEIN = "protein", "Белковый обмен"
    LIPID = "lipid", "Липидный профиль"
    CARB = "carb", "Углеводный обмен"
    IRON = "iron", "Железо/ферритин"
    MICRO = "micro", "Микроэлементы"
    INFLAMM = "inflamm", "Воспаление"
    ALLERGY = "allergy", "Аллергология"
    THYROID = "thyroid", "Щитовидная железа"
    HEMAT = "hemat", "Гематология"
    PLATELET = "platelet", "Тромбоциты"
    LEUKO = "leuko", "Лейкоформула"
    HORMON = "hormon", "Гормоны"

class Biochemistry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateField(verbose_name = "Дата",default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="biochemistry_obj")
    alat = models.DecimalField(verbose_name = "АлАТ", max_digits = 10, decimal_places=7)
    asat = models.DecimalField(verbose_name = "АсАТ", max_digits = 10, decimal_places=7)
    ldh = models.DecimalField(verbose_name = "ЛДГ", max_digits = 10, decimal_places=7)
    cpk = models.DecimalField(verbose_name = "КФК", max_digits = 10, decimal_places=7)

class ProteinMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="protein_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="lipid_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="carbohydrate_obj")
    fastingGlucose = models.DecimalField(verbose_name = "Глюкоза (натощак)", max_digits = 10, decimal_places=7) 
    glycatedHemoglobin = models.DecimalField(verbose_name = "Гликированный гемоглобин", max_digits = 10, decimal_places=7)

class IronMetabolism(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="iron_obj")
    serumIron = models.DecimalField(verbose_name = "Сывороточное железо", max_digits = 10, decimal_places=7)
    ferritin = models.DecimalField(verbose_name = "Ферритин", max_digits = 10, decimal_places=7)
    transferrin = models.DecimalField(verbose_name = "Трансферрин", max_digits = 10, decimal_places=7)
    TIBC = models.DecimalField(verbose_name = "ОЖСС", max_digits = 10, decimal_places=7)
    transferrinSat = models.DecimalField(verbose_name = "Насыщение трансферрина", max_digits = 10, decimal_places=7)



class Micronutrients(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="micronutrients_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="inflammatory_obj")
    cReactiveProtein = models.DecimalField(verbose_name = "C‑реактивный белок", max_digits = 10, decimal_places=7)
    fibrinogen = models.DecimalField(verbose_name = "Фибриноген", max_digits = 10, decimal_places=7)
    ASLO = models.DecimalField(verbose_name = "АСЛО", max_digits = 10, decimal_places=7)
    homocysteine = models.DecimalField(verbose_name = "Гомоцистеин", max_digits = 10, decimal_places=7)



class AllergiesInfections(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="allergies_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="thyroid_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="hematology_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="platelets_obj")
    platelets = models.DecimalField(verbose_name = "Тромбоциты", max_digits = 10, decimal_places=7)
    MPV = models.DecimalField(verbose_name = "MPV (средний объём тромбоцитов)", max_digits = 10, decimal_places=7)
    PCT = models.DecimalField(verbose_name = "PCT (тромбокрит)", max_digits = 10, decimal_places=7)
    PDW = models.DecimalField(verbose_name = "PDW (ширина распределения)", max_digits = 10, decimal_places=7)


class Leukocytes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="leukocytes_obj")
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
    entry = models.OneToOneField("LabEntry", on_delete=models.SET_NULL, null=True, blank=True, related_name="hormonal_obj")
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
    
    
class LabEntry(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="lab_entries")
    kind = models.CharField("Тип анализа", max_length=20, choices=LabKind.choices)

    taken_at = models.DateTimeField("Дата анализа", default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("content_type", "object_id")
        indexes = [
            models.Index(fields=["patient", "-taken_at"]),
            models.Index(fields=["kind", "-taken_at"]),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} — {self.taken_at:%d.%m.%Y}"


class LabDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="lab_documents")
    uploaded_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    file = models.FileField(upload_to="lab_docs/%Y/%m/%d/", verbose_name = "Файл")
    original_name = models.CharField(max_length=255, blank=True, default="")
    note = models.CharField(max_length=255, blank=True, verbose_name = "Замечания", default="")

    entries = models.ManyToManyField("LabEntry", related_name="source_documents", blank=True)

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Заполнен"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f"PDF анализов {self.patient} ({self.created_at:%d.%m.%Y})"
