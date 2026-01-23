from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import make_aware
from form.models import LabEntry, LabKind
from form.models import (Biochemistry, ProteinMetabolism, LipidMetabolism, CarbohydrateMetabolism,
    IronMetabolism, Micronutrients, InflammatoryMarkers, AllergiesInfections, ThyroidFunction,
    Hematology, Platelets, Leukocytes, HormonalLevels)


class Command(BaseCommand):
    help = "Create EntryLab records for existing entry models"
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
        updated_labs_total = 0
        qs = LabEntry.objects.all()
        self.stdout.write(self.style.SUCCESS(f"Total entries cont: {LabEntry.objects.count()}"))
        for le in qs.iterator():
            obj = le.content_type.model_class().objects.get(pk = le.object_id)
            obj.entry = le
            obj.save(update_fields=["entry"])
            updated_labs_total += 1
            self.stdout.write(self.style.SUCCESS(f"Currently updated labs:{updated_labs_total}"))
        self.stdout.write(self.style.SUCCESS(f"Total updated labs:{updated_labs_total}"))

