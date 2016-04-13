from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from yardstick.models import Manager, Administrator, Arbiter, Subject

class Organization(models.Model):
    name = models.CharField(max_length=56)
    created_at = models.DateTimeField(auto_now=True)

    managers = GenericRelation(Manager,
                        object_id_field='organization_pk'
                     )
    administrators = GenericRelation(Administrator,
                        object_id_field='organization_pk'
                     )
    arbiters = GenericRelation(Arbiter,
                        object_id_field='organization_pk'
                     )
    subjects = GenericRelation(Arbiter,
                        object_id_field='organization_pk'
                     )
