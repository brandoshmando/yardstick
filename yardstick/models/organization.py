from django.db import models

from yardstick.models import AuthUser

class OrganizationManager(models.Manager):
    def create_account(self, name, unique_identifier, auth_data):
        organization = Organization.objects.create(
            name=name
        )

        try:
            auth_user = AuthUser.objects.get(email=auth_data['email'])
        except AuthUser.DoesNotExist:
            auth_user = AuthUser.objects.create_user(**auth_data)

        from yardstick.models import Manager
        Manager.objects.create(
            organization_id=organization,
            user=auth_user,
            unique_identifier=unique_identifier
        )

        return organization

class Organization(models.Model):
    name = models.CharField(max_length=56)
    created_at = models.DateTimeField(auto_now=True)

    objects = OrganizationManager()
