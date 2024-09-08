"""
Django settings for remorex project.
"""

import os
from pathlib import Path

import dj_database_url
import pymysql
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default=os.getenv("SECRET_KEY"),
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = "zonevs.eu" not in os.environ.get("VS_LOOPBACK_HOST", "")

šALLOWED_HOSTS = [
    "[fe80::acc8:46ff:fea7:db6e]",
    "localhost",
    "127.1.151.231",
    "127.0.0.1",
    "0.0.0.0",
    "185.43.106.116",
    "remoreks.ee",
    "www.remoreks.ee",
]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "accounts",
    "yard",
    "posts",
    "compressor",
    "storages",
    "coverage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "yard.middleware.CustomLocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "remorex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "remorex.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        os.environ.get("DATABASE_URI"),
        default=os.getenv("DATABASE_URI"),
        conn_max_age=600,
    )
}

DATABASES["default"].update(
    {"OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"}}
)

pymysql.version_info = (1, 4, 6, "final", 0)
pymysql.install_as_MySQLdb()

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "et"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# https://flowbite.com/docs/getting-started/django/
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

COMPRESS_ROOT = BASE_DIR / "static"
COMPRESS_ENABLED = True

if not DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# AWS settings
USE_S3 = os.getenv("USE_S3") == "TRUE"

if os.getenv("USE_S3"):
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None

    # http://bucket-name.s3-website.Region.amazonaws.com/object-name
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.eu-north-1.amazonaws.com"

    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    DEFAULT_FILE_STORAGE = (
        "storages.backends.s3boto3.S3Boto3Storage"  # /remorex/storage_backends.py
    )

LANGUAGES = (
    ("et", _("Estonian")),
    ("ru", _("Russian")),
    ("en", _("English")),
    ("de", _("German")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = "remoreks@remoreks.ee"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USE_TLS = True if DEBUG else False
EMAIL_TIMEOUT = 60
