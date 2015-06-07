"""
Customize the Jinja2 environment
"""

from __future__ import absolute_import
from hashlib import md5

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment


def environment(**kwargs):
    """
    Add some utility functions to the Jinja2 environment
    """
    env = Environment(**kwargs)
    env.globals.update({
        'md5': lambda x: md5(x).hexdigest(),
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
