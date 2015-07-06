"""
Customize the Jinja2 environment
"""

from __future__ import absolute_import
from hashlib import md5

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment
from widget_tweaks.templatetags.widget_tweaks import add_class


def environment(**kwargs):
    """
    Add some utility functions to the Jinja2 environment
    """
    env = Environment(**kwargs)
    env.filters.update({
        'add_class': add_class,
    })
    env.globals.update({
        'md5': lambda x: md5(x).hexdigest(),
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
