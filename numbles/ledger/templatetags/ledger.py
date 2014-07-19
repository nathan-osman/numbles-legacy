from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe

from numbles.ledger.models import Account

register = template.Library()


@register.filter
def currency(value):
    if value > 0:
        return mark_safe('<span class="text-success">$%s</span>' % value)
    elif value == 0:
        return mark_safe('$%s' % value)
    else:
        return mark_safe('<span class="text-danger">-$%s</span>' % abs(value))


@register.inclusion_tag('ledger/account_sidebar.html', takes_context=True)
def account_sidebar(context):
    return {
        'accounts': Account.objects.filter(user=context['user']),
    }


@register.simple_tag(takes_context=True)
def accumulate(context, name, value):
    if name not in context:
        context[name] = Decimal('0.00')
    context[name] += value
    return currency(context[name])
