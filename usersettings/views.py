from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from ..views.shortview import render_request_to_response
from registry import register
from formgen import get_settings_form





@login_required
def index(request):
    if request.method == 'POST':
        form = get_settings_form(request.user, request.POST)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse('settings:index'))
    else:
        form = get_settings_form(request.user)

    return render(
        request,
        'settings/index.html',
        dict(
            form = form,
        ),
    )



