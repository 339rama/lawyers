from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
import uuid

from users.models import *
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings


def SendMail(sender, instance, created, **kwargs):
    if not instance.is_active:
        uuid = instance.uuid
        email = instance.email
        message = 'Потвердите свою регистрацию  {0}/user/confirm/{1}'.format(settings.ALLOWED_HOSTS[0], uuid)
        send_mail('Confirm your email', message,
                'samosvalom@gmail.com', [email], fail_silently=False)
    else:
        pass


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, help_text=_('Email address'))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, verbose_name='Группы')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


post_save.connect(SendMail, sender=CustomUser)
