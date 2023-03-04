import os

from config.settings import settings

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres.db,
        "USER": settings.postgres.user,
        "PASSWORD": settings.postgres.password,
        "HOST": settings.postgres.host,
        "PORT": settings.postgres.port,
        "OPTIONS": {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            "options": "-c search_path=public,content"
        },
    }
}
