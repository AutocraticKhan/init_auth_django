from django.contrib import admin
from .models import (
    Category, Location, Business, OperatingHours, Amenity, Tag, Photo,
    PaymentMethod, AccessibilityFeature, BusinessSecondaryCategory,
    BusinessTag, BusinessAmenity, BusinessPaymentMethod,
    BusinessAccessibilityFeature, PhotoTag
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Business)
admin.site.register(OperatingHours)
admin.site.register(Amenity)
admin.site.register(Tag)
admin.site.register(Photo)
admin.site.register(PaymentMethod)
admin.site.register(AccessibilityFeature)
admin.site.register(BusinessSecondaryCategory)
admin.site.register(BusinessTag)
admin.site.register(BusinessAmenity)
admin.site.register(BusinessPaymentMethod)
admin.site.register(BusinessAccessibilityFeature)
admin.site.register(PhotoTag)
