from django import template

register = template.Library()


@register.filter(name='range')
def filter_range(start, end=None):
    if end is None:
        return range(start)
    else:
        return range(start, end)
