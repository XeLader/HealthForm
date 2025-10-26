import json
from django.core.management.base import BaseCommand
from form.models import QuestionnaireTemplate, SectionTemplate, QuestionTemplate

class Command(BaseCommand):
    help = "Импорт анкеты-шаблона из JSON"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="Путь к JSON-файлу")

    def handle(self, path, *args, **options):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tmpl, _ = QuestionnaireTemplate.objects.get_or_create(
            code=data["code"], defaults={"title": data["title"]})

        # апдейт названия, если изменилось
        if tmpl.title != data["title"]:
            tmpl.title = data["title"]; tmpl.save(update_fields=["title"])
        for p in data["parts"]:
            order_s = 0
            for s in p["sections"]:
                order_s += 1
                section_title = p["title"] + ' ' + s["title"]
                section, _ = SectionTemplate.objects.get_or_create(
                    template=tmpl, order=order_s, defaults={"title": section_title})
                if section.title != section_title:
                    section.title = section_title; section.save(update_fields=["title"])
                order = 0
                for q in s["questions"]:
                    order += 1 
                    qt, _ = QuestionTemplate.objects.get_or_create(
                        section=section, code=q["id"],
                        defaults={"order": order, "text": q["text"], "scale": q.get("options", "0148")}
                    )
                    
                    changed = False
                    if qt.order != order:
                        qt.order = order; changed = True
                    if qt.text != q["text"]:
                        qt.text = q["text"]; changed = True
                    if qt.scale != q.get("options", "0148"):
                        qt.scale = q.get("options", "0148"); changed = True
                    if changed:
                        qt.save(update_fields=["order", "text", "scale"])
                

        self.stdout.write(self.style.SUCCESS(f"Импортирован шаблон {tmpl.code}"))
