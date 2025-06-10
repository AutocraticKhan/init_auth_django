from django.db import models
from django.utils.text import slugify
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator

# Assuming a User model exists in an 'authentication' app
from authentication.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    icon = models.CharField(max_length=100, blank=True, null=True)
    level = models.PositiveIntegerField(default=0)
    listing_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DietaryFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
class Location(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    neighbourhood = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"

class Business(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    primary_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='primary_businesses')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    claimed_by_user = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_businesses') # Will uncomment after authentication app is fully set up
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True) # Example: {'facebook': 'url', 'twitter': 'url'}
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    review_count = models.PositiveIntegerField(default=0)
    price_range = models.CharField(max_length=50, blank=True, null=True) # Example: '$', '$$', '$$$'
    is_claimed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending') # Consider using choices
    year_established = models.PositiveIntegerField(null=True, blank=True)
    video_url = models.URLField(max_length=200, blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True) # For simple key-value pairs, more complex in listing_details
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many relationships (defined as separate models below)
    secondary_categories = models.ManyToManyField(Category, related_name='secondary_businesses', blank=True)
    tags = models.ManyToManyField('Tag', related_name='businesses', blank=True)
    amenities = models.ManyToManyField('Amenity', related_name='businesses', blank=True)
    payment_methods = models.ManyToManyField('PaymentMethod', related_name='businesses', blank=True)
    accessibility_features = models.ManyToManyField('AccessibilityFeature', related_name='businesses', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class OperatingHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='operating_hours')
    day_of_week = models.IntegerField() # 0 for Monday, 6 for Sunday
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    is_24_hours = models.BooleanField(default=False)
    specific_date = models.DateField(null=True, blank=True) # For exceptions
    notes = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'day_of_week', 'specific_date') # Ensure unique hours per day/date

    def __str__(self):
        return f"{self.business.name} - Day {self.day_of_week}"

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True) # e.g., 'General', 'Food', 'Service'

    class Meta:
        verbose_name_plural = "Amenities / Features"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_photos')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200, blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    source = models.CharField(max_length=100, blank=True, null=True) # e.g., 'user_upload', 'google_places'
    status = models.CharField(max_length=50, default='active') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many relationship (defined as separate model below)
    tags = models.ManyToManyField(Tag, related_name='photos', blank=True)

    def __str__(self):
        return f"Photo for {self.business.name}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class AccessibilityFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Join Tables (explicitly defined for clarity, Django often handles these implicitly)
class BusinessSecondaryCategory(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('business', 'category')

class BusinessTag(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('business', 'tag')

class BusinessAmenity(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('business', 'amenity')

class BusinessPaymentMethod(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('business', 'payment_method')

class BusinessAccessibilityFeature(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    accessibility_feature = models.ForeignKey(AccessibilityFeature, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('business', 'accessibility_feature')

class PhotoTag(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('photo', 'tag')

class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=50, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.business.name}"

class Menu(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} Menu for {self.business.name}"

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    photo_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    dietary_flags = models.ManyToManyField('DietaryFlag', related_name='menu_items', blank=True)

    def __str__(self):
        return self.name

class MenuItemDietaryFlag(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    dietary_flag = models.ForeignKey(DietaryFlag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu_item', 'dietary_flag')

    def __str__(self):
        return f"{self.menu_item.name} - {self.dietary_flag.name}"
