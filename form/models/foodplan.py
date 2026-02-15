from django.db import models
from django.conf import settings
from django.utils import timezone

from .models import Patient

class Foodplan(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default = 0)
    created_date = models.DateTimeField(default=timezone.now)

    title = models.CharField("Название", max_length=100)
    subtitle = models.CharField("Описание", max_length=300, blank=True)

    text = models.TextField("Протокол")

    class Meta:
        verbose_name = "Диетологическая рекомендация"
        verbose_name_plural = "Диетологические рекомендации"

    def __str__(self):
        return f"{self.title}"


class FoodplanTemplate(models.Model):
    title = models.CharField("Название", max_length=100)
    subtitle = models.CharField("Описание", max_length=300, blank=True)

    text = models.TextField("Протокол")
    comment = models.TextField("Комментарий")

    class Meta:
        verbose_name = "Шаблон диетологической рекомендации"
        verbose_name_plural = "Шаблоны диетологических рекомендаций"

    def __str__(self):
        return f"{self.title}"
