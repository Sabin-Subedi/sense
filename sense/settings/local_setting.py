from sense.settings.base_setting import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sense_db",
        "HOST": "127.0.0.1",
        "USER": "sense",
        "PORT": "5434",
        "PASSWORD": "sense_123",
    }
}
