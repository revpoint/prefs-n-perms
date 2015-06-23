from django.apps import AppConfig


class PrefsNPermsConfig(AppConfig):
    name = 'prefs_n_perms'
    verbose_name = 'Preferences and Permissions'

    def ready(self):
        # Loop through each app and look for preferences registry
        pass
