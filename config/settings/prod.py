from .base import *  # noqa

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # type: ignore
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)  # type: ignore
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)  # type: ignore

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
