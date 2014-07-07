from decimal import Decimal

from django import template

from numbles.ledger.models import Account

register = template.Library()


@register.inclusion_tag('ledger/account_list.html', takes_context=True)
def account_list(context):
    return {
        'accounts': Account.objects.filter(user=context['user']),
    }


@register.simple_tag(takes_context=True)
def accumulate(context, name, value):
    if name not in context:
        context[name] = Decimal('0.00')
    context[name] += value
    return context[name]
