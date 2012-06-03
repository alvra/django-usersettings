from models import UserSetting
from registry import register


# TODO: what to do with anonymous users?


def getsetting(user, name):
    # this makes sure it exists
    setting = register.get(name)
    if user.is_anonymous():
        return setting.default()
    try:
        obj = UserSetting.objects.get(name=name, user=user)
    except UserSetting.DoesNotExist:
        return setting.default()
    else:
        return setting.decode(obj.value)


def getsettings(user, only=[]):
    if user.is_anonymous():
        if only:
            return dict((setting.name, setting.default()) for setting in register.settings() if setting.name in only)
        else:
            return dict((setting.name, setting.default()) for setting in register.settings())
    else:
        filters = dict(
            user=user,
        )
        if only:
            filters['name__in'] = only
        values = dict(UserSetting.objects.filter(**filters).values_list('name', 'value'))
        settings = {}
        for setting in register.settings():
            if not only or setting.name in only:
                if setting.name in values:
                    settings[setting.name] = setting.decode(values[setting.name])
                else:
                    settings[setting.name] = setting.default()
        return settings


def setsetting(user, name, value):
    # this makes sure it exists
    setting = register.get(name)
    encoded = setting.encode(value)
    if value == setting.default():
        # setting is default
        # using filter to avoid problems when setting does not exist
        # TODO: check if 'filter' instead of 'get' is faster
        UserSetting.objects.filter(name=name, user=user).delete()
        return True  # succesfully saved (by deleting)
    try:
        # TODO: use update here instead
        obj = UserSetting.objects.get(name=name, user=user)
    except UserSetting.DoesNotExist:
        obj = UserSetting(name=name, user=user, value=encoded)
        obj.save()
    else:
        obj.value = encoded
        obj.save()
    return True  # succesfully saved new value


def setsettings(user, values):
    # only save the values for settings that exist
    existing_settings = [s.name for s in register.settings()]
    values = dict((k, v) for k, v in values.iteritems() if k in existing_settings)
    # TODO: can this be made any faster?
    settings = dict((s.name, s) for s in register.settings() if s.name in values)
    # first delete settings that are set to the default
    default_settings = [n for n in settings.keys() if values[n] == settings[n].default()]
    UserSetting.objects.filter(name__in=default_settings, user=user).delete()
    # then set rest of the settings
    create_settings = []
    for setting in settings.keys():
        if setting not in default_settings:
            changes = UserSetting.objects.filter(name=setting, user=user).update(
                value=settings[setting].encode(values[setting]),
            )
            if not changes:
                create_settings.append(setting)
    # create the settings that could not be updated because they dont exist
    create = []
    for setting in create_settings:
        create.append(UserSetting(
            user=user,
            name=setting,
            value=settings[setting].encode(values[setting]),
        ))
    UserSetting.objects.bulk_create(create)
