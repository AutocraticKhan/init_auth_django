from django.db import models
from django.contrib.auth.models import AbstractUser

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class UserProfile(AbstractUser):
    class UserType(models.TextChoices):
        PATIENT = 'PATIENT', 'Patient'
        PROVIDER = 'PROVIDER', 'Provider'
        FACILITY_ADMIN = 'FACILITY_ADMIN', 'Facility Admin'
        SYSTEM_ADMIN = 'SYSTEM_ADMIN', 'System Admin'

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users'
    )
    is_premium = models.BooleanField(default=False)

    # date_joined and last_login are already part of AbstractUser,
    # but I'll keep them in the description for clarity as per the request.
    # date_joined = models.DateTimeField(auto_now_add=True) # Inherited from AbstractUser
    # last_login = models.DateTimeField(auto_now=True) # Inherited from AbstractUser

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.username
