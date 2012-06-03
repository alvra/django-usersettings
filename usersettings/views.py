from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from registry import register
from formgen import get_settings_form
from functions import getsetting, getsettings, setsetting


class Group(object):
    def __init__(self, name):
        self.name = name

    def get_absolute_url(self):
        return reverse('usersettings:group', kwargs=dict(group=self.name), current_app='usersettings')


def list_groups(request):
    return render(
        request,
        'usersettings/list_groups.html',
        dict(
            groups=(Group(n) for n in register.groups()),
        ),
        current_app='usersettings',
    )


def view_group(request, group):
    setting_objects = register.in_group(group)
    setting_names = (s.name for s in setting_objects)
    settings = getsettings(request.user, setting_names)
    form_type = get_settings_form(setting_objects)
    if request.method == 'POST':
        form = form_type(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = form_type(request.user)
    return render(
        request,
        'usersettings/view_group.html',
        dict(
            group=group,
            form=form,
        ),
        current_app='usersettings',
    )
