from django import forms
from registry import register
from functions import getsetting, setsetting, get_all_settings





def form_save_method(self, user):
    # TODO: limit the amount of queries this makes
    field_values = {}
    k = self.cleaned_data
    for fieldname,field in self.fields.iteritems():
        key = fieldname[len(field._setting.name)+1:]
        if field._setting in field_values:
            field_values[field._setting][key] = self.cleaned_data[fieldname]
        else:
            field_values[field._setting] = {key:self.cleaned_data[fieldname]}
    for setting,value in field_values.iteritems():
        setsetting(user, setting.name, setting.value_from_form_data(value))



def get_settings_form(user, POST={}):
    fields = {}
    if POST:
        for setting in register.settings():
            for k,v in setting.formfields(None).iteritems():
                v._setting = setting
                fields['%s_%s'%(setting.name,k)] = v
    else:
        all_settings = get_all_settings(user)
        for setting in register.settings():
            formfields = setting.formfields(all_settings[setting.name])
            for k,v in formfields.iteritems():
                v._setting = setting
                fields['%s_%s'%(setting.name,k)] = v
    fields['save'] = lambda self: form_save_method(self, user)
    form_type = type(
        'SettingsForm',
        (forms.Form,),
        fields,
    )
    if POST:
        return form_type(POST)
    else:
        return form_type()



