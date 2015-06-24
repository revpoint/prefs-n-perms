from django.conf.global_settings import *

DEBUG = False # will be False anyway by DjangoTestRunner.
TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    # 'dynamic_preferences.processors.global_preferences',
    # 'dynamic_preferences.processors.user_preferences',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',

    'prefs_n_perms',
    'tests.test_app'
)

ROOT_URLCONF = 'tests.urls'

PREFS_N_PERMS = {
    'REDIS_URL': 'redis://localhost:6379/0',
}

SITE_ID = 1
STATIC_URL = "/static/"
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

PREFS_N_PERMS_USE_TEST_PREFERENCES=True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}
TESTING=True
TEST_RUNNER='django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=prefs_n_perms',
]