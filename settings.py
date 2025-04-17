

import dj_database_url
from os import environ

DATABASES = {
    'default': dj_database_url.config(
        default=environ.get('DATABASE_URL')
    )
}

SESSION_CONFIGS = [
    dict(
        name='Curiosity', app_sequence=['coin_flip'], num_demo_participants=20
    ),
]




# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)
# Payment and earnings strcuture

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='infodemand',
        display_name='Experiment on Curiosity and Demand for Information',
        participant_label_file='_rooms/infodemand.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]

# For displaying winnings
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOT_URLCONF = 'csrfprotect.urls'

SECRET_KEY = '8093711393089'

INSTALLED_APPS = ['otree',
                     'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles']
    'django.contrib.staticfiles']

