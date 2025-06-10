from django.contrib import admin
from .models import Event, Offer, FeaturedListing

# Register your models here.
admin.site.register(Event)
admin.site.register(Offer)
admin.site.register(FeaturedListing)
