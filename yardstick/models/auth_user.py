from __future__ import unicode_literals

import pgcrypto
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.contenttypes.fields import GenericRelation

class AuthUserManager(BaseUserManager):
    def _create_user(self, password, is_staff, is_superuser, email=None, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email) if email else email
        user = self.model(
                        email=email,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        last_login=now,
                        date_joined=now,
                        **extra_fields
                    )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(password, False, False, email,  **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return self._create_user(password, True, True, email, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True, blank=True, null=True)
    first_name = pgcrypto.EncryptedCharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = pgcrypto.EncryptedCharField(_('first name'), max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
