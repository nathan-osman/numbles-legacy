"""
Customize the Jinja2 environment
"""

from __future__ import absolute_import

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment


def environment(**kwargs):
    """
    Add the static() and url() functions to the Jinja2 environment
    """
    env = Environment(**kwargs)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
