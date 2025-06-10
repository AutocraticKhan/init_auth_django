from django.db import models
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator

# Assuming User model is in 'authentication' app and Business/Photo in 'listings' app
from authentication.models import User
from listings.models import Business, Photo

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    aspect_ratings = models.JSONField(blank=True, null=True) # Example: {'service': 4.5, 'food': 5.0}
    helpful_count = models.PositiveIntegerField(default=0)
    reply_to_review = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    status = models.CharField(max_length=50, default='published') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for Business ID {self.business_id} by User ID {self.user_id}" # Will update after FKs are added

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'business')

    def __str__(self):
        return f"Bookmark by User ID {self.user_id} for Business ID {self.business_id}" # Will update after FKs are added

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    status = models.CharField(max_length=50, default='open') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question for Business ID {self.business_id} by User ID {self.user_id}" # Will update after FKs are added

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_owner_answer = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, default='published') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to Question ID {self.question.id} by User ID {self.user_id}" # Will update after FKs are added

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    content_type = models.CharField(max_length=50) # e.g., 'review', 'question', 'answer', 'business', 'photo'
    content_id = models.PositiveIntegerField() # ID of the reported content
    reason_category = models.CharField(max_length=100) # Consider using choices
    reason_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending') # Consider using choices
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_resolved')
    resolution_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report on {self.content_type} ID {self.content_id} by User ID {self.user_id}" # Will update after FKs are added

# Join Table (explicitly defined for clarity)
class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'photo')

    def __str__(self):
        return f"Photo ID {self.photo_id} for Review ID {self.review.id}" # Will update after FKs are added
