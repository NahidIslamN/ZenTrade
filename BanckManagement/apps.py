from django.apps import AppConfig


import threading




class BanckmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BanckManagement'

    # def ready(self):
    #     from .tasks import run_schedule
    #     threading.Thread(target=run_schedule, daemon=False).start()





