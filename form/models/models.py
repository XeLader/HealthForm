import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserInvite(models.Model):
    email = models.EmailField("E-mail ассистента")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    make_staff = models.BooleanField(
        "Сделать сотрудником",
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
