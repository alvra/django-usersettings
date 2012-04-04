from django.conf.urls.defaults import *


urlpatterns = patterns('omesium.meta.usersettings.views',
    url(r'^$', 'index', name="index"),
)
