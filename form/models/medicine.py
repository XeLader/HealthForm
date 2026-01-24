from django.db import models

class MedicineEffect(models.Model):
    name = models.CharField("Воздействие", max_length=100, unique=True)

    class Meta:
        verbose_name = "Воздействие"
        verbose_name_plural = "Воздействия"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MedicineType(models.Model):
    name = models.CharField("Тип", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Medicine(models.Model):
    title = models.CharField("Название", max_length=200)
    effect = models.ForeignKey(
        MedicineEffect,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="medicines",
        verbose_name="Воздействие",
    )
    mtype = models.ForeignKey(
        MedicineType,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="medicines",
        verbose_name="Тип",
    )
    usage = models.TextField("Применение", blank=True, default="")

    class Meta:
        verbose_name = "Препарат"
        verbose_name_plural = "Препараты"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "effect", "mtype"],
                name="uniq_medicine_name_effect_type"
            )
        ]

    def __str__(self):
        return self.title
