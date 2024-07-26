from dotenv import load_dotenv
from __future__ import absolute_import, unicode_literals
from core.celery import app as celery_app
import os


load_dotenv()

__all__ = ("celery_app")

GJANGO_ENV = os.getenv("GJANGO_ENV", "dev")

if GJANGO_ENV == "prod":
    from prod import *
else:
    from dev import *
