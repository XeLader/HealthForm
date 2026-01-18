# yourapp/signals.py
from __future__ import annotations

from typing import Dict, Type

from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import LabEntry, LabKind

# Импортируй ВСЕ модели анализов:
from .models import (
    Biochemistry,
    ProteinMetabolism,
    LipidMetabolism,
    CarbohydrateMetabolism,
    IronMetabolism,
    Micronutrients,
    InflammatoryMarkers,
    AllergiesInfections,
    ThyroidFunction,
    Hematology,
    Platelets,
    Leukocytes,
    HormonalLevels,
)

LAB_MODEL_KIND: Dict[Type, str] = {
    Biochemistry: LabKind.BIOCHEM,
    ProteinMetabolism: LabKind.PROTEIN,
    LipidMetabolism: LabKind.LIPID,
    CarbohydrateMetabolism: LabKind.CARB,
    IronMetabolism: LabKind.IRON,
    Micronutrients: LabKind.MICRO,
    InflammatoryMarkers: LabKind.INFLAMM,
    AllergiesInfections: LabKind.ALLERGY,
    ThyroidFunction: LabKind.THYROID,
    Hematology: LabKind.HEMAT,
    Platelets: LabKind.PLATELET,
    Leukocytes: LabKind.LEUKO,
    HormonalLevels: LabKind.HORMON,
}

_CT_CACHE: Dict[Type, ContentType] = {}


def _get_ct(model_cls: Type) -> ContentType:
    ct = _CT_CACHE.get(model_cls)
    if ct is None:
        ct = ContentType.objects.get_for_model(model_cls)
        _CT_CACHE[model_cls] = ct
    return ct


def _taken_at(instance) -> timezone.datetime:
    return getattr(instance, "created_date", None) or timezone.now()


def _sync_lab_entry(instance, kind: str) -> None:
    model_cls = instance.__class__
    ct = _get_ct(model_cls)

    LabEntry.objects.update_or_create(
        content_type=ct,
        object_id=instance.pk,
        defaults={
            "patient": instance.patient,
            "kind": kind,
            "taken_at": _taken_at(instance),
        },
    )


def _delete_lab_entry(instance) -> None:
    model_cls = instance.__class__
    ct = _get_ct(model_cls)

    LabEntry.objects.filter(content_type=ct, object_id=instance.pk).delete()


def _post_save_handler(sender, instance, **kwargs):
    kind = LAB_MODEL_KIND.get(sender)
    if not kind:
        return
    _sync_lab_entry(instance, kind)


def _post_delete_handler(sender, instance, **kwargs):
    if sender not in LAB_MODEL_KIND:
        return
    _delete_lab_entry(instance)


def connect_lab_signals() -> None:

    for model_cls in LAB_MODEL_KIND.keys():
        post_save.connect(
            _post_save_handler,
            sender=model_cls,
            dispatch_uid=f"labentry_post_save_{model_cls.__name__}",
        )
        post_delete.connect(
            _post_delete_handler,
            sender=model_cls,
            dispatch_uid=f"labentry_post_delete_{model_cls.__name__}",
        )

