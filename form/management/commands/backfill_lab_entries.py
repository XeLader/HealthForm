from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import make_aware
from form.models import LabEntry, LabKind
from form.models import (Biochemistry, ProteinMetabolism, LipidMetabolism, CarbohydrateMetabolism,
    IronMetabolism, Micronutrients, InflammatoryMarkers, AllergiesInfections, ThyroidFunction,
    Hematology, Platelets, Leukocytes, HormonalLevels)


class Command(BaseCommand):
    help = "Create LabEntry records for existing lab models"
    def handle(self, *args, **options):
        mapping = [
            (LabKind.BIOCHEM, Biochemistry),
            (LabKind.PROTEIN, ProteinMetabolism),
            (LabKind.LIPID, LipidMetabolism),
            (LabKind.CARB, CarbohydrateMetabolism),
            (LabKind.IRON, IronMetabolism),
            (LabKind.MICRO, Micronutrients),
            (LabKind.INFLAMM, InflammatoryMarkers),
            (LabKind.ALLERGY, AllergiesInfections),
            (LabKind.THYROID, ThyroidFunction),
            (LabKind.HEMAT, Hematology),
            (LabKind.PLATELET, Platelets),
            (LabKind.LEUKO, Leukocytes),
            (LabKind.HORMON, HormonalLevels),
        ]

        created_total = 0

        for kind, model in mapping:
            ct = ContentType.objects.get_for_model(model)

            qs = model.objects.all().select_related("patient")
            for obj in qs.iterator():
                taken_at = getattr(obj, "created_date", None) or getattr(obj, "taken_at", None) or obj.pk
                if not hasattr(taken_at, "year"):
                    taken_at = obj.created_date if hasattr(obj, "created_date") else None

                defaults = {
                    "patient": obj.patient,
                    "kind": kind,
                    "taken_at": getattr(obj, "created_date", None) or timezone.now(),
                }

                le, created = LabEntry.objects.get_or_create(
                    content_type=ct,
                    object_id=obj.pk,
                    defaults=defaults,
                )
                if created:
                    created_total += 1

            self.stdout.write(self.style.SUCCESS(f"{model.__name__}: done"))

        self.stdout.write(self.style.SUCCESS(f"Total created: {created_total}"))

