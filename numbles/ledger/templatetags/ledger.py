from django import template

from numbles.ledger.models import Account

register = template.Library()


@register.inclusion_tag('ledger/account_list.html')
def account_list():
    return {
        'accounts': Account.objects.all()
    }
