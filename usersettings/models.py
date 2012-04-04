from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import base64
import cPickle as pickle


class UserSetting(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=20, unique=False)
    value = models.TextField(_('value'))
    user = models.ForeignKey(User, related_name='settings')
    
    class Meta:
        db_table = 'usersettings'
        unique_together = (("user", "name"),)

admin.site.register(UserSetting)


# The setting itself should now deside to use this or not
# not every setting needs this, so it'll save some time
##    def set(self, value=''):
##        """
##        Returns the setting value pickled and encoded as a string.
##        """
##        pickled = pickle.dumps(value)
##        self.value = base64.encodestring(pickled)
##        return True
##
##    def get(self):
##        pickled = base64.decodestring(self.value)
##        try:
##            return pickle.loads(pickled)
##        # Unpickling can cause a variety of exceptions. If something happens,
##        # just return an empty string (Though this will cause a delete for the setting!).
##        except:
##            return None
