from django.conf import settings as django_settings
import settings as test_settings

if not django_settings.configured:
    django_settings.configure(test_settings)
