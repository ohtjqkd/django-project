from .base import *
import sys

for key, value in json.loads(open(SECRET_PATH_FILE).read())['django']['production'].items():
    setattr(sys.modules[__name__], key, value)

DEBUG = False

ALLOWED_HOSTS += ['*']