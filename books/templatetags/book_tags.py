from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def params_send(context, **kwargs):
    params = context['request'].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()