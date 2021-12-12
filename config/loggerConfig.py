logger_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'request': {
            'format': '[%(asctime)s] %(ip)s:%(user)s %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'app_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'logs/app.log'
        },
        'web_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'request',
            'filename': 'logs/web.log'
        },
        'db_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'logs/db.log'
        }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'app_file']
    },
    'loggers': {
        'web_logger': {
            'level': 'INFO',
            'handlers': ['web_file']
        },
        'default': {
            'level': 'INFO',
            'handlers': ['app_file', 'console', 'wsgi']
        },
        'db_logger': {
            'level': 'INFO',
            'handlers': ['db_file']
        }
    },
}
