from utils import get_config

CONFIG = get_config()

broker_url = CONFIG["celery"]["CELERY_BROKER_URL"]
result_backend = CONFIG["celery"]["CELERY_RESULT_BACKEND"]
result_expires = CONFIG.getint("celery", "CELERY_RESULT_EXPIRES")