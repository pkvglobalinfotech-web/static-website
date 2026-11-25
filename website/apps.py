from django.apps import AppConfig
from django.db.models.signals import post_migrate
import logging

logger = logging.getLogger(__name__)


def auto_seed_data(sender, **kwargs):
    """
    Auto-seed default company settings, products, and services if database is unseeded.
    Runs on deployment when `manage.py migrate` finishes.
    """
    import sys
    if 'test' in sys.argv:
        return

    try:
        from website.models import Project, Service
        from django.core.management import call_command

        if not Project.objects.exists() or not Service.objects.exists():
            call_command('seed_sample', '--create')
    except Exception as e:
        logger.warning("Auto-seed on migrate check skipped: %s", e)


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        post_migrate.connect(auto_seed_data, sender=self)

