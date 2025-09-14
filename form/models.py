from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Patient(models.Model):
	full_name = models.CharField("Ф.И.О.", max_length=150)
	growth = models.IntegerField()
	weight = models.DecimalField(max_digits = 10, decimal_places=3)


class Biochemistry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    alat = models.DecimalField(max_digits = 10, decimal_places=7)
    asat = models.DecimalField(max_digits = 10, decimal_places=7)
    ldh = models.DecimalField(max_digits = 10, decimal_places=7)
    cpk = models.DecimalField(max_digits = 10, decimal_places=7)


class Medicine(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Prescription(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=200)
    regime = models.CharField(max_length=200)
    duration = models.CharField(max_length = 200)
    comment = models.TextField()


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
    "FISH":"руба",
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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    complaints = models.CharField("Жалобы", max_length=1000)
    anamnesis = models.CharField("Анамнез", max_length=1000)
    diet = models.CharField(max_length=7, choices=NUTR_TYPE)
    mealscount = models.IntegerField()
    snacks = models.CharField(max_length=1, choices=SNACK_OFT)
    preference = models.CharField(max_length=4, choices=PREFS)
    cardiovascular = models.CharField(max_length=1, choices=YNU)
    oncological = models.CharField(max_length=1, choices=YNU)
    diabetes = models.CharField(max_length=1, choices=YNU)
    thyroid = models.CharField(max_length=1, choices=YNU)
    autoimmune = models.CharField(max_length=1, choices=YNU)
    allergic = models.CharField(max_length=1, choices=YNU)

    foodAllergy = models.CharField("Пищевая аллергия", max_length=150)
    medicineAllergy = models.CharField("Медикаментозная аллергия", max_length=150)
    seasonalAllergy = models.CharField("Сезонная аллергия", max_length=150)
    contactAllergy = models.CharField("Контактная аллергия", max_length=150)
    noAllergy = models.CharField("Отсутствие аллергии", max_length=150)

    biochemistry = models.ForeignKey(Biochemistry, on_delete=models.CASCADE)

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    next_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
