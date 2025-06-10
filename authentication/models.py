from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True) # Consider using choices for roles
    email_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="authentication_user_set",
        related_query_name="authentication_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="authentication_user_set",
        related_query_name="authentication_user",
    )

    def __str__(self):
        return self.username

class ClaimRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey('listings.Business', on_delete=models.CASCADE)
    status = models.CharField(max_length=50) # Consider using choices for status
    proof_documentation_url = models.URLField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claim_requests_reviewed')

    def __str__(self):
        return f"Claim Request by {self.user.username} for Business ID {self.business_id}" # business_id will be available after listings app is created
