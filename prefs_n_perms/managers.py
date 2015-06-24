import collections


# Base

class BaseInstanceDict(collections.Mapping):
    def __init__(self, descriptor, instance):
        self.descriptor = descriptor
        self.instance = instance

    def __repr__(self):
        return repr(dict(self))

    def __iter__(self):
        return self.descriptor.model_configs.iterkeys()

    def __len__(self):
        return len(self.descriptor.model_configs)

    def __getitem__(self, item):
        model_config = self.descriptor.model_configs[item]
        section = model_config.section
        kwargs = model_config.get_kwargs(self.instance)
        return self.get_value(section, kwargs)

    def get_value(self, section, kwargs):
        raise NotImplementedError


class DescriptorBase(object):
    instance_dict = None

    def __init__(self, model_config):
        self.check()
        self.model_configs = {}
        self.add_model_config(model_config)

    def check(self):
        if self.instance_dict is None:
            raise NotImplementedError
        if not issubclass(self.instance_dict, BaseInstanceDict):
            raise ValueError

    def add_model_config(self, model_config):
        self.model_configs[model_config.section.name] = model_config

    def remove_model_config(self, model_config):
        del self.model_configs[model_config.section.name]

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        return self.instance_dict(self, instance)


class ManagerBase(object):
    descriptor = None

    def __init__(self, model_config):
        self.check()
        self.model_config = model_config

    def check(self):
        if self.descriptor is None:
            raise NotImplementedError
        if not issubclass(self.descriptor, DescriptorBase):
            raise ValueError

    def contribute_to_class(self, cls, name, **kwargs):
        if not hasattr(cls, name):
            setattr(cls, name, self.descriptor(self.model_config))
        else:
            getattr(cls, name).add_model_config(self.model_config)


# Preferences

class PreferencesInstanceDict(BaseInstanceDict):
    def get_value(self, section, kwargs):
        return section.get_preferences(**kwargs)


class PreferencesDescriptor(DescriptorBase):
    instance_dict = PreferencesInstanceDict


class PreferencesManager(ManagerBase):
    descriptor = PreferencesDescriptor


# Permissions

class PermissionsInstanceDict(BaseInstanceDict):
    def get_value(self, section, kwargs):
        return section.get_permissions(**kwargs)


class PermissionsDescriptor(DescriptorBase):
    instance_dict = PermissionsInstanceDict


class PermissionsManager(ManagerBase):
    descriptor = PermissionsDescriptor
