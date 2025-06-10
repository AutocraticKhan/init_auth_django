from django.db import models
from django.db.models import JSONField

# Assuming User model is in 'authentication' app and Category in 'listings' app
from authentication.models import User
from listings.models import Category

class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_logs')
    session_id = models.CharField(max_length=255, blank=True, null=True) # For tracking anonymous sessions
    query_text = models.CharField(max_length=255)
    category_filter = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location_filter = models.CharField(max_length=255, blank=True, null=True)
    applied_filters = models.JSONField(blank=True, null=True) # Example: {'price_range': '$$', 'amenities': ['wifi']}
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    result_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search: '{self.query_text}' at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
