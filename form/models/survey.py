import uuid
from django.db import models
from django.utils import timezone

from .models import Patient

class QuestionnaireTemplate(models.Model):
    code = models.CharField(max_length=64, unique=True)
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
    code = models.CharField(max_length=64)
    order = models.PositiveIntegerField()
    text = models.TextField()
    scale = models.CharField(max_length=16, default="0148")
    class Meta:
        unique_together = ("section", "code")


class Questionnaire(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="questionnaires")
    template = models.ForeignKey(QuestionnaireTemplate, on_delete=models.PROTECT)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
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
    score = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("questionnaire", "question")
        indexes = [
            models.Index(fields=["questionnaire"]),
            models.Index(fields=["question"]),
        ]

