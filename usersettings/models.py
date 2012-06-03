from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserSetting(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=20, unique=False)
    value = models.TextField(_('value'))
    user = models.ForeignKey(User, related_name='settings')

    class Meta:
        db_table = 'usersettings'
        unique_together = (("user", "name"),)

admin.site.register(UserSetting)
