from django.apps import AppConfig


class HotelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hotel"

    def ready(self):
        from . import signals
