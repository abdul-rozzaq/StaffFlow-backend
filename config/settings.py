from datetime import timedelta
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-c^^#r1_io2bbj+iy=bc5t7*vngl)_^=6nk0)$napacv3x50v9-"

DEBUG = env.bool("DEBUG", default=False)
BOT_TOKEN = env.str("BOT_TOKEN")

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Tashqi
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_yasg",
    "django_filters",
    # Ichki
    "project",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "project.middleware.CompanyMiddleware",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "project.paginations.PageSizePagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "PAGE_SIZE": 2,
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic",
        },
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    },
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
    "UILayout": "SwaggerUI",
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.41.1/",
    "SWAGGER_UI_SETTINGS": {
        "theme": "dark",  # Qora rejimni tanlash
    },
}


WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = "static_files"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "project.Employee"
