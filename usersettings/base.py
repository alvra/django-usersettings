import base64
import cPickle as pickle





class SettingsRegister(object):
    def __init__(self):
        self._settings = dict()
        self._groups = dict()

    class DoesNotExists(Exception):
        pass
        
    def register(self, setting):
        name = setting.name
        if name in self._settings:
            raise Exception('Trying to register setting %s named %s, that name already exists!'%(setting,name))
        self._settings[name] = setting
        self.addto_group(setting)

    def register_all(self, *settings):
        for s in settings:
            self.register(s)

    def addto_group(self, setting):
        group = setting.group
        name = setting.name
        if group in self._groups:
            self._groups[group].append(setting)
        else:
            self._groups[group] = [setting]

    def get(self, name):
        if name not in self._settings:
            raise self.DoesNotExists(name)
        else:
            return self._settings[name]

    def settingnames(self):
        return self._settings.keys()
    
    def settings(self):
        return self._settings.values()
    
    def groups(self):
        return self._groups.keys()
    
    def in_group(self, group):
        return self._groups[group]



class Setting(object):
    @property
    def name(self):
        raise NotImplementedError('The name attribute of this setting %s is not implemented'%self)
    @property
    def group(self):
        raise NotImplementedError('The group attribute of this setting %s is not implemented'%self)
    @property
    def description(self):
        raise NotImplementedError('The description attribute of this setting %s is not implemented'%self)
    
    def decode(self, value):
        "Converts the value from the db to a python object"
        return value
    def encode(self, value):
        "Converts the python value to the string to be stored in the database, or returns None for an invalid value"
        return value

    def default(self):
        """The default value for a setting.
        This is used in the following cases:
        * when requesting a setting:
          - if setting does not exist in database (or error in unpickling), default is returned
        * when saving a setting:
          - if the new setting equals the default, nothing is stored in the database (old settings are removed)
          """
        return None

    def formfields(self, value):
        """Returns a dict of django form fields that can be used to edit this setting.
        """
        raise NotImplementedError('The formfields method of this setting %s is not implemented'%self)

    def value_from_form_data(self, value):
        """Returns a dict of django form fields that can be used to edit this setting.
        """
        raise NotImplementedError('The value_from_form_data method of this setting %s is not implemented'%self)



class PickledSetting(Setting):
    def encode(self, value):
        pickled = pickle.dumps(value)
        return base64.encodestring(pickled)
    def decode(self, value):
        pickled = base64.decodestring(value)
        try:
            return pickle.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return an empty string (Though this will cause a delete for the setting!).
        except:
            return None


