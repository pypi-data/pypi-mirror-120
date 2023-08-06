from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField('e-mail address', unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        default_related_name = 'users'

    def __str__(self):
        return self.email

    @cached_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
