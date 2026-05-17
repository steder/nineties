"""
Django settings for the Librarian service.

Environment is read via django-environ; see .env.example at the repo root.
This project is a self-hosted service, so we expect a real Postgres in dev
and prod. SQLite is NOT supported.

All env vars and their defaults are declared in the Env() constructor below
to keep the call sites tidy and make the type-checker happy.
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent

env = environ.Env(
    # Optional with defaults. DJANGO_SECRET_KEY and DATABASE_URL are required
    # and read directly via env('KEY') — not in the scheme — so a missing
    # value raises ImproperlyConfigured with a clear error.
    DJANGO_DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    TZ=(str, "UTC"),
    LOG_LEVEL=(str, "INFO"),
    QCLUSTER_WORKERS=(int, 2),
    VOICE_ADAPTER=(str, "voice.alexa.AlexaVoiceAdapter"),
    MEDIA_BACKEND=(str, "media.abs.AudioBookShelfBackend"),
    AUDIOBOOKSHELF_URL=(str, "http://localhost:13378"),
    AUDIOBOOKSHELF_TOKEN=(str, ""),
    ALEXA_SKILL_ID=(str, ""),
)
# Load .env from the repo root if present (dev convenience; never in container).
environ.Env.read_env(REPO_ROOT / ".env")

# --- Core ---

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# --- Apps ---

INSTALLED_APPS = [
    # Django contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third-party
    "django_q",
    # Local apps (kept in dependency-friendly order: policy is pure, no FKs;
    # catalog has Item/Tag; kids depends on catalog tags conceptually;
    # loans depends on kids + catalog; voice/media are adapters)
    "policy",
    "catalog",
    "kids",
    "loans",
    "voice",
    "media",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "librarian.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "librarian.wsgi.application"
ASGI_APPLICATION = "librarian.asgi.application"

# --- Database ---
# Real Postgres in all environments. pgvector extension created via migration.

DATABASES = {
    "default": {
        **env.db_url("DATABASE_URL"),
        "ATOMIC_REQUESTS": True,
    },
}

# --- Auth ---
# Parents use Django's built-in User. Kids are NOT auth users — they're
# identified by their voice-adapter device IDs (see `kids` app).

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/admin/login/"

# --- i18n / TZ ---

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TZ")
USE_I18N = True
USE_TZ = True

# --- Static / templates ---

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- Defaults ---

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Background jobs (django-q2) ---

Q_CLUSTER = {
    "name": "librarian",
    "workers": env("QCLUSTER_WORKERS"),
    "timeout": 60,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",  # use the Django ORM as the broker (no Redis needed)
    "catch_up": False,
}

# --- Logging ---
# Privacy: never log child PII. Kid identifiers in logs are internal IDs.
# See requirements/privacy.md.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "concise": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "concise",
        },
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL")},
    "loggers": {
        "django": {"level": "INFO", "propagate": True},
        "librarian": {"level": "DEBUG" if DEBUG else "INFO", "propagate": True},
    },
}

# --- Adapter configuration ---
# Concrete adapter classes resolved at runtime via these dotted paths.
# Keep core code free of direct imports of these — go through the abstractions.

VOICE_ADAPTER = env("VOICE_ADAPTER")
MEDIA_BACKEND = env("MEDIA_BACKEND")

# Media backend (AudioBookShelf) configuration.
AUDIOBOOKSHELF_URL = env("AUDIOBOOKSHELF_URL")
AUDIOBOOKSHELF_TOKEN = env("AUDIOBOOKSHELF_TOKEN")

# Alexa skill configuration.
ALEXA_SKILL_ID = env("ALEXA_SKILL_ID")
