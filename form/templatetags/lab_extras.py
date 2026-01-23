from django import template

register = template.Library()

SKIP_FIELDS = {
    "id", "pk",
    "patient",
    "created_date", "taken_at",
    "author", "report", "entry"
}

@register.filter
def lab_kv(obj):
    if obj is None:
        return []

    out = []
    for f in obj._meta.fields:
        name = f.name
        if name in SKIP_FIELDS:
            continue

        value = getattr(obj, name, None)
        if value in (None, "", 0):
            continue

        if getattr(f, "choices", None):
            try:
                value = getattr(obj, f"get_{name}_display")()
            except Exception:
                pass

        out.append((f.verbose_name or name, value))
    return out

