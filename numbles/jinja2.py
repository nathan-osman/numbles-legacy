"""
Customize the Jinja2 environment
"""

from __future__ import absolute_import
from hashlib import md5

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils.timezone import template_localtime
from jinja2 import Environment
from widget_tweaks.templatetags.widget_tweaks import add_class, widget_type


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
        'localtime': lambda x: template_localtime(x).strftime('%Y-%m-%d %H:%M:%S'),
        'md5': lambda x: md5(x).hexdigest(),
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
