from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

UserModel = get_user_model()


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        try:
            superuser = UserModel.objects.get(
                username=settings.DJANGO_SUPERUSER_USERNAME)
            if superuser is None:
                superuser = UserModel.objects.create_superuser(
                    username=settings.DJANGO_SUPERUSER_USERNAME, password=settings.DJANGO_SUPERUSER_PASSWORD)
            application = Application.objects.get(
                name=settings.DJANGO_CLIENT_NAME)
            if application is None:
                Application.objects.create(name=settings.DJANGO_CLIENT_NAME,
                                           client_id=settings.DJANGO_UID, client_secret=settings.DJANGO_SECRET, client_type=settings.DJANGO_CLIENT_TYPE, authorization_grant_type=settings.DJANGO_GRANT_AUTHORIZATION,  user=superuser)
        except Exception as e:
            print("error", str(e))

        self.stdout.write(self.style.SUCCESS("All Done !"))
