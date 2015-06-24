from prefs_n_perms.managers import PreferencesManager, PermissionsManager


class BaseConfig(object):
    pass


class SectionConfig(BaseConfig):
    tiers = ()
    default_preferences = {}
    available_permissions = ()

    def __init__(self, section, model_dict):
        self.section = section
        self.model_dict = model_dict
        self.initialize()

    def initialize(self):
        # set up initial preferences and permissions
        pass


class ModelConfig(BaseConfig):
    model = None

    def __init__(self, section_config, tier):
        if self.model is None:
            raise NotImplementedError
        self.section_config = section_config
        self.section = section_config.section
        self.tier = tier
        self.attach_to_model()

    def __del__(self):
        self.detach_from_model()

    def get_kwargs(self, obj):
        raise NotImplementedError

    def attach_to_model(self):
        if self.section.has_preferences():
            self.model.add_to_class('preferences', PreferencesManager(self))
        if self.section.has_permissions():
            self.model.add_to_class('permissions', PermissionsManager(self))

    def detach_from_model(self):
        if hasattr(self.model, 'preferences'):
            self.model.preferences.remove_model_config(self)
        if hasattr(self.model, 'permissions'):
            self.model.permissions.remove_model_config(self)
