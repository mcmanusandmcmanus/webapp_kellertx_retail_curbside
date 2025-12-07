from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ["django_extensions"]  # type: ignore

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use local channel layer for dev if Redis unavailable
if env.bool("USE_INMEMORY_CHANNEL_LAYER", default=False):  # type: ignore
    CHANNEL_LAYERS["default"] = {  # type: ignore
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
