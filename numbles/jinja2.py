"""
Customize the Jinja2 environment.
"""

from __future__ import absolute_import
from datetime import timedelta
from hashlib import md5
from os.path import basename

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr
from django.utils.timezone import now, template_localtime
from jinja2 import Environment
from widget_tweaks.templatetags.widget_tweaks import add_class, widget_type


def paginate(queryset, page):
    """
    """
    paginator = Paginator(queryset, 10)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def qs(request, **kwargs):
    """
    Output the query string for the current page with the specified additions
    and/or modifications.
    """
    get = request.GET.copy()
    for k, v in kwargs.items():
        get[k] = v
    return get.urlencode()


def environment(**kwargs):
    """
    Add some utility functions to the Jinja2 environment
    """
    env = Environment(**kwargs)
    env.filters.update({
        'add_class': add_class,
        'widget_type': widget_type,
    })
    env.globals.update({
        'basename': basename,
        'linebreaksbr': linebreaksbr,
        'localtime': lambda x: template_localtime(x).strftime('%Y-%m-%d %H:%M:%S'),
        'md5': lambda x: md5(x).hexdigest(),
        'now': now,
        'paginate': paginate,
        'qs': qs,
        'static': staticfiles_storage.url,
        'timedelta': timedelta,
        'url': reverse,
    })
    return env
