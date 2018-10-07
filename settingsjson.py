import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Settings'},
    {'type': 'bool',
     'title': 'Datenbank',
     'desc': 'Upload zu Adafruit.io',
     'section': 'grillen',
     'key': 'datenbank'},
    {'type': 'options',
     'title': 'Zeit Datenbank',
     'desc': 'Wert, wie oft in die Datenbank geschrieben werden soll.',
     'section': 'grillen',
     'key': 'datenbank2',
     'options': ['10 Sekunden', '30 Sekunden', '1 Minute']},
    {'type': 'bool',
     'title': 'Licht',
     'desc': 'Visuelle unterstuetzung der Grilltemperatur.',
     'section': 'grillen',
     'key': 'led'}
    ])
