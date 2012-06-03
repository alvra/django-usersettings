from django import forms
from base import Setting
from registry import register
from functions import getsetting, setsetting, getsettings, setsettings


class SettingsForm(forms.Form):
    settings = NotImplemented

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['initial'] = getsettings(user, [s.name for s in self.settings])
        super(SettingsForm, self).__init__(*args, **kwargs)

    def save(self):
        updates = {}
        # it could just be that the self.settings list
        # does not match the posted data (server restart with new settings)
        # in that case, only save the ones that were posted,
        # the form is valid anyways
        setsettings(self.user, self.cleaned_data)


def get_settings_form(settings):
    setting_objects = []
    for s in settings:
        if isinstance(s, Setting):
            setting_objects.append(s)
        elif isinstance(s, basestring):
            setting_objects.append(register.get(s))
        else:
            raise TypeError

    fields = {}
    for setting in settings:
        field = setting.formfield()
        if not field.help_text and setting.description:
            field.help_text = setting.description
        fields[setting.name] = field

    fields['settings'] = settings

    return type(
        'CustomSettingsForm',
        (SettingsForm,),
        fields,
    )
