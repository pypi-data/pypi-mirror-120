from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailauthConfig(AppConfig):
    name = 'mailauth'
    verbose_name = _('Mail Auth')
