from .base import *
import sys

for key, value in json.loads(open(SECRET_PATH_FILE).read())['django']['development'].items():
    setattr(sys.modules[__name__], key, value)

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
