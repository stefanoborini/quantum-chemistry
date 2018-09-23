from django import template
from django.template.defaultfilters import stringfilter
from lib import utils

register = template.Library()

@register.filter
@stringfilter
def add_braces(value):
    return "{"+value+"}"

@register.filter
@stringfilter
def uriToUrl(value):
    return "/resources/%7B"+utils.uriToUuid(value)+"%7D"

