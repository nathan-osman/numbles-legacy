from django import template

from numbles.ledger.models import Account

register = template.Library()


@register.inclusion_tag('ledger/account_list.html', takes_context=True)
def account_list(context):
    return {
        'accounts': Account.objects.filter(user=context['user']),
    }
