

class PreferencesManager(object):
    def __init__(self, model_config):
        self.model_config = model_config

    def contribute_to_class(self, cls, name, **kwargs):
        if not hasattr(cls, name):
            setattr(cls, name, PreferencesDescriptor(self.model_config))
        else:
            getattr(cls, name).add_model_config(self.model_config)


class PermissionsManager(object):
    def __init__(self, model_config):
        self.model_config = model_config

    def contribute_to_class(self, cls, name, **kwargs):
        if not hasattr(cls, name):
            setattr(cls, name, PermissionsDescriptor(self.model_config))
        else:
            getattr(cls, name).add_model_config(self.model_config)


class DescriptorBase(object):
    def __init__(self, model_config):
        self.model_configs = {}
        self.add_model_config(model_config)

    def add_model_config(self, model_config):
        self.model_configs[model_config.section.name] = model_config

    def remove_model_config(self, model_config):
        del self.model_configs[model_config.section.name]

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        return self.get_instance(instance)

    def get_instance(self, instance):
        raise NotImplementedError


class PreferencesDescriptor(DescriptorBase):
    def get_instance(self, instance):
        pass


class PermissionsDescriptor(DescriptorBase):
    def get_instance(self, instance):
        pass
