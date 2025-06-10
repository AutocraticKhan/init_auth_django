from django.db import models
from django.utils.text import slugify
from django.db.models import JSONField
from listings.models import Business, Category # Import models from listings app

class AttributeType(models.Model):
    VALUE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('url', 'URL'),
        ('date', 'Date'),
        ('enum', 'Enum'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    value_type = models.CharField(max_length=10, choices=VALUE_TYPE_CHOICES, default='text')
    allowed_values = models.JSONField(blank=True, null=True) # For 'enum' type
    applicable_categories = models.ManyToManyField(Category, blank=True, related_name='attribute_types')
    icon = models.CharField(max_length=100, blank=True, null=True)
    is_filterable = models.BooleanField(default=False)
    is_searchable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ListingAttributeValue(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='attribute_values')
    attribute_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE, related_name='listing_values')
    value_text = models.TextField(blank=True, null=True)
    value_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_boolean = models.BooleanField(null=True, blank=True)
    value_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'attribute_type')

    def __str__(self):
        return f"{self.business.name} - {self.attribute_type.name}: {self.get_value()}"

    def get_value(self):
        if self.attribute_type.value_type == 'text' or self.attribute_type.value_type == 'url' or self.attribute_type.value_type == 'enum':
            return self.value_text
        elif self.attribute_type.value_type == 'number':
            return self.value_number
        elif self.attribute_type.value_type == 'boolean':
            return self.value_boolean
        elif self.attribute_type.value_type == 'date':
            return self.value_date
        return None
