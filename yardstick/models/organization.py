from django.db import models

from yardstick.models import AuthUser

class OrganizationManager(models.Manager):
    def create_account(self, name, unique_identifier, first_name, last_name, email, password):
        organization = Organization.objects.create(
            name=name
        )

        try:
            auth_user = AuthUser.objects.get(email=email)
        except AuthUser.DoesNotExist:
            auth_user = AuthUser.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password
                        )

        from yardstick.models import Manager
        mgr = Manager.objects.create(
            organization_id=organization,
            user=auth_user,
            unique_identifier=unique_identifier
        )

        return organization, mgr, auth_user

class Organization(models.Model):
    name = models.CharField(max_length=56)
    created_at = models.DateTimeField(auto_now=True)

    objects = OrganizationManager()
