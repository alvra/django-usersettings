from django.utils.translation import ugettext_lazy as _
from django import forms
from usersettings import Setting, PickledSetting
from usersettings.registry import register  # importing straight from usersettings causes errors on django 1.2.7


class Test1Setting(Setting):
    name = 'test1'
    group = 'first half'
    description = _('Setting for testing purposes')

    def default(self):
        return 'default value'

    def formfield(self):
        return forms.CharField()

register.register(Test1Setting())


class Test2Setting(Setting):
    name = 'test2'
    group = 'first half'
    description = _('Another setting for testing purposes')

    def default(self):
        return 'default'

    def formfield(self):
        return forms.ChoiceField(choices=(
            ('default', _('default')),
            ('1', _('first')),
            ('2', _('second')),
            ('3', _('third')),
            ('4', _('fourth')),
        ))

register.register(Test2Setting())


class Test3Setting(PickledSetting):
    name = 'test3'
    group = 'second half'
    description = _('One more setting for testing purposes')

    def default(self):
        return False

    def formfield(self):
        return forms.BooleanField(required=False)

register.register(Test3Setting())
