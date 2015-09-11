from django.core.management.base import BaseCommand
from prefs_n_perms import section_registry


class Command(BaseCommand):
    help = 'Restore all default preferences to Redis DB.'

    def handle(self, *args, **options):
        for section, config in section_registry.iteritems():
            self.stdout.write('Setting preferences for: %s' % section)
            if config.default_preferences:
                config.section.get_preferences().update_global(config.default_preferences)
            if config.available_permissions:
                config.section.get_permissions().update_available(config.available_permissions)
