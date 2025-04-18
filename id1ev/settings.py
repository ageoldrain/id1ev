import os
from decouple import config
import dj_database_url

# ──────────────────────────────────────────────────────────────────────────────
# BASE_DIR: two levels up from this file → project root
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ──────────────────────────────────────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='8093711393089')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ──────────────────────────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# ──────────────────────────────────────────────────────────────────────────────
# oTree session configs
# ──────────────────────────────────────────────────────────────────────────────
SESSION_CONFIGS = [
    dict(
        name='Curiosity',
        app_sequence=['coin_flip'],
        num_demo_participants=20,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    doc="",
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ──────────────────────────────────────────────────────────────────────────────
# INTERNATIONALIZATION & CURRENCY
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

# ──────────────────────────────────────────────────────────────────────────────
# ROOMS (participant labels)
# ──────────────────────────────────────────────────────────────────────────────
ROOMS = [
    dict(
        name='infodemand',
        display_name='Experiment on Curiosity and Demand for Information',
        participant_label_file=os.path.join(BASE_DIR, '_rooms', 'infodemand.txt'),
    ),
    dict(
        name='live_demo',
        display_name='Room for live demo (no participant labels)',
    ),
]

# ──────────────────────────────────────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────────────────────────────────────
ADMIN_USERNAME = config('OTREE_ADMIN_USERNAME', default='admin')
ADMIN_PASSWORD = config('OTREE_ADMIN_PASSWORD', default=None)

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# ──────────────────────────────────────────────────────────────────────────────
# APPLICATION DEFINITION
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'otree',
    'coin_flip',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # for serving static files on Heroku
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'id1ev.urls'
WSGI_APPLICATION = 'id1ev.wsgi.application'

# ──────────────────────────────────────────────────────────────────────────────
# STATIC FILES
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
