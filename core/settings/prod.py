from core.settings.common import *

DEBUG = os.getenv("DEBUG", "False").lower == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOST", "127.0.0.1:8000").split(",")
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
