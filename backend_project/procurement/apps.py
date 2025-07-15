from django.apps import AppConfig

class ProcurementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'procurement'

    def ready(self):
        from django.contrib.auth.models import Group
        roles = ['Administrator', 'Supplier', 'Manufacturer', 'Procurement Officer']
        for role in roles:
            Group.objects.get_or_create(name=role)
