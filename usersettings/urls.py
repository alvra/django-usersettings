from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from views import list_groups, view_group


urlpatterns = patterns(
    'usersettings.views',
    url(r'^$', login_required(list_groups), name="index"),
    url(r'^(?P<group>.+)/$', login_required(view_group), name="group"),
)
