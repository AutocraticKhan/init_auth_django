from django.contrib import admin
from .models import User, ClaimRequest

# Register your models here.
admin.site.register(User)
admin.site.register(ClaimRequest)
