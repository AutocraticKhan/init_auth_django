from django.db import models

# Assuming User model is in 'authentication' app and Business/Location in 'listings' app
from authentication.models import User
from listings.models import Business, Location

class Event(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='events')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_events')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, blank=True, null=True)
    venue_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    ticket_url = models.URLField(max_length=200, blank=True, null=True)
    price_info = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True) # Consider using choices or FK to Category if needed
    status = models.CharField(max_length=50, default='active') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_offers')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    terms_conditions = models.TextField(blank=True, null=True)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    offer_url = models.URLField(max_length=200, blank=True, null=True)
    discount_type = models.CharField(max_length=50, blank=True, null=True) # e.g., 'percentage', 'fixed_amount'
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, default='active') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FeaturedListing(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='featured_placements')
    start_date = models.DateField()
    end_date = models.DateField()
    level = models.CharField(max_length=50, blank=True, null=True) # e.g., 'premium', 'standard'
    placement_area = models.CharField(max_length=100, blank=True, null=True) # e.g., 'homepage', 'category_page'
    payment_id = models.CharField(max_length=255, blank=True, null=True) # Link to a payment record if applicable
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured: Business ID {self.business_id} ({self.start_date} to {self.end_date})"
