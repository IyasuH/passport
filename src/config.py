# config.py
DATABASE_CONFIG = {
    'connections': {
        'default': 'sqlite://../passport_copy.db',  # Adjust to your database URI
    },
    'apps': {
        'models': {
            'models': ['models.identity'],
            'default_connection': 'default',
        }
    }
}