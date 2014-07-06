from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.shortcuts import redirect
from django.template.response import SimpleTemplateResponse

def login_(request, **kwargs):
    """Adds template variables to the login view."""
    response = login(request, **kwargs)
    if isinstance(response, SimpleTemplateResponse):
        response.context_data.update({
            'title': 'Login',
            'fullscreen': True,
        })
    return response

urlpatterns = patterns('numbles.accounts.views',

    url(r'^login/$', login_, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page':'accounts:login'}, name='logout'),
)