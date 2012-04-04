from models import UserSetting
from registry import register





def getsetting(user, name):
    # this makes sure it exists
    setting = register.get(name)
    if user.is_anonymous():
        return setting.default()
    try:
        obj = UserSetting.objects.get(name=name,user=user)
    except UserSetting.DoesNotExist:
        obj = None
    # obj can also be None if dbobj could not be unpickled
    if obj is None:
        return setting.default()
    else:
        value = obj.value
        return setting.decode(value)


def get_all_settings(user):
    if user.is_anonymous():
        return dict((setting.name, setting.default()) for setting in register.settings())
    else:
        values = dict(UserSetting.objects.filter(user=user).values_list('name','value'))
        settings = {}
        for setting in register.settings():
            if setting.name in values:
                settings[setting.name] = setting.decode(values[setting.name])
            else:
                settings[setting.name] = setting.default()
        return settings


def setsetting(user, name, value):
    # this makes sure it exists
    setting = register.get(name)
    encoded = setting.encode(value)
    if encoded is None:
        return False # value could not be encoded, its probaly invalid!
    if value == setting.default():
        # setting is default
        # using filter to avoid problems when setting does not exist
        # TODO: check if 'filter' instead of 'get' is faster
        UserSetting.objects.filter(name=name,user=user).delete()
        return True # succesfully saved (by deleting)
    try:
        obj = UserSetting.objects.get(name=name,user=user)
    except UserSetting.DoesNotExist:
        obj = UserSetting(name=name,user=user,value=encoded)
        obj.save()
    else:
        obj.value = encoded
        obj.save()
    return True # succesfully saved new value



