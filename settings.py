# settings.py  ← at repo root, next to manage.py
from id1ev.settings import *



ROOMS = [
    {
        'name': '29May2025',
        'display_name': 'Live room',
        # optional: path relative to project root
        # participant_label_file must exist if you include it
        'participant_label_file': 'rooms/live_labels.txt',
    },
]
