from __future__ import unicode_literals

import pgcrypto
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class AuthUserManager(BaseUserManager):
    def _create_user(self, password, is_staff, is_superuser, email=None, unique_identifier=None, **extra_fields):
        now = timezone.now()
        if not (email or unique_identifier):
            raise ValueError('Email or Unique Identifier is required')
        email = self.normalize_email(email) if email else email
        user = self.model(
                        email=email,
                        unique_identifier=unique_identifier,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        last_login=now,
                        date_joined=now,
                        **extra_fields
                    )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, unique_identifier=None, password=None, **extra_fields):
        return self._create_user(password, False, False, email, unique_identifier, **extra_fields)

    def create_superuser(self, email=None, unique_identifier=None, password=None, **extra_fields):
        return self._create_user(password, True, True, email, unique_identifier, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True, blank=True, null=True)
    unique_identifier = models.CharField(_('unique_identifier'), max_length=254, unique=True, blank=True, null=True)
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
