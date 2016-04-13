from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from yardstick.models import Organization, AuthUser

class BaseAccount(models.Model):
    unique_identifier = models.CharField(_('unique_identifier'), max_length=254, unique=True, blank=True, null=True)
    user = models.ForeignKey(AuthUser,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='%(class)ss'
           )
    organization_id = models.ForeignKey(Organization,
                        null=True,
                        blank=True,
                        on_delete=models.CASCADE,
                        related_name='%(class)ss'
                      )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        unique_together = ('organization_id', 'user')


class Manager(BaseAccount):
    pass


class Administrator(BaseAccount):
    pass


class Arbiter(BaseAccount):
    pass


class Subject(BaseAccount):
    pass
