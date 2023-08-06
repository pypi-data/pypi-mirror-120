import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _('Create a default superuser account')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **options):
        logger = logging.getLogger('django')
        email = settings.DEFAULT_ADMIN_EMAIL
        password = settings.DEFAULT_ADMIN_PASSWORD
        first_name = settings.DEFAULT_ADMIN_FIRST_NAME
        last_name = settings.DEFAULT_ADMIN_LAST_NAME

        try:
            if self.UserModel.objects.filter(email=email).exists():
                self.stderr.write(_('Superuser already exists.'))
            else:
                user = self.UserModel.objects.create_superuser(
                    email=email,
                    password=password,
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                self.stdout.write(_('Superuser is successfully created.'))
        except IntegrityError as error:
            logger.warning("DB Error Thrown %s" % error)
