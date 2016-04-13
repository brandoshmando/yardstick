from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class BaseAccount(models.Model):
    unique_identifier = models.CharField(_('unique_identifier'), max_length=254, unique=True, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                               on_delete=models.SET_NULL)
    organization_pk = models.PositiveIntegerField()
    organization_id = GenericForeignKey('content_type', 'organization_pk')
    user_pk = models.PositiveIntegerField()
    user_id = GenericForeignKey('content_type', 'user_pk')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        unique_together = ('organization_pk', 'user_pk')


class Manager(BaseAccount):
    pass


class Administrator(BaseAccount):
    pass


class Arbiter(BaseAccount):
    pass


class Subject(BaseAccount):
    pass
