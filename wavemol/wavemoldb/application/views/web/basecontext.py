import settings
from application import models

def context():
    return {
        "wavemol_version" : settings.VERSION,
        "database_name" : settings.NAME
    }
