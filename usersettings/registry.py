from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _, ugettext_lazy
from base import SettingsRegister, Setting, PickledSetting





register = SettingsRegister()



class StyleSetting(Setting):
    name = 'display_style'
    group = 'appearence'
    description = ugettext_lazy('The style to display the pages of this site in.')
    def decode(self, value):
        # checking because a deletion of a style could lead to errors
        # if the style still appears as a setting in the database
        if value in settings.TEMPLATE_STYLE_NAMES:
            return value
        else:
            return self.default()
    def encode(self, value):
        if value in settings.TEMPLATE_STYLE_NAMES:
            return value
        else:
            return None
    def default(self):
        return settings.TEMPLATE_STYLE_NAMES[0]

    def formfields(self, value):
        kwargs = dict(
            label = _('Style'),
            help_text = self.description,
        )
        if value:
            kwargs['initial'] = value
        return dict(
            value = forms.ChoiceField(choices=((n,n) for n in settings.TEMPLATE_STYLE_NAMES), **kwargs),
        )
    def value_from_form_data(self, value):
        return value['value']

class DateTimeSetting(Setting):
    name = 'format_datetime'
    group = 'formatting'
    description = ugettext_lazy('The formatting of datetimes.')
    def decode(self, value):
        return value
    def encode(self, value):
        return value
    def default(self):
        return '%a %b %d, %Y %H:%M:%S %z'

    def formfields(self, value):
        kwargs = dict(
            label = _('Datetime formatting'),
            help_text = self.description,
        )
        if value:
            kwargs['initial'] = value
        return dict(
            value = forms.CharField(**kwargs),
        )
    def value_from_form_data(self, value):
        return value['value']

class DateSetting(Setting):
    name = 'format_date'
    group = 'formatting'
    description = ugettext_lazy('The formatting of dates.')
    def decode(self, value):
        return value
    def encode(self, value):
        return value
    def default(self):
        return '%a %b %d, %Y'

    def formfields(self, value):
        kwargs = dict(
            label = _('Date formatting'),
            help_text = self.description,
        )
        if value:
            kwargs['initial'] = value
        return dict(
            value = forms.CharField(**kwargs),
        )
    def value_from_form_data(self, value):
        return value['value']

class TimeSetting(Setting):
    name = 'format_time'
    group = 'formatting'
    description = ugettext_lazy('The formatting of times.')
    def decode(self, value):
        return value
    def encode(self, value):
        return value
    def default(self):
        return '%H:%M:%S %z'

    def formfields(self, value):
        kwargs = dict(
            label = _('Time formatting'),
            help_text = self.description,
        )
        if value:
            kwargs['initial'] = value
        return dict(
            value = forms.CharField(**kwargs),
        )
    def value_from_form_data(self, value):
        return value['value']
    
class FilesizeSetting(Setting):
    name = 'format_filesize'
    group = 'formatting'
    description = ugettext_lazy('The formatting of filesizes.')
    def decode(self, value):
        return value
    def encode(self, value):
        return value
    def default(self):
        return '1'

    def formfields(self, value):
        kwargs = dict(
            label = _('Filesize formatting'),
            help_text = self.description,
        )
        if value:
            kwargs['initial'] = value
        return dict(
            value = forms.CharField(**kwargs),
        )
    def value_from_form_data(self, value):
        return value['value']





register.register_all(
    StyleSetting(),
    DateTimeSetting(),
    DateSetting(),
    TimeSetting(),
    FilesizeSetting(),
)


