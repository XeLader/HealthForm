from django.db import migrations

INSP_SKIN = {
    "CLN":"чистые, без высыпаний",
    "DRY":"сухость",
    "PAL":"бледность",
    "PIG":"гиперпигментация",
    "JAN":"желтушность",
    "EDM":"чёрный акантоз",
    "NON":"-",
    }

INSP_ABDOMEN = {
    "SFT":"мягкий",
    "MTN":"умеренно напряжённый",
    "TNS":"напряжённый",
    "BLT":"вздутие",
    "NPN":"безболезненный",
    "PNF":"болезненный",
    "SAV":"перистальтика сохранена",
    "WEA":"перистальтика ослаблена",
    "ABS":"перистальтика отсутствует",
    "NON":"-",
    }

INSP_TUNG = {
    "PLQ":"налёт",
    "MRK":"отпчетки зубов",
    "GEO":"географический язык",
    "CLR":"цвет",
    }

def forwards_func(apps, schema_editor):
    SkinInspectOption = apps.get_model("form", "SkinInspectOption")
    AbdomenInspectOption = apps.get_model("form", "AbdomenInspectOption")
    TongueInspectOption = apps.get_model("form", "TongueInspectOption")
    Report = apps.get_model("form", "Report")

    code_to_obj_abdm = {}
    for code, label in INSP_SKIN.items():
        obj, created = SkinInspectOption.objects.get_or_create(
            code=code,
            defaults={"label": label},
        )
        if not created and obj.label != label:
            obj.label = label
            obj.save(update_fields=["label"])

    for code, label in INSP_ABDOMEN.items():
        obj, created = AbdomenInspectOption.objects.get_or_create(
            code=code,
            defaults={"label": label},
        )
        if not created and obj.label != label:
            obj.label = label
            obj.save(update_fields=["label"])
        code_to_obj_abdm[code] = obj

    for code, label in INSP_TUNG.items():
        obj, created = TongueInspectOption.objects.get_or_create(
            code=code,
            defaults={"label": label},
        )
        if not created and obj.label != label:
            obj.label = label
            obj.save(update_fields=["label"])


    for report in Report.objects.all():
        code = report.insp_Abdomen
        if not code:
            continue
        if code == "NON":
            continue
        opt = code_to_obj_abdm.get(code)
        if opt is not None:
            report.insp_abdomen.add(opt)


def backwards_func(apps, schema_editor):

    SkinInspectOption  = apps.get_model("form", "SkinInspectOption")
    AbdomenInspectOption = apps.get_model("form", "AbdomenInspectOption")
    TongueInspectOption = apps.get_model("form", "TongueInspectOption")
    Report = apps.get_model("form", "Report")


    for report in Report.objects.all():
        opts = list(report.insp_abdomen.all())
        if opts:
            report.insp_Abdomen = opts[0].code
        else:
            report.insp_Abdomen = "NON"


        report.save(update_fields=["insp_Abdomen"])





class Migration(migrations.Migration):

    dependencies = [
        ('form', '0022_abdomeninspectoption_heredityoption_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
