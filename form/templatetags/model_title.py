from django import template

register = template.Library()


@register.filter
def model_title(model):
    return model._meta.verbose_name

@register.filter
def model_title_plural(model):
    return model._meta.verbose_name_plural
