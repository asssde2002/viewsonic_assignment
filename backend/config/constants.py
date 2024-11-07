from utils import get_config

CONFIG = get_config()
DATABASES = CONFIG["databases"]
DATABASE_URL = f"postgresql://{DATABASES["USER"]}:{DATABASES["PASSWORD"]}@{DATABASES["HOST"]}:{DATABASES["PORT"]}/{DATABASES["NAME"]}"